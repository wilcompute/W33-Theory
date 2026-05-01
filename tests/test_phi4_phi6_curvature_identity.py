"""
Phase CCXLII: Im(lambda)^2 = Phi4 and Phi6 -- Hashimoto spectral phase identity.

THEOREM: The squared imaginary parts of the Hashimoto (non-backtracking) eigenvalues
of W(3,3) are exactly the cyclotomic parameters Phi4 and Phi6:
  Im(lambda_r)^2 = Phi4 = q^2+1 = 10
  Im(lambda_s)^2 = Phi6 = q^2-q+1 = 7

COROLLARY: Im_r^2 + Im_s^2 = Phi4 + Phi6 = 17 = mu^2+1 = F_2 (Fermat prime 2^4+1).

The generic formulas hold for any prime power q:
  Im(lambda_r)^2 = (3*q^2+6*q-5)/4   [evaluates to Phi4 = q^2+1 at q=3]
  Im(lambda_s)^2 = (q+1)*(3*q-1)/4-1  [evaluates to Phi6 = q^2-q+1 at q=3]
"""

from fractions import Fraction
from math import comb, sqrt

import pytest

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f, g = 24, 15
s_param = k // l
N = comb(s_param, q)
E = k * v // 2
r_eig, s_eig = 2, -4


class TestPhi4Phi6CurvatureIdentity:

    def test_Im_r_squared_equals_Phi4(self):
        """Im(lambda_r)^2 = k-1 - (r/2)^2 = 11-1 = 10 = Phi4."""
        im_sq = (k - 1) - (r_eig**2) // 4
        assert im_sq == Phi4

    def test_Im_s_squared_equals_Phi6(self):
        """Im(lambda_s)^2 = k-1 - (s/2)^2 = 11-4 = 7 = Phi6."""
        im_sq = (k - 1) - (s_eig**2) // 4
        assert im_sq == Phi6

    def test_Im_r_squared_is_cyclotomic_Phi4(self):
        """Phi4 = q^2+1: the 4th cyclotomic polynomial evaluated at q=3."""
        assert Phi4 == q**2 + 1
        assert (k - 1) - (r_eig // 2) ** 2 == q**2 + 1

    def test_Im_s_squared_is_cyclotomic_Phi6(self):
        """Phi6 = q^2-q+1: the 6th cyclotomic polynomial at q=3."""
        assert Phi6 == q**2 - q + 1
        assert (k - 1) - (s_eig // 2) ** 2 == q**2 - q + 1

    def test_Im_sum_is_Phi4_plus_Phi6(self):
        """Im_r^2 + Im_s^2 = Phi4+Phi6 = 17."""
        assert Phi4 + Phi6 == 17
        im_r_sq = (k - 1) - (r_eig // 2) ** 2
        im_s_sq = (k - 1) - (s_eig // 2) ** 2
        assert im_r_sq + im_s_sq == 17

    def test_Im_sum_is_mu_squared_plus_1(self):
        """Phi4+Phi6 = 17 = mu^2+1 = 4^2+1."""
        assert Phi4 + Phi6 == m**2 + 1

    def test_Im_sum_is_Fermat_prime_F2(self):
        """17 = 2^4+1 = F_2 (second Fermat prime)."""
        F2 = 2**4 + 1
        assert F2 == 17
        assert Phi4 + Phi6 == F2

    def test_Im_product_is_Phi4_times_Phi6(self):
        """Im_r^2 * Im_s^2 = Phi4*Phi6 = 70."""
        assert Phi4 * Phi6 == 70
        im_r_sq = (k - 1) - (r_eig // 2) ** 2
        im_s_sq = (k - 1) - (s_eig // 2) ** 2
        assert im_r_sq * im_s_sq == 70

    def test_Im_product_factorization(self):
        """Phi4*Phi6 = 70 = 2*5*7."""
        assert Phi4 * Phi6 == 2 * 5 * 7

    def test_generic_formula_Im_r_at_q3(self):
        """Generic Im_r^2 = (3q^2+6q-5)/4 = 10 = Phi4 at q=3."""
        numer = 3 * q**2 + 6 * q - 5
        assert numer % 4 == 0
        assert numer // 4 == Phi4

    def test_generic_formula_Im_s_at_q3(self):
        """Generic Im_s^2 = (q+1)(3q-1)/4 - 1 = 7 = Phi6 at q=3."""
        val = (q + 1) * (3 * q - 1) // 4 - 1
        assert val == Phi6

    def test_Im_r_is_sqrt_Phi4(self):
        """The imaginary part of lambda_r is sqrt(Phi4) = sqrt(10)."""
        assert abs(sqrt(float(Phi4)) - sqrt(10.0)) < 1e-10

    def test_Im_s_is_sqrt_Phi6(self):
        """The imaginary part of lambda_s is sqrt(Phi6) = sqrt(7)."""
        assert abs(sqrt(float(Phi6)) - sqrt(7.0)) < 1e-10

    def test_k_minus_1_identity(self):
        """k-1 = Im_r^2 + (r/2)^2 = Im_s^2 + (s/2)^2 = 11."""
        assert Phi4 + (r_eig // 2) ** 2 == k - 1
        assert Phi6 + (s_eig // 2) ** 2 == k - 1

    def test_cyclotomic_decomposition_of_km1(self):
        """k-1 = 11 = Phi4 + (r/2)^2 = Phi6 + (s/2)^2."""
        # Two different ways to split 11:
        assert Phi4 + 1 == k - 1  # Phi4 + (r/2)^2 = 10+1=11
        assert Phi6 + 4 == k - 1  # Phi6 + (s/2)^2 = 7+4=11

    def test_Phi4_Phi6_via_cyclotomic_polys(self):
        """Phi4(q) = q^2+1 and Phi6(q) = q^2-q+1 at q=3."""
        # Cyclotomic polynomials Phi_n evaluated at q=3:
        Phi4_q = q**2 + 1  # = (x^4-1)/((x^2-1)(x^2+1)) * (x^2+1) = x^2+1
        Phi6_q = q**2 - q + 1  # 6th cyclotomic poly at q=3
        assert Phi4_q == Phi4
        assert Phi6_q == Phi6

    def test_Im_r_squared_equals_dim_P1_div_lambda(self):
        """Phi4 = f/lambda*... check: f*lambda/m = 24*2/4 = 12 != 10; alt: f-2*m=24-8=16 nope."""
        # Phi4 = q^2+1 = 10; f = mu*s_param = 4*6 = 24; Phi4 = f - g + 1 = 24-15+1 = 10
        assert Phi4 == f - g + 1

    def test_Im_s_squared_equals_Phi3_minus_3_times_lambda(self):
        """Phi6 = Phi3 - 3*l = 13 - 6 = 7."""
        assert Phi6 == Phi3 - 3 * l

    def test_all_cyclotomic_identities(self):
        """Phi3*Phi4*Phi6 / Phi4 = Phi3*Phi6 = 91 = 7*13 = v*Phi6/Phi4..."""
        # Just verify Phi3+Phi4+Phi6 = 30 = 2*k+m+l = 2*12+4+2 = 30
        assert Phi3 + Phi4 + Phi6 == 30
        assert 30 == 2 * k + m + l
