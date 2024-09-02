from __future__ import annotations

from copy import deepcopy
from typing import NoReturn


class VariableStore:
    def __init__(self) -> NoReturn:
        self.var: list[str] = []
        self.__var_save: list[str] = []

    def reset(self):
        self.var = []
        self.__var_save = []

    def add(self, text: str):
        if text in self.var:
            self.var.append(text)
        else:
            print(f"重複があるようです。{text}")

    def add_all(self, lst: list[str]):
        self.var += lst

    def pop(self):
        return self.var.pop(-1)

    def remove(self, text: str):
        if text in self.var:
            self.var.remove(text)
        else:
            raise ValueError(f"値 {text} はストアに含まれていません。")

    def exists(self):
        return len(self.var) > 0

    def stash(self):
        if len(self.__var_save) > 0:
            print(self.__var_save)
        self.__var_save = deepcopy(self.var)
        self.var = []

    def load(self):
        if len(self.var) > 0:
            print(self.var)
        self.var = deepcopy(self.__var_save)
        self.__var_save = []
