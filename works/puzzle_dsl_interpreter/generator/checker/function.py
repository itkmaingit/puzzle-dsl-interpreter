from __future__ import annotations

from collections.abc import Callable
from typing import Any

from generator.checker.dataclass import (
    Attribute,
    Board,
    Element,
    Relationship,
    is_related,
)
from generator.checker.errors import PanicError
from generator.checker.helper import same_attr


def is_subset(A: set[Any], B: set[Any]) -> bool:
    if not isinstance(A, set):
        raise PanicError(f"{A} is not set")
    if not isinstance(B, set):
        raise PanicError(f"{B} is not set")
    return all(a in B for a in A)


def is_in(A: Any, B: set[Any]) -> bool:
    if not isinstance(B, set):
        raise PanicError(f"{B} is not set")
    return A in B


def compare_set(A: set[Any], B: set[Any]) -> bool:
    return A == B


def connect(e: Element, relationships: set[Relationship], board: Board) -> set[Element]:
    neighbors = set()
    elements: set
    if e.attr in {Attribute.C, Attribute.P}:
        elements = board.b(e.attr)
    elif e.attr in {Attribute.Hp, Attribute.Vp}:
        elements = board.b(Attribute.Ep)
    elif e.attr in {Attribute.Hc, Attribute.Vc}:
        elements = board.b(Attribute.Ec)
    else:
        raise PanicError("given element's attr is not be allowed.")

    for other in elements:
        if e != other:
            if any(is_related(e, other, rel) for rel in relationships):
                neighbors.add(other)
    return neighbors


def cross(e: Element, board: Board) -> int:
    if e.attr != Attribute.P:
        raise PanicError(f"Element at {e} is not P")

    i, j = e.i, e.j
    sum_values = 0

    hp1 = board.get_element(Attribute.Hp, i, j - 1)
    hp2 = board.get_element(Attribute.Hp, i, j)
    vp1 = board.get_element(Attribute.Vp, i - 1, j)
    vp2 = board.get_element(Attribute.Vp, i, j)

    for elem in [hp1, hp2, vp1, vp2]:
        if elem:
            sum_values += elem.value

    return sum_values


def cycle(e: Element, board: Board) -> int:
    if e.attr != Attribute.C:
        raise PanicError(f"Element {e} is not C")

    i, j = e.i, e.j
    sum_values = 0

    hp1 = board.get_element(Attribute.Hp, i, j)
    hp2 = board.get_element(Attribute.Hp, i + 1, j)
    vp1 = board.get_element(Attribute.Vp, i, j)
    vp2 = board.get_element(Attribute.Vp, i, j + 1)

    for elem in [hp1, hp2, vp1, vp2]:
        if elem:
            sum_values += elem.value

    return sum_values


def is_rectangle(elements: set[Element]) -> bool:
    """Check if the elements form a rectangle on a grid with all interior points filled."""
    if not isinstance(elements, set):
        raise PanicError(f"{elements} is not set")
    if not elements:
        return True

    if not same_attr(elements):
        return False

    # 任意のelementsの要素のAttrがC or PでないならFalse
    if next(iter(elements)).attr not in {Attribute.C, Attribute.P}:
        return False

    # Extract all x (i) and y (j) coordinates
    j_coords = {elem.j for elem in elements}
    i_coords = {elem.i for elem in elements}

    # Determine the bounding box of the rectangle
    min_i, max_i = min(i_coords), max(i_coords)
    min_j, max_j = min(j_coords), max(j_coords)

    if len(elements) != (max_i - min_i + 1) * (max_j - min_j + 1):
        return False
    # Check that every point within the bounding box is covered
    for e in elements:
        if e.i < min_i or max_i < e.i or e.j < min_j or max_j < e.j:
            return False

    # If all checks pass, the elements form a rectangle
    return True


def is_square(elements: set[Element]) -> bool:
    if not isinstance(elements, set):
        raise PanicError(f"{elements} is not set")
    j_coords = {elem.j for elem in elements}
    i_coords = {elem.i for elem in elements}

    min_i, max_i = min(i_coords), max(i_coords)
    min_j, max_j = min(j_coords), max(j_coords)
    if max_i - min_i != max_j - min_j:
        return False

    return is_rectangle(elements)


def all_different(elements: set[Element]) -> bool:
    """Check if all values in the set of Elements are unique."""
    if not isinstance(elements, set):
        raise PanicError(f"{elements} is not set")
    seen_values = set()
    if not same_attr(elements):
        return False
    for elem in elements:
        if elem.value in seen_values:
            return False
        seen_values.add(elem.value)
    return True


def solution(element: Element) -> int:
    return element.value


def generation_set(
    elements: set[Element],
    filter: Callable[[Element], bool],
) -> set[Element]:
    """generation setが来たら、defで関数を作成し、それをgeneration_setに入力値に用いる"""
    if not isinstance(elements, set):
        raise PanicError(f"{elements} is not set")
    return {e for e in elements if filter(e)}


def is_exists(elements: set[Element], filter: Callable[[Element], bool]) -> bool:
    """Check if any element in the set satisfies the filter."""
    if not isinstance(elements, set):
        raise PanicError(f"{elements} is not set")
    return any(filter(e) for e in elements)


def is_all(elements: set[Element], filter: Callable[[Element], bool]) -> bool:
    """Check if all elements in the set satisfy the filter."""
    if not isinstance(elements, set):
        raise PanicError(f"{elements} is not set")
    return all(filter(e) for e in elements)


def not_bool(P: bool):
    return not P


def and_bool(P: bool, Q: bool):
    if P is True and Q is True:
        return True
    return False


def or_bool(P: bool, Q: bool):
    if P is False and Q is False:
        return False
    return True


def then_bool(P: bool, Q: bool):
    if P is True and Q is False:
        return False
    return True


def equivalent_bool(P: bool, Q: bool):
    return P == Q


def int_value_comparison(op: str, left: int, right: int) -> bool:
    match op:
        case "!=":
            return left != right
        case "==":
            return left == right
        case "<":
            return left < right
        case ">":
            return left < right

        case _:
            raise PanicError("Unsupported int comparison operator.")


def int_operation(op: str, left: int, right: int) -> int:
    match op:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case _:
            raise PanicError("Unsupported int operator.")


def absolute_set(elements: set[Element]) -> int:
    if not isinstance(elements, set):
        raise PanicError(f"{elements} is not set")
    return len(elements)
