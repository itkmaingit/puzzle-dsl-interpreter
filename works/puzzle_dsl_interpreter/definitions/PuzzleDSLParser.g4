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
	structsDeclaration structDefinitions domainDeclaration domainDefinitions;

// struct pattern
structsDeclaration: STRUCTS_DECLARATION;

structDefinitions: (INDENT? structDefinition)*;

structDefinition:
	otherStructID ASSIGN COMBINE LPAREN structID COMMA relationshipSet RPAREN;

otherStructID: OTHER_STRUCTS_IDENT;

structID: P | C | EP | EC | OTHER_STRUCTS_IDENT;

// domain pattern
domainDeclaration: DOMAIN_DECLARATION;

domainDefinitions:
	pDefinition cDefinition epDefinition ecDefinition (
		customStructDefinition
	)*;

pDefinition: (INDENT? P ASSIGN domainSet);
cDefinition: (INDENT? C ASSIGN domainSet);
epDefinition: (INDENT? EP ASSIGN domainSet);
ecDefinition: (INDENT? EC ASSIGN domainSet);

customStructDefinition: (INDENT? otherStructID ASSIGN domainSet);

domainSet: LCURLY domainSetBody RCURLY;

domainSetBody:
	domainValue (COMMA domainValue)* {
    elements = [e.getText() for e in self._ctx.domainValue()]
    self.validate_domain_set(elements)
};

domainValue: NUMBER | NULL | VALUE_IDENT;

// utils pattern

relationshipSet: LCURLY relationshipSetBody RCURLY;

relationshipSetBody:
	relationshipID (COMMA relationshipID)* {
    elements = [e.getText() for e in self._ctx.relationshipID()]
    self.validate_relationship_set(elements)
};

relationshipID: H | V | D;