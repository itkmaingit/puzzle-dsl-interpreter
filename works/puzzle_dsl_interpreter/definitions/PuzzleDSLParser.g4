parser grammar PuzzleDSLParser;

options {
	tokenVocab = PuzzleDSLLexer;
	language = Python3;
}

@members {
from members.utils import validate_relationship_set, check_unique
from members.domain import validate_domain_set
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
structDefinitonBody:
	COMBINE LPAREN structID COMMA relationshipSet RPAREN;
structDefinition:
	INDENT newStructID ASSIGN structDefinitonBody SEMI;
structDefinitions: structDefinition*;

// relationship
relationshipID: H | V | D;
relationshipSetBody:
	relationshipID (COMMA relationshipID)* {
    elements = [e.getText() for e in self._ctx.relationshipID()]
    self.validate_relationship_set(elements)
};
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

domainSetBody:
	domainValue (COMMA domainValue)* {
    elements = [e.getText() for e in self._ctx.domainValue()]
    self.validate_domain_set(elements)
};
domainSet: LCURLY domainSetBody RCURLY;

// hidden

// assignable Value (in hidden)
hiddenValue: domainValue | UNDECIDED;

hiddenSetBody:
	hiddenValue (COMMA hiddenValue)* {
    elements = [e.getText() for e in self._ctx.hiddenValue()]
    self.validate_domain_set(elements)
};
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
	| productFunction
	| sumFunction
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

//general function
sumFunction:
	SUM LCURLY (generationBoundVariable COMMA)*? set (
		SUBSET
		| IN
	) set RCURLY LPAREN int RPAREN;
productFunction:
	PRODUCT LCURLY (generationBoundVariable COMMA)*? set (
		SUBSET
		| IN
	) set RCURLY LPAREN int RPAREN;

// generation variables
structElement: BOUND_VARIABLE;

generationBoundVariable: (ALL | EXISTS) LPAREN BOUND_VARIABLE RPAREN IN (
		set
	);

generationSet:
	LCURLY BOUND_VARIABLE (IN set)? PIPE constraint RCURLY;

// boolean
singleBoolBase:
	(generationBoundVariable COMMA)*? NOT? (
		fillFunction
		| noOverlapFunction
		| allDifferentFunction
		| set (SUBSET | IN) set
		| primitiveValue IN set
		| isSquareFunction
		| isRectangleFunction
		| set (NOTEQUAL | EQUAL) (set | EMPTYSET)
		| primitiveValue (NOTEQUAL | EQUAL) primitiveValue
	);

singleBool: (singleBoolBase ((THEN | EQUIVALENT) singleBool)?)
	| LBRACKET (singleBoolBase ((THEN | EQUIVALENT) singleBool)?) RBRACKET;

// constraint definitions
constraint: singleBool (AND singleBool)*;
constraintDefinition: (INDENT constraint SEMI);
constraintsDefinitions: constraintDefinition+;