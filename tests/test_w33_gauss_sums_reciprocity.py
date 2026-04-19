"""Pin Gauss sums, quadratic reciprocity, and Gauss's sign theorem.

Tests cover:
    (1) Legendre symbol via Euler criterion matches Jacobi/Kronecker;
    (2) Quadratic reciprocity over all odd prime pairs p,q <= 100;
    (3) Supplementary laws (-1/p), (2/p) for odd primes p <= 200;
    (4) |g(chi_D)|^2 = |D| for 20 fundamental D;
    (5) Gauss sign theorem: g(chi_D) = i sqrt|D| for D<0 fundamental;
    (6) Gauss sign theorem: g(chi_D) = sqrt(D) for D>0 fundamental;
    (7) Specific Gauss sum values for D = -3, -4, -7, -8 and D = 5, 8.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_gauss_sums_reciprocity import (  # noqa: E402
    derive_all,
    gauss_sum,
    legendre,
    verify_gauss_sign_negative,
    verify_gauss_sign_positive,
    verify_gauss_squared_modulus,
    verify_legendre_equals_kronecker,
    verify_quadratic_reciprocity,
    verify_supplementary_minus_one,
    verify_supplementary_two,
)


# ----------------------------------------------------------------------
# Legendre symbol.
# ----------------------------------------------------------------------
def test_legendre_quadratic_residues_mod_7():
    """{1, 2, 4} QR mod 7; {3, 5, 6} NQR mod 7."""
    for a in [1, 2, 4]:
        assert legendre(a, 7) == 1
    for a in [3, 5, 6]:
        assert legendre(a, 7) == -1


def test_legendre_zero_when_divisible():
    assert legendre(0, 11) == 0
    assert legendre(11, 11) == 0


def test_legendre_matches_kronecker_up_to_p_100():
    r = verify_legendre_equals_kronecker(prime_limit=100)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Quadratic reciprocity.
# ----------------------------------------------------------------------
def test_qr_small_pair_3_5():
    """(3/5)(5/3). 3 QR mod 5? 3 not in {1,4}, so (3/5)=-1. 5 mod 3 = 2,
    2 not in {1}, so (5/3)=-1. Product = 1. (p-1)/2=1, (q-1)/2=2;
    (-1)^2 = 1.  Match."""
    assert legendre(3, 5) * legendre(5, 3) == 1
    assert (-1) ** (1 * 2) == 1


def test_qr_pair_3_7():
    """3 mod 7 = 3 NQR, so (3/7)=-1. 7 mod 3 = 1 QR, so (7/3)=1. Product
    = -1.  (p-1)/2=1, (q-1)/2=3; (-1)^3=-1. Match."""
    assert legendre(3, 7) * legendre(7, 3) == -1
    assert (-1) ** (1 * 3) == -1


def test_qr_full_verifier():
    r = verify_quadratic_reciprocity(prime_limit=100)
    assert r["all_match"] is True
    assert r["check_count"] > 0


def test_qr_check_count_positive():
    r = verify_quadratic_reciprocity(prime_limit=30)
    # primes 3,5,7,11,13,17,19,23,29 -> 9 primes -> C(9,2)=36 pairs
    assert r["check_count"] == 36


# ----------------------------------------------------------------------
# Supplementary laws.
# ----------------------------------------------------------------------
def test_supplementary_minus_one_p_5():
    """(-1/5) = +1 because 5 == 1 mod 4."""
    assert legendre(-1, 5) == 1


def test_supplementary_minus_one_p_7():
    """(-1/7) = -1 because 7 == 3 mod 4."""
    assert legendre(-1, 7) == -1


def test_supplementary_two_p_7():
    """(2/7) = 1 because 7 == 7 mod 8 in {1,7}."""
    assert legendre(2, 7) == 1


def test_supplementary_two_p_5():
    """(2/5) = -1 because 5 == 5 mod 8 in {3,5}."""
    assert legendre(2, 5) == -1


def test_supplementary_verifier_minus_one():
    r = verify_supplementary_minus_one(prime_limit=200)
    assert r["all_match"] is True


def test_supplementary_verifier_two():
    r = verify_supplementary_two(prime_limit=200)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Gauss sum |g|^2 = |D|.
# ----------------------------------------------------------------------
def test_gauss_squared_minus_3():
    mp.mp.dps = 40
    g = gauss_sum(-3, dps=40)
    assert abs(abs(g) ** 2 - 3) < mp.mpf("1e-30")


def test_gauss_squared_minus_23():
    mp.mp.dps = 40
    g = gauss_sum(-23, dps=40)
    assert abs(abs(g) ** 2 - 23) < mp.mpf("1e-30")


def test_gauss_squared_verifier():
    r = verify_gauss_squared_modulus(dps=60)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Gauss sign theorem.
# ----------------------------------------------------------------------
def test_gauss_sign_minus_3_is_i_sqrt_3():
    mp.mp.dps = 40
    g = gauss_sum(-3, dps=40)
    expected = mp.mpc(0, mp.sqrt(3))
    assert abs(g - expected) < mp.mpf("1e-30")


def test_gauss_sign_minus_4_is_2i():
    """g(chi_{-4}) = i sqrt(4) = 2i."""
    mp.mp.dps = 40
    g = gauss_sum(-4, dps=40)
    assert abs(g - mp.mpc(0, 2)) < mp.mpf("1e-30")


def test_gauss_sign_minus_163():
    """The Heegner 163 case."""
    mp.mp.dps = 60
    g = gauss_sum(-163, dps=60)
    expected = mp.mpc(0, mp.sqrt(163))
    assert abs(g - expected) < mp.mpf("1e-30")


def test_gauss_sign_negative_verifier():
    r = verify_gauss_sign_negative(dps=60)
    assert r["all_match"] is True


def test_gauss_sign_positive_5_is_sqrt_5():
    mp.mp.dps = 40
    g = gauss_sum(5, dps=40)
    expected = mp.mpc(mp.sqrt(5), 0)
    assert abs(g - expected) < mp.mpf("1e-30")


def test_gauss_sign_positive_8_is_sqrt_8():
    mp.mp.dps = 40
    g = gauss_sum(8, dps=40)
    expected = mp.mpc(mp.sqrt(8), 0)
    assert abs(g - expected) < mp.mpf("1e-30")


def test_gauss_sign_positive_verifier():
    r = verify_gauss_sign_positive(dps=60)
    assert r["all_match"] is True


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
        "gauss_squared",
        "gauss_sign_negative",
        "gauss_sign_positive",
        "quadratic_reciprocity",
        "supplementary_minus_one",
        "supplementary_two",
        "legendre_kronecker",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_seven_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 7
