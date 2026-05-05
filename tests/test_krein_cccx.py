"""Tests for PART CCCX — Krein Parameters of W(3,3)."""

import pytest
from fractions import Fraction
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from exploration.PART_CCCX_KREIN_BRIDGE import (
    V, K, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    K0, K1, K2, M0, M1, M2,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    Q00, Q01, Q02, Q10, Q11, Q12, Q20, Q21, Q22,
    Q_COL0_WEIGHTEDSUM, Q_COL1_WEIGHTEDSUM, Q_COL2_WEIGHTEDSUM,
    Q_COL0_CHECK, Q_COL1_ZERO, Q_COL2_ZERO,
    KR_11_0, KR_11_1, KR_11_2,
    KR_12_0, KR_12_1, KR_12_2,
    KR_22_0, KR_22_1, KR_22_2,
    KR_ALL_NONNEG,
    KR_11_1_NUM, KR_11_1_DEN, KR_11_2_NUM, KR_11_2_DEN,
    KR_22_0_SM, KR_22_0_SM2,
    KR_22_2_NUM, KR_22_2_DEN, KR_22_2_SM,
    KR_12_1_NUM, KR_12_1_NUM_SM,
    KR_12_2_NUM, KR_12_2_NUM_SM,
    KR_SUM_NONTRIVIAL, KR_SUM_NONTRIVIAL_SM, KR_SUM_SM2,
    KR_COMMON_DEN, KR_DEN_SM,
    verify_all, build_cccx_summary,
)


class TestSRGConstants:
    def test_srg_params(self):
        assert V == 40 and K == 12 and LAM == 2 and MU == 4

    def test_edges(self):
        assert EDGES == 240

    def test_eigenvalues(self):
        assert R_EIG == 2 and S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24 and MULT_S == 15

    def test_class_sizes(self):
        assert K0 == 1 and K1 == 12 and K2 == 27
        assert K0 + K1 + K2 == V - 1 + 1  # = V


class TestQMatrix:
    def test_row0(self):
        assert Q00 == Fraction(1) and Q01 == Fraction(24) and Q02 == Fraction(15)

    def test_row1(self):
        assert Q10 == Fraction(1) and Q11 == Fraction(4) and Q12 == Fraction(-5)

    def test_row2(self):
        assert Q20 == Fraction(1) and Q21 == Fraction(-8, 3) and Q22 == Fraction(5, 3)

    def test_col0_sum_V(self):
        assert Q_COL0_WEIGHTEDSUM == V
        assert Q_COL0_CHECK

    def test_col1_orthogonality(self):
        assert Q_COL1_WEIGHTEDSUM == 0
        assert Q_COL1_ZERO

    def test_col2_orthogonality(self):
        assert Q_COL2_WEIGHTEDSUM == 0
        assert Q_COL2_ZERO

    def test_q_row1_sum(self):
        # Row 1 entry sums: 1 + 4 + (-5) = 0 (sum of dual eigenvalues for non-trivial class)
        assert Q10 + Q11 + Q12 == 0


class TestKreinParameters:
    def test_kr_11_0(self):
        assert KR_11_0 == Fraction(24)  # = MULT_R

    def test_kr_11_1(self):
        assert KR_11_1 == Fraction(44, 3)

    def test_kr_11_2(self):
        assert KR_11_2 == Fraction(40, 3)

    def test_kr_12_0_orthogonality(self):
        assert KR_12_0 == Fraction(0)

    def test_kr_12_1(self):
        assert KR_12_1 == Fraction(25, 3)

    def test_kr_12_2(self):
        assert KR_12_2 == Fraction(32, 3)

    def test_kr_22_0(self):
        assert KR_22_0 == Fraction(15)  # = MULT_S

    def test_kr_22_1(self):
        assert KR_22_1 == Fraction(20, 3)

    def test_kr_22_2(self):
        assert KR_22_2 == Fraction(10, 3)


class TestKreinFeasibility:
    def test_all_nonneg(self):
        assert KR_ALL_NONNEG

    def test_symmetry_12_21(self):
        # q_{12}^k = q_{21}^k by symmetry of the Hadamard product
        from exploration.PART_CCCX_KREIN_BRIDGE import _krein, _Qmat, _Kclass, _Mmult
        for k in range(3):
            assert _krein(1, 2, k, _Qmat, _Kclass, _Mmult, V) == \
                   _krein(2, 1, k, _Qmat, _Kclass, _Mmult, V)

    def test_q_00_0(self):
        # q_{00}^0 = 1 (identity idempotent)
        from exploration.PART_CCCX_KREIN_BRIDGE import _krein, _Qmat, _Kclass, _Mmult
        q000 = _krein(0, 0, 0, _Qmat, _Kclass, _Mmult, V)
        assert q000 == Fraction(1)

    def test_q_01_1(self):
        # q_{01}^1 = 1 (identity acts trivially)
        from exploration.PART_CCCX_KREIN_BRIDGE import _krein, _Qmat, _Kclass, _Mmult
        q011 = _krein(0, 1, 1, _Qmat, _Kclass, _Mmult, V)
        assert q011 == Fraction(1)


class TestSMEncodings:
    def test_kr_11_1_numerator_SM(self):
        assert KR_11_1_NUM == 44
        assert KR_11_1_NUM == ALPHA * EW_GAUGE_4 + EW_GAUGE_4

    def test_kr_11_1_denominator_SM(self):
        assert KR_11_1_DEN == GENERATIONS

    def test_kr_11_2_numerator_SM(self):
        assert KR_11_2_NUM == V
        assert KR_11_2_NUM == ALPHA * EW_GAUGE_4

    def test_kr_22_0_SM(self):
        assert KR_22_0_SM  # KR_22_0 == MULT_S
        assert int(KR_22_0) == ALPHA + GENERATIONS + LAM  # 10+3+2=15

    def test_kr_22_2_SM(self):
        assert KR_22_2_NUM == ALPHA
        assert KR_22_2_DEN == GENERATIONS
        assert KR_22_2_SM

    def test_kr_12_1_numerator_SM(self):
        assert KR_12_1_NUM == (MU + 1) ** 2  # 5^2 = 25
        assert KR_12_1_NUM_SM

    def test_kr_12_2_numerator_SM(self):
        assert KR_12_2_NUM == 2 ** (GENERATIONS + LAM)  # 2^5 = 32
        assert KR_12_2_NUM_SM


class TestSpectralSums:
    def test_sum_nontrivial(self):
        expected = (Fraction(44, 3) + Fraction(40, 3) + Fraction(25, 3) +
                    Fraction(32, 3) + Fraction(20, 3) + Fraction(10, 3))
        assert KR_SUM_NONTRIVIAL == expected
        assert KR_SUM_NONTRIVIAL == Fraction(57)

    def test_sum_nontrivial_SM(self):
        assert KR_SUM_NONTRIVIAL_SM  # == V + MULT_S + LAM = 57
        assert KR_SUM_SM2

    def test_common_denominator(self):
        assert KR_COMMON_DEN == Fraction(3)
        assert KR_DEN_SM  # == GENERATIONS

    def test_kr11_sum(self):
        # KR_11_1 + KR_11_2 = 44/3 + 40/3 = 84/3 = 28
        assert KR_11_1 + KR_11_2 == Fraction(28)

    def test_kr22_sum(self):
        # KR_22_1 + KR_22_2 = 20/3 + 10/3 = 30/3 = 10
        assert KR_22_1 + KR_22_2 == Fraction(10)
        assert int(KR_22_1 + KR_22_2) == ALPHA


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_exactly_27_checks(self):
        checks, passed, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == 27

    def test_check_keys(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "name" in c and "ok" in c


class TestBuildSummary:
    def test_returns_dict(self):
        s = build_cccx_summary()
        assert isinstance(s, dict)

    def test_part_label(self):
        s = build_cccx_summary()
        assert s["part"] == "CCCX"

    def test_title(self):
        s = build_cccx_summary()
        assert "Krein" in s["title"]

    def test_status_pass(self):
        s = build_cccx_summary()
        assert s["status"] == "PASS"

    def test_checks(self):
        s = build_cccx_summary()
        assert s["checks_pass"] == 27 and s["checks_total"] == 27

    def test_fields_present(self):
        s = build_cccx_summary()
        assert "KR_11_0" in s["fields"] and "KR_22_2" in s["fields"]
