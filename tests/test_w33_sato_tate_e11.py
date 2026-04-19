"""Pin Sato-Tate for E_11 (non-CM) vs the CM curve y^2 = x^3 - x.

Tests cover:
    (1) x_p = a_p / (2 sqrt p) in [-1, 1] for E_11 over primes <= 1000;
    (2) Sample second moment of E_11 -> 1/4 (semicircle);
    (3) Sample fourth moment of E_11 -> 1/8 (semicircle);
    (4) Sample odd moments of E_11 -> 0 by symmetry;
    (5) CM curve y^2 = x^3 - x has a_p = 0 on roughly half the primes
        (the inert ones, p ≡ 3 mod 4);
    (6) CM fourth moment ~ 3/16, distinct from semicircle 1/8;
    (7) Semicircle moment ladder matches Catalan numbers / 4^k.
"""

from __future__ import annotations

import sys
from math import comb
from pathlib import Path

import mpmath as mp


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_sato_tate_e11 import (  # noqa: E402
    CM_sample_moments,
    E11_sample_moments,
    cm_even_moment,
    derive_all,
    primes_up_to,
    semicircle_even_moment,
    verify_CM_fourth_moment_larger,
    verify_CM_fraction_of_zero_traces,
    verify_E11_fourth_moment,
    verify_E11_odd_moments_small,
    verify_E11_second_moment,
    verify_E11_xp_in_unit_interval,
    verify_moment_ladder_semicircle,
)


# ----------------------------------------------------------------------
# Semicircle moment ladder.
# ----------------------------------------------------------------------
def test_semicircle_m0_is_1():
    assert semicircle_even_moment(0) == 1


def test_semicircle_m2_is_quarter():
    assert semicircle_even_moment(1) == mp.mpf(1) / 4


def test_semicircle_m4_is_eighth():
    assert semicircle_even_moment(2) == mp.mpf(1) / 8


def test_semicircle_m6_is_5_over_64():
    assert semicircle_even_moment(3) == mp.mpf(5) / 64


def test_semicircle_m8_is_7_over_128():
    assert semicircle_even_moment(4) == mp.mpf(7) / 128


def test_semicircle_ladder_catalan_scaling():
    for k in range(0, 6):
        Ck = comb(2 * k, k) // (k + 1)
        assert semicircle_even_moment(k) == mp.mpf(Ck) / mp.mpf(4 ** k)


def test_semicircle_ladder_verifier():
    r = verify_moment_ladder_semicircle()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# CM moments (symbolic).
# ----------------------------------------------------------------------
def test_cm_m0():
    assert cm_even_moment(0) == mp.mpf(1) / 2


def test_cm_m2_matches_semicircle():
    """E_CM[x^2] = 1/4 — same as semicircle."""
    assert cm_even_moment(1) == mp.mpf(1) / 4


def test_cm_m4_is_3_over_16():
    """E_CM[x^4] = 3/16, strictly larger than semicircle 1/8."""
    assert cm_even_moment(2) == mp.mpf(3) / 16
    assert mp.mpf(3) / 16 > mp.mpf(1) / 8


# ----------------------------------------------------------------------
# E_11 unit interval (Hasse).
# ----------------------------------------------------------------------
def test_E11_xp_in_unit_interval():
    r = verify_E11_xp_in_unit_interval(prime_limit=1000)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# E_11 sample moments.
# ----------------------------------------------------------------------
def test_E11_second_moment():
    r = verify_E11_second_moment(prime_limit=2000, tol=0.08)
    assert r["match"] is True


def test_E11_fourth_moment():
    r = verify_E11_fourth_moment(prime_limit=2000, tol=0.05)
    assert r["match"] is True


def test_E11_odd_moments():
    r = verify_E11_odd_moments_small(prime_limit=2000, tol=0.05)
    assert r["match"] is True


# ----------------------------------------------------------------------
# CM curve dichotomy.
# ----------------------------------------------------------------------
def test_CM_fraction_zero_about_half():
    r = verify_CM_fraction_of_zero_traces(prime_limit=2000, tol=0.05)
    assert r["match"] is True


def test_CM_fourth_moment():
    r = verify_CM_fourth_moment_larger(prime_limit=2000, tol=0.05)
    assert r["match"] is True


def test_CM_vs_noncm_fourth_moment_distinguishable():
    """The CM m4 target 3/16 differs from non-CM m4 target 1/8 by 1/16,
    so sample-moment differences at p_max = 2000 should land on the
    correct side of 5/32 (midpoint between semi and CM)."""
    e11 = E11_sample_moments(prime_limit=2000, k_max=4)
    cm = CM_sample_moments(prime_limit=2000, k_max=4)
    mid = (1.0 / 8 + 3.0 / 16) / 2  # = 5/32
    assert e11["moments"][4] < mid
    assert cm["moments"][4] > mid


# ----------------------------------------------------------------------
# Prime sieve sanity.
# ----------------------------------------------------------------------
def test_primes_up_to_50():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    assert primes_up_to(50) == expected


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
        "hasse",
        "E11_second_moment",
        "E11_fourth_moment",
        "E11_odd_moments",
        "CM_fraction_zero",
        "CM_fourth_moment",
        "semicircle_ladder",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_seven_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 7
