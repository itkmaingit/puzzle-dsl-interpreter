from __future__ import annotations

import random
from enum import StrEnum
from functools import lru_cache

from generator.checker.errors import InvalidError


class Attribute(StrEnum):
    P = "P"
    C = "C"
    Hp = "Hp"
    Vp = "Vp"
    Ep = "Ep"
    Hc = "Hc"
    Vc = "Vc"
    Ec = "Ec"


class Relationship(StrEnum):
    H = "H"
    V = "V"
    D = "D"


point_candidates = [0, 1, 2, 3]
edge_candidates = [0, 1]


HEIGHT = 4
WIDTH = 4


class Element:
    def __init__(self, attr: Attribute, i: int, j: int, value: int = 0):
        if attr in {Attribute.Ep, Attribute.Ec}:
            raise InvalidError("element's attr should not ep or ec.")
        self.value = value
        self.attr = attr
        self.i = i
        self.j = j

    def __eq__(self, other):
        if other is None or isinstance(type(self), type(other)):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.attr, self.i, self.j))

    def __str__(self):
        return f"value: {self.value}, attr: {self.attr}, (i, j): ({self.i}, {self.j})"

    def __repr__(self):
        return self.__str__()


class ElementList:
    def __init__(self, height: int, width: int, attr: str):
        self.elements = [
            [Element(attr, i, j) for j in range(width)] for i in range(height)
        ]

    @lru_cache
    def flatten(self) -> set[Element]:
        return {elem for row in self.elements for elem in row}

    def change_value(self, i: int, j: int, val: int):
        """for debug"""
        self.elements[i][j].value = val

    def shuffle(self, candidates: list[int]):
        for row in self.elements:
            for col in row:
                col.value = random.choice(candidates)


class Board:
    def __init__(
        self,
        c_list: ElementList,
        p_list: ElementList,
        hc_list: ElementList,
        vc_list: ElementList,
        hp_list: ElementList,
        vp_list: ElementList,
    ):
        self.c_list = c_list
        self.p_list = p_list
        self.hc_list = hc_list
        self.vc_list = vc_list
        self.hp_list = hp_list
        self.vp_list = vp_list
        self.elements_map = self._register_elements()

    def _register_elements(self) -> dict:
        elements_map = {}
        for elist in [
            (Attribute.C, self.c_list),
            (Attribute.P, self.p_list),
            (Attribute.Hc, self.hc_list),
            (Attribute.Vc, self.vc_list),
            (Attribute.Hp, self.hp_list),
            (Attribute.Vp, self.vp_list),
        ]:
            attr, grid = elist
            for i, row in enumerate(grid.elements):
                for j, elem in enumerate(row):
                    key = (attr, i, j)
                    elements_map[key] = elem
        return elements_map

    @lru_cache
    def get_element(self, attr: Attribute, i: int, j: int) -> Element | None:
        return self.elements_map.get((attr, i, j))

    @lru_cache
    def b(self, attr: Attribute) -> set[Element]:
        match attr:
            case Attribute.C:
                return self.c_list.flatten()
            case Attribute.P:
                return self.p_list.flatten()
            case Attribute.Ec:
                return self.hc_list.flatten() | self.vc_list.flatten()
            case Attribute.Ep:
                return self.hp_list.flatten() | self.vp_list.flatten()
            case Attribute.Hc:
                return self.hc_list.flatten()
            case Attribute.Vc:
                return self.vc_list.flatten()
            case Attribute.Hp:
                return self.hp_list.flatten()
            case Attribute.Vp:
                return self.vp_list.flatten()
            case _:
                raise InvalidError("Invalid attribute.")

    def shuffle(self, attrs: set[str]):
        for attr in attrs:
            match attr:
                case Attribute.C:
                    self.c_list.shuffle(point_candidates)
                case Attribute.P:
                    self.p_list.shuffle(point_candidates)
                case Attribute.Ec:
                    self.hc_list.shuffle(edge_candidates)
                    self.vc_list.shuffle(edge_candidates)
                case Attribute.Ep:
                    self.hp_list.shuffle(edge_candidates)
                    self.vp_list.shuffle(edge_candidates)


def is_horizontal(e1: Element, e2: Element) -> bool:
    """Check if two elements are horizontally adjacent."""
    if e1.i == e2.i and abs(e1.j - e2.j) == 1:
        return (
            e1.attr == e2.attr
            and e1.attr in {Attribute.P, Attribute.C, Attribute.Hp, Attribute.Hc}
        ) or (
            (e1.attr, e2.attr)
            in {
                (Attribute.P, Attribute.Hp),
                (Attribute.Hp, Attribute.P),
                (Attribute.C, Attribute.Hc),
                (Attribute.Hc, Attribute.C),
            }
        )
    return False


def is_vertical(e1: Element, e2: Element) -> bool:
    """Check if two elements are vertically adjacent."""
    if e1.j == e2.j and abs(e1.i - e2.i) == 1:
        return (
            e1.attr == e2.attr
            and e1.attr in {Attribute.P, Attribute.C, Attribute.Vp, Attribute.Vc}
        ) or (
            (e1.attr, e2.attr)
            in {
                (Attribute.P, Attribute.Vp),
                (Attribute.Vp, Attribute.P),
                (Attribute.C, Attribute.Vc),
                (Attribute.Vc, Attribute.C),
            }
        )
    return False


def is_diagonal(e1: Element, e2: Element) -> bool:
    """Check if two elements are diagonally adjacent."""
    diff_i = e1.i - e2.i
    diff_j = e1.j - e2.j
    if e1.attr == e2.attr and e1.attr in {Attribute.P, Attribute.C}:
        return abs(diff_i) == 1 and abs(diff_j) == 1
    if (e1.attr, e2.attr) in {
        (Attribute.Hp, Attribute.Vp),
        (Attribute.Hc, Attribute.Vc),
    }:
        return diff_i in {0, 1} and diff_j in {0, -1}
    if (e1.attr, e2.attr) in {
        (Attribute.Vp, Attribute.Hp),
        (Attribute.Vc, Attribute.Hc),
    }:
        return diff_i in {0, -1} and diff_j in {0, 1}
    return False


def is_related(e1: Element, e2: Element, rel: str) -> bool:
    if rel == Relationship.H:
        return is_horizontal(e1, e2)
    if rel == Relationship.V:
        return is_vertical(e1, e2)
    if rel == Relationship.D:
        return is_diagonal(e1, e2)
    return False


def main():
    random.seed(42)

    # c_list = ElementList(HEIGHT, WIDTH, [0, 1, 2, 3, 4], Attribute.C)
    # p_list = ElementList(HEIGHT + 1, WIDTH + 1, [0, 1, 2, 3, 4], Attribute.P)
    # hc_list = ElementList(HEIGHT, WIDTH - 1, [0, 1], Attribute.Hc)
    # vc_list = ElementList(HEIGHT - 1, WIDTH, [0, 1], Attribute.Vc)
    # hp_list = ElementList(HEIGHT + 1, WIDTH, [0, 1], Attribute.Hp)
    # vp_list = ElementList(HEIGHT, WIDTH + 1, [0, 1], Attribute.Vp)

    # board = Board(c_list, p_list, hc_list, vc_list, hp_list, vp_list)

    # results = cycle(board)
    # for coord, total in results.items():
    #     print(f"Cycle at P{coord} = {total}")


if __name__ == "__main__":
    main()
