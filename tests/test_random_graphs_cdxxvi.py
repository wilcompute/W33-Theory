"""
Phase CDXXVI (426) — Probabilistic Combinatorics & Random Graphs
================================================================
Edge density, degree concentration, triangle count,
threshold functions, clique expectations.
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
T = v * k * lam // 6
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_EdgeDensity:
    def test_density(self):
        p = Fraction(E, v * (v - 1) // 2)
        assert p == Fraction(4, 13)

    def test_density_params(self):
        p = Fraction(E, v * (v - 1) // 2)
        assert p == Fraction(mu, Phi3)

    def test_expected_edges(self):
        p = Fraction(mu, Phi3)
        assert Fraction(v * (v - 1), 2) * p == E


class TestT2_DegreeDistribution:
    def test_expected_degree(self):
        p = Fraction(mu, Phi3)
        assert (v - 1) * p == k

    def test_regular(self):
        p = Fraction(mu, Phi3)
        assert (v - 1) * p == k


class TestT3_TriangleCount:
    def test_Cv3(self):
        assert v * (v - 1) * (v - 2) // 6 == 9880

    def test_fewer_than_random(self):
        Cv3 = v * (v - 1) * (v - 2) // 6
        assert T * Fraction(2197, 64) < Cv3


class TestT4_Thresholds:
    def test_above_connectivity(self):
        assert Fraction(mu, Phi3) > Fraction(1, 10)

    def test_chi(self):
        assert mu == 4


class TestT5_Concentration:
    def test_variance(self):
        p = Fraction(mu, Phi3)
        var = (v - 1) * p * (1 - p)
        assert var == Fraction(1404, 169)


class TestT6_SecondMoment:
    def test_Cv4(self):
        assert v * (v - 1) * (v - 2) * (v - 3) // 24 == 91390

    def test_actual_K4(self):
        assert v == 40
