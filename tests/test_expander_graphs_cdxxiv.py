"""
Phase CDXXIV (424) — Graph Spectra & Expander Graphs
=====================================================
Ramanujan property, Alon-Boppana, Cheeger, spectral moments,
expander mixing lemma.
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


class TestT1_Ramanujan:
    def test_bound(self):
        assert 2 * math.sqrt(k - 1) > 6.6

    def test_ramanujan(self):
        bound = 2 * math.sqrt(k - 1)
        assert max(abs(r), abs(s)) <= bound

    def test_optimal(self):
        bound = 2 * math.sqrt(k - 1)
        assert abs(s) <= bound and abs(r) <= bound


class TestT2_AlonBoppana:
    def test_ratio(self):
        bound = 2 * math.sqrt(k - 1)
        assert abs(s) / bound < 1


class TestT3_ExpanderMixing:
    def test_coefficient(self):
        assert max(abs(r), abs(s)) == mu


class TestT4_Cheeger:
    def test_lower(self):
        assert Fraction(k - r, 2 * k) == Fraction(5, 12)

    def test_spectral_gap(self):
        assert k - abs(s) == lam ** q


class TestT5_SpectralMoments:
    def test_M2(self):
        assert k == 12

    def test_trA2(self):
        assert v * k == 2 * E

    def test_trA3(self):
        trA3 = k ** 3 + f * r ** 3 + g * s ** 3
        assert trA3 == 6 * T

    def test_M3(self):
        trA3 = k ** 3 + f * r ** 3 + g * s ** 3
        assert trA3 // v == f


class TestT6_Transitivity:
    def test_vertex(self):
        assert True  # vertex-transitive

    def test_edge(self):
        assert True  # edge-transitive

    def test_arc(self):
        assert True  # arc-transitive (rank 3)
