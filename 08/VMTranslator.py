# =============================================================================
# Description : converts a single VM file (or a series of VM files located in a 
# given directory) to a corresponding asm file (or a series of corresponding 
# asm files).
# 
# Returns 0 even if the conversion failed. The only case in which the script 
# does not returns 0 is when unexpected errors were encountered, for example 
# file open error.
# 
# ------------------------------------------------------------------- Syntaxe : 
# python VMTranslator.py VM_file_path | VM_directory_path
#  
# =========================================== Quotes Ch. 4 "Machine Language" :
# 
# Reminder on the concept of a variable. A variable is a label designating a 
# memory location (= an address). Let V be such a variable, and suppose it is 
# associated with address 23 in memory. In classical programming, the 
# instruction V = 8 would cause the location 23 to contain the value 8.
# 
# Set variable V to 1 :
#	@V		// Put V address (so 23 in the above example) in A.
#	M=1		// Put 1 in the memory slot designated by A (so 23).
# 
# Put the content of variable X in D :
# 	@X
#	D=M
# 
# Analysis of the assembly code corresponding to the VM instruction 
# "push constant 2" :
# We assume that SP (Stack Pointer) refers to address 0, and that SP = RAM[0] = 
# 127. In the end, we see that we correctly obtain RAM[SP] = 2 and SP++ !
#
# // push constant 2
# 			// -------------------------------------------------------- RAM 1 :
# @2		// A = 2
# D=A		// D = A = 2
# @SP		// A = SP address = 0
# A=M		// A = SP = RAM[0] = 127
# 			// -------------------------------------------------------- RAM 2 :
# M=D		// Put D (= 2) into RAM at address 127, so RAM[127]=2
# @SP		// A = SP address = 0
# 			// -------------------------------------------------------- RAM 3 :
# M=M+1		// Increment memory content at address 0 so SP new content = 128 
# 
# ======================================================== Quotes Ch. 7 p. 20 :
# 
# 	Register	Name  	Usage
# 	----------	------	------------------------------------------------------------------- 
# 	RAM[0]		SP		Stack pointer: points to the next topmost location in the stack   
# 	RAM[1]		LCL		Points to the base of the current VM function's local segment 
# 	RAM[2]		ARG		Points to the base of the current VM function 's argument segment 
# 	RAM[3]		THIS	Points to the base of the current this segment (within the heap) 
# 	RAM[4]		THAT	Points to the base of the current that segment (within the heap) 
# 	RAM[5-12]	TEMP	Hold the contents of the temp segment   
# 	RAM[13-15]	(-)		Can be used by the VM implementation as general-purpose registers.
# 
# ============================ Quotes on memory access commands (Ch. 7 p. 10) : 
# There are two memory access commands : 
# . push segment index : push the value of segment[index] onto the stack. 
# . pop segment index : pop the topmost stack item and store its value in 
#		segment[index].
# 
# =============================================================================

import sys
import os
import pathlib
import glob

# ========================================================= Pseudo-constants :

SCRIPT_VERSION = "1.10"

# __ Authorized characters for labels :
LABEL_BEGIN_CHECK = "_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
LABEL_STANDARD_CHECK = LABEL_BEGIN_CHECK + "0123456789"
FUNCTION_NAME_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
FUNCTION_NAME_CHARSET = FUNCTION_NAME_CHARSET + "0123456789_."

ERR_LEVEL = 1
INFO_LEVEL = 2
TRACE_LEVEL = 3
MSGSEP = ", "
VMEXT = ".vm"
ASMEXT = ".asm"
LABELSEP = ":"

# __ Conversion dictionaries :

# Correspondance between a VM segment name (Table 7 Ch. 07 p. 10) and 
# assembler symbols (Table 14 Ch. 07 p. 20) : 
vmSegToASM = {
	"local" : "LCL", 
	# __ See Ch. 07 p. 20-21 : 
	"temp"  : "5", 
	"argument" : "ARG", 
 	"static" : "???", 
 	"constant" : "???", 
 	"this" : "THIS", 
 	"that" : "THAT", 
 	"pointer" : "3"
}

# __ 2.2 + 2.3 : Arithmetic, logical and memory access commands  
# key = command, value = operands number
vmCmdDict = {
	"add"      : 0,
	"sub"      : 0,
	"neg"      : 0,
	"eq"       : 0,  
	"gt"       : 0,
	"lt"       : 0,
	"and"      : 0,
	"or"       : 0,
	"not"      : 0,
	"push"     : 2,
	"pop"      : 2, 
	"label"    : 1, 
	"goto"     : 1, 
	"if-goto"  : 1, 
	"function" : 2, 
	"call"     : 2, 
	"return"   : 0
}

# __ Conversion dictionary for a two-operand VM arithmetic or logical 
# instruction to an assembly operator.
vmToAsmBinaryOpDict = {
	"add" : "+", 
	"sub" : "-", 
	"and" : "&", 
	"or"  : "|"
}

# __ Conversion dictionary for a comparison VM instruction to an assembly jump.
vmCompToAsmDict = {
	"eq"  : "JEQ", 
	"lt"  : "JLT", 
	"gt"  : "JGT"
}

vmToAsmUnaryOpDict = {
	"neg" : "-", 
	"not" : "!"
}

# ================================================================= Functions :

# __ Sends back the label following a function call. We use a dictionary to 
# manage a counter insuring label unicity.
def funcRetLabel(strName):
	strRet = ""
	if strName in vmFncCallDict:
		nCount = vmFncCallDict[strName] + 1		
	else:
		nCount = 1
	strRet = "RETURN_FROM_" + strName + "." + str(nCount)
	vmFncCallDict[strName] = nCount

	return(strRet)

# -----------------------------------------------------------------------------  
# Quote Ch. 08 p. 6 about the VM command 'label c' : "This command labels the 
# current location in the function’s code.  Only labeled locations can be 
# jumped to from other parts of the program.  The label c is an arbitrary 
# string composed of letters, numbers, and the special characters '_', ':', and 
# '.'. The scope of the label is the current function."
# -----------------------------------------------------------------------------  
# Checks a label syntax. Quote Ch. 06 : "A user-deﬁned symbol can be any 
# sequence of letters, digits, underscore (_), dot (.), dollar sign ($), and 
# colon (:) that does not begin with a digit."
def labelCheck(label):
	rc = 0 ; nChar = 0
	for c in label:
		nChar += 1
		if nChar == 1 and not(c in LABEL_BEGIN_CHECK):
			rc = 1
			break
		elif nChar > 1 and not(c in LABEL_STANDARD_CHECK):
			rc = 2
			break	
	return(rc)

# -----------------------------------------------------------------------------  
# Checks a function name syntax. Quote Ch. 08 p. 7 : "The function name is an 
# arbitrary string composed of letters, numbers, and the special characters '_' 
# and '.'. (We expect that a method 'bar' in class 'Foo' in some high-level 
# language will be translated by the language compiler to a VM function named 
# 'Foo.bar')."
# -----------------------------------------------------------------------------  
def functionNameCheck(strName):
	rc = 0 ; nChar = 0
	
	for c in strName:
		nChar += 1
		if not(c in FUNCTION_NAME_CHARSET):
			rc = 1
			break

	return(rc)

# ------------------------------ Adding 'macro-instructions' to factorisation :

# __ MI01 : SP = 256 generalized "REG_NAME = int" :
def MI_initReg(regName, nValue):
	asmCode = "@" + str(nValue) + "\n"
	asmCode = asmCode + "D=A\n"
	asmCode = asmCode + "@" + regName + "\n"
	asmCode = asmCode + "M=D\n"
	return(asmCode)

# __ MI02 : REG = RAM[--SP] (<=> SP = SP - 1 ; REG = RAM[SP]) :
def MI_PreRamToReg(regName):
	asmCode = "@SP\n"
	asmCode = asmCode + "M=M-1\n"
	asmCode = asmCode + "A=M\n"	
	asmCode = asmCode + regName + "=M\n"	
	return(asmCode)

# __ Initialize asle code assembler renvoyé par une fonction :
def initAsmCode(fncName):
	asmCode = ""

	return(asmCode)

# __ Assembler code initialization.
def setAsmHeader(fAsm):
	global g_bBootStrapped
	myself = "setAsmHeader()"

	asmCode = "// " + "=" * 76 + "\n"
	title = "Code created by VMTranslator.py V" + SCRIPT_VERSION
	asmCode = asmCode + "// " + title.center(76) + "\n"
	asmCode = asmCode + "// " + "=" * 76 + "\n\n"
	if g_bBootStrapped:
		asmCode = asmCode + "// -- Bootstrap code :\n"
		asmCode = asmCode + MI_initReg("SP", 256)
		asmCode = asmCode + parseCall("Sys.init", "0")		
	else:
		asmCode = asmCode + "// -- Code without bootstrap...\n"

	fAsm.write(asmCode)

	return

# __ Assembler code finalization. Particularly, we must insert an infinite 
# loop :
def endAsmFile(fAsm):
	myself = "endAsmFile()"

	asmCode = initAsmCode(myself)
	asmCode = asmCode + "// -- Infinite loop at program end :\n"
	asmCode = asmCode + "(ENDPRGM)\n"
	asmCode = asmCode + "@ENDPRGM\n"
	asmCode = asmCode + "0;JMP\n"

	fAsm.write(asmCode)

# __ pop() command generation :
def parsePop(segment, index):
	myself = "parsePop()"

	asmCode = initAsmCode(myself)

	# __ segment exists in vmSegToASM by construction :
	asmSymbol = vmSegToASM[segment]		

	# __ For 'static' segment, see lecture Ch. 07 p. 75 for example :
	# pop static 5 => 	// D = stack.pop (code omitted)
	#					@Foo.5
	# 					M=D 
	if segment == "static":
		asmCode = asmCode + MI_PreRamToReg("D")
		asmCode = asmCode + "@" + g_strNS + "." + index + "\n"	# A = @vm_name.i, example : A = @BasicTest.i
		asmCode = asmCode + "M=D\n"								# R5 = D = RAM[SP]	
	else:
		asmCode = asmCode + "@" + asmSymbol + "\n"		# Example : A = @LCL
		# __ Particular case for the 'temp' and 'pointer' segments. In 
		# vmSegToASM[], the keys of those 2 segments match respectively the  
		# values 5 and 3 and not asm symbols : so, we must use those values as 
		# they are, so A content !
		if segment == "temp" or segment == "pointer":
			asmCode = asmCode + "D=A\n"					# D = A = 5
		else:
			asmCode = asmCode + "D=M\n"					# Example : D = LCL
		asmCode = asmCode + "@" + str(index) + "\n"		# A = index
		asmCode = asmCode + "D=A+D\n"					# Example : D = index + LCL
		asmCode = asmCode + "@" + g_strNS + ".i\n"		# A = @vm_name.i, example : A = @BasicTest.i
		asmCode = asmCode + "M=D\n"						# R5 = D = RAM[SP]
		asmCode = asmCode + "@SP\n"						# A = @SP = 0
		asmCode = asmCode + "M=M-1\n"					# SP = SP - 1
		asmCode = asmCode + "A=M\n"						# A = SP	
		asmCode = asmCode + "D=M\n"						# D = RAM[SP]	
		asmCode = asmCode + "@" + g_strNS + ".i\n"		# A = @vm_name.i, example : A = @BasicTest.i
		asmCode = asmCode + "A=M\n"						# A = SP	
		asmCode = asmCode + "M=D\n"						# D = RAM[SP]	

	return asmCode

# __ Utility function generating the asm code of a pseudo-command like  
# 'push symbol' which serves to pile up a predefined symbol like ARG, LCL, THIS 
# or THAT. 
def pushReg(strSymbol):
	myself = "pushReg()"

	asmCode = initAsmCode(myself)
	asmCode = asmCode + "@" + strSymbol + "\n"
	asmCode = asmCode + "D=M\n"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "A=M\n"
	asmCode = asmCode + "M=D\n"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "M=M+1\n"

	return asmCode

# __ Utility function initially called by parseReturn() and generating the asm 
# code for the restoration of a register ARG, LCL, THIS or THAT using the 
# content of a variable. 
def restoreReg(regName, varName):
	myself = "restoreReg()"

	asmCode = initAsmCode(myself)
	asmCode = asmCode + "@" + varName + "\n"
	asmCode = asmCode + "M=M-1\n"
	asmCode = asmCode + "A=M\n"
	asmCode = asmCode + "D=M\n"
	asmCode = asmCode + "@" + regName + "\n"
	asmCode = asmCode + "M=D\n"

	return asmCode

# __ Generates the asm code of a vm command 'push segment index'. The case of 
# the 'constant' segment is treated separately (see Ch. 07 p. 21 for example).
def parsePush(segment, index):
	myself = "parsePush()"

	asmCode = initAsmCode(myself)

	if segment == "constant":
		asmCode = asmCode + "@" + index + "\n"
		asmCode = asmCode + "D=A\n"
		asmCode = asmCode + "@SP\n"
		asmCode = asmCode + "A=M\n"
		asmCode = asmCode + "M=D\n"
		asmCode = asmCode + "@SP\n"
		asmCode = asmCode + "M=M+1\n"
	elif segment == "static":
		asmCode = asmCode + "@" + g_strNS + "." + index + "\n"	# example : @StaticTest.3
		asmCode = asmCode + "D=M\n"								# D = RAM[A]
		asmCode = asmCode + "@SP\n"								# A = @SP
		asmCode = asmCode + "A=M\n"								# A = SP
		asmCode = asmCode + "M=D\n"								# RAM[SP] = RAM[RAM[A]]
		asmCode = asmCode + "@SP\n"								# A = @SP
		asmCode = asmCode + "M=M+1\n"							# SP = SP + 1
	else:
		# __ segment exists in vmSegToASM because of parseVMLine() :
		asmSymbol = vmSegToASM[segment]
		asmCode = asmCode + "@" + asmSymbol + "\n"				# example : A = @ARG
		# __ Particular case of the 'temp' segment : see parsePop() above.
		if segment == "temp" or segment == "pointer":
			asmCode = asmCode + "D=A\n"					# D = A = 5
		else:
			asmCode = asmCode + "D=M\n"					# Example : D = LCL
		asmCode = asmCode + "@" + str(index) + "\n"		# example : @8
		asmCode = asmCode + "A=D+A\n"					# example : A = ARG + 8
		asmCode = asmCode + "D=M\n"
		asmCode = asmCode + "@SP\n"
		asmCode = asmCode + "A=M\n"
		asmCode = asmCode + "M=D\n"						# example : RAM[SP] = RAM[ARG + 8]
		asmCode = asmCode + "@SP\n"
		asmCode = asmCode + "M=M+1\n"

	return asmCode

# __ Access memory command parsing.
def parseMemAccessCommand(strCmd, segment, index):
	myself = "parseMemAccessCommand()"
	
	if strCmd == "push":
		traceMsg(myself, "push() command processing...")
		asmCode = parsePush(segment, index)
	else:
		traceMsg(myself, "pop() command processing...")
		asmCode = parsePop(segment, index)

	return asmCode

# __ Unary logical or arithmetic command parsing.
def parseUnaryAL(strCmd): 
	myself = "parseUnaryAL()"

	asmCode = initAsmCode(myself)

	traceMsg(myself, "unary command parsing [" + strCmd + "]...")
	
	asmCode = asmCode + "@SP\n"					# A = @SP = 0	
	asmCode = asmCode + "M=M-1\n"				# SP = SP - 1
	asmCode = asmCode + "A=M\n"					# A = SP
	asmOp = vmToAsmUnaryOpDict[strCmd]
	asmCode = asmCode + "M=" + asmOp + "M\n"	# Example : M=-M
	asmCode = asmCode + "@SP\n"					# A = @SP = 0
	asmCode = asmCode + "M=M+1\n"				# SP = SP - 1

	return asmCode

# __ Comparison command parsing.
def parseCompCmd(strCmd):
	myself = "parseCompCmd()"
	
	asmCode = initAsmCode(myself)

	# __ Without 'global', Python considers g_nLabelCount as local because of  
	# the assigment below !
	global g_nLabelCount

	traceMsg(myself, "comparison parsing [" + strCmd + "]...")

	# __ Dynamic labels :
	g_nLabelCount += 1
	# __ Example : StackTest-eq1-TRUE
	strLblTRUE = g_strNS + "-" + strCmd + str(g_nLabelCount) + "-TRUE" 
	# __ Example : StackTest-eq1-END
	strLblEND = g_strNS + "-" + strCmd + str(g_nLabelCount) + "-END" 

	asmCode = asmCode + "@SP\n"						# A = @SP = 0	
	asmCode = asmCode + "M=M-1\n"					# SP = SP - 1
	asmCode = asmCode + "A=M\n"						# A = SP
	asmCode = asmCode + "D=M\n"						# D = x
	asmCode = asmCode + "@SP\n"						# A = @SP = 0
	asmCode = asmCode + "M=M-1\n"					# SP = SP - 1
	asmCode = asmCode + "A=M\n"						# A = SP
	asmCode = asmCode + "D=M-D\n"					# D = RAM[SP] - D = x - y
	asmCode = asmCode + "@" + strLblTRUE + "\n"		# Example : @StackTest-eq1-TRUE
	asmOp = vmCompToAsmDict[strCmd]					# Example : eq
	asmCode = asmCode + "D;" + asmOp + "\n"			# Example : D;JEQ
	asmCode = asmCode + "D=0\n"						# D = false
	asmCode = asmCode + "@" + strLblEND + "\n"		# Example : @StackTest-eq1-END
	asmCode = asmCode + "0;JMP\n"					# Unconditional jump
	asmCode = asmCode + "(" + strLblTRUE + ")\n"	# Example : (StackTest-eq1-TRUE)
	asmCode = asmCode + "D=-1\n"					# D = true
	asmCode = asmCode + "(" + strLblEND + ")\n"		# Example : (StackTest-eq1-END)
	asmCode = asmCode + "@SP\n"						# A = @SP = 0
	asmCode = asmCode + "A=M\n"						# A = SP
	asmCode = asmCode + "M=D\n"						# SP = D = true or false
	asmCode = asmCode + "@SP\n"						# A = @SP = 0
	asmCode = asmCode + "M=M+1\n"					# SP = SP + 1

	return asmCode

# __ Parsing of one of the 2 operands following commands : add, sub, and, or
def parseBinaryALCmd(strCmd):
	myself = "parseBinaryALCmd()"

	asmCode = initAsmCode(myself)

	traceMsg(myself, "binary command parsing [" + strCmd + "]...")

	asmCode = asmCode + "@SP\n"					# A = @SP = 0	
	asmCode = asmCode + "M=M-1\n"				# SP = SP - 1
	asmCode = asmCode + "A=M\n"					# A = SP
	asmCode = asmCode + "D=M\n"					# D = x
	asmCode = asmCode + "@SP\n"					# A = @SP = 0
	asmCode = asmCode + "M=M-1\n"				# SP = SP - 1
	asmCode = asmCode + "A=M\n"					# A = SP
	asmOp = vmToAsmBinaryOpDict[strCmd]
	asmCode = asmCode + "M=M" + asmOp + "D\n"	# D=x+y
	asmCode = asmCode + "@SP\n"					# A = @SP = 0
	asmCode = asmCode + "M=M+1\n"				# SP = SP + 1

	return asmCode

# __ Parsing a logical or arithmetic command.
def parseALCommand(strCmd):
	myself = "parseALCommand()" ; asmCode = ""

	traceMsg(myself, "parsing [" + strCmd + "]...")
	# __ Logical or arithmetic binary command ?
	if strCmd in vmToAsmBinaryOpDict:
		asmCode = parseBinaryALCmd(strCmd)
	# __ Logical or arithmetic unnary command ?
	elif strCmd in vmToAsmUnaryOpDict:
		asmCode = parseUnaryAL(strCmd)
	# __ Comparison ?
	elif strCmd in vmCompToAsmDict:
		asmCode = parseCompCmd(strCmd)
	else:
		errMsg(myself, "unknown command [" + strCmd + "] !")

	return asmCode

# __ Parsing a label command.
def parseLabelCmd(strLabel):
	myself = "parseLabelCmd()"

	if g_strCurrentFunction != "":
		strLabel = g_strCurrentFunction + LABELSEP + strLabel
	else: 
		strLabel = g_strNS + LABELSEP + strLabel

	traceMsg(myself, "label declaration [" + strLabel + "]...")
	asmCode = "(" + strLabel + ")"

	return asmCode

# __ goto command parsing.
def parseGotoCmd(strLabel):
	myself = "parseGotoCmd()"
	traceMsg(myself, "parsing goto command [goto " + strLabel + "]...")

	if g_strCurrentFunction != "":
		strLabel = g_strCurrentFunction + LABELSEP + strLabel
	else:
		strLabel = g_strNS + LABELSEP + strLabel

	asmCode = "@" + strLabel + "\n"		# Example : @OUTPUT_D	
	asmCode = asmCode + "0;JMP\n"

	return asmCode

# __ Parsing a if-goto command.
# Quote Ch. 08 p. 6 about 'if-goto c' : "This command effects a 'conditional 
# goto' operation.  The stack’s topmost value is popped; if the value is not 
# zero, execution continues from the location marked by the c label ; 
# otherwise, execution continues from the next command in the program. 
# The jump destination must be located in the same function."
def parseIfGotoCmd(strLabel):
	myself = "parseIfGotoCmd()"

	traceMsg(myself, "parsing [if-goto " + strLabel + "]...")
	asmCode = "@SP\n"							# A = @SP = 0	
	asmCode = asmCode + "M=M-1\n"				# SP = SP - 1
	asmCode = asmCode + "A=M\n"					# A = SP
	asmCode = asmCode + "D=M\n"					# D = x

	if g_strCurrentFunction != "":
		strLabel = g_strCurrentFunction + LABELSEP + strLabel
	else:
		strLabel = g_strNS + LABELSEP + strLabel

	asmCode = asmCode + "@" + strLabel + "\n"	# Example : @OUTPUT_D	
	asmCode = asmCode + "D;JNE\n"				# Jump if D <> 0

	return asmCode

# __ Function declaration parsing : 'function f n'. Quote Ch. 08 p. 7 : "Here 
# starts the code of a function named f, which has n local variables;"
# NB : 
# - One should probably take g_strNS namespace into account !
# - Ch. 08 (and mostly the associated lecture) contains instructions about how  
# labels and functions should be named, mainly in relation with the file name.  
# Dollar sign $' is used as separator. 
def parseFunction(strName, strVarCount):
	myself = "parseFunction()"

	asmCode = initAsmCode(myself)

	global g_strCurrentFunction

	g_strCurrentFunction = strName
	traceMsg(myself, "function declaration [" + g_strCurrentFunction + "], " + strVarCount + " local variable(s)")

	asmCode = asmCode + "(" + g_strCurrentFunction + ")\n"

	nLocals = int(strVarCount)
	if nLocals > 0:
		asmCode = asmCode + "// -- Setting " + strVarCount + " local variable(s) to 0 :\n"
		for i in range(nLocals):
			asmCode = asmCode + "@SP\n"
			asmCode = asmCode + "A=M\n"
			asmCode = asmCode + "M=0\n"
			asmCode = asmCode + "@SP\n"
			asmCode = asmCode + "M=M+1\n"
	else:
		asmCode = asmCode + "// -- Function without local variable...\n"

	return asmCode

# __ Function call parsing : 'call f n'.
# Quote Ch. 08 p. 7 : "Call function  f, stating that  m arguments have 
# already been pushed onto the stack" => We must have VM instructions of the  
# following kind before the call instruction :
#		push argument x
#		push argument y
#		push argument z
#		call f 3
# 
def parseCall(strName, strArgCount):
	myself = "parseCall()"

	asmCode = initAsmCode(myself)

	traceMsg(myself, "calling [" + strName + "] with " + strArgCount + " argument(s)...")

	strRetLabel = funcRetLabel(strName)
	asmCode = asmCode + "@" + strRetLabel + "\n"
	asmCode = asmCode + "D=A\n"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "A=M\n"
	asmCode = asmCode + "M=D\n"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "M=M+1\n"

	# push LCL :
	asmCode = asmCode + pushReg("LCL")

	# push ARG :
	asmCode = asmCode + pushReg("ARG")

	# push THIS :
	asmCode = asmCode + pushReg("THIS")

	# push THAT :
	asmCode = asmCode + pushReg("THAT")

	# We have saved ARG, so we can make it point to argument 0 => cf. 
	# Ch. 08 p. 11 + cf. lecture p. 112 : 
	# "ARG = SP-5-nArgs // Repositions ARG"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "D=M\n"
	for i in range(int(strArgCount) + 5):
		asmCode = asmCode + "D=D-1\n"
	asmCode = asmCode + "@ARG\n"
	asmCode = asmCode + "M=D\n"

	# We have saved LCL, so we can make it point to local 0 => cf.  
	# Ch. 08 p. 11 + cf. lecture p. 114 : 
	# "LCL = SP // Repositions LCL"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "D=M\n"
	asmCode = asmCode + "@LCL\n"
	asmCode = asmCode + "M=D\n"

	# We must end by an unconditional jump to the function label :
	asmCode = asmCode + "@" + strName + "\n"		# Example : @StackTest-eq1-END
	asmCode = asmCode + "0;JMP\n"					# Unconditional jump

	# We must create a label that will serve as return point for the execution 
	# of 'return'. For example 'RET_ADDRESS_CALLnnn' like in Pong.asm :
	asmCode = asmCode + "(" + strRetLabel + ")\n"

	return asmCode

# __ 'return' parsing.
# See Ch. 08 p. 7 : "Return to the calling function."
# __ V0.1 : get name of currently parsed function (NB : it must exist by  
# construction because of the preprocessing).
def parseReturn():
	myself = "parseReturn()"

	asmCode = initAsmCode(myself)

	traceMsg(myself, "parsing 'return' for " + g_strCurrentFunction + " function...")
	asmCode = asmCode + "// -- R14 = FRAME = LCL :\n"
	asmCode = asmCode + "@LCL\n"
	asmCode = asmCode + "D=M\n"
	asmCode = asmCode + "@R14\n"
	asmCode = asmCode + "M=D\n"
	asmCode = asmCode + "// -- R13 = *(FRAME-5) = Return address :\n"
	asmCode = asmCode + "@R13\n"
	asmCode = asmCode + "M=D\n"
	asmCode = asmCode + "M=M-1\n"
	asmCode = asmCode + "M=M-1\n"
	asmCode = asmCode + "M=M-1\n"
	asmCode = asmCode + "M=M-1\n"
	asmCode = asmCode + "M=M-1\n"
	asmCode = asmCode + "A=M\n"
	asmCode = asmCode + "D=M\n"
	asmCode = asmCode + "@R13\n"
	asmCode = asmCode + "M=D\n"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "A=M-1\n"
	asmCode = asmCode + "D=M\n"
	asmCode = asmCode + "@ARG\n"
	asmCode = asmCode + "A=M\n"
	asmCode = asmCode + "M=D\n"
	asmCode = asmCode + "@ARG\n"
	asmCode = asmCode + "D=M+1\n"
	asmCode = asmCode + "@SP\n"
	asmCode = asmCode + "M=D\n"
	# THAT = *(endFrame – 1) => restores THAT of the caller :\n"
	asmCode = asmCode + restoreReg("THAT", "R14")
	asmCode = asmCode + restoreReg("THIS", "R14")
	asmCode = asmCode + restoreReg("ARG", "R14")
	asmCode = asmCode + restoreReg("LCL", "R14")
	asmCode = asmCode + "@R13\n"
	asmCode = asmCode + "A=M\n"
	asmCode = asmCode + "0;JMP\n"					# unconditional jump

	return asmCode

# __ Source file line parsing.
# 
# Quote Ch. 07 §2.1 p. 7 : "Within a  .vm file, each VM command appears in a 
# separate line, and in one of the following formats : 
# <command>, <command  arg>, or  <command arg1 arg2>, where the arguments are 
# separated from each other and from the command part by an arbitrary number of 
# spaces. "//" comments can appear at the end of any line and are ignored."
# 
# Quote Ch. 07 §2.3 p. 10 : "There are two memory access commands: 
# - push segment index : push the value of segment[index] onto the stack; 
# - pop segment index : pop the topmost stack item and store its value in 
# segment[index]. 
# Where segment is one of the eight segment names and index is a non-negative 
# integer.
# 
def parseVMLine(vmLine):
	myself = "parseVMLine()" ; strAsm = ""

	strAsm = strAsm + "@7777\n"
	strAsm = strAsm + "M=1\n"
	strAsm = strAsm + "M=0\n"

	tokensList = vmLine.split()
	# __ tokensList contains at least 1 token by construction so we do not 
	# check if the first one exists.
	vmCmd = tokensList[0] ; arg1 = "" ; arg2 = ""

	# __ Known command ?
	if vmCmd in vmCmdDict:
		nOps = vmCmdDict[vmCmd]
	else:
		errMsg(myself, "unknown command [" + vmCmd + "] line [" + vmLine + "] !")
		return strAsm

	# __ Operands count ok ?
	if len(tokensList) - 1 < nOps:
		errMsg(myself, "the command " + vmCmd + " expects " + str(nOps) + " operand(s) !")
		return strAsm

	# __ Initialize arg1 and arg2 if possible :
	if len(tokensList) > 1:
		arg1 = tokensList[1]

	if len(tokensList) > 2:
		arg2 = tokensList[2]

	# __ Memory access commands validation (see function header) :
	if vmCmd == "push" or vmCmd == "pop":
		if not(arg1 in vmSegToASM):
			errMsg(myself, arg1 + " is not a valid segment !")
			return strAsm
		if not(arg2.isdigit()):
			errMsg(myself, arg2 + " is not a valid index !")
			return strAsm
		strAsm = parseMemAccessCommand(vmCmd, arg1, arg2)
	elif vmCmd == "label":
		# __ Label Syntax ok ?
		if labelCheck(arg1) != 0:
			errMsg(myself, arg1 + " is not a valid label !")
			return strAsm
		strAsm = parseLabelCmd(arg1)			
	elif vmCmd == "goto":
		strAsm = parseGotoCmd(arg1)
	elif vmCmd == "if-goto":
		strAsm = parseIfGotoCmd(arg1)
	elif vmCmd == "function":
		tSplit = arg1.split('.')
		if len(tSplit) < 2:
			errMsg(myself, arg1 + " without namespace !")
			return strAsm
		traceMsg(myself, "adding [" + tSplit[0] + "] namespace to fncNSList...")
		fncNSList.append(tSplit[0])
		if functionNameCheck(tSplit[1]) != 0:
			errMsg(myself, tSplit[1] + " is not a valid function name !")
			return strAsm
		if not(arg2.isdigit()):
			errMsg(myself, arg2 + " is not an integer !")
			return strAsm
		strAsm = parseFunction(arg1, arg2)
	elif vmCmd == "call":
		tSplit = arg1.split('.')
		if functionNameCheck(tSplit[1]) != 0:
			errMsg(myself, tSplit[1] + " is not a valid function name !")
			return strAsm
		if not(arg2.isdigit()):
			errMsg(myself, arg2 + " is not an integer !")
			return strAsm
		strAsm = parseCall(arg1, arg2)
	elif vmCmd == "return":
		strAsm = parseReturn()
	else:
		strAsm = parseALCommand(vmCmd)			

	return strAsm

# __ Read vmFile a first time to associate in the dictionary vmFncLocalsDict 
# the functions names to their respective local variables count. Check also 
# that each function contains at least a 'return' instruction and that each 
# 'return' matches a function.
def preProcessVMFile(vmFilePath):
	global g_bBootStrapped, g_strNS
	myself = "preProcessVMFile()" ; rc = 0 ; nLine = 0
	strFunction = ""

	traceMsg(myself, "preprocessing " + vmFilePath + "...")

	try:
		fInput = open(vmFilePath)
	except:
		errMsg(myself, "failed to open " + vmFilePath + " !")
		return 1

	# __ Indique si on doit trouver une commande 'return' :
	bReturnCheck = False

	for l in fInput:
		nLine += 1
		line = l.strip()
		if line[0:2] == "//" or line == "":
			traceMsg(myself, "comment or white line...")
		else:
			tokensList = line.split()
			vmCmd = tokensList[0] ; arg1 = "" ; arg2 = ""
			if vmCmd == "function":
				if len(tokensList) > 2:
					arg1 = tokensList[1]
					strFunction = arg1
					arg2 = tokensList[2]
					if arg1 in vmFncLocalsDict:
						errMsg(myself, "ligne " + str(nLine) + " : duplicate declaration for [" + arg1 + "] !")
						rc = 3
						break
					# __ On ne vérifier pas la validité du nom de fonction ni 
					# si arg2 est numérique car fait pendant le parsing :
					traceMsg(myself, "function '" + arg1 + "()' has " + arg2 + " local variable(s)...")
					vmFncLocalsDict[arg1] = arg2
					bReturnCheck = True
					if arg1.upper() == "SYS.INIT":
						bReturnCheck = False
						g_strNS = pathlib.Path(vmFilePath).stem
						traceMsg(myself, "g_strNS initialized to [" + g_strNS + "]")
						traceMsg(myself, "Sys.init() found")
						g_bBootStrapped = True
				else:
					errMsg(myself, "line " + str(nLine) + " : the 'function' command takes 2 arguments !")
					rc = 2
					break
			elif vmCmd == "return":
				bReturnCheck = False

	if bReturnCheck:
		errMsg(myself, "function '" + strFunction + "()' has no ending 'return' !")
		rc = 5

	traceMsg(myself, "closing [" + vmFilePath + "]...")
	fInput.close()

	return rc

# __ Parses each line of the input file and writes down the result in the 
# output file. Returns the count of detected errors.
def parseVMFile(vmFilePath, fAsm):
	myself = "parseVMFile()" ; nErrCount = 0

	header = " Conversion of " + vmFilePath + " : \n"
	s = "\n// " + f"{header:=>78}"
	fAsm.write(s)

	traceMsg(myself, "opening [" + vmFilePath + "]...")
	try:
		fInput = open(vmFilePath)
	except:
		errMsg(myself, "failed to open " + vmFilePath + " !")
		return 1
	
	for vmLine in fInput:
		line = vmLine.strip()
		if line[0:2] == "//" or line == "":
			traceMsg(myself, "comment or white line...")
		else:
			traceMsg(myself, "conversion of [" + line + "]...")
			asmCode = parseVMLine(line)
			if asmCode != "":
				fAsm.write("// " + vmFilePath + ", [" + line + "] : \n")
				fAsm.write(asmCode + "\n")
			else:
				nErrCount += 1
				errMsg(myself, "parsing failure !")

	traceMsg(myself, "closing [" + vmFilePath + "]...")
	fInput.close()
	traceMsg(myself, "parsing errors count : " + str(nErrCount))

	return nErrCount

# __ Renvoie la description d'un niveau de message :
def levelDesc(level):
	if level == ERR_LEVEL:
		return("Error")
	elif level == INFO_LEVEL:
		return("Info")
	elif level == TRACE_LEVEL:
		return("Trace")
	else:
		return("???")

# __ Affichage d'un message :
def msgOut(who, level, msg):
	if level <= g_nTraceLevel:
		print(who + MSGSEP + levelDesc(level) + MSGSEP + msg)

# __ Affiche une erreur :
def errMsg(who, msg):
	msgOut(who, ERR_LEVEL, msg)

# __ Affiche une trace :
def traceMsg(who, msg):
	msgOut(who, TRACE_LEVEL, msg)

# __ Affiche une info :
def infoMsg(who, msg):
	msgOut(who, INFO_LEVEL, msg)

# ====================================================================== Main :
myself = os.path.basename(__file__)

# __ Globale du niveau d'information :
g_nTraceLevel = TRACE_LEVEL

infoMsg(myself, "starting version V" + SCRIPT_VERSION)

# __ Dictionnaire de comptage servant aux appels de fonctions :
vmFncCallDict = {}

if (len(sys.argv) < 2):
	errMsg(myself, "file or directory name expected !")
	exit(1)

arg1 = sys.argv[1]

# __ Fichier or repertoire ?
if os.path.isdir(arg1):
	traceMsg(myself, arg1 + " is a directory !")
	# __ Ici on remplit la liste vmList avec le nom des fichiers vm du repertoire
	vmList = glob.glob(arg1 + "\*" + VMEXT)
	# __ Inutile de continuer si la liste est vide :
	if len(vmList) == 0:
		errMsg(myself, "no file " + VMEXT + " in " + arg1 + " !")
		exit(5)
	# __ Fichier de sortie :
	asmFile = arg1 + "\\" + pathlib.PurePath(arg1).name + ASMEXT
elif os.path.isfile(arg1):
	fileExt = pathlib.Path(arg1).suffix
	traceMsg(myself, arg1 + " is a file with [" + fileExt + "] extension !")
	# __ Tester si fichier vm !
	if fileExt != VMEXT:
		errMsg(myself, "expected " + VMEXT + " extension !")
		exit(3)
	# __ Ici on initialise vmList avec le nom du fichier 
	vmList = [arg1]
	# __ Fichier de sortie :
	asmFile = os.path.splitext(arg1)[0] + ASMEXT
else:
	errMsg(myself, arg1 + " is not a VM file nor a directory !")
	exit(2)

traceMsg(myself, str(len(vmList)) + " VM file(s) to process :")
traceMsg(myself, str(vmList))
traceMsg(myself, "output : " + asmFile)

# __ Sortie = fichier assembler
try:
	fAsmFile = open(asmFile, "w")
except Exception as e:
	errMsg(myself, "failed to open " + asmFile + " in write mode !")
	exit(3)

nErrCount = 0
nVMCount = 0
g_bBootStrapped = False 

for vmFile in vmList:
	nVMCount += 1
	try:
		# __ Pré-traitement de vmFile pour construire vmFncLocalsDict, un 
		# dictionnaire associant un nom de fonction à son nombre de variables 
		# locales.
		vmFncLocalsDict = {}
		if preProcessVMFile(vmFile) == 0:
			traceMsg(myself, str(len(vmFncLocalsDict)) + " function declaration(s) detected...")
		else:
			errMsg(myself, "preprocessing failure for " + vmFile + " !")
			nErrCount += 1
	except Exception as e:
		errMsg(myself, "exception " + str(e) + " during [" + vmFile + "] preprocessing !?")
		nErrCount += 1

# __ Assemble file header :
setAsmHeader(fAsmFile) 

# __ V0.8 : we manage a namespace list deduced from the name of the VM files 
# and another list deduced from the function names. At the end, we check that 
# the namespace of each function is part of the first list.
vmNSList = []
fncNSList = []

# __ Loop on the VM files :
for vmFile in vmList:
	# __ We use the file name as a namespace :
	g_strNS = pathlib.Path(vmFile).stem
	vmNSList.append(g_strNS)
	traceMsg(myself, "processing [" + vmFile + "], namespace '" + g_strNS + "'")
	# __ Global counter serving to generate labels used during comparisons :
	g_nLabelCount = 0
	# __ V0.1 : currently parsed function name. 
	g_strCurrentFunction = ""
	try:
		nRC = parseVMFile(vmFile, fAsmFile)
		infoMsg(myself, str(nRC) + " conversion error(s) for [" + vmFile + "]")
		nErrCount += nRC
	except Exception as e:
		errMsg(myself, "exception " + str(e) + " during [" + vmFile + "] conversion !?")
		nErrCount += 1

infoMsg(myself, "VM namespaces : " + str(vmNSList))
for fncNS in fncNSList:
	if fncNS not in vmNSList:
		errMsg(myself, "function namespace [" + fncNS + "] not found in the VM namespace !")
		nErrCount += 1

# __ Finalisations globales :
endAsmFile(fAsmFile) 

fAsmFile.close()

infoMsg(myself, str(nVMCount) + " VM file(s) processed, " + str(nErrCount) + " error(s)")

exit(nErrCount)
