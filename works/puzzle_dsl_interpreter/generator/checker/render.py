from __future__ import annotations

from generator.checker.errors import PanicError


def compound_boolean(name: str, left: str, right: str, op: str) -> str:
    if op == "||":
        return f"{name} = or_bool({left}, {right})"
    if op == "&&":
        return f"{name} = and_bool({left}, {right})"
    if op == "=>":
        return f"{name} = then_bool({left}, {right})"
    if op == "<=>":
        return f"{name} = equivalent_bool({left}, {right})"
    raise PanicError(op)


def quantifier_boolean(name: str, set_name: str, func_name: str, type: str) -> str:
    if type == "All":
        return f"{name} = is_all({set_name}, {func_name})"
    if type == "Exists":
        return f"{name} = is_exists({set_name}, {func_name})"
    raise PanicError(type)


def set_comparison(name: str, left: str, right: str, op: str):
    if op == "<-":
        return f"{name} = is_in({left}, {right})"
    if op == "<=":
        return f"{name} = is_subset({left}, {right})"
    raise PanicError(op)


def set_equation(name: str, left: str, right: str, op: str):
    if op in ["==", "!="]:
        return f"{name} = {left} {op} {right}"
    raise PanicError(op)


def int_convert(val: str):
    if val.isdigit():
        return val
    if val == "n":
        return "HEIGHT"
    if val == "m":
        return "WIDTH"
    raise PanicError(val)
