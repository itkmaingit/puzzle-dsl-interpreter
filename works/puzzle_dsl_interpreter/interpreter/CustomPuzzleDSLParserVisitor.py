from __future__ import annotations

from antlr4 import ParserRuleContext
from interpreter.definitions.token import Token, TokenAttribute
from interpreter.errors import (
    DuplicationStructDefinitionError,
    EvaluationError,
    ExistsUndefinedStructError,
    InsufficientStructError,
    InvalidRelationshipSetError,
    NotDefinitionStructError,
    SubsetViolationError,
    UndefinedStructError,
    UndefinedValueError,
)
from parser.PuzzleDSLParser import PuzzleDSLParser
from parser.PuzzleDSLParserVisitor import PuzzleDSLParserVisitor

P = Token(attr=TokenAttribute.ELEMENT, text="P")
C = Token(attr=TokenAttribute.ELEMENT, text="C")
Ep = Token(attr=TokenAttribute.ELEMENT, text="Ep")
Ec = Token(attr=TokenAttribute.ELEMENT, text="Ec")


class PuzzleDSLEvaluators:
    @classmethod
    def check_unique(cls, elements):
        seen = set()
        for e in elements:
            if e in seen:
                return False
            seen.add(e)
        return True

    @classmethod
    def validate_relationship_set(cls, ctx: ParserRuleContext, elements):
        if not (1 <= len(elements) <= 3):  # noqa: PLR2004
            raise InvalidRelationshipSetError(
                ctx,
                "The set must contain between 1 and 3 elements",
            )
        if not cls.check_unique(elements):
            raise InvalidRelationshipSetError(ctx, "Duplicate elements are not allowed")


class PuzzleDSLOperators:
    # use for domain set or hidden set
    @classmethod
    def extract_set(cls, set_ctx: ParserRuleContext) -> set:
        result_set = set()
        elements: list[str] = set_ctx.getText().strip("{}").split(",")
        for element in elements:
            result_set = result_set.union(cls.evaluate_expression(element.strip()))

        return result_set

    @classmethod
    def evaluate_expression(cls, expr: str) -> set:
        if "..." in expr:
            return cls.evaluate_range(expr)
        return {cls.__convert_to_int(expr)}

    @classmethod
    def evaluate_range(cls, expr: str) -> set:
        try:
            start, end = expr.split("...")
            if "n" in start or "m" in start or "n" in end or "m" in end:
                return {f"{start}...{end}"}  # 簡易評価
            start, end = int(start), int(end)
            return set(range(start, end + 1))
        except ValueError:
            return {expr}  # 数値以外の範囲はそのまま保持

    @classmethod
    def is_subset(
        cls, ctx: ParserRuleContext, domain_set: set, hidden_set: set
    ) -> bool:
        evaluatable_hidden_set = set()
        unevaluable_terms = set()

        # 各要素を評価しやすいものと評価できないものに分ける
        for item in hidden_set:
            if item == "null":
                evaluatable_hidden_set.add(item)
            elif isinstance(item, str) and any(
                symbol in item for symbol in ("n", "m")
            ):  # itemが文字列の場合のみチェック
                unevaluable_terms.add(item)
            else:
                evaluatable_hidden_set.add(item)

        # 評価可能な要素のみで部分集合かどうかチェック
        if not evaluatable_hidden_set.issubset(domain_set):
            raise SubsetViolationError(
                ctx,
                f"Subset Error: {hidden_set} is not a subset of {domain_set}.",
            )

        # n または m を含む要素がある場合、警告を発する
        if unevaluable_terms:
            EvaluationError(
                ctx,
                f"Warning: Unable to fully evaluate expressions involving 'n' or 'm' in {unevaluable_terms}. Partial evaluation only.",
            )

        return True

    @classmethod
    def __convert_to_int(cls, value) -> bool:
        try:
            # 文字列を整数に変換を試みる
            return int(value)
        except ValueError:
            return value

    @classmethod
    def construct_struct_token(cls, struct_id: str) -> Token:
        if struct_id in ["P", "C", "Ep", "Ec"]:
            return Token(
                attr=TokenAttribute.ELEMENT,
                text=struct_id,
            )
        return Token(
            attr=TokenAttribute.STRUCT,
            text=struct_id,
        )


# Semantics Errorの発見
class CustomPuzzleDSLParserVisitor(PuzzleDSLParserVisitor):
    def __init__(self, parser: PuzzleDSLParser):
        self.__parser = parser
        self.__defined_structs: set = {P, C, Ep, Ec}
        self.__eval_tool = PuzzleDSLEvaluators
        self.__oper_tool = PuzzleDSLOperators
        self.__bound_variables_by_index: list[str] = []
        self.__bound_variables_by_quantifier: list[str] = []
        self.__bound_variables_by_set: list[str] = []
        self.__defined_constants = set()

    @property
    def __bound_variables(self):
        class BoundVariables:
            def __init__(self, by_index, by_quantifier, by_set):
                self.bound_variables_by_index = by_index
                self.bound_variables_by_quantifier = by_quantifier
                self.bound_variables_by_set = by_set

            def combined(self):
                return (
                    self.bound_variables_by_index
                    + self.bound_variables_by_quantifier
                    + self.bound_variables_by_set
                )

        bound_variables = BoundVariables(
            self.__bound_variables_by_index,
            self.__bound_variables_by_quantifier,
            self.__bound_variables_by_set,
        )

        return bound_variables.combined()

    def visitStructDefinition(self, ctx: PuzzleDSLParser.StructDefinitionContext):
        struct_token = Token(
            attr=TokenAttribute.STRUCT,
            text=ctx.newStructID().getText(),
        )
        # すでに定義されているIDかどうかをチェック
        if struct_token in self.__defined_structs:
            # 重複エラーを表示または処理
            raise DuplicationStructDefinitionError(
                ctx,
                f"Error: Struct ID '{struct_token.text}' is duplicated.",
            )
        # 新しいIDとして辞書に追加
        self.__defined_structs.add(struct_token)
        # 次のノードを訪問
        return self.visitChildren(ctx)

    def visitRelationshipSetBody(self, ctx: PuzzleDSLParser.RelationshipSetBodyContext):
        elements = [e.getText() for e in ctx.relationshipID()]
        self.__eval_tool.validate_relationship_set(ctx, elements)
        return self.visitChildren(ctx)

    def visitDomainValue(self, ctx: PuzzleDSLParser.DomainValueContext):
        constant_val = ctx.CONSTANT_ID()
        if constant_val:
            token = Token(attr=TokenAttribute.CONSTANTS, text=constant_val.getText())
            self.__defined_constants.add(token)
        return self.visitChildren(ctx)

    def visitStructDefinitionBody(
        self,
        ctx: PuzzleDSLParser.StructDefinitionBodyContext,
    ):
        base_struct_token = self.__oper_tool.construct_struct_token(
            ctx.structID().getText(),
        )

        if base_struct_token not in self.__defined_structs:
            # 未定義のstructがcombineに用いられている場合にエラーを吐く
            raise NotDefinitionStructError(
                ctx,
                f"Error: Struct ID '{base_struct_token.text}' is not defined. ",
            )
        return self.visitChildren(ctx)

    def visitDomainDefinitions(self, ctx: PuzzleDSLParser.DomainDefinitionsContext):
        custom_struct_definitions = {
            Token(
                attr=TokenAttribute.STRUCT,
                text=e.newStructID().getText(),
            )
            for e in ctx.customStructDefinition()
        }
        default_struct_definitions = {P, C, Ep, Ec}
        struct_definitions_in_domain_context = default_struct_definitions.union(
            custom_struct_definitions,
        )
        if self.__defined_structs != struct_definitions_in_domain_context:
            undefined_structs = (
                struct_definitions_in_domain_context - self.__defined_structs
            )
            insufficient_structs = (
                self.__defined_structs - struct_definitions_in_domain_context
            )
            if undefined_structs:
                raise ExistsUndefinedStructError(
                    ctx,
                    f"Undefined Struct ID: {undefined_structs}",
                )
            if insufficient_structs:
                raise InsufficientStructError(
                    ctx,
                    f"Insufficent Structs: {insufficient_structs}",
                )

        return self.visitChildren(ctx)

    def visitDomainDefinitionBody(
        self,
        ctx: PuzzleDSLParser.DomainDefinitionBodyContext,
    ):
        domain_set = self.__oper_tool.extract_set(ctx.domainSet())
        hidden_set = self.__oper_tool.extract_set(ctx.hiddenSet())
        hidden_set = {x for x in hidden_set if x != "undecided"}
        try:
            if not self.__oper_tool.is_subset(ctx, domain_set, hidden_set):
                raise SubsetViolationError(
                    ctx,
                    f"Hidden set {hidden_set} is not a subset of domain set {domain_set}.",
                )
        except EvaluationError as e:
            print(e)
        return self.visitChildren(ctx)

    def visitNoOverlapFunction(self, ctx: PuzzleDSLParser.NoOverlapFunctionContext):
        arg_structs = {
            self.__oper_tool.construct_struct_token(element.getText())
            for element in ctx.newStructID()
        }

        if not arg_structs.issubset(self.__defined_structs):
            raise UndefinedStructError(
                ctx,
                f"Error: Undefined Structs: {[e.text for e in arg_structs-self.__defined_structs]}",
            )

        return self.visitChildren(ctx)

    def visitFillFunction(self, ctx: PuzzleDSLParser.FillFunctionContext):
        arg_structs = {
            self.__oper_tool.construct_struct_token(element.getText())
            for element in ctx.newStructID()
        }

        if not arg_structs.issubset(self.__defined_structs):
            raise UndefinedStructError(
                ctx,
                f"Error: Undefined Structs: {[e.text for e in arg_structs-self.__defined_structs]}",
            )
        return self.visitChildren(ctx)

    def visitStructElement(self, ctx: PuzzleDSLParser.StructElementContext):
        struct_element = ctx.getText()
        if struct_element not in self.__bound_variables:
            raise UndefinedStructError(
                ctx,
                f"Undefined Variable: {struct_element}, current bound variables are {self.__bound_variables}",
            )
        return self.visitChildren(ctx)

    def visitBFunction(self, ctx: PuzzleDSLParser.BFunctionContext):
        struct_id = ctx.structID().getText()
        struct_token = self.__oper_tool.construct_struct_token(
            struct_id=struct_id,
        )
        if struct_token not in self.__defined_structs:
            raise UndefinedStructError(ctx, f"{struct_id} is not defined.")
        return self.visitChildren(ctx)

    def visitPrimitiveValue(self, ctx: PuzzleDSLParser.PrimitiveValueContext):
        constant_val = ctx.CONSTANT_ID()
        if constant_val:
            token = Token(attr=TokenAttribute.CONSTANTS, text=constant_val.getText())
            if token not in self.__defined_constants:
                raise UndefinedValueError(
                    ctx,
                    f"constant value ({token.text}) is not undefined in domain-hidden context.",
                )
        return self.visitChildren(ctx)

    def visitIndex(self, ctx: PuzzleDSLParser.IndexContext):
        local_bound_variable = ctx.BOUND_VARIABLE().getText()
        self.__bound_variables_by_index.append(local_bound_variable)
        return self.visitChildren(ctx)

    def visitQuantifierIndex(self, ctx: PuzzleDSLParser.QuantifierIndexContext):
        local_bound_variable = ctx.quantifier().BOUND_VARIABLE().getText()
        self.__bound_variables_by_quantifier.append(local_bound_variable)
        result = self.visitChildren(ctx)
        self.__bound_variables_by_quantifier.pop(-1)
        return result

    def visitIndexFunction(self, ctx: PuzzleDSLParser.IndexFunctionContext):
        result = self.visitChildren(ctx)
        self.__bound_variables_by_index.pop(-1)
        return result

    def visitGenerationSet(self, ctx: PuzzleDSLParser.GenerationSetContext):
        local_bound_variable = ctx.BOUND_VARIABLE().getText()
        self.__bound_variables_by_set.append(local_bound_variable)
        result = self.visitChildren(ctx)
        self.__bound_variables_by_set.pop(-1)
        return result

    def visitQuantifierBoolean(self, ctx: PuzzleDSLParser.QuantifierBooleanContext):
        local_bound_variable = ctx.quantifier().BOUND_VARIABLE().getText()
        self.__bound_variables_by_quantifier.append(local_bound_variable)
        result = self.visitChildren(ctx)
        self.__bound_variables_by_quantifier.pop(-1)
        return result


# ctx method

# getChild(int i)

# 指定したインデックス i の子ノードを取得します。
# getChildCount()

# 子ノードの数を返します。
# getText()

# このノードおよびすべての子ノードのテキストを連結して返します。
# children

# すべての子ノードのリストを返します。
# start

# このコンテキストの開始トークンを返します。
# stop

# このコンテキストの終了トークンを返します。
# getRuleContext(Class<? extends T> ctxType, int i)

# 指定したインデックス i の子ノードを指定したコンテキスト型で取得します。
# accept(ParseTreeVisitor<? extends T> visitor)

# ビジターパターンを使用してこのノードを訪問します。
# toStringTree(Parser parser)
