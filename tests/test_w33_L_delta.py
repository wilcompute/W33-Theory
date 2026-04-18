"""Pin the L-function of Delta: Euler product, Deligne bound, Satake data.

Tests cover:
    (1) Deligne-Ramanujan-Petersson bound |tau(p)| <= 2 p^{11/2} for all
        primes p <= 100;
    (2) Euler product matches truncated Dirichlet series at s=8 within
        1e-3 (cutoff at P=40 primes, N=500 terms);
    (3) Hecke recursion tau(p^{r+1}) = tau(p) tau(p^r) - p^{11} tau(p^{r-1})
        for all (p, r) with p^{r+1} <= 1500;
    (4) tau(m n) = tau(m) tau(n) when gcd(m, n) = 1, m n <= 1500;
    (5) Hecke polynomial X^2 - tau(p) X + p^{11} has nonpositive
        discriminant (Satake roots are complex conjugate pairs of modulus
        p^{11/2});
    (6) cos(theta_p) = tau(p) / (2 p^{11/2}) lies in [-1, 1] up to p=50;
    (7) specific tau values match the Eisenstein-derived Delta.
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_L_delta import (  # noqa: E402
    L_partial,
    derive_all,
    euler_product_partial,
    primes_up_to,
    tau,
    tau_table,
    verify_deligne_bound,
    verify_euler_product_convergence,
    verify_hecke_recursion,
    verify_multiplicativity,
    verify_satake_angle_in_0_pi,
    verify_satake_product_equals_p_11,
)


# ----------------------------------------------------------------------
# Tau table sanity.
# ----------------------------------------------------------------------
def test_tau_1_is_1():
    assert tau(1) == 1


def test_tau_2_is_minus_24():
    assert tau(2) == -24


def test_tau_3_is_252():
    assert tau(3) == 252


def test_tau_5_is_4830():
    assert tau(5) == 4830


def test_tau_7_is_minus_16744():
    assert tau(7) == -16744


def test_tau_table_first_10_ramanujan():
    t = tau_table(11)
    expected = {1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830,
                6: -6048, 7: -16744, 8: 84480, 9: -113643,
                10: -115920}
    for n, e in expected.items():
        assert t[n] == e


# ----------------------------------------------------------------------
# Primes helper.
# ----------------------------------------------------------------------
def test_primes_up_to_30():
    assert primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


# ----------------------------------------------------------------------
# Deligne bound.
# ----------------------------------------------------------------------
def test_deligne_up_to_100():
    r = verify_deligne_bound(prime_limit=100)
    assert r["all_match"] is True


def test_deligne_bound_is_strict_at_p_2():
    """|tau(2)| = 24 < 2 * 2^{11/2} ~ 90.5."""
    assert abs(tau(2)) < 2 * 2 ** 5.5


def test_deligne_bound_at_p_23_matches_table():
    """tau(23) = 18643272, bound 2*23^{11/2} ~ 6.17e7."""
    bound = 2 * mp.power(23, mp.mpf(11) / 2)
    assert abs(tau(23)) < bound


# ----------------------------------------------------------------------
# Hecke recursion.
# ----------------------------------------------------------------------
def test_hecke_recursion_cap_1500():
    r = verify_hecke_recursion(prime_limit=20, cap=1500)
    assert r["all_match"] is True


def test_hecke_recursion_at_p_2_r_1():
    """tau(4) = tau(2)^2 - 2^{11} = 576 - 2048 = -1472."""
    lhs = tau(4)
    rhs = tau(2) ** 2 - 2 ** 11
    assert lhs == rhs == -1472


def test_hecke_recursion_at_p_3_r_1():
    """tau(9) = tau(3)^2 - 3^{11} = 63504 - 177147 = -113643."""
    lhs = tau(9)
    rhs = tau(3) ** 2 - 3 ** 11
    assert lhs == rhs == -113643


# ----------------------------------------------------------------------
# Multiplicativity.
# ----------------------------------------------------------------------
def test_multiplicativity_cap_1500():
    r = verify_multiplicativity(cap=1500)
    assert r["all_match"] is True
    assert r["check_count"] > 0


def test_multiplicativity_at_2_and_3():
    """tau(6) = tau(2) * tau(3) = -24 * 252 = -6048."""
    assert tau(6) == tau(2) * tau(3)
    assert tau(6) == -6048


def test_multiplicativity_at_5_and_7():
    """tau(35) = tau(5) * tau(7)."""
    assert tau(35) == tau(5) * tau(7)


# ----------------------------------------------------------------------
# Hecke polynomial discriminant (Deligne).
# ----------------------------------------------------------------------
def test_hecke_polynomial_discriminant_nonpositive_up_to_p_50():
    r = verify_satake_product_equals_p_11(prime_limit=50)
    assert r["all_match"] is True


def test_hecke_discriminant_at_p_2():
    """tau(2)^2 - 4 * 2^{11} = 576 - 8192 = -7616 < 0."""
    assert tau(2) ** 2 - 4 * 2 ** 11 == 576 - 8192 == -7616


def test_hecke_discriminant_at_p_3():
    """tau(3)^2 - 4 * 3^{11} = 63504 - 708588 < 0."""
    assert tau(3) ** 2 - 4 * 3 ** 11 < 0


# ----------------------------------------------------------------------
# Satake cos(theta) in [-1, 1].
# ----------------------------------------------------------------------
def test_satake_angle_in_unit_interval():
    r = verify_satake_angle_in_0_pi(prime_limit=50)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Euler product convergence.
# ----------------------------------------------------------------------
def test_euler_product_matches_dirichlet_at_s_8():
    r = verify_euler_product_convergence(s=8.0, P=40, N=500, dps=40)
    assert r["small"] is True


def test_euler_product_factor_at_p_2_s_8():
    """(1 - tau(2) * 2^{-8} + 2^{11 - 16})^{-1} factor shape."""
    mp.mp.dps = 30
    f = euler_product_partial(8.0, P=2)
    assert f.imag == 0 or abs(f.imag) < mp.mpf("1e-20")


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
        "euler_convergence",
        "deligne_bound",
        "hecke_recursion",
        "multiplicativity",
        "satake_discriminant",
        "satake",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_six_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 6
