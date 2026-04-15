"""Pin the cyclotomic trigonometry derivation.

Verify that Phi_n(x) and T_n(x) are exactly what classical trigonometry
produces, that the primitive n-th roots of unity satisfy Phi_n(zeta) = 0,
and that every standard identity (Pythagorean, double-angle, angle
addition, Euler, hyperbolic) holds at machine precision.

Also verify the bridge to the W(3,3) master derivation: the Weinberg
identity sin^2 + cos^2 = 1 is the q=3 evaluation of the universal
cyclotomic identity q + Phi_4(q) = Phi_3(q).
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from math import pi
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_cyclotomic_trig import (  # noqa: E402
    chebyshev_T,
    chebyshev_U,
    cyclotomic,
    derive_all_trig,
    peval,
    verify_angle_addition,
    verify_chebyshev_T_matches_cos_nx,
    verify_cosh_is_cos_of_ix,
    verify_double_angle,
    verify_euler_identity,
    verify_hyperbolic_pythagorean,
    verify_primitive_root_satisfies_Phi_n,
    verify_pythagorean,
    weinberg_from_cyclotomics,
    _sym_numeric,
)


# ----------------------------------------------------------------------
# Cyclotomic polynomials Phi_n(x) for small n.
# ----------------------------------------------------------------------
EXPECTED_CYCLO = {
    1:  [-1, 1],
    2:  [1, 1],
    3:  [1, 1, 1],
    4:  [1, 0, 1],
    5:  [1, 1, 1, 1, 1],
    6:  [1, -1, 1],
    7:  [1, 1, 1, 1, 1, 1, 1],
    8:  [1, 0, 0, 0, 1],
    9:  [1, 0, 0, 1, 0, 0, 1],
    10: [1, -1, 1, -1, 1],
    11: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    12: [1, 0, -1, 0, 1],
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_CYCLO.items()))
def test_cyclotomic_polynomial_coefficients(n, expected):
    p = [int(c) for c in cyclotomic(n)]
    assert p == expected


def test_x_to_n_minus_1_factors_through_cyclotomics():
    """x^n - 1 = prod_{d | n} Phi_d(x). Verify by multiplying back out."""
    from w33_cyclotomic_trig import divisors, pmul, x_to_n_minus_1
    for n in range(1, 13):
        prod = [Fraction(1)]
        for d in divisors(n):
            prod = pmul(prod, cyclotomic(d))
        expect = x_to_n_minus_1(n)
        assert [Fraction(c) for c in prod] == [Fraction(c) for c in expect]


# ----------------------------------------------------------------------
# Chebyshev polynomials T_n(x) and U_n(x).
# ----------------------------------------------------------------------
EXPECTED_T = {
    0: [1],
    1: [0, 1],
    2: [-1, 0, 2],
    3: [0, -3, 0, 4],
    4: [1, 0, -8, 0, 8],
    5: [0, 5, 0, -20, 0, 16],
    6: [-1, 0, 18, 0, -48, 0, 32],
}
EXPECTED_U = {
    0: [1],
    1: [0, 2],
    2: [-1, 0, 4],
    3: [0, -4, 0, 8],
    4: [1, 0, -12, 0, 16],
}


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_T.items()))
def test_chebyshev_T_coefficients(n, expected):
    p = [int(c) for c in chebyshev_T(n)]
    assert p == expected


@pytest.mark.parametrize("n,expected", sorted(EXPECTED_U.items()))
def test_chebyshev_U_coefficients(n, expected):
    p = [int(c) for c in chebyshev_U(n)]
    assert p == expected


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 7, 8])
def test_chebyshev_T_n_matches_cos_nx(n):
    # Check at multiple angles
    for theta in (pi / 7, pi / 5, 1.1, 2.3):
        assert verify_chebyshev_T_matches_cos_nx(n, theta) < 1e-12


# ----------------------------------------------------------------------
# Primitive roots of unity: zeta_n = exp(2 pi i / n) satisfies Phi_n.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
def test_primitive_root_is_root_of_Phi_n(n):
    err = verify_primitive_root_satisfies_Phi_n(n)
    assert err < 1e-12


# ----------------------------------------------------------------------
# Special angles: (cos(2 pi / n), sin(2 pi / n)) exact values.
# ----------------------------------------------------------------------
SPECIAL_EXACT = {
    # n  :  (cos_str, sin_str)  --  radical expressions.
    3:  ("-1/2",              "sqrt(3)/2"),
    4:  ("0",                 "1"),
    6:  ("1/2",               "sqrt(3)/2"),
    8:  ("sqrt(2)/2",         "sqrt(2)/2"),
    12: ("sqrt(3)/2",         "1/2"),
}


@pytest.mark.parametrize("n,cos_s,sin_s", [(k, v[0], v[1]) for k, v in SPECIAL_EXACT.items()])
def test_special_angle_exact_matches_numeric(n, cos_s, sin_s):
    c_sym = _sym_numeric(cos_s)
    s_sym = _sym_numeric(sin_s)
    c_tru = math.cos(2 * pi / n)
    s_tru = math.sin(2 * pi / n)
    assert abs(c_sym - c_tru) < 1e-12
    assert abs(s_sym - s_tru) < 1e-12


def test_cos_pi_over_5_golden_ratio():
    """cos(2 pi / 5) = (sqrt(5) - 1) / 4 = (phi - 1) / 2 where phi is the golden ratio."""
    phi = (1 + math.sqrt(5)) / 2
    lhs = math.cos(2 * pi / 5)
    rhs = (phi - 1) / 2
    assert abs(lhs - rhs) < 1e-12


# ----------------------------------------------------------------------
# Pythagorean identity  cos^2 + sin^2 = 1.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("theta", [k * pi / 7 for k in range(1, 7)] + [0.3, 1.23, 2.71])
def test_pythagorean_identity(theta):
    assert verify_pythagorean(theta) < 1e-14


# ----------------------------------------------------------------------
# Double-angle identities.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("theta", [k * pi / 9 for k in range(1, 6)])
def test_double_angle_cos_and_sin(theta):
    r = verify_double_angle(theta)
    assert r["cos2x_minus_identity"] < 1e-14
    assert r["sin2x_minus_identity"] < 1e-14


# ----------------------------------------------------------------------
# Angle addition formulas.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("a,b", [(pi / 5, pi / 7), (pi / 3, pi / 4),
                                 (pi / 6, pi / 12), (0.7, 1.3)])
def test_angle_addition(a, b):
    r = verify_angle_addition(a, b)
    assert r["cos_sum"] < 1e-14
    assert r["sin_sum"] < 1e-14


# ----------------------------------------------------------------------
# Euler's identity  e^(i pi) + 1 = 0.
# ----------------------------------------------------------------------
def test_euler_identity():
    assert verify_euler_identity() < 1e-12


# ----------------------------------------------------------------------
# Hyperbolic:  cosh^2 - sinh^2 = 1,  cosh(x) = cos(i x).
# ----------------------------------------------------------------------
@pytest.mark.parametrize("x", [0.1, 0.5, 1.0, 2.0, 3.14])
def test_hyperbolic_pythagorean(x):
    assert verify_hyperbolic_pythagorean(x) < 1e-12


@pytest.mark.parametrize("x", [0.1, 0.5, 1.0, 2.0])
def test_cosh_is_cos_of_imaginary_argument(x):
    assert verify_cosh_is_cos_of_ix(x) < 1e-12


# ----------------------------------------------------------------------
# Phi_n(3): cyclotomic slots at q=3 match master-derivation denominators.
# ----------------------------------------------------------------------
EXPECTED_PHI_AT_3 = {
    1: 2, 2: 4, 3: 13, 4: 10, 5: 121, 6: 7, 7: 1093,
    8: 82, 9: 757, 10: 61, 11: 88573, 12: 73,
}


@pytest.mark.parametrize("n,val", sorted(EXPECTED_PHI_AT_3.items()))
def test_phi_n_at_q_is_3(n, val):
    assert int(peval(cyclotomic(n), 3)) == val


# ----------------------------------------------------------------------
# Weinberg closure as the q=3 image of the universal cyclotomic identity.
# ----------------------------------------------------------------------
def test_weinberg_from_cyclotomic_at_q_three():
    w = weinberg_from_cyclotomics(q=3)
    assert w["Phi_3(q)"] == 13
    assert w["Phi_4(q)"] == 10
    assert w["Phi_6(q)"] == 7
    assert w["sin2_theta_W"] == "3/13"
    assert w["cos2_theta_W"] == "10/13"
    assert w["sum_equals_one"] is True


def test_cyclotomic_identity_q_plus_phi4_equals_phi3():
    """The algebraic root of the Weinberg identity:
         q + Phi_4(q) = q + (q^2 + 1) = q^2 + q + 1 = Phi_3(q).
    Holds for every integer q, not just q=3."""
    for q in range(-5, 10):
        assert q + int(peval(cyclotomic(4), q)) == int(peval(cyclotomic(3), q))


# ----------------------------------------------------------------------
# Aggregate driver.
# ----------------------------------------------------------------------
def test_derive_all_trig_completes():
    chain = derive_all_trig()
    assert chain["weinberg_closure"]["sum_equals_one"] is True
    assert chain["phi_at_q=3"][3] == 13
    assert chain["phi_at_q=3"][4] == 10
    assert chain["phi_at_q=3"][6] == 7
    # All numerical identity residuals below 1e-10.
    idn = chain["identities_numerical"]
    assert max(idn["pythagorean"]) < 1e-10
    assert idn["euler_pi"] < 1e-10
    assert max(idn["hyperbolic_pyth"]) < 1e-10
