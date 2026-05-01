"""
Phase CCXLI: Hashimoto-Weil bridge via closed walk spectrum.

The Hashimoto (non-backtracking) eigenvalues of W(3,3) are:
  ev=r=2:  lambda = 1 +/- i*sqrt(Phi4),  |lambda| = sqrt(k-1) = sqrt(11)
  ev=s=-4: lambda = -2 +/- i*sqrt(Phi6), |lambda| = sqrt(k-1) = sqrt(11)

The imaginary parts are exactly sqrt(Phi4) and sqrt(Phi6).

Closed walk formula: Tr(A^n) = k^n + r^n*f + s^n*g.
Ihara zeta prefactor: (1-u^2)^{E-v} = (1-u^2)^{200}.
Weil-Ihara substitution: u = q^{-s} with q^s = sqrt(k-1).
"""

from fractions import Fraction
from itertools import product as iproduct
from math import atan2, comb, log, pi, sqrt

import numpy as np
import pytest

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f, g = 24, 15
s_param = k // l
N = comb(s_param, q)
E = k * v // 2
r_eig, s_eig = 2, -4
PI_val = float(pi)


class TestHashimotoWeilBridge:

    def test_hashimoto_r_real_part(self):
        """Re(lambda_r) = r_eig/2 = 1."""
        assert r_eig / 2 == 1

    def test_hashimoto_s_real_part(self):
        """Re(lambda_s) = s_eig/2 = -2."""
        assert s_eig / 2 == -2

    def test_hashimoto_r_imaginary_squared(self):
        """Im(lambda_r)^2 = k-1-(r/2)^2 = 11-1 = 10 = Phi4."""
        im_sq = (k - 1) - (r_eig / 2) ** 2
        assert abs(im_sq - Phi4) < 1e-10

    def test_hashimoto_s_imaginary_squared(self):
        """Im(lambda_s)^2 = k-1-(s/2)^2 = 11-4 = 7 = Phi6."""
        im_sq = (k - 1) - (s_eig / 2) ** 2
        assert abs(im_sq - Phi6) < 1e-10

    def test_hashimoto_r_modulus_is_sqrt_km1(self):
        """Re^2 + Im^2 = 1 + 10 = 11 = k-1."""
        mod_sq = (r_eig / 2) ** 2 + Phi4
        assert abs(mod_sq - (k - 1)) < 1e-10

    def test_hashimoto_s_modulus_is_sqrt_km1(self):
        """Re^2 + Im^2 = 4 + 7 = 11 = k-1."""
        mod_sq = (s_eig / 2) ** 2 + Phi6
        assert abs(mod_sq - (k - 1)) < 1e-10

    def test_hashimoto_args(self):
        """Angles of Hashimoto eigenvalues."""
        arg_r = atan2(sqrt(float(Phi4)), 1.0)
        arg_s = atan2(sqrt(float(Phi6)), -2.0)
        assert abs(arg_r - 1.26451896) < 1e-5
        assert abs(arg_s - 2.21808117) < 1e-5

    def test_closed_walks_n1(self):
        """Tr(A^1) = 0 (no self-loops)."""
        assert k + r_eig * f + s_eig * g == 0

    def test_closed_walks_n2(self):
        """Tr(A^2) = k*v = 480 (number of edges * 2)."""
        assert k**2 + r_eig**2 * f + s_eig**2 * g == k * v

    def test_closed_walks_n3(self):
        """Tr(A^3) = 6*lambda*v = 960 (number of triangles * 6)."""
        Wn = k**3 + r_eig**3 * f + s_eig**3 * g
        assert Wn == 960
        n_triangles = Wn // 6
        assert n_triangles == v * k * l // 6
        assert n_triangles == 160

    def test_closed_walks_n4(self):
        """Tr(A^4) = 24960."""
        assert k**4 + r_eig**4 * f + s_eig**4 * g == 24960

    def test_closed_walks_n5(self):
        """Tr(A^5) = 234240."""
        assert k**5 + r_eig**5 * f + s_eig**5 * g == 234240

    def test_closed_walks_n6(self):
        """Tr(A^6) = 3048960."""
        assert k**6 + r_eig**6 * f + s_eig**6 * g == 3048960

    def test_ihara_prefactor_exponent(self):
        """Ihara: (1-u^2)^{E-v} where E-v = 200 = v*(k-2)/2."""
        assert E - v == 200
        assert E - v == v * (k - 2) // 2

    def test_weil_ihara_substitution(self):
        """Weil-Ihara: u = q^{-s} with q^s = sqrt(k-1) => s = log(k-1)/(2*log(q))."""
        s_weil = log(k - 1) / (2 * log(q))
        assert abs(q**s_weil - sqrt(k - 1)) < 1e-10
        assert abs(s_weil - 1.09132917) < 1e-6

    def test_trivial_ihara_pole_at_u1(self):
        """Trivial pole: 1-k*1+(k-1)*1^2 = 0."""
        assert 1 - k + (k - 1) == 0

    def test_trivial_ihara_pole_at_u_inv_km1(self):
        """Trivial pole: 1 - k/(k-1) + 1/(k-1) = 0."""
        u_val = Fraction(1, k - 1)
        assert 1 - k * u_val + (k - 1) * u_val**2 == 0

    def test_nontrivial_discriminants_negative(self):
        """Both non-trivial Ihara factors have negative discriminant."""
        disc_r = r_eig**2 - 4 * (k - 1)
        disc_s = s_eig**2 - 4 * (k - 1)
        assert disc_r == -40
        assert disc_s == -28
        assert disc_r < 0
        assert disc_s < 0

    def test_disc_r_equals_minus_4_Phi4(self):
        """disc(ev=r) = r^2 - 4*(k-1) = -4*Phi4."""
        disc_r = r_eig**2 - 4 * (k - 1)
        assert disc_r == -4 * Phi4

    def test_disc_s_equals_minus_4_Phi6(self):
        """disc(ev=s) = s^2 - 4*(k-1) = -4*Phi6."""
        disc_s = s_eig**2 - 4 * (k - 1)
        assert disc_s == -4 * Phi6

    def test_girth_is_3(self):
        """Girth = 3: triangles exist since lambda = 2 > 0."""
        assert l > 0  # triangles exist
        assert l == 2  # exactly 2 common neighbors per adjacent pair

    def test_triangle_count(self):
        """Number of triangles = Tr(A^3)/6 = 160."""
        Tr_A3 = k**3 + r_eig**3 * f + s_eig**3 * g
        n_triangles = Tr_A3 // 6
        assert n_triangles == 160
        # Also: n_triangles = v*k*lambda/6 = 40*12*2/6 = 160
        assert v * k * l // 6 == 160

    def test_generating_function_coefficients(self):
        """Coefficients of Tr((I-Au)^{-1}) match Tr(A^n)."""
        # 1/(1-12u) + 24/(1-2u) + 15/(1+4u)
        # Coefficient of u^n: 12^n + 24*2^n + 15*(-4)^n
        for n in range(1, 7):
            coeff = k**n + r_eig**n * f + s_eig**n * g
            direct = k**n + 24 * r_eig**n + 15 * s_eig**n
            assert coeff == direct
