"""Pin Bernoulli numbers and Riemann zeta values at integer arguments.

The Bernoulli numbers B_n come from  z / (e^z - 1) = sum B_n z^n / n!.
The Riemann zeta values at even positive integers follow from

    zeta(2 n)  =  (2 pi)^(2 n) |B_{2 n}| / (2 (2 n)!)

and at negative odd integers from the analytic continuation

    zeta(1 - 2 n)  =  -B_{2 n} / (2 n).

Trivial zeros: zeta(-2 n) = 0 for n >= 1 (since B_{2 n + 1} = 0).
Special value: zeta(0) = -1/2.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from math import pi
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_bernoulli_zeta import (  # noqa: E402
    bernoulli,
    cot_taylor_coefficients_from_bernoulli,
    derive_all_zeta,
    zeta_even_pi_coefficient,
    zeta_negative_odd,
    zeta_partial_sum,
)


# ----------------------------------------------------------------------
# Bernoulli numbers.  Convention: B_1 = -1/2.
# ----------------------------------------------------------------------
EXPECTED_BERN = {
    0:  Fraction(1, 1),
    1:  Fraction(-1, 2),
    2:  Fraction(1, 6),
    3:  Fraction(0, 1),
    4:  Fraction(-1, 30),
    5:  Fraction(0, 1),
    6:  Fraction(1, 42),
    7:  Fraction(0, 1),
    8:  Fraction(-1, 30),
    9:  Fraction(0, 1),
    10: Fraction(5, 66),
    11: Fraction(0, 1),
    12: Fraction(-691, 2730),
    13: Fraction(0, 1),
    14: Fraction(7, 6),
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_BERN.items()))
def test_bernoulli_numbers_exact(n, expected):
    assert bernoulli(n) == expected


def test_odd_bernoulli_vanish_for_n_ge_3():
    for n in range(3, 20, 2):
        assert bernoulli(n) == 0


# ----------------------------------------------------------------------
# Zeta at positive even integers  zeta(2n) = c * pi^(2n).
# ----------------------------------------------------------------------
EXPECTED_ZETA_EVEN = {
    1: Fraction(1, 6),
    2: Fraction(1, 90),
    3: Fraction(1, 945),
    4: Fraction(1, 9450),
    5: Fraction(1, 93555),
    6: Fraction(691, 638512875),
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_ZETA_EVEN.items()))
def test_zeta_even_pi_coefficient(n, expected):
    assert zeta_even_pi_coefficient(n) == expected


def test_zeta_2_is_pi_squared_over_6_basel_problem():
    assert zeta_even_pi_coefficient(1) == Fraction(1, 6)


def test_zeta_4_is_pi_fourth_over_90():
    assert zeta_even_pi_coefficient(2) == Fraction(1, 90)


def test_zeta_6_is_pi_sixth_over_945():
    assert zeta_even_pi_coefficient(3) == Fraction(1, 945)


# ----------------------------------------------------------------------
# Numerical cross-check:  exact zeta(2n) matches partial sum.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", [2, 3, 4])
def test_zeta_even_matches_partial_sum(n):
    exact = float(zeta_even_pi_coefficient(n)) * pi ** (2 * n)
    # zeta(2) converges slowly; use n >= 2 for tight agreement.
    approx = zeta_partial_sum(2 * n, N=20000)
    assert abs(exact - approx) / exact < 1e-6


# ----------------------------------------------------------------------
# Zeta at negative odd integers  zeta(1 - 2n) = -B_{2n} / (2n).
# ----------------------------------------------------------------------
EXPECTED_ZETA_NEG_ODD = {
    1: Fraction(-1, 12),    # zeta(-1) = -1/12   (Ramanujan sum)
    2: Fraction(1, 120),    # zeta(-3) = 1/120
    3: Fraction(-1, 252),   # zeta(-5) = -1/252
    4: Fraction(1, 240),    # zeta(-7) = 1/240
    5: Fraction(-1, 132),   # zeta(-9) = -1/132
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_ZETA_NEG_ODD.items()))
def test_zeta_negative_odd(n, expected):
    assert zeta_negative_odd(n) == expected


def test_zeta_minus_one_equals_minus_one_twelfth_ramanujan():
    """The famous 'sum 1 + 2 + 3 + ... = -1/12' (analytic continuation)."""
    assert zeta_negative_odd(1) == Fraction(-1, 12)


# ----------------------------------------------------------------------
# Cot Taylor expansion matches zeta via Bernoulli numbers.
#     pi x cot(pi x)  =  1  -  2 sum_{k >= 1}  zeta(2 k)  x^(2 k).
# ----------------------------------------------------------------------
def test_cot_taylor_coefficients_match_zeta():
    coefs = cot_taylor_coefficients_from_bernoulli(order=6)
    assert coefs[0] == Fraction(1, 1)
    for k in range(1, 7):
        # coefficient of x^(2k) in pi x cot(pi x) equals  -2 * coef_k
        # where zeta(2k) = coef_k * pi^(2k).
        assert coefs[k] == -2 * zeta_even_pi_coefficient(k)


# ----------------------------------------------------------------------
# The full driver dict.
# ----------------------------------------------------------------------
@pytest.fixture(scope="module")
def chain():
    return derive_all_zeta()


def test_driver_produces_all_expected_values(chain):
    assert chain["zeta(0)"] == "-1/2"
    # Trivial zeros
    for k, v in chain["zeta_negative_even_trivial"].items():
        assert v == "0"
    # Even zeta coefficients
    assert chain["zeta_even_positive"]["zeta(2)"]["coefficient_of_pi^{2n}"] == "1/6"
    assert chain["zeta_even_positive"]["zeta(4)"]["coefficient_of_pi^{2n}"] == "1/90"
    assert chain["zeta_even_positive"]["zeta(6)"]["coefficient_of_pi^{2n}"] == "1/945"


def test_w33_bridge_has_phi_3_4_6_slots(chain):
    slots = chain["w33_bridge"]["finite_slots_at_q=3"]
    assert slots["Phi_3(3)"] == 13
    assert slots["Phi_4(3)"] == 10
    assert slots["Phi_6(3)"] == 7


def test_numerical_verification_tight(chain):
    for label, rec in chain["numerical_verification"].items():
        assert rec["rel_error"] < 1e-4


# ----------------------------------------------------------------------
# Sanity: |B_{2n}| strictly increasing from n=4 on (for our derivation).
# ----------------------------------------------------------------------
def test_bernoulli_magnitudes_grow_at_large_n():
    # |B_{2n}| grows factorially; verify |B_12| > |B_10| > |B_8|.
    assert abs(bernoulli(12)) > abs(bernoulli(10))
    assert abs(bernoulli(10)) > abs(bernoulli(8))
    # And B_14 > B_12.
    assert abs(bernoulli(14)) > abs(bernoulli(12))
