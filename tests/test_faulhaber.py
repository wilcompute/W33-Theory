"""Pin Faulhaber's formula:  sum_{k=1}^N k^p  as exact polynomial in N.

The coefficients come from Bernoulli numbers via

    S_p(N)  =  (1/(p+1))  sum_{j=0}^p  C(p+1, j)  B_j^+  N^(p+1-j)

with  B_1^+ = +1/2  (Faulhaber / "plus" convention).  Faulhaber's theorem
says for odd  p  that  S_p(N)  is a polynomial in  u = N(N+1)  of degree
(p+1)/2, generalizing  S_3(N) = S_1(N)^2 = (u/2)^2.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "exploration"))

from w33_faulhaber import (  # noqa: E402
    bernoulli_plus,
    derive_all_faulhaber,
    faulhaber_in_u,
    faulhaber_poly,
    peval,
    power_sum_direct,
    srg_faulhaber_closures,
)


# ----------------------------------------------------------------------
# Faulhaber polynomials for p = 0 .. 8.
# ----------------------------------------------------------------------
EXPECTED_POLYS = {
    0: [0, 1],                                              # N
    1: [0, Fraction(1, 2), Fraction(1, 2)],                 # N(N+1)/2
    2: [0, Fraction(1, 6), Fraction(1, 2), Fraction(1, 3)], # N(N+1)(2N+1)/6
    3: [0, 0, Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)],
    4: [0, Fraction(-1, 30), 0, Fraction(1, 3), Fraction(1, 2), Fraction(1, 5)],
    5: [0, 0, Fraction(-1, 12), 0, Fraction(5, 12), Fraction(1, 2), Fraction(1, 6)],
    6: [0, Fraction(1, 42), 0, Fraction(-1, 6), 0, Fraction(1, 2), Fraction(1, 2), Fraction(1, 7)],
}


@pytest.mark.parametrize("p,expected", sorted(EXPECTED_POLYS.items()))
def test_faulhaber_polynomial_coefficients(p, expected):
    S = faulhaber_poly(p)
    assert [Fraction(c) for c in S] == [Fraction(c) for c in expected]


# ----------------------------------------------------------------------
# Direct verification against sum_{k=1}^N k^p.
# ----------------------------------------------------------------------
@pytest.mark.parametrize("p", range(0, 8))
@pytest.mark.parametrize("N", [1, 2, 5, 10, 50, 100])
def test_faulhaber_matches_direct_sum(p, N):
    S = faulhaber_poly(p)
    assert int(peval(S, N)) == power_sum_direct(N, p)


# ----------------------------------------------------------------------
# Sum-of-cubes identity:  S_3(N) = S_1(N)^2.
# ----------------------------------------------------------------------
def test_sum_of_cubes_equals_square_of_sum():
    S1 = faulhaber_poly(1)
    S3 = faulhaber_poly(3)
    # compute S_1(N)^2 as polynomial
    S1_sq = [Fraction(0)] * (2 * len(S1) - 1)
    for i, a in enumerate(S1):
        for j, b in enumerate(S1):
            S1_sq[i + j] += a * b
    while len(S1_sq) > 1 and S1_sq[-1] == 0:
        S1_sq.pop()
    assert S3 == S1_sq


# ----------------------------------------------------------------------
# Faulhaber's theorem: for odd p, S_p(N) is a polynomial in u = N(N+1).
# ----------------------------------------------------------------------
@pytest.mark.parametrize("p", [1, 3, 5, 7, 9])
def test_faulhaber_odd_is_polynomial_in_u(p):
    in_u = faulhaber_in_u(p)
    # Verify by evaluating at several N.
    S = faulhaber_poly(p)
    for N in (1, 3, 7, 20, 50):
        u = N * (N + 1)
        lhs = peval(S, N)
        rhs = Fraction(0)
        for k, c in enumerate(in_u):
            rhs += c * Fraction(u) ** k
        assert lhs == rhs


def test_S_1_in_u_is_half_u():
    # S_1(N) = u / 2
    assert faulhaber_in_u(1) == [Fraction(0), Fraction(1, 2)]


def test_S_3_in_u_is_u_squared_over_four():
    # S_3(N) = u^2 / 4
    assert faulhaber_in_u(3) == [Fraction(0), Fraction(0), Fraction(1, 4)]


# ----------------------------------------------------------------------
# Euler-Maclaurin leading terms:
#       S_p(N) = N^{p+1}/(p+1) + N^p/2 + (Bernoulli corrections).
# ----------------------------------------------------------------------
@pytest.mark.parametrize("p", range(1, 8))
def test_leading_coefficient_is_1_over_p_plus_1(p):
    S = faulhaber_poly(p)
    assert S[p + 1] == Fraction(1, p + 1)


@pytest.mark.parametrize("p", range(1, 8))
def test_subleading_coefficient_is_one_half(p):
    S = faulhaber_poly(p)
    assert S[p] == Fraction(1, 2)


# ----------------------------------------------------------------------
# SRG Faulhaber closures:  S_p(v), S_p(k), S_p(mu), S_p(nn).
# ----------------------------------------------------------------------
EXPECTED_SRG = {
    "S_0": {"S_p(v=40)": 40, "S_p(k=12)": 12, "S_p(mu=4)": 4, "S_p(nn=27)": 27},
    "S_1": {"S_p(v=40)": 820, "S_p(k=12)": 78, "S_p(mu=4)": 10, "S_p(nn=27)": 378},
    "S_2": {"S_p(v=40)": 22140, "S_p(k=12)": 650, "S_p(mu=4)": 30, "S_p(nn=27)": 6930},
    "S_3": {"S_p(v=40)": 672400, "S_p(k=12)": 6084, "S_p(mu=4)": 100, "S_p(nn=27)": 142884},
}


@pytest.mark.parametrize("p,vals", sorted(EXPECTED_SRG.items()))
def test_srg_faulhaber_closures(p, vals):
    all_closures = srg_faulhaber_closures()
    assert all_closures[p] == vals


def test_S_3_v_equals_S_1_v_squared():
    # S_3(40) = 820^2 = 672400
    assert 820 ** 2 == 672400
    closures = srg_faulhaber_closures()
    assert closures["S_3"]["S_p(v=40)"] == closures["S_1"]["S_p(v=40)"] ** 2


def test_S_2_v_is_22140():
    # Square-pyramidal number on v=40:  40 * 41 * 81 / 6 = 22140.
    assert srg_faulhaber_closures()["S_2"]["S_p(v=40)"] == 22140


def test_S_1_v_is_triangular_820():
    # Triangular number T_40 = 40 * 41 / 2 = 820.
    assert srg_faulhaber_closures()["S_1"]["S_p(v=40)"] == 820


# ----------------------------------------------------------------------
# Bernoulli-plus convention:  B_1^+ = +1/2, all other B_j^+ = B_j.
# ----------------------------------------------------------------------
def test_bernoulli_plus_flips_B_1_only():
    from w33_bernoulli_zeta import bernoulli
    assert bernoulli_plus(0) == bernoulli(0)
    assert bernoulli_plus(1) == Fraction(1, 2)
    assert bernoulli(1) == Fraction(-1, 2)
    for n in range(2, 10):
        assert bernoulli_plus(n) == bernoulli(n)


# ----------------------------------------------------------------------
# Full driver.
# ----------------------------------------------------------------------
def test_derive_all_faulhaber_consistency():
    chain = derive_all_faulhaber(max_p=6)
    assert chain["sum_of_cubes_equals_square_of_sum"] is True
    # Every direct verification entry matches.
    for rec in chain["direct_verification"]:
        assert rec["ok"] is True
    # Leading coefficient of S_p is 1/(p+1).
    em = chain["euler_maclaurin_leading_terms"]
    for p_key, rec in em.items():
        assert rec["leading_ok"] is True
        assert rec["subleading_ok"] is True
