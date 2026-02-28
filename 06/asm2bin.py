
import sys
import os

# ========================================================== Pseudo-constants :

# __ Valid characters for labels :
LABEL_BEGIN_CHECK = "_.$;abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
LABEL_STANDARD_CHECK = LABEL_BEGIN_CHECK + "0123456789"

ERR_LEVEL = 1
INFO_LEVEL = 2
TRACE_LEVEL = 3
MSGSEP = ", "

# __ Returns the description of a message level :
def levelDesc(level):
	if level == ERR_LEVEL:
		return("Erreur")
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

# __ Conversion dictionaries :

predefSymbols = {
	"SP" :     "0000000000000000",
	"LCL" :    "0000000000000001",
	"ARG" :    "0000000000000010",
	"THIS" :   "0000000000000011",
	"THAT" :   "0000000000000100",
	"R0" :     "0000000000000000",
	"R1" :     "0000000000000001",
	"R2" :     "0000000000000010",
	"R3" :     "0000000000000011",
	"R4" :     "0000000000000100",
	"R5" :     "0000000000000101",
	"R6" :     "0000000000000110",
	"R7" :     "0000000000000111",
	"R8" :     "0000000000001000",
	"R9" :     "0000000000001001",
	"R10" :    "0000000000001010",
	"R11" :    "0000000000001011",
	"R12" :    "0000000000001100",
	"R13" :    "0000000000001101",
	"R14" :    "0000000000001110",
	"R15" :    "0000000000001111",
	"SCREEN" : "0100000000000000",
	"KBD" :    "0110000000000000"
}

destDict = {
	"null" : "000",
	"M"    : "001",
	"D"    : "010",
	"MD"   : "011",
	"A"    : "100",
	"AM"   : "101",
	"AD"   : "110",
	"AMD"  : "111"
}

jumpDict = {
	"null" : "000",
	"JGT" : "001",
	"JEQ" : "010",
	"JGE" : "011",
	"JLT" : "100",
	"JNE" : "101",
	"JLE" : "110",
	"JMP" : "111"
}

compDict = {
	"0"   : "0101010",
	"1"   : "0111111",
	"-1"  : "0111010",
	"D"   : "0001100",
	"A"   : "0110000",
	"!D"  : "0001101",
	"!A"  : "0110001",
	"-D"  : "0001111",
	"-A"  : "0110011",
	"D+1" : "0011111",
	"A+1" : "0110111",
	"D-1" : "0001110",
	"A-1" : "0110010",
	"D+A" : "0000010",
	"D-A" : "0010011",
	"A-D" : "0000111",
	"D&A" : "0000000",
	"D|A" : "0010101",
	"M"   : "1110000",
	"!M"  : "1110001",
	"-M"  : "1110011",
	"M+1" : "1110111",
	"M-1" : "1110010",
	"D+M" : "1000010",
	"D-M" : "1010011",
	"M-D" : "1000111",
	"D&M" : "1000000",
	"D|M" : "1010101"
}

# ================================================================= Functions :

# __ Converts a decimal into a binary string of nBinLen length  
def dec2bin(nDec, nBinLen = 16):
	myself = "dec2bin()"
	strOut = "" ; n = 1 ; nDec0 = nDec
	while n != 0:
		n = nDec // 2 ; r = nDec % 2
		strOut = str(r) + strOut
		nDec = n
	if len(strOut) > nBinLen:
		errMsg(myself, "failed to convert " + str(nDec0) + " into a maximum of " + str(nBinLen) + " bit(s) !")
		raise OverflowError()
	elif len(strOut) < nBinLen:
		strOut = strOut.rjust(nBinLen, '0') 
	return(strOut)

# __ Parses a 'C' instruction
# 
# __ Source : chapter 06 p. 109
# 
# C-instruction : dest=comp;jump	// Either the dest or jump ﬁelds may be empty.
# 									// If dest is empty, the "=" is omitted
# 									// If jump is empty, the ";" is omitted
# 
# 		   15          10               5                0
# 		   +-----------+----------------+----------------+
#                [       comp        ] [ dest   ] [  jump  ]
# Binary : 1 1 1 [a c1 c2 c3 c4 c5 c6] [d1 d2 d3] [j1 j2 j3]
# 
# The translation of each of the three ﬁelds comp, dest, jump to their binary 
# forms is speciﬁed in the following three tables.
#  
#                         comp                                        comp 
#                                    c1   c2   c3   c4  c5   c6 
#                  (when a=0)                                         (when a=1) 
#                             0       1    0    1    0   1    0 
#                             1       1    1    1    1   1    1 
#                            -1       1    1    1    0   1    0 
#                             D       0    0    1    1   0    0 
#                             A       1    1    0    0   0    0       M 
#                            !D       0    0    1    1   0    1 
#                            !A       1    1    0    0   0    1       !M 
#                            -D       0    0    1    1   1    1 
#                            -A       1    1    0    0   1    1       -M 
#                          D+1        0    1    1    1   1    1 
#                          A+1        1    1    0    1   1    1       M+1 
#                          D-1        0    0    1    1   1    0 
#                          A-1        1    1    0    0   1    0       M-1 
#                          D+A        0    0    0    0   1    0       D+M 
#                          D-A        0    1    0    0   1    1       D-M 
#                          A-D        0    0    0    1   1    1       M-D 
#                          D&A        0    0    0    0   0    0       D&M 
#                          D|A        0    1    0    1   0    1       D|M 
# 
#  
#                  dest        d1   d2   d3          jump        j1  j2   j3 
#                  null         0    0    0          null        0    0    0 
#                  M            0    0    1          JGT         0    0    1 
#                  D            0    1    0          JEQ         0    1    0 
#                  MD           0    1    1          JGE         0    1    1 
#                  A            1    0    0          JLT         1    0    0 
#                  AM           1    0    1          JNE         1    0    1 
#                  AD           1    1    0          JLE         1    1    0 
#                  AMD          1    1    1          JMP         1    1    1 
# 
# TO DO : differentiate "decimal number" and "symbol referring to such number"
# -----------------------------------------------------------------------------
def parseCInstr(strCInstr):
	myself = "parseCInstr()"
	strBin = "" ; comp = "" ; dest = "null" ; jump = "null" 

	# __ Check if instruction is followed by a comment and, if yes, remove it 
	nSpacePos = strCInstr.find(" ")
	if nSpacePos > 0:
		traceMsg(myself, "comment detected into [" + strCInstr + "]")
		strCInstr = strCInstr[0:nSpacePos]
		traceMsg(myself, "modified instruction [" + strCInstr + "]")

	tSplit1 = strCInstr.split("=")
	# __ If only 1 element, we are in the case : comp[;jump] 
	if len(tSplit1) == 1:
		tSplit2 = tSplit1[0].split(";")
		# __ If only 1 element, we are in the case : comp
		if len(tSplit2) == 1:
			comp = tSplit2[0]
		elif len(tSplit2) == 2:
			comp = tSplit2[0] ; jump = tSplit2[1]
		else:
			errMsg(myself, "syntax error : [" + strCInstr + "]")
			raise SyntaxError()
	# __ If 2 elements, we are in the case : dest=comp[;jump] 
	elif len(tSplit1) == 2:
		dest = tSplit1[0]
		tSplit2 = tSplit1[1].split(";")
		# __ If only 1 element, we are in the case : comp
		if len(tSplit2) == 1:
			comp = tSplit2[0]
		elif len(tSplit2) == 2:
			comp = tSplit2[0] ; jump = tSplit2[1]
		else:
			errMsg(myself, "syntax error : [" + strCInstr + "]")
			raise SyntaxError()
	# __ Else, it's an error !
	else:
		errMsg(myself, "syntax error : [" + strCInstr + "]")
		raise SyntaxError()

	# __ If we get here, comp, dest and jump are initialized :
	if jump in jumpDict:
		jumpBin = jumpDict[jump]
	else:
		errMsg(myself, "illegal jump : [" + jump + "]")
		raise SyntaxError()

	if dest in destDict:
		destBin = destDict[dest]
	else:
		errMsg(myself, "illegal dest : [" + dest + "]")
		raise SyntaxError()

	if comp in compDict:
		compBin = compDict[comp]
	else:
		errMsg(myself, "illegal comp : [" + comp + "]")
		raise SyntaxError()

	strBin = "111" + compBin + destBin + jumpBin
 
	return(strBin)

# __ Parses an 'A' instruction 
# 
# __ Source : chapter 06 p. 109
# 
# A-instruction : @value	// Where value is either a non-negative decimal 
#							// number or a symbol referring to such number.
# value (v = 0 or 1)
# 
# 		// 15   10   5    0
# 		// +----+----+----+
# Binary : 0vvvvvvvvvvvvvvv
# 
# TO DO : differentiate "decimal number" and "symbol referring to such number"
# -----------------------------------------------------------------------------
def parseAInstr(strAInstr):
	myself = "parseAInstr()"
	strBin = ""

	# __ Check if instruction is followed by a comment and, if yes, remove it 
	nSpacePos = strAInstr.find(" ")
	if nSpacePos > 0:
		traceMsg(myself, "commentaire detecte dans [" + strAInstr + "]")
		strAInstr = strAInstr[0:nSpacePos]
		traceMsg(myself, "instruction modifiee [" + strAInstr + "]")

	strArg = strAInstr[1:]

	# __ If integer argument, it's a literal address :
	if strArg.isdigit():
		nAddress = int(strArg)
		try:
			strAddress = dec2bin(nAddress, 15)
		except:
			errMsg(myself, "decimal - binary conversion failure !")
			raise SyntaxError()
		else:
			strBin = "0" + strAddress
	else:
		# __ Else, we look into the symbols table :		
		if strArg in predefSymbols:
			strBin = predefSymbols[strArg]		
		# __ If the symbol was not found, we consider it to be a variable ("Any 
		# symbol Xxx appearing in an assembly program that is not predeﬁned and 
		# is not deﬁned elsewhere using the (Xxx) command is treated as a 
		# variable. Variables are mapped to consecutive memory locations as 
		# they are ﬁrst encountered, starting at RAM address 16"). 
		else:
			traceMsg(myself, "symbol [" + strArg + "] not found : adding variable...")
			strBin = addVar(strArg)
			traceMsg(myself, "variable [" + strArg + "] linked to address [" + strBin + "]...")

	return(strBin)

# __ Parses a line of the source file.
def parseLine(asmLine):
	myself = "parseLine()" ; strBin = ""

	if asmLine[0:2] == "//" or asmLine == "":
		traceMsg(myself, "comment or empty line...")
	elif asmLine[0:1] == "@":
		try:
			strBin = parseAInstr(asmLine)
		except:		
			errMsg(myself, "parseAInstr() failure on [" + asmLine + "] !")
			raise SyntaxError()
	elif asmLine[0:1] == "(":
		traceMsg(myself, "label (handled during 1st pass)...")
	else:
		try:
			strBin = parseCInstr(asmLine)
		except:
			errMsg(myself, "parseCInstr() failure on [" + asmLine + "] !")
			raise SyntaxError()
	return strBin

# __ Checks a label syntax. Chapter 06 p. 108 quote : "A user-deﬁned symbol can 
# be any sequence of letters, digits, underscore (_), dot (.), dollar sign ($), 
# and colon (:) that does not begin with a digit."
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

# __ chapter 6 lecture slide 31 quote :
# "The (label) directive defines the symbol label to refer to the memory 
# location holding the next instruction in the program, which corresponds to 
# the instruction’s line number."
# For example, in the following code extract, the assembler must associate the 
# LOOP label to address 4 :
# 
# line		instruction
# -----		--------------------------------
# 2			@sum
# 3			M=0
# (LOOP)
# 			// if i>R0 goto STOP
# 4			@i
# 
# 
def addLabel(label, line):
	myself = "addLabel()" ; rc = 0
	# __ The label must be unique !
	if label in predefSymbols:
		errMsg(myself, "duplicate label [" + label + "] line " + str(line) + " !")
		rc = 1
	else:
		# __ No reason for dec2bin() to fail with line so we do not use a try 
		# block. 
		predefSymbols[label] = dec2bin(line)

	return(rc)	

#  __ Adds a variable to the symbols table. This function adds the variable to 
# the symbols dictionary, associating it with the binary value of the global 
# variable g_nVarAddress (the return value). It then increments this global 
# variable and returns its value. At the moment this function is created, it is 
# only called by parseAInstr() if the variable has not been found in the 
# symbols table. Therefore, there is no need to check if the variable already 
# exists.
def addVar(varName):
	global g_nVarAddress 	
	myself = "addVar()"
	traceMsg(myself, "adding variable [" + varName + "]...")
	traceMsg(myself, "target address [" + str(g_nVarAddress) + "]")
	strBin = dec2bin(g_nVarAddress)
	traceMsg(myself, "strBin = " + strBin)
	predefSymbols[varName] = strBin
	g_nVarAddress += 1

	return(strBin)

# ====================================================================== Main :
myself = os.path.basename(__file__)

# __ Globale du niveau d'information :
g_nTraceLevel = TRACE_LEVEL

if (len(sys.argv) < 2):
	errMsg(myself, "missing file name !")
	exit(1)

inputFile = sys.argv[1]

try:
	fInput = open(inputFile)
except:
	errMsg(myself, "failed to open " + inputFile + " !")
	exit(2)

# __ Global containing the next address to use for variable declaration (see 
# § 6.2.3) :
g_nVarAddress = 16

# __ First pass to get all the labels :
nLine = 0
# __ nInstrLine increased only from one instruction to another :
nInstrLine = 0
nErrCount = 0
strLabel = ""
# __ We can have several labels one after the other !
labelList = []
infoMsg(myself, "first pass...")
for l in fInput:
	nLine += 1
	line=l.strip()
	if line[0:1] == "(":
		if line[-1] != ")":
			errMsg(myself, "incomplete label line " + str(nLine) + " !")
			nErrCount += 1
			continue
		strLabel = line[1:len(line)-1]
		traceMsg(myself, "label [" + strLabel + "] line " + str(nLine))
		# __ Label syntax  ok ?
		if labelCheck(strLabel) != 0:
			errMsg(myself, "incorrect label !")
			strLabel = ""
			nErrCount += 1
			continue
		# __ We can have several labels one after the other :
		labelList.append(strLabel)
		traceMsg(myself, "labels count in current list : " + str(len(labelList)))	
	elif line[0:2] == "//" or line == "":
		traceMsg(myself, "comment or empty line at line number " + str(nLine))	
	else:
		traceMsg(myself, "instruction at line " + str(nLine) + ", instruction number : " + str(nInstrLine))
		for label in labelList:
			# __ Try to add the label to the list of known symbols :
			if addLabel(label, nInstrLine) != 0:
				errMsg(myself, "failed to add label [" + label + "] line " + str(nInstrLine) + " !")	
				nErrCount += 1
				continue
			else:
				traceMsg(myself, "label [" + label + "] associated to line" + str(nInstrLine) + " !")
		labelList.clear()
		nInstrLine += 1

if nErrCount > 0:
	infoMsg(myself, "at leat one error found during first pass !")
	fInput.close()
	exit(nErrCount)

# __ Second pass :
fInput.seek(0)

outFile = os.path.splitext(inputFile)[0] + ".hack"
fOut = open(outFile, "w")

nLine = 0
nRC = 0 
infoMsg(myself, "second pass...")
for l in fInput:
	nLine += 1
	line=l.strip()
	try:
		strBin = parseLine(line)
		if strBin != "":
			traceMsg(myself, "[" + line + "] converted to [" + strBin + "]")
			fOut.write(strBin + "\n")
	except:
		errMsg(myself, "failed to parse [" + line + "] line " + str(nLine) + " !")
		nErrCount += 1
fInput.close()
fOut.close()

if nErrCount == 0:
	infoMsg(myself, "result in " + outFile)

exit(nErrCount)
