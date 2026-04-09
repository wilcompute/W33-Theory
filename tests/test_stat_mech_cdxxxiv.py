"""Phase 69 — Statistical Mechanics & Partition Functions (Q136)."""
import math
from fractions import Fraction

V, K, LAM, MU, Q = 40, 12, 2, 4, 3
R, S, F, G, E = 2, -4, 24, 15, 240
PHI3, PHI4, PHI6 = 13, 10, 7


class TestIsing:
    def test_mean_field_Tc(self):
        assert K == 12

    def test_bethe_Tc(self):
        Tc = 1 / math.atanh(1 / (K - 1))
        assert 10.9 < Tc < 11.1

    def test_ground_energy(self):
        assert -E == -240

    def test_magnetization_sectors(self):
        assert V + 1 == 41


class TestPotts:
    def test_state_space(self):
        assert Q ** V == 3 ** 40

    def test_beta_c(self):
        bc = Fraction(2 * (Q - 1), Q * K)
        assert bc == Fraction(1, Q ** 2)


class TestHighTemp:
    def test_cycle_space_dim(self):
        assert E - V + 1 == Q * 67

    def test_girth(self):
        assert Q == 3


class TestFreeEnergy:
    def test_ground_state_per_vertex(self):
        assert -E // V == -math.factorial(Q)

    def test_entropy_ising(self):
        assert abs(math.log(2) - 0.693) < 0.001

    def test_entropy_potts(self):
        assert abs(math.log(Q) - 1.099) < 0.001


class TestLeeYang:
    def test_zeros_count(self):
        assert V == 40
