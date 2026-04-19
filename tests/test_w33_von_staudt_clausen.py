"""Pin Von Staudt-Clausen denominators and Kummer's irregular primes.

Tests cover:
    (1) denom(B_n) = prod_{(p-1)|n} p for every even n <= 30;
    (2) B_n + sum_{(p-1)|n} 1/p is an integer for every even n <= 30;
    (3) First 8 irregular primes are 37, 59, 67, 101, 103, 131, 149, 157;
    (4) 691 | numerator(B_12) -- in fact numerator(B_12) = 691;
    (5) 37 | numerator(B_32);
    (6) Primes 5, 7, 11, 13, 17, 19, 23, 29, 31 are all regular;
    (7) Specific B_n denominators (B_2 = 1/6, ..., B_24 = .../2730).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_von_staudt_clausen import (  # noqa: E402
    derive_all,
    divisors,
    integral_part_bernoulli,
    irregular_indices,
    is_regular_prime,
    staudt_clausen_denominator,
    staudt_clausen_primes,
    verify_37_irregular_index,
    verify_691_is_irregular_via_B_12,
    verify_denominator_formula,
    verify_first_irregular_primes,
    verify_integral_part,
    verify_small_primes_regular,
    verify_specific_denominators,
)
from w33_zeta_functional_equation import bernoulli  # noqa: E402


# ----------------------------------------------------------------------
# Helper sanity checks.
# ----------------------------------------------------------------------
def test_divisors_of_12():
    assert divisors(12) == [1, 2, 3, 4, 6, 12]


def test_divisors_of_30():
    assert divisors(30) == [1, 2, 3, 5, 6, 10, 15, 30]


# ----------------------------------------------------------------------
# Primes p with (p-1) | n.
# ----------------------------------------------------------------------
def test_sc_primes_n_2():
    """(p-1) | 2 => p-1 in {1,2} => p in {2,3}."""
    assert staudt_clausen_primes(2) == [2, 3]


def test_sc_primes_n_4():
    """(p-1) | 4 => p-1 in {1,2,4} => p in {2,3,5}."""
    assert staudt_clausen_primes(4) == [2, 3, 5]


def test_sc_primes_n_6():
    """(p-1) | 6 => p-1 in {1,2,3,6} => p in {2,3,7}  (4 not prime)."""
    assert staudt_clausen_primes(6) == [2, 3, 7]


def test_sc_primes_n_12():
    """divisors of 12: {1,2,3,4,6,12}; primes among +1: {2,3,5,7,13}."""
    assert staudt_clausen_primes(12) == [2, 3, 5, 7, 13]


def test_sc_primes_n_14():
    """divisors of 14: {1,2,7,14}; primes among {2,3,8,15}: only {2,3}."""
    assert staudt_clausen_primes(14) == [2, 3]


def test_sc_denominator_product():
    assert staudt_clausen_denominator(12) == 2 * 3 * 5 * 7 * 13


# ----------------------------------------------------------------------
# Specific denominators of B_n.
# ----------------------------------------------------------------------
def test_B_2_denom_6():
    assert bernoulli(2) == Fraction(1, 6)


def test_B_4_denom_30():
    assert bernoulli(4) == Fraction(-1, 30)


def test_B_12_is_minus_691_over_2730():
    assert bernoulli(12) == Fraction(-691, 2730)


def test_B_12_numerator_is_691():
    """The 691 that shows up in both Ramanujan tau and Kummer's irregularity."""
    assert abs(bernoulli(12).numerator) == 691


def test_specific_denominators_verifier():
    r = verify_specific_denominators()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Von Staudt-Clausen theorem.
# ----------------------------------------------------------------------
def test_denominator_formula_up_to_30():
    r = verify_denominator_formula(n_max=30)
    assert r["all_match"] is True


def test_integral_part_is_integer_up_to_30():
    r = verify_integral_part(n_max=30)
    assert r["all_match"] is True


def test_integral_part_n_2_is_1():
    """B_2 + 1/2 + 1/3 = 1/6 + 1/2 + 1/3 = 1."""
    v = integral_part_bernoulli(2)
    assert v.denominator == 1
    assert v.numerator == 1


def test_integral_part_n_4_is_1():
    """B_4 + 1/2 + 1/3 + 1/5 = -1/30 + 15/30 + 10/30 + 6/30 = 30/30 = 1."""
    v = integral_part_bernoulli(4)
    assert v.denominator == 1
    assert v.numerator == 1


def test_integral_part_n_6_is_1():
    """B_6 + 1/2 + 1/3 + 1/7 = 1/42 + 21/42 + 14/42 + 6/42 = 42/42 = 1."""
    v = integral_part_bernoulli(6)
    assert v.denominator == 1
    assert v.numerator == 1


# ----------------------------------------------------------------------
# Kummer irregular primes.
# ----------------------------------------------------------------------
def test_691_is_irregular_via_B_12():
    r = verify_691_is_irregular_via_B_12()
    assert r["match"] is True


def test_37_is_irregular_at_index_32():
    r = verify_37_irregular_index()
    assert r["match"] is True


def test_first_eight_irregular_primes():
    r = verify_first_irregular_primes()
    assert r["found"] == [37, 59, 67, 101, 103, 131, 149, 157]
    assert r["match"] is True


def test_37_irregular_indices_is_32():
    """At p=37, the only 2k <= 34 with 37 | numerator(B_{2k}) is 2k = 32."""
    idx = irregular_indices(37)
    assert 32 in idx


def test_small_primes_are_regular():
    r = verify_small_primes_regular()
    assert r["all_match"] is True


def test_5_is_regular():
    assert is_regular_prime(5) is True


def test_13_is_regular():
    assert is_regular_prime(13) is True


def test_31_is_regular():
    assert is_regular_prime(31) is True


def test_37_is_not_regular():
    assert is_regular_prime(37) is False


def test_59_is_not_regular():
    assert is_regular_prime(59) is False


def test_691_is_not_regular():
    """691 is irregular because 691 | numerator(B_12)."""
    assert is_regular_prime(691) is False


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
        "denominator_formula",
        "integral_part",
        "irregular_primes",
        "b691",
        "b37",
        "small_regular",
        "specific_dens",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_seven_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 7
