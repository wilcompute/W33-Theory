"""BT1141 regression tests for spin and Hodge a4 coefficients."""

from fractions import Fraction

K_NORM = 24
N = 440
F4_OVER_2 = 8160


def a4(rank, omega, e2):
    return Fraction(K_NORM, 720) * (2 * rank + 30 * omega + 180 * e2)


def product_c4(a4_value):
    return N * a4_value + F4_OVER_2


def test_spin_dirac_square_lane_is_numeric():
    spin = a4(4, Fraction(-1, 2), Fraction(0))
    assert spin == Fraction(-7, 30)
    assert product_c4(spin) == Fraction(24172, 3)


def test_hodge_all_forms_ordinary_trace_lane_is_numeric():
    hodge = a4(16, Fraction(-4), Fraction(1))
    assert hodge == Fraction(46, 15)
    assert product_c4(hodge) == Fraction(28528, 3)


def test_four_lanes_remain_distinct():
    corpus = Fraction(24)
    scalar = a4(1, Fraction(0), Fraction(0))
    spin = a4(4, Fraction(-1, 2), Fraction(0))
    hodge = a4(16, Fraction(-4), Fraction(1))
    assert scalar == Fraction(1, 15)
    assert len({corpus, scalar, spin, hodge}) == 4
