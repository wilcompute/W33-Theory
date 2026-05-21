"""Tests for Part MCLX: Clique Complex and Simplicial Homology of W(3,3)."""
import pytest
from fractions import Fraction
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
from w33_clique_complex import (
    f_vector, euler_characteristic, reduced_euler_characteristic,
    simplex_counts_from_lines, link_of_vertex, spectral_check,
    clique_complex_main, v, k, lam, mu_param, s_gq, t_gq,
)


class TestFVector:
    def setup_method(self):
        self.fv = f_vector()

    def test_f0_vertices(self):
        assert self.fv[0] == 40

    def test_f1_edges(self):
        assert self.fv[1] == 240

    def test_f2_triangles(self):
        assert self.fv[2] == 160

    def test_f3_4cliques(self):
        assert self.fv[3] == 40

    def test_total_simplices(self):
        assert sum(self.fv) == 480

    def test_f1_equals_edges_formula(self):
        assert self.fv[1] == v * k // 2

    def test_f3_equals_gq_lines(self):
        # GQ(3,3): b = (t+1)(1+st) = 4*10 = 40
        b = (t_gq + 1) * (1 + s_gq * t_gq)
        assert self.fv[3] == b

    def test_v_equals_b(self):
        # In GQ(3,3) the number of points equals the number of lines
        b = (t_gq + 1) * (1 + s_gq * t_gq)
        assert self.fv[0] == b


class TestEulerCharacteristic:
    def setup_method(self):
        self.fv = f_vector()

    def test_chi_value(self):
        chi = euler_characteristic(self.fv)
        assert chi == Fraction(-80)

    def test_chi_equals_minus_2v(self):
        chi = euler_characteristic(self.fv)
        assert chi == Fraction(-2 * v)

    def test_reduced_chi_value(self):
        chi_r = reduced_euler_characteristic(self.fv)
        assert chi_r == Fraction(-81)

    def test_reduced_chi_equals_chi_minus_1(self):
        chi = euler_characteristic(self.fv)
        chi_r = reduced_euler_characteristic(self.fv)
        assert chi_r == chi - Fraction(1)

    def test_spectral_check(self):
        assert spectral_check() == Fraction(-80)


class TestSimplexCountsFromLines:
    def test_all_simplices_from_lines(self):
        fv = f_vector()
        from_lines = simplex_counts_from_lines()
        assert from_lines == fv

    def test_f1_from_lines(self):
        _, f1c, _, _ = simplex_counts_from_lines()
        assert f1c == 240   # 40 lines * 6 edges each

    def test_f2_from_lines(self):
        _, _, f2c, _ = simplex_counts_from_lines()
        assert f2c == 160   # 40 lines * 4 triangles each

    def test_f3_from_lines(self):
        _, _, _, f3c = simplex_counts_from_lines()
        assert f3c == 40    # 40 lines * 1 4-clique each

    def test_f_ratios(self):
        fv = f_vector()
        assert Fraction(fv[1], fv[3]) == Fraction(6)   # C(4,2)
        assert Fraction(fv[2], fv[3]) == Fraction(4)   # C(4,3)
        assert Fraction(fv[0], fv[3]) == Fraction(1)   # points = lines in GQ(3,3)


class TestLinkOfVertex:
    def setup_method(self):
        self.f0L, self.f1L, self.f2L, self.chiL = link_of_vertex()

    def test_link_f0(self):
        assert self.f0L == Fraction(12)

    def test_link_f1(self):
        assert self.f1L == Fraction(12)

    def test_link_f2(self):
        assert self.f2L == Fraction(4)

    def test_link_chi(self):
        assert self.chiL == Fraction(4)

    def test_link_chi_formula(self):
        chi_L = self.f0L - self.f1L + self.f2L
        assert chi_L == Fraction(4)

    def test_link_f2_from_lines(self):
        # Lines through v: t+1 = 4, each gives 1 triangle in link
        assert self.f2L == Fraction(t_gq + 1)


class TestFullPacket:
    def test_main_verified_count(self):
        results = clique_complex_main()
        assert results["n_verified"] == 19

    def test_main_chi(self):
        results = clique_complex_main()
        assert results["euler_characteristic"] == "-80"

    def test_main_f0(self):
        results = clique_complex_main()
        assert results["f0"] == 40

    def test_main_f1(self):
        results = clique_complex_main()
        assert results["f1"] == 240

    def test_main_f2(self):
        results = clique_complex_main()
        assert results["f2"] == 160

    def test_main_f3(self):
        results = clique_complex_main()
        assert results["f3"] == 40
