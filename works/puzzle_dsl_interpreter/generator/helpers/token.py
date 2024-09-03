from __future__ import annotations

from generator.definitions.rules import RawToken
from generator.definitions.token import Token, TokenType
from generator.stores.context import Context
from generator.stores.store import store


class StructsDeclaration(RawToken):
    def __init__(self):
        token = Token(type=TokenType.STRUCTS_DECLARATION)
        super().__init__(token=token)


class DomainHiddenDeclaration(RawToken):
    def __init__(self):
        token = Token(type=TokenType.DOMAIN_HIDDEN_DECLARATION)
        super().__init__(token=token)


class ConstraintsDeclaration(RawToken):
    def __init__(self):
        token = Token(type=TokenType.CONSTRAINTS_DECLARATION)
        super().__init__(token=token)


class P(RawToken):
    def __init__(self):
        token = Token(type=TokenType.P)
        super().__init__(token=token)


class C(RawToken):
    def __init__(self):
        token = Token(type=TokenType.C)
        super().__init__(token=token)


class EP(RawToken):
    def __init__(self):
        token = Token(type=TokenType.EP)
        super().__init__(token=token)


class EC(RawToken):
    def __init__(self):
        token = Token(type=TokenType.EC)
        super().__init__(token=token)


class NewStructId(RawToken):
    def __init__(self):
        type = TokenType.NEW_STRUCT_ID
        if store.context in [Context.STRUCT_DEFINITION]:
            token = Token(type=type, ng=store.defined_structs)
            store.register_struct(token.text)
        elif store.context in [Context.STRUCT_DEFINITION_BODY]:
            token = Token(type=type, ng=store.defined_structs[:-1])
        elif store.context in [Context.CUSTOM_STRUCT_DEFINITION]:
            token = Token(type=type, ok=store.defined_structs)
            store.remove_struct(token.text)
        elif store.context in [Context.B_FUNCTION]:
            token = Token(type=type, ok=store.defined_structs[4:])
        token = Token(type=type)
        super().__init__(token=token)


class RelationshipId(RawToken):
    def __init__(self):
        type = TokenType.RELATIONSHIP_ID
        if store.context in [Context.RELATIONSHIP_SET_BODY]:
            token = Token(type=Token, ng=store.relationship)
            store.register_relationship(token.text)
        token = Token(type=type)
        super().__init__(token=token)


class Combine(RawToken):
    def __init__(self):
        token = Token(type=TokenType.COMBINE)
        super().__init__(token=token)


class Number(RawToken):
    def __init__(self):
        token = Token(type=TokenType.NUMBER)
        super().__init__(token=token)


class ConstantId(RawToken):
    def __init__(self):
        type = TokenType.CONSTANT_ID
        if store.context in [Context.DOMAIN_SET_BODY]:
            token = Token(type=type)
            store.register_constants(token.text)
        else:
            token = Token(type=type, ok=store.constants)

        super().__init__(token=token)


class Dots(RawToken):
    def __init__(self):
        token = Token(type=TokenType.DOTS)
        super().__init__(token=token)


class RightArrow(RawToken):
    def __init__(self):
        token = Token(type=TokenType.RIGHT_ARROW)
        super().__init__(token=token)


class LeftRightArrow(RawToken):
    def __init__(self):
        token = Token(type=TokenType.LEFT_RIGHT_ARROW)
        super().__init__(token=token)


class Solution(RawToken):
    def __init__(self):
        token = Token(type=TokenType.SOLUTION)
        super().__init__(token=token)


class B(RawToken):
    def __init__(self):
        token = Token(type=TokenType.B)
        super().__init__(token=token)


class Cross(RawToken):
    def __init__(self):
        token = Token(type=TokenType.CROSS)
        super().__init__(token=token)


class Cycle(RawToken):
    def __init__(self):
        token = Token(type=TokenType.CYCLE)
        super().__init__(token=token)


class AllDifferent(RawToken):
    def __init__(self):
        token = Token(type=TokenType.ALL_DIFFERENT)
        super().__init__(token=token)


class IsRectangle(RawToken):
    def __init__(self):
        token = Token(type=TokenType.IS_RECTANGLE)
        super().__init__(token=token)


class IsSquare(RawToken):
    def __init__(self):
        token = Token(type=TokenType.IS_SQUARE)
        super().__init__(token=token)


class Connect(RawToken):
    def __init__(self):
        token = Token(type=TokenType.CONNECT)
        super().__init__(token=token)


class NoOverlap(RawToken):
    def __init__(self):
        token = Token(type=TokenType.NO_OVERLAP)
        super().__init__(token=token)


class Fill(RawToken):
    def __init__(self):
        token = Token(type=TokenType.FILL)
        super().__init__(token=token)


class Sum(RawToken):
    def __init__(self):
        token = Token(type=TokenType.SUM)
        super().__init__(token=token)


class Product(RawToken):
    def __init__(self):
        token = Token(type=TokenType.PRODUCT)
        super().__init__(token=token)


class BoundVariable(RawToken):
    def __init__(self):
        token = Token(type=TokenType.BOUND_VARIABLE)
        super().__init__(token=token)


class Inf(RawToken):
    def __init__(self):
        token = Token(type=TokenType.INF)
        super().__init__(token=token)


class Height(RawToken):
    def __init__(self):
        token = Token(type=TokenType.HEIGHT)
        super().__init__(token=token)


class Width(RawToken):
    def __init__(self):
        token = Token(type=TokenType.WIDTH)
        super().__init__(token=token)


class Null(RawToken):
    def __init__(self):
        token = Token(type=TokenType.NULL)
        super().__init__(token=token)


class Undecided(RawToken):
    def __init__(self):
        token = Token(type=TokenType.UNDECIDED)
        super().__init__(token=token)


class EmptySet(RawToken):
    def __init__(self):
        token = Token(type=TokenType.EMPTYSET)
        super().__init__(token=token)


class Integer(RawToken):
    def __init__(self):
        token = Token(type=TokenType.INTEGER)
        super().__init__(token=token)


class And(RawToken):
    def __init__(self):
        token = Token(type=TokenType.AND)
        super().__init__(token=token)


class Or(RawToken):
    def __init__(self):
        token = Token(type=TokenType.OR)
        super().__init__(token=token)


class Not(RawToken):
    def __init__(self):
        token = Token(type=TokenType.NOT)
        super().__init__(token=token)


class Subset(RawToken):
    def __init__(self):
        token = Token(type=TokenType.SUBSET)
        super().__init__(token=token)


class In(RawToken):
    def __init__(self):
        token = Token(type=TokenType.IN)
        super().__init__(token=token)


class Equal(RawToken):
    def __init__(self):
        token = Token(type=TokenType.EQUAL)
        super().__init__(token=token)


class NotEqual(RawToken):
    def __init__(self):
        token = Token(type=TokenType.NOTEQUAL)
        super().__init__(token=token)


class All(RawToken):
    def __init__(self):
        token = Token(type=TokenType.ALL)
        super().__init__(token=token)


class Exists(RawToken):
    def __init__(self):
        token = Token(type=TokenType.EXISTS)
        super().__init__(token=token)


class Then(RawToken):
    def __init__(self):
        token = Token(type=TokenType.THEN)
        super().__init__(token=token)


class Equivalent(RawToken):
    def __init__(self):
        token = Token(type=TokenType.EQUIVALENT)
        super().__init__(token=token)


class LParen(RawToken):
    def __init__(self):
        token = Token(type=TokenType.LPAREN)
        super().__init__(token=token)


class RParen(RawToken):
    def __init__(self):
        token = Token(type=TokenType.RPAREN)
        super().__init__(token=token)


class LCurly(RawToken):
    def __init__(self):
        token = Token(type=TokenType.LCURLY)
        super().__init__(token=token)


class RCurly(RawToken):
    def __init__(self):
        token = Token(type=TokenType.RCURLY)
        super().__init__(token=token)


class LBracket(RawToken):
    def __init__(self):
        token = Token(type=TokenType.LBRACKET)
        super().__init__(token=token)


class RBracket(RawToken):
    def __init__(self):
        token = Token(type=TokenType.RBRACKET)
        super().__init__(token=token)


class Comma(RawToken):
    def __init__(self):
        token = Token(type=TokenType.COMMA)
        super().__init__(token=token)


class Semi(RawToken):
    def __init__(self):
        token = Token(type=TokenType.SEMI)
        super().__init__(token=token)


class Assign(RawToken):
    def __init__(self):
        token = Token(type=TokenType.ASSIGN)
        super().__init__(token=token)


class Pipe(RawToken):
    def __init__(self):
        token = Token(type=TokenType.PIPE)
        super().__init__(token=token)


class Plus(RawToken):
    def __init__(self):
        token = Token(type=TokenType.PLUS)
        super().__init__(token=token)


class Minus(RawToken):
    def __init__(self):
        token = Token(type=TokenType.MINUS)
        super().__init__(token=token)


class Times(RawToken):
    def __init__(self):
        token = Token(type=TokenType.TIMES)
        super().__init__(token=token)


class Space(RawToken):
    def __init__(self):
        token = Token(type=TokenType.SPACE)
        super().__init__(token=token)


class Newline(RawToken):
    def __init__(self):
        token = Token(type=TokenType.NEWLINE)
        super().__init__(token=token)


class Indent(RawToken):
    def __init__(self):
        token = Token(type=TokenType.INDENT)
        super().__init__(token=token)


class LineComment(RawToken):
    def __init__(self):
        token = Token(type=TokenType.LINE_COMMENT)
        super().__init__(token=token)


class BlockComment(RawToken):
    def __init__(self):
        token = Token(type=TokenType.BLOCK_COMMENT)
        super().__init__(token=token)
