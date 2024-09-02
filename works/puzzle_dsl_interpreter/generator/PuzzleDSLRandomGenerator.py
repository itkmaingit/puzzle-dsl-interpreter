from __future__ import annotations

from generator.definitions.rules import (
    AlternativeRule,
    MultipleRule,
    OrderRule,
    Range,
    RawToken,
)
from generator.definitions.token import Token, TokenType
from generator.helpers import token


class File(OrderRule):
    def __init__(self):
        order = [
            StructsDeclaration,
            StructDefinitions,
            DomainHiddenDeclaration,
            DomainDefinitions,
            ConstraintsDeclaration,
            ConstraintsDefinitions,
        ]
        super().__init__(order=order)


class StructsDeclaration(OrderRule):
    def __init__(self):
        order = [token.StructsDeclaration, token.Newline]
        super().__init__(order=order)


class DomainHiddenDeclaration(OrderRule):
    def __init__(self):
        order = [token.DomainHiddenDeclaration, token.Newline]
        super().__init__(order=order)


class ConstraintsDeclaration(OrderRule):
    def __init__(self):
        order = [token.ConstraintsDeclaration, token.Newline]
        super().__init__(order=order)


class StructId(AlternativeRule):
    def __init__(self):
        choices = [
            token.P,
            token.C,
            token.EP,
            token.EC,
            token.NewStructId,
        ]
        super().__init__(choices=choices)


class StructDefinitionBody(OrderRule):
    def __init__(self):
        order = [
            token.Combine,
            token.LParen,
            StructId,
            token.Comma,
            RelationshipSet,
            token.RParen,
        ]
        super().__init__(order=order)


class StructDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent,
            token.NewStructId,
            token.Assign,
            StructDefinitionBody,
            token.Semi,
            token.Newline,
        ]
        super().__init__(order=order)

    def generate(self):
        super().generate()


class StructDefinitions(MultipleRule):
    def __init__(self):
        range = Range(min=1, max=3)
        rule = StructDefinition
        super().__init__(rule=rule, range=range)


class RelationshipId(AlternativeRule):
    def __init__(self):
        choices = [
            token.H,
            token.V,
            token.D,
        ]
        super().__init__(choices=choices)


class RelationshipSetBody(OrderRule):
    class AdditionalRelationshipId(MultipleRule):
        class RelationshipIdWithComma(OrderRule):
            def __init__(self):
                order = [token.Comma, RelationshipId]
                super().__init__(order=order)

        def __init__(self):
            rule = self.RelationshipIdWithComma
            range = Range(min=1, max=3)
            super().__init__(rule=rule, range=range)

    def __init__(self):
        order = [
            RelationshipId,
            self.AdditionalRelationshipId,
        ]
        super().__init__(order=order)


class RelationshipSet(OrderRule):
    def __init__(self):
        order = [
            token.LCurly,
            RelationshipSetBody,
            token.RCurly,
        ]
        super().__init__(order=order)


# FIXME: 出現確率に偏りがある(Numberが出ない)
class IntDomainValue(AlternativeRule):
    def __init__(self):
        choices = [
            self.IntDomainValue_1,
            self.IntDomainValue_2,
            token.Width,
            token.Height,
            self.IntDomainValue_5,
            token.Number,
        ]
        super().__init__(choices)

    class W_H(AlternativeRule):
        def __init__(self):
            choices = [token.Width, token.Height]
            super().__init__(choices)

    class P_M_T(AlternativeRule):
        def __init__(self):
            choices = [token.Plus, token.Minus, token.Times]
            super().__init__(choices)

    class IntDomainValue_1(OrderRule):
        def __init__(self):
            order = [IntDomainValue.W_H, IntDomainValue.P_M_T, IntDomainValue.W_H]
            super().__init__(order=order)

    class IntDomainValue_2(OrderRule):
        def __init__(self):
            order = [
                IntDomainValue.W_H,
                IntDomainValue.P_M_T,
                IntDomainValue,
            ]
            super().__init__(order=order)

    class IntDomainValue_5(OrderRule):
        def __init__(self):
            order = [
                IntDomainValue,
                IntDomainValue.P_M_T,
                IntDomainValue.W_H,
            ]
            super().__init__(order=order)


class RangeValue(OrderRule):
    class EndRangeValue(AlternativeRule):
        def __init__(self):
            choices = [
                IntDomainValue,
                token.Inf,
            ]
            super().__init__(choices=choices)

    def __init__(self):
        order = [
            IntDomainValue,
            token.Dots,
            self.EndRangeValue,
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
        super().__init__(choices=choices)


class DomainSetBody(OrderRule):
    class AdditionalDomainValue(MultipleRule):
        class DomainValueWithComma(OrderRule):
            def __init__(self):
                order = [token.Comma, DomainValue]
                super().__init__(order=order)

        def __init__(self):
            rule = self.DomainValueWithComma
            range = Range(min=1, max=2)
            super().__init__(rule=rule, range=range)

    def __init__(self):
        order = [
            DomainValue,
            self.AdditionalDomainValue,
        ]
        super().__init__(order=order)


class DomainSet(OrderRule):
    def __init__(self):
        order = [
            token.LCurly,
            DomainSetBody,
            token.RCurly,
        ]
        super().__init__(order=order)


class HiddenValue(AlternativeRule):
    def __init__(self):
        choices = [
            DomainValue,
            token.Undecided,
        ]
        super().__init__(choices=choices)


class HiddenSetBody(OrderRule):
    class AdditionalHiddenValue(MultipleRule):
        class HiddenValueWithComma(OrderRule):
            def __init__(self):
                order = [token.Comma, HiddenValue]
                super().__init__(order=order)

        def __init__(self):
            rule = self.HiddenValueWithComma
            range = Range(min=1, max=2)
            super().__init__(rule=rule, range=range)

    def __init__(self):
        order = [
            HiddenValue,
            self.AdditionalHiddenValue,
        ]
        super().__init__(order=order)


class HiddenSet(OrderRule):
    def __init__(self):
        order = [
            token.LCurly,
            HiddenSetBody,
            token.RCurly,
        ]
        super().__init__(order=order)


class DomainDefinitionBody(OrderRule):
    def __init__(self):
        order = [
            DomainSet,
            token.RightArrow,
            HiddenSet,
        ]
        super().__init__(order=order)


class PDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent,
            token.P,
            token.LeftRightArrow,
            DomainDefinitionBody,
            token.Semi,
            token.Newline,
        ]
        super().__init__(order=order)


class CDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent,
            token.C,
            token.LeftRightArrow,
            DomainDefinitionBody,
            token.Semi,
            token.Newline,
        ]
        super().__init__(order=order)


class EPDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent,
            token.EP,
            token.LeftRightArrow,
            DomainDefinitionBody,
            token.Semi,
            token.Newline,
        ]
        super().__init__(order=order)


class ECDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent,
            token.EC,
            token.LeftRightArrow,
            DomainDefinitionBody,
            token.Semi,
            token.Newline,
        ]
        super().__init__(order=order)


class CustomStructDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent,
            token.NewStructId,
            token.LeftRightArrow,
            DomainDefinitionBody,
            token.Semi,
            token.Newline,
        ]
        super().__init__(order=order)


class DomainDefinitions(OrderRule):
    class CustomStructDefinitions(MultipleRule):
        def __init__(self):
            rule = CustomStructDefinition
            range = Range(min=1, max=2)
            super().__init__(rule=rule, range=range)

    def __init__(self):
        order = [
            PDefinition,
            CDefinition,
            EPDefinition,
            ECDefinition,
            self.CustomStructDefinitions,
        ]
        super().__init__(order=order)


# TODO: Implement depth
class Int(AlternativeRule):
    DEPTH_LIMIT = 3

    class RecursionInt(OrderRule):
        class P_M_T(AlternativeRule):
            def __init__(self):
                choices = [token.Plus, token.Minus, token.Times]
                super().__init__(choices)

        def __init__(self):
            order = [Int, self.P_M_T, Int]
            super().__init__(order=order)

    class AbsoluteSet(OrderRule):
        def __init__(self):
            order = [token.Pipe, Set, token.Pipe]
            super().__init__(order=order)

    def __init__(self):
        choices = [
            token.Number,
            token.Width,
            token.Height,
            SolutionFunction,
            CrossFunction,
            CycleFunction,
            IndexFunction,
            self.AbsoluteSet,
            self.RecursionInt,
        ]
        super().__init__(choices=choices)


class PrimitiveValue(AlternativeRule):
    def __init__(self):
        choices = [Int, SolutionFunction, token.Null, token.ConstantId]
        super().__init__(choices=choices)


class Set(AlternativeRule):
    def __init__(self):
        choices = [
            token.Integer,
            BFunction,
            StructElement,
            ConnectFunction,
            GenerationSet,
        ]
        super().__init__(choices=choices)


class SolutionFunction(OrderRule):
    def __init__(self):
        order = [
            token.Solution,
            token.LParen,
            StructElement,
            token.RParen,
        ]
        super().__init__(order=order)


class BFunction(OrderRule):
    def __init__(self):
        order = [
            token.B,
            token.LParen,
            StructId,
            token.RParen,
        ]
        super().__init__(order=order)


class CrossFunction(OrderRule):
    def __init__(self):
        order = [
            token.Cross,
            token.LParen,
            StructElement,
            token.RParen,
        ]
        super().__init__(order=order)


class CycleFunction(OrderRule):
    def __init__(self):
        order = [
            token.Cycle,
            token.LParen,
            StructElement,
            token.RParen,
        ]
        super().__init__(order=order)


class AllDifferentFunction(OrderRule):
    def __init__(self):
        order = [
            token.AllDifferent,
            token.LParen,
            StructElement,
            token.RParen,
        ]
        super().__init__(order=order)


class IsRectangleFunction(OrderRule):
    def __init__(self):
        order = [
            token.IsRectangle,
            token.LParen,
            StructElement,
            token.RParen,
        ]
        super().__init__(order=order)


class IsSquareFunction(OrderRule):
    def __init__(self):
        order = [
            token.IsSquare,
            token.LParen,
            StructElement,
            token.RParen,
        ]
        super().__init__(order=order)


class ConnectFunction(OrderRule):
    def __init__(self):
        order = [
            token.Connect,
            token.LParen,
            StructElement,
            token.Comma,
            RelationshipSet,
            token.RParen,
        ]
        super().__init__(order=order)


class NoOverlapFunction(OrderRule):
    class MultipleNewStructID(MultipleRule):
        class NewStructIdWithComma(OrderRule):
            def __init__(self):
                order = [token.Comma, token.NewStructId]
                super().__init__(order=order)

        def __init__(self):
            rule = self.NewStructIdWithComma
            range = Range(min=1, max=3)
            super().__init__(rule=rule, range=range)

    def __init__(self):
        order = [
            token.NoOverlap,
            token.LParen,
            token.NewStructId,
            self.MultipleNewStructID,
            token.RParen,
        ]
        super().__init__(order=order)


class FillFunction(OrderRule):
    class MultipleNewStructID(MultipleRule):
        class NewStructIdWithComma(OrderRule):
            def __init__(self):
                order = [token.Comma, token.NewStructId]
                super().__init__(order=order)

        def __init__(self):
            rule = self.NewStructIdWithComma
            range = Range(min=1, max=3)
            super().__init__(rule=rule, range=range)

    def __init__(self):
        order = [
            token.Fill,
            token.LParen,
            token.NewStructId,
            self.MultipleNewStructID,
            token.RParen,
        ]
        super().__init__(order=order)


class Quantifier(OrderRule):
    class A_E(AlternativeRule):
        def __init__(self):
            choices = [token.All, token.Exists]
            super().__init__(choices=choices)

    def __init__(self):
        order = [
            self.A_E,
            token.LParen,
            token.BoundVariable,
            token.RParen,
            token.In,
            Set,
        ]
        super().__init__(order=order)


class Index(OrderRule):
    class S_I(AlternativeRule):
        def __init__(self):
            choices = [token.Subset, token.In]
            super().__init__(choices=choices)

    def __init__(self):
        order = [
            token.BoundVariable,
            self.S_I,
            Set,
        ]
        super().__init__(order=order)


## FIXME: Implement Depth
class QuantifierIndex(OrderRule):
    class I_Q(AlternativeRule):
        def __init__(self):
            choices = [Index, QuantifierIndex]
            super().__init__(choices=choices)

    def __init__(self):
        order = [
            Quantifier,
            token.Comma,
            token.LParen,
            self.I_Q,
            token.RParen,
        ]
        super().__init__(order=order)


class IndexFunction(OrderRule):
    class S_P(AlternativeRule):
        def __init__(self):
            choices = [token.Sum, token.Product]
            super().__init__(choices=choices)

    class I_Q(AlternativeRule):
        def __init__(self):
            choices = [Index, QuantifierIndex]
            super().__init__(choices=choices)

    def __init__(self):
        order = [
            self.S_P,
            token.LCurly,
            self.I_Q,
            token.RCurly,
            token.LParen,
            Int,
            token.RParen,
        ]
        super().__init__(order=order)


class StructElement(RawToken):
    def __init__(self):
        token = Token(type=TokenType.BOUND_VARIABLE)
        super().__init__(token=token)


class GenerationSet(OrderRule):
    def __init__(self):
        order = [
            token.LCurly,
            token.BoundVariable,
            token.Pipe,
            Constraint,
            token.RCurly,
        ]
        super().__init__(order=order)


class Boolean(AlternativeRule):
    class SetComparison(OrderRule):
        class S_I(AlternativeRule):
            def __init__(self):
                choices = [
                    token.Subset,
                    token.In,
                ]
                super().__init__(choices=choices)

        def __init__(self):
            order = [
                Set,
                self.S_I,
                Set,
            ]
            super().__init__(order=order)

    class PrimitiveValueInSet(OrderRule):
        def __init__(self):
            order = [
                PrimitiveValue,
                token.In,
                Set,
            ]
            super().__init__(order=order)

    class SetEquality(OrderRule):
        class N_E(AlternativeRule):
            def __init__(self):
                choices = [
                    token.NotEqual,
                    token.Equal,
                ]
                super().__init__(choices=choices)

        class S_E(AlternativeRule):
            def __init__(self):
                choices = [
                    Set,
                    token.EmptySet,
                ]
                super().__init__(choices=choices)

        def __init__(self):
            order = [
                Set,
                self.N_E,
                self.S_E,
            ]
            super().__init__(order=order)

    class PrimitiveValueComparison(OrderRule):
        class N_E(AlternativeRule):
            def __init__(self):
                choices = [
                    token.NotEqual,
                    token.Equal,
                ]
                super().__init__(choices=choices)

        def __init__(self):
            order = [
                PrimitiveValue,
                self.N_E,
                PrimitiveValue,
            ]
            super().__init__(order=order)

    def __init__(self):
        choices = [
            FillFunction,
            NoOverlapFunction,
            AllDifferentFunction,
            self.SetComparison,
            self.PrimitiveValueInSet,
            IsSquareFunction,
            IsRectangleFunction,
            self.SetEquality,
            self.PrimitiveValueComparison,
        ]
        super().__init__(choices=choices)


class SingleBoolean(AlternativeRule):
    def __init__(self):
        choices = [
            Boolean,
            NotBoolean,
            ParenthesizedBoolean,
            QuantifierBoolean,
        ]
        super().__init__(choices=choices)


class NotBoolean(OrderRule):
    def __init__(self):
        order = [
            token.Not,
            token.LParen,
            CompoundBoolean,
            token.RParen,
        ]
        super().__init__(order=order)


class ParenthesizedBoolean(OrderRule):
    def __init__(self):
        order = [
            token.LBracket,
            CompoundBoolean,
            token.RBracket,
        ]
        super().__init__(order=order)


class QuantifierBoolean(OrderRule):
    def __init__(self):
        order = [
            Quantifier,
            token.Comma,
            token.LParen,
            CompoundBoolean,
            token.RParen,
        ]
        super().__init__(order=order)


class CompoundBoolean(OrderRule):
    class MultipleAdditionalBoolean(MultipleRule):
        def __init__(self):
            rule = self.AdditionalBoolean
            range = Range(min=0, max=0)
            super().__init__(rule=rule, range=range)

        class AdditionalBoolean(OrderRule):
            class A_O_T_E(AlternativeRule):
                def __init__(self):
                    choices = [
                        token.And,
                        token.Or,
                        token.Then,
                        token.Equivalent,
                    ]
                    super().__init__(choices)

            def __init__(self):
                order = [self.A_O_T_E, SingleBoolean]
                super().__init__(order=order)

    def __init__(self):
        order = [SingleBoolean, self.MultipleAdditionalBoolean]
        super().__init__(order=order)


class Constraint(OrderRule):
    def __init__(self):
        order = [
            CompoundBoolean,
        ]
        super().__init__(order=order)


class ConstraintDefinition(OrderRule):
    def __init__(self):
        order = [
            token.Indent,
            Constraint,
            token.Semi,
            token.Newline,
        ]
        super().__init__(order=order)


class ConstraintsDefinitions(MultipleRule):
    def __init__(self):
        rule = ConstraintDefinition
        range = Range(min=1, max=3)
        super().__init__(rule=rule, range=range)
