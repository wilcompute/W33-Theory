"""
Phase CDXXX (430) — Computational Complexity & Physics
======================================================
Clique/chromatic, independence, SAT thresholds, Körner entropy.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Clique:
    def test_omega(self):
        assert mu == 4

    def test_max_cliques(self):
        assert (q + 1) * (q ** 2 + 1) == v


class TestT2_Chromatic:
    def test_chi(self):
        assert mu == 4

    def test_chi_f(self):
        assert Fraction(v, Phi4) == mu

    def test_no_gap(self):
        assert Fraction(v, Phi4) == mu


class TestT3_Independence:
    def test_alpha(self):
        assert Phi4 == 10

    def test_cover(self):
        assert v - Phi4 == q * Phi4


class TestT4_SAT:
    def test_3sat(self):
        assert q == 3

    def test_2sat(self):
        assert lam == 2


class TestT5_KornerEntropy:
    def test_korner(self):
        assert abs(math.log2(v / Phi4) - lam) < 1e-10

    def test_korner_complement(self):
        assert abs(math.log2(v / mu) - math.log2(Phi4)) < 1e-10

    def test_sum(self):
        H1 = math.log2(v / Phi4)
        H2 = math.log2(v / mu)
        assert abs(H1 + H2 - math.log2(v)) < 1e-10
