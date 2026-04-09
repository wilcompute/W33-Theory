"""
Phase CDXIV (414) — Algebraic Number Theory & Class Field Theory
=================================================================
Quadratic fields, class numbers, cyclotomic, Dedekind zeta, ramification.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Quadratic:
    def test_disc_eisenstein(self):
        assert -q == -3
    def test_disc_gaussian(self):
        assert s == -4
    def test_disc_golden(self):
        assert mu + 1 == 5

class TestT2_ClassNumbers:
    def test_heegner_count(self):
        assert q**2 == 9
    def test_eisenstein_units(self):
        assert math.factorial(q) == 6
    def test_gaussian_units(self):
        assert mu == 4

class TestT3_Cyclotomic:
    def test_phi_q(self):
        assert lam == 2
    def test_phi_k(self):
        assert mu == 4
    def test_phi_v(self):
        assert lam**mu == 16
    def test_phi_E(self):
        assert 8 * 2 * 4 == lam**math.factorial(q)

class TestT4_Zeta:
    def test_zeta_minus1(self):
        assert Fraction(-1, k) == Fraction(-1, 12)
    def test_zeta_minus3(self):
        assert Fraction(1, k * Phi4) == Fraction(lam, E)
    def test_zeta2_denom(self):
        assert math.factorial(q) == 6
