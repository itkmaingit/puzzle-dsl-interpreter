from __future__ import annotations

from copy import deepcopy

from generator.stores.context import Context, ContextStore
from generator.stores.variables import VariableStore


class StateStore:
    def __init__(self):
        self.__defined_struct_store = VariableStore()
        self.__relationship_store = VariableStore()
        self.__index_store = VariableStore()
        self.__quantifier_store = VariableStore()
        self.__set_store = VariableStore()
        self.__constants_store = VariableStore()

        self.__ctx_store = ContextStore()

        self.__defined_struct_store.add_all(["P", "C", "Ep", "Ec"])

    @property
    def context(self) -> Context:
        return self.__ctx_store.context

    @property
    def defined_structs(self) -> list[str]:
        return self.__defined_struct_store.var

    @property
    def relationship(self) -> list[str]:
        return self.__relationship_store.var

    @property
    def count_defined_structs(self) -> int:
        return len(self.defined_structs) - 4

    def register_struct(self, struct_id: str):
        self.__defined_struct_store.add(struct_id)

    def register_relationship(self, relationship_id: str):
        self.__relationship_store.add(relationship_id)

    def register_constants(self, constants_id: str):
        self.__constants_store.add(constants_id)

    def remove_struct(self, struct_id: str):
        self.__defined_struct_store.remove(struct_id)

    def enter(self, context: Context):
        self.__ctx_store.switch(context)

    def exit(self):
        self.__ctx_store.switch_back()

    def enter_relationship_set_body(self):
        self.__relationship_store.reset()
        self.enter(Context.RELATIONSHIP_SET_BODY)

    def exit__relationship_set_body(self):
        self.__relationship_store.reset()
        self.exit()

    def enter_domain_definitions(self):
        cands = deepcopy(self.__defined_struct_store.var[4:])
        self.__defined_struct_store.stash()
        self.__defined_struct_store.add_all(cands)

    def exit_domain_difinitions(self):
        self.__defined_struct_store.load()
        self.exit()


store = StateStore()
