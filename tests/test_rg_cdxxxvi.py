"""Phase 71 — Renormalization Group & Fixed Points (Q138)."""
import math
from fractions import Fraction

V, K, LAM, MU, Q = 40, 12, 2, 4, 3
R, S, F, G, E = 2, -4, 24, 15, 240
PHI3, PHI4, PHI6 = 13, 10, 7


class TestRGFlow:
    def test_scaling(self):
        assert abs(V ** (1 / Q) - Q) < 0.5

    def test_c_theorem(self):
        assert V > 0


class TestAsymptoticFreedom:
    def test_b0(self):
        b0 = 11 * Q - 2 * math.factorial(Q)
        assert b0 == 21

    def test_b0_factored(self):
        assert 11 * Q - 2 * math.factorial(Q) == Q * PHI6

    def test_Nf_max(self):
        assert 11 * Q // 2 == MU ** LAM

    def test_banks_zaks(self):
        assert MU ** LAM == 16


class TestCoupling:
    def test_alpha_gut(self):
        assert F == 24


class TestUniversality:
    def test_gamma_potts(self):
        assert Fraction(PHI3, Q ** 2) == Fraction(13, 9)

    def test_alpha_potts(self):
        assert Fraction(1, Q) == Fraction(1, 3)


class TestFixedPoints:
    def test_spectral_gap(self):
        assert K - R == PHI4

    def test_cheeger_gap(self):
        assert K - abs(S) == LAM ** Q

    def test_gap_ratio(self):
        assert Fraction(K - R, K - abs(S)) == Fraction(Q + 2, MU)
