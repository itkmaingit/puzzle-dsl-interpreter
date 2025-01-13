from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from generator.checker.dataclass import (
    Attribute,
    Board,
    Element,
    ElementList,
    Relationship,
)
from generator.checker.function import (
    all_different,
    compare_set,
    connect,
    cross,
    cycle,
    generation_set,
    is_all,
    is_exists,
    is_in,
    is_rectangle,
    is_square,
    is_subset,
)

HEIGHT, WIDTH = 3, 3


@pytest.fixture
def board():
    c_list = ElementList(HEIGHT, WIDTH, Attribute.C)
    p_list = ElementList(HEIGHT + 1, WIDTH + 1, Attribute.P)
    hc_list = ElementList(HEIGHT, WIDTH - 1, Attribute.Hc)
    vc_list = ElementList(HEIGHT - 1, WIDTH, Attribute.Vc)
    hp_list = ElementList(HEIGHT + 1, WIDTH, Attribute.Hp)
    vp_list = ElementList(HEIGHT, WIDTH + 1, Attribute.Vp)

    board = Board(c_list, p_list, hc_list, vc_list, hp_list, vp_list)
    return board


def test_set_operations():
    elem1 = Element(Attribute.P, 0, 0)
    elem2 = Element(Attribute.P, 0, 1)
    elem3 = Element(Attribute.C, 1, 1)
    set_a = {elem1, elem2}
    set_b = {elem1, elem2, elem3}

    # Test is_subset
    assert is_subset(set_a, set_b) is True
    assert is_subset(set_b, set_a) is False

    # Test is_in
    assert is_in(elem1, set_b) is True
    assert is_in(Element(Attribute.Hp, 0, 0), set_b) is False

    # Test compare_set
    assert compare_set(set_a, {elem1, elem2}) is True
    assert compare_set(set_a, set_b) is False


def test_connect():
    board = MagicMock()
    board.b.side_effect = lambda attr: {
        Attribute.P: {
            Element(Attribute.P, 0, 1),
            Element(Attribute.P, 1, 1),
            Element(Attribute.P, 1, 0),
        },
        Attribute.Ep: {
            Element(Attribute.Hp, 0, 0),
            Element(Attribute.Hp, 0, 1),
            Element(Attribute.Hp, 1, 0),
            Element(Attribute.Hp, 1, 1),
            Element(Attribute.Hp, 2, 0),
            Element(Attribute.Hp, 2, 1),
            Element(Attribute.Vp, 0, 0),
            Element(Attribute.Vp, 0, 1),
            Element(Attribute.Vp, 0, 2),
            Element(Attribute.Vp, 1, 0),
            Element(Attribute.Vp, 1, 1),
            Element(Attribute.Vp, 1, 2),
        },
        Attribute.Ec: {
            Element(Attribute.Hc, 0, 0),
            Element(Attribute.Hc, 0, 1),
            Element(Attribute.Hc, 1, 0),
            Element(Attribute.Hc, 1, 1),
            Element(Attribute.Hc, 2, 0),
            Element(Attribute.Hc, 2, 1),
            Element(Attribute.Vc, 0, 0),
            Element(Attribute.Vc, 0, 1),
            Element(Attribute.Vc, 0, 2),
            Element(Attribute.Vc, 1, 0),
            Element(Attribute.Vc, 1, 1),
            Element(Attribute.Vc, 1, 2),
        },
    }.get(attr, set())

    # Test for Point element
    e = Element(Attribute.P, 0, 0)
    relationships = {Relationship.H, Relationship.V}
    neighbors = connect(e, relationships, board)
    expected_neighbors = {
        Element(Attribute.P, 0, 1),
        Element(Attribute.P, 1, 0),
    }
    assert neighbors == expected_neighbors

    # Test for Edge element (Hp)
    e = Element(Attribute.Hp, 0, 0)
    relationships = {Relationship.H, Relationship.V}
    neighbors = connect(e, relationships, board)
    expected_neighbors = {
        Element(Attribute.Hp, 0, 1),
    }
    assert neighbors == expected_neighbors

    # Test for Edge element (Hc)
    e = Element(Attribute.Hc, 0, 0)
    relationships = {Relationship.H, Relationship.V}
    neighbors = connect(e, relationships, board)
    expected_neighbors = {
        Element(Attribute.Hc, 0, 1),
    }
    assert neighbors == expected_neighbors

    # Test for Edge element (Hp) diagonal
    e = Element(Attribute.Hc, 1, 0)
    relationships = {Relationship.D}
    neighbors = connect(e, relationships, board)
    expected_neighbors = {
        Element(Attribute.Vc, 0, 0),
        Element(Attribute.Vc, 0, 1),
        Element(Attribute.Vc, 1, 0),
        Element(Attribute.Vc, 1, 1),
    }

    assert neighbors == expected_neighbors


def test_cross_and_cycle(board: Board):
    # arrange
    board.hp_list.change_value(0, 2, 1)
    board.hp_list.change_value(1, 0, 1)
    board.hp_list.change_value(1, 1, 1)
    board.hp_list.change_value(2, 0, 1)
    board.hp_list.change_value(3, 1, 1)
    board.vp_list.change_value(0, 1, 1)
    board.vp_list.change_value(0, 3, 1)
    board.vp_list.change_value(1, 2, 1)
    board.vp_list.change_value(2, 1, 1)
    board.vp_list.change_value(2, 3, 1)
    p00 = board.get_element(Attribute.P, 0, 0)
    p11 = board.get_element(Attribute.P, 1, 1)
    p21 = board.get_element(Attribute.P, 2, 1)
    c00 = board.get_element(Attribute.C, 0, 0)
    c10 = board.get_element(Attribute.C, 1, 0)
    c22 = board.get_element(Attribute.C, 2, 2)

    # act & assert
    assert cross(p00, board) == 0
    assert cross(p11, board) == 3
    assert cross(p21, board) == 2

    assert cycle(c00, board) == 2
    assert cycle(c10, board) == 2
    assert cycle(c22, board) == 1


def test_all_different(board: Board):
    # arrange
    board.c_list.change_value(0, 2, 1)
    board.c_list.change_value(1, 0, 2)
    board.c_list.change_value(1, 1, 3)
    board.c_list.change_value(2, 0, 4)

    c00_0 = board.get_element(Attribute.C, 0, 0)
    c01_0 = board.get_element(Attribute.C, 0, 1)
    c02_1 = board.get_element(Attribute.C, 0, 2)
    c10_2 = board.get_element(Attribute.C, 1, 0)
    c11_3 = board.get_element(Attribute.C, 1, 1)
    c20_4 = board.get_element(Attribute.C, 2, 0)

    true_sut = {c00_0, c02_1, c10_2, c11_3, c20_4}
    false_sut = {c00_0, c01_0, c02_1, c10_2, c11_3, c20_4}

    # act & assert
    assert all_different(true_sut) is True
    assert all_different(false_sut) is False


def test_is_rectangle_and_is_square(board: Board):
    c00 = board.get_element(Attribute.C, 0, 0)
    c01 = board.get_element(Attribute.C, 0, 1)
    c02 = board.get_element(Attribute.C, 0, 2)
    c10 = board.get_element(Attribute.C, 1, 0)
    c11 = board.get_element(Attribute.C, 1, 1)
    c12 = board.get_element(Attribute.C, 1, 2)
    hp00 = board.get_element(Attribute.Hp, 0, 0)

    true_sut_1 = {c00, c01, c02, c10, c11, c12}
    true_sut_2 = {}
    false_sut_1 = {c00, c01, c02, c11, c12}
    false_sut_2 = {hp00, c01, c02, c10, c11, c12}

    true_sut_3 = {c01, c02, c11, c12}
    false_sut_3 = {c00, c01, c02, c11, c12}

    assert is_rectangle(true_sut_1) is True
    assert is_rectangle(true_sut_2) is True
    assert is_rectangle(false_sut_1) is False
    assert is_rectangle(false_sut_2) is False

    assert is_square(true_sut_3) is True
    assert is_square(false_sut_3) is False


def test_generation_set():
    elements = {
        Element(Attribute.P, 0, 0, 1),
        Element(Attribute.P, 0, 1, 2),
        Element(Attribute.C, 1, 0, 3),
    }

    # Filter elements with value > 1
    result = generation_set(elements, lambda e: e.value > 1)
    expected = {
        Element(Attribute.P, 0, 1, 2),
        Element(Attribute.C, 1, 0, 3),
    }
    assert result == expected


def test_is_exists_and_is_all():
    elements = {
        Element(Attribute.P, 0, 0, 1),
        Element(Attribute.P, 0, 1, 2),
        Element(Attribute.C, 1, 0, 3),
    }

    # Test is_exists
    assert is_exists(elements, lambda e: e.value == 2) is True
    assert is_exists(elements, lambda e: e.value == 4) is False

    # Test is_all
    assert is_all(elements, lambda e: e.value > 0) is True
    assert is_all(elements, lambda e: e.value > 1) is False
