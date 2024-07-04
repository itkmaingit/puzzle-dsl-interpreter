lexer grammar PuzzleDSLLexer;

tokens {
	STRUCTS_DECLARATION,
	P,
	C,
	EP,
	EC,
	H,
	V,
	D,
	RELATIONSHIP_IDENT,
	OTHER_STRUCTS_IDENT,
	STRUCTS_IDENT,
	COMBINE,
	NUMBER,
	NULL,
	VALUE_IDENT,
	NL,
	TAB,
	ASSIGN,
	RIGHT_ARROW,
	LPAREN,
	RPAREN,
	LCURLY,
	RCURLY,
	COMMA,
	SPACE,
	NEWLINE,
	INDENT
}

// sturcts tokens

STRUCTS_DECLARATION: 'structs:';

P: 'P';
C: 'C';
EP: 'Ep';
EC: 'Ec';

H: 'H';
V: 'V';
D: 'D';

fragment RELATIONSHIP_IDENT: H | V | D;

OTHER_STRUCTS_IDENT:
	[ADFGI-OQ-UW-Z]
	| [ADFGI-OQ-UW-Z][0-9]
	| [ADFGI-OQ-UW-Z][a-z];

fragment STRUCTS_IDENT: P | C | EP | EC | OTHER_STRUCTS_IDENT;

COMBINE: 'combine';

// domain tokens

NUMBER: [0-9]+;

NULL: 'null';

VALUE_IDENT: [a-z] | [a-z]'_' [0-9];

// other tokens

ASSIGN: '=';

RIGHT_ARROW: '->';

LPAREN: '(';
RPAREN: ')';
LCURLY: '{';
RCURLY: '}';

COMMA: ',';

SPACE: (' ' | '\t') -> channel(HIDDEN); // スペースとタブを隠しチャンネルに送る
NEWLINE: '\r'? '\n' -> channel(HIDDEN); // 改行を隠しチャンネルに送る
INDENT: '\t'; // タブをインデントとして明示的に扱う