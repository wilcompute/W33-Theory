"""Tests for Part MCLIX: Seidel Matrix and Two-Graph for W(3,3)."""
import pytest
from fractions import Fraction
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
from w33_seidel_matrix import (
    seidel_eigenvalues, verify_seidel_trace, verify_seidel_trace_sq,
    seidel_energy, seidel_spectral_moments, equiangular_lines_data,
    triangle_data, novel_seidel_identities, seidel_tr_cube,
    seidel_matrix_main,
    v, k, m_r, m_s,
)


class TestSeidelEigenvalues:
    def setup_method(self):
        self.sigma = seidel_eigenvalues()

    def test_sigma_0(self):
        assert self.sigma[0][0] == Fraction(15)

    def test_sigma_r(self):
        assert self.sigma[1][0] == Fraction(-5)

    def test_sigma_s(self):
        assert self.sigma[2][0] == Fraction(7)

    def test_multiplicities(self):
        assert self.sigma[0][1] == 1
        assert self.sigma[1][1] == 24
        assert self.sigma[2][1] == 15

    def test_total_dimension(self):
        total = sum(m for _, m in self.sigma)
        assert total == v


class TestSeidelTraceIdentities:
    def setup_method(self):
        self.sigma = seidel_eigenvalues()

    def test_trace_zero(self):
        assert verify_seidel_trace(self.sigma) == Fraction(0)

    def test_trace_sq_v_times_vm1(self):
        assert verify_seidel_trace_sq(self.sigma) == Fraction(v * (v - 1))

    def test_trace_sq_value(self):
        tr2 = sum(e ** 2 * m for e, m in self.sigma)
        assert tr2 == Fraction(1560)

    def test_trace_cube_value(self):
        tr3 = seidel_tr_cube(self.sigma)
        assert tr3 == Fraction(5520)


class TestSeidelEnergy:
    def test_energy_equals_edge_count(self):
        sigma = seidel_eigenvalues()
        E_S = seidel_energy(sigma)
        assert E_S == Fraction(v * k, 2)

    def test_energy_value(self):
        sigma = seidel_eigenvalues()
        E_S = seidel_energy(sigma)
        assert E_S == Fraction(240)

    def test_energy_breakdown(self):
        # 15*1 + 5*24 + 7*15 = 15 + 120 + 105 = 240
        assert 15 * 1 + 5 * 24 + 7 * 15 == 240


class TestSpectralMoments:
    def setup_method(self):
        sigma = seidel_eigenvalues()
        self.m = seidel_spectral_moments(sigma)

    def test_M1_zero(self):
        assert self.m[0] == Fraction(0)

    def test_M2_v_vm1(self):
        assert self.m[1] == Fraction(1560)

    def test_M3(self):
        assert self.m[2] == Fraction(5520)

    def test_M4(self):
        assert self.m[3] == Fraction(101640)


class TestEquiangularLines:
    def setup_method(self):
        sigma = seidel_eigenvalues()
        self.eq = equiangular_lines_data(sigma)

    def test_angle(self):
        assert self.eq["angle"] == Fraction(1, 5)

    def test_dimension(self):
        assert self.eq["d"] == m_r

    def test_n_lines(self):
        assert self.eq["n"] == v

    def test_gerzon_satisfied(self):
        assert self.eq["gerzon_satisfied"]

    def test_gerzon_bound_value(self):
        assert self.eq["gerzon_bound"] == Fraction(300)

    def test_welch_satisfied(self):
        assert self.eq["welch_satisfied"]

    def test_welch_lhs(self):
        assert self.eq["welch_lhs"] == Fraction(1, 25)

    def test_welch_rhs(self):
        assert self.eq["welch_rhs"] == Fraction(2, 117)


class TestTriangleGQStructure:
    def test_tr_A3(self):
        tr_A3, _ = triangle_data()
        assert tr_A3 == Fraction(960)

    def test_n_triangles(self):
        _, n_tri = triangle_data()
        assert n_tri == Fraction(160)

    def test_all_triangles_on_lines(self):
        # GQ(3,3): 40 lines x C(4,3)=4 triangles each = 160
        _, n_tri = triangle_data()
        assert n_tri == 40 * 4


class TestNovelIdentities:
    def setup_method(self):
        sigma = seidel_eigenvalues()
        moments = seidel_spectral_moments(sigma)
        self.ids = novel_seidel_identities(sigma, moments)

    def test_sigma_sum_r_s(self):
        assert self.ids["sigma_r_plus_sigma_s"] == Fraction(2)

    def test_sigma_product_r_s(self):
        assert self.ids["sigma_r_times_sigma_s"] == Fraction(-35)

    def test_kemeny_collision_root(self):
        # (1+r) = -(1+s) = 3: the same root that caused strong-product collision
        assert self.ids["one_plus_r"] == Fraction(3)
        assert self.ids["one_plus_s"] == Fraction(-3)
        assert self.ids["sum_1pr_1ps"] == Fraction(0)

    def test_energy_equals_edges(self):
        assert self.ids["energy_eq_edges"]

    def test_gq_lambda(self):
        assert self.ids["gq_two_graph_lambda"] == Fraction(4)


class TestFullPacket:
    def test_main_verified_count(self):
        results = seidel_matrix_main()
        assert results["n_verified"] == 21

    def test_main_sigma_values(self):
        results = seidel_matrix_main()
        assert results["sigma_0"] == "15"
        assert results["sigma_r"] == "-5"
        assert results["sigma_s"] == "7"

    def test_main_energy(self):
        results = seidel_matrix_main()
        assert results["seidel_energy"] == "240"
