from __future__ import annotations

from generator.checker.dataclass import (
    Attribute,
    Element,
    is_diagonal,
    is_horizontal,
    is_vertical,
)


def test_is_horizontal():
    assert is_horizontal(Element(Attribute.P, 0, 0), Element(Attribute.P, 0, 1)) is True
    assert is_horizontal(Element(Attribute.C, 1, 2), Element(Attribute.C, 1, 3)) is True
    assert (
        is_horizontal(Element(Attribute.P, 0, 0), Element(Attribute.P, 1, 0)) is False
    )
    assert (
        is_horizontal(Element(Attribute.P, 0, 0), Element(Attribute.Hp, 0, 1)) is True
    )
    assert (
        is_horizontal(Element(Attribute.Hp, 0, 0), Element(Attribute.P, 0, 1)) is True
    )
    assert (
        is_horizontal(Element(Attribute.Hp, 0, 0), Element(Attribute.Hp, 0, 1)) is True
    )


def test_is_vertical():
    assert is_vertical(Element(Attribute.P, 0, 0), Element(Attribute.P, 1, 0)) is True
    assert is_vertical(Element(Attribute.C, 1, 2), Element(Attribute.C, 2, 2)) is True
    assert is_vertical(Element(Attribute.P, 0, 0), Element(Attribute.P, 0, 1)) is False
    assert is_vertical(Element(Attribute.P, 0, 0), Element(Attribute.Vp, 1, 0)) is True
    assert is_vertical(Element(Attribute.Vp, 1, 0), Element(Attribute.P, 0, 0)) is True
    assert is_vertical(Element(Attribute.Vp, 1, 0), Element(Attribute.P, 2, 0)) is True


def test_is_diagonal():
    assert is_diagonal(Element(Attribute.P, 0, 0), Element(Attribute.P, 1, 1)) is True
    assert is_diagonal(Element(Attribute.C, 2, 2), Element(Attribute.C, 3, 3)) is True
    assert is_diagonal(Element(Attribute.P, 0, 0), Element(Attribute.P, 0, 1)) is False
    assert (
        is_diagonal(Element(Attribute.Hp, 0, 0), Element(Attribute.Vp, 1, 1)) is False
    )
    assert (
        is_diagonal(Element(Attribute.Vc, 1, 1), Element(Attribute.Hc, 2, 2)) is False
    )
    assert is_diagonal(Element(Attribute.Hc, 1, 0), Element(Attribute.Vc, 0, 0)) is True
    assert is_diagonal(Element(Attribute.Hc, 1, 0), Element(Attribute.Vc, 0, 1)) is True
    assert is_diagonal(Element(Attribute.Hc, 1, 0), Element(Attribute.Vc, 1, 0)) is True
    assert is_diagonal(Element(Attribute.Hc, 1, 0), Element(Attribute.Vc, 1, 1)) is True


def test_compare_same_elements():
    # arrange
    c1 = Element(attr=Attribute.C, i=1, j=1)
    c2 = Element(attr=Attribute.C, i=1, j=1)

    c1.value = 1
    c2.value = 1

    # act
    # assert
    assert c1 == c2


def test_compare_other_elements():
    # arrange
    c1 = Element(attr=Attribute.C, i=1, j=1)
    c2 = Element(attr=Attribute.C, i=1, j=1)
    c3 = Element(attr=Attribute.C, i=1, j=3)

    c1.value = 1
    c2.value = 3
    c3.value = 1

    # act
    # assert
    assert c1 != c2
