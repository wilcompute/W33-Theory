"""Phase 73 — Gauge Theory & Yang-Mills Structure (Q140)."""
from fractions import Fraction

V, K, LAM, MU, Q = 40, 12, 2, 4, 3
R, S, F, G, E = 2, -4, 24, 15, 240
PHI3, PHI4, PHI6 = 13, 10, 7
T = 160


class TestGaugeGroup:
    def test_dim_su3(self):
        assert Q ** 2 - 1 == LAM ** Q

    def test_dim_su2(self):
        assert LAM ** 2 - 1 == Q

    def test_dim_sum(self):
        assert (Q ** 2 - 1) + (LAM ** 2 - 1) == K - 1

    def test_dim_sm_total(self):
        assert LAM ** Q + Q + 1 == K


class TestBosons:
    def test_total_gauge(self):
        assert LAM ** Q + Q + 1 == K

    def test_massless(self):
        assert Q ** 2 == 9

    def test_massive(self):
        assert Q == 3


class TestInstanton:
    def test_topological_density(self):
        assert Fraction(T, E) == Fraction(LAM, Q)


class TestAnomaly:
    def test_colors(self):
        assert Q == 3

    def test_doublets(self):
        assert LAM == 2


class TestChiral:
    def test_pions(self):
        assert LAM ** 2 - 1 == Q

    def test_mesons(self):
        assert Q ** 2 - 1 == LAM ** Q
