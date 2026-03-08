# =============================================================================
# Description : converts a single VM file (or a series of VM files located in a 
# given directory) to a corresponding asm file (or a series of corresponding 
# asm files).
# 
# Returns 0 even if the conversion failed. The only case in which the script 
# does not returns 0 is when unexpected errors were encountered, for example 
# file open error.  
# 
# Syntax : python VMTranslator.py VM_file_path | VM_directory_path
#
# ======================================== Reminders Ch. 4 "Machine Language" :
# 
# A variable is a label designating a memory location (= an address). Let V be  
# such a variable and let suppose it is associated to memory address 23. In  
# classical programming, the instruction V = 8 would set the memory location 23 
# to contain 8.
# 
# Set the variable V to 1 :
#	@V		// Put V address (so 23 in the previous example) into A.
#	M=1		// Put 1 into the memory location pointed to by A (so 23).
# 
# Put the content of variable X into D :
# 	@X
#	D=M
# 
# Assembler code analysis corresponding to the VM instruction "push constant 2".
# To simplify, we suppose that SP point to address 47. Ultimately, we see that  
# we indeed obtained RAM[SP] = 2 and SP++ !
#
# // push constant 2
# 			// -------------------------------------------------------- RAM 1 :
# @2		// A = 2
# D=A		// D = A = 2
# @SP		// A = SP address = 47
# A=M		// A = Memory content at address 47 = 127
# 			// -------------------------------------------------------- RAM 2 :
# M=D		// Put D (= 2) in RAM at address 127, so RAM[127]=2
# @SP		// A = SP address = 47
# 			// -------------------------------------------------------- RAM 3 :
# M=M+1		// Increment memory content at address 47 so new SP content = 128 
# 
# 
# 		RAM 1 :					     			RAM 2 :                         		RAM 3 :							
# 			                			                                                                 
# 		Address	Content  						Address	Content              		Address	Content          
# 		-------	-------- 						-------	--------             		-------	--------         
# 		45 :	[ ? ]       					45 :	[ ? ]                    		45 :	[ ? ]            
# 		46 :	[ ? ]       					46 :	[ ? ]                    		46 :	[ ? ]            
# SP -> 47 :	[ 127 ]	 ---+			SP -> 	47 :	[ 127 ]  ---+ 			SP -> 	47 :	[ 128 ]  ---+    
# 		48 :	[ ? ]		|    				48 :	[ ? ]		|                  	48 :	[ ? ]		|    
# 		(...)				(...)		 		(...)				(...)				(...)				(...)
# 		126 :	[ ? ]		|   				126 :	[ ? ]		|                 	126 :	[ ? ]		|    
# 		127 :	[ ? ]	<---+					127 :	[ 2 ]	<---+	 	          	127 :	[ 2 ]		|	 
# 		128 :	[ ? ]      						128 :	[ ? ]                  			128 :	[ ? ]	<---+ 
# 
# 
# =============================================================================

import sys
import os
import pathlib
import glob

# ========================================================== Pseudo-constants :

ERR_LEVEL = 1
INFO_LEVEL = 2
TRACE_LEVEL = 3
MSGSEP = ", "
VMEXT = ".vm"
ASMEXT = ".asm"

# __ Conversion dictionaries :

# Connection between a VM segment name (Table 7 Ch. 07 p. 10) and assembler 
# symbols (Table 14 Ch. 07 p. 20) : 
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
almaDict = {
	"add"  : 0,
	"sub"  : 0,
	"neg"  : 0,
	"eq"   : 0,  
	"gt"   : 0,
	"lt"   : 0,
	"and"  : 0,
	"or"   : 0,
	"not"  : 0,
	"push" : 2,
	"pop"  : 2
}

# __ Conversion dictionary from a 2 operands arithmetic or logical VM 
# instruction to an assembler operator.
vmToAsmBinaryOpDict = {
	"add" : "+", 
	"sub" : "-", 
	"and" : "&", 
	"or"  : "|"
}

# __ Conversion dictionary from a VM comparison instruction to an assembler 
# jump.
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

# __ Assembler code initialization 
def initAsmFile(fAsm):
	myself = "initAsmFile()" ; asmCode = ""

	asmCode = "// ==== Global initializations :\n"
	asmCode = asmCode + "// Global initializations end ===\n\n"

	fAsm.write(asmCode)

	return

# __ pop() command code generation :
def parsePop(segment, index):
	myself = "parsePop()" ; asmCode = ""

	# __ segment exists in vmSegToASM by construction :
	asmSymbol = vmSegToASM[segment]		

	# __ For the 'static' segment, see for example lecture Ch. 07 p. 75 :
	# pop static 5 => 	// D = stack.pop (code omitted)
	#					@Foo.5
	# 					M=D 
	if segment == "static":
		asmCode = asmCode + "@SP\n"						# A = @SP = 0
		asmCode = asmCode + "M=M-1\n"					# SP = SP - 1
		asmCode = asmCode + "A=M\n"						# A = SP	
		asmCode = asmCode + "D=M\n"						# D = RAM[SP]	
		asmCode = asmCode + "@" + g_strNS + "." + index + "\n"	# A = @vm_name.i, example : A = @BasicTest.i
		asmCode = asmCode + "M=D\n"						# R5 = D = RAM[SP]		
	else:
		asmCode = asmCode + "@" + asmSymbol + "\n"		# Example : A = @LCL
		# __ Special case for 'temp' and 'pointer' segments. In vmSegToASM[], 
		# the keys of those 2 segments correspond respectively to the values  
		# 5 and 3 and not to assembler symbols : we must so use those values as 
		# is, that is A content !
		if segment == "temp" or segment == "pointer":
			asmCode = asmCode + "D=A\n"						# D = A = 5
		else:
			asmCode = asmCode + "D=M\n"						# Example : D = LCL
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

# __ Asm code generation of a VM command 'push segment index'. The case of the  
# constant segment is treated separately (see Ch. 07 p. 21 par example).
def parsePush(segment, index):
	myself = "parsePush()" ; asmCode = ""

	if segment == "constant":
		asmCode = "@" + index + "\n"
		asmCode = asmCode + "D=A\n"
		asmCode = asmCode + "@SP\n"
		asmCode = asmCode + "A=M\n"
		asmCode = asmCode + "M=D\n"
		asmCode = asmCode + "@SP\n"
		asmCode = asmCode + "M=M+1\n"
	elif segment == "static":
		asmCode = "@" + g_strNS + "." + index + "\n"	# example : @StaticTest.3
		asmCode = asmCode + "D=M\n"						# D = RAM[A]
		asmCode = asmCode + "@SP\n"						# A = @SP
		asmCode = asmCode + "A=M\n"						# A = SP
		asmCode = asmCode + "M=D\n"						# RAM[SP] = RAM[RAM[A]]
		asmCode = asmCode + "@SP\n"						# A = @SP
		asmCode = asmCode + "M=M+1\n"					# SP = SP + 1
	else:
		# __ segment exists in vmSegToASM according to parseVMLine() :
		asmSymbol = vmSegToASM[segment]
		asmCode = "@" + asmSymbol + "\n"				# example : A = @ARG
		# __ Special case for temp segment, see parsePop() above.
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

# __ Description : memory access command parsing.
def parseMemAccessCommand(strCmd, segment, index):
	myself = "parseMemAccessCommand()" ; asmCode = ""
	
	if strCmd == "push":
		traceMsg(myself, "push() command handling...")
		asmCode = parsePush(segment, index)
	else:
		traceMsg(myself, "pop() command handling...")
		asmCode = parsePop(segment, index)

	return asmCode


# __ Description : parsing of a 1 operand arithmetic or logical command.
def parseUnaryAL(strCmd): 
	myself = "parseUnaryAL()" ; asmCode = ""

	traceMsg(myself, "parsing unary command [" + strCmd + "]...")

	asmCode = "@SP\n"							# A = @SP = 0	
	asmCode = asmCode + "M=M-1\n"				# SP = SP - 1
	asmCode = asmCode + "A=M\n"					# A = SP
	asmOp = vmToAsmUnaryOpDict[strCmd]
	asmCode = asmCode + "M=" + asmOp + "M\n"	# Example : M=-M
	asmCode = asmCode + "@SP\n"					# A = @SP = 0
	asmCode = asmCode + "M=M+1\n"				# SP = SP - 1

	return asmCode

# __ Description : parsing a comparison command.
def parseCompCmd(strCmd):
	myself = "parseCompCmd()" ; asmCode = ""
	# __ Without the 'global'declaration, Python considers g_nLabelCount as 
	# local because of the below assignment !
	global g_nLabelCount

	traceMsg(myself, "comparison parsing [" + strCmd + "]...")

	# __ Dynamic labels :
	g_nLabelCount += 1
	# __ Example : StackTest-eq1-TRUE
	strLblTRUE = g_strNS + "-" + strCmd + str(g_nLabelCount) + "-TRUE" 
	# __ Example : StackTest-eq1-END
	strLblEND = g_strNS + "-" + strCmd + str(g_nLabelCount) + "-END" 

	asmCode = "@SP\n"								# A = @SP = 0	
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
	asmCode = asmCode + "M=D\n"						# SP = D = true ou false
	asmCode = asmCode + "@SP\n"						# A = @SP = 0
	asmCode = asmCode + "M=M+1\n"					# SP = SP + 1

	return asmCode

# __ Description : parsing of one of the following 2 operands arithmetical or 
# logical commands : add, sub, and, or
def parseBinaryALCmd(strCmd):
	myself = "parseBinaryALCmd()" ; asmCode = ""

	traceMsg(myself, "parsing of the binary command [" + strCmd + "]...")

	asmCode = "@SP\n"							# A = @SP = 0	
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

# __ Description : parsing of an arithmetic or logical command.
def parseALCommand(strCmd):
	myself = "parseALCommand()" ; asmCode = ""

	traceMsg(myself, "parsing [" + strCmd + "]...")
	# __ 2 operands arithmetic or logical ?
	if strCmd in vmToAsmBinaryOpDict:
		asmCode = parseBinaryALCmd(strCmd)
	# __ 1 operand arithmetic or logical ?
	elif strCmd in vmToAsmUnaryOpDict:
		asmCode = parseUnaryAL(strCmd)
	# __ Comparison ?
	elif strCmd in vmCompToAsmDict:
		asmCode = parseCompCmd(strCmd)
	else:
		asmCode = "// __ Unhandled command [" + strCmd + "]"

	return asmCode

# __ Description : parsing a source file line.
# 
# Ch. 07 §2.1 p. 7 quote : "Within a  .vm file, each VM command appears in a 
# separate line, and in one of the following formats : 
# <command>, <command  arg>, or  <command arg1 arg2>, where the arguments are 
# separated from each other and from the command part by an arbitrary number of 
# spaces. "//" comments can appear at the end of any line and are ignored."
# 
# Ch. 07 §2.3 p. 10 quote : "There are two memory access commands: 
# - push segment index : push the value of segment[index] onto the stack; 
# - pop segment index : pop the topmost stack item and store its value in 
# segment[index]. 
# Where segment is one of the eight segment names and index is a non-negative 
# integer.
# 
def parseVMLine(vmLine):
	myself = "parseVMLine()" ; strAsm = ""

	tokensList = vmLine.split()
	# __ tokensList contains at least 1 token by construction so we do not test 
	# if the first one exists.
	command = tokensList[0] ; arg1 = "" ; arg2 = ""

	# __ Known command ?
	if command in almaDict:
		nOps = almaDict[command]
	else:
		errMsg(myself, "unknown command [" + command + "] in [" + vmLine + "] !")
		return strAsm

	# __ Operands count ok ?
	if len(tokensList) - 1 < nOps:
		errMsg(myself, "the command " + command + " expects " + str(nOps) + " operands !")
		return strAsm

	# __ Feed arg1 and arg2 if possible :
	if len(tokensList) > 1:
		arg1 = tokensList[1]

	if len(tokensList) > 2:
		arg2 = tokensList[2]

	# __ Memory access commands validation (see function header) :
	if command == "push" or command == "pop":
		if not(arg1 in vmSegToASM):
			errMsg(myself, arg1 + " is not a valide segment !")
			return strAsm

		if not(arg2.isdigit()):
			errMsg(myself, arg2 + " is not a valid index !")
			return strAsm

		strAsm = parseMemAccessCommand(command, arg1, arg2)
	else:
		strAsm = parseALCommand(command)			

	return strAsm

# __ Description : parses each line of the input file and writes down the 
# result into the output file. Returns the found errors count.
def parseVMFile(vmFilePath, fAsm):
	myself = "parseVMFile()" ; nErrCount = 0

	fAsm.write("// ==== Conversion of " + vmFilePath + " :\n")
	traceMsg(myself, "opening [" + vmFilePath + "]...")
	try:
		fInput = open(vmFilePath)
	except:
		errMsg(myself, "failed to open " + vmFilePath + " !")
		return 1
	
	for l in fInput:
		line = l.strip()
		if line[0:2] == "//" or line == "":
			traceMsg(myself, "comment or white line...")
		else:
			traceMsg(myself, "conversion of [" + line + "]...")
			asmCode = parseVMLine(line)
			if asmCode != "":
				fAsm.write("// " + line + ": \n")
				fAsm.write(asmCode + "\n")
			else:
				nErrCount += 1
				errMsg(myself, "parsing failure !")
	traceMsg(myself, "closing [" + vmFilePath + "]...")
	fInput.close()
	traceMsg(myself, "parsing errors count : " + str(nErrCount))

	return nErrCount

# __ Returns a message level description :
def levelDesc(level):
	if level == ERR_LEVEL:
		return("Error")
	elif level == INFO_LEVEL:
		return("Info")
	elif level == TRACE_LEVEL:
		return("Trace")
	else:
		return("???")

# __ Displays a message :
def msgOut(who, level, msg):
	if level <= g_nTraceLevel:
		print(who + MSGSEP + levelDesc(level) + MSGSEP + msg)

# __ Displays an error :
def errMsg(who, msg):
	msgOut(who, ERR_LEVEL, msg)

# __ Displays a trace :
def traceMsg(who, msg):
	msgOut(who, TRACE_LEVEL, msg)

# __ Displays an info :
def infoMsg(who, msg):
	msgOut(who, INFO_LEVEL, msg)

# ====================================================================== Main :
myself = os.path.basename(__file__)

# __ Information level global :
g_nTraceLevel = TRACE_LEVEL

if (len(sys.argv) < 2):
	errMsg(myself, "file or directory name expected !")
	exit(1)

arg1 = sys.argv[1]

# __ File or directory ?
if os.path.isdir(arg1):
	traceMsg(myself, arg1 + " is a directory !")
	# __ Here we fill the vmList list with the name of the VM files of the 
	# directory 
	vmList = glob.glob(arg1 + "\*" + VMEXT)
	# __ Useless to continue if the list is empty :
	if len(vmList) == 0:
		errMsg(myself, "no " + VMEXT + " file into " + arg1 + " !")
		exit(5)
	# __ Output file :
	asmFile = arg1 + "\\" + pathlib.PurePath(arg1).name + ASMEXT
elif os.path.isfile(arg1):
	fileExt = pathlib.Path(arg1).suffix
	traceMsg(myself, arg1 + " if a file having [" + fileExt + "] extension !")
	# __ Test if VM file !
	if fileExt != VMEXT:
		errMsg(myself, VMEXT + " extension expected !")
		exit(3)
	# __ Here we initialize vmList with the file name 
	vmList = [arg1]
	# __ Output file :
	asmFile = os.path.splitext(arg1)[0] + ASMEXT
else:
	errMsg(myself, arg1 + " is not a VM file nor a directory !")
	exit(2)

traceMsg(myself, str(len(vmList)) + " VM file(s) to handle :")
traceMsg(myself, str(vmList))
traceMsg(myself, "output : " + asmFile)

# __ Output = assembler file
try:
	fAsmFile = open(asmFile, "w")
except Exception as e:
	errMsg(myself, "failed to open " + asmFile + " in write mode !")
	exit(3)

# __ Global initializations :
initAsmFile(fAsmFile) 

# __ Loop on VM files :
nErrCount = 0
nVMCount = 0
for vmFile in vmList:
	nVMCount += 1
	# __ We take the file name as namespace :
	g_strNS = pathlib.Path(vmFile).stem
	traceMsg(myself, "handling [" + vmFile + "], namespace " + g_strNS)
	# __ Global counter used for labels generation during the comparisons :
	g_nLabelCount = 0
	try:
		nRC = parseVMFile(vmFile, fAsmFile)
		infoMsg(myself, str(nRC) + " conversion error(s) for [" + vmFile + "]")
		nErrCount += nRC
	except Exception as e:
		errMsg(myself, "exception " + str(e) + " during [" + vmFile + "] conversion !?")
		nErrCount += 1

fAsmFile.close()

infoMsg(myself, str(nVMCount) + " VM file(s) handled, " + str(nErrCount) + " error(s)")

exit(0)
