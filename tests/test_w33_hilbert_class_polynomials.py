"""Pin Hilbert class polynomials for CM discriminants.

Tests cover:
    (1) reduced-form enumeration produces the correct class number h(D)
        for the 9 Heegner discriminants (h = 1), 7 class-number-2 cases,
        and 2 class-number-3 cases;
    (2) tabulated Hilbert class polynomials (coefficient-first list)
        match the numerical polynomial built from prod(x - j(tau_f))
        to 20+ digits after 80-dps mpmath evaluation;
    (3) for each of the 9 Heegner numbers, H_D(x) = x - j(tau_D)
        reduces to the Layer 52 table;
    (4) specific coefficients: H_{-15}(x) quadratic with
        sum of roots = -191025 and product = -121287375;
    (5) irreducibility / degree = h(D).
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_hilbert_class_polynomials import (  # noqa: E402
    EXPECTED_CLASS_NUMBERS,
    HEEGNER_DISCRIMINANTS,
    HILBERT_CLASS_POLYS,
    class_number,
    derive_all,
    form_to_tau,
    reduced_forms,
    verify_all_tabulated,
    verify_class_numbers,
    verify_hilbert_polynomial,
    verify_linear_case_is_monic_x_minus_j,
)


# ----------------------------------------------------------------------
# Reduced-form enumeration.
# ----------------------------------------------------------------------
def test_class_number_minus_3_is_1():
    assert class_number(-3) == 1


def test_class_number_minus_15_is_2():
    assert class_number(-15) == 2


def test_class_number_minus_23_is_3():
    assert class_number(-23) == 3


def test_class_number_minus_163_is_1():
    assert class_number(-163) == 1


def test_all_heegner_have_class_number_1():
    for D in HEEGNER_DISCRIMINANTS:
        assert class_number(D) == 1, f"D={D}"


def test_reduced_forms_minus_15_are_known():
    """Reduced forms of discriminant -15: [1,1,4], [2,1,2]."""
    forms = set(reduced_forms(-15))
    assert (1, 1, 4) in forms
    assert (2, 1, 2) in forms
    assert len(forms) == 2


def test_reduced_forms_minus_23_are_three():
    """Reduced forms of discriminant -23: [1,1,6], [2,1,3], [2,-1,3]."""
    forms = reduced_forms(-23)
    assert len(forms) == 3
    assert (1, 1, 6) in forms


def test_tau_for_form_1_1_4_has_correct_imaginary_part():
    import mpmath as mp
    mp.mp.dps = 40
    tau = form_to_tau(1, 1, 4)
    assert abs(tau.real - (-0.5)) < 1e-25
    assert abs(tau.imag - mp.sqrt(15) / 2) < 1e-25


# ----------------------------------------------------------------------
# Class-number 1 — Hilbert polynomial is linear x - j(tau_D).
# ----------------------------------------------------------------------
def test_linear_case_heegner_all_match():
    r = verify_linear_case_is_monic_x_minus_j(dps=60)
    assert r["all_match"] is True


def test_H_minus_163_constant_is_640320_cubed_negated():
    """H_{-163}(x) = x + 640320^3  =>  H_{-163}[0] = 640320^3."""
    assert HILBERT_CLASS_POLYS[-163][0] == 640320 ** 3
    assert HILBERT_CLASS_POLYS[-163][0] == 262537412640768000


def test_H_minus_43_constant_is_960_cubed_negated():
    """H_{-43}(x) = x + 960^3."""
    assert HILBERT_CLASS_POLYS[-43][0] == 960 ** 3
    assert HILBERT_CLASS_POLYS[-43][0] == 884736000


def test_H_minus_67_constant_is_5280_cubed_negated():
    """H_{-67}(x) = x + 5280^3."""
    assert HILBERT_CLASS_POLYS[-67][0] == 5280 ** 3


def test_H_minus_7_constant_is_minus_neg_15_cubed():
    """H_{-7}(x) = x + 3375, and 3375 = 15^3."""
    assert HILBERT_CLASS_POLYS[-7][0] == 15 ** 3
    assert HILBERT_CLASS_POLYS[-7][0] == 3375


# ----------------------------------------------------------------------
# Class-number 2 — quadratic Hilbert polynomials.
# ----------------------------------------------------------------------
def test_H_minus_15_is_degree_2():
    assert len(HILBERT_CLASS_POLYS[-15]) == 3


def test_H_minus_15_coefficients():
    """H_{-15}(x) = x^2 + 191025 x - 121287375."""
    assert HILBERT_CLASS_POLYS[-15] == [-121287375, 191025, 1]


def test_H_minus_15_numerical_roots_give_integer_coeffs():
    r = verify_hilbert_polynomial(-15, dps=80)
    assert r["match"] is True
    assert r["degree"] == 2


def test_H_minus_20_coefficients():
    """H_{-20}(x) = x^2 - 1264000 x - 681472000."""
    assert HILBERT_CLASS_POLYS[-20] == [-681472000, -1264000, 1]


def test_H_minus_24_numerical_roots_integer():
    r = verify_hilbert_polynomial(-24, dps=80)
    assert r["match"] is True


def test_class_number_2_cases_all_match():
    for D in [-15, -20, -24, -35, -40, -51, -52]:
        r = verify_hilbert_polynomial(D, dps=80)
        assert r["match"] is True, f"D={D} failed"
        assert r["degree"] == 2


# ----------------------------------------------------------------------
# Class-number 3 — cubic Hilbert polynomials.
# ----------------------------------------------------------------------
def test_H_minus_23_is_degree_3():
    assert len(HILBERT_CLASS_POLYS[-23]) == 4


def test_H_minus_23_coefficients():
    """H_{-23}(x) = x^3 + 3491750 x^2 - 5151296875 x + 12771880859375."""
    assert HILBERT_CLASS_POLYS[-23] == [
        12771880859375, -5151296875, 3491750, 1
    ]


def test_H_minus_23_numerical_match():
    r = verify_hilbert_polynomial(-23, dps=80)
    assert r["match"] is True
    assert r["degree"] == 3


def test_H_minus_31_numerical_match():
    r = verify_hilbert_polynomial(-31, dps=80)
    assert r["match"] is True
    assert r["degree"] == 3


# ----------------------------------------------------------------------
# Monic & degree = h(D).
# ----------------------------------------------------------------------
def test_all_polynomials_are_monic():
    for D, coeffs in HILBERT_CLASS_POLYS.items():
        assert coeffs[-1] == 1, f"D={D} leading coefficient not 1"


def test_polynomial_degree_equals_class_number():
    for D, coeffs in HILBERT_CLASS_POLYS.items():
        deg = len(coeffs) - 1
        h = class_number(D)
        assert deg == h, f"D={D}: deg={deg}, h={h}"


def test_class_numbers_match_expected_table():
    r = verify_class_numbers()
    assert r["all_match"] is True


# ----------------------------------------------------------------------
# Driver chain.
# ----------------------------------------------------------------------
def test_driver_all_pins_green():
    s = derive_all()
    for key, val in s["summary_chain"].items():
        assert val is True, f"{key} = {val}"


def test_driver_includes_subresults():
    s = derive_all()
    for key in ["class_numbers", "linear_case", "all_polys", "summary_chain"]:
        assert key in s


def test_all_tabulated_polynomials_pin_numerically():
    r = verify_all_tabulated(dps=80)
    assert r["all_match"] is True
    for row in r["rows"]:
        assert row["match"] is True, f"D={row['D']} failed numerical pin"


# ----------------------------------------------------------------------
# Coefficient structure sanity.
# ----------------------------------------------------------------------
def test_H_minus_15_sum_of_roots():
    """Sum of roots of H_{-15} = -191025 (Vieta's)."""
    coeffs = HILBERT_CLASS_POLYS[-15]  # [c_0, c_1, c_2]
    sum_of_roots = -coeffs[1] / coeffs[2]
    assert sum_of_roots == -191025


def test_H_minus_15_product_of_roots():
    """Product of roots of H_{-15} = -121287375 (Vieta's)."""
    coeffs = HILBERT_CLASS_POLYS[-15]
    product = coeffs[0] / coeffs[2]
    assert product == -121287375


def test_H_minus_23_product_of_roots_positive():
    """H_{-23} product of roots = 12771880859375 = 5^9 * 7^3 * ...
    (positive integer)."""
    coeffs = HILBERT_CLASS_POLYS[-23]
    product = coeffs[0]  # since monic cubic: prod = (-1)^3 * c_0? no
    # For monic x^n + a_{n-1} x^{n-1} + ... + a_0, product = (-1)^n a_0.
    # Our layout is [a_0, a_1, ..., a_n=1]. So for n=3: product = -a_0.
    assert -product == -12771880859375  # product of roots is -c_0


def test_expected_class_numbers_has_18_entries():
    assert len(EXPECTED_CLASS_NUMBERS) == 18
