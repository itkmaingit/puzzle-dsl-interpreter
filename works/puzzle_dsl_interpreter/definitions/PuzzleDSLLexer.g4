lexer grammar PuzzleDSLLexer;

tokens {
	// Declaration Tokens
	STRUCTS_DECLARATION,
	DOMAIN_HIDDEN_DECLARATION,
	CONSTRAINTS_DECLARATION,

	// Structural Identifier Tokens
	P,
	C,
	EP,
	EC,
	NEW_STRUCT_ID,

	// Relationship Identifier Tokens
	H,
	V,
	D,

	// Combine Function Tokens
	COMBINE,

	// Domain Tokens
	NUMBER,
	CONSTANT_ID,

	// Domain Operator Tokens
	DOTS,
	RIGHT_ARROW,
	LEFT_RIGHT_ARROW,

	// Heuristic Function Tokens
	SOLUTION,
	B,
	CROSS,
	CYCLE,
	ALL_DIFFERENT,
	IS_RECTANGLE,
	IS_SQUARE,
	CONNECT,
	NO_OVERLAP,
	FILL,

	// General Function Tokens
	SUM,
	PRODUCT,

	// Bound Variable Tokens
	BOUND_VARIABLE,

	// Predefined Identifier Tokens
	INF,
	HEIGHT,
	WIDTH,
	NULL,
	UNDECIDED,
	EMPTYSET,
	INTEGER,

	// Logical Operator Tokens
	AND,
	NOT,
	SUBSET,
	IN,
	EQUAL,
	NOTEQUAL,
	ALL,
	EXISTS,
	THEN,
	EQUIVALENT,

	// Symbol Tokens
	LPAREN,
	RPAREN,
	LCURLY,
	RCURLY,
	LBRACKET,
	RBRACKET,
	COMMA,
	SEMI,
	ASSIGN,
	PIPE,
	PLUS,
	MINUS,
	TIMES,

	// Formatting Tokens
	SPACE,
	NEWLINE,
	INDENT,
	LINE_COMMENT,
	BLOCK_COMMENT
}

// declaration tokens

STRUCTS_DECLARATION: 'structs:';
DOMAIN_HIDDEN_DECLARATION: 'domain-hidden:';
CONSTRAINTS_DECLARATION: 'constraints:';

// -----------------------------------------------------------------------------------------

// struct tokens

// structural identifiers

P: 'P';
C: 'C';
EP: 'Ep';
EC: 'Ec';
NEW_STRUCT_ID:
	[ADFGI-MOQ-UW-Z]
	| [ADFGI-MOQ-UW-Z][0-9]
	| [ADFGI-MOQ-UW-Z][a-z];

// relationship identifiers

H: 'H';
V: 'V';
D: 'D';

// combine function
COMBINE: 'combine';

// -----------------------------------------------------------------------------------------

// domain tokens

// domain identifier

NUMBER: [1-9][0-9] | [0-9];
CONSTANT_ID: 'x' | 'x_' [0-9];

// domain operators
DOTS: '...';
RIGHT_ARROW: '->';
LEFT_RIGHT_ARROW: '<->';

// ------------------------------------------------------------------------------------------

// constraint tokens

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

// general functions
SUM: 'Sum';
PRODUCT: 'Product';

// All() or EXISTS()
BOUND_VARIABLE:
	[a-lo-wyz]
	| [a-lo-wyz][a-z]
	| [a-lo-wyz][0-9];

// -----------------------------------------------------------------------------------------

// other tokens

// predefined identifiers
INF: 'inf';
HEIGHT: 'n';
WIDTH: 'm';
NULL: 'null';
UNDECIDED: 'undecided';
EMPTYSET: 'None';
INTEGER: 'N';

// logical operators
EQUAL: '==';
NOTEQUAL: '!=';
AND: '&&';
NOT: '!';
IN: '<-';
SUBSET: '<=';
ALL: 'All';
EXISTS: 'Exists';
THEN: '=>';
EQUIVALENT: '<=>';

// symbols
LPAREN: '(';
RPAREN: ')';
LCURLY: '{';
RCURLY: '}';
LBRACKET: '[';
RBRACKET: ']';
COMMA: ',';
SEMI: ';';
ASSIGN: '=';
PIPE: '|';
PLUS: '+';
MINUS: '-';
TIMES: '*';

// For formatting purposes.
SPACE: (' ') -> channel(HIDDEN); // スペースとタブを隠しチャンネルに送る
NEWLINE: '\r'? '\n' -> channel(HIDDEN); // 改行を隠しチャンネルに送る
INDENT: '\t'; // タブをインデントとして明示的に扱う
LINE_COMMENT: '--' ~[\r\n]* -> skip;
BLOCK_COMMENT: '--[[' .*? ']]' -> skip;