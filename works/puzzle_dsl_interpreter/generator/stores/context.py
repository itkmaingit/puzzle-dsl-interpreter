from __future__ import annotations

from enum import IntEnum, auto

from generator.definitions.errors import ForbiddenOperationError, NotMatchContextError
from generator.utils.logger import logger


class Context(IntEnum):
    DEFAULT = auto()
    STRUCT_DEFINITION = auto()
    STRUCT_DEFINITION_BODY = auto()
    RELATIONSHIP_SET_BODY = auto()
    DOMAIN_SET_BODY = auto()
    DOMAIN_DEFINITIONS = auto()
    B_FUNCTION = auto()
    STRUCT_ELEMENT = auto()
    BOARD_FUNCTION = auto()
    QUANTIFIER_BOOLEAN = auto()
    GENERATION_SET = auto()
    QUANTIFIER_INDEX = auto()
    INDEX_FUNCTION = auto()


class ContextStore:
    def __init__(self):
        self.__contexts: list[Context] = [Context.DEFAULT]

    @property
    def context(self):
        return self.__contexts[-1]

    @property
    def contexts(self):
        return self.__contexts

    def switch(self, context: Context, cls_name: str):
        self.__contexts.append(context)
        self.__compare_ctx_and_cls(self.context.name, cls_name)
        logger.info(
            f"[bright_green]ENTER[/bright_green]: {self.__contexts[-2].name} -> [bright_cyan]{self.__contexts[-1].name}[/bright_cyan] (called by {cls_name})",
        )

    def switch_back(self, cls_name: str):
        if len(self.contexts) > 1:
            pre_ctx = self.__contexts.pop(-1)
            self.__compare_ctx_and_cls(pre_ctx.name, cls_name)
            logger.info(
                f"[bright_red]EXIT[/bright_red]: {pre_ctx.name} -> [bright_cyan]{self.context.name}[/bright_cyan] (called by {cls_name})",
            )
        else:
            raise ForbiddenOperationError(
                f"存在しないContextから抜けようとしています。(now context is {self.context.name})",
            )

    def __compare_ctx_and_cls(self, cmp: str, cls_name: str) -> bool:
        if cmp.lower().replace("_", "") != cls_name.lower().replace("_", ""):
            logger.error(f"Context: {cmp}, Class: {cls_name}")
            raise NotMatchContextError("Contextとクラス名が一致していません。")


ctx_store = ContextStore()
