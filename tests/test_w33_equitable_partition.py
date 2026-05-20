"""Tests for Part MCLVI: Equitable Partition and Quotient Matrix for W(3,3)."""
import pytest
from fractions import Fraction
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
from w33_equitable_partition import (
    verify_srg_parameters,
    trivial_equitable_partition,
    quotient_matrix_eigenvalues_3cell,
    characteristic_polynomial_3cell,
    two_cell_partition_line_spread,
    interlacing_theorem_bounds,
    quotient_matrix_trace_identities,
    equitable_partition_main,
)

# SRG parameters
V, K, LAM, MU, R, S = 40, 12, 2, 4, 2, -4
M_R, M_S = 24, 15


class TestSRGParameters:
    def test_srg_params_verified(self):
        assert verify_srg_parameters() is True

    def test_multiplicities(self):
        assert M_R + M_S + 1 == V
        # Trace: k + m_r*r + m_s*s = 0
        assert K + M_R * R + M_S * S == 0


class TestThreeCellPartition:
    def setup_method(self):
        self.B, self.sizes = trivial_equitable_partition()

    def test_cell_sizes(self):
        assert self.sizes == (1, K, V - K - 1)
        assert sum(self.sizes) == V

    def test_row_sums_equal_k(self):
        for row in self.B:
            assert sum(row) == K

    def test_b_entries(self):
        B = self.B
        assert B[0][0] == Fraction(0)
        assert B[0][1] == Fraction(K)
        assert B[0][2] == Fraction(0)
        assert B[1][0] == Fraction(1)
        assert B[1][1] == Fraction(LAM)
        assert B[1][2] == Fraction(K - 1 - LAM)
        assert B[2][0] == Fraction(0)
        assert B[2][1] == Fraction(MU)
        assert B[2][2] == Fraction(K - MU)

    def test_equitability_edge_counts(self):
        # Between cells: n_i * B[i][j] = n_j * B[j][i]
        B, (n0, n1, n2) = self.B, self.sizes
        # C0 <-> C1
        assert n0 * B[0][1] == n1 * B[1][0]
        # C1 <-> C2
        assert n1 * B[1][2] == n2 * B[2][1]


class TestQuotientEigenvalues:
    def setup_method(self):
        B, _ = trivial_equitable_partition()
        self.eigs, self.v_k, self.v_r, self.v_s = quotient_matrix_eigenvalues_3cell(B)

    def test_eigenvalue_set(self):
        assert set(self.eigs) == {Fraction(K), Fraction(R), Fraction(S)}

    def test_eigenvalues_are_srg_spectrum(self):
        srg_spectrum = {Fraction(K), Fraction(R), Fraction(S)}
        for e in self.eigs:
            assert e in srg_spectrum

    def test_perron_eigenvector(self):
        # Perron eigenvector is [1,1,1]
        assert self.v_k == [Fraction(1), Fraction(1), Fraction(1)]


class TestCharacteristicPolynomial:
    def setup_method(self):
        B, _ = trivial_equitable_partition()
        self.tr, self.sum_minors, self.det = characteristic_polynomial_3cell(B)

    def test_trace(self):
        assert self.tr == Fraction(10)  # k + r + s = 12 + 2 - 4 = 10

    def test_det(self):
        assert self.det == Fraction(-96)  # k * r * s = 12 * 2 * (-4) = -96

    def test_sum_of_minors(self):
        assert self.sum_minors == Fraction(-32)

    def test_char_poly_factors(self):
        def p(x): return x**3 - 10*x**2 - 32*x + 96
        assert p(K) == 0
        assert p(R) == 0
        assert p(S) == 0

    def test_det_equals_product_of_eigenvalues(self):
        # det(B) = k * r * s = 12 * 2 * (-4) = -96
        assert self.det == Fraction(K * R * S)


class TestTwoCellPartition:
    def setup_method(self):
        self.B2, self.sizes, self.info = two_cell_partition_line_spread()

    def test_cell_sizes(self):
        n0, n1 = self.sizes
        assert n0 == 4   # = q+1
        assert n1 == 36
        assert n0 + n1 == V

    def test_equitability(self):
        B2, (n0, n1) = self.B2, self.sizes
        assert n0 * B2[0][1] == n1 * B2[1][0]

    def test_eigenvalues(self):
        tr, det = self.info
        assert tr == Fraction(14)
        assert det == Fraction(24)
        # char poly: x^2 - 14x + 24 = (x-12)(x-2)
        def p2(x): return x**2 - 14*x + 24
        assert p2(12) == 0
        assert p2(2) == 0

    def test_two_cell_misses_s(self):
        # 2-cell spread partition has eigenvalues {k, r} only -- no s=-4
        tr, det = self.info
        # roots of x^2 - 14x + 24
        # Sum = 14 = k + r = 12 + 2
        # product = 24 = k * r = 12 * 2
        assert tr == Fraction(K + R)
        assert det == Fraction(K * R)


class TestInterlacingTheorem:
    def test_interlacing_is_sharp(self):
        _, _, sharp = interlacing_theorem_bounds()
        assert sharp is True

    def test_quotient_eigs_are_srg_eigs(self):
        q_eigs, srg_eigs, _ = interlacing_theorem_bounds()
        for e in q_eigs:
            assert e in srg_eigs


class TestTraceIdentities:
    def setup_method(self):
        self.traces = quotient_matrix_trace_identities()

    def test_trace_B1(self):
        assert self.traces[1] == Fraction(10)  # k + r + s

    def test_trace_B2(self):
        assert self.traces[2] == Fraction(164)  # 144 + 4 + 16

    def test_trace_B3(self):
        assert self.traces[3] == Fraction(1672)  # 1728 + 8 - 64

    def test_trace_B4(self):
        assert self.traces[4] == Fraction(21008)  # 20736 + 16 + 256


class TestAllMasterIdentities:
    def test_full_packet(self):
        results = equitable_partition_main()
        assert results["srg_params_ok"] is True
        assert results["interlacing_sharp"] is True
        assert results["quotient_eigs_in_srg_spectrum"] is True
        assert results["n_verified"] == 14
