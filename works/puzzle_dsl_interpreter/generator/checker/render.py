from __future__ import annotations

from generator.checker.errors import PanicError


def compound_boolean(name: str, left: str, right: str, op: str):
    if op == "||":
        return f"{name} = or_bool({left}, {right})"
    if op == "&&":
        return f"{name} = and_bool({left}, {right})"
    if op == "=>":
        return f"{name} = then_bool({left}, {right})"
    if op == "<=>":
        return f"{name} = equivalent_bool({left}, {right})"
    raise PanicError
