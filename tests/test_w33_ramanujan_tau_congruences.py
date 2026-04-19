"""Pin Ramanujan's tau congruences modulo 691, 5, 7, 256, 27.

Tests cover:
    (1) tau(n) ≡ sigma_{11}(n) (mod 691) up to n = 500;
    (2) tau(n) ≡ n sigma_1(n) (mod 5) up to n = 500;
    (3) tau(n) ≡ n sigma_3(n) (mod 7) up to n = 500;
    (4) tau(n) ≡ sigma_{11}(n) (mod 2^8 = 256) for odd n up to 500;
    (5) tau(n) ≡ n^2 sigma_7(n) (mod 27) for gcd(n,3)=1, n up to 500;
    (6) prime consequence tau(p) ≡ 1 + p^11 (mod 691), p <= 100;
    (7) the 691 lineage: B_12 = -691/2730 and zeta(-11) = 691/32760;
    (8) sigma_k helper correctness on small inputs.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_ramanujan_tau_congruences import (  # noqa: E402
    derive_all,
    sigma_k,
    verify_691_congruence,
    verify_691_prime_consequence,
    verify_bernoulli_691_connection,
    verify_mod_5,
    verify_mod_7,
    verify_mod_27_coprime3,
    verify_mod_256_odd,
    verify_specific_tau_values,
)


# ----------------------------------------------------------------------
# sigma_k helper.
# ----------------------------------------------------------------------
def test_sigma_0_is_divisor_count():
    """sigma_0(n) counts divisors."""
    assert sigma_k(1, 0) == 1
    assert sigma_k(6, 0) == 4   # 1,2,3,6
    assert sigma_k(12, 0) == 6  # 1,2,3,4,6,12


def test_sigma_1_at_small_n():
    assert sigma_k(1, 1) == 1
    assert sigma_k(6, 1) == 12
    assert sigma_k(7, 1) == 8


def test_sigma_11_at_p_equals_1_plus_p11():
    for p in [2, 3, 5, 7, 11, 13]:
        assert sigma_k(p, 11) == 1 + p ** 11


def test_sigma_k_multiplicative():
    """sigma_k is multiplicative on coprime arguments."""
    for a, b in [(2, 3), (5, 7), (4, 9), (8, 27)]:
        for k in [1, 3, 7, 11]:
            from math import gcd
            if gcd(a, b) == 1:
                assert sigma_k(a * b, k) == sigma_k(a, k) * sigma_k(b, k)


# ----------------------------------------------------------------------
# Main congruence tests.
# ----------------------------------------------------------------------
def test_tau_mod_691():
    r = verify_691_congruence(N=500)
    assert r["all_match"] is True


def test_tau_mod_5():
    r = verify_mod_5(N=500)
    assert r["all_match"] is True


def test_tau_mod_7():
    r = verify_mod_7(N=500)
    assert r["all_match"] is True


def test_tau_mod_256_odd():
    r = verify_mod_256_odd(N=500)
    assert r["all_match"] is True


def test_tau_mod_27_coprime3():
    r = verify_mod_27_coprime3(N=500)
    assert r["all_match"] is True


def test_tau_prime_691_consequence():
    r = verify_691_prime_consequence(prime_limit=100)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Specific numeric checks.
# ----------------------------------------------------------------------
def test_tau_2_mod_691():
    """tau(2) = -24 ≡ 667 mod 691, and 1 + 2^11 = 2049 ≡ 667 mod 691."""
    assert (-24) % 691 == 667
    assert (1 + 2 ** 11) % 691 == 667


def test_tau_3_mod_691():
    """tau(3) = 252, and 1 + 3^11 = 177148 ≡ 252 mod 691."""
    assert 252 % 691 == 252
    assert (1 + 3 ** 11) % 691 == 252


def test_tau_5_mod_691():
    """tau(5) = 4830 ≡ 684 mod 691."""
    assert 4830 % 691 == 684


def test_specific_values_verifier():
    r = verify_specific_tau_values()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Bernoulli 691 connection.
# ----------------------------------------------------------------------
def test_bernoulli_link_32760_equals_12_times_2730():
    """zeta(-11) = 691/32760;  B_12 = -691/2730;  32760 = 12 * 2730."""
    assert 12 * 2730 == 32760


def test_bernoulli_verifier():
    r = verify_bernoulli_691_connection()
    assert r["match"] is True


def test_tau_mod_5_at_small_n():
    from w33_ramanujan_tau_congruences import sigma_k
    # Direct spot-checks.
    # tau(1)=1, 1*sigma_1(1)=1. 1 mod 5 = 1.
    assert (1 * sigma_k(1, 1)) % 5 == 1 % 5
    # tau(2)=-24 ≡ 1 mod 5;  2*sigma_1(2)=2*3=6 ≡ 1 mod 5.
    assert (-24) % 5 == 1
    assert (2 * sigma_k(2, 1)) % 5 == 1


def test_tau_mod_7_at_small_n():
    from w33_ramanujan_tau_congruences import sigma_k
    # tau(2)=-24 ≡ 4 mod 7;  2*sigma_3(2)=2*9=18 ≡ 4 mod 7.
    assert (-24) % 7 == 4
    assert (2 * sigma_k(2, 3)) % 7 == 4


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
        "mod_691",
        "mod_5",
        "mod_7",
        "mod_256",
        "mod_27",
        "prime_691",
        "bernoulli",
        "specific",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_eight_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 8
