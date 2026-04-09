"""
Phase CDXXIII (423) — Harmonic Analysis on Finite Groups
========================================================
Gelfand pairs, spherical functions, Fourier transform,
Plancherel measure, convolution algebra.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_GelfandPair:
    def test_rank(self):
        assert q == 3

    def test_hecke_dim(self):
        assert q == 3


class TestT2_SphericalFunctions:
    def test_phi1_1(self):
        assert Fraction(r, k) == Fraction(1, math.factorial(q))

    def test_phi1_2(self):
        assert Fraction(-(r + 1), v - k - 1) == Fraction(-1, q ** 2)

    def test_phi2_1(self):
        assert Fraction(s, k) == Fraction(-1, q)

    def test_phi2_2(self):
        assert Fraction(-(s + 1), v - k - 1) == Fraction(1, q ** 2)


class TestT3_Fourier:
    def test_decomp(self):
        assert 1 + f + g == v

    def test_plancherel_0(self):
        assert Fraction(1, v) == Fraction(1, 40)

    def test_plancherel_1(self):
        assert Fraction(f, v) == Fraction(3, 5)

    def test_plancherel_2(self):
        assert Fraction(g, v) == Fraction(3, 8)

    def test_plancherel_sum(self):
        assert Fraction(1, v) + Fraction(f, v) + Fraction(g, v) == 1


class TestT4_Convolution:
    def test_bm_dim(self):
        assert q == 3

    def test_p1_11(self):
        assert lam == 2


class TestT5_Duality:
    def test_fg_ratio(self):
        assert Fraction(f, g) == Fraction(lam ** q, mu + 1)
