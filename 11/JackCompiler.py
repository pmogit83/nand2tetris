# =============================================================================
#
# ------------------------------------------------------------------- Syntax :
# See JackCompiler.bat
#
# ------------------------------------------------------------------ Versions :
# 	NB : Only Major.Minor level is indicated here (see SCRIPT_VERSION below).
#
# 	- V0.1 (21/07/24) : Initial version.
# 		. V0.1.1 (22/09/24) : Alignment with JackParser.py correction = added
# 		'this' line in the symbol table for method declarations.
# 		. V0.1.2 (01/11/24) : Counting local variables in
# 		parseSubroutineBody() for later generation of VM code for function 
#		declarations.
# 		. V0.1.3 (01/11/24) : Generation of code 'function clsName.fName N'
# 		with clsName = class name, fName = function name, and N = number of
# 		local variables in the function [N01].
# 		. V0.1.4 (23/02/25) : Generation of code for string literals.
# 		. V0.1.5 (02/03/25) : First attempt at implementing code generation for 
#		expression terms (see p. 17).
# 		. V0.1.6 (20/04/25) : Modification of nextToken().
# 		. V0.1.7 (20/04/25) : Compilation of arithmetic expressions.
# 		. V0.1.8 (27/04/25) : Attempt to handle "do" and "let".
# 		. V0.1.9 (01/05/25) : Cleanup and minor improvements.
# 		. V0.1.10 (01/05/25) : Added 'while' and handling of array element 
#		assignments.
# 		. V0.1.11 (02/05/25) : Added 'return'.
# 		. V0.1.12 (02/05/25) : Refactored parseTerm() code for identifiers.
# 		. V0.1.13 (04/05/25) : Post-Compilation additions for ComplexArrays / 
#		handling 'if'.
# 		. V0.1.14 (04/05/25) : Post-Compilation additions for ComplexArrays / 
#		handling function calls.
# 		. V0.1.15 (08/05/25) : Handling ConvertToBin.
# 		. V0.1.16 (09/05/25) : Handling Square.
# 		. V0.1.17 (10/05/25) : Continuation of Square and trace of VM code 
#		addition with reporter feedback.
# 		. V0.1.18 (18/05/25) : Continuation of Square, method declaration.
# 		. V0.1.19 (24/05/25) : Fixed bug in constructor declaration.
# 		. V0.1.20 (24/05/25) : Fixed bug in symbol table management.
# 		. V0.1.21 (29/05/25) : Fixed bug in parseStatements() seen in 
#		ComplexArrays [do Main.fill(a, 10)].
# 		. V0.1.22 (29/05/25) : Fixed bug in WHILE_END* label (NB : bug detected 
#		by VMEmulator).
# 		. V0.1.23 (29/05/25) : Fixed bugs revealed by Pong compilation,
# 		mainly missing calls to the standard library, especially this one 
#		appearing during Main class compilation :
# 			parseStatements(), Trace, Type of id PongGame = []
# 			kindToSegment(), Error, Unsupported identifier type : 0
# 			writeVMCode(), Trace, parseStatements() => 
#				adding VM code [push unknown 0]
# 			writeVMCode(), Trace, parseStatements() => 
#				adding VM code [call .newInstance 1]
# 		The bug comes from the fact that we check if PongGame belongs to the 
#		list of already identified classes ['Ball', 'Bat', 'Main'], which is 
#		missing PongGame !
# 		. V0.1.24 (30/05/25) : Fixed bug in Pong, in the following block,
# 		"push pointer 0" should come before "push local 0" :
# 				push local 0
# 				push local 1
# 				push pointer 0
# 				call Ball.setDestination 3
# 		NB : Jack code = do setDestination(newx, newy);
# 		See if needed https://tinyurl.com/2n8tnp49 regarding "push pointer 0"
# 		. V0.1.25 (31/05/25) : Fixed bugs in Perso\Exemple_forum + refactored 
#		parseSubCall().
# 	- V0.2 (08/06/25) : Since yesterday, version V0.1.25 correctly compiles the 
#		following 7 projects in Perso : Average, ComplexArrays, Pong,
# 		ConvertToBin, Exemple_forum, Seven, and Square. By "correctly", we mean 
#		first that the generated VM files are not always
# 		strictly identical to the original VM files, but the differences are in 
#		control instructions (if and while) : the labels and
# 		how tests are done generally differ from the original version (probably 
#		because the original code is optimized). And second,
# 		that each project runs as expected in the VM emulator 
#		(tools\VMEmulator.bat). Version 0.2 is mainly a cleanup and 
#		optimization of V0.1.25 code.
# 		. V0.2.1 (08/06/25) : Removed useless code.
#
# =============================================================================

# Example : sys.argv
import sys

# Example : myself = os.path.basename(__file__)
import os

# Example : g_strNS = pathlib.Path(jackFilePath).stem
import pathlib

# Example : jackList = glob.glob(arg1 + "\*" + JACKEXT)
import glob

# __ V0.1 :
from typing import NamedTuple

# Example : xmlTree = etree.parse(xmlFile)
from lxml import etree

# ========================================================= Pseudo-constants :

# __ Version numbers : Major.Minor.Revision
SCRIPT_VERSION = "0.2.1"

ERR_LEVEL = 1
INFO_LEVEL = 2
TRACE_LEVEL = 3
MSGSEP = ", "
XMLEXT = ".xml"
VMEXT = ".vm"
JACKEXT = ".jack"
NULLCHAR = "\0"

# --- Token types :
NULLTOKEN = 0
UNKNOWNTOKEN = 1
KWTOKEN = 2
SYMTOKEN = 3
INTTOKEN = 4
STRTOKEN = 5
IDTOKEN = 6
# __ V0.2 :
BEGINSUBDECL = 10
ENDSUBDECL = 11
BEGINCLSVARDECL = 12
ENDCLSVARDECL = 13
BEGINPARAMLST = 14
ENDPARAMLST = 15
BEGINSUBBODY = 16
ENDSUBBODY = 17
BEGINVARDECL = 18
ENDVARDECL = 19
BEGINSTMTS = 20
ENDSTMTS = 21
BEGINWHILESTMT = 22
ENDWHILESTMT = 23
BEGINIFSTMT = 24
ENDIFSTMT = 25
BEGINRTNSTMT = 26
ENDRTNSTMT = 27
BEGINLETSTMT = 28
ENDLETSTMT = 29
BEGINDOSTMT = 30
ENDDOSTMT = 31
BEGINEXPR = 32
ENDEXPR = 34
BEGINTERM = 35
ENDTERM = 36
BEGINEXPRLST = 37
ENDEXPRLST = 38

# __ V0.0.1 :
BEGINPROGTOKEN = 98
ENDPROGTOKEN = 99

# __ V0.2 :
BEGINTAG = 0
ENDTAG = 1

# __ V0.5 :
TOKENDECL = "declared"
TOKENUSED = "used"

JackCharset = {
	32: " ",
	33: "!",
	34: "\"",
	35: "#",
	36: "$",
	37: "%",
	38: "&",
	39: "'",
	40: "(",
	41: ")",
	42: "*",
	43: "+",
	44: ",",
	45: "-",
	46: ".",
	47: "/",
	48: "0",
	49: "1",
	50: "2",
	51: "3",
	52: "4",
	53: "5",
	54: "6",
	55: "7",
	56: "8",
	57: "9",
	58: ":",
	59: ";",
	60: "<",
	61: "=",
	62: ">",
	63: "?",
	64: "@",
	65: "A",
	66: "B",
	67: "C",
	68: "D",
	69: "E",
	70: "F",
	71: "G",
	72: "H",
	73: "I",
	74: "J",
	75: "K",
	76: "L",
	77: "M",
	78: "N",
	79: "O",
	80: "P",
	81: "Q",
	82: "R",
	83: "S",
	84: "T",
	85: "U",
	86: "V",
	87: "W",
	88: "X",
	89: "Y",
	90: "Z",
	91: "[",
	92: "\\",
	93: "]",
	94: "^",
	95: "_",
	96: "`",
	97: "a",
	98: "b",
	99: "c",
	100: "d",
	101: "e",
	102: "f",
	103: "g",
	104: "h",
	105: "i",
	106: "j",
	107: "k",
	108: "l",
	109: "m",
	110: "n",
	111: "o",
	112: "p",
	113: "q",
	114: "r",
	115: "s",
	116: "t",
	117: "u",
	118: "v",
	119: "w",
	120: "x",
	121: "y",
	122: "z",
	123: "{",
	124: "|",
	125: "}",
	126: "~",
	127: "DEL",
	128: "newLine",
	129: "backSpace",
	130: "leftArrow",
	131: "upArrow",
	132: "rightArrow",
	133: "downArrow",
	134: "home",
	135: "end",
	136: "pageUp",
	137: "pageDown",
	138: "insert",
	139: "delete",
	140: "esc",
	141: "f1",
	142: "f2",
	143: "f3",
	144: "f4",
	145: "f5",
	146: "f6",
	147: "f7",
	148: "f8",
	149: "f9",
	150: "f10",
	151: "f11",
	152: "f12"
}

# --- V0.4.2 and later (added tokenOrigin, etc.) => revised in V0.5. 
# Quote from §11.4 :
# "Presently, whenever an identifier is encountered in the source code, say
# foo, the syntax analyzer outputs the XML line <identifier> foo </identifier>.
# Instead, extend your syntax analyzer to output the following information
# about each identifier :
# - name
# - category (field, static, var, arg, class, subroutine)
# - index : if the identifier’s category is field, static, var, or arg, the
# running index assigned to the identifier by the symbol table
# - usage : whether the identifier is presently being declared (for example,
# the identifier appears in a static / field / var Jack variable declaration)
# or used (for example, the identifier appears in a Jack expression)"

class token_t(NamedTuple):
	tokenValue: str
	tokenType: int
	tokenOrigin: str
	tokenUsage: str
	tokenCategory: str
	tokenIndex: int

# ---- Syntax :
kwSet = { "class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this",  "let", "do", "if", "else", "while", "return" }

symbolSet = { "{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~" }

# ---- Symbol table constants :

# 	1 : Scope level = class or sub
# 	2 : Scope name = class name or sub name (e.g., Point or distance)
# 	3 : Identifier name (e.g., x or other)
# 	4 : Identifier type (e.g., int or Point)
# 	5 : Identifier kind (e.g., field or arg)
# 	6 : Identifier index (e.g., 0 or 1)

# __ Column IDs :
STCOLSCOPEID = 0	# Scope id, int, allowed values : STCLASS or STSUB
STCOLSCOPENAME = 1	# Scope name, str, example : "distance"
STCOLIDNAME = 2		# Id name, str, example : "other"
STCOLIDTYPE = 3		# Id type, str, example : "Point"
STCOLIDKIND = 4		# Id kind, int, allowed values : STSTATIC, STFIELD,
					# STVAR or STARG
STCOLIDINDEX = 5	# Id index, int

# __ Values for certain columns :
STNONE = 0		# Unknown scope id or kind id
STCLASS = 1		# Scope = class
STSUB = 2		# Scope = sub
STSTATIC = 1	# Kind = static class var
STFIELD = 2		# Kind = class field
STVAR = 3		# Kind = sub variable
STARG = 4		# Kind = sub argument

SCOPELIB = [ "none", "class", "sub" ]
KINDLIB = [ "none", "static class var", "class field", "sub var", "sub arg" ]

# __ Empty element :
VOIDELT = [ STNONE, "", "", "", STNONE, 0 ]

# ----------------------------------------------------------------- Functions :

# __ Converts an identifier kind to a segment name (to be validated !!!!) :
def kindToSegment(nKind):
	segment = "inconnu"
	if nKind == STSTATIC:
		segment = "static"
	elif nKind == STFIELD:
		# segment = "this or that ???" See 11.1.1 "Handling variables"
		segment = "this"
	elif nKind == STVAR:
		segment = "local"
	elif nKind == STARG:
		segment = "argument"
	else:
		errMsg("kindToSegment()", "Unsupported identifier kind : " + str(nKind))

	return segment

# __ Returns the Jack code of the character in parameter if it exists, -1 otherwise.
def jackCharCode(argChar):
	retVal = -1
	# for jackCode, jackChar in JackCharset.items() :
	for jackCode in JackCharset:
		if JackCharset[jackCode] == argChar:
			retVal = jackCode
			break
	return(retVal)

# __ Displays the entire symbol table. In V0.1.16, symTableDisp() accepts an
# optional parameter indicating a symbol scope. In other words, a filter
# on the STCOLSCOPEID column (which can be STCLASS or STSUB).
def symTableDisp(*args):
	myself = "symTableDisp()"

	nScopeId = STNONE
	tblDescr = "-------- Displaying the entire symbol table " + "(" + str(len(g_SymTable)) + " line(s)) :"
	if len(args) > 0:
		nScopeId = int(args[0])
		if nScopeId == STSUB:
			tblDescr = "-------- Displaying the symbol table at sub level :"
		elif nScopeId == STCLASS:
			tblDescr = "-------- Displaying the symbol table at class level :"
		else:
			nScopeId = STNONE
			errMsg(myself, "Argument [" + args[0] + "] not supported !")

	nMaxClsSub = 17
	nMaxId = 10
	for e in g_SymTable:
		if len(e[STCOLSCOPENAME]) > nMaxClsSub: nMaxClsSub = len(e[STCOLSCOPENAME])
		if len(e[STCOLIDNAME]) > nMaxId: nMaxId = len(e[STCOLIDNAME])

	print(tblDescr)
	strLine = "scope | " + "class or sub name".ljust(nMaxClsSub, ' ') + " | "
	strLine = strLine + "identifier".ljust(nMaxId, ' ') + " | "
	strLine = strLine + "id type     | id kind          | id index"
	print(strLine)
	strLine = "----- | " + "-----------------".ljust(nMaxClsSub, '-') + " | "
	strLine = strLine + "----------".ljust(nMaxId, '-') + " | "
	strLine = strLine + "----------- | ---------------- | --------"
	print(strLine)

	for e in g_SymTable:
		if e[STCOLSCOPEID] == nScopeId or nScopeId == STNONE:
			# 5 = len("class") :
			strLine = f"{SCOPELIB[e[STCOLSCOPEID]]:<5}"

			if e[STCOLSCOPENAME] == "":
				strLine = strLine + " | \"\"               "
			else:
				strLine = strLine + " | " + e[STCOLSCOPENAME].ljust(nMaxClsSub, ' ')

			if e[STCOLIDNAME] == "":
				strLine = strLine + " | \"\"        "
			else:
				strLine = strLine + " | " + e[STCOLIDNAME].ljust(nMaxId, ' ')

			if e[STCOLIDTYPE] == "":
				strLine = strLine + " | \"\"         "
			else:
				strLine = strLine + " | " + f"{e[STCOLIDTYPE]:<11}"

			if e[STCOLIDKIND] == "":
				strLine = strLine + " | \"\"         "
			else:
				strLine = strLine + " | " + f"{KINDLIB[e[STCOLIDKIND]]:<16}"

			strLine = strLine + " | " + str(e[STCOLIDINDEX])
			print(strLine)

	return

# __ Returns the number of fields in a class :
def getFieldsCount(className):
	nCount = 0

	for e in g_SymTable:
		if e[STCOLSCOPEID] == STCLASS and e[STCOLSCOPENAME] == className and e[STCOLIDKIND] == STFIELD:
			nCount += 1

	return nCount

# __ Finds an element at a given level (sub or class). Returns emptyElt if not found :
def symTableLevelFind(nLevel, idName):
	for e in g_SymTable:
		if e[STCOLSCOPEID] == nLevel and e[STCOLIDNAME] == idName:
			return e
	return VOIDELT

# __ Searches for an element at the sub level, then at the class level, and returns
# emptyElt if not found :
def symTableFind(idName):
	e = symTableLevelFind(STSUB, idName)
	if e[STCOLSCOPEID] == STNONE:
		e = symTableLevelFind(STCLASS, idName)
	return e

# __ Adds the identifier strIdName of type strIdType and kind idKind at
# level nLevel = STCLASS or STSUB, found in the class or subroutine nameInScope.
def symTableAdd(nLevel, nameInScope, strIdName, strIdType, idKind):
	global g_SymTable

	nIndex = 0

	for e in g_SymTable:
		if e[STCOLSCOPEID] == nLevel and e[STCOLIDKIND] == idKind:
			nIndex += 1

	traceMsg("symTableAdd()", "Adding '" + strIdName + "' at level " + SCOPELIB[nLevel] + " (" + nameInScope + "), type " + strIdType + ", kind '" + KINDLIB[idKind] + "', index " + str(nIndex) + "...")
	g_SymTable.append([ nLevel, nameInScope, strIdName, strIdType, idKind, nIndex ])

	return nIndex

# __ Clears symbols at the class or sub level. Uses a temporary table to keep the global table intact in the first for loop
# (otherwise it gets lost !).
def symTableClear(nLevel):
	global g_SymTable
	tempTable = []

	traceMsg("symTableClear()", "Clearing the symbol table at level " + SCOPELIB[nLevel] + "...")

	for e in g_SymTable:
		if e[STCOLSCOPEID] == nLevel:
			tempTable.append(e)

	for e in tempTable:
		g_SymTable.remove(e)

	tempTable.clear()

	return

# ---- Access to fields of the token_t class

def getTOrigin():
	return g_Token.tokenOrigin

def getTUsage():
	return g_Token.tokenUsage

def getTIndex():
	return g_Token.tokenIndex

def getTCategory():
	return g_Token.tokenCategory

def getTVal():
	return g_Token.tokenValue

def getTType():
	return g_Token.tokenType

def setTokenValue(strVal):
	global g_Token
	g_Token = g_Token._replace(tokenValue = strVal)
	return

def setTokenType(nType):
	global g_Token
	g_Token = g_Token._replace(tokenType = nType)
	return

def setTokenOrigin(strOrigin):
	global g_Token
	g_Token = g_Token._replace(tokenOrigin = strOrigin)
	return

def setTokenUsage(strUsage):
	global g_Token
	g_Token = g_Token._replace(tokenUsage = strUsage)
	return

def setTokenIndex(nIndex):
	global g_Token
	g_Token = g_Token._replace(tokenIndex = nIndex)
	return

def setTokenCategory(strCategory):
	global g_Token
	g_Token = g_Token._replace(tokenCategory = strCategory)
	return

# __ ... end of access functions for token_t class fields

# Converts an XML tag to a token type :
def xmlTag2TokenType(tag):
	if tag == "NULL":
		return NULLTOKEN
	elif tag == "inconnu":
		return UNKNOWNTOKEN
	elif tag == "keyword":
		return KWTOKEN
	elif tag == "symbol":
		return SYMTOKEN
	elif tag == "integerConstant":
		return INTTOKEN
	elif tag == "stringConstant":
		return STRTOKEN
	elif tag == "identifier":
		return IDTOKEN
	elif tag == "end_of_prog":
		return ENDPROGTOKEN
	elif tag == "tokens":
		return BEGINPROGTOKEN
	else:
		return UNKNOWNTOKEN

# __ Recognizes an identifier = a token of type IDTOKEN and a value
# corresponding to that of an identifier.
def MatchId(strOrigin, strCategory, strUsage, nIndex):
	myself = "MatchId()"

	if getTType() == IDTOKEN:
		# Valid value ?
		if getTVal().isidentifier():
			# __ V0.4.2 :
			setTokenOrigin(strOrigin)
			setTokenCategory(strCategory)
			setTokenUsage(strUsage)
			setTokenIndex(nIndex)
			# __ V0.2 :
			if getTType() != BEGINPROGTOKEN:
				g_tokenList.append(g_Token)
			nextToken()
		else:
			handleErr(myself, tokenDescr() + " is not an identifier !")
	else:
		handleErr(myself, "identifier [" + getTVal() + "] is invalid !")

	return

# __ Recognizes a token = a type + a value :
def Match(nType, strValue):
	myself = "Match()"

	if getTType() == nType and getTVal() == strValue:
		if getTType() != BEGINPROGTOKEN:
			g_tokenList.append(g_Token)
		nextToken()
	else:
		argToken = token_t(strValue, nType, "", "", "", 0)
		handleErr(myself, "expected token : " + tokenDescr(argToken) + ", current token : " + tokenDescr() + " !")

	return

# __ Reads the next token (see test3.bis.py for debugging) :
def nextToken():
	myself = "nextToken()"

	global g_Token, g_Iter

	try:
		token = next(g_Iter)

		if token.text is None:
			traceMsg(myself, "tag [" + token.tag + "] (contains no text)")
		else:
			if token.text.isprintable():
				g_Token = token_t("", NULLTOKEN, "", "", "", 0)
				setTokenType(xmlTag2TokenType(token.tag))
				setTokenValue(token.text)
				traceMsg(myself, "token : " + tokenDescr() + "...")
			else:
				traceMsg(myself, "tag [" + token.tag + "] (non-printable text)")
	except StopIteration:
		traceMsg(myself, "StopIteration exception detected...")
		g_Token = token_t("", NULLTOKEN, "", "", "", 0)
		setTokenType(xmlTag2TokenType("end_of_prog"))
		setTokenValue("")

	return

# __ Returns true if the current token corresponds to the definition of a type :
# 'int' | 'char' | 'boolean' | className
def isType():

	if getTType() == KWTOKEN:
		if getTVal() in { "int", "boolean", "char" }:
			return True
		else:
			return False
	elif getTType() == IDTOKEN:
		# Check class name ?
		return True
	else:
		return False

# __ V0.5.* : returns the name of the type
# type : 'int' | 'char' | 'boolean' | className
def parseType():
	myself = "parseType()"
	strType = ""

	if getTType() == KWTOKEN:
		strType = getTVal()
		if strType in { "int", "boolean", "char" }:
			Match(KWTOKEN, strType)
		else:
			handleErr(myself, strType + " not recognized ! Expected : char, int or boolean")
	# If not one of the 3 basic types, it must be a class name :
	elif getTType() == IDTOKEN:
		# Check class name ?
		strType = getTVal()
		MatchId(myself, "class", TOKENDECL, 0)
	else:
		handleErr(myself, "Unrecognized type : " + tokenDescr() + " !")

	return strType

# Class variable declaration :
# 	classVarDec : ('static' | 'field') type varName (',' varName)* ';'
# V0.4, by construction [see parseClass()] we already know the type of
# declaration = static or field :
def parseClassVarDecl(classVarType):

	# A declaration starts with 'static' or 'field'. NB : we know we will
	# encounter one of these 2 tokens by construction, see parseClass() :
	Match(KWTOKEN, classVarType)
	# Type of the variable list :
	strType = parseType()
	# We must have at least one variable and we assume a static declaration by default :
	nKindId = STSTATIC
	if classVarType == "field": nKindId = STFIELD
	nIndex = symTableAdd(STCLASS, g_ClassName, getTVal(), strType, nKindId)
	MatchId(myself, classVarType, TOKENDECL, nIndex)
	traceMsg("parseClassVarDecl()", "Token : " + tokenDescr())

	# We can then have a list of other variables :
	while getTVal() == ",":
		Match(SYMTOKEN, ",")
		nIndex = symTableAdd(STCLASS, g_ClassName, getTVal(), strType, nKindId)
		MatchId(myself, classVarType, TOKENDECL, nIndex)

	# The list must end with a ';' :
	Match(SYMTOKEN, ";")

	return

# ------------------------------------------------------------ subroutineCall :
# 							 subroutineName '(' expressionList ')' |
# (className | varName) '.' subroutineName '(' expressionList ')'
#
# So there are 3 possible cases :
# Case 1 : subroutineName '(' expressionList ')'
# Case 2 : className '.' subroutineName '(' expressionList ')'
# Case 3 : varName '.' subroutineName '(' expressionList ')'
#
# - A subroutine call with a simple name (i.e., without mention of the '.' separator)
# must be considered as a method call of the current class.
# - If the subroutine name is in the format ident.sub, then the compiler
# must look in the symbol table to see if it finds a variable
# associated with this identifier. If yes, it must consider that it is a call to
# a method of the class associated with the identifier. If no variable is
# found, it is assumed to be a class identifier and that sub is
# a function of this class.
#
# strName must contain className, varName, or subroutineName => it's a name !
def parseSubCall(strName):
	myself = "parseSubCall()"

	traceMsg(myself, "className, varName or subroutineName = [" + strName + "]")

	# strVal contains the token that follows className, varName, or subroutineName
	# so '(' or '.' :
	nType = getTType() ; strVal = getTVal()

	className = "" ; subName = ""
	# nArg is an integer that allows, if needed, to increase by 1 the number
	# of arguments of the call :
	nArg = 0
	# Case 2 or Case 3 ?
	if strVal == ".":
		Match(SYMTOKEN, ".")
		subName = getTVal()
		MatchId(myself, "subroutine", TOKENUSED, 0)
		# className or varName ?
		e = symTableFind(strName)
		if e[STCOLSCOPEID] == STNONE:
			# Case 2 :
			traceMsg(myself, "Case 2 : [" + strName + "] is not a variable so a class : processing call to function " + subName + "() of this class")
			className = strName
		else:
			# Case 3 :
			className = e[STCOLIDTYPE]
			traceMsg(myself, "Case 3 : [" + strName + "] is a variable : processing call to method " + subName + "() of the class associated with this variable = " + className)
			idTypeName = e[STCOLIDTYPE]
			if not idTypeName in { "int", "boolean", "char", "void" }:
				segment = kindToSegment(e[STCOLIDKIND])
				writeVMCode(myself, "push " + segment + " " + str(e[STCOLIDINDEX]))
				nArg = 1
	elif strVal == "(":
		# Case 1 :
		className = g_ClassName
		subName = strName
		traceMsg(myself, "Case 1 : [" + strName + "] is a variable : processing call to method " + subName + "() of the current class = " + className)
		nArg = 1
		writeVMCode(myself, "push pointer 0")
	else:
		handleErr(myself, "Unexpected token [" + strVal + "] !")

	# In all cases we must find '(' here :
	Match(SYMTOKEN, "(")
	nExpr = parseExprList()
	Match(SYMTOKEN, ")")

	if className in { "Math", "String", "Array", "Output", "Array", "Screen", "Keyboard", "Memory", "Sys" }:
		writeStdLibCode(myself, className, subName)
	else:
		writeVMCode(myself, "call " + className + "." + subName + " " + str(nExpr + nArg))

	return

# term : integerConstant | stringConstant | keywordConstant | varName |
# varName '[' expression ']' | subroutineCall | '(' expression ')' |
# unaryOp term
def parseTerm():
	myself = "parseTerm()"

	traceMsg(myself, "Token at start of function : " + tokenDescr())

	nType = getTType() ; termVal = getTVal()

	# integerConstant ?
	if nType == INTTOKEN:
		Match(INTTOKEN, termVal)
		writeVMCode(myself, "push constant " + termVal)
	# stringConstant ?
	elif nType == STRTOKEN:
		Match(STRTOKEN, termVal)
		writeVMCode(myself, "push constant " + str(len(termVal)))
		writeStdLibCode(myself, "String", "new")
		for c in termVal:
			charCode = jackCharCode(c)
			if charCode < 0:
				handleErr(myself, "Unexpected character in constant string : [" + c + "] ! ")
			else:
				writeVMCode(myself, "push constant " + str(charCode))
				writeStdLibCode(myself, "String", "appendChar")
	# keywordConstant ?
	elif nType == KWTOKEN:
		# ATTENTION : keywordConstant : 'true' | 'false' | 'null' | 'this'
		if termVal in { "true", "false", "null", "this" }:
			Match(KWTOKEN, termVal)
			if termVal == "true":
				writeVMCode(myself, "push constant 0")
				writeVMCode(myself, "not")
			elif termVal == "false":
				writeVMCode(myself, "push constant 0")
			elif termVal == "null":
				# See lecture p. 20 / 104 :
				writeVMCode(myself, "push constant 0")
			else:
				# See lecture p. 20 / 104 :
				writeVMCode(myself, "push pointer 0")
		else:
			handleErr(myself, "Unexpected keyword : [" + termVal + "] ! ")
	# Complication here because an ID can correspond to multiple cases :
	#	varName													: case 1
	#	varName '[' expression ']'								: case 2
	# 	subName'('exprLst')'			# subroutineCall		: case 3
	#	clsName'.'subName(exprLst)		# subroutineCall		: case 4
	#	varName'.'subName(exprLst)		# subroutineCall		: case 5
	elif nType == IDTOKEN:
		traceMsg(myself, "Token before MatchId() : " + tokenDescr())
		MatchId(myself, getTCategory(), TOKENUSED, getTIndex())
		traceMsg(myself, "Token after MatchId() : " + tokenDescr())
		# case 2 : '[' expression ']' ?
		if getTVal() == "[":
			e = symTableFind(termVal)
			if e[STCOLSCOPEID] == STNONE:
				handleErr(myself, "Undeclared array : [" + termVal + "] ! ")
			else:
				scope = SCOPELIB[e[STCOLSCOPEID]]
				traceMsg(myself, "The id '" + termVal + "' exists at level " + scope + " in the symbol table...")
				segment = kindToSegment(e[STCOLIDKIND])
				Match(SYMTOKEN, "[")
				parseExpr()
				Match(SYMTOKEN, "]")
				# V0.1.10 to validate !
				writeVMCode(myself, "push " + segment + " " + str(e[STCOLIDINDEX]))
				writeVMCode(myself, "add")
				writeVMCode(myself, "pop pointer 1")
				writeVMCode(myself, "push that 0")
		# case 3 : '('exprLst')' ?
		elif getTVal() == "(":
			parseSubCall(termVal)
		# case 4 or 5 : '.'subName(exprLst) ?
		elif getTVal() == ".":
			parseSubCall(termVal)
		# case 1 : varName
		else:
			e = symTableFind(termVal)
			if e[STCOLSCOPEID] == STNONE:
				handleErr(myself, "Undeclared variable : [" + termVal + "] ! ")
			else:
				scope = SCOPELIB[e[STCOLSCOPEID]]
				traceMsg(myself, "The id '" + termVal + "' exists at level " + scope + " in the symbol table...")
				segment = kindToSegment(e[STCOLIDKIND])
				writeVMCode(myself, "push " + segment + " " + str(e[STCOLIDINDEX]))
	# '(' expression ')' ?
	elif nType == SYMTOKEN and termVal == "(":
		Match(SYMTOKEN, "(")
		parseExpr()
		Match(SYMTOKEN, ")")
	# unaryOp : '-' | '~'
	elif nType == SYMTOKEN and termVal in { "-", "~" }:
		Match(SYMTOKEN, termVal)
		parseTerm()
		if termVal == "-":
			writeVMCode(myself, "neg")
		else:
			writeVMCode(myself, "not")
	# Impossible case ???
	else:
		handleErr(myself, "Unexpected token : " + tokenDescr() + " ! ")

	return

# __ Returns true if the current token is an operator =>
# op : '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
def isOp():
	return (getTType() == SYMTOKEN and getTVal() in { "+", "-", "*", "/", "&", "|", "<", ">", "=" })

# See isOp() for grammar. NB: parseOp() is preceded by a call to isOp()
# which indicates if we are dealing with an operator.
def parseOp():
	Match(SYMTOKEN, getTVal())
	return

# expressionList : (expression (',' expression)*) ?
def parseExprList():
	myself = "parseExprList()"

	traceMsg(myself, "Token : " + tokenDescr())

	nType = getTType() ; strVal = getTVal()

	nExpr = 0

	# An expression list can be empty !
	# NB : The Match() of the ')' is done by the caller, see parseSubCall().
	if nType == SYMTOKEN and strVal == ")":
		return nExpr

	# Otherwise, we have at least one expression :
	parseExpr()
	nExpr += 1
	# Possibly followed by other expressions separated by commas :
	while getTType() == SYMTOKEN and getTVal() == ",":
		Match(SYMTOKEN, ",")
		parseExpr()
		nExpr += 1

	traceMsg(myself, "Parsed " + str(nExpr) + " expression(s)...")

	return nExpr

# expression : term (op term)*
def parseExpr():
	myself = "parseExpr()"

	parseTerm()

	while isOp():
		curOp = getTVal()
		traceMsg(myself, "current operator saved : [" + curOp + "]")
		parseOp()
		parseTerm()
		# __ V0.1.7 - Adds the operation corresponding to curOp (Attention :
		# unary operator "-" (to be converted to "neg") not handled !)
		if curOp == "+":
			writeVMCode(myself, "add")
		elif curOp == "-":
			writeVMCode(myself, "sub")
		elif curOp == "*":
			# See Ch. 9 "Jack Standard Library / Operating System" p. 16
			writeStdLibCode(myself, "Math", "multiply")
		elif curOp == "/":
			writeStdLibCode(myself, "Math", "divide")
		elif curOp == "&":
			writeVMCode(myself, "and")
		elif curOp == "|":
			writeVMCode(myself, "or")
		elif curOp == "<":
			writeVMCode(myself, "lt")
		elif curOp == ">":
			writeVMCode(myself, "gt")
		elif curOp == "=":
			writeVMCode(myself, "eq")
		else:
			errMsg(myself, "Warning : operator [" + curOp + "] not supported !")

	return

# statements : statement*
# statement : letStatement | ifStatement | whileStatement | doStatement |
# returnStatement
def parseStatements():
	myself = "parseStatements()"

	global g_nWhileLabel, g_nIfLabel

	nType = getTType() ; strVal = getTVal()

	while nType == KWTOKEN and strVal in { "let", "if", "while", "do", "return" }:
		if strVal == "let":
			traceMsg(myself, "Parsing 'let'...")
			Match(KWTOKEN, "let")
			strIdName = getTVal()
			# __ Search for the id in the symbol table :
			e = symTableFind(strIdName)
			if e[STCOLSCOPEID] == STNONE:
				# __ If the id is not found, there is a bug in the Jack code =>
				handleErr(myself, "identifier [" + strIdName + "] is invalid !")
			else:
				strSegment = kindToSegment(e[STCOLIDKIND])
				nIndex = e[STCOLIDINDEX]
				traceMsg(myself, "Id '" + strIdName + "' of type [" + KINDLIB[e[STCOLIDKIND]] + "] in the symbol table => segment [" + strSegment + "], index " + str(nIndex))
				MatchId(myself, "var", TOKENUSED, 0)
				if getTType() == SYMTOKEN and getTVal() == "[":
					Match(SYMTOKEN, "[")
					parseExpr()
					Match(SYMTOKEN, "]")
					# V0.1.10 - array element assignment :
					writeVMCode(myself, "push " + strSegment + " " + str(nIndex))
					writeVMCode(myself, "add")
					Match(SYMTOKEN, "=")
					parseExpr()
					Match(SYMTOKEN, ";")
					# See 11.1.6. "Compiling Arrays"
					writeVMCode(myself, "pop temp 0")
					writeVMCode(myself, "pop pointer 1")
					writeVMCode(myself, "push temp 0")
					writeVMCode(myself, "pop that 0")
				else:
					Match(SYMTOKEN, "=")
					parseExpr()
					Match(SYMTOKEN, ";")
					writeVMCode(myself, "pop " + strSegment + " " + str(nIndex))
		# ifStatement : 'if' '(' expression ')' '{' statements '}'
		# ( 'else' '{' statements '}' ) ?
		elif strVal == "if":
			nLocalIfLabel = g_nIfLabel
			g_nIfLabel += 1
			traceMsg(myself, "Parsing 'if', nLocalIfLabel = " + str(nLocalIfLabel))
			Match(KWTOKEN, "if")
			Match(SYMTOKEN, "(")
			parseExpr()
			Match(SYMTOKEN, ")")
			writeVMCode(myself, "not")
			writeVMCode(myself, "if-goto IF_FALSE" + str(nLocalIfLabel))
			Match(SYMTOKEN, "{")
			parseStatements()
			Match(SYMTOKEN, "}")
			writeVMCode(myself, "goto IF_END" + str(nLocalIfLabel))
			writeVMCode(myself, "label IF_FALSE" + str(nLocalIfLabel))
			if getTType() == KWTOKEN and getTVal() == "else":
				Match(KWTOKEN, "else")
				Match(SYMTOKEN, "{")
				parseStatements()
				Match(SYMTOKEN, "}")
			writeVMCode(myself, "label IF_END" + str(nLocalIfLabel))
		elif strVal == "while":
			nLocalWhileLabel = g_nWhileLabel
			g_nWhileLabel += 1
			traceMsg(myself, "nLocalWhileLabel = " + str(nLocalWhileLabel))
			writeVMCode(myself, "label WHILE_EXP" + str(nLocalWhileLabel))
			traceMsg(myself, "Parsing 'while'...")
			Match(KWTOKEN, "while")
			Match(SYMTOKEN, "(")
			parseExpr()
			Match(SYMTOKEN, ")")
			writeVMCode(myself, "not")
			writeVMCode(myself, "if-goto WHILE_END" + str(nLocalWhileLabel))
			Match(SYMTOKEN, "{")
			parseStatements()
			Match(SYMTOKEN, "}")
			writeVMCode(myself, "goto WHILE_EXP" + str(nLocalWhileLabel))
			writeVMCode(myself, "label WHILE_END" + str(nLocalWhileLabel))
		# doStatement : 'do' subroutineCall ';'
		elif strVal == "do":
			Match(KWTOKEN, "do")
			# Same as parseTerm(), the name of the called object is recognized here :
			calledName = getTVal()
			MatchId(myself, "subroutine", TOKENUSED, 0)
			parseSubCall(calledName)
			writeVMCode(myself, "pop temp 0")
			Match(SYMTOKEN, ";")
		# returnStatement : 'return' expression? ';'
		elif strVal == "return":
			traceMsg(myself, "Parsing 'return'...")
			Match(KWTOKEN, "return")
			if getTType() != SYMTOKEN or getTVal() != ";":
				parseExpr()
			else:
				writeVMCode(myself, "push constant 0")
			Match(SYMTOKEN, ";")
			writeVMCode(myself, "return")
		nType = getTType() ; strVal = getTVal()

	return

# Subroutine body : '{' varDec* statements '}'
# V0.1.17 :
def parseSubroutineBody(nFields):
	global g_SubName, g_SubKind, g_ClassName

	myself = "parseSubroutineBody()"

	traceMsg(myself, "Start...")

	Match(SYMTOKEN, "{")

	# varDec* : 'var' type varName (',' varName)* ';'
	nType = getTType() ; strVal = getTVal()
	nLocalVarsCount = 0
	while nType == KWTOKEN and strVal == "var":
		Match(KWTOKEN, "var")
		traceMsg(myself, "Token before parseType() : " + tokenDescr())
		strVarType = parseType()
		traceMsg(myself, "Token before 1st MatchId : " + tokenDescr())
		# __ g_SubName was initialized by parseSubDecl() :
		nIndex = symTableAdd(STSUB, g_SubName, getTVal(), strVarType, STVAR)
		nLocalVarsCount += 1
		MatchId(myself, "var", TOKENDECL, nIndex)
		# Then possibly other declarations :
		while getTVal() == ",":
			Match(SYMTOKEN, ",")
			nIndex = symTableAdd(STSUB, g_SubName, getTVal(), strVarType, STVAR)
			nLocalVarsCount += 1
			MatchId(myself, "var", TOKENDECL, nIndex)
		Match(SYMTOKEN, ";")
		nType = getTType() ; strVal = getTVal()

	traceMsg(myself, "Number of local variables in " + g_SubName + " : " + str(nLocalVarsCount))
	writeVMCode(myself, "function " + g_ClassName + "." + g_SubName + " " + str(nLocalVarsCount))

	if g_SubKind == "constructor":
		writeVMCode(myself, "push constant " + str(nFields))
		writeVMCode(myself, "call Memory.alloc 1")
		writeVMCode(myself, "pop pointer 0")
	elif g_SubKind == "method":
		# V0.1.16 (See Ch. 11.1.5.2 - "Compiling methods") :
		writeVMCode(myself, "push argument 0")
		writeVMCode(myself, "pop pointer 0")

	parseStatements()

	# End of subroutine body :
	Match(SYMTOKEN, "}")

	# __ Finished analyzing the subroutine body :
	g_SubName = ""
	g_SubKind = ""

	traceMsg(myself, "End...")

	return

# Subroutine declaration :
# ('constructor' | 'function' | 'method') ('void' | type) subroutineName
# '(' parameterList ')' subroutineBody
def parseSubDecl():
	global g_SubName, g_SubKind

	myself = "parseSubDecl()"

	traceMsg(myself, "Begin...")

	symTableClear(STSUB)

	nFields = 0

	# We know we will encounter one of these 3 tokens by construction, see
	# parseClass() :
	g_SubKind = getTVal()
	if g_SubKind == "constructor":
		Match(KWTOKEN, "constructor")
		nFields = getFieldsCount(g_ClassName)
		traceMsg(myself, "Compiling constructor of class [" + g_ClassName + "] => " + str(nFields) + " field(s)...")
	elif g_SubKind == "function":
		Match(KWTOKEN, "function")
	else:
		Match(KWTOKEN, "method")

	traceMsg(myself, "Before 'void' | type...")

	# 'void' | type :
	nType = getTType() ; strVal = getTVal()
	if nType == KWTOKEN and strVal == "void":
		Match(KWTOKEN, "void")
	elif nType == KWTOKEN and isType():
		strType = parseType()
	elif nType == IDTOKEN:
		MatchId(myself, "subroutine", TOKENDECL, 0)
	else:
		handleErr(myself, tokenDescr() + " not recognized ! Expected : 'void' or type !")

	traceMsg(myself, "After 'void' | type...")

	# __ V0.5.* : save the sub name in a global for symbol table management :
	g_SubName = getTVal()
	traceMsg(myself, "Current sub : " + g_SubName)

	# __ V0.6.1 :
	if g_SubKind == "method":
		nIndex = symTableAdd(STSUB, g_SubName, "this", g_ClassName, STARG)
		# Check that the index is 0 !
		if nIndex != 0:
			handleErr(myself, "Non-zero index for 'this' in the symbol table of " + g_SubName + "() !")

	MatchId(myself, "subroutine", TOKENDECL, 0)
	Match(SYMTOKEN, "(")

	# parameterList : ((type varName) (',' type varName)*)?
	# Reminder : '?' => 0 or 1
	# Duplicate code with parseType() !
	if isType():
		strType = parseType()
		# If we recognized a type, we must have a variable :
		nIndex = symTableAdd(STSUB, g_SubName, getTVal(), strType, STARG)
		MatchId(myself, "arg", TOKENDECL, nIndex)
		# Then possibly other declarations :
		while getTVal() == ",":
			Match(SYMTOKEN, ",")
			strType = parseType()
			nIndex = symTableAdd(STSUB, g_SubName, getTVal(), strType, STARG)
			MatchId(myself, "arg", TOKENDECL, nIndex)

	# End of parameterList :
	Match(SYMTOKEN, ")")

	traceMsg(myself, "Before parseSubroutineBody()...")

	parseSubroutineBody(nFields)

	traceMsg(myself, "End...")

	symTableDisp()

	return

# __ Analyzes a Jack program, i.e., a class followed by a name and a block :
# 'class' className '{' classVarDec* subroutineDec* '}'
def parseClass():
	global g_ClassName

	myself = "parseClass()"

	symTableClear(STSUB)
	symTableClear(STCLASS)

	# The first token must correspond to the <tokens> tag which is not part of
	# the language, so we read the next one :
	nextToken()

	# Temporary solution :
	Match(KWTOKEN, "class")

	g_ClassName = getTVal()
	traceMsg(myself, "Parsing class g_ClassName = [" + g_ClassName + "]")
	MatchId(myself, "class", TOKENDECL, 0)

	# Opening brace :
	Match(SYMTOKEN, "{")

	# classVarDec* :
	nType = getTType() ; strVal = getTVal()
	while nType == KWTOKEN and strVal in { "static", "field" }:
		parseClassVarDecl(strVal)
		nType = getTType() ; strVal = getTVal()

	# subroutineDec* :
	nType = getTType() ; strVal = getTVal()
	while nType == KWTOKEN and strVal in { "constructor", "function", "method" }:
		parseSubDecl()
		nType = getTType() ; strVal = getTVal()

	# End of class declaration :
	Match(SYMTOKEN, "}")

	traceMsg(myself, "End...")

	return

# Parsing a token XML tree :
def parseTree(xmlTokens):
	myself = "parseTree()"

	global g_Iter

	traceMsg(myself, "Initializing g_Iter...")
	g_Iter = xmlTokens.iter()

	traceMsg(myself, "Reading first token...")
	nextToken()

	parseClass()

	traceMsg(myself, "End...")

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
	elif nType == BEGINPROGTOKEN:
		return "beginning_of_prog"
	elif nType == ENDPROGTOKEN:
		return "end_of_prog"
	elif nType == BEGINSUBDECL:
		return "subroutineDec"
	elif nType == ENDSUBDECL:
		return "/subroutineDec"
	elif nType == BEGINCLSVARDECL:
		return "classVarDec"
	elif nType == ENDCLSVARDECL:
		return "/classVarDec"
	elif nType == BEGINPARAMLST:
		return "parameterList"
	elif nType == ENDPARAMLST:
		return "/parameterList"
	elif nType == BEGINSUBBODY:
		return "subroutineBody"
	elif nType == ENDSUBBODY:
		return "/subroutineBody"
	elif nType == BEGINVARDECL:
		return "varDec"
	elif nType == ENDVARDECL:
		return "/varDec"
	elif nType == BEGINSTMTS:
		return "statements"
	elif nType == ENDSTMTS:
		return "/statements"
	elif nType == BEGINWHILESTMT:
		return "whileStatement"
	elif nType == ENDWHILESTMT:
		return "/whileStatement"
	elif nType == BEGINIFSTMT:
		return "ifStatement"
	elif nType == ENDIFSTMT:
		return "/ifStatement"
	elif nType == BEGINRTNSTMT:
		return "returnStatement"
	elif nType == ENDRTNSTMT:
		return "/returnStatement"
	elif nType == BEGINLETSTMT:
		return "letStatement"
	elif nType == ENDLETSTMT:
		return "/letStatement"
	elif nType == BEGINDOSTMT:
		return "doStatement"
	elif nType == ENDDOSTMT:
		return "/doStatement"
	elif nType == BEGINEXPR:
		return "expression"
	elif nType == ENDEXPR:
		return "/expression"
	elif nType == BEGINTERM:
		return "term"
	elif nType == ENDTERM:
		return "/term"
	elif nType == BEGINEXPRLST:
		return "expressionList"
	elif nType == ENDEXPRLST:
		return "/expressionList"
	else:
		return "unknown type: " + str(nType)

# Current token in readable format. In V0.0.2, the default token is the
# current one, but a token can be passed to the function.
def tokenDescr(*args):

	if len(args) > 0:
		token = args[0]
	else:
		token = g_Token

	tokenValue = token.tokenValue
	if token.tokenType == BEGINPROGTOKEN:
		tokenValue = "tag <tokens>"

	return "'" + token2XMLTag(token.tokenType) + "'" + " [" + tokenValue + "]"

# __ Opens and initializes the VM file. If successful, returns 0 and initializes
# the global g_VMFileHandle. Returns 1 otherwise.
def openVMFile(vmFile, xmlSrc):
	myself = "openVMFile()"
	global g_VMFileHandle

	traceMsg(myself, "opening for writing [" + vmFile + "]...")
	try:
		g_VMFileHandle = open(vmFile, "w")
	except Exception as e:
		handleErr(myself, "failed to open " + vmFile + " for writing !")
		return 1

	strTitle = "VM code generated by " + os.path.basename(__file__)
	strTitle = strTitle + " V" + SCRIPT_VERSION
	strTitle = strTitle + " from " + xmlSrc

	return 0

# __ Adds a comment to the VM file. Adds a newline.
def writeVMComment(vmComment):
	traceMsg("writeVMComment", "Old VM comment [" + vmComment + "]")
	return 0

# __ Adds code to the VM file. Adds a newline if needed.
def writeVMCode(askedBy, vmCode):
	traceMsg("writeVMCode()", askedBy + " => adding VM code [" + vmCode + "]")
	if not vmCode.endswith("\n"):
		vmCode = vmCode + "\n"
	g_VMFileHandle.write(vmCode)
	return 0

# __ Adds "Jack Standard Library / Operating System" code (see Ch. 9 p. 16).
def writeStdLibCode(askedBy, className, funcName):
	myself = "writeStdLibCode()"
	# Indicates whether the class and function are handled :
	bHandled = False

	# ------------------------------------------------------------------ Math :
	if className == "Math":
		if funcName == "multiply":
			bHandled = True ; nArgs = 2
		elif funcName == "divide":
			bHandled = True ; nArgs = 2
		elif funcName == "abs":
			bHandled = True ; nArgs = 1
	# ---------------------------------------------------------------- String :
	elif className == "String":
		if funcName == "new":
			bHandled = True ; nArgs = 1
		elif funcName == "appendChar":
			bHandled = True ; nArgs = 2
	# ----------------------------------------------------------------- Array :
	elif className == "Array":
		if funcName == "new":
			bHandled = True ; nArgs = 1
		else:
			writeVMComment("To do : handle function '" + className + "." + funcName + "()'...")
	# ---------------------------------------------------------------- Output :
	elif className == "Output":
		if funcName == "printInt":
			bHandled = True ; nArgs = 1
		elif funcName == "printString":
			bHandled = True ; nArgs = 1
		elif funcName == "println":
			bHandled = True ; nArgs = 0
		elif funcName == "moveCursor":
			bHandled = True ; nArgs = 2
	# ---------------------------------------------------------------- Screen :
	elif className == "Screen":
		if funcName == "setColor":
			bHandled = True ; nArgs = 1
		elif funcName == "drawRectangle":
			bHandled = True ; nArgs = 4
		elif funcName == "clearScreen":
			bHandled = True ; nArgs = 0
	# -------------------------------------------------------------- Keyboard :
	elif className == "Keyboard":
		if funcName == "readInt":
			bHandled = True ; nArgs = 1
		elif funcName == "keyPressed":
			bHandled = True ; nArgs = 0
	# ---------------------------------------------------------------- Memory :
	elif className == "Memory":
		if funcName == "peek":
			bHandled = True ; nArgs = 1
		elif funcName == "poke":
			bHandled = True ; nArgs = 2
		elif funcName == "deAlloc":
			bHandled = True ; nArgs = 1
	# ------------------------------------------------------------------- Sys :
	elif className == "Sys":
		if funcName == "wait":
			bHandled = True ; nArgs = 1
	# ------------------------------------------------------- Unknown class :
	else:
		errMsg(myself, "Unknown class : [" + className + "] !")

	if bHandled:
		writeVMCode(askedBy, "call " + className + "." + funcName + " " + str(nArgs))
	else:
		errMsg(myself, "Standard library call '" + className + "." + funcName + "()' not supported !")

	return

# __ Closes the VM file.
def closeVMFile():
	# global g_VMFileHandle
	g_VMFileHandle.close()
	return 0

# __ Returns the description of a message level :
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
	return

# __ Displays an error :
def errMsg(who, msg):
	msgOut(who, ERR_LEVEL, msg)
	return

# __ Displays a trace :
def traceMsg(who, msg):
	msgOut(who, TRACE_LEVEL, msg)
	return

# __ Displays an info :
def infoMsg(who, msg):
	msgOut(who, INFO_LEVEL, msg)
	return

# __ Error handling : g_nErrCount counter + display.
def handleErr(who, msg):
	global g_nErrCount
	g_nErrCount += 1
	errMsg(who, msg)
	return

# =============================================================================
# 								Script start
# =============================================================================
myself = os.path.basename(__file__)

# __ Global information level :
g_nTraceLevel = TRACE_LEVEL

infoMsg(myself, "starting version V" + SCRIPT_VERSION)

if (len(sys.argv) < 2):
	errMsg(myself, "file or directory name is required !")
	infoMsg(myself, "WARNING : prefer Unix-style paths !")
	exit(1)

arg1 = sys.argv[1]

jackDir = ""

# __ V0.5.9 => loop over .jack files instead of .xml files to fix a bug
# revealed by processing the Pong project.
if os.path.isdir(arg1):
	traceMsg(myself, arg1 + " is a directory !")
	# __ Fill jackList with the names of Jack files in the directory
	jackList = glob.glob(arg1 + "\*" + JACKEXT)
	# __ No need to continue if the list is empty :
	if len(jackList) == 0:
		errMsg(myself, "no *" + JACKEXT + " files in " + arg1 + " !")
		exit(5)
	jackDir = arg1
elif os.path.isfile(arg1):
	fileExt = pathlib.Path(arg1).suffix
	traceMsg(myself, arg1 + " is a file with extension [" + fileExt + "]...")
	if fileExt != JACKEXT:
		errMsg(myself, JACKEXT + " extension expected !")
		exit(3)
	jackList = [arg1]
	jackDir = pathlib.Path(arg1).parent
else:
	errMsg(myself, arg1 + " is neither a Jack file nor a directory !")
	infoMsg(myself, "WARNING : prefer Unix-style paths !")
	exit(2)

traceMsg(myself, "jackDir = [" + jackDir + "]")
jackDirPath = pathlib.Path(jackDir)

# __ Here, we should have a jackList containing at least one element and
# each element is of the form source_name.jack. We deduce the xmlTList
# containing the elements source_nameT.xml
xmlTList = []
for jackFile in jackList:
	xmlTFile = os.path.splitext(jackFile)[0] + "T" + XMLEXT
	xmlTList.append(xmlTFile)
	# __ Check that all files exist, exit otherwise :
	if not(os.path.isfile(xmlTFile)):
		errMsg(myself, xmlTFile + " not found for " + jackFile + " !")
		infoMsg(myself, "Reminder : these files are created by JackTokenizer.py")
		exit(3)

traceMsg(myself, str(len(xmlTList)) + " XML file(s) to process :")
traceMsg(myself, str(xmlTList))

g_nErrCount = 0
nXMLCount = 0
# __ Counters for 'while' and 'if' labels :
g_nWhileLabel = 0
g_nIfLabel = 0

g_SymTable = []

# __ Loop through XML files :
for xmlTFile in xmlTList:
	# __ Current class and sub names :
	g_ClassName = ""
	g_SubName = ""
	g_SubKind = ""
	nXMLCount += 1
	try:
		infoMsg(myself, "Reading [" + xmlTFile + "]...")
		vmOutFile = os.path.splitext(xmlTFile)[0][0:-1] + VMEXT
		traceMsg(myself, "Saving code in " + vmOutFile)
		if openVMFile(vmOutFile, xmlTFile) == 0:
			xmlTree = etree.parse(xmlTFile)
			g_tokenList = []
			traceMsg(myself, "Calling parseTree() on an etree with " + str(len(xmlTree.xpath(".//*"))) + " descendants...")
			parseTree(xmlTree)
			symTableDisp()
			closeVMFile()
		else:
			g_nErrCount += 1
			errMsg(myself, "Problem opening " + vmOutFile + " !")
	except Exception as e:
		g_nErrCount += 1
		errMsg(myself, "exception [" + str(e) + "] while processing [" + xmlTFile + "] !?")

infoMsg(myself, str(nXMLCount) + " XML file(s) processed, " + str(g_nErrCount) + " error(s)")

exit(g_nErrCount)
