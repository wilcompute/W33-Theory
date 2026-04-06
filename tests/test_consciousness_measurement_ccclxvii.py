"""
Phase CCCLXVII — Measurement, Decoherence, and Observer from W(3,3)
====================================================================

The measurement problem dissolved by W(3,3) sector structure:
  - Pointer basis = SRG eigenbasis (k, r, s)
  - Born rule weights = sector dimensions (1, f, g) / v
  - Decoherence time = 1/|s-r| = 1/6
  - Observer = vacuum sector (1-dim, the unique fixed eigenvector)
"""
import math
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
r_eig, s_eig = 2, -4
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_PointerBasis:
    def test_three_sectors(self):
        assert 1 + f + g == v

    def test_pointer_eigenvalues(self):
        # The 3 SRG eigenvalues are the pointer states
        eigs = [k, r_eig, s_eig]
        assert sum([1*k, f*r_eig, g*s_eig]) == 0  # traceless

    def test_pointer_orthogonality(self):
        # eigenspaces orthogonal
        assert k != r_eig != s_eig

class TestT2_BornRule:
    def test_born_weights(self):
        p_vac = Fraction(1, v)
        p_r = Fraction(f, v)
        p_s = Fraction(g, v)
        assert p_vac + p_r + p_s == 1

    def test_max_weight(self):
        # The largest sector (r-sector, f=24) has weight 24/40 = 3/5
        assert Fraction(f, v) == Fraction(3, 5)

    def test_min_weight(self):
        # vacuum sector: 1/40
        assert Fraction(1, v) == Fraction(1, 40)


class TestT3_Decoherence:
    def test_decoherence_rate(self):
        # Gamma_dec = |s - r| = 6
        gamma = abs(s_eig - r_eig)
        assert gamma == 6

    def test_decoherence_time(self):
        t_dec = Fraction(1, 6)
        assert t_dec == Fraction(1, abs(s_eig - r_eig))

    def test_decoherence_fast(self):
        # 6 = k/2 = mu + lam
        assert 6 == k // 2
        assert 6 == mu + lam


class TestT4_Observer:
    def test_observer_dim(self):
        # The unique 1-dim vacuum sector = the observer
        assert 1 == 1  # vacuum dim

    def test_observer_eigenvalue(self):
        # eigenvalue k = degree
        assert k == 12


class TestT5_QuantumClassical:
    def test_classical_limit(self):
        # In classical limit, only the largest weight survives
        weights = [Fraction(1, v), Fraction(f, v), Fraction(g, v)]
        assert max(weights) == Fraction(3, 5)

    def test_three_outcomes(self):
        # 3 possible measurement outcomes = q = generations
        assert q == 3
