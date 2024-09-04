from __future__ import annotations

from copy import deepcopy
from typing import NoReturn

from generator.definitions.errors import DuplicationVariableError, NotDeletableError
from generator.utils.logger import logger


class VariableStore:
    def __init__(self, is_deletable: bool) -> NoReturn:
        self.var: list[str] = []
        self.__var_save: list[str] = []
        self.__is_deletable = is_deletable

    def __check_deletable(self):
        if not self.__is_deletable:
            raise NotDeletableError("要素の削除は禁止されています!")

    def reset(self):
        self.__check_deletable()
        self.var = []
        self.__var_save = []

    def add(self, text: str):
        if text not in self.var:
            self.var.append(text)
        else:
            raise DuplicationVariableError(f"重複があるようです。{text}")

    def add_all(self, lst: list[str]):
        self.var += lst

    def pop(self):
        self.__check_deletable()
        return self.var.pop(-1)

    def remove(self, text: str):
        self.__check_deletable()
        if text in self.var:
            self.var.remove(text)
        else:
            logger.error(f"text: {text}, store: {self.var}")
            raise ValueError(f"値 {text} はストアに含まれていません。")

    def exists(self):
        return len(self.var) > 0

    def stash(self):
        self.__check_deletable()
        if len(self.__var_save) > 0:
            print("stash: ", self.__var_save)
        self.__var_save = deepcopy(self.var)
        self.var = []

    def load(self):
        if len(self.var) > 0:
            print("load", self.var)
        self.var = deepcopy(self.__var_save)
        self.__var_save = []
