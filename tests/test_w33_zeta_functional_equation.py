"""Pin the Riemann zeta function: Bernoulli, Euler formula, functional equation.

Tests cover:
    (1) Bernoulli numbers B_0..B_14 exact rational values;
    (2) Euler formula zeta(2k) = (-1)^{k+1} B_{2k} (2 pi)^{2k} / (2 (2k)!)
        for k = 1..6;
    (3) Trivial zeros zeta(-2k) = 0 for k = 1..6;
    (4) Negative odd integers zeta(1 - 2k) = -B_{2k}/(2k);
    (5) zeta(0) = -1/2;
    (6) Euler product matches Dirichlet series at s = 3;
    (7) Functional equation xi(s) = xi(1 - s) at off-line points;
    (8) First nontrivial zero t_1 = 14.134725... lies on Re(s) = 1/2.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_zeta_functional_equation import (  # noqa: E402
    bernoulli,
    derive_all,
    verify_basel_and_euler_even_values,
    verify_bernoulli_values,
    verify_euler_product_at_s,
    verify_first_nontrivial_zero,
    verify_functional_equation,
    verify_negative_odd_closed_form,
    verify_trivial_zeros,
    verify_zeta_at_zero_is_minus_one_half,
    xi,
    zeta_even_closed_form,
    zeta_neg_odd_closed_form,
    zeta_partial_dirichlet,
    zeta_partial_euler,
)


# ----------------------------------------------------------------------
# Bernoulli numbers.
# ----------------------------------------------------------------------
def test_bernoulli_0_is_1():
    assert bernoulli(0) == Fraction(1)


def test_bernoulli_1_is_minus_half():
    assert bernoulli(1) == Fraction(-1, 2)


def test_bernoulli_2_is_one_sixth():
    assert bernoulli(2) == Fraction(1, 6)


def test_bernoulli_12_is_minus_691_over_2730():
    """The 691 that shows up everywhere in Ramanujan / Delta."""
    assert bernoulli(12) == Fraction(-691, 2730)


def test_bernoulli_odd_vanish():
    for k in [3, 5, 7, 9, 11, 13, 15]:
        assert bernoulli(k) == 0


def test_bernoulli_pin_B14():
    assert bernoulli(14) == Fraction(7, 6)


def test_bernoulli_verifier():
    r = verify_bernoulli_values()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Basel / Euler formula.
# ----------------------------------------------------------------------
def test_basel_zeta_2_equals_pi2_over_6():
    mp.mp.dps = 40
    val = zeta_even_closed_form(1)
    expected = mp.pi ** 2 / 6
    assert abs(val - expected) < mp.mpf("1e-35")


def test_euler_zeta_4_equals_pi4_over_90():
    mp.mp.dps = 40
    val = zeta_even_closed_form(2)
    expected = mp.pi ** 4 / 90
    assert abs(val - expected) < mp.mpf("1e-35")


def test_euler_zeta_6_equals_pi6_over_945():
    mp.mp.dps = 40
    val = zeta_even_closed_form(3)
    expected = mp.pi ** 6 / 945
    assert abs(val - expected) < mp.mpf("1e-33")


def test_euler_zeta_8_equals_pi8_over_9450():
    mp.mp.dps = 40
    val = zeta_even_closed_form(4)
    expected = mp.pi ** 8 / 9450
    assert abs(val - expected) < mp.mpf("1e-33")


def test_even_values_verifier():
    r = verify_basel_and_euler_even_values(k_max=6, dps=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Trivial zeros.
# ----------------------------------------------------------------------
def test_zeta_minus_2_is_zero():
    mp.mp.dps = 40
    assert abs(mp.zeta(-2)) < mp.mpf("1e-35")


def test_trivial_zeros_verifier():
    r = verify_trivial_zeros(k_max=6, dps=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Negative odd integers.
# ----------------------------------------------------------------------
def test_zeta_minus_1_is_minus_one_twelfth():
    """zeta(-1) = -1/12."""
    assert zeta_neg_odd_closed_form(1) == Fraction(-1, 12)


def test_zeta_minus_3_is_one_over_120():
    assert zeta_neg_odd_closed_form(2) == Fraction(1, 120)


def test_zeta_minus_5_is_minus_1_over_252():
    assert zeta_neg_odd_closed_form(3) == Fraction(-1, 252)


def test_zeta_minus_11_has_691_numerator():
    """zeta(-11) = 691 / 32760 — another 691 sighting."""
    v = zeta_neg_odd_closed_form(6)
    assert v == Fraction(691, 32760)
    assert v.numerator == 691


def test_negative_odd_verifier():
    r = verify_negative_odd_closed_form(k_max=6, dps=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# zeta(0) = -1/2.
# ----------------------------------------------------------------------
def test_zeta_at_zero():
    r = verify_zeta_at_zero_is_minus_one_half(dps=50)
    assert r["match"] is True


# ----------------------------------------------------------------------
# Euler product.
# ----------------------------------------------------------------------
def test_euler_product_at_s_3():
    r = verify_euler_product_at_s(s=3.0, P=500, dps=40)
    assert r["match"] is True


def test_euler_product_single_factor_p_2():
    """At s = 3, the p = 2 factor is (1 - 1/8)^{-1} = 8/7."""
    mp.mp.dps = 40
    f = zeta_partial_euler(3.0, P=2)
    expected = mp.mpf(8) / 7
    assert abs(f - expected) < mp.mpf("1e-35")


# ----------------------------------------------------------------------
# Functional equation.
# ----------------------------------------------------------------------
def test_functional_equation_off_line():
    r = verify_functional_equation(dps=50)
    assert r["all_match"] is True


def test_xi_is_symmetric_at_complex_point():
    mp.mp.dps = 50
    s = mp.mpc(mp.mpf("0.75"), mp.mpf("2.3"))
    assert abs(xi(s) - xi(1 - s)) < mp.mpf("1e-40")


# ----------------------------------------------------------------------
# First nontrivial zero.
# ----------------------------------------------------------------------
def test_first_nontrivial_zero():
    r = verify_first_nontrivial_zero(dps=30)
    assert r["match"] is True


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_subresults():
    s = derive_all()
    for key in [
        "bernoulli",
        "euler_even_values",
        "trivial_zeros",
        "negative_odd_values",
        "zeta_at_zero",
        "euler_product",
        "functional_equation",
        "first_nontrivial_zero",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_eight_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 8
