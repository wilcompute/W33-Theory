"""Tests for PART CCCXI — Bose-Mesner Algebra of W(3,3)."""

import sys
import os
import pytest
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))
from PART_CCCXI_BOSE_MESNER_BRIDGE import (
    V, K, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    K0, K1, K2,
    P11_0, P11_1, P11_2,
    P12_0, P12_1, P12_2,
    P22_0, P22_1, P22_2,
    EIGEN_P, EIGEN_TRACE_A1, EIGEN_TRACE_A2,
    BMA_DIM,
    ROW11, ROW12, ROW22,
    verify_all, build_cccxi_summary,
)


class TestSRGParameters:
    def test_vertices(self):
        assert V == 40

    def test_valency(self):
        assert K == 12

    def test_lambda_mu(self):
        assert LAM == 2
        assert MU == 4

    def test_eigenvalues(self):
        assert R_EIG == 2
        assert S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24
        assert MULT_S == 15
        assert 1 + MULT_R + MULT_S == V


class TestClassSizes:
    def test_k0(self):
        assert K0 == 1

    def test_k1(self):
        assert K1 == 12
        assert K1 == K

    def test_k2(self):
        assert K2 == 27
        assert K2 == V - 1 - K

    def test_partition(self):
        assert K0 + K1 + K2 == V


class TestIntersectionNumbersA1A1:
    """p_{11}^k: coefficients of A_1^2 = A^2 in basis {A_0, A_1, A_2}."""

    def test_P11_0_equals_k(self):
        assert P11_0 == K
        assert P11_0 == 12

    def test_P11_1_equals_lambda(self):
        assert P11_1 == LAM
        assert P11_1 == 2

    def test_P11_2_equals_mu(self):
        assert P11_2 == MU
        assert P11_2 == 4

    def test_A1_squared_formula(self):
        # A^2 = k*I + lambda*A + mu*A_2
        assert P11_0 == K and P11_1 == LAM and P11_2 == MU

    def test_row_sum_identity(self):
        # sum_k p_{11}^k * k_k = k_1^2
        assert ROW11 == K1 * K1
        assert ROW11 == 144


class TestIntersectionNumbersA1A2:
    """p_{12}^k: coefficients of A_1*A_2 = A*(J-I-A)."""

    def test_P12_0_zero(self):
        assert P12_0 == 0

    def test_P12_1(self):
        assert P12_1 == K - 1 - LAM
        assert P12_1 == 9

    def test_P12_2(self):
        assert P12_2 == K - MU
        assert P12_2 == 8

    def test_P12_1_plus_P12_2(self):
        # 9 + 8 = 17
        assert P12_1 + P12_2 == 17

    def test_row_sum_identity(self):
        # sum_k p_{12}^k * k_k = k_1 * k_2
        assert ROW12 == K1 * K2
        assert ROW12 == 324


class TestIntersectionNumbersA2A2:
    """p_{22}^k: coefficients of A_2^2 = (J-I-A)^2."""

    def test_P22_0_equals_k2(self):
        assert P22_0 == K2
        assert P22_0 == 27

    def test_P22_1_equals_18(self):
        assert P22_1 == 18

    def test_P22_2_equals_18(self):
        assert P22_2 == 18

    def test_P22_1_equals_P22_2(self):
        # Both off-diagonal parameters are equal
        assert P22_1 == P22_2

    def test_row_sum_identity(self):
        # sum_k p_{22}^k * k_k = k_2^2
        assert ROW22 == K2 * K2
        assert ROW22 == 729


class TestEigenvalueMatrix:
    """Tests for the P eigenvalue matrix and trace constraints."""

    def test_P_shape(self):
        assert len(EIGEN_P) == 3
        assert all(len(row) == 3 for row in EIGEN_P)

    def test_P_col0_all_ones(self):
        # A_0 = I, eigenvalue 1 for all eigenspaces
        assert all(EIGEN_P[i][0] == 1 for i in range(3))

    def test_P_col1_eigenvalues(self):
        # A_1 has eigenvalues k, r, s
        assert EIGEN_P[0][1] == K    # 12
        assert EIGEN_P[1][1] == R_EIG  # 2
        assert EIGEN_P[2][1] == S_EIG  # -4

    def test_P_col2_eigenvalues(self):
        # A_2 has eigenvalues k2, -(1+r), -(1+s)
        assert EIGEN_P[0][2] == K2          # 27
        assert EIGEN_P[1][2] == -(1 + R_EIG)  # -3
        assert EIGEN_P[2][2] == -(1 + S_EIG)  # 3

    def test_trace_A1_zero(self):
        assert EIGEN_TRACE_A1 == 0

    def test_trace_A2_zero(self):
        assert EIGEN_TRACE_A2 == 0

    def test_trace_weighted_identity(self):
        # Multiplicities sum to V
        assert 1 + MULT_R + MULT_S == V


class TestBMADimension:
    def test_dim_is_3(self):
        assert BMA_DIM == 3

    def test_dim_equals_num_classes_plus_1(self):
        assert BMA_DIM == 3  # 1 trivial + 2 non-trivial = 3 classes

    def test_dim_equals_generations(self):
        assert BMA_DIM == GENERATIONS


class TestSMEncodings:
    def test_P11_0_alpha_plus_lambda(self):
        # K = 12 = ALPHA + LAM = 10 + 2
        assert P11_0 == ALPHA + LAM

    def test_P12_1_alpha_minus_1(self):
        # 9 = ALPHA - 1 = 10 - 1
        assert P12_1 == ALPHA - 1

    def test_P12_1_generations_squared(self):
        # 9 = 3^2 = GENERATIONS^2
        assert P12_1 == GENERATIONS ** 2

    def test_P22_0_GUT_DIM(self):
        # 27 = GUT_DIM (E6 dimension count)
        assert P22_0 == GUT_DIM

    def test_P22_1_two_gen_squared(self):
        # 18 = 2 * GENERATIONS^2 = 2 * 9
        assert P22_1 == 2 * GENERATIONS ** 2

    def test_P12_2_power_of_two(self):
        # 8 = 2^3 = 2^GENERATIONS
        assert P12_2 == 2 ** GENERATIONS

    def test_BMA_dim_generations(self):
        assert BMA_DIM == GENERATIONS


class TestVerifyAll:
    def test_returns_tuple_of_three(self):
        result = verify_all()
        assert len(result) == 3

    def test_total_is_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total

    def test_check_names_unique(self):
        checks, _, _ = verify_all()
        names = [c["name"] for c in checks]
        assert len(names) == len(set(names))


class TestBuildSummary:
    def test_returns_dict(self):
        s = build_cccxi_summary()
        assert isinstance(s, dict)

    def test_part_is_cccxi(self):
        s = build_cccxi_summary()
        assert s["part"] == "CCCXI"

    def test_status_pass(self):
        s = build_cccxi_summary()
        assert s["status"] == "PASS"

    def test_checks_27(self):
        s = build_cccxi_summary()
        assert s["checks_total"] == 27

    def test_fields_present(self):
        s = build_cccxi_summary()
        assert "P11" in s["fields"]
        assert "P12" in s["fields"]
        assert "P22" in s["fields"]

    def test_discoveries_nonempty(self):
        s = build_cccxi_summary()
        assert len(s["discoveries"]) >= 5
