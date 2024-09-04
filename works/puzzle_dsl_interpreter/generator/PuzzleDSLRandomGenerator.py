from __future__ import annotations

from generator.definitions.rules import (
    AlternativeRule,
    MultipleRule,
    OrderRule,
    Range,
    SingleRule,
)
from generator.definitions.token import Token, TokenType
from generator.helpers import token
from generator.helpers.operators import lottery, repeat
from generator.stores.context import Context
from generator.stores.store import store
from generator.utils.logger import logger


class File(OrderRule):
    def __init__(self):
        order = [
            StructsDeclaration(),
            StructDefinitions(),
            token.Newline(),
            DomainHiddenDeclaration(),
            DomainDefinitions(),
            token.Newline(),
            ConstraintsDeclaration(),
            ConstraintsDefinitions(),
        ]
        super().__init__(order=order)


class StructsDeclaration(OrderRule):
    def __init__(self):
        order = [
            token.StructsDeclaration(),
            token.Newline(),
        ]
        super().__init__(order=order)


class DomainHiddenDeclaration(OrderRule):
    def __init__(self):
        order = [
            token.DomainHiddenDeclaration(),
            token.Newline(),
        ]
        super().__init__(order=order)


class ConstraintsDeclaration(OrderRule):
    def __init__(self):
        order = [
            token.ConstraintsDeclaration(),
            token.Newline(),
        ]
        super().__init__(order=order)


class StructId(AlternativeRule):
    def __init__(self):
        choices = [
            token.P,
            token.C,
            token.EP,
            token.EC,
        ]
        if (
            store.count_new_structs >= 2
            or store.context != Context.STRUCT_DEFINITION_BODY
        ):
            choices.append(token.NewStructId)
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class StructDefinitionBody(OrderRule):
    def __init__(self):
        store.enter(Context.STRUCT_DEFINITION_BODY, self.__class__.__name__)
        order = [
            token.Combine(),
            token.LParen(),
            StructId(),
            token.Comma(),
            token.Space(),
            RelationshipSet(),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.exit(self.__class__.__name__)


class StructDefinition(OrderRule):
    def __init__(self):
        store.enter(Context.STRUCT_DEFINITION, self.__class__.__name__)
        order = [
            token.Indent(),
            token.NewStructId(),
            token.Space(),
            token.Assign(),
            token.Space(),
            StructDefinitionBody(),
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)
        store.exit(self.__class__.__name__)


class StructDefinitions(MultipleRule):
    def __init__(self):
        range = Range(min=1, max=3)
        rule = StructDefinition
        order = repeat(rule, range)
        super().__init__(order=order)
        store.exit_struct_definitions()


class RelationshipSetBody(OrderRule):
    class AdditionalRelationshipId(MultipleRule):
        class RelationshipIdWithComma(OrderRule):
            def __init__(self):
                order = [
                    token.Comma(),
                    token.Space(),
                    token.RelationshipId(),
                ]
                super().__init__(order=order)

        def __init__(self):
            rule = self.RelationshipIdWithComma
            range = Range(min=0, max=2)
            order = repeat(rule, range)
            super().__init__(order=order)

    def __init__(self):
        store.enter_relationship_set_body()
        order = [
            token.RelationshipId(),
            self.AdditionalRelationshipId(),
        ]
        super().__init__(order=order)
        store.exit__relationship_set_body()


class RelationshipSet(OrderRule):
    def __init__(self):
        order = [
            token.LCurly(),
            token.Space(),
            RelationshipSetBody(),
            token.Space(),
            token.RCurly(),
        ]
        super().__init__(order=order)


# FIXME: 出現確率に偏りがある(Numberが出ない)
# FIXME: Through Semantic Error
# TODO: Fixed Output
class IntDomainValue(AlternativeRule):
    class W_H(AlternativeRule):
        def __init__(self):
            choices = [
                token.Width,
                token.Height,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    class P_M_T(AlternativeRule):
        def __init__(self):
            choices = [
                token.Plus,
                token.Minus,
                token.Times,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    class IntDomainValue_1(OrderRule):
        def __init__(self):
            order = [
                IntDomainValue.W_H(),
                token.Space(),
                IntDomainValue.P_M_T(),
                token.Space(),
                IntDomainValue.W_H(),
            ]
            super().__init__(order=order)

    class IntDomainValue_2(OrderRule):
        def __init__(self):
            order = [
                IntDomainValue.W_H(),
                token.Space(),
                IntDomainValue.P_M_T(),
                token.Space(),
                IntDomainValue(),
            ]
            super().__init__(order=order)

    class IntDomainValue_5(OrderRule):
        def __init__(self):
            order = [
                IntDomainValue(),
                token.Space(),
                IntDomainValue.P_M_T(),
                token.Space(),
                IntDomainValue.W_H(),
            ]
            super().__init__(order=order)

    def __init__(self):
        choices = [
            self.IntDomainValue_1,
            self.IntDomainValue_2,
            token.Width,
            token.Height,
            self.IntDomainValue_5,
            token.Number,
        ]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class RangeValue(OrderRule):
    class EndRangeValue(AlternativeRule):
        def __init__(self):
            choices = [
                IntDomainValue,
                token.Inf,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    def __init__(self):
        order = [
            IntDomainValue(),
            token.Dots(),
            self.EndRangeValue(),
        ]
        super().__init__(order=order)


class DomainValue(AlternativeRule):
    def __init__(self):
        choices = [
            IntDomainValue,
            RangeValue,
            token.Null,
            token.ConstantId,
        ]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class DomainSetBody(OrderRule):
    class AdditionalDomainValue(MultipleRule):
        class DomainValueWithComma(OrderRule):
            def __init__(self):
                order = [
                    token.Comma(),
                    token.Space(),
                    DomainValue(),
                ]
                super().__init__(order=order)

        def __init__(self):
            rule = self.DomainValueWithComma
            range = Range(min=1, max=2)
            order = repeat(rule, range)
            super().__init__(order=order)

    def __init__(self):
        store.enter(Context.DOMAIN_SET_BODY, self.__class__.__name__)
        order = [
            DomainValue(),
            self.AdditionalDomainValue(),
        ]
        super().__init__(order=order)
        store.exit(self.__class__.__name__)


class DomainSet(OrderRule):
    def __init__(self):
        order = [
            token.LCurly(),
            token.Space(),
            DomainSetBody(),
            token.Space(),
            token.RCurly(),
        ]
        super().__init__(order=order)


class HiddenValue(AlternativeRule):
    def __init__(self):
        choices = [
            DomainValue,
            token.Undecided,
        ]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class HiddenSetBody(OrderRule):
    class AdditionalHiddenValue(MultipleRule):
        class HiddenValueWithComma(OrderRule):
            def __init__(self):
                order = [
                    token.Comma(),
                    token.Space(),
                    HiddenValue(),
                ]
                super().__init__(order=order)

        def __init__(self):
            rule = self.HiddenValueWithComma
            range = Range(min=1, max=2)
            order = repeat(rule, range)
            super().__init__(order=order)

    def __init__(self):
        order = [
            HiddenValue(),
            self.AdditionalHiddenValue(),
        ]
        super().__init__(order=order)


class HiddenSet(OrderRule):
    def __init__(self):
        order = [
            token.LCurly(),
            token.Space(),
            HiddenSetBody(),
            token.Space(),
            token.RCurly(),
        ]
        super().__init__(order=order)


# FIXME: いずれランダムに出力するようにする
class DomainDefinitionBody(OrderRule):
    def __init__(self):
        order = [
            DomainSet(),
            token.Space(),
            token.RightArrow(),
            token.Space(),
            HiddenSet(),
        ]
        super().__init__(order=order)

    # for fixed states
    def generate(self) -> list[Token]:
        fixed_state = [
            Token(type=TokenType.LCURLY),
            Token(type=TokenType.SPACE),
            Token(type=TokenType.NUMBER, ok=["1"]),
            Token(type=TokenType.DOTS),
            Token(type=TokenType.NUMBER, ok=["4"]),
            Token(type=TokenType.SPACE),
            Token(type=TokenType.RCURLY),
            Token(type=TokenType.SPACE),
            Token(type=TokenType.RIGHT_ARROW),
            Token(type=TokenType.SPACE),
            Token(type=TokenType.LCURLY),
            Token(type=TokenType.SPACE),
            Token(type=TokenType.NUMBER, ok=["1"]),
            Token(type=TokenType.DOTS),
            Token(type=TokenType.NUMBER, ok=["4"]),
            Token(type=TokenType.COMMA),
            Token(type=TokenType.UNDECIDED),
            Token(type=TokenType.SPACE),
            Token(type=TokenType.RCURLY),
        ]

        return fixed_state


class PDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent(),
            token.P(),
            token.Space(),
            token.LeftRightArrow(),
            token.Space(),
            DomainDefinitionBody(),
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)


class CDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent(),
            token.C(),
            token.Space(),
            token.LeftRightArrow(),
            token.Space(),
            DomainDefinitionBody(),
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)


class EPDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent(),
            token.EP(),
            token.Space(),
            token.LeftRightArrow(),
            token.Space(),
            DomainDefinitionBody(),
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)


class ECDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent(),
            token.EC(),
            token.Space(),
            token.LeftRightArrow(),
            token.Space(),
            DomainDefinitionBody(),
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)


class CustomStructDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent(),
            token.NewStructId(),
            token.Space(),
            token.LeftRightArrow(),
            token.Space(),
            DomainDefinitionBody(),
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)


class DomainDefinitions(OrderRule):
    class CustomStructDefinitions(MultipleRule):
        def __init__(self):
            rule = CustomStructDefinition
            range = Range(
                min=store.count_new_structs,
                max=store.count_new_structs,
            )
            order = repeat(rule, range)
            super().__init__(order=order)

    def __init__(self):
        store.enter_domain_definitions()
        order = [
            PDefinition(),
            CDefinition(),
            EPDefinition(),
            ECDefinition(),
            self.CustomStructDefinitions(),
        ]
        super().__init__(order=order)
        store.exit_domain_difinitions()


class Int(AlternativeRule):
    class RecursionInt(OrderRule):
        class P_M_T(AlternativeRule):
            def __init__(self):
                choices = [
                    token.Plus,
                    token.Minus,
                    token.Times,
                ]
                choice = lottery(choices, self.__class__.__name__)()
                super().__init__(choice=choice)

        def __init__(self):
            order = [
                Int(),
                token.Space(),
                self.P_M_T(),
                token.Space(),
                Int(),
            ]
            super().__init__(order=order)

    class AbsoluteSet(OrderRule):
        def __init__(self):
            order = [
                token.LeftAbsolute(),
                Set(),
                token.RightAbsolute(),
            ]
            super().__init__(order=order)

    def __init__(self):
        choices = [
            token.Number,
            token.Width,
            token.Height,
            self.AbsoluteSet,
            self.RecursionInt,
        ]
        if store.exists_bound_variables():
            choices += [SolutionFunction, CrossFunction, CycleFunction, IndexFunction]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class PrimitiveValue(AlternativeRule):
    def __init__(self):
        choices = [
            Int,
            token.Null,
            token.ConstantId,
        ]
        if store.exists_bound_variables():
            choices.append(SolutionFunction)
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class Set(AlternativeRule):
    def __init__(self):
        choices = [
            BFunction,
            GenerationSet,
        ]
        if len(store.bound_variables) >= 1:
            choices += [StructElement, ConnectFunction]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class SolutionFunction(OrderRule):
    def __init__(self):
        order = [
            token.Solution(),
            token.LParen(),
            StructElement(),
            token.RParen(),
        ]
        super().__init__(order=order)


class BFunction(OrderRule):
    WEIGHT = 1

    def __init__(self):
        store.enter(Context.B_FUNCTION, self.__class__.__name__)
        order = [
            token.B(),
            token.LParen(),
            StructId(),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.exit(self.__class__.__name__)


class CrossFunction(OrderRule):
    def __init__(self):
        order = [
            token.Cross(),
            token.LParen(),
            StructElement(),
            token.RParen(),
        ]
        super().__init__(order=order)


class CycleFunction(OrderRule):
    def __init__(self):
        order = [
            token.Cycle(),
            token.LParen(),
            StructElement(),
            token.RParen(),
        ]
        super().__init__(order=order)


class AllDifferentFunction(OrderRule):
    def __init__(self):
        order = [
            token.AllDifferent(),
            token.LParen(),
            StructElement(),
            token.RParen(),
        ]
        super().__init__(order=order)


class IsRectangleFunction(OrderRule):
    def __init__(self):
        order = [
            token.IsRectangle(),
            token.LParen(),
            StructElement(),
            token.RParen(),
        ]
        super().__init__(order=order)


class IsSquareFunction(OrderRule):
    def __init__(self):
        order = [
            token.IsSquare(),
            token.LParen(),
            StructElement(),
            token.RParen(),
        ]
        super().__init__(order=order)


class ConnectFunction(OrderRule):
    def __init__(self):
        order = [
            token.Connect(),
            token.LParen(),
            StructElement(),
            token.Comma(),
            token.Space(),
            RelationshipSet(),
            token.RParen(),
        ]
        super().__init__(order=order)


class NoOverlapFunction(OrderRule):
    class MultipleNewStructID(MultipleRule):
        class NewStructIdWithComma(OrderRule):
            def __init__(self):
                order = [
                    token.Comma(),
                    token.Space(),
                    token.NewStructId(),
                ]
                super().__init__(order=order)

        def __init__(self):
            rule = self.NewStructIdWithComma
            range = Range(min=1, max=store.count_new_structs - 1)
            order = repeat(rule, range)
            super().__init__(order=order)

    def __init__(self):
        store.enter_board_function()
        order = [
            token.NoOverlap(),
            token.LParen(),
            token.NewStructId(),
            self.MultipleNewStructID(),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.exit_board_function()


class FillFunction(OrderRule):
    class MultipleNewStructID(MultipleRule):
        class NewStructIdWithComma(OrderRule):
            def __init__(self):
                order = [
                    token.Comma(),
                    token.Space(),
                    token.NewStructId(),
                ]
                super().__init__(order=order)

        def __init__(self):
            rule = self.NewStructIdWithComma
            range = Range(min=1, max=store.count_new_structs - 1)
            order = repeat(rule, range)
            super().__init__(order=order)

    def __init__(self):
        store.enter_board_function()
        order = [
            token.Fill(),
            token.LParen(),
            token.NewStructId(),
            self.MultipleNewStructID(),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.exit_board_function()


class Quantifier(OrderRule):
    class A_E(AlternativeRule):
        def __init__(self):
            choices = [
                token.All,
                token.Exists,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    def __init__(self):
        order = [
            self.A_E(),
            token.LParen(),
            token.BoundVariable(),
            token.RParen(),
            token.Space(),
            token.In(),
            token.Space(),
        ]
        concealed_value = store.conceal_bound_variable()
        order += [Set()]
        store.restore_bound_variable(concealed_value)
        super().__init__(order=order)


class Index(OrderRule):
    class S_I(AlternativeRule):
        def __init__(self):
            choices = [
                token.Subset,
                token.In,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    def __init__(self):
        order = [
            token.BoundVariable(),
            token.Space(),
            self.S_I(),
            token.Space(),
            Set(),
        ]
        super().__init__(order=order)


## FIXME: Implement Depth
class QuantifierIndex(OrderRule):
    class I_Q(AlternativeRule):
        def __init__(self):
            choices = [
                Index,
                QuantifierIndex,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    def __init__(self):
        store.enter(Context.QUANTIFIER_INDEX, self.__class__.__name__)
        order = [
            Quantifier(),
            token.Comma(),
            token.Space(),
            token.LParen(),
            self.I_Q(),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.exit_with_cleanup(self.__class__.__name__)


class IndexFunction(OrderRule):
    class S_P(AlternativeRule):
        def __init__(self):
            choices = [
                token.Sum,
                token.Product,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    class I_Q(AlternativeRule):
        def __init__(self):
            choices = [
                Index,
                QuantifierIndex,
            ]
            choice = lottery(choices, self.__class__.__name__)()
            super().__init__(choice=choice)

    def __init__(self):
        store.enter(Context.INDEX_FUNCTION, self.__class__.__name__)
        order = [
            self.S_P(),
            token.LCurly(),
            token.Space(),
            self.I_Q(),
            token.Space(),
            token.RCurly(),
            token.LParen(),
            Int(),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.exit(self.__class__.__name__)


class StructElement(SingleRule):
    def __init__(self):
        store.enter(Context.STRUCT_ELEMENT, self.__class__.__name__)
        rule = token.BoundVariable()
        super().__init__(rule=rule)
        store.exit(self.__class__.__name__)


class GenerationSet(OrderRule):
    def __init__(self):
        store.enter(Context.GENERATION_SET, self.__class__.__name__)
        order = [
            token.LCurly(),
            token.Space(),
            token.BoundVariable(),
            token.Space(),
            token.In(),
            token.Space(),
        ]
        concealed_value = store.conceal_bound_variable()
        order.append(Set())
        store.register_bound_variables(concealed_value)
        order += [
            token.Space(),
            token.Pipe(),
            token.Space(),
            CompoundBoolean(),
            token.Space(),
            token.RCurly(),
        ]
        super().__init__(order=order)
        store.exit_with_cleanup(self.__class__.__name__)


class Boolean(AlternativeRule):
    WEIGHT = 5

    class SetComparison(OrderRule):
        class S_I(AlternativeRule):
            def __init__(self):
                choices = [
                    token.Subset,
                    token.In,
                ]
                choice = lottery(choices, self.__class__.__name__)()
                super().__init__(choice=choice)

        def __init__(self):
            order = [
                Set(),
                token.Space(),
                self.S_I(),
                token.Space(),
                Set(),
            ]
            super().__init__(order=order)

    # class IntInInterger(OrderRule):
    #     def __init__(self):
    #         order = [
    #             Int(),
    #             token.Space(),
    #             token.In(),
    #             token.Space(),
    #             token.Integer(),
    #         ]
    #         super().__init__(order=order)

    class SetEquality(OrderRule):
        class N_E(AlternativeRule):
            def __init__(self):
                choices = [
                    token.NotEqual,
                    token.Equal,
                ]
                choice = lottery(choices, self.__class__.__name__)()
                super().__init__(choice=choice)

        class S_E(AlternativeRule):
            def __init__(self):
                choices = [
                    Set,
                    token.EmptySet,
                ]
                choice = lottery(choices, self.__class__.__name__)()
                super().__init__(choice=choice)

        def __init__(self):
            order = [
                Set(),
                token.Space(),
                self.N_E(),
                token.Space(),
                self.S_E(),
            ]
            super().__init__(order=order)

    class PrimitiveValueComparison(OrderRule):
        class N_E_M_T(AlternativeRule):
            def __init__(self):
                choices = [
                    token.NotEqual,
                    token.Equal,
                    token.MoreThan,
                    token.LessThan,
                ]
                choice = lottery(choices, self.__class__.__name__)()
                super().__init__(choice=choice)

        def __init__(self):
            order = [
                PrimitiveValue(),
                token.Space(),
                self.N_E_M_T(),
                token.Space(),
                PrimitiveValue(),
            ]
            super().__init__(order=order)

    def __init__(self):
        choices = [
            # FillFunction,
            # NoOverlapFunction,
            self.SetComparison,
            # self.IntInInterger,
            self.SetEquality,
            self.PrimitiveValueComparison,
        ]
        if store.exists_bound_variables():
            choices += [AllDifferentFunction, IsSquareFunction, IsRectangleFunction]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class SingleBoolean(AlternativeRule):
    PREVENT_NOT_BOOLEAN = False

    def __init__(self):
        choices = [
            Boolean,
            # ParenthesizedBoolean,
            QuantifierBoolean,
        ]
        if not self.PREVENT_NOT_BOOLEAN:
            choices.append(NotBoolean)
        choice = lottery(choices, self.__class__.__name__)
        logger.debug(choice.__name__)
        if choice.__name__ == "NotBoolean":
            self.PREVENT_NOT_BOOLEAN = True
        super().__init__(choice=choice())


class NotBoolean(OrderRule):
    def __init__(self):
        order = [
            token.Not(),
            token.LParen(),
            CompoundBoolean(),
            token.RParen(),
        ]
        super().__init__(order=order)


class ParenthesizedBoolean(OrderRule):
    def __init__(self):
        order = [
            token.LBracket(),
            CompoundBoolean(),
            token.RBracket(),
        ]
        super().__init__(order=order)


class QuantifierBoolean(OrderRule):
    def __init__(self):
        store.enter(Context.QUANTIFIER_BOOLEAN, self.__class__.__name__)
        order = [
            Quantifier(),
            token.Comma(),
            token.Space(),
            token.LParen(),
            CompoundBoolean(),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.exit_with_cleanup(self.__class__.__name__)


class CompoundBoolean(OrderRule):
    WEIGHT = 10

    class MultipleAdditionalBoolean(MultipleRule):
        def __init__(self):
            rule = self.AdditionalBoolean
            range = Range(min=0, max=1)
            order = repeat(rule, range)
            super().__init__(order=order)

        class AdditionalBoolean(OrderRule):
            class A_O_T_E(AlternativeRule):
                def __init__(self):
                    choices = [
                        token.And,
                        token.Or,
                        token.Then,
                        token.Equivalent,
                    ]
                    choice = lottery(choices, self.__class__.__name__)()
                    super().__init__(choice=choice)

            def __init__(self):
                order = [
                    token.Space(),
                    self.A_O_T_E(),
                    token.Space(),
                    SingleBoolean(),
                ]
                super().__init__(order=order)

    def __init__(self):
        order = [
            SingleBoolean(),
            self.MultipleAdditionalBoolean(),
        ]
        super().__init__(order=order)


# TODO: Apply FillFunction and NoOverlapFunction
class Constraint(AlternativeRule):
    def __init__(self):
        choices = [
            CompoundBoolean,
            # FillFunction,
            # NoOverlapFunction,
        ]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)


class ConstraintDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent(),
            Constraint(),
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)
        store.exit_constraint_definition()


class ConstraintsDefinitions(MultipleRule):
    def __init__(self):
        rule = ConstraintDefinition
        range = Range(min=3, max=5)
        order = repeat(rule, range)
        super().__init__(order=order)
