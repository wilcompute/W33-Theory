"""Pin Euler's pentagonal theorem and the partition recurrence.

    prod(1 - q^n) = sum_{k in Z} (-1)^k q^{k(3k-1)/2}

gives the recurrence  p(n) = p(n-1) + p(n-2) - p(n-5) - p(n-7) + ...

The q^{1/24} prefactor of eta comes from zeta(-1) = -1/12.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_euler_pentagonal import (  # noqa: E402
    OEIS_A000041,
    derive_all_pentagonal,
    euler_pentagonal_series,
    first_pentagonal_exponents,
    generalized_pentagonal,
    partition_numbers,
    verify_partition_recurrence,
    verify_product_inverse,
    zeta_neg_1_equals_minus_1_over_12,
)


# ----------------------------------------------------------------------
# Pentagonal exponents.
# ----------------------------------------------------------------------
def test_generalized_pentagonal_k_0():
    assert generalized_pentagonal(0) == 0


def test_generalized_pentagonal_k_1():
    assert generalized_pentagonal(1) == 1


def test_generalized_pentagonal_k_neg_1():
    assert generalized_pentagonal(-1) == 2


def test_generalized_pentagonal_k_2():
    assert generalized_pentagonal(2) == 5


def test_generalized_pentagonal_k_neg_2():
    assert generalized_pentagonal(-2) == 7


def test_generalized_pentagonal_k_3():
    assert generalized_pentagonal(3) == 12


def test_first_pentagonal_exponents():
    exps = first_pentagonal_exponents(8)
    assert exps == [0, 1, 2, 5, 7, 12, 15, 22]


# ----------------------------------------------------------------------
# Euler's product formula coefficients.
# ----------------------------------------------------------------------
def test_euler_product_at_zero_is_1():
    c = euler_pentagonal_series(30)
    assert c[0] == 1


def test_euler_product_at_1_is_minus_1():
    c = euler_pentagonal_series(30)
    assert c[1] == -1


def test_euler_product_at_2_is_minus_1():
    c = euler_pentagonal_series(30)
    assert c[2] == -1


def test_euler_product_at_5_is_plus_1():
    c = euler_pentagonal_series(30)
    assert c[5] == 1


def test_euler_product_at_7_is_plus_1():
    c = euler_pentagonal_series(30)
    assert c[7] == 1


def test_euler_product_at_12_is_minus_1():
    c = euler_pentagonal_series(30)
    assert c[12] == -1


def test_euler_product_only_on_pentagonal_exponents():
    """prod(1-q^n) coefficients are zero except at pentagonal exponents."""
    order = 30
    c = euler_pentagonal_series(order)
    pent_set = set(first_pentagonal_exponents(20))
    for n in range(order + 1):
        if c[n] != 0:
            assert n in pent_set, f"Nonzero at non-pentagonal n={n}"


# ----------------------------------------------------------------------
# Partition numbers via Euler recurrence.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n,val", list(enumerate(OEIS_A000041)))
def test_partition_number_matches_oeis(n, val):
    p = partition_numbers(n + 1)
    assert p[n] == val


def test_partition_recurrence_all_match():
    for r in verify_partition_recurrence(25):
        assert r["match"] is True


def test_p_of_0_is_1():
    assert partition_numbers(0) == [1]


def test_p_of_5_is_7():
    """Partitions of 5: 5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1 = 7."""
    p = partition_numbers(5)
    assert p[5] == 7


def test_p_of_10_is_42():
    p = partition_numbers(10)
    assert p[10] == 42


# ----------------------------------------------------------------------
# Product inverse: Euler * partition = 1.
# ----------------------------------------------------------------------
def test_euler_times_partitions_is_1():
    r = verify_product_inverse(25)
    assert r["inverse_check"] is True
    assert r["constant_is_1"] is True
    assert r["higher_all_zero"] is True


# ----------------------------------------------------------------------
# zeta(-1) = -1/12 and the 1/24 in eta.
# ----------------------------------------------------------------------
def test_zeta_neg_1_is_minus_1_over_12():
    r = zeta_neg_1_equals_minus_1_over_12()
    assert r["zeta(-1) = -1/12"] is True
    assert Fraction(r["zeta(-1)"]) == Fraction(-1, 12)


def test_B2_is_1_over_6():
    r = zeta_neg_1_equals_minus_1_over_12()
    assert Fraction(r["B_2"]) == Fraction(1, 6)


def test_eta_prefactor_exponent_is_1_over_24():
    r = zeta_neg_1_equals_minus_1_over_12()
    assert r["is_1_over_24"] is True
    assert Fraction(r["zeta_neg_1_over_2"]) == Fraction(1, 24)


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_chain_all_true():
    chain = derive_all_pentagonal(25)
    for key, val in chain["summary_chain"].items():
        assert val is True, f"{key} = {val}"
