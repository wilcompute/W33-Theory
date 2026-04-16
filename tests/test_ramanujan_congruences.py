"""Pin the Ramanujan 691-congruence  tau(n) == sigma_11(n)  (mod 691).

The prime 691 appears as the numerator of B_12 = -691/2730, which gives the
E_12 Eisenstein constant  -4*6/B_12 = 65520/691.  Clearing this denominator
forces the weight-12 cusp form Delta to match the divisor-sum E_12 modulo 691,
giving Ramanujan's congruence.

For primes p,  sigma_11(p) = 1 + p^11  gives the specialization

    tau(p)  ==  1  +  p^11  (mod 691).
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_ramanujan_congruences import (  # noqa: E402
    bernoulli_B12,
    derive_all_ramanujan,
    E12_eisenstein_constant,
    factor_B12_numerator,
    first_primes_up_to,
    verify_691_congruence_at_n,
    verify_691_congruence_range,
    verify_tau_prime_congruence,
)


# ----------------------------------------------------------------------
# The source of 691: B_12's numerator.
# ----------------------------------------------------------------------
def test_B12_equals_minus_691_over_2730():
    assert bernoulli_B12() == Fraction(-691, 2730)


def test_E12_eisenstein_constant_is_65520_over_691():
    assert E12_eisenstein_constant() == Fraction(65520, 691)


def test_691_is_numerator_of_B12():
    info = factor_B12_numerator()
    assert info["numerator_abs"] == 691
    assert info["denominator"] == 2730


def test_2730_factorization():
    """2730 = 2 * 3 * 5 * 7 * 13."""
    assert 2 * 3 * 5 * 7 * 13 == 2730


def test_691_is_prime():
    """691 is prime (trial division up to sqrt(691) ~ 26)."""
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23):
        assert 691 % p != 0


# ----------------------------------------------------------------------
# Ramanujan 691-congruence:  tau(n) == sigma_11(n)  mod 691.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", list(range(1, 21)))
def test_tau_equiv_sigma_11_mod_691(n):
    r = verify_691_congruence_at_n(n)
    assert r["match"] is True


def test_tau_of_1_equals_sigma_11_of_1_exactly():
    """At n=1, tau(1) = 1 = sigma_11(1) exactly, not just mod 691."""
    r = verify_691_congruence_at_n(1)
    assert r["tau"] == 1
    assert r["sigma_11"] == 1


def test_tau_of_2_difference_is_3_times_691():
    """tau(2) = -24, sigma_11(2) = 1 + 2048 = 2049, diff = 2073 = 3 * 691."""
    r = verify_691_congruence_at_n(2)
    assert r["tau"] == -24
    assert r["sigma_11"] == 2049
    assert r["sigma_11"] - r["tau"] == 2073
    assert 2073 == 3 * 691


def test_congruence_all_match_up_to_20():
    results = verify_691_congruence_range(20)
    assert all(r["match"] for r in results)


# ----------------------------------------------------------------------
# Prime case:  tau(p) == 1 + p^11  (mod 691).
# ----------------------------------------------------------------------
EXPECTED_PRIMES_UP_TO_30 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_primes_up_to_30():
    assert first_primes_up_to(30) == EXPECTED_PRIMES_UP_TO_30


@pytest.mark.parametrize("p", EXPECTED_PRIMES_UP_TO_30)
def test_tau_prime_equiv_1_plus_p11_mod_691(p):
    r = verify_tau_prime_congruence(p)
    assert r["match"] is True


def test_tau_of_2_mod_691():
    """tau(2) = -24, and -24 mod 691 = 667.  Also (1 + 2^11) mod 691 = 2049 mod 691 = 667."""
    r = verify_tau_prime_congruence(2)
    assert r["tau(p)"] == -24
    assert r["1 + p^11"] == 1 + 2048
    assert r["tau mod 691"] == (-24) % 691
    assert r["tau mod 691"] == r["pred mod 691"]
    assert r["tau mod 691"] == 667


def test_tau_of_3_congruence():
    """tau(3) = 252, sigma_11(3) = 177148.  177148 - 252 = 176896 = 256 * 691."""
    r = verify_691_congruence_at_n(3)
    assert r["tau"] == 252
    assert r["sigma_11"] == 1 + 3 ** 11
    assert r["sigma_11"] - r["tau"] == 256 * 691


# ----------------------------------------------------------------------
# Driver consistency.
# ----------------------------------------------------------------------
def test_driver_chain_all_match():
    chain = derive_all_ramanujan(n_max=30)
    assert chain["ramanujan_691_congruence"]["all_match"] is True
    assert chain["prime_congruence_tau_p_equiv_1_plus_p11"]["all_match"] is True
    assert chain["the_prime_691"]["numerator_abs"] == 691
    assert chain["E_12_constant"] == "65520/691"
