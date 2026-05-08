# =============================================================================
# Description : takes JackTokenizer.py XML output as input and produces another  
# XML containing the parsing of the input. NB : the XML produced by  
# JackParser.py contains (with one exception !) the XML produced by 
# JackTokenizer.py + the tags resulting from the parsing of the input file. 
# The exception is that the root pair <tokens>...</tokens> is replaced by the 
# pair <class>...</class>.
# 
# -------------------------------------------------------------------- Syntax : 
# See JackParser.bat
#
# ---------------------------------------------------------------- Validation :
# Use validation.bat
# 
# ------------------------------------------------------------------ Versions :
#
#	- V0.0 (30/09/23) : initial version .
#	- V0.1 (31/10/23) : error handling and parser development.
#	- V0.2 (01/11/23) : output handling (cf. Ch. 10 p. 9).
#	- V0.3 (04/11/23) : final version (all tests ok) + adding functions 
#		getTVal() and getTType() for g_Token reading.
# 
# =============================================================================

# example : sys.argv
import sys

# example : myself = os.path.basename(__file__)
import os

# example : g_strNS = pathlib.Path(jackFilePath).stem
import pathlib

# example : jackList = glob.glob(arg1 + "\*" + JACKEXT)
import glob

# __ V0.1 :
from typing import NamedTuple

# example : xmlTree = etree.parse(xmlFile)
from lxml import etree

# ========================================================== Pseudo-constants :

# __ Version number : Major.Minor.Revision
SCRIPT_VERSION = "0.3.2"

ERR_LEVEL = 1
INFO_LEVEL = 2
TRACE_LEVEL = 3
MSGSEP = ", "
XMLEXT = ".xml"
NULLCHAR = "\0"

# --- Token types :
NULLTOKEN = 0
UNKNOWNTOKEN = 1
KWTOKEN = 2
SYMTOKEN = 3
INTTOKEN = 4
STRTOKEN = 5
IDTOKEN = 6

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

BEGINPROGTOKEN = 98
ENDPROGTOKEN = 99

BEGINTAG = 0
ENDTAG = 1

class token_t(NamedTuple):
    tokenValue: str
    tokenType: int

# ---- Syntax :
kwSet = { "class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this",  "let", "do", "if", "else", "while", "return" }

symbolSet = { "{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~" }

# ----------------------------------------------------------------- Functions :

# __ Returns g_Token value :
def getTVal():
	return g_Token.tokenValue

# __ Returns g_Token type :
def getTType():
	return g_Token.tokenType


# __ Updates g_Token value :
def setTokenValue(strVal):
	global g_Token
	g_Token = g_Token._replace(tokenValue = strVal)
	return

# __ Updates g_Token type : 
def setTokenType(nType):
	global g_Token
	g_Token = g_Token._replace(tokenType = nType)
	return

# Converts a token type into a XML tag :
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
	# __ V0.0.1 :
	elif tag == "tokens":
		return BEGINPROGTOKEN
	else:
		return UNKNOWNTOKEN

# __ Recognizes an identifier = a token typed IDTOKEN and a value matching  
# that of an identifier :
def MatchId():
	myself = "MatchId()"
	
	if getTType() == IDTOKEN:
		# Valid value ?
		if getTVal().isidentifier():
			if getTType() != BEGINPROGTOKEN:
				g_tokenList.append(g_Token)
			nextToken()
		else:
			handleErr(myself, tokenDescr() + " is not an identifier !")
	else:
		handleErr(myself, "the identifier [" + getTVal() + "] is invalid !")

	return

# __ Recognizes a token = a type + a value :
def Match(nType, strValue):
	myself = "Match()"
	
	if getTType() == nType and getTVal() == strValue:
		if getTType() != BEGINPROGTOKEN:
			g_tokenList.append(g_Token)
		nextToken()
	else:
		argToken = token_t(strValue, nType)
		handleErr(myself, "token expected : " + tokenDescr(argToken) + ", current token : " + tokenDescr() + " !")

	return

# __ Reads the next token :
def nextToken():
	myself = "nextToken()"

	global g_Token, g_Iter, g_tokenList

	try:
		token = next(g_Iter)
		g_Token = token_t("", NULLTOKEN)
		setTokenType(xmlTag2TokenType(token.tag))
		setTokenValue(token.text)
	except:
		g_Token = token_t("", ENDPROGTOKEN)
		setTokenType(xmlTag2TokenType("end_of_prog"))
		setTokenValue("")

	traceMsg(myself, "token : " + tokenDescr() + "...")

	return

# __ Returns true if the current token matches the definition of a type :
# 'int' | 'char' | 'boolean' | className
def isType():

	if getTType() == KWTOKEN:
		if getTVal() in { "int", "boolean", "char" }:
			return True
		else:
			return False
	elif getTType() == IDTOKEN:
		return True
	else:
		return False

# type:  'int' | 'char' | 'boolean' | className
def parseType():
	myself = "parseType()"

	if getTType() == KWTOKEN:
		if getTVal() in { "int", "boolean", "char" }:
			Match(KWTOKEN, getTVal())
		else:
			handleErr(myself, getTVal() + " unrecognized ! Expected : char, int or boolean")
	# If not one of the three base types, it must be a class name :
	elif getTType() == IDTOKEN:
		# Check class name ?
		MatchId()
		return
	else:
		handleErr(myself, "Unrecognized Type : " + tokenDescr() + " !")

	return

# Class variables declaration :
#	classVarDec:  ('static' | 'field' ) type varName (',' varName)*  ';'
def parseClassVarDec():

	addOutputTag(BEGINCLSVARDECL)

	# A declaration starts with 'static' or 'field'. NB : we know that we will  
	# get one of those 2 tokens by construction, cf. parseClass() :
	if getTVal() == "static":
		Match(KWTOKEN, "static")
	else:
		Match(KWTOKEN, "field")
	# Variables list type :
	parseType() 
	# We must have at least one variable :
	MatchId()
	# Next, we can have a list of other variables :
	while getTVal() == ",":
		Match(SYMTOKEN, ",")
		MatchId()
	# The list must end with ';' :
	Match(SYMTOKEN, ";")

	addOutputTag(ENDCLSVARDECL)

	return

# subroutineCall : 
#							 subroutineName '(' expressionList ')' | 
# ( className | varName) '.' subroutineName  '(' expressionList ')'
def parseSubCall():
	myself = "parseSubCall()"

	traceMsg(myself, "Token : " + tokenDescr())

	# NB : the ID corresponding to subroutineName, className or varName has 
	# already been recognized, cf. parseTerm().
	
	nType = getTType() ; strVal = getTVal()
	
	# We are in the case (className | varName) if we find a dot here. And, 
	# in that case, we have already recognized className or varName so we have  
	# to recognize the dot AND subroutineName :
	if nType == SYMTOKEN and strVal == ".":
		Match(SYMTOKEN, ".")
		MatchId()

	# In all cases, we must find '(' here :
	Match(SYMTOKEN, "(")
	parseExprList()
	Match(SYMTOKEN, ")")

	return

# term : integerConstant | stringConstant | keywordConstant | varName | 
#	varName '[' expression ']' | subroutineCall  | '(' expression ')' | 
#	unaryOp term
def parseTerm():
	myself = "parseTerm()"

	addOutputTag(BEGINTERM)

	traceMsg(myself, "Token : " + tokenDescr())

	nType = getTType() ; strVal = getTVal()

	# integerConstant ?
	if nType == INTTOKEN:
		Match(INTTOKEN, strVal)
	# stringConstant ?
	elif nType == STRTOKEN:
		Match(STRTOKEN, strVal)
	# keywordConstant ?
	elif nType == KWTOKEN:
		# ATTENTION : keywordConstant:  'true' | 'false' | 'null' | 'this'
		if strVal in { "true", "false", "null", "this" }:
			Match(KWTOKEN, strVal)
		else:
			handleErr(myself, "Unexpected keyword  : [" + strVal + "] ! ")
	# Difficulty here because an ID can correspond to multiple cases :
	#	varName
	#	varName '[' expression ']'
	# 	subName'('exprLst')'			# subroutineCall
	#	clsName'.'subName(exprLst)		# subroutineCall
	#	varName'.'subName(exprLst)		# subroutineCall
	elif nType == IDTOKEN:
		MatchId()
		# ID followed by a symbol ?
		if getTType() == SYMTOKEN:
			# '[' expression ']' ?
			if getTVal() == "[":
				Match(SYMTOKEN, "[")
				parseExpr()
				Match(SYMTOKEN, "]")
			elif getTVal() in { "(", "." }:
				parseSubCall()
			else:
				traceMsg(myself, "Symbol following an ID : [" + getTVal() + "] ! ")
	# '(' expression ')' ?
	elif nType == SYMTOKEN and strVal == "(":
		Match(SYMTOKEN, "(")
		parseExpr()
		Match(SYMTOKEN, ")")
	# unaryOp : '-' | '~'
	elif nType == SYMTOKEN and strVal in { "-", "~" }:
		Match(SYMTOKEN, strVal)
		parseTerm()
	# Impossible case ???
	else:
		handleErr(myself, "Unexpected token  : " + tokenDescr() + " ! ")

	addOutputTag(ENDTERM)

	return

# __ Returns true if the current token is an operator => 
# op : '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' 
def isOp():
	return (getTType() == SYMTOKEN and getTVal() in { "+", "-", "*", "/", "&", "|", "<", ">", "=" })

# Cf. isOp() for the grammar. NB : parseOp() is preceded by a call to isOp() 
# that says if we are dealing with an operator.
def parseOp():
	Match(SYMTOKEN, getTVal())
	return

# expressionList : (expression (',' expression)* )? 
def parseExprList():
	myself = "parseExprList()"

	addOutputTag(BEGINEXPRLST)

	traceMsg(myself, "Token : " + tokenDescr())

	nType = getTType() ; strVal = getTVal()

	# An expression list can be empty !
	# NB : ')' is matched by the caller, cf. parseSubCall().
	if nType == SYMTOKEN and strVal == ")":
		addOutputTag(ENDEXPRLST)
		return
	
	# Else, we have at least an expression :
	parseExpr()
	# Possibly followed by other comma separated expressions :
	while getTType() == SYMTOKEN and getTVal() == ",":
		Match(SYMTOKEN, ",")
		parseExpr()

	addOutputTag(ENDEXPRLST)

	return

# expression : term (op term)* 
def parseExpr():

	addOutputTag(BEGINEXPR)

	parseTerm()
	
	while isOp():
		parseOp()
		parseTerm()

	addOutputTag(ENDEXPR)

	return

# statements : statement*
# statement :  letStatement | ifStatement | whileStatement | doStatement | 
# returnStatement 
def parseStatements():
	myself = "parseStatements()"

	addOutputTag(BEGINSTMTS)

	nType = getTType() ; strVal = getTVal()

	while nType == KWTOKEN and strVal in { "let", "if", "while", "do", "return" } :
		if strVal == "let":
			addOutputTag(BEGINLETSTMT)
			traceMsg(myself, "Parsing 'let'...")
			Match(KWTOKEN, "let")
			MatchId()
			if getTType() == SYMTOKEN and getTVal() == "[":
				Match(SYMTOKEN, "[")
				parseExpr()
				Match(SYMTOKEN, "]")
			Match(SYMTOKEN, "=")
			parseExpr()
			Match(SYMTOKEN, ";")
			addOutputTag(ENDLETSTMT)
		# ifStatement :  'if' '(' expression ')' '{' statements '}'  
		# ( 'else' '{' statements '}' )?
		elif strVal == "if":
			addOutputTag(BEGINIFSTMT)
			traceMsg(myself, "Parsing 'if'...")
			Match(KWTOKEN, "if")
			Match(SYMTOKEN, "(")
			parseExpr()
			Match(SYMTOKEN, ")")
			Match(SYMTOKEN, "{")
			parseStatements()
			Match(SYMTOKEN, "}")
			if getTType() == KWTOKEN and getTVal() == "else":
				Match(KWTOKEN, "else")
				Match(SYMTOKEN, "{")
				parseStatements()
				Match(SYMTOKEN, "}")
			addOutputTag(ENDIFSTMT)
		# whileStatement : 'while' '(' expression ')' '{' statements '}' 
		elif strVal == "while":
			addOutputTag(BEGINWHILESTMT)
			traceMsg(myself, "Parsing 'while'...")
			Match(KWTOKEN, "while")
			Match(SYMTOKEN, "(")
			parseExpr()
			Match(SYMTOKEN, ")")
			Match(SYMTOKEN, "{")
			parseStatements()
			Match(SYMTOKEN, "}")
			addOutputTag(ENDWHILESTMT)
		# doStatement : 'do' subroutineCall ';' 
		elif strVal == "do":
			addOutputTag(BEGINDOSTMT)
			traceMsg(myself, "Parsing 'do'...")
			Match(KWTOKEN, "do")
			# Idem parseTerm(), the routine id is matched here :
			MatchId()
			parseSubCall()
			Match(SYMTOKEN, ";")
			addOutputTag(ENDDOSTMT)
		# returnStatement : 'return' expression? ';' 
		elif strVal == "return":
			addOutputTag(BEGINRTNSTMT)
			traceMsg(myself, "Parsing 'return'...")
			Match(KWTOKEN, "return")
			if getTType() != SYMTOKEN or getTVal() != ";":
				parseExpr()
			Match(SYMTOKEN, ";")
			addOutputTag(ENDRTNSTMT)
		nType = getTType() ; strVal = getTVal()

	addOutputTag(ENDSTMTS)

	return

# Function body : '{' varDec* statements '}'
def parseSubroutineBody():
	myself = "parseSubroutineBody()"

	traceMsg(myself, "Start...")

	addOutputTag(BEGINSUBBODY)

	Match(SYMTOKEN, "{")

	# varDec* : 'var' type varName (',' varName)* ';'
	nType = getTType() ; strVal = getTVal()
	while nType == KWTOKEN and strVal == "var":
		addOutputTag(BEGINVARDECL)
		Match(KWTOKEN, "var")
		# type :
		parseType()
		# varName :
		MatchId()
		# Then possibly other declarations :
		while getTVal() == ",":
			Match(SYMTOKEN, ",")
			MatchId()
		Match(SYMTOKEN, ";")
		nType = getTType() ; strVal = getTVal()
		addOutputTag(ENDVARDECL)

	parseStatements()

	# Function body end :
	Match(SYMTOKEN, "}")

	addOutputTag(ENDSUBBODY)

	traceMsg(myself, "End...")

	return	

# __ Adds a virtual token corresponing to a non-terminal. For example :
# addOutputTag("subroutineDec", BEGINTAG) and 
# addOutputTag("subroutineDec", ENDTAG) add respectively the virtual tokens  
# (BEGINSUBDECL, "") and (ENDSUBDECL, "") to g_tokenList
def addOutputTag(tokenId):
	global g_tokenList

	vToken = token_t("", tokenId)

	g_tokenList.append(vToken)
	
	return

# Function declaration :
#	('constructor' | 'function' | 'method')  ('void' | type) subroutineName 
#		'('  parameterList ')' subroutineBody
def parseSubDecl():
	myself = "parseSubDecl()"

	addOutputTag(BEGINSUBDECL)

	# We know that we are going to find one of those 3 tokens by construction, 
	# cf. parseClass() :
	if getTVal() == "constructor":
		Match(KWTOKEN, "constructor")
	elif getTVal() == "function":
		Match(KWTOKEN, "function")
	else:
		Match(KWTOKEN, "method")

	# 'void' | type :
	nType = getTType() ; strVal = getTVal()
	if nType == KWTOKEN and strVal == "void":
		Match(KWTOKEN, "void")
	elif nType == IDTOKEN:
		MatchId()
	else:
		handleErr(myself, tokenDescr() + " unrecognized ! Expected : 'void' or type !")

	# subroutineName :
	MatchId()
	Match(SYMTOKEN, "(")

	addOutputTag(BEGINPARAMLST)

	# parameterList : ( (type varName)  (',' type varName)*)?
	# Reminder : '?' => 0 or 1
	# Duplicate code with parseType() !
	if isType():
		parseType()
		# If we recognized a type, we must have a variable :
		MatchId()
		# Then possibly other declarations :
		while getTVal() == ",":
			Match(SYMTOKEN, ",")
			parseType()
			MatchId()
	
	addOutputTag(ENDPARAMLST)

	# End of parameterList :			
	Match(SYMTOKEN, ")")

	# Function body :
	parseSubroutineBody()

	addOutputTag(ENDSUBDECL)

	traceMsg(myself, "End...")

	return

# __ Analyse of a Jack program, i.e. a class followed by a name and a bloc :
#		'class' className '{' classVarDec*  subroutineDec* '}'
def parseClass():
	myself = "parseClass()"

	# The first token must correspond to the tag <tokens> which does not belong  
	# to the language. So we read the next token :
	nextToken()

	# We expect to find a class :
	# <keyword>class</keyword>
	# Ugly until something better :
	Match(KWTOKEN, "class")
	# className :
	MatchId()
	# Opening curly bracket :
	Match(SYMTOKEN, "{")

	# classVarDec* :
	nType = getTType() ; strVal = getTVal()
	while nType == KWTOKEN and strVal in { "static", "field" }:
		parseClassVarDec()
		nType = getTType() ; strVal = getTVal()

	# subroutineDec* :
	nType = getTType() ; strVal = getTVal()
	while nType == KWTOKEN and strVal in { "constructor", "function", "method" }:
		parseSubDecl()
		nType = getTType() ; strVal = getTVal()

	# End of the class declaration :
	Match(SYMTOKEN, "}")

	traceMsg(myself, "End...")

	return

# Parsing a tokens XML tree : 
def parseTree(xmlTokens):
	myself = "parseTree()"

	global g_Iter
	
	traceMsg(myself, "g_Iter initialization ...")
	g_Iter = xmlTokens.iter()
	
	traceMsg(myself, "First token reading...")
	nextToken()

	parseClass()

	traceMsg(myself, "End...")

	return

# Converts a token type to a XML tag :
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
		return "type inconnu : " + str(nType)

# Returns a readable description of a token (or the current token by default).
def tokenDescr(*args):
	
	if len(args) > 0:
		token = args[0]
	else:
		token = g_Token

	tokenValue = token.tokenValue
	if token.tokenType == BEGINPROGTOKEN:
		tokenValue = "tag <tokens>"

	return "'" + token2XMLTag(token.tokenType) + "'" + " [" + tokenValue + "]"

# __ Saves the tokens list :
def saveTokenList(xmlFile):
	myself = "saveTokenList()"
	global g_tokenList
	
	nRC = 0

	traceMsg(myself, "opening [" + xmlFile + "] for write access...")
	try:
		fXML = open(xmlFile, "w")
	except Exception as e:
		handleErr(myself, "failed to open " + xmlFile + " in write mode !")
		return 1

	fXML.write("<class>\n")

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
		if strXMLValue.strip() == "":
			fXML.write("\t<" + token2XMLTag(token.tokenType) + ">\n")
		else:
			fXML.write("\t<" + token2XMLTag(token.tokenType) + ">" + strXMLValue + "</" + token2XMLTag(token.tokenType) + ">\n")

	fXML.write("</class>")

	traceMsg(myself, "closing [" + xmlFile + "]...")
	fXML.close()

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

# __ Displays a trace message :
def traceMsg(who, msg):
	msgOut(who, TRACE_LEVEL, msg)
	return

# __ Displays an information :
def infoMsg(who, msg):
	msgOut(who, INFO_LEVEL, msg)
	return

# __ Error handling : g_nErrCount counter + display.
def handleErr(who, msg):
	global g_nErrCount
	g_nErrCount = g_nErrCount + 1
	errMsg(who, msg)
	return

# ============================================================================= 
#								Script start
# =============================================================================
myself = os.path.basename(__file__)

# __ Information level global variable :
g_nTraceLevel = TRACE_LEVEL

infoMsg(myself, "starting V" + SCRIPT_VERSION)

if (len(sys.argv) < 2):
	errMsg(myself, "missing file or directory name !")
	exit(1)

arg1 = sys.argv[1]

# __ File or directory ?
if os.path.isdir(arg1):
	traceMsg(myself, arg1 + " is a directory !")
	# __ Fill xmlTList  list with the xml file names of the directory :
	xmlTList = glob.glob(arg1 + "\*T" + XMLEXT)
	# __ No need to continue if the list is empty :
	if len(xmlTList) == 0:
		errMsg(myself, "no file *T" + XMLEXT + " in " + arg1 + " !")
		exit(5)
elif os.path.isfile(arg1):
	fileExt = pathlib.Path(arg1).suffix
	traceMsg(myself, arg1 + " is a [" + fileExt + "] extension file...")
	if fileExt != XMLEXT:
		errMsg(myself, XMLEXT + " extension expected !")
		exit(3)
	# __ *T.xml file name ?
	xmlTFile = os.path.splitext(arg1)[0]
	if not(xmlTFile.endswith("T")):
		errMsg(myself, xmlTFile + " does not have *T" + XMLEXT + " format !")
		exit(4)	
	xmlTList = [arg1]
else:
	errMsg(myself, arg1 + " is not a XML file nor a directory !")
	exit(2)

traceMsg(myself, str(len(xmlTList)) + " XML file(s) to process :")
traceMsg(myself, str(xmlTList))

g_nErrCount = 0
nXMLCount = 0

# __ xml files loop :
for xmlTFile in xmlTList:
	nXMLCount += 1
	try:
		infoMsg(myself, "Processing [" + xmlTFile + "]...")
		xmlTree = etree.parse(xmlTFile)
		g_tokenList = []
		traceMsg(myself, "Calling parseTree() on an etree with " + str(len(xmlTree.xpath(".//*"))) + " descendants...")
		parseTree(xmlTree)
		xmlOutFile = os.path.splitext(xmlTFile)[0][0:-1] + XMLEXT
		traceMsg(myself, "Saving tokens list into " + xmlOutFile)
		nRC = saveTokenList(xmlOutFile)
		traceMsg(myself, "saveTokenList() rc = " + str(nRC))
	except Exception as e:
		errMsg(myself, "exception [" + str(e) + "] during the processing of [" + xmlTFile + "] !?")

infoMsg(myself, str(nXMLCount) + " XML file(s) processed, " + str(g_nErrCount) + " error(s)")

exit(g_nErrCount)
