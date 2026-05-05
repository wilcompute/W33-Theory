"""Tests for PART CCCXII — Equitable Partition & Interlacing Eigenvalues of W(3,3)."""

import sys
import os
import pytest
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))
from PART_CCCXII_EQUITABLE_PARTITION_BRIDGE import (
    V, K, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    M0, M1, M2,
    Q_00, Q_01, Q_02, Q_10, Q_11, Q_12, Q_20, Q_21, Q_22,
    Q, Q_EIGS, Q_TRACE, Q_DET,
    Q_SQ, Q_SQ_00, Q_SQ_11, Q_SQ_22, Q_SQ_TRACE,
    verify_all, build_cccxii_summary,
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


class TestPartitionStructure:
    def test_M0_is_one(self):
        assert M0 == 1

    def test_M1_equals_K(self):
        assert M1 == K
        assert M1 == 12

    def test_M2_equals_v_minus_1_minus_K(self):
        assert M2 == V - 1 - K
        assert M2 == 27

    def test_partition_sum_to_v(self):
        assert M0 + M1 + M2 == V

    def test_M2_equals_GUT_DIM(self):
        assert M2 == GUT_DIM


class TestQuotientMatrixStructure:
    def test_Q_shape(self):
        assert len(Q) == 3
        assert all(len(row) == 3 for row in Q)

    def test_Q_00_zero(self):
        assert Q_00 == 0
        assert Q[0][0] == 0

    def test_Q_01_equals_K(self):
        assert Q_01 == K
        assert Q[0][1] == K

    def test_Q_02_zero(self):
        assert Q_02 == 0
        assert Q[0][2] == 0

    def test_Q_10_equals_one(self):
        assert Q_10 == 1
        assert Q[1][0] == 1

    def test_Q_11_equals_lambda(self):
        assert Q_11 == LAM
        assert Q[1][1] == LAM

    def test_Q_12_equals_K_minus_1_minus_lambda(self):
        assert Q_12 == K - 1 - LAM
        assert Q_12 == 9
        assert Q[1][2] == 9

    def test_Q_20_zero(self):
        assert Q_20 == 0
        assert Q[2][0] == 0

    def test_Q_21_equals_mu(self):
        assert Q_21 == MU
        assert Q[2][1] == MU

    def test_Q_22_equals_K_minus_mu(self):
        assert Q_22 == K - MU
        assert Q_22 == 8
        assert Q[2][2] == 8


class TestQuotientMatrixRegularity:
    """Test that Q is row-regular (each row sums to K)."""

    def test_row_0_sum(self):
        assert Q_00 + Q_01 + Q_02 == K

    def test_row_1_sum(self):
        assert Q_10 + Q_11 + Q_12 == K

    def test_row_2_sum(self):
        assert Q_20 + Q_21 + Q_22 == K


class TestQuotientMatrixEigenvalues:
    def test_eigs_are_three_values(self):
        assert len(Q_EIGS) == 3

    def test_eigs_match_SRG_spectrum(self):
        # The eigenvalues of Q are exactly K, R, S
        assert K in Q_EIGS
        assert R_EIG in Q_EIGS
        assert S_EIG in Q_EIGS

    def test_eigs_perfect_interlacing(self):
        # For this partition, eigenvalues are exactly the SRG eigenvalues
        assert set(Q_EIGS) == {K, R_EIG, S_EIG}


class TestQuotientMatrixTrace:
    def test_trace_zero_plus_lambda_plus_k_minus_mu(self):
        assert Q_TRACE == Q_00 + Q_11 + Q_22

    def test_trace_sum_of_eigenvalues(self):
        assert Q_TRACE == sum(Q_EIGS)

    def test_trace_equals_alpha(self):
        assert Q_TRACE == ALPHA
        assert Q_TRACE == 10

    def test_trace_equals_0_plus_2_plus_8(self):
        assert Q_TRACE == 0 + LAM + (K - MU)


class TestQuotientMatrixDeterminant:
    def test_determinant(self):
        assert Q_DET == K * R_EIG * S_EIG
        assert Q_DET == 12 * 2 * (-4)
        assert Q_DET == -96

    def test_det_equals_product_of_eigenvalues(self):
        product = Q_EIGS[0] * Q_EIGS[1] * Q_EIGS[2]
        assert Q_DET == product


class TestQSquared:
    def test_Q_sq_shape(self):
        assert len(Q_SQ) == 3
        assert all(len(row) == 3 for row in Q_SQ)

    def test_Q_sq_diagonal_entries(self):
        assert Q_SQ[0][0] == 12
        assert Q_SQ[1][1] == 52
        assert Q_SQ[2][2] == 100

    def test_Q_sq_trace_is_sum_of_squared_eigenvalues(self):
        eigs_sq_sum = sum(e**2 for e in Q_EIGS)
        assert Q_SQ_TRACE == eigs_sq_sum
        assert Q_SQ_TRACE == 12**2 + 2**2 + (-4)**2
        assert Q_SQ_TRACE == 144 + 4 + 16
        assert Q_SQ_TRACE == 164

    def test_Q_sq_00(self):
        assert Q_SQ_00 == 12

    def test_Q_sq_11(self):
        assert Q_SQ_11 == 52

    def test_Q_sq_22(self):
        assert Q_SQ_22 == 100


class TestSMEncodings:
    def test_Q_trace_alpha(self):
        assert Q_TRACE == ALPHA

    def test_M2_GUT_DIM(self):
        assert M2 == GUT_DIM

    def test_K_alpha_plus_lambda(self):
        assert K == ALPHA + LAM

    def test_Q_12_generations_squared(self):
        assert Q_12 == GENERATIONS ** 2

    def test_Q_22_power_of_two_generations(self):
        assert Q_22 == 2 ** GENERATIONS

    def test_M0_M1_M2_sum_V(self):
        assert M0 + M1 + M2 == V

    def test_partition_encodes_SRG_structure(self):
        # Partition sizes encode the SRG structure
        assert M1 == K
        assert M2 == V - 1 - K


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
        s = build_cccxii_summary()
        assert isinstance(s, dict)

    def test_part_is_cccxii(self):
        s = build_cccxii_summary()
        assert s["part"] == "CCCXII"

    def test_status_pass(self):
        s = build_cccxii_summary()
        assert s["status"] == "PASS"

    def test_checks_27(self):
        s = build_cccxii_summary()
        assert s["checks_total"] == 27
        assert s["checks_pass"] == 27

    def test_fields_present(self):
        s = build_cccxii_summary()
        assert "partition_sizes" in s["fields"]
        assert "Q_entries" in s["fields"]
        assert "Q_eigs" in s["fields"]

    def test_discoveries_nonempty(self):
        s = build_cccxii_summary()
        assert len(s["discoveries"]) >= 5
