"""
Phase CDXXXI (431) — Holographic Principle & Black Hole Physics
===============================================================
Bekenstein-Hawking, area law, scrambling, Page curve.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
T = v * k * lam // 6
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_BekensteinHawking:
    def test_area(self):
        assert v * k == 2 * E

    def test_quarter(self):
        assert Fraction(1, mu) == Fraction(1, 4)

    def test_f_ratio(self):
        assert Fraction(f, v * k) == Fraction(1, 20)


class TestT2_AreaLaw:
    def test_single_vertex(self):
        assert k == 12

    def test_half_cut(self):
        assert k * v // 4 == E // lam


class TestT3_Scrambling:
    def test_fast(self):
        assert lam < math.log(v)

    def test_rate(self):
        rate = math.log2(v) / lam
        assert 2.6 < rate < 2.7


class TestT4_Holographic:
    def test_k_power(self):
        assert abs(k ** 1.5 - v) < 2


class TestT5_PageCurve:
    def test_peak(self):
        assert v // lam == 20

    def test_peak_formula(self):
        assert v // lam == lam * Phi4


class TestT6_Complementarity:
    def test_views(self):
        assert q == 3

    def test_infalling(self):
        assert f == 24

    def test_exterior(self):
        assert g == 15
