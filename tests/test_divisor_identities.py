"""Pin divisor-sum identities forced by M_*(SL(2,Z)) = C[E_4, E_6].

E_4^2 = E_8  forces  sigma_7(n) = sigma_3(n) + 120 * conv(sigma_3, sigma_3).
E_4*E_6 = E_10  forces  11 sigma_9 = 21 sigma_5 - 10 sigma_3 + 5040 * conv.
1728 Delta = E_4^3 - E_6^2  expresses tau(n) as convolutions of divisors.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_divisor_identities import (  # noqa: E402
    derive_all_divisor_identities,
    verify_E12_combination,
    verify_sigma_7_identity,
    verify_sigma_9_identity,
    verify_tau_from_E4_E6,
)


# ----------------------------------------------------------------------
# sigma_7 identity.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", list(range(1, 16)))
def test_sigma_7_identity_at_n(n):
    results = verify_sigma_7_identity(n)
    assert results[n - 1]["match"] is True


def test_sigma_7_of_1():
    """sigma_7(1) = 1^7 = 1.  Conv = 0.  RHS = 1 + 120*0 = 1."""
    r = verify_sigma_7_identity(1)[0]
    assert r["sigma_7"] == 1
    assert r["conv"] == 0
    assert r["rhs"] == 1


def test_sigma_7_of_2():
    """sigma_7(2) = 1 + 128 = 129.  sigma_3(2) = 1 + 8 = 9.  Conv = sigma_3(1)^2 = 1.
    RHS = 9 + 120 = 129."""
    r = verify_sigma_7_identity(2)[1]
    assert r["sigma_7"] == 129
    assert r["conv"] == 1
    assert r["rhs"] == 9 + 120


def test_sigma_7_all_match():
    for r in verify_sigma_7_identity(15):
        assert r["match"] is True


# ----------------------------------------------------------------------
# sigma_9 identity.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", list(range(1, 11)))
def test_sigma_9_identity_at_n(n):
    results = verify_sigma_9_identity(n)
    assert results[n - 1]["match"] is True


def test_sigma_9_of_1():
    """11 sigma_9(1) = 11.  RHS = 21 - 10 + 0 = 11."""
    r = verify_sigma_9_identity(1)[0]
    assert r["11*sigma_9"] == 11
    assert r["conv"] == 0
    assert r["rhs"] == 11


def test_sigma_9_all_match():
    for r in verify_sigma_9_identity(12):
        assert r["match"] is True


# ----------------------------------------------------------------------
# E_12 decomposition in span(E_4^3, E_6^2) -- the 691 reappears.
# ----------------------------------------------------------------------
def test_E12_alpha_plus_beta_is_1():
    r = verify_E12_combination(5)
    assert Fraction(r["alpha"]) + Fraction(r["beta"]) == 1


def test_E12_denominator_is_691():
    """E_12 = (441/691) E_4^3 + (250/691) E_6^2.  Denominator 691 = same as Ramanujan."""
    r = verify_E12_combination(5)
    alpha = Fraction(r["alpha"])
    beta = Fraction(r["beta"])
    assert alpha.denominator == 691
    assert beta.denominator == 691


def test_E12_numerators_sum_to_691():
    """441 + 250 = 691 (since alpha + beta = 1 and common denominator is 691)."""
    r = verify_E12_combination(5)
    alpha = Fraction(r["alpha"])
    beta = Fraction(r["beta"])
    assert alpha.numerator + beta.numerator == 691
    assert alpha == Fraction(441, 691)
    assert beta == Fraction(250, 691)


def test_E12_combination_all_match():
    r = verify_E12_combination(5)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# 1728 tau(n) = [q^n] (E_4^3 - E_6^2).
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", list(range(1, 11)))
def test_1728_tau_equals_E4cubed_minus_E6sq(n):
    results = verify_tau_from_E4_E6(n)
    assert results[n - 1]["match"] is True


def test_tau_1_identity():
    """1728 tau(1) = 1728 = [q^1] E_4^3 - [q^1] E_6^2 = 720 - (-1008) = 1728."""
    r = verify_tau_from_E4_E6(1)[0]
    assert r["tau(n)"] == 1
    assert r["1728*tau(n)"] == 1728
    assert r["E4^3 - E6^2"] == 1728


def test_tau_2_identity():
    """1728 * (-24) = -41472.  Matches E_4^3[q^2] - E_6^2[q^2]."""
    r = verify_tau_from_E4_E6(2)[1]
    assert r["tau(n)"] == -24
    assert r["1728*tau(n)"] == -41472


def test_tau_all_divisible_by_1728():
    """The right-hand side must be divisible by 1728 for every n (tau is integer)."""
    for r in verify_tau_from_E4_E6(10):
        assert r["E4^3 - E6^2"] % 1728 == 0


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_chain_all_true():
    chain = derive_all_divisor_identities(n_max=15)
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"
