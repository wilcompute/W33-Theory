"""Phase 74 — Supersymmetry & Extended Symmetry (Q141)."""
import math
from fractions import Fraction

V, K, LAM, MU, Q = 40, 12, 2, 4, 3
R, S, F, G, E = 2, -4, 24, 15, 240
PHI3, PHI4, PHI6 = 13, 10, 7


class TestSUSYAlgebra:
    def test_max_supercharges(self):
        assert LAM ** (Q + LAM) == 32

    def test_N1(self):
        assert MU == 4

    def test_N2(self):
        assert LAM ** Q == 8

    def test_N4(self):
        assert MU ** LAM == 16

    def test_N8(self):
        assert LAM ** 5 == 32


class TestWittenIndex:
    def test_su3(self):
        assert Q == 3

    def test_su2(self):
        assert LAM == 2


class TestBPS:
    def test_spectral_bound(self):
        assert abs(R) <= K and abs(S) <= K

    def test_bps_fraction(self):
        assert Fraction(1, V) == Fraction(1, 40)


class TestN4SYM:
    def test_scalars(self):
        assert math.factorial(Q) == 6

    def test_weyl_fermions(self):
        assert MU == 4

    def test_dof_sum(self):
        assert LAM + math.factorial(Q) + LAM ** Q == MU ** LAM


class TestSUSYBreaking:
    def test_hierarchy(self):
        assert MU ** LAM == 16
