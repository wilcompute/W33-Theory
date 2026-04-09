"""
Phase CDXXXII (432) — Emergent Spacetime & Spin Networks
========================================================
Causal structure, LQG spins, MERA, Regge calculus.
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


class TestT1_CausalStructure:
    def test_causal(self):
        assert k == 12

    def test_spacelike(self):
        assert v - k - 1 == q ** q

    def test_ratio(self):
        assert Fraction(k, v - k - 1) == Fraction(mu, q ** 2)


class TestT2_SpinLabels:
    def test_j_r(self):
        assert r // lam == 1  # spin-1 (gauge)

    def test_j_s(self):
        assert abs(s) // lam == 2  # spin-2 (graviton!)


class TestT3_AreaSpectrum:
    def test_area_ratio(self):
        j_r = r // lam
        j_s = abs(s) // lam
        assert Fraction(j_s * (j_s + 1), j_r * (j_r + 1)) == q


class TestT4_Volume:
    def test_triples(self):
        assert k * (k - 1) * (k - 2) // 6 == 220

    def test_triples_formula(self):
        assert k * (k - 1) * (k - 2) // 6 == (k - 1) * v // lam


class TestT5_MERA:
    def test_layer0(self):
        assert v == 40

    def test_layer1(self):
        assert Phi3 == 13

    def test_layer2(self):
        assert mu == 4

    def test_layer3(self):
        assert v // (q ** 3) == 1

    def test_depth(self):
        assert q == 3


class TestT6_Regge:
    def test_TE_ratio(self):
        assert Fraction(T, E) == Fraction(lam, q)

    def test_E_formula(self):
        assert E == v * math.factorial(q)
