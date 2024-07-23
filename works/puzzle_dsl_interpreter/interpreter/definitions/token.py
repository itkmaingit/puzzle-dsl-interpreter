from __future__ import annotations

from enum import Flag, auto

from pydantic import BaseModel


class TokenAttribute(Flag):
    ELEMENT = auto()
    STRUCT = auto()
    NULL = auto()
    CONSTANTS = auto()


class Token(BaseModel):
    attr: TokenAttribute
    text: str

    def __eq__(self, other: Token):
        return self.attr == other.attr and self.text == other.text

    def __hash__(self):
        return hash((self.attr, self.text))
