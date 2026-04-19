"""Pin Eisenstein series E_k and the identity E_4^3 - E_6^2 = 1728 Delta.

Tests cover:
    (1) E_4 = 1 + 240 q + 2160 q^2 + ...  (240 sigma_3(n) coefficients);
    (2) E_6 = 1 - 504 q - 16632 q^2 - ... (-504 sigma_5(n));
    (3) E_4^2 = E_8 on q-series up to q^20;
    (4) E_4 E_6 = E_10 on q-series up to q^20;
    (5) E_4^3 - E_6^2 = 1728 Delta on q-series up to q^20;
    (6) Delta = q - 24 q^2 + 252 q^3 - 1472 q^4 + 4830 q^5 - ...;
    (7) E_12 q-coefficient = 65520/691 (the 691 locus);
    (8) Bernoulli-based coefficient table matches 240/-504/480/-264/65520/-24.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_eisenstein_delta_identity import (  # noqa: E402
    delta_q_series,
    derive_all,
    eisenstein_q_series,
    series_mul,
    series_sub,
    sigma_k,
    verify_delta_first_coefficients,
    verify_E12_leading_coefficient_is_65520_over_691,
    verify_E4_coeff_formula_via_bernoulli,
    verify_E4_cubed_minus_E6_squared_is_1728_delta,
    verify_E4_E6_equals_E10,
    verify_E4_leading,
    verify_E4_squared_equals_E8,
    verify_E6_leading,
)


# ----------------------------------------------------------------------
# sigma_k helper.
# ----------------------------------------------------------------------
def test_sigma_3_of_6_is_252():
    """sigma_3(6) = 1 + 8 + 27 + 216 = 252."""
    assert sigma_k(6, 3) == 252


def test_sigma_5_of_1_is_1():
    assert sigma_k(1, 5) == 1


def test_sigma_11_of_2_is_2049():
    """sigma_11(2) = 1 + 2^11 = 1 + 2048 = 2049."""
    assert sigma_k(2, 11) == 2049


# ----------------------------------------------------------------------
# Eisenstein leading coefficients.
# ----------------------------------------------------------------------
def test_E4_constant_term_is_1():
    E4 = eisenstein_q_series(2, 2)
    assert E4[0] == Fraction(1)


def test_E4_q_coefficient_is_240():
    E4 = eisenstein_q_series(2, 2)
    assert E4[1] == Fraction(240)


def test_E6_constant_term_is_1():
    E6 = eisenstein_q_series(3, 2)
    assert E6[0] == Fraction(1)


def test_E6_q_coefficient_is_minus_504():
    E6 = eisenstein_q_series(3, 2)
    assert E6[1] == Fraction(-504)


def test_E4_leading_verifier():
    r = verify_E4_leading()
    assert r["all_match"] is True


def test_E6_leading_verifier():
    r = verify_E6_leading()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Dimension-1 identities E_4^2 = E_8, E_4 E_6 = E_10.
# ----------------------------------------------------------------------
def test_E4_squared_equals_E8():
    r = verify_E4_squared_equals_E8(N=20)
    assert r["all_match"] is True


def test_E4_times_E6_equals_E10():
    r = verify_E4_E6_equals_E10(N=20)
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# E_4^3 - E_6^2 = 1728 Delta.
# ----------------------------------------------------------------------
def test_cubic_identity_up_to_q20():
    r = verify_E4_cubed_minus_E6_squared_is_1728_delta(N=20)
    assert r["all_match"] is True


def test_cubic_identity_leading_terms():
    """At q^1, E_4^3 - E_6^2 starts 1728 q + O(q^2)."""
    N = 5
    E4 = eisenstein_q_series(2, N)
    E6 = eisenstein_q_series(3, N)
    E4_cubed = series_mul(E4, series_mul(E4, E4, N), N)
    E6_squared = series_mul(E6, E6, N)
    diff = series_sub(E4_cubed, E6_squared, N)
    assert diff[0] == Fraction(0)
    assert diff[1] == Fraction(1728)  # = 1728 * tau(1)


# ----------------------------------------------------------------------
# Delta coefficients.
# ----------------------------------------------------------------------
def test_delta_q_coefficient_is_1():
    d = delta_q_series(2)
    assert d[1] == Fraction(1)


def test_tau_of_2_is_minus_24():
    d = delta_q_series(3)
    assert d[2] == Fraction(-24)


def test_tau_of_3_is_252():
    d = delta_q_series(4)
    assert d[3] == Fraction(252)


def test_tau_of_5_is_4830():
    d = delta_q_series(6)
    assert d[5] == Fraction(4830)


def test_delta_first_coefficients_verifier():
    r = verify_delta_first_coefficients()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# E_12 and 691.
# ----------------------------------------------------------------------
def test_E12_q_coefficient_is_65520_over_691():
    E12 = eisenstein_q_series(6, 2)
    assert E12[1] == Fraction(65520, 691)


def test_E12_verifier():
    r = verify_E12_leading_coefficient_is_65520_over_691()
    assert r["all_match"] is True


def test_E12_q2_is_65520_over_691_times_2049():
    """sigma_11(2) = 2049 -- so q^2 coeff = (65520/691) * 2049."""
    E12 = eisenstein_q_series(6, 3)
    assert E12[2] == Fraction(65520, 691) * Fraction(2049)


# ----------------------------------------------------------------------
# Coefficient table -4k/B_{2k}.
# ----------------------------------------------------------------------
def test_coefficient_table():
    r = verify_E4_coeff_formula_via_bernoulli()
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
        "E4_leading",
        "E6_leading",
        "E4_squared_equals_E8",
        "E4_E6_equals_E10",
        "cubic_identity",
        "delta_coefficients",
        "E12_coefficient",
        "coefficient_table",
        "summary_chain",
    ]:
        assert key in s


def test_summary_chain_has_eight_pins():
    s = derive_all()
    assert len(s["summary_chain"]) == 8
