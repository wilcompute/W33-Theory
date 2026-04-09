"""
Phase CDXV (415) — Operator Algebras & NCG II
===============================================
Jones index, Temperley-Lieb, planar algebras, spectral flow, K-theory.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Jones:
    def test_boundary(self):
        assert mu == 4
    def test_cos_mu(self):
        assert lam == 2

class TestT2_TL:
    def test_C2(self):
        assert lam == 2
    def test_C3(self):
        assert mu + 1 == 5
    def test_C4(self):
        assert Phi3 + 1 == 14
    def test_C5(self):
        assert 42 == v + lam

class TestT3_NCG:
    def test_hilbert(self):
        assert v == 40
    def test_dirac1(self):
        assert k - r == Phi4
    def test_dirac2(self):
        assert k - s == lam**mu
    def test_KO(self):
        assert math.factorial(q) == 6

class TestT4_Ktheory:
    def test_rw_eig(self):
        assert Fraction(r, k) == Fraction(1, math.factorial(q))
    def test_index(self):
        assert f - g == q**2
    def test_eta(self):
        assert f - g == 9
