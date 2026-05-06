"""
Tests for PART CCCXLVI -- Q-Matrix Coupling Ratios and the Weinberg Angle
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCXLVI_Q_MATRIX_WEINBERG_BRIDGE import (
    V, K, LAM, MU, R_EIG, S_EIG,
    MULT_R, MULT_S,
    K0, K1, K2,
    EW_GAUGE_4, GENERATIONS, GUT_DIM, SU5_DIM, SU5_ADJ, GLUON_COUNT,
    Q, Q00, Q01, Q02, Q10, Q11, Q12, Q20, Q21, Q22,
    KAPPA_Y, SIN2_W_GUT, COS2_W_GUT,
    _pq_row_col, _col_inner,
    verify_all, build_cccxlvi_summary,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def verify_result():
    return verify_all()


@pytest.fixture(scope="module")
def summary():
    return build_cccxlvi_summary()


# ── Group 1: Q matrix exact values ───────────────────────────────────────────

class TestQMatrixValues:
    def test_Q00(self):
        assert Q00 == Fraction(1)

    def test_Q01_equals_mult_r(self):
        assert Q01 == Fraction(MULT_R)

    def test_Q01_value(self):
        assert Q01 == 24

    def test_Q02_equals_mult_s(self):
        assert Q02 == Fraction(MULT_S)

    def test_Q02_value(self):
        assert Q02 == 15

    def test_Q10(self):
        assert Q10 == Fraction(1)

    def test_Q11_equals_mu(self):
        assert Q11 == Fraction(MU)

    def test_Q11_value(self):
        assert Q11 == 4

    def test_Q12_equals_neg_mu_plus1(self):
        assert Q12 == Fraction(-(MU + 1))

    def test_Q12_value(self):
        assert Q12 == -5

    def test_Q20(self):
        assert Q20 == Fraction(1)

    def test_Q21_formula(self):
        assert Q21 == Fraction(-(K - MU), GENERATIONS)

    def test_Q21_value(self):
        assert Q21 == Fraction(-8, 3)

    def test_Q22_formula(self):
        assert Q22 == Fraction(MU + 1, GENERATIONS)

    def test_Q22_value(self):
        assert Q22 == Fraction(5, 3)


# ── Group 2: SRG parameter encodings ─────────────────────────────────────────

class TestSRGEncodings:
    def test_gluon_count_from_Q21(self):
        assert abs(Q21) * GENERATIONS == GLUON_COUNT

    def test_gluon_count_equals_K_minus_MU(self):
        assert GLUON_COUNT == K - MU

    def test_gluon_count_value(self):
        assert GLUON_COUNT == 8

    def test_su5_dim_from_Q12(self):
        assert abs(Q12) == SU5_DIM

    def test_su5_dim_value(self):
        assert SU5_DIM == 5

    def test_gluons_equals_V_over_SU5(self):
        assert K - MU == V // SU5_DIM

    def test_ew_gauge_from_Q11(self):
        assert Q11 == EW_GAUGE_4


# ── Group 3: Weinberg angle derivation ───────────────────────────────────────

class TestWeinbergAngle:
    def test_kappa_y_equals_Q22(self):
        assert KAPPA_Y == Q22

    def test_kappa_y_value(self):
        assert KAPPA_Y == Fraction(5, 3)

    def test_sin2_w_from_kappa(self):
        assert SIN2_W_GUT == Fraction(1) / (1 + KAPPA_Y)

    def test_sin2_w_value(self):
        assert SIN2_W_GUT == Fraction(3, 8)

    def test_sin2_w_from_generations_and_su5(self):
        assert SIN2_W_GUT == Fraction(GENERATIONS, GENERATIONS + SU5_DIM)

    def test_cos2_w_value(self):
        assert COS2_W_GUT == Fraction(5, 8)

    def test_unitarity(self):
        assert SIN2_W_GUT + COS2_W_GUT == 1

    def test_8_sin2_w_equals_3(self):
        assert GLUON_COUNT * SIN2_W_GUT == GENERATIONS


# ── Group 4: SM coupling cross-checks ────────────────────────────────────────

class TestSMCouplingCrossChecks:
    def test_Q11_is_EW_GAUGE_4(self):
        assert Q11 == EW_GAUGE_4 == 4

    def test_abs_Q12_is_SU5_DIM(self):
        assert abs(Q12) == SU5_DIM == 5

    def test_gluon_count_equals_8(self):
        assert GLUON_COUNT == 8

    def test_SU5_ADJ(self):
        assert SU5_ADJ == SU5_DIM ** 2 - 1 == 24

    def test_mult_r_equals_SU5_ADJ(self):
        assert MULT_R == SU5_ADJ

    def test_mult_s_equals_SU5_matter(self):
        assert MULT_S == 15

    def test_Q_row0_first_entry(self):
        assert Q[0][0] == 1


# ── Group 5: Q column weighted orthogonality ─────────────────────────────────

class TestColumnOrthogonality:
    def test_col0_norm_equals_m0(self):
        assert _col_inner(0, 0) == Fraction(1)

    def test_col1_norm_equals_m1(self):
        assert _col_inner(1, 1) == Fraction(MULT_R)

    def test_col2_norm_equals_m2(self):
        assert _col_inner(2, 2) == Fraction(MULT_S)

    def test_col0_col1_orthogonal(self):
        assert _col_inner(0, 1) == 0

    def test_col0_col2_orthogonal(self):
        assert _col_inner(0, 2) == 0

    def test_col1_col2_orthogonal(self):
        assert _col_inner(1, 2) == 0


# ── PQ = vI sanity ────────────────────────────────────────────────────────────

class TestPQProduct:
    def test_pq_diagonal_00(self):
        assert _pq_row_col(0, 0) == V

    def test_pq_diagonal_11(self):
        assert _pq_row_col(1, 1) == V

    def test_pq_diagonal_22(self):
        assert _pq_row_col(2, 2) == V

    def test_pq_offdiag_01(self):
        assert _pq_row_col(0, 1) == 0

    def test_pq_offdiag_10(self):
        assert _pq_row_col(1, 0) == 0

    def test_pq_offdiag_12(self):
        assert _pq_row_col(1, 2) == 0


# ── Master verify_all ─────────────────────────────────────────────────────────

class TestVerifyAll:
    def test_all_27_checks_pass(self, verify_result):
        checks, passed, total = verify_result
        assert total == 27
        assert passed == 27

    def test_no_failed_checks(self, verify_result):
        checks, passed, total = verify_result
        failed = [c["name"] for c in checks if not c["passed"]]
        assert failed == [], f"Failed: {failed}"


# ── Summary JSON ──────────────────────────────────────────────────────────────

class TestSummary:
    def test_summary_status_pass(self, summary):
        assert summary["status"] == "PASS"

    def test_summary_checks(self, summary):
        assert summary["checks_pass"] == 27
        assert summary["checks_total"] == 27

    def test_summary_kappa_y(self, summary):
        assert summary["fields"]["KAPPA_Y"] == "5/3"

    def test_summary_sin2_w(self, summary):
        assert summary["fields"]["SIN2_W_GUT"] == "3/8"

    def test_summary_Q22(self, summary):
        assert summary["fields"]["Q22"] == "5/3"

    def test_summary_discoveries_count(self, summary):
        assert len(summary["discoveries"]) == 7
