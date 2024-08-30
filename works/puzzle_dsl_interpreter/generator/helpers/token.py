from __future__ import annotations

from generator.definitions.rules import RawToken
from generator.definitions.token import Token, TokenType


class StructsDeclaration(RawToken):
    def __init__(self):
        token = Token(TokenType.STRUCTS_DECLARATION)
        super().__init__(token=token)


class DomainHiddenDeclaration(RawToken):
    def __init__(self):
        token = Token(TokenType.DOMAIN_HIDDEN_DECLARATION)
        super().__init__(token=token)


class ConstraintsDeclaration(RawToken):
    def __init__(self):
        token = Token(TokenType.CONSTRAINTS_DECLARATION)
        super().__init__(token=token)


class P(RawToken):
    def __init__(self):
        token = Token(TokenType.P)
        super().__init__(token=token)


class C(RawToken):
    def __init__(self):
        token = Token(TokenType.C)
        super().__init__(token=token)


class EP(RawToken):
    def __init__(self):
        token = Token(TokenType.EP)
        super().__init__(token=token)


class EC(RawToken):
    def __init__(self):
        token = Token(TokenType.EC)
        super().__init__(token=token)


class NewStructId(RawToken):
    def __init__(self):
        token = Token(TokenType.NEW_STRUCT_ID)
        super().__init__(token=token)


class H(RawToken):
    def __init__(self):
        token = Token(TokenType.H)
        super().__init__(token=token)


class V(RawToken):
    def __init__(self):
        token = Token(TokenType.V)
        super().__init__(token=token)


class D(RawToken):
    def __init__(self):
        token = Token(TokenType.D)
        super().__init__(token=token)


class Combine(RawToken):
    def __init__(self):
        token = Token(TokenType.COMBINE)
        super().__init__(token=token)


class Number(RawToken):
    def __init__(self):
        token = Token(TokenType.NUMBER)
        super().__init__(token=token)


class ConstantId(RawToken):
    def __init__(self):
        token = Token(TokenType.CONSTANT_ID)
        super().__init__(token=token)


class Dots(RawToken):
    def __init__(self):
        token = Token(TokenType.DOTS)
        super().__init__(token=token)


class RightArrow(RawToken):
    def __init__(self):
        token = Token(TokenType.RIGHT_ARROW)
        super().__init__(token=token)


class LeftRightArrow(RawToken):
    def __init__(self):
        token = Token(TokenType.LEFT_RIGHT_ARROW)
        super().__init__(token=token)


class Solution(RawToken):
    def __init__(self):
        token = Token(TokenType.SOLUTION)
        super().__init__(token=token)


class B(RawToken):
    def __init__(self):
        token = Token(TokenType.B)
        super().__init__(token=token)


class Cross(RawToken):
    def __init__(self):
        token = Token(TokenType.CROSS)
        super().__init__(token=token)


class Cycle(RawToken):
    def __init__(self):
        token = Token(TokenType.CYCLE)
        super().__init__(token=token)


class AllDifferent(RawToken):
    def __init__(self):
        token = Token(TokenType.ALL_DIFFERENT)
        super().__init__(token=token)


class IsRectangle(RawToken):
    def __init__(self):
        token = Token(TokenType.IS_RECTANGLE)
        super().__init__(token=token)


class IsSquare(RawToken):
    def __init__(self):
        token = Token(TokenType.IS_SQUARE)
        super().__init__(token=token)


class Connect(RawToken):
    def __init__(self):
        token = Token(TokenType.CONNECT)
        super().__init__(token=token)


class NoOverlap(RawToken):
    def __init__(self):
        token = Token(TokenType.NO_OVERLAP)
        super().__init__(token=token)


class Fill(RawToken):
    def __init__(self):
        token = Token(TokenType.FILL)
        super().__init__(token=token)


class Sum(RawToken):
    def __init__(self):
        token = Token(TokenType.SUM)
        super().__init__(token=token)


class Product(RawToken):
    def __init__(self):
        token = Token(TokenType.PRODUCT)
        super().__init__(token=token)


class BoundVariable(RawToken):
    def __init__(self):
        token = Token(TokenType.BOUND_VARIABLE)
        super().__init__(token=token)


class Inf(RawToken):
    def __init__(self):
        token = Token(TokenType.INF)
        super().__init__(token=token)


class Height(RawToken):
    def __init__(self):
        token = Token(TokenType.HEIGHT)
        super().__init__(token=token)


class Width(RawToken):
    def __init__(self):
        token = Token(TokenType.WIDTH)
        super().__init__(token=token)


class Null(RawToken):
    def __init__(self):
        token = Token(TokenType.NULL)
        super().__init__(token=token)


class Undecided(RawToken):
    def __init__(self):
        token = Token(TokenType.UNDECIDED)
        super().__init__(token=token)


class EmptySet(RawToken):
    def __init__(self):
        token = Token(TokenType.EMPTYSET)
        super().__init__(token=token)


class Integer(RawToken):
    def __init__(self):
        token = Token(TokenType.INTEGER)
        super().__init__(token=token)


class And(RawToken):
    def __init__(self):
        token = Token(TokenType.AND)
        super().__init__(token=token)


class Or(RawToken):
    def __init__(self):
        token = Token(TokenType.OR)
        super().__init__(token=token)


class Not(RawToken):
    def __init__(self):
        token = Token(TokenType.NOT)
        super().__init__(token=token)


class Subset(RawToken):
    def __init__(self):
        token = Token(TokenType.SUBSET)
        super().__init__(token=token)


class In(RawToken):
    def __init__(self):
        token = Token(TokenType.IN)
        super().__init__(token=token)


class Equal(RawToken):
    def __init__(self):
        token = Token(TokenType.EQUAL)
        super().__init__(token=token)


class NotEqual(RawToken):
    def __init__(self):
        token = Token(TokenType.NOTEQUAL)
        super().__init__(token=token)


class All(RawToken):
    def __init__(self):
        token = Token(TokenType.ALL)
        super().__init__(token=token)


class Exists(RawToken):
    def __init__(self):
        token = Token(TokenType.EXISTS)
        super().__init__(token=token)


class Then(RawToken):
    def __init__(self):
        token = Token(TokenType.THEN)
        super().__init__(token=token)


class Equivalent(RawToken):
    def __init__(self):
        token = Token(TokenType.EQUIVALENT)
        super().__init__(token=token)


class LParen(RawToken):
    def __init__(self):
        token = Token(TokenType.LPAREN)
        super().__init__(token=token)


class RParen(RawToken):
    def __init__(self):
        token = Token(TokenType.RPAREN)
        super().__init__(token=token)


class LCurly(RawToken):
    def __init__(self):
        token = Token(TokenType.LCURLY)
        super().__init__(token=token)


class RCurly(RawToken):
    def __init__(self):
        token = Token(TokenType.RCURLY)
        super().__init__(token=token)


class LBracket(RawToken):
    def __init__(self):
        token = Token(TokenType.LBRACKET)
        super().__init__(token=token)


class RBracket(RawToken):
    def __init__(self):
        token = Token(TokenType.RBRACKET)
        super().__init__(token=token)


class Comma(RawToken):
    def __init__(self):
        token = Token(TokenType.COMMA)
        super().__init__(token=token)


class Semi(RawToken):
    def __init__(self):
        token = Token(TokenType.SEMI)
        super().__init__(token=token)


class Assign(RawToken):
    def __init__(self):
        token = Token(TokenType.ASSIGN)
        super().__init__(token=token)


class Pipe(RawToken):
    def __init__(self):
        token = Token(TokenType.PIPE)
        super().__init__(token=token)


class Plus(RawToken):
    def __init__(self):
        token = Token(TokenType.PLUS)
        super().__init__(token=token)


class Minus(RawToken):
    def __init__(self):
        token = Token(TokenType.MINUS)
        super().__init__(token=token)


class Times(RawToken):
    def __init__(self):
        token = Token(TokenType.TIMES)
        super().__init__(token=token)


class Space(RawToken):
    def __init__(self):
        token = Token(TokenType.SPACE)
        super().__init__(token=token)


class Newline(RawToken):
    def __init__(self):
        token = Token(TokenType.NEWLINE)
        super().__init__(token=token)


class Indent(RawToken):
    def __init__(self):
        token = Token(TokenType.INDENT)
        super().__init__(token=token)


class LineComment(RawToken):
    def __init__(self):
        token = Token(TokenType.LINE_COMMENT)
        super().__init__(token=token)


class BlockComment(RawToken):
    def __init__(self):
        token = Token(TokenType.BLOCK_COMMENT)
        super().__init__(token=token)
