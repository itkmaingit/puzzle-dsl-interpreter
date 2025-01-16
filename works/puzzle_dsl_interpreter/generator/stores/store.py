from __future__ import annotations

from copy import deepcopy

from generator.checker.dataclass import Attribute
from generator.definitions.constants import BoundVariableData
from generator.stores.context import Context, ContextStore
from generator.stores.variables import VariableStore
from generator.utils.logger import logger


class StateStore:
    def __init__(self):
        self.initialize()

    @property
    def context(self) -> Context:
        return self.__ctx_store.context

    @property
    def contexts(self) -> Context:
        return self.__ctx_store.contexts

    @property
    def defined_structs(self) -> list[str]:
        return self.__defined_struct_store.var

    @property
    def new_structs(self) -> list[str]:
        return self.__new_struct_store.var

    @property
    def relationship(self) -> list[str]:
        return self.__relationship_store.var

    @property
    def constants(self) -> list[str]:
        return self.__constants_store.var

    @property
    def count_new_structs(self) -> int:
        return len(self.new_structs)

    @property
    def bound_variables(self) -> list[BoundVariableData]:
        return self.__bound_variables_store.var

    # @property
    # def ng_bound_variables(self) -> list[str]:
    #     return (
    #         self.__bound_variables_store.var
    #         # + self.__tmp_banned_bound_variables_store.var
    #     )

    @property
    def target_structs(self) -> list[str]:
        return list(set(self.__target_structs_store.var))

    @property
    def can_choose_quantifier_boolean_counts(self) -> int:
        return self.__choose_quantifier_boolean_counts < 4

    def exists_bound_variables(self) -> bool:
        return len(self.bound_variables) >= 1

    def exists_specific_attr_bound_variables(self, attr: Attribute) -> bool:
        filtered_list = [elem for elem in store.bound_variables if elem.attr == attr]
        return len(filtered_list) >= 1

    def register_struct(self, struct_id: str):
        self.__defined_struct_store.add(struct_id)
        self.__new_struct_store.add(struct_id)

    def register_relationship(self, relationship_id: str):
        self.__relationship_store.add(relationship_id)

    def register_constants(self, constants_id: str):
        self.__constants_store.add(constants_id)

    def register_bound_variables(self, bound_variables_id: str | BoundVariableData):
        self.__bound_variables_store.add(bound_variables_id)

    def remove_struct(self, struct_id: str):
        self.__new_struct_store.remove(struct_id)

    def enter(self, context: Context, cls_name: str):
        self.__ctx_store.switch(context, cls_name)

    def exit(self, cls_name: str):
        self.__ctx_store.switch_back(cls_name)

    def enter_relationship_set_body(self):
        self.enter(Context.RELATIONSHIP_SET_BODY, "RelationshipSetBody")
        self.__relationship_store.reset()

    def exit__relationship_set_body(self):
        self.__relationship_store.reset()
        self.exit("RelationshipSetBody")

    def enter_domain_definitions(self):
        self.enter(Context.DOMAIN_DEFINITIONS, "DomainDefinitions")
        cands = deepcopy(self.new_structs)
        self.__new_struct_store.stash()
        self.__new_struct_store.add_all(cands)

    def exit_domain_difinitions(self):
        self.__new_struct_store.load()
        self.exit("DomainDefinitions")

    def enter_board_function(self):
        self.enter(Context.BOARD_FUNCTION, "BoardFunction")
        cands = deepcopy(self.new_structs)
        logger.debug(f"cands: {cands}")
        self.__new_struct_store.stash()
        self.__new_struct_store.add_all(cands)

    def exit_board_function(self):
        self.__new_struct_store.load()
        self.exit("BoardFunction")

    def exit_with_cleanup(self, cls_name: str):
        self.__bound_variables_store.pop()
        self.exit(cls_name)

    def enter_constraint_definition(self):
        self.__target_structs_store.reset()

    def exit_constraint_definition(self):
        self.__bound_variables_store.reset()

    # def conceal_bound_variable(self) -> str:
    #     concealed_value = self.__bound_variables_store.pop()
    #     self.__tmp_banned_bound_variables_store.add(concealed_value)
    #     return concealed_value

    # def restore_bound_variable(self, concealed_value: str):
    #     self.__tmp_banned_bound_variables_store.remove(concealed_value)
    #     self.__bound_variables_store.add(concealed_value)

    def register_target_structs(self, target: str | list[str]):
        if isinstance(target, list):
            self.__target_structs_store.add_all(target)
        else:
            self.__target_structs_store.add(target)

    def remove_bound_variable(self, bound_variable: BoundVariableData):
        self.__bound_variables_store.remove(bound_variable)

    def choose_quantifier_boolean(self):
        self.__choose_quantifier_boolean_counts += 1

    def gen_bound_variable_name(self) -> str:
        self.__bound_variable_counter += 1
        return f"b{self.__bound_variable_counter}"

    def initialize(self):
        self.__defined_struct_store = VariableStore(
            is_deletable=False,
        )  # Forbidden to delete element
        self.__constants_store = VariableStore(
            is_deletable=False,
        )  # Forbidden to delete element

        self.__new_struct_store = VariableStore(is_deletable=True)
        self.__relationship_store = VariableStore(is_deletable=True)
        self.__bound_variables_store = VariableStore(is_deletable=True)
        # self.__tmp_banned_bound_variables_store = VariableStore(is_deletable=True)
        self.__target_structs_store = VariableStore(
            is_deletable=True,
            is_duplicatable=True,
        )

        self.__ctx_store = ContextStore()

        self.__defined_struct_store.add_all(["P", "C", "Ep", "Ec"])

        self.__choose_quantifier_boolean_counts = 0
        self.__bound_variable_counter = 0

    # --------------------for debug------------------------
    def exit_struct_definitions(self):
        logger.debug(store.new_structs)


store = StateStore()
