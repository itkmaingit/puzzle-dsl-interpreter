from __future__ import annotations

import sys
from collections.abc import Callable
from random import choice, choices, randint

from generator.constants import C, Ec, Ep, P
from generator.token import Token, TokenType
from pydantic import BaseModel

Func = Callable[..., list[Token]]
F_T = Func | Token


class Range(BaseModel):
    min: int = 1
    max: int = 1

    def decline(self):
        self.max = max(min - 1, max - 1)

    def callable(self) -> bool:
        return min <= max

    def clone(self) -> Range:
        return Range(min=self.min, max=self.max)

    def dec_clone(self) -> Range:
        return Range(min=self.min, max=self.max - 1)


class OrComp(BaseModel):
    cands: set[Comp]

    def exec(self) -> list[Token]:
        result: list[Token] = []
        for _ in randint(min, max):
            # 各候補の重みに基づいて一つを確率的に選択
            # https://magazine.techacademy.jp/magazine/33531
            chosen_comp = choices(
                list(self.cands),
                weights=[1 / comp.weight for comp in self.cands],
                k=1,
            )[0]

            # 選択されたコンポーネントを実行
            result.extend(chosen_comp.exec())
        return result


class Comp(BaseModel):
    el: F_T
    weight: int = 1
    limit: Range = Range()

    def exec(self) -> list[Token]:
        self.weight += 1
        if callable(self.el):
            return self.el()  # Callableを実行した場合、その結果を返す
        return [self.el]  # Tokenをリストとして返す

    def decline(self):
        self.limit.decline()
        if not self.limit.callable():
            self.weight = sys.maxsize


class PuzzleDSLGenerator:
    def __init__(self):
        self.__defined_structs: set = {P, C, Ep, Ec}
        self.__bound_variables_by_index: list[str] = []
        self.__bound_variables_by_quantifier: list[str] = []
        self.__bound_variables_by_set: list[str] = []
        self.__defined_constants = set()

    def __expand_tokens(
        items: list[OrComp],
    ) -> list[Token]:
        result: list[Token] = []
        for item in items:
            if isinstance(
                item,
                Callable,
            ):  # callable(item) だと厳密ではないため isinstance を使用
                result.extend(item())  # Execute the function and collect its results
            elif isinstance(item, Token):
                result.append(item)  # Append the token directly
            else:
                raise TypeError("List should only contain functions or Tokens")
        return result

    def generate(self) -> list[Token]:
        return self.__expand_tokens([])

    def __generateFile(self) -> list[Token]:
        lst = [
            self.__generateStructsDeclaration,
            Token(type=TokenType.NEWLINE),
            self.__generateStructDefinitions,
            self.__generateDomainHiddenDeclaration,
            self.__generateDomainDefinitions,
            self.__generateConstraintsDeclaration,
            self.__generateConstraintsDefinitions,
        ]
        return self.__expand_tokens(lst)

    def __generateStructsDeclaration(self) -> list[Token]:
        return Token(type=TokenType.STRUCTS_DECLARATION)

    def __generateStructDefinitions(self) -> list[Token]:
        pass

    def __generateIntDomainValue(self, limit: Range) -> Callable[[], list[F_T]]:
        def wrapper() -> list[F_T]:
            def w_h():
                w = Comp(el=Token(TokenType.WIDTH))
                h = Comp(el=Token(TokenType.HEIGHT))
                return OrComp(set(w, h))

            def p_m_t():
                p = Comp(el=Token(TokenType.PLUS))
                m = Comp(el=Token(TokenType.MINUS))
                t = Comp(el=Token(TokenType.TIMES))
                return OrComp(p, m, t)

            choice_1 = [w_h, p_m_t, w_h]
            choice_2 = [
                w_h,
                p_m_t,
                lambda _: OrComp(
                    Comp(el=self.__generateIntDomainValue, limit=limit.dec_clone()),
                ),
            ]

            return choice([choice_1, choice_2])

        return wrapper


# class CustomVisitor(PuzzleDSLParserVisitor):
#     # Visit a parse tree produced by PuzzleDSLParser#file.
#     def visitFile(self, ctx: PuzzleDSLParser.FileContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#structsDeclaration.
#     def visitStructsDeclaration(self, ctx: PuzzleDSLParser.StructsDeclarationContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#domainHiddenDeclaration.
#     def visitDomainHiddenDeclaration(
#         self,
#         ctx: PuzzleDSLParser.DomainHiddenDeclarationContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#constraintsDeclaration.
#     def visitConstraintsDeclaration(
#         self,
#         ctx: PuzzleDSLParser.ConstraintsDeclarationContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#structID.
#     def visitStructID(self, ctx: PuzzleDSLParser.StructIDContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#newStructID.
#     def visitNewStructID(self, ctx: PuzzleDSLParser.NewStructIDContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#structDefinitionBody.
#     def visitStructDefinitionBody(
#         self,
#         ctx: PuzzleDSLParser.StructDefinitionBodyContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#structDefinition.
#     def visitStructDefinition(self, ctx: PuzzleDSLParser.StructDefinitionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#structDefinitions.
#     def visitStructDefinitions(self, ctx: PuzzleDSLParser.StructDefinitionsContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#relationshipID.
#     def visitRelationshipID(self, ctx: PuzzleDSLParser.RelationshipIDContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#relationshipSetBody.
#     def visitRelationshipSetBody(self, ctx: PuzzleDSLParser.RelationshipSetBodyContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#relationshipSet.
#     def visitRelationshipSet(self, ctx: PuzzleDSLParser.RelationshipSetContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#pID.
#     def visitPID(self, ctx: PuzzleDSLParser.PIDContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#cID.
#     def visitCID(self, ctx: PuzzleDSLParser.CIDContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#epID.
#     def visitEpID(self, ctx: PuzzleDSLParser.EpIDContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#ecID.
#     def visitEcID(self, ctx: PuzzleDSLParser.EcIDContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#intDomainValue.
#     def visitIntDomainValue(self, ctx: PuzzleDSLParser.IntDomainValueContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#rangeValue.
#     def visitRangeValue(self, ctx: PuzzleDSLParser.RangeValueContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#domainValue.
#     def visitDomainValue(self, ctx: PuzzleDSLParser.DomainValueContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#domainSetBody.
#     def visitDomainSetBody(self, ctx: PuzzleDSLParser.DomainSetBodyContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#domainSet.
#     def visitDomainSet(self, ctx: PuzzleDSLParser.DomainSetContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#hiddenValue.
#     def visitHiddenValue(self, ctx: PuzzleDSLParser.HiddenValueContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#hiddenSetBody.
#     def visitHiddenSetBody(self, ctx: PuzzleDSLParser.HiddenSetBodyContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#hiddenSet.
#     def visitHiddenSet(self, ctx: PuzzleDSLParser.HiddenSetContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#domainDefinitionBody.
#     def visitDomainDefinitionBody(
#         self,
#         ctx: PuzzleDSLParser.DomainDefinitionBodyContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#pDefinition.
#     def visitPDefinition(self, ctx: PuzzleDSLParser.PDefinitionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#cDefinition.
#     def visitCDefinition(self, ctx: PuzzleDSLParser.CDefinitionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#epDefinition.
#     def visitEpDefinition(self, ctx: PuzzleDSLParser.EpDefinitionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#ecDefinition.
#     def visitEcDefinition(self, ctx: PuzzleDSLParser.EcDefinitionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#customStructDefinition.
#     def visitCustomStructDefinition(
#         self,
#         ctx: PuzzleDSLParser.CustomStructDefinitionContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#domainDefinitions.
#     def visitDomainDefinitions(self, ctx: PuzzleDSLParser.DomainDefinitionsContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#int.
#     def visitInt(self, ctx: PuzzleDSLParser.IntContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#primitiveValue.
#     def visitPrimitiveValue(self, ctx: PuzzleDSLParser.PrimitiveValueContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#set.
#     def visitSet(self, ctx: PuzzleDSLParser.SetContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#solutionFunction.
#     def visitSolutionFunction(self, ctx: PuzzleDSLParser.SolutionFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#bFunction.
#     def visitBFunction(self, ctx: PuzzleDSLParser.BFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#crossFunction.
#     def visitCrossFunction(self, ctx: PuzzleDSLParser.CrossFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#cycleFunction.
#     def visitCycleFunction(self, ctx: PuzzleDSLParser.CycleFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#allDifferentFunction.
#     def visitAllDifferentFunction(
#         self,
#         ctx: PuzzleDSLParser.AllDifferentFunctionContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#isRectangleFunction.
#     def visitIsRectangleFunction(self, ctx: PuzzleDSLParser.IsRectangleFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#isSquareFunction.
#     def visitIsSquareFunction(self, ctx: PuzzleDSLParser.IsSquareFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#connectFunction.
#     def visitConnectFunction(self, ctx: PuzzleDSLParser.ConnectFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#noOverlapFunction.
#     def visitNoOverlapFunction(self, ctx: PuzzleDSLParser.NoOverlapFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#fillFunction.
#     def visitFillFunction(self, ctx: PuzzleDSLParser.FillFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#quantifier.
#     def visitQuantifier(self, ctx: PuzzleDSLParser.QuantifierContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#index.
#     def visitIndex(self, ctx: PuzzleDSLParser.IndexContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#quantifierIndex.
#     def visitQuantifierIndex(self, ctx: PuzzleDSLParser.QuantifierIndexContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#indexFunction.
#     def visitIndexFunction(self, ctx: PuzzleDSLParser.IndexFunctionContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#structElement.
#     def visitStructElement(self, ctx: PuzzleDSLParser.StructElementContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#generationSet.
#     def visitGenerationSet(self, ctx: PuzzleDSLParser.GenerationSetContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#boolean.
#     def visitBoolean(self, ctx: PuzzleDSLParser.BooleanContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#singleBoolean.
#     def visitSingleBoolean(self, ctx: PuzzleDSLParser.SingleBooleanContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#notBoolean.
#     def visitNotBoolean(self, ctx: PuzzleDSLParser.NotBooleanContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#parenthesizedBoolean.
#     def visitParenthesizedBoolean(
#         self,
#         ctx: PuzzleDSLParser.ParenthesizedBooleanContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#quantifierBoolean.
#     def visitQuantifierBoolean(self, ctx: PuzzleDSLParser.QuantifierBooleanContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#compoundBoolean.
#     def visitCompoundBoolean(self, ctx: PuzzleDSLParser.CompoundBooleanContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#constraint.
#     def visitConstraint(self, ctx: PuzzleDSLParser.ConstraintContext):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#constraintDefinition.
#     def visitConstraintDefinition(
#         self,
#         ctx: PuzzleDSLParser.ConstraintDefinitionContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)

#     # Visit a parse tree produced by PuzzleDSLParser#constraintsDefinitions.
#     def visitConstraintsDefinitions(
#         self,
#         ctx: PuzzleDSLParser.ConstraintsDefinitionsContext,
#     ):
#         print("Visiting rule:", type(ctx).__name__)
#         return self.visitChildren(ctx)
