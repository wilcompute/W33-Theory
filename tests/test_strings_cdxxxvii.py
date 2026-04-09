"""Phase 72 — String Theory Amplitudes & Dualities (Q139)."""
import math
from fractions import Fraction

V, K, LAM, MU, Q = 40, 12, 2, 4, 3
R, S, F, G, E = 2, -4, 24, 15, 240
PHI3, PHI4, PHI6 = 13, 10, 7


class TestRegge:
    def test_slope_r(self):
        assert Fraction(1, K - R) == Fraction(1, PHI4)

    def test_slope_s(self):
        assert Fraction(1, K + abs(S)) == Fraction(1, MU ** LAM)

    def test_slope_ratio(self):
        assert Fraction(PHI4, MU ** LAM) == Fraction(5, 8)


class TestDimensions:
    def test_bosonic(self):
        assert Q ** Q - 1 == 26

    def test_super(self):
        assert PHI4 == 10

    def test_M_theory(self):
        assert K - 1 == 11

    def test_F_theory(self):
        assert K == 12

    def test_tower(self):
        assert [PHI4, K - 1, K, Q ** Q - 1] == [10, 11, 12, 26]


class TestTDuality:
    def test_eigen_product(self):
        assert R * abs(S) == LAM ** Q

    def test_geometric_mean(self):
        assert abs(math.sqrt(R * abs(S)) - LAM ** (Q / 2)) < 1e-10


class TestSDuality:
    def test_duality_sum(self):
        s = Fraction(F, G) + Fraction(G, F)
        assert s == Fraction(89, V)


class TestModuli:
    def test_srg_count(self):
        assert LAM ** Q * (LAM ** Q - 1) // 2 == 28

    def test_so8_dim(self):
        assert LAM ** Q * (LAM ** Q - 1) // 2 == 28
