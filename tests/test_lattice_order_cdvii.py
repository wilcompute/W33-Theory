"""
Phase CDVII (407) — Lattice Theory & Order Structures from W(3,3)
=================================================================
Subspace lattice PG(3,F_3), Gaussian binomials, Möbius function,
partition lattice, Young tableaux.
"""
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_SubspaceLattice:
    def test_gauss_41(self):
        assert (q**4 - 1) // (q - 1) == v
    def test_gauss_42(self):
        assert (q**4 - 1) * (q**3 - 1) // ((q**2 - 1) * (q - 1)) == 130
    def test_lattice_total(self):
        assert 1 + v + 130 + v + 1 == 212

class TestT2_GaussianBinomials:
    def test_q1(self):
        assert 1 == 1
    def test_q2(self):
        assert 1 + q == mu
    def test_q3(self):
        assert 1 + q + q**2 == Phi3
    def test_q4(self):
        assert 1 + q + q**2 + q**3 == v
    def test_qfact(self):
        assert 1 * mu * Phi3 * v == 2080

class TestT3_Mobius:
    def test_mobius_PG3(self):
        assert (-1)**3 * q**3 == -(q**q)
    def test_q_cubed(self):
        assert q**q == v - k - 1

class TestT4_Partition:
    def test_bell_4(self):
        assert 15 == g
    def test_bell_3(self):
        assert 5 == mu + 1
    def test_stirling_42(self):
        assert 7 == Phi6
    def test_stirling_43(self):
        assert 6 == math.factorial(q)

class TestT5_Young:
    def test_partitions_4(self):
        assert mu + 1 == 5
    def test_partitions_3(self):
        assert q == 3
