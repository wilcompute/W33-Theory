"""Regression tests for Part CCCCCXXIII: Moment-Ratio Scalar Action."""
from fractions import Fraction
import math


def atoms():
    q = 3
    lam = 2
    mu = 4
    k = q * (q + 1)
    v = (q + 1) * (q*q + 1)
    E = v * k // 2
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1
    return q, lam, mu, k, v, E, r, s, f, g, phi3, phi4, phi6


def test_master_equation():
    q, *_ = atoms()
    assert math.factorial(q) == 2*q == 6


def test_spectral_moment_identity():
    q, lam, mu, k, v, E, r, s, f, g, phi3, phi4, phi6 = atoms()
    tr_a2 = k*k + f*r*r + g*s*s
    tr_a3 = k**3 + f*r**3 + g*s**3
    assert tr_a2 == 480
    assert tr_a3 == 960
    assert Fraction(tr_a3, tr_a2) == r == 2


def test_scalar_action_forms_agree():
    q, lam, mu, k, v, E, r, s, f, g, phi3, phi4, phi6 = atoms()
    delta_r = k-r
    delta_s = k-s
    gap_ratio = Fraction(delta_s, delta_r)
    tr_a2 = k*k + f*r*r + g*s*s
    tr_a3 = k**3 + f*r**3 + g*s**3
    dim_e6 = lam*q*phi3

    lambda_triangle = gap_ratio * Fraction(dim_e6, tr_a3)
    lambda_moment = gap_ratio * Fraction(dim_e6, r*tr_a2)
    lambda_cyclotomic = Fraction(phi3, phi4*phi4)
    assert lambda_triangle == lambda_moment == lambda_cyclotomic == Fraction(13, 100)


def test_inverse_action_forms_agree():
    q, lam, mu, k, v, E, r, s, f, g, phi3, phi4, phi6 = atoms()
    delta_r = k-r
    delta_s = k-s
    gap_ratio = Fraction(delta_s, delta_r)
    tr_a2 = k*k + f*r*r + g*s*s
    dim_e6 = lam*q*phi3
    lambda_inv = Fraction(r*tr_a2, 1) / (gap_ratio * dim_e6)
    assert lambda_inv == Fraction(phi4*phi4, phi3) == Fraction(100, 13)


def test_descendants_preserved():
    q, lam, mu, k, v, E, r, s, f, g, phi3, phi4, phi6 = atoms()
    lambda_h = Fraction(13, 100)
    a_ckm = Fraction(q**4, phi3) * lambda_h
    theta13 = Fraction(q*q, lam*lam*phi3) * lambda_h

    d_t = v + 1
    d_b = q*d_t + lam
    d_c = d_b + k
    y_b = Fraction(q, d_b)
    y_c = Fraction(1, d_c)
    y_tau = lambda_h * y_b*y_b / y_c

    assert (a_ckm, theta13, y_tau) == (Fraction(81,100), Fraction(9,400), Fraction(16029,1562500))
    assert (d_t, d_b, d_c, y_b, y_c) == (41, 125, 137, Fraction(3,125), Fraction(1,137))


def test_latest_commit_consistency_values():
    q, lam, mu, k, v, E, r, s, f, g, phi3, phi4, phi6 = atoms()
    zero_modes = 2*E - 320 - 48 - 30
    a6 = 4**3 * 320 + 10**3 * 48 + 16**3 * 30
    assert zero_modes == 2*(v+1) == 82
    assert a6 == 191360
    assert E - v == 200
