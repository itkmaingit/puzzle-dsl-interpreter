from __future__ import annotations

from generator.checker.dataclass import Attribute

# P = Token(type=TokenType.P)
# C = Token(type=TokenType.C)
# Ep = Token(type=TokenType.EP)
# Ec = Token(type=TokenType.EC)


class BoundVariableData:
    def __init__(self, text: str, attr: Attribute):
        self.__text = text
        self.__attr = attr
        self.__appearance_count = 0

    def appearance(self):
        self.__appearance_count += 1

    @property
    def text(self) -> str:
        return self.__text

    @property
    def attr(self) -> Attribute:
        return self.__attr

    @property
    def appearance_count(self) -> int:
        return self.__appearance_count

    def __str__(self) -> str:
        return f"(text: {self.__text}, attr: {self.__attr}, counts: {self.__appearance_count})"

    def __repr__(self) -> str:
        return self.__str__()
