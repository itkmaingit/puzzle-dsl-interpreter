from __future__ import annotations

from generator.definitions.rules import (
    AlternativeRule,
)
from generator.helpers import token


class W_H(AlternativeRule):
    def __init__(self):
        choices = {token.Width(), token.Height()}
        super().__init__(choices)


class P_M_T(AlternativeRule):
    def __init__(self):
        choices = {token.Plus(), token.Minus(), token.Times()}
        super().__init__(choices)
