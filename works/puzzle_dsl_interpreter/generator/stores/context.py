from __future__ import annotations

from enum import IntEnum, auto


class Context(IntEnum):
    DEFAULT = auto()
    STRUCT_DEFINITION = auto()
    STRUCT_DEFINITION_BODY = auto()
    RELATIONSHIP_SET_BODY = auto()
    CUSTOM_STRUCT_DEFINITION = auto()
    DOMAIN_SET_BODY = auto()
    DOMAIN_DEFINITIONS = auto()
    B_FUNCTION = auto()


class ContextStore:
    def __init__(self):
        self.__context = Context.DEFAULT
        self.__save: list[Context] = []

    @property
    def context(self):
        return self.__context

    def switch(self, context: Context):
        self.__save.append(self.__context)
        self.__context = context

    def switch_back(self):
        if len(self.__save) > 0:
            self.__context = self.__save.pop(-1)
        else:
            self.__context = Context.DEFAULT


ctx_store = ContextStore()
