"""Pin Jacobi's eight-squares theorem.

Tests cover:
    (1) theta_3(q)^8 coefficients match r_8(n) from brute-force
        enumeration of Z^8 lattice points of squared norm n (n up to 5);
    (2) Jacobi formula r_8(n) = 16 sigma_3^*(n)  for  n up to 39;
    (3) specific small values: r_8(1)=16, r_8(2)=112, ..., r_8(8)=9328;
    (4) sigma_3^*(n) divisor formula for n up to 6;
    (5) r_8(n) > 0 for 1 <= n <= 59 (the 4-sq Lagrange result extends);
    (6) contrast with E_8 theta: 112 Z^8 + 128 half-integer = 240 E_8.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_eight_squares import (  # noqa: E402
    compare_r8_to_e8_theta,
    derive_all,
    r8_brute_force,
    r8_formula,
    sigma_3_star,
    theta3_eighth,
    theta3_sixth,
    verify_jacobi_eight_squares,
    verify_r8_always_positive,
    verify_r8_brute_force_small,
    verify_sigma_3_star_small,
    verify_specific_small_values,
)


# ----------------------------------------------------------------------
# theta_3^8 basic values.
# ----------------------------------------------------------------------
def test_theta3_eighth_q0_is_1():
    assert theta3_eighth(1)[0] == 1


def test_r8_of_1_is_16():
    assert theta3_eighth(2)[1] == 16


def test_r8_of_2_is_112():
    """2 = sum of 2 signed unit squares in 8 positions: C(8,2)*2^2 = 112."""
    t = theta3_eighth(3)
    assert t[2] == 112


def test_r8_of_3_is_448():
    assert theta3_eighth(4)[3] == 448


def test_r8_of_4_is_1136():
    assert theta3_eighth(5)[4] == 1136


# ----------------------------------------------------------------------
# Jacobi divisor formula.
# ----------------------------------------------------------------------
def test_sigma_3_star_of_1_is_1():
    assert sigma_3_star(1) == 1


def test_sigma_3_star_of_2_is_7():
    """d=1: (-1)^{2-1}*1 = -1; d=2: (-1)^0 * 8 = 8. Sum = 7."""
    assert sigma_3_star(2) == 7


def test_sigma_3_star_of_4_is_71():
    """d=1: -1; d=2: 8; d=4: 64. Sum = 71."""
    assert sigma_3_star(4) == 71


def test_r8_formula_matches_16_sigma():
    for n in range(1, 20):
        assert r8_formula(n) == 16 * sigma_3_star(n)


def test_verify_jacobi_eight_squares_up_to_40():
    r = verify_jacobi_eight_squares(N=40)
    assert r["all_match"] is True


def test_sigma_3_star_small_all_match():
    r = verify_sigma_3_star_small()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Brute-force enumeration sanity.
# ----------------------------------------------------------------------
def test_brute_force_matches_theta_for_small_n():
    r = verify_r8_brute_force_small(up_to=4)
    assert r["all_match"] is True


def test_r8_brute_of_1_is_16():
    assert r8_brute_force(1) == 16


def test_r8_brute_of_2_is_112():
    assert r8_brute_force(2) == 112


# ----------------------------------------------------------------------
# Specific values table.
# ----------------------------------------------------------------------
def test_specific_small_values_all_match():
    r = verify_specific_small_values()
    assert r["all_match"] is True


def test_r8_of_8_is_9328():
    assert theta3_eighth(9)[8] == 9328


# ----------------------------------------------------------------------
# Positivity (every n >= 1 is sum of 8 squares with multiplicity).
# ----------------------------------------------------------------------
def test_r8_positive_for_all_n_in_range():
    r = verify_r8_always_positive(N=60)
    assert r["no_zero_values"] is True


# ----------------------------------------------------------------------
# Contrast with E_8 lattice.
# ----------------------------------------------------------------------
def test_Z8_norm_2_plus_half_integer_equals_E8_240():
    r = compare_r8_to_e8_theta()
    assert r["Z8_norm_2_count_r8_of_2"] == 112
    assert r["E8_norm_2_count_E4_q1_coeff"] == 240
    assert r["gap_half_integer_coset"] == 128
    assert r["matches_128_equals_2_to_7"] is True
    assert 128 == 2 ** 7


def test_Z8_112_equals_C82_times_4():
    """112 = C(8,2) * 2^2 (choose 2 positions, 4 sign patterns)."""
    assert 112 == 28 * 4


# ----------------------------------------------------------------------
# theta_3^6 sanity (6-squares leading coefficients).
# ----------------------------------------------------------------------
def test_theta3_sixth_q0_is_1():
    assert theta3_sixth(1)[0] == 1


def test_theta3_sixth_first_few():
    """theta_3^6 first few: 1, 12, 60, 160, 252, 312, ..."""
    t = theta3_sixth(6)
    assert t[0] == 1
    assert t[1] == 12
    assert t[2] == 60


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_subresults():
    s = derive_all()
    for key in [
        "jacobi_eight_squares",
        "brute_force",
        "specific_values",
        "sigma_3_star",
        "positivity",
        "e8_gap",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_six_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 6
