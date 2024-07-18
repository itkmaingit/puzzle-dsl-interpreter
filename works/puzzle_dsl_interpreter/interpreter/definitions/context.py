from __future__ import annotations

from enum import Flag, auto


class Context(Flag):
    STRUCTS_DECLARATION = auto()
    DOMAIN_DECLARATION = auto()
    CONSTRAINTS_DECLARATION = auto()
