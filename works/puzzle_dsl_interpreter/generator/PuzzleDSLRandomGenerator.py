from __future__ import annotations

import random

from generator.definitions.rules import AlternativeRule, OrderRule
from generator.helpers import token
from generator.helpers.instant_rule import P_M_T, W_H


class File(OrderRule):
    def __init__(self):
        order = [token.StructsDeclaration()]
        super().__init__(order=order)


class IntDomainValue(AlternativeRule):
    DEPTH_LIMIT = 10

    def __init__(self, depth: int = 0):
        if depth >= self.DEPTH_LIMIT:
            # 再帰深度が上限に達したら、再帰しない選択肢のみを使用
            choices = [
                IntDomainValue_1(),
                token.Width(),
                token.Height(),
                token.Number(),
            ]
        else:
            # 再帰の深さに応じて、再帰的選択肢を加える
            choices = [
                IntDomainValue_1(),
                IntDomainValue_2(depth + 1)
                if random.random() > depth / self.DEPTH_LIMIT
                else token.Number(),
                token.Width(),
                token.Height(),
                IntDomainValue_5(depth + 1)
                if random.random() > depth / self.DEPTH_LIMIT
                else token.Number(),
                token.Number(),
            ]
        super().__init__(choices)


class IntDomainValue_1(OrderRule):
    def __init__(self):
        order = [W_H(), P_M_T(), W_H()]
        super().__init__(order)


class IntDomainValue_2(OrderRule):
    def __init__(self, depth):
        order = [W_H(), P_M_T(), IntDomainValue(depth)]
        super().__init__(order)


class IntDomainValue_5(OrderRule):
    def __init__(self, depth: int):
        order = [IntDomainValue(depth), P_M_T(), W_H()]
        super().__init__(order)


# class PuzzleDSLGenerator:
#     def __init__(self):
#         self.__defined_structs: set = {P, C, Ep, Ec}
#         self.__bound_variables_by_index: list[str] = []
#         self.__bound_variables_by_quantifier: list[str] = []
#         self.__bound_variables_by_set: list[str] = []
#         self.__defined_constants = set()

#     def __expand_tokens(
#         items: list[OrComp],
#     ) -> list[Token]:
#         result: list[Token] = []
#         for item in items:
#             if isinstance(
#                 item,
#                 Callable,
#             ):  # callable(item) だと厳密ではないため isinstance を使用
#                 result.extend(item())  # Execute the function and collect its results
#             elif isinstance(item, Token):
#                 result.append(item)  # Append the token directly
#             else:
#                 raise TypeError("List should only contain functions or Tokens")
#         return result

#     def generate(self) -> list[Token]:
#         return self.__expand_tokens([])

#     def __generateFile(self) -> list[Token]:
#         lst = [
#             self.__generateStructsDeclaration,
#             Token(type=TokenType.NEWLINE),
#             self.__generateStructDefinitions,
#             self.__generateDomainHiddenDeclaration,
#             self.__generateDomainDefinitions,
#             self.__generateConstraintsDeclaration,
#             self.__generateConstraintsDefinitions,
#         ]
#         return self.__expand_tokens(lst)

#     def __generateStructsDeclaration(self) -> list[Token]:
#         return Token(type=TokenType.STRUCTS_DECLARATION)

#     def __generateStructDefinitions(self) -> list[Token]:
#         pass

#     def __generateIntDomainValue(self, limit: Range) -> Callable[[], list[F_T]]:
#         def wrapper() -> list[F_T]:
#             def w_h():
#                 w = Comp(el=Token(TokenType.WIDTH))
#                 h = Comp(el=Token(TokenType.HEIGHT))
#                 return OrComp(set(w, h))

#             def p_m_t():
#                 p = Comp(el=Token(TokenType.PLUS))
#                 m = Comp(el=Token(TokenType.MINUS))
#                 t = Comp(el=Token(TokenType.TIMES))
#                 return OrComp(p, m, t)

#             choice_1 = [w_h, p_m_t, w_h]
#             choice_2 = [
#                 w_h,
#                 p_m_t,
#                 lambda _: OrComp(
#                     Comp(el=self.__generateIntDomainValue, limit=limit.dec_clone()),
#                 ),
#             ]

#             return choice([choice_1, choice_2])

#         return wrapper


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
