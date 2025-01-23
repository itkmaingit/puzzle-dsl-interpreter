from __future__ import annotations

from generator.checker.dataclass import Element


def same_attr(elements: set[Element]) -> bool:
    attr = None
    for elem in elements:
        if attr is None:
            attr = elem.attr
        elif attr and attr != elem.attr:
            return False
    return True
