parser grammar PuzzleDSLParser;

options {
	tokenVocab = PuzzleDSLLexer;
	language = Python3;
}

@members {
from members.utils import validate_relationship_set, check_unique
from members.domain import validate_domain_set
}

file:
	structsDeclaration structDefinitions domainDeclaration domainDefinitions constraintsDeclaration
		constraintsDefinitions;

// struct pattern
structsDeclaration: STRUCTS_DECLARATION; //

structDefinitions: (INDENT? structDefinition)*; //

structDefinition:
	otherStructID ASSIGN COMBINE LPAREN structID COMMA relationshipSet RPAREN SEMI; //

otherStructID: OTHER_STRUCTS_IDENT; //

structID: P | C | EP | EC | OTHER_STRUCTS_IDENT; //

// domain pattern
domainDeclaration: DOMAIN_DECLARATION; //

domainDefinitions:
	pDefinition cDefinition epDefinition ecDefinition (
		customStructDefinition
	)*; //

pDefinition: (INDENT? P ASSIGN domainSet SEMI); //
cDefinition: (INDENT? C ASSIGN domainSet SEMI); //
epDefinition: (INDENT? EP ASSIGN domainSet SEMI); //
ecDefinition: (INDENT? EC ASSIGN domainSet SEMI); //

customStructDefinition: (
		INDENT? otherStructID ASSIGN domainSet SEMI
	); //

domainSet: LCURLY domainSetBody RCURLY; //

domainSetBody:
	domainValue (COMMA domainValue)* {
    elements = [e.getText() for e in self._ctx.domainValue()]
    self.validate_domain_set(elements)
}; //

domainValue: intDomainValue | rangeValue | NULL | VALUE_IDENT; //

intDomainValue:
	(WIDTH | HEIGHT) (PLUS | MINUS | TIMES) (WIDTH | HEIGHT) //
	| (WIDTH | HEIGHT) (PLUS | MINUS | TIMES) intDomainValue
	| WIDTH
	| HEIGHT
	| intDomainValue (PLUS | MINUS | TIMES) (WIDTH | HEIGHT)
	| NUMBER;

rangeValue: intDomainValue DOTS intDomainValue;

// constraints pattern
constraintsDeclaration: CONSTRAINTS_DECLARATION; //

constraintsDefinitions: (INDENT constraint SEMI)+; //

constraint: singleBool (AND singleBool)*; //

singleBool: singleBoolBase ((THEN | EQUIVALENT) singleBool)?; //

singleBoolBase: (
		(generationBoundVariable | generationStructElement) COMMA
	)*? NOT? (
		fillFunction
		| noOverlapFunction
		| allDifferentFunction
		| set (SUBSET | IN) set
		| isRectangleFunction
		| isRectangleFunction
		| set (NOTEQUAL | EQUAL) (set | EMPTYSET)
		| value (NOTEQUAL | EQUAL) value
	); //

value: int | solutionFunction;
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
	| int (PLUS | MINUS | TIMES) int; //

// heuristic function pattern
bFunction: B LPAREN structID RPAREN; //
crossFunction: CROSS LPAREN structElement RPAREN; //
cycleFunction: CYCLE LPAREN structElement RPAREN; //
allDifferentFunction:
	ALL_DIFFERENT LPAREN structElement RPAREN; //
isRectangleFunction: IS_RECTANGLE LPAREN structElement RPAREN; //
isSquareFunction: IS_SQUARE LPAREN structElement RPAREN; //
connectFunction:
	CONNECT LPAREN structElement COMMA relationshipSet RPAREN; //
noOverlapFunction: NO_OVERLAP LPAREN structID RPAREN; //
fillFunction: FILL LPAREN structID (COMMA structID)* RPAREN; //

//builtin function pattern
solutionFunction: SOLUTION LPAREN structElement RPAREN; //
sumFunction: SUM LCURLY pickUp RCURLY LPAREN int RPAREN; //
productFunction:
	PRODUCT LCURLY pickUp RCURLY LPAREN int RPAREN; //

// variables
structElement: VARIABLE; //

generationStructElement:
	(ALL | EXISTS) LPAREN structElement RPAREN IN (
		bFunction
		| structElement
	); //

generationBoundVariable: (ALL | EXISTS) LPAREN VARIABLE RPAREN IN (
		set
	); //

generationSet:
	LCURLY VARIABLE (IN set)? PIPE constraint RCURLY; //

set:
	bFunction
	| structElement
	| connectFunction
	| generationSet; //

pickUp: VARIABLE IN set; //

// utils pattern
relationshipSet: LCURLY relationshipSetBody RCURLY; //

relationshipSetBody:
	relationshipID (COMMA relationshipID)* {
    elements = [e.getText() for e in self._ctx.relationshipID()]
    self.validate_relationship_set(elements)
}; //

relationshipID: H | V | D; //