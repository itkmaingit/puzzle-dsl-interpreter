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
	DOMAIN_VALUE,
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
	INDENT,
	AND,
	SUBSET,
	M,
	N
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

OTHER_STRUCTS_IDENT:
	[ADFGI-MOQ-UW-Z]
	| [ADFGI-MOQ-UW-Z][0-9]
	| [ADFGI-MOQ-UW-Z][a-z];

COMBINE: 'combine';

// domain tokens

DOMAIN_DECLARATION: 'domain:';

NUMBER: [1-9][0-9] | [0-9];

NULL: 'null';

VALUE_IDENT: 'x' | 'x_' [0-9];

DOTS: '...';

// constraints tokens
CONSTRAINTS_DECLARATION: 'constraints:';

// heuristic function tokens
SOLUTION: 'solution';
B: 'B'; // STRUCT_SET -> STRUCT_ELEMENT
CROSS: 'cross'; // P_ELEMENT -> NUMBER
CYCLE: 'cycle'; // C_ELEMENT -> NUMBER
ALL_DIFFERENT: 'all_different'; // SET -> BOOL
IS_RECTANGLE: 'is_rectangle'; // STRUCT_ELEMENT -> BOOL
IS_SQUARE: 'is_square'; // STRUCT_ELEMENT -> BOOL
CONNECT: 'connect'; // STRUCT_ELEMENT -> BOOL
NO_OVERLAP: 'no_overlap'; // STRUCT_SET -> BOOL
FILL: 'fill'; // STRUCT_SET -> BOOL

VARIABLE: [a-lo-wyz]| [a-lo-wyz][a-z]| [a-lo-wyz][0-9];
SUM: 'Sum';
PRODUCT: 'Product';
EMPTYSET: 'None';

// other tokens
ASSIGN: '=';

RIGHT_ARROW: '->';
THEN: '=>';
EQUIVALENT: '<=>';

LPAREN: '(';
RPAREN: ')';
LCURLY: '{';
RCURLY: '}';
LBRACKET: '[';
RBRACKET: ']';

COMMA: ',';

EQUAL: '==';
NOTEQUAL: '!=';
AND: '&&';
NOT: '!';
PIPE: '|';
SEMI: ';';
IN: '<-';
SUBSET: '<=';
ALL: 'All';
EXISTS: 'Exists';

PLUS: '+';
MINUS: '-';
TIMES: '*';

INTEGER: 'N';
HEIGHT: 'n';
WIDTH: 'm';

// For formatting purposes.
SPACE: (' ') -> channel(HIDDEN); // スペースとタブを隠しチャンネルに送る
NEWLINE: '\r'? '\n' -> channel(HIDDEN); // 改行を隠しチャンネルに送る
INDENT: '\t'; // タブをインデントとして明示的に扱う