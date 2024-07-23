from __future__ import annotations

from enum import Flag, auto


class Context(Flag):
    INITIAL = auto()
    STRUCTS_DECLARATION = auto()
    DOMAIN_HIDDEN_DECLARATION = auto()
    CONSTRAINTS_DECLARATION = auto()
