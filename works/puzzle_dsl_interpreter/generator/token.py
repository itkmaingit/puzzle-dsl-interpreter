from __future__ import annotations

from enum import IntEnum, auto

import rstr
from pydantic import BaseModel


class Token(BaseModel):
    type: TokenType
    text: str

    def __init__(self, type: TokenType, text: str | None = None) -> Token:
        if text is None:
            pattern = TOKEN_PATTERNS.get(type)
            if pattern is None:
                raise ValueError(f"No pattern found for token type: {type}")
            # hypothesisを使用してランダムな文字列を生成
            text = rstr.xeger(pattern)
        super().__init__(type=type, text=text)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return (self.type, self.text) == (other.type, other.text)

    def __hash__(self) -> int:
        return hash((self.type, self.text))


class TokenType(IntEnum):
    STRUCTS_DECLARATION = auto()
    DOMAIN_HIDDEN_DECLARATION = auto()
    CONSTRAINTS_DECLARATION = auto()
    P = auto()
    C = auto()
    EP = auto()
    EC = auto()
    NEW_STRUCT_ID = auto()
    H = auto()
    V = auto()
    D = auto()
    COMBINE = auto()
    NUMBER = auto()
    CONSTANT_ID = auto()
    DOTS = auto()
    RIGHT_ARROW = auto()
    LEFT_RIGHT_ARROW = auto()
    SOLUTION = auto()
    B = auto()
    CROSS = auto()
    CYCLE = auto()
    ALL_DIFFERENT = auto()
    IS_RECTANGLE = auto()
    IS_SQUARE = auto()
    CONNECT = auto()
    NO_OVERLAP = auto()
    FILL = auto()
    SUM = auto()
    PRODUCT = auto()
    BOUND_VARIABLE = auto()
    INF = auto()
    HEIGHT = auto()
    WIDTH = auto()
    NULL = auto()
    UNDECIDED = auto()
    EMPTYSET = auto()
    INTEGER = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    SUBSET = auto()
    IN = auto()
    EQUAL = auto()
    NOTEQUAL = auto()
    ALL = auto()
    EXISTS = auto()
    THEN = auto()
    EQUIVALENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LCURLY = auto()
    RCURLY = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMI = auto()
    ASSIGN = auto()
    PIPE = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    SPACE = auto()
    NEWLINE = auto()
    INDENT = auto()
    LINE_COMMENT = auto()
    BLOCK_COMMENT = auto()


TOKEN_PATTERNS = {
    TokenType.STRUCTS_DECLARATION: r"^structs:$",
    TokenType.DOMAIN_HIDDEN_DECLARATION: r"^domain-hidden:$",
    TokenType.CONSTRAINTS_DECLARATION: r"^constraints:$",
    TokenType.P: r"^P$",
    TokenType.C: r"^C$",
    TokenType.EP: r"^Ep$",
    TokenType.EC: r"^Ec$",
    TokenType.NEW_STRUCT_ID: r"^[ADFGI-MOQ-UW-Z][0-9a-z]?$",
    TokenType.H: r"^H$",
    TokenType.V: r"^V$",
    TokenType.D: r"^D$",
    TokenType.COMBINE: r"^combine$",
    TokenType.NUMBER: r"^([1-9][0-9]?|0)$",
    TokenType.CONSTANT_ID: r"^x(_\d)?$",
    TokenType.DOTS: r"^\.\.\.$",
    TokenType.RIGHT_ARROW: r"^->$",
    TokenType.LEFT_RIGHT_ARROW: r"^<->$",
    TokenType.SOLUTION: r"^solution$",
    TokenType.B: r"^B$",
    TokenType.CROSS: r"^cross$",
    TokenType.CYCLE: r"^cycle$",
    TokenType.ALL_DIFFERENT: r"^all_different$",
    TokenType.IS_RECTANGLE: r"^is_rectangle$",
    TokenType.IS_SQUARE: r"^is_square$",
    TokenType.CONNECT: r"^connect$",
    TokenType.NO_OVERLAP: r"^no_overlap$",
    TokenType.FILL: r"^fill$",
    TokenType.SUM: r"^Sum$",
    TokenType.PRODUCT: r"^Product$",
    TokenType.BOUND_VARIABLE: r"^[a-lo-wyz][a-z0-9]?$",
    TokenType.INF: r"^inf$",
    TokenType.HEIGHT: r"^n$",
    TokenType.WIDTH: r"^m$",
    TokenType.NULL: r"^null$",
    TokenType.UNDECIDED: r"^undecided$",
    TokenType.EMPTYSET: r"^None$",
    TokenType.INTEGER: r"^N$",
    TokenType.EQUAL: r"^==$",
    TokenType.NOTEQUAL: r"^!=$",
    TokenType.AND: r"^&&$",
    TokenType.OR: r"^\|\|$",
    TokenType.NOT: r"^!$",
    TokenType.IN: r"^<-$",
    TokenType.SUBSET: r"^<=$",
    TokenType.ALL: r"^All$",
    TokenType.EXISTS: r"^Exists$",
    TokenType.THEN: r"^=>$",
    TokenType.EQUIVALENT: r"^<=>$",
    TokenType.LPAREN: r"^\($",
    TokenType.RPAREN: r"^\)$",
    TokenType.LCURLY: r"^\{$",
    TokenType.RCURLY: r"^\}$",
    TokenType.LBRACKET: r"^\[$",
    TokenType.RBRACKET: r"^\]$",
    TokenType.COMMA: r"^,$",
    TokenType.SEMI: r"^;$",
    TokenType.ASSIGN: r"^=$",
    TokenType.PIPE: r"^\|$",
    TokenType.PLUS: r"^\+$",
    TokenType.MINUS: r"^-$",
    TokenType.TIMES: r"^\*$",
    TokenType.SPACE: r"^ $",
    TokenType.NEWLINE: r"^(\r?\n)$",
    TokenType.INDENT: r"^\t$",
    TokenType.LINE_COMMENT: r"^--[^[\r\n]*$",
    TokenType.BLOCK_COMMENT: r"^--\[\[.*?\]\]$",
}
