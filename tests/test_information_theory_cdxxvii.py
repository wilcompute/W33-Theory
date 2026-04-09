"""
Phase CDXXVII (427) — Information Theory & Entropy
====================================================
Shannon entropy, von Neumann entropy, channel capacity,
holographic bounds.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_SpectralWeights:
    def test_sum(self):
        assert Fraction(1, v) + Fraction(f, v) + Fraction(g, v) == 1


class TestT2_ShannonEntropy:
    def test_range(self):
        w0, w1, w2 = 1/v, f/v, g/v
        H = -w0*math.log2(w0) - w1*math.log2(w1) - w2*math.log2(w2)
        assert 1.0 < H < 1.2

    def test_Hmax(self):
        assert 1.58 < math.log2(q) < 1.59


class TestT3_VonNeumann:
    def test_l1(self):
        assert Fraction(1, 1) - Fraction(r, k) == Fraction(5, 6)

    def test_l2(self):
        assert 1 - Fraction(s, k) == Fraction(4, 3)

    def test_trL(self):
        assert f * Fraction(5, 6) + g * Fraction(4, 3) == v

    def test_equal_contribution(self):
        assert f * Fraction(5, 6) == 20
        assert g * Fraction(4, 3) == 20


class TestT4_Holographic:
    def test_ratio(self):
        assert Fraction(k, v) == Fraction(q, Phi4)

    def test_log_ratio(self):
        ratio = math.log2(k) / math.log2(v)
        assert abs(ratio - lam/q) < 0.01
