"""Pin the Eisenstein ring closure and Ramanujan's 691 congruence.

Main integer-series claims:

    E_8  = E_4^2                                    (weight 8,  dim M = 1),
    E_10 = E_4 * E_6                                (weight 10, dim M = 1),
    E_14 = E_4^2 * E_6                              (weight 14, dim M = 1),
    691 * E_12 = 441 * E_4^3 + 250 * E_6^2          (weight 12, dim M = 2).

Ramanujan's 691 congruence:
    tau(n) == sigma_11(n)  (mod 691)  for every positive integer n.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_eisenstein_closure import (  # noqa: E402
    bernoulli_weight_12_signature,
    derive_all,
    e10_series,
    e12_times_691_series,
    e14_series,
    e8_series,
    eisenstein_ring_closure_ladder,
    verify_691_E12_equals_441_E4cubed_plus_250_E6sq,
    verify_E10_equals_E4_E6,
    verify_E14_equals_E4_squared_E6,
    verify_E8_equals_E4_squared,
    verify_ramanujan_691_congruence,
)
from w33_ramanujan_system import (  # noqa: E402
    delta_series,
    e4_series,
    e6_series,
    series_mul,
)


# ----------------------------------------------------------------------
# E_8 = E_4^2.
# ----------------------------------------------------------------------
def test_E8_equals_E4_squared_holds():
    r = verify_E8_equals_E4_squared(n_max=25)
    assert r["all_match"] is True


def test_E8_q1_is_480():
    e8 = e8_series(3)
    assert e8[1] == 480


def test_E8_q2_is_61920():
    """sigma_7(2) = 1 + 128 = 129.  480 * 129 = 61920."""
    e8 = e8_series(3)
    assert e8[2] == 61920


def test_E8_q2_matches_E4_squared_at_q2():
    e4 = e4_series(3)
    e4_sq = series_mul(e4, e4, 3)
    assert e4_sq[2] == 61920


# ----------------------------------------------------------------------
# E_10 = E_4 * E_6.
# ----------------------------------------------------------------------
def test_E10_equals_E4_E6_holds():
    r = verify_E10_equals_E4_E6(n_max=25)
    assert r["all_match"] is True


def test_E10_q1_is_minus_264():
    e10 = e10_series(3)
    assert e10[1] == -264


def test_E10_q1_matches_E4_E6_at_q1():
    """E_4[1] + E_6[1] = 240 + (-504) = -264."""
    e4 = e4_series(3)
    e6 = e6_series(3)
    e4_e6 = series_mul(e4, e6, 3)
    assert e4_e6[1] == -264


# ----------------------------------------------------------------------
# E_14 = E_4^2 * E_6.
# ----------------------------------------------------------------------
def test_E14_equals_E4_squared_E6_holds():
    r = verify_E14_equals_E4_squared_E6(n_max=25)
    assert r["all_match"] is True


def test_E14_q1_is_minus_24():
    e14 = e14_series(3)
    assert e14[1] == -24


# ----------------------------------------------------------------------
# 691 * E_12 = 441 * E_4^3 + 250 * E_6^2.
# ----------------------------------------------------------------------
def test_691_E12_integer_identity_holds():
    r = verify_691_E12_equals_441_E4cubed_plus_250_E6sq(n_max=25)
    assert r["all_match"] is True


def test_691_E12_constant_term_is_691():
    lhs = e12_times_691_series(3)
    assert lhs[0] == 691


def test_441_plus_250_equals_691():
    """The two coefficients in the M_12 decomposition sum to 691."""
    assert 441 + 250 == 691


def test_691_E12_q1_coefficient():
    """691*E_12[1] = 65520*sigma_11(1) = 65520."""
    lhs = e12_times_691_series(3)
    assert lhs[1] == 65520


def test_441_E4cubed_plus_250_E6sq_at_q1_matches():
    """441*720 + 250*(-1008) = 317520 - 252000 = 65520."""
    e4 = e4_series(3)
    e6 = e6_series(3)
    e4_cubed = series_mul(series_mul(e4, e4, 3), e4, 3)
    e6_sq = series_mul(e6, e6, 3)
    value = 441 * e4_cubed[1] + 250 * e6_sq[1]
    assert value == 65520


# ----------------------------------------------------------------------
# Ramanujan's 691 congruence: tau(n) == sigma_11(n) (mod 691).
# ----------------------------------------------------------------------
def test_ramanujan_691_congruence_holds():
    r = verify_ramanujan_691_congruence(n_max=25)
    assert r["all_match"] is True
    assert r["discrepancies"] == []


def test_ramanujan_691_tau_2():
    """tau(2) = -24,  sigma_11(2) = 1 + 2048 = 2049,  2049 - (-24) = 2073 = 3*691."""
    delta = delta_series(5)
    assert delta[2] == -24
    sigma_11_2 = 1 + 2 ** 11
    assert sigma_11_2 == 2049
    assert (sigma_11_2 - delta[2]) % 691 == 0
    assert (sigma_11_2 - delta[2]) == 2073


def test_ramanujan_691_tau_3():
    """tau(3) = 252,  sigma_11(3) = 1 + 3^11 = 177148,
       177148 - 252 = 176896 = 691 * 256."""
    delta = delta_series(5)
    assert delta[3] == 252
    sigma_11_3 = 1 + 3 ** 11
    assert sigma_11_3 == 177148
    assert (sigma_11_3 - delta[3]) % 691 == 0


def test_ramanujan_691_tau_5():
    """tau(5) = 4830.  sigma_11(5) = 1 + 5^11 = 48828126.
       Both congruent mod 691 → difference divisible by 691."""
    delta = delta_series(7)
    assert delta[5] == 4830
    sigma_11_5 = 1 + 5 ** 11
    assert (sigma_11_5 - delta[5]) % 691 == 0


def test_ramanujan_691_tau_7():
    delta = delta_series(10)
    assert delta[7] == -16744
    sigma_11_7 = 1 + 7 ** 11
    assert (sigma_11_7 - delta[7]) % 691 == 0


# ----------------------------------------------------------------------
# Bernoulli and closure ladder signatures.
# ----------------------------------------------------------------------
def test_bernoulli_weight_12_has_denominator_691():
    b = bernoulli_weight_12_signature()
    assert b["E_12_coefficient_numerator"] == 65520
    assert b["E_12_coefficient_denominator"] == 691
    assert b["first_prime_of_ring_failure"] == 691


def test_closure_ladder_lists_first_failure_at_12():
    l = eisenstein_ring_closure_ladder()
    assert l["first_failure_at"] == 12
    assert l["first_failure_prime"] == 691


def test_closure_ladder_marks_monomial_weights():
    l = eisenstein_ring_closure_ladder()
    assert l["weight_8_monomial"]["E_8 = E_4^2"] is True
    assert l["weight_10_monomial"]["E_10 = E_4 * E_6"] is True
    assert l["weight_14_monomial"]["E_14 = E_4^2 * E_6"] is True


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_seven_pins():
    s = derive_all(n_max=20)
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"
