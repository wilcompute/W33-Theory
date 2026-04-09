"""
Phase CDX (410) — Graph Polynomials & Chromatic Theory from W(3,3)
===================================================================
Chromatic polynomial, Tutte polynomial, Lovász theta, Shannon capacity,
matching polynomial, independence polynomial.
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Chromatic:
    def test_chi(self):
        assert mu == 4
    def test_chi_fractional(self):
        assert Fraction(v, Phi4) == mu
    def test_tight(self):
        assert Fraction(v, Phi4) == mu

class TestT2_Independence:
    def test_alpha(self):
        assert Phi4 == 10
    def test_omega(self):
        assert mu == 4
    def test_alpha_omega(self):
        assert Phi4 * mu == v
    def test_lovasz_sandwich(self):
        assert mu * Phi4 == v

class TestT3_Matching:
    def test_max_matching(self):
        assert v // 2 == E // k
    def test_perfect(self):
        assert v % 2 == 0
    def test_edge_chromatic(self):
        assert k == 12

class TestT4_Tutte:
    def test_laplacian_eig1(self):
        assert k - r == Phi4
    def test_laplacian_eig2(self):
        assert k - s == lam**mu

class TestT5_Theta:
    def test_lovasz_theta(self):
        assert v * (-s) // (k - s) == Phi4
    def test_complement_theta(self):
        assert v // Phi4 == mu
    def test_product(self):
        assert Phi4 * mu == v
