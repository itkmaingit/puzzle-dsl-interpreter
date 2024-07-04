parser grammar PuzzleDSLParser;

options {
	tokenVocab = PuzzleDSLLexer;
	language = Python3;
}

@members {
from members.utils import validateSet, checkUnique
}

file: structsDeclaration structDefinitions;

structsDeclaration: STRUCTS_DECLARATION;

structDefinitions: (INDENT structDefinition NEWLINE)*?;

structDefinition:
	otherStructID ASSIGN COMBINE LPAREN STRUCTS_IDENT COMMA relationshipSet RPAREN;

otherStructID: OTHER_STRUCTS_IDENT;

structsID: STRUCTS_IDENT;

relationshipSet:
	LCURLY relationshipSetBody RCURLY; // Allow empty sets

relationshipSetBody:
	relationshipID (COMMA relationshipID)* {
    elements = [e.getText() for e in self._ctx.relationshipID()]
    self.validateSet(elements)
	self.checkUnique(elements)
};

relationshipID: RELATIONSHIP_IDENT;