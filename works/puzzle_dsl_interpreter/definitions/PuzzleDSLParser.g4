parser grammar PuzzleDSLParser;

options {
	tokenVocab = PuzzleDSLLexer;
	language = Python3;
}

// -----------------------------------------------------------------------------------------

// root context
file:
	structsDeclaration structDefinitions domainHiddenDeclaration domainDefinitions
		constraintsDeclaration constraintsDefinitions;

// -----------------------------------------------------------------------------------------

// Declation Context
structsDeclaration: STRUCTS_DECLARATION;
domainHiddenDeclaration: DOMAIN_HIDDEN_DECLARATION;
constraintsDeclaration: CONSTRAINTS_DECLARATION;

// -----------------------------------------------------------------------------------------

// Structs Context
structID: P | C | EP | EC | NEW_STRUCT_ID;
newStructID: NEW_STRUCT_ID;
structDefinitionBody:
	COMBINE LPAREN structID COMMA relationshipSet RPAREN;
structDefinition:
	INDENT newStructID ASSIGN structDefinitionBody SEMI;
structDefinitions: structDefinition*;

// relationship
relationshipID: H | V | D;
relationshipSetBody: relationshipID (COMMA relationshipID)*;
relationshipSet: LCURLY relationshipSetBody RCURLY;

// -----------------------------------------------------------------------------------------

// Domain Hidden Context

// Predefined Struct ID
pID: P;
cID: C;
epID: EP;
ecID: EC;

// domain

// assignable Value (in domain)
intDomainValue:
	(WIDTH | HEIGHT) (PLUS | MINUS | TIMES) (WIDTH | HEIGHT)
	| (WIDTH | HEIGHT) (PLUS | MINUS | TIMES) intDomainValue
	| WIDTH
	| HEIGHT
	| intDomainValue (PLUS | MINUS | TIMES) (WIDTH | HEIGHT)
	| NUMBER;
rangeValue: intDomainValue DOTS (intDomainValue | INF);
domainValue: intDomainValue | rangeValue | NULL | CONSTANT_ID;

domainSetBody: domainValue (COMMA domainValue)*;
domainSet: LCURLY domainSetBody RCURLY;

// hidden

// assignable Value (in hidden)
hiddenValue: domainValue | UNDECIDED;

hiddenSetBody: hiddenValue (COMMA hiddenValue)*;
hiddenSet: LCURLY hiddenSetBody RCURLY;

// definition body
domainDefinitionBody: domainSet RIGHT_ARROW hiddenSet;

// definition expressions
pDefinition: (
		INDENT pID LEFT_RIGHT_ARROW domainDefinitionBody SEMI
	);
cDefinition: (
		INDENT cID LEFT_RIGHT_ARROW domainDefinitionBody SEMI
	);
epDefinition: (
		INDENT epID LEFT_RIGHT_ARROW domainDefinitionBody SEMI
	);
ecDefinition: (
		INDENT ecID LEFT_RIGHT_ARROW domainDefinitionBody SEMI
	);
customStructDefinition: (
		INDENT newStructID LEFT_RIGHT_ARROW domainDefinitionBody SEMI
	);

domainDefinitions:
	pDefinition cDefinition epDefinition ecDefinition (
		customStructDefinition
	)*;

// -----------------------------------------------------------------------------------------

// Constraints Context

// value
int:
	NUMBER
	| WIDTH
	| HEIGHT
	| solutionFunction
	| crossFunction
	| cycleFunction
	| indexFunction
	| PIPE set PIPE
	| int (PLUS | MINUS | TIMES) int;

primitiveValue: int | solutionFunction | NULL | CONSTANT_ID;

set:
	INTEGER
	| bFunction
	| structElement
	| connectFunction
	| generationSet;

// heuristic function
solutionFunction: SOLUTION LPAREN structElement RPAREN;
bFunction: B LPAREN structID RPAREN;
crossFunction: CROSS LPAREN structElement RPAREN;
cycleFunction: CYCLE LPAREN structElement RPAREN;
allDifferentFunction: ALL_DIFFERENT LPAREN structElement RPAREN;
isRectangleFunction: IS_RECTANGLE LPAREN structElement RPAREN;
isSquareFunction: IS_SQUARE LPAREN structElement RPAREN;
connectFunction:
	CONNECT LPAREN structElement COMMA relationshipSet RPAREN;
noOverlapFunction:
	NO_OVERLAP LPAREN newStructID (COMMA newStructID)* RPAREN;
fillFunction:
	FILL LPAREN newStructID (COMMA newStructID)* RPAREN;

quantifier: (ALL | EXISTS) LPAREN BOUND_VARIABLE RPAREN IN (set);

index: BOUND_VARIABLE (SUBSET | IN) set;

quantifierIndex:
	quantifier COMMA LPAREN (index | quantifierIndex) RPAREN;

//index function (summation or production)
indexFunction:
	(SUM | PRODUCT) LCURLY (index | quantifierIndex) RCURLY LPAREN int RPAREN;

// generation variables
structElement: BOUND_VARIABLE;

generationSet: LCURLY BOUND_VARIABLE PIPE constraint RCURLY;

boolean:
	fillFunction
	| noOverlapFunction
	| allDifferentFunction
	| set (SUBSET | IN) set
	| primitiveValue IN set
	| isSquareFunction
	| isRectangleFunction
	| set (NOTEQUAL | EQUAL) (set | EMPTYSET)
	| primitiveValue (NOTEQUAL | EQUAL) primitiveValue;

singleBoolean: (
		boolean
		| notBoolean
		| parenthesizedBoolean
		| quantifierBoolean
	);

notBoolean: NOT LPAREN compoundBoolean RPAREN;

parenthesizedBoolean: LBRACKET compoundBoolean RBRACKET;

quantifierBoolean:
	quantifier COMMA LPAREN compoundBoolean RPAREN;

compoundBoolean:
	singleBoolean (
		(AND | OR | THEN | EQUIVALENT) (singleBoolean)
	)*;

// constraint definitions
constraint: compoundBoolean;
constraintDefinition: (INDENT constraint SEMI);
constraintsDefinitions: constraintDefinition+;
