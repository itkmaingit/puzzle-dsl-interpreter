from __future__ import annotations

import copy

from generator.checker.dataclass import Attribute
from generator.definitions.constants import BoundVariableData
from generator.definitions.errors import UnableToContinueError
from generator.definitions.rules import (
    AlternativeRule,
    MultipleRule,
    OrderRule,
    Range,
    SingleRule,
)
from generator.helpers import token
from generator.helpers.operators import lottery, repeat
from generator.stores.context import Context
from generator.stores.store import store
from generator.utils.logger import logger


class File(OrderRule):
    def __init__(self):
        store.initialize()
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

    def to_json(self):
        struct_definitions = self.get(1).to_json()
        domain_definitions = self.get(4).to_json()
        constraints_definitions = self.get(7).to_json()
        return {
            "structs": struct_definitions,
            "domain": domain_definitions,
            "constraints": constraints_definitions,
        }


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
    def __init__(self, attr: Attribute | None = None):
        match attr:
            case Attribute.P:
                choices = [token.P]
            case Attribute.C:
                choices = [token.C]
            case Attribute.Ec:
                choices = [token.EC]
            case Attribute.Ep:
                choices = [token.EP]
            case _:
                choices = [token.P, token.C, token.EC, token.EP]
        # if (
        #     store.count_new_structs >= 2
        #     or store.context != Context.STRUCT_DEFINITION_BODY
        # ):
        #     choices.append(token.NewStructId)
        choice = lottery(choices, self.__class__.__name__)()
        self.__attr = choice.attr
        super().__init__(choice=choice)
        store.register_target_structs(choice.to_json())

    @property
    def attr(self) -> Attribute:
        return self.__attr


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

    @property
    def base(self):
        return self.get(2)

    @property
    def relationship(self):
        return self.get(5)


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
        range = Range(min=0, max=0)
        rule = StructDefinition
        order = repeat(rule, range)
        super().__init__(order=order)
        store.exit_struct_definitions()

    def to_json(self):
        properties: list[dict] = []
        for el in self.order:
            if isinstance(el, OrderRule):
                name = el.get(1).to_json()
                base = el.get(5).base.to_json()
                relationship = el.get(5).relationship.to_json()
                property = {
                    "name": name,
                    "base": base,
                    "relationship": relationship,
                }
                properties.append(property)
            else:
                logger.debug("誤った型に入力されています。")
        return properties


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

            def to_json(self):
                relationship = self.get(2)
                return relationship.to_json()

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

    def to_json(self):
        relationships = self.get(2).to_json()
        return relationships


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
            # self.IntDomainValue_1,
            # self.IntDomainValue_2,
            token.Width,
            token.Height,
            # self.IntDomainValue_5,
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
            # RangeValue,
            token.Null,
        ]
        if len(store.constants) >= 1:
            choices.append(token.ConstantId)
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)

    def to_json(self):
        return self.choice.to_json()


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

            def to_json(self):
                ret = self.get(2).to_json()
                return ret

        def __init__(self):
            rule = self.DomainValueWithComma
            range = Range(min=1, max=2)
            order = repeat(rule, range)
            super().__init__(order=order)

        def to_json(self):
            ret = []
            for el in self.order:
                if isinstance(el.get(2).to_json(), list):
                    ret.extend(el.get(2).to_json())
                else:
                    ret.append(el.get(2).to_json())
            return ret

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

    def to_json(self):
        ret = self.get(2).to_json()
        return ret


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

            def to_json(self):
                ret = self.get(2).to_json()
                return ret

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

    def to_json(self):
        ret = self.get(2).to_json()
        return ret


# FIXME: いずれランダムに出力するようにする
# TODO: DomainSet > HiddenSet/undecidedとなる出力を行う。
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

    def to_json(self):
        domain = self.get(0).to_json()
        hidden = self.get(4).to_json()
        return domain, hidden

    # for fixed states
    # def generate(self) -> list[Token]:
    #     fixed_state = [
    #         Token(type=TokenType.LCURLY),
    #         Token(type=TokenType.SPACE),
    #         Token(type=TokenType.NUMBER, ok=["1"]),
    #         Token(type=TokenType.DOTS),
    #         Token(type=TokenType.NUMBER, ok=["4"]),
    #         Token(type=TokenType.SPACE),
    #         Token(type=TokenType.RCURLY),
    #         Token(type=TokenType.SPACE),
    #         Token(type=TokenType.RIGHT_ARROW),
    #         Token(type=TokenType.SPACE),
    #         Token(type=TokenType.LCURLY),
    #         Token(type=TokenType.SPACE),
    #         Token(type=TokenType.NUMBER, ok=["1"]),
    #         Token(type=TokenType.DOTS),
    #         Token(type=TokenType.NUMBER, ok=["4"]),
    #         Token(type=TokenType.COMMA),
    #         Token(type=TokenType.UNDECIDED),
    #         Token(type=TokenType.SPACE),
    #         Token(type=TokenType.RCURLY),
    #     ]

    #     return fixed_state


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

    def to_json(self):
        name = self.get(1).to_json()
        domain, hidden = self.get(5).to_json()
        logger.debug(domain)
        logger.debug(hidden)
        ret = {
            "name": name,
            "domain": domain,
            "hidden": hidden,
        }
        return ret


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

    def to_json(self):
        name = self.get(1).to_json()
        domain, hidden = self.get(5).to_json()
        return {
            "name": name,
            "domain": domain,
            "hidden": hidden,
        }


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

    def to_json(self):
        name = self.get(1).to_json()
        domain, hidden = self.get(5).to_json()
        return {
            "name": name,
            "domain": domain,
            "hidden": hidden,
        }


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

    def to_json(self):
        name = self.get(1).to_json()
        domain, hidden = self.get(5).to_json()
        return {
            "name": name,
            "domain": domain,
            "hidden": hidden,
        }


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

    def to_json(self):
        name = self.get(1).to_json()
        domain, hidden = self.get(5).to_json()
        return {
            "name": name,
            "domain": domain,
            "hidden": hidden,
        }


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

        def to_json(self):
            ret = {
                "type": "value",
                "name": "int_operation",
                "properties": {"op": self.get(2).to_json()},
                "args": {
                    "left": self.get(0).to_json(),
                    "right": self.get(4).to_json(),
                },
            }
            return ret

    class AbsoluteSet(OrderRule):
        def __init__(self):
            order = [
                token.LeftAbsolute(),
                PartialSet(),
                token.RightAbsolute(),
            ]
            super().__init__(order=order)

        def to_json(self):
            ret = {
                "type": "value",
                "name": "absolute_set",
                "args": self.get(1).to_json(),
            }
            return ret

    def __init__(self):
        choices = [
            # token.Number,
            token.Width,
            token.Height,
            self.AbsoluteSet,
            self.RecursionInt,
        ]
        if store.exists_bound_variables():
            choices.append(SolutionFunction)
        if store.exists_specific_attr_bound_variables(Attribute.P):
            choices.append(CrossFunction)
        if store.exists_specific_attr_bound_variables(Attribute.C):
            choices.append(CycleFunction)
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)

    def to_json(self):
        args = super().to_json()
        ret = {
            "type": "value",
            "name": "int",
            "args": {"value": copy.deepcopy(args)},
        }
        return ret


class PrimitiveValue(AlternativeRule):
    def __init__(self):
        choices = [
            token.Null,
        ]
        if len(store.constants) >= 1:
            choices.append(token.ConstantId)
        if store.exists_bound_variables():
            choices.append(SolutionFunction)
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)

    def to_json(self):
        ret = {
            "type": "value",
            "name": "primitive",
            "args": {"value": super().to_json()},
        }
        return ret


class Set(AlternativeRule):
    def __init__(self, attr: Attribute | None = None):
        choices = [
            BFunction,
            GenerationSet,
        ]
        if len(store.bound_variables) >= 1:
            choices += [ConnectFunction]
        choice = lottery(choices, self.__class__.__name__)(attr)
        self.__attr = choice.attr
        super().__init__(choice=choice)

    @property
    def attr(self) -> Attribute:
        return self.__attr


class PartialSet(AlternativeRule):
    def __init__(self):
        choices = [
            GenerationSet,
        ]
        if len(store.bound_variables) >= 1:
            choices += [ConnectFunction]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)
        self.__attr = choice.attr

    @property
    def attr(self) -> Attribute:
        return self.__attr


class SolutionFunction(OrderRule):
    WEIGHT = 4

    def __init__(self):
        order = [
            token.Solution(),
            token.LParen(),
            StructElement(None),
            token.RParen(),
        ]
        super().__init__(order=order)

    def to_json(self):
        ret = {
            "type": "value",
            "name": "solution",
            "args": {"variable": self.get(2).to_json()},
        }
        return ret


class BFunction(OrderRule):
    def __init__(self, attr: Attribute | None):
        store.enter(Context.B_FUNCTION, self.__class__.__name__)
        b = token.B()
        lparen = token.LParen()
        struct_id = StructId(attr)
        rparen = token.RParen()
        self.__attr = struct_id.attr
        order = [b, lparen, struct_id, rparen]

        super().__init__(order=order)
        store.exit(self.__class__.__name__)

    def to_json(self):
        ret = {
            "type": "set",
            "name": "B",
            "args": {"struct": self.get(2).to_json()},
        }
        return ret

    @property
    def attr(self) -> Attribute:
        return self.__attr


class CrossFunction(OrderRule):
    def __init__(self):
        order = [
            token.Cross(),
            token.LParen(),
            StructElement(Attribute.P),
            token.RParen(),
        ]
        super().__init__(order=order)
        store.register_target_structs("Ep")

    def to_json(self):
        ret = {
            "type": "value",
            "name": "cross",
            "args": {"variable": self.get(2).to_json()},
        }
        return ret


class CycleFunction(OrderRule):
    def __init__(self):
        order = [
            token.Cycle(),
            token.LParen(),
            StructElement(Attribute.C),
            token.RParen(),
        ]
        store.register_target_structs("Ep")
        super().__init__(order=order)

    def to_json(self):
        ret = {
            "type": "value",
            "name": "cycle",
            "args": {"variable": self.get(2).to_json()},
        }
        return ret


class AllDifferentFunction(OrderRule):
    def __init__(self):
        order = [
            token.AllDifferent(),
            token.LParen(),
            PartialSet(),
            token.RParen(),
        ]
        super().__init__(order=order)

    def to_json(self):
        ret = {
            "type": "boolean",
            "name": "all_different",
            "args": {"variable": self.get(2).to_json()},
        }
        return ret


class IsRectangleFunction(OrderRule):
    def __init__(self):
        order = [
            token.IsRectangle(),
            token.LParen(),
            PartialSet(),
            token.RParen(),
        ]
        super().__init__(order=order)

    def to_json(self):
        ret = {
            "type": "boolean",
            "name": "is_rectangle",
            "args": {"variable": self.get(2).to_json()},
        }
        return ret


class IsSquareFunction(OrderRule):
    def __init__(self):
        order = [
            token.IsSquare(),
            token.LParen(),
            PartialSet(),
            token.RParen(),
        ]
        super().__init__(order=order)

    def to_json(self):
        ret = {
            "type": "boolean",
            "name": "is_square",
            "args": {"variable": self.get(2).to_json()},
        }
        return ret


class ConnectFunction(OrderRule):
    WEIGHT = 3

    def __init__(self, attr: Attribute | None = None):
        struct_element = StructElement(attr)
        self.__attr = struct_element.attr
        order = [
            token.Connect(),
            token.LParen(),
            struct_element,
            token.Comma(),
            token.Space(),
            RelationshipSet(),
            token.RParen(),
        ]
        super().__init__(order=order)

    def to_json(self):
        ret = {
            "type": "set",
            "name": "connect",
            "args": {
                "variable": self.get(2).to_json(),
                "relationship": self.get(5).to_json(),
            },
        }
        return ret

    @property
    def attr(self) -> Attribute:
        return self.__attr


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

            def to_json(self):
                ret = self.get(2).to_json()
                return ret

        def __init__(self):
            rule = self.NewStructIdWithComma
            range = Range(min=0, max=store.count_new_structs - 1)
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

    def to_json(self):
        args = [self.get(2).to_json()]
        args += self.get(3).to_json()
        ret = {
            "type": "boolean",
            "name": "no_overlap",
            "args": args,
        }
        return ret


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

            def to_json(self):
                ret = self.get(2).to_json()
                return ret

        def __init__(self):
            rule = self.NewStructIdWithComma
            range = Range(min=0, max=store.count_new_structs - 1)
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

    def to_json(self):
        args = [self.get(2).to_json()]
        args += self.get(3).to_json()
        ret = {
            "type": "boolean",
            "name": "fill",
            "args": args,
        }
        return ret


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
        universal_set = Set()
        attr = universal_set.attr
        order = [
            self.A_E(),
            token.LParen(),
            token.BoundVariable(attr),
            token.RParen(),
            token.Space(),
            token.In(),
            token.Space(),
            universal_set,
        ]
        # concealed_value = store.conceal_bound_variable()
        # order += [Set()]
        # store.restore_bound_variable(concealed_value)
        super().__init__(order=order)
        self.__data = self.get(2).data

    def cleanup(self):
        store.remove_bound_variable(self.__data)

    @property
    def properties(self):
        ret = {
            "quantifier": self.get(0).to_json(),
            "variable": self.get(2).to_json(),
            "universal_set": self.get(7).to_json(),
        }
        return ret

    @property
    def data(self) -> BoundVariableData:
        return self.__data


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
    def __init__(self, attr: Attribute | None = None):
        store.enter(Context.STRUCT_ELEMENT, self.__class__.__name__)
        rule = token.BoundVariable(attr)
        self.__attr = rule.attr
        super().__init__(rule=rule)
        store.exit(self.__class__.__name__)

    def cleanup(self):
        store.remove_bound_variable(self.text)

    @property
    def attr(self) -> Attribute:
        return self.__attr


## NOTE: WEIGHTを1以上にすると、再帰エラーが発生する。
class GenerationSet(OrderRule):
    class SetWithoutGerationSet(AlternativeRule):
        def __init__(self, attr: Attribute | None):
            choices = [
                BFunction,
            ]
            if len(store.bound_variables) >= 1:
                choices += [ConnectFunction]
            choice = lottery(choices, self.__class__.__name__)(attr)
            self.__attr = choice.attr
            super().__init__(choice=choice)

        @property
        def attr(self) -> Attribute:
            return self.__attr

    def __init__(self, attr: Attribute | None = None):
        store.enter(Context.GENERATION_SET, self.__class__.__name__)
        universal_set = self.SetWithoutGerationSet(attr)
        self.__attr = universal_set.attr
        order = [
            token.LCurly(),
            token.Space(),
            token.BoundVariable(self.__attr),
            token.Space(),
            token.In(),
            token.Space(),
            universal_set,
            token.Space(),
            token.Pipe(),
            token.Space(),
            CompoundBoolean(),
            token.Space(),
            token.RCurly(),
        ]
        # concealed_value = store.conceal_bound_variable()
        # order.append(self.SetWithoutGerationSet())
        # store.register_bound_variables(concealed_value)
        # order += [
        #     token.Space(),
        #     token.Pipe(),
        #     token.Space(),
        #     CompoundBoolean(),
        #     token.Space(),
        #     token.RCurly(),
        # ]
        super().__init__(order=order)
        if self.get(2).data.appearance_count == 0:
            raise UnableToContinueError(
                "generation setの中で束縛変数が登場しませんでした",
            )
        store.remove_bound_variable(self.get(2).data)

    def to_json(self):
        ret = {
            "type": "set",
            "name": "generation_set",
            "properties": {
                "variable": self.get(2).to_json(),
                "universal_set": self.get(6).to_json(),
                "filter": self.get(10).to_json(),
            },
        }
        return ret

    @property
    def attr(self) -> Attribute:
        return self.__attr


class Boolean(AlternativeRule):
    WEIGHT = 5

    class SubsetComparison(OrderRule):
        def __init__(self):
            left = Set()
            right = Set()
            if left.attr != right.attr:
                UnableToContinueError("left.attr != right.attr")
            order = [
                left,
                token.Space(),
                token.Subset(),
                token.Space(),
                right,
            ]
            super().__init__(order=order)

        def to_json(self):
            ret = {
                "type": "boolean",
                "name": "set_comparison",
                "properties": {
                    "op": self.get(2).to_json(),
                },
                "args": {
                    "left": self.get(0).to_json(),
                    "right": self.get(4).to_json(),
                },
            }
            return ret

    class InComparison(OrderRule):
        def __init__(self):
            right = Set()
            left = StructElement(right.attr)
            order = [
                left,
                token.Space(),
                token.In(),
                token.Space(),
                right,
            ]
            super().__init__(order=order)

        def to_json(self):
            ret = {
                "type": "boolean",
                "name": "set_comparison",
                "properties": {
                    "op": self.get(2).to_json(),
                },
                "args": {
                    "left": self.get(0).to_json(),
                    "right": self.get(4).to_json(),
                },
            }
            return ret

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
                self.__attr = choice.attr
                super().__init__(choice=choice)

            @property
            def attr(self) -> Attribute | None:
                return self.__attr

        def __init__(self):
            left = Set()
            right = self.S_E()
            if right.attr and left.attr != right.attr:
                raise UnableToContinueError("setのattrが適切ではありません。")
            order = [
                Set(),
                token.Space(),
                self.N_E(),
                token.Space(),
                self.S_E(),
            ]
            super().__init__(order=order)

        def to_json(self):
            ret = {
                "type": "boolean",
                "name": "set_equation",
                "properties": {
                    "op": self.get(2).to_json(),
                },
                "args": {
                    "left": self.get(0).to_json(),
                    "right": self.get(4).to_json(),
                },
            }
            return ret

    class PrimitiveValueComparison(OrderRule):
        class N_E(AlternativeRule):
            def __init__(self):
                choices = [
                    token.NotEqual,
                    token.Equal,
                ]
                choice = lottery(choices, self.__class__.__name__)()
                super().__init__(choice=choice)

        def __init__(self):
            order = [
                PrimitiveValue(),
                token.Space(),
                self.N_E(),
                token.Space(),
                PrimitiveValue(),
            ]
            super().__init__(order=order)

        def to_json(self):
            ret = {
                "type": "boolean",
                "name": "primitive_value_comparison",
                "properties": {"op": self.get(2).to_json()},
                "args": {
                    "left": self.get(0).to_json(),
                    "right": self.get(4).to_json(),
                },
            }
            return ret

    class IntValueComparison(OrderRule):
        WEIGHT = 6

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
                Int(),
                token.Space(),
                self.N_E_M_T(),
                token.Space(),
                Int(),
            ]
            super().__init__(order=order)

        def to_json(self):
            ret = {
                "type": "boolean",
                "name": "int_value_comparison",
                "properties": {"op": self.get(2).to_json()},
                "args": {
                    "left": self.get(0).to_json(),
                    "right": self.get(4).to_json(),
                },
            }
            return ret

    def __init__(self):
        choices = [
            self.SubsetComparison,
            self.InComparison,
            # self.IntInInterger, // Not to need
            self.SetEquality,
            # self.PrimitiveValueComparison,
            self.IntValueComparison,
        ]
        # if store.exists_bound_variables():
        #     choices += [AllDifferentFunction, IsSquareFunction, IsRectangleFunction]
        choice = lottery(choices, self.__class__.__name__)()
        super().__init__(choice=choice)

    def to_json(self):
        ret = self.choice.to_json()
        return ret


class SingleBoolean(AlternativeRule):
    PREVENT_NOT_BOOLEAN = False
    WEIGHT = 10

    def __init__(self):
        choices = [
            Boolean,
        ]
        if store.can_choose_quantifier_boolean_counts:
            choices.append(QuantifierBoolean)
        if not self.PREVENT_NOT_BOOLEAN:
            choices.append(NotBoolean)
        choice = lottery(choices, self.__class__.__name__)
        logger.debug(choice.__name__)
        if choice.__name__ == "NotBoolean":
            self.PREVENT_NOT_BOOLEAN = True
        if choice.__name__ == "QuantifierBoolean":
            store.choose_quantifier_boolean()
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

    def to_json(self):
        ret = {
            "type": "boolean",
            "name": "not",
            "args": self.get(2).to_json(),
        }
        return ret


class ParenthesizedBoolean(OrderRule):
    def __init__(self):
        order = [
            token.LBracket(),
            CompoundBoolean(),
            token.RBracket(),
        ]
        super().__init__(order=order)

    def to_json(self):
        ret = self.get(1).to_json()
        return ret


class QuantifierBoolean(OrderRule):
    WEIGHT = 2

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
        if self.get(0).data.appearance_count == 0:
            raise UnableToContinueError(
                "Quantifier Booleanの中で束縛変数が使われませんでした。",
            )
        self.get(0).cleanup()

    def to_json(self):
        ret = {
            "type": "boolean",
            "name": "quantifier",
            "properties": self.get(0).properties,
            "args": self.get(4).to_json(),
        }
        return ret


class CompoundBoolean(OrderRule):
    class MultipleAdditionalBoolean(MultipleRule):
        def __init__(self):
            rule = self.AdditionalBoolean
            range = Range(min=0, max=0)
            order = repeat(rule, range)
            super().__init__(order=order)

        @property
        def size(self):
            return len(self.order)

        def to_json(self):
            ret = {}
            for i, el in reversed(list(enumerate(self.order))):
                if i == len(self.order) - 1:
                    ret = {
                        "type": "boolean",
                        "name": "compound",
                        "properties": {
                            "op": el.op,
                        },
                        "args": {
                            "right": el.boolean,
                        },
                    }
                else:
                    ret["args"]["left"] = el.boolean
                    ret = {
                        "type": "boolean",
                        "name": "compound",
                        "properties": {
                            "op": el.op,
                        },
                        "args": {
                            "right": copy.deepcopy(ret),
                        },
                    }

            return ret

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

            @property
            def op(self):
                return self.get(1).to_json()

            @property
            def boolean(self):
                return self.get(3).to_json()

    def __init__(self):
        order = [
            SingleBoolean(),
            self.MultipleAdditionalBoolean(),
        ]
        super().__init__(order=order)

    def to_json(self):
        if self.get(1).size >= 1:
            ret = self.get(1).to_json()
            ret["args"]["left"] = self.get(0).to_json()
        else:
            ret = self.get(0).to_json()

        return ret


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
        while True:
            store.enter_constraint_definition()
            constraint = Constraint()
            store.exit_constraint_definition()
            if len(store.target_structs) == 0:
                continue
            break
        order = [
            token.Indent(),
            constraint,
            token.Semi(),
            token.Newline(),
        ]
        super().__init__(order=order)
        self.__target_structs = store.target_structs

    def to_json(self):
        ret = {
            "targets": self.__target_structs,
            "constraint": self.get(1).to_json(),
        }
        return ret


class ConstraintsDefinitions(MultipleRule):
    def __init__(self):
        rule = ConstraintDefinition
        range = Range(min=1, max=1)
        order = repeat(rule, range)
        super().__init__(order=order)
