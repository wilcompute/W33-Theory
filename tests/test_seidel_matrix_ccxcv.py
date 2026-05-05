"""
Tests for Part CCXCV: Seidel Matrix Eigenvalue Structure of W(3,3).
"""

import pytest
from exploration.PART_CCXCV_SEIDEL_MATRIX_BRIDGE import (
    # SRG constants
    V, K, LAM, MU, K2, EDGES, MULT_R, MULT_S,
    # SRG eigenvalues
    R_EIG, S_EIG,
    # SM constants
    EW_GAUGE_4, QUARKS_36, Q,
    # Seidel eigenvalues and multiplicities
    TAU_0, TAU_R, TAU_S,
    MULT_TAU_0, MULT_TAU_R, MULT_TAU_S,
    # Spectral invariants
    SEIDEL_TRACE, SEIDEL_TRACE_SQ, SEIDEL_TRACE_SQ_FORMULA,
    # Equiangular lines
    ANGLE_DENOM, EMBEDDING_DIM,
    # Cross-checks
    ABS_TAU_R, TAU_S_FROM_S, ABS_TAU_R_FROM_Q, MULT_DIFF,
    # Products / sums / differences
    TAU_PRODUCT, PRODUCT_FORMULA, TAU_SUM_0S, SUM_0S_FORMULA,
    TAU_DIFF_0S, DIFF_0S_FORMULA,
    # SM
    QUARKS_MINUS_MULT_R, TAU_0_IS_MULT_S, HALF_TAU_0_PLUS1,
    # Functions
    verify_all, build_ccxcv_summary,
)


class TestSRGConstants:
    def test_v(self):      assert V == 40
    def test_k(self):      assert K == 12
    def test_lam(self):    assert LAM == 2
    def test_mu(self):     assert MU == 4
    def test_k2(self):     assert K2 == 27
    def test_edges(self):  assert EDGES == 240
    def test_mult_r(self): assert MULT_R == 24
    def test_mult_s(self): assert MULT_S == 15
    def test_mult_sum(self): assert 1 + MULT_R + MULT_S == V


class TestSRGEigenvalues:
    def test_r_eig(self):   assert R_EIG == 2
    def test_s_eig(self):   assert S_EIG == -4
    def test_s_eig_neg(self): assert S_EIG < 0


class TestSeidelEigenvalues:
    def test_tau_0(self):  assert TAU_0 == 15
    def test_tau_r(self):  assert TAU_R == -5
    def test_tau_s(self):  assert TAU_S == 7

    def test_tau_0_formula(self):  assert TAU_0 == V - 1 - 2 * K
    def test_tau_r_formula(self):  assert TAU_R == -(1 + 2 * R_EIG)
    def test_tau_s_formula(self):  assert TAU_S == -(1 + 2 * S_EIG)

    def test_tau_0_pos(self):  assert TAU_0 > 0
    def test_tau_r_neg(self):  assert TAU_R < 0
    def test_tau_s_pos(self):  assert TAU_S > 0


class TestSeidelMultiplicities:
    def test_mult_tau_0(self):    assert MULT_TAU_0 == 1
    def test_mult_tau_r(self):    assert MULT_TAU_R == 24
    def test_mult_tau_s(self):    assert MULT_TAU_S == 15
    def test_mult_tau_r_eq_mult_r(self): assert MULT_TAU_R == MULT_R
    def test_mult_tau_s_eq_mult_s(self): assert MULT_TAU_S == MULT_S
    def test_mult_sum(self):      assert MULT_TAU_0 + MULT_TAU_R + MULT_TAU_S == V


class TestSpectralInvariants:
    def test_trace_zero(self):
        assert SEIDEL_TRACE == 0

    def test_trace_formula(self):
        assert TAU_0 * 1 + TAU_R * MULT_R + TAU_S * MULT_S == 0

    def test_trace_sq(self):
        assert SEIDEL_TRACE_SQ == 1560

    def test_trace_sq_formula(self):
        assert SEIDEL_TRACE_SQ == V * (V - 1)

    def test_trace_sq_value2(self):
        assert SEIDEL_TRACE_SQ_FORMULA == 1560

    def test_trace_sq_consistent(self):
        assert SEIDEL_TRACE_SQ == SEIDEL_TRACE_SQ_FORMULA

    def test_trace_sq_components(self):
        comp = TAU_0**2 * MULT_TAU_0 + TAU_R**2 * MULT_TAU_R + TAU_S**2 * MULT_TAU_S
        assert comp == 1560


class TestEquiangularLines:
    def test_angle_denom(self):
        assert ANGLE_DENOM == 5

    def test_angle_denom_abs_tau_r(self):
        assert ANGLE_DENOM == abs(TAU_R)

    def test_embedding_dim(self):
        assert EMBEDDING_DIM == 15

    def test_embedding_dim_eq_mult_s(self):
        assert EMBEDDING_DIM == MULT_S

    def test_lines_count(self):
        assert V == 40   # 40 equiangular lines in R^15


class TestCrossChecks:
    def test_abs_tau_r(self):
        assert ABS_TAU_R == 5

    def test_abs_tau_r_s_eig_plus1(self):
        assert ABS_TAU_R == abs(S_EIG) + 1

    def test_tau_s_from_s(self):
        assert TAU_S_FROM_S == 7

    def test_tau_s_2abs_s_minus1(self):
        assert TAU_S == TAU_S_FROM_S

    def test_abs_tau_r_q_plus2(self):
        assert ABS_TAU_R == ABS_TAU_R_FROM_Q

    def test_abs_tau_r_from_q_value(self):
        assert ABS_TAU_R_FROM_Q == Q + 2

    def test_mult_diff(self):
        assert MULT_DIFF == 9

    def test_mult_diff_q_sq(self):
        assert MULT_DIFF == Q ** 2


class TestProductsSumsDiffs:
    def test_tau_product(self):
        assert TAU_PRODUCT == -35

    def test_tau_product_formula(self):
        assert TAU_PRODUCT == -(V - MU - 1)

    def test_tau_product_consistent(self):
        assert TAU_PRODUCT == PRODUCT_FORMULA

    def test_tau_sum_0s(self):
        assert TAU_SUM_0S == 22

    def test_tau_sum_0s_formula(self):
        assert TAU_SUM_0S == 2 * K - LAM

    def test_tau_sum_0s_consistent(self):
        assert TAU_SUM_0S == SUM_0S_FORMULA

    def test_tau_diff_0s(self):
        assert TAU_DIFF_0S == 8

    def test_tau_diff_0s_formula(self):
        assert TAU_DIFF_0S == K - MU

    def test_tau_diff_0s_consistent(self):
        assert TAU_DIFF_0S == DIFF_0S_FORMULA


class TestSMConnections:
    def test_quarks_minus_mult_r(self):
        assert QUARKS_MINUS_MULT_R == 12

    def test_quarks_minus_mult_r_eq_k(self):
        assert QUARKS_MINUS_MULT_R == K

    def test_tau_0_is_mult_s(self):
        assert TAU_0_IS_MULT_S is True

    def test_tau_0_equals_mult_s(self):
        assert TAU_0 == MULT_S

    def test_half_tau_0_plus1(self):
        assert HALF_TAU_0_PLUS1 == 8

    def test_half_tau_0_plus1_k_minus_mu(self):
        assert HALF_TAU_0_PLUS1 == K - MU


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_27_pass(self):
        _, passed, total = verify_all()
        assert passed == 27

    def test_no_failed_checks(self):
        checks, _, _ = verify_all()
        failed = [name for name, ok, _ in checks if not ok]
        assert failed == [], f"Failed: {failed}"


class TestBuildSummary:
    def setup_method(self):
        self.s = build_ccxcv_summary()

    def test_part(self):            assert self.s["part"] == "CCXCV"
    def test_title_seidel(self):    assert "Seidel" in self.s["title"]
    def test_checks_pass(self):     assert self.s["checks_pass"] == 27
    def test_checks_total(self):    assert self.s["checks_total"] == 27
    def test_status(self):          assert self.s["status"] == "ALL_PASS"
    def test_tau_0(self):           assert self.s["tau_0"] == 15
    def test_tau_r(self):           assert self.s["tau_r"] == -5
    def test_tau_s(self):           assert self.s["tau_s"] == 7
    def test_mult_tau_0(self):      assert self.s["mult_tau_0"] == 1
    def test_mult_tau_r(self):      assert self.s["mult_tau_r"] == 24
    def test_mult_tau_s(self):      assert self.s["mult_tau_s"] == 15
    def test_trace(self):           assert self.s["seidel_trace"] == 0
    def test_trace_sq(self):        assert self.s["seidel_trace_sq"] == 1560
    def test_angle_denom(self):     assert self.s["angle_denom"] == 5
    def test_embedding_dim(self):   assert self.s["embedding_dim"] == 15
    def test_mult_diff(self):       assert self.s["mult_diff"] == 9
    def test_discoveries(self):
        assert isinstance(self.s["discoveries"], list)
        assert len(self.s["discoveries"]) >= 5
