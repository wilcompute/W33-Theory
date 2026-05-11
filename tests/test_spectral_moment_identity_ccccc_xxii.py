#!/usr/bin/env python3
"""Tests for PART CCCCCXXII: Spectral Moment Identity."""
import math
from fractions import Fraction
import pytest

Q = 3; V = 40; K = 12; R = 2; S_ = -4; F = 24; G = 15
PHI3 = 13; PHI4 = 10; E = 240; DIM_E6 = 78; TR_A3 = 960


def test_master_equation():
    assert math.factorial(Q) == 2*Q


def test_spectral_moment_identity():
    """Tr(A^3)/Tr(A^2) = r = 2"""
    tr2 = 1*K**2 + F*R**2 + G*S_**2
    tr3 = 1*K**3 + F*R**3 + G*S_**3
    assert Fraction(tr3, tr2) == R


def test_algebraic_identity_proof():
    """k^2*(k-r) + g*s^2*(s-r) = 0"""
    assert K**2*(K-R) + G*S_**2*(S_-R) == 0


def test_master_equation_in_eigenvalues():
    """r - s = q! = 2q"""
    assert R - S_ == math.factorial(Q) == 2*Q


def test_zero_mode_perron():
    """D_F^2 zero modes = 2*(v+1) = 82"""
    zero_modes = 480 - 320 - 48 - 30
    assert zero_modes == 2*(V+1) == 82


def test_seeley_dewitt_a0_a2_a4():
    assert 4*320 + 10*48 + 16*30 == 2240
    assert 16*320 + 100*48 + 256*30 == 17600


def test_seeley_dewitt_a6_new():
    """NEW: a_6 = 191360"""
    a6 = 4**3*320 + 10**3*48 + 16**3*30
    assert a6 == 191360


def test_ihara_exponent():
    """Trivial zeros E-v = 200"""
    assert E - V == 200


def test_lambda_H():
    assert Fraction(PHI3, PHI4**2) == Fraction(13, 100)


def test_lambda_CKM():
    assert Fraction(Q**2, V) == Fraction(9, 40)


def test_sin2_theta12():
    assert Fraction(4, PHI3) == Fraction(4, 13)


def test_scalar_topology_cross_check():
    gap_ratio = Fraction(16, 10)
    lH = gap_ratio * Fraction(DIM_E6, TR_A3)
    assert lH == Fraction(13, 100)
