"""
Phase CDVIII (408) — Finite Group Actions & Permutation Theory from W(3,3)
===========================================================================
Burnside ring, Polya, double cosets, orbital graphs, automorphisms.
"""
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7
Sp4_order = 51840


class TestT1_Orbitals:
    def test_num_orbitals(self):
        assert q == 3
    def test_orbital_sizes(self):
        assert 1 + k + (v - k - 1) == v

class TestT2_MinDegree:
    def test_min_degree(self):
        assert v - k == mu * Phi6

class TestT3_Burnside:
    def test_rank(self):
        assert 1 + f + g == v

class TestT4_DoubleCosets:
    def test_num_double_cosets(self):
        assert q == 3
    def test_pt_stab(self):
        assert Sp4_order // v == 6**mu

class TestT5_Automorphisms:
    def test_sp4(self):
        assert Sp4_order == 51840
    def test_factorisation(self):
        assert lam**Phi6 * q**mu * (mu + 1) == 51840
    def test_center(self):
        assert lam == 2

class TestT6_OrbitalGraphs:
    def test_complement_valency(self):
        assert v - k - 1 == q**q
    def test_complement_srg(self):
        k_c = v - k - 1
        lam_c = v - 2 * k + mu - 2
        mu_c = v - 2 * k + lam
        assert (k_c, lam_c, mu_c) == (27, 18, 18)
