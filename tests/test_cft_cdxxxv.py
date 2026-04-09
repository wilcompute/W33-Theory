"""Phase 70 — Conformal Field Theory & Modular Invariance (Q137)."""
from fractions import Fraction

V, K, LAM, MU, Q = 40, 12, 2, 4, 3
R, S, F, G, E = 2, -4, 24, 15, 240
PHI3, PHI4, PHI6 = 13, 10, 7


class TestVirasoro:
    def test_c_ising(self):
        c = 1 - Fraction(6 * (Q - (Q + 1)) ** 2, Q * (Q + 1))
        assert c == Fraction(1, LAM)

    def test_c_tricritical(self):
        c = 1 - Fraction(6, (Q + 1) * (Q + 2))
        assert c == Fraction(PHI6, PHI4)

    def test_c_yang_lee(self):
        c = 1 - Fraction(6 * (Q - (Q + 2)) ** 2, Q * (Q + 2))
        assert c == Fraction(-Q, Q + 2)


class TestWZW:
    def test_c_su2_q(self):
        c = Fraction(3 * Q, Q + 2)
        assert c == Fraction(Q ** 2, Q + 2)

    def test_primaries(self):
        assert Q + 1 == MU

    def test_h_half(self):
        h = Fraction(3, 4 * (Q + 2))
        assert h == Fraction(3, 20)

    def test_h_one(self):
        h = Fraction(2, Q + 2)
        assert h == Fraction(LAM, Q + 2)


class TestModular:
    def test_pentagon_golden(self):
        assert Q + 2 == 5

    def test_T_phase(self):
        phase = Fraction(Q ** 2, Q + 2) / 24
        assert phase == Fraction(Q, V)


class TestString:
    def test_bosonic_dim(self):
        assert Q ** Q - 1 == 26

    def test_super_dim(self):
        assert PHI4 == 10

    def test_super_c_matter(self):
        assert 3 * PHI4 // LAM == G
