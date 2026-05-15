# =============================================================================
# Description: Takes a Jack source as input and extracts a description in XML 
# format.
# Example from "Project 10.pdf":
#
# Jack: let quit = "yes";
#
# XML:
# 	<keyword> let </keyword>
# 	<identifier> quit </identifier>
# 	<symbol> = </symbol>
# 	<stringConstant> yes </stringConstant>
# 	<symbol> ; </symbol>
#
# ---------------------------------------------------------------- Validation:
#
# 1. After conversion, we should find 1 or more *T.xml files corresponding to
# the source(s) in the input directory:
#
# 	C:\(...)\nand2tetris\projects\10>JackTokenizer.bat Perso\ArrayTest =>
# 	creates Perso\ArrayTest\MainT.xml
#
# 2. Comparison (from C:\(...)\nand2tetris\projects\10):
#
# call ..\..\tools\TextComparer.bat Perso\ArrayTest\MainT.xml ArrayTest\MainT.xml
# Comparison failure in line 21:
# <inconnu></inconnu>
# <symbol>,</symbol>
#
# ------------------------------------------------------------------ Versions:
# 	NB: The Major.Minor level is indicated here (see SCRIPT_VERSION below).
# 	However, try to change the revision with each script modification while saving.
#
# 	- V0.0 (XX/09/23): Initial version.
# 	- V0.1 (17/09/23): Attempt to add a structure for tokens using NamedTuple.
# 	- V0.2 (23/09/23): Processing of the following Jack files OK :
# 		Perso\Test01\Main.jack, ArrayTest, ExpressionLessSquare, Square
#
# =============================================================================

# Example: sys.argv
import sys

# Example: myself = os.path.basename(__file__)
import os

# Example: g_strNS = pathlib.Path(jackFilePath).stem
import pathlib

# Example: jackList = glob.glob(arg1 + "\*" + JACKEXT)
import glob

# __ V0.1:
from typing import NamedTuple

# ========================================================= Pseudo-constants:

# __ Version numbers: Major.Minor.Revision
SCRIPT_VERSION = "0.2.3"

ERR_LEVEL = 1
INFO_LEVEL = 2
TRACE_LEVEL = 3
MSGSEP = ", "
JACKEXT = ".jack"
XMLEXT = ".xml"
NULLCHAR = "\0"

# --- Token types:
NULLTOKEN = 0
UNKNOWNTOKEN = 1
KWTOKEN = 2
SYMTOKEN = 3
INTTOKEN = 4
STRTOKEN = 5
IDTOKEN = 6
ENDPROGTOKEN = 99

# --- V0.1 (Class name => epeire/types.h):
class token_t(NamedTuple):
    tokenValue: str
    tokenType: int

# ---- Syntax:
kwSet = { "class", "constructor", "function", "method", "field", "static",  "var", "int", "char", "boolean", "void", "true", "false", "null", "this",  "let", "do", "if", "else", "while", "return" }

symbolSet = { "{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~" }

# ----------------------------------------------------------------- Functions:

# Indicates if the string contains an integer between 0 and 32767:
def isValidInt(strValue):
	if strValue.isdigit():
		if len(strValue) < 6:
			nValue = int(strValue)
			if nValue > 32767:
				return False
		else:
			return False
	else:
		return False
	return True

# Returns a buffer containing an entire Jack file.
def readJackFile(strFilePath):
	myself = "readJackFile()"
	strBuffer = ""
	traceMsg(myself, "reading [" + strFilePath + "]...")
	try:
		fInput = open(strFilePath)
		strBuffer = fInput.read()
		traceMsg(myself, "closing [" + strFilePath + "]...")
		fInput.close()
	except:
		errMsg(myself, "problem opening or reading " + strFilePath + " !")

	return strBuffer

# Reads the next character in the input buffer or NULLCHAR at the end of the buffer.
def readChar():
	myself = "readChar()"
	global g_nBufferPtr, g_strLook, g_jackBuffer

	g_strLook = NULLCHAR
	if g_nBufferPtr < len(g_jackBuffer):
		g_strLook = g_jackBuffer[g_nBufferPtr]
		g_nBufferPtr += 1
		# For the case where g_strLook contains '\n':
		strDisp = g_strLook
		if g_strLook == "\n":
			strDisp = "<LF>"
		traceMsg(myself, "g_strLook = [" + strDisp + "], g_nBufferPtr = " + str(g_nBufferPtr))

	return

# Skip spaces:
def skipWhite():
	global g_strLook
	while (g_strLook.isspace() and g_strLook != NULLCHAR):
		readChar()
	return

# Reads the next non-white character in the input buffer:
def getNoWhiteChar():
	readChar()
	skipWhite()
	return

# Indicates if the current token is a symbol or a keyword (or neither)
# based on its value:
def setTokenTypeFromValue():
	global g_Token

	setTokenType(UNKNOWNTOKEN)
	if g_Token.tokenValue in kwSet:
		setTokenType(KWTOKEN)

	return

# Skip a comment:
def skipComment():
	myself = "skipComment()"
	global g_strLook, g_nBufferPtr, g_jackBuffer

	# 2 possible cases:
	if g_strLook == "/":
		traceMsg(myself, "removing single-line comment...")
		while g_strLook != "\n" and g_strLook != NULLCHAR:
			readChar()
	else:
		traceMsg(myself, "removing multi-line comment...")
		# NB: In C, "nested comments" are not allowed. Assume the same in Jack...
		nPos = g_jackBuffer.find("*/", g_nBufferPtr)
		if nPos < 0:
			# Analysis should stop on this kind of error !
			errMsg(myself, "multi-line comment without termination !?")
		else:
			# g_nBufferPtr = nPos + 1
			g_nBufferPtr = nPos + 2
			readChar()

	return

# Processes a /: either the division operator or the start of a comment.
def scanSlash():
	myself = "scanSlash()"
	global g_strLook, g_Token

	# Need to read the next character to know:
	readChar()
	if g_strLook == "/" or g_strLook == "*":
		skipComment()
	else:
		traceMsg(myself, "division operator...")
		# Add '/' directly since g_strLook no longer contains it !
		tokenValuePush("/")
		setTokenType(SYMTOKEN)

	return

# Scans a string:
def scanString():
	myself = "scanString()"
	global g_strLook, g_Token

	readChar()
	while g_strLook != "\"" and g_strLook != "\n":
		tokenValuePush()
		readChar()

	# Unfinished string?
	if g_strLook == "\n":
		setTokenType(UNKNOWNTOKEN)
		errMsg(myself, "unfinished string [" + g_Token.tokenValue + "] !")
	else:
		setTokenType(STRTOKEN)
		traceMsg(myself, "string detected: [" + g_Token.tokenValue + "]...")

	readChar()

	return

# Reads a name. A name can be a keyword or an identifier. An identifier
# is a sequence of letters, digits, and '_' not starting with a digit
# [Ref.: Ch. 10 p. 8]. Keywords are in kwSet.
def scanName():
	myself = "scanName()"
	global g_strLook, g_Token

	while g_strLook.isalnum() or g_strLook == "_":
		tokenValuePush()
		readChar()

	setTokenTypeFromValue()
	# If the token type is still unknown, it's an identifier:
	if g_Token.tokenType == UNKNOWNTOKEN:
		setTokenType(IDTOKEN)

	return

# Reads a single-character operator (unlike what we have in scanOp() in scanner.c !).
def scanSymbol():
	myself = "scanSymbol()"
	traceMsg(myself, "scanning [" + g_strLook + "]...")
	tokenValuePush()
	setTokenType(SYMTOKEN)
	readChar()

	return

# Reads an integer in the range [0, 32767].
def scanInt():
	myself = "scanInt()"
	global g_strLook, g_Token

	while g_strLook.isdigit():
		tokenValuePush()
		readChar()

	if isValidInt(g_Token.tokenValue):
		setTokenType(INTTOKEN)
	else:
		setTokenType(UNKNOWNTOKEN)
		errMsg(myself, "invalid integer: " + g_Token.tokenValue + " !")

	return

# __ Adds the current character to the value of g_Token.
# Uses a variable number of arguments to pass a value other than g_strLook, see scanSlash() for example:
def tokenValuePush(*argTuple):
	global g_strLook, g_Token
	if len(argTuple) > 0:
		g_Token = g_Token._replace(tokenValue = g_Token.tokenValue + argTuple[0])
	else:
		g_Token = g_Token._replace(tokenValue = g_Token.tokenValue + g_strLook)
	return

# __ Updates the type of g_Token:
def setTokenType(nType):
	global g_Token
	g_Token = g_Token._replace(tokenType = nType)
	return

# Returns the next token (function based on epeire / next()):
def nextToken():
	myself = "nextToken()"
	global g_strLook, g_Token
	traceMsg(myself, "resetting g_Token...")
	g_Token = token_t("", NULLTOKEN)
	if g_strLook.isalpha() or g_strLook == "_":
		scanName()
	elif g_strLook.isdigit():
		scanInt()
	elif g_strLook == NULLCHAR:
		traceMsg(myself, "end of program !")
		setTokenType(ENDPROGTOKEN)
	elif g_strLook == "/":
		# __ A / can be the start of a comment (// or /*) or the division operator.
		# Be careful with the order ! This test must be placed BEFORE
		# checking if g_strLook is in symbolSet, otherwise the parser
		# will treat '/' as a symbol without checking the next character !
		traceMsg(myself, "calling scanSlash()...")
		scanSlash()
	elif g_strLook in symbolSet:
		scanSymbol()
	elif g_strLook == "\"":
		scanString()
	else:
		traceMsg(myself, "unknown token !")
		setTokenType(UNKNOWNTOKEN)
		readChar()

	skipWhite()

	traceMsg(myself, "end of nextToken()...")
	return

# __ Description: Parses each line of the input file and writes the result
# in the output file. Returns the number of errors found.
#
# References / Quotes:
# 	- "Comments are of the standard formats /* comment until closing */,
# 		/** API comment */, and // comment to end of line."
# 		[ch_10_compiler_I.pdf p. 7]
def scan():
	myself = "scan()"; nErrCount = 0

	global g_jackBuffer, g_tokenList

	# __ V0.1:
	traceMsg(myself, "initial call to getNoWhiteChar()...")
	getNoWhiteChar()
	traceMsg(myself, "initial call to nextToken()...")
	nextToken()
	# Warning: while logic slightly different from scan() !
	while g_Token.tokenType != ENDPROGTOKEN:
		# Add the token to the global list:
		if g_Token.tokenType != NULLTOKEN:
			traceMsg(myself, "adding token " + tokenDescr() + " to g_tokenList...")
			g_tokenList.append(g_Token)
		traceMsg(myself, "calling nextToken()...")
		nextToken()

	traceMsg(myself, "end of scan()...")

	return

# Converts a token type to an XML tag:
def token2XMLTag(nType):
	if nType == NULLTOKEN:
		return "NULL"
	elif nType == UNKNOWNTOKEN:
		return "inconnu"
	elif nType == KWTOKEN:
		return "keyword"
	elif nType == SYMTOKEN:
		return "symbol"
	elif nType == INTTOKEN:
		return "integerConstant"
	elif nType == STRTOKEN:
		return "stringConstant"
	elif nType == IDTOKEN:
		return "identifier"
	elif nType == ENDPROGTOKEN:
		return "end_of_prog"
	else:
		return "unknown type: " + str(nType)

# Current token in readable format:
def tokenDescr():
	global g_Token

	return "'" + token2XMLTag(g_Token.tokenType) + "'" + " [" + g_Token.tokenValue + "]"

# __ V0.1:
def saveTokenList(xmlFile):
	myself = "saveTokenList()"
	global g_tokenList

	nRC = 0

	traceMsg(myself, "opening for writing [" + xmlFile + "]...")
	try:
		fXML = open(xmlFile, "w")
	except Exception as e:
		errMsg(myself, "failed to open " + xmlFile + " for writing !")
		return 1

	fXML.write("<tokens>\n")

	for token in g_tokenList:
		if token.tokenValue == "<":
			strXMLValue = "&lt;"
		elif token.tokenValue == ">":
			strXMLValue = "&gt;"
		elif token.tokenValue == "\"":
			strXMLValue = "&quot;"
		elif token.tokenValue == "&":
			strXMLValue = "&amp;"
		else:
			strXMLValue = token.tokenValue
		fXML.write("\t<" + token2XMLTag(token.tokenType) + ">" + strXMLValue + "</" + token2XMLTag(token.tokenType) + ">\n")

	fXML.write("</tokens>")

	traceMsg(myself, "closing [" + xmlFile + "]...")
	fXML.close()

	return 0

# __ Returns the description of a message level:
def levelDesc(level):
	if level == ERR_LEVEL:
		return("Error")
	elif level == INFO_LEVEL:
		return("Info")
	elif level == TRACE_LEVEL:
		return("Trace")
	else:
		return("???")

# __ Display a message:
def msgOut(who, level, msg):
	if level <= g_nTraceLevel:
		print(who + MSGSEP + levelDesc(level) + MSGSEP + msg)
	return

# __ Display an error:
def errMsg(who, msg):
	msgOut(who, ERR_LEVEL, msg)
	return

# __ Display a trace:
def traceMsg(who, msg):
	msgOut(who, TRACE_LEVEL, msg)
	return

# __ Display an info:
def infoMsg(who, msg):
	msgOut(who, INFO_LEVEL, msg)
	return

# ====================================================================== Main:
myself = os.path.basename(__file__)

# __ Global information level:
g_nTraceLevel = TRACE_LEVEL

infoMsg(myself, "starting version V" + SCRIPT_VERSION)

if (len(sys.argv) < 2):
	errMsg(myself, "file or directory name is required !")
	exit(1)

arg1 = sys.argv[1]

# __ File or directory?
if os.path.isdir(arg1):
	traceMsg(myself, arg1 + " is a directory !")
	# __ Fill jackList with the names of Jack files in the directory
	jackList = glob.glob(arg1 + "\*" + JACKEXT)
	# __ No need to continue if the list is empty:
	if len(jackList) == 0:
		errMsg(myself, "no " + JACKEXT + " files in " + arg1 + " !")
		exit(5)
elif os.path.isfile(arg1):
	fileExt = pathlib.Path(arg1).suffix
	traceMsg(myself, arg1 + " is a file with extension [" + fileExt + "] !")
	if fileExt != JACKEXT:
		errMsg(myself, JACKEXT + " extension expected !")
		exit(3)
	jackList = [arg1]
else:
	errMsg(myself, arg1 + " is neither a JACK file nor a directory !")
	exit(2)

traceMsg(myself, str(len(jackList)) + " JACK file(s) to process:")
traceMsg(myself, str(jackList))

nErrCount = 0
nJACKCount = 0

# __ Loop through Jack files:
for jackFile in jackList:
	nJACKCount += 1
	try:
		infoMsg(myself, "Reading [" + jackFile + "]...")
		g_jackBuffer = readJackFile(jackFile).strip()
		if len(g_jackBuffer) == 0:
			errMsg(myself, "The file seems empty !")
			nErrCount += 1
			continue
		g_nBufferPtr = 0
		g_strLook = NULLCHAR
		g_tokenList = []
		traceMsg(myself, "Calling scan() on a buffer of " + str(len(g_jackBuffer)) + " characters...")
		scan()
		xmlFile = os.path.splitext(jackFile)[0] + "T" + XMLEXT
		traceMsg(myself, "Saving the list of tokens in " + xmlFile)
		nRC = saveTokenList(xmlFile)
		traceMsg(myself, "RC saveTokenList() = " + str(nRC))
	except Exception as e:
		errMsg(myself, "exception [" + str(e) + "] while processing [" + jackFile + "] !?")
		nErrCount += 1

infoMsg(myself, str(nJACKCount) + " JACK file(s) processed, " + str(nErrCount) + " error(s)")

exit(nErrCount)
