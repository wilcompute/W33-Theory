"""
Tests for Part CCXCVII: Eigenvalue Interlacing in W(3,3).
"""

import pytest
from exploration.PART_CCXCVII_INTERLACING_BRIDGE import (
    V, K, LAM, MU, K2, EDGES, MULT_R, MULT_S,
    R_EIG, S_EIG,
    EW_GAUGE_4, Q,
    ALPHA, OMEGA,
    SINGLE_EIG, SINGLE_LOWER, SINGLE_UPPER, SINGLE_INTERLACES,
    INDEP_M, INDEP_LOWER_IDX, INDEP_LAMBDA_AT_31, INDEP_LAMBDA_AT_1, INDEP_INTERLACES,
    CLIQUE_M, CLIQUE_EIG_MAX, CLIQUE_EIG_MIN,
    CLIQUE_LOWER_IDX, CLIQUE_UPPER_IDX,
    CLIQUE_LAMBDA_AT_37, CLIQUE_LAMBDA_AT_4, CLIQUE_INTERLACES,
    INTERLACING_UPPER, INTERLACING_LOWER,
    CLIQUE_DEGREE_IN_H, CLIQUE_DEGREE_LE_K, CLIQUE_EIG_MAX_LE_K,
    SPLIT_POS, SPLIT_EQ_V_MINUS_MULT_S, AT_SPLIT, AT_FIRST_S,
    LAMBDA_AT_ALPHA, LAMBDA_AT_ALPHA_EQ_REIG,
    RAMANUJAN_LHS_SQ, RAMANUJAN_RHS, IS_RAMANUJAN,
    EIG_SPREAD, EIG_SPREAD_EQ_DENOM,
    EIG_PRODUCT, EIG_PRODUCT_VALUE, EIG_PRODUCT_CHECK, EIG_PRODUCT_FROM_EDGES,
    V_MINUS_MULT_S,
    eigval_at,
    verify_all, build_ccxcvii_summary,
)


class TestSRGConstants:
    def test_v(self):      assert V == 40
    def test_k(self):      assert K == 12
    def test_lam(self):    assert LAM == 2
    def test_mu(self):     assert MU == 4
    def test_mult_r(self): assert MULT_R == 24
    def test_mult_s(self): assert MULT_S == 15
    def test_edges(self):  assert EDGES == 240


class TestEigvalAt:
    def test_pos1(self):   assert eigval_at(1)  == K
    def test_pos2(self):   assert eigval_at(2)  == R_EIG
    def test_pos10(self):  assert eigval_at(10) == R_EIG
    def test_pos25(self):  assert eigval_at(25) == R_EIG
    def test_pos26(self):  assert eigval_at(26) == S_EIG
    def test_pos40(self):  assert eigval_at(40) == S_EIG


class TestSingleVertex:
    def test_single_eig(self):      assert SINGLE_EIG == 0
    def test_single_lower(self):    assert SINGLE_LOWER == S_EIG
    def test_single_upper(self):    assert SINGLE_UPPER == K
    def test_interlaces(self):      assert SINGLE_INTERLACES is True
    def test_s_le_0(self):          assert S_EIG <= 0
    def test_0_le_k(self):          assert 0 <= K


class TestIndependentSet:
    def test_indep_m(self):             assert INDEP_M == ALPHA
    def test_lower_idx(self):           assert INDEP_LOWER_IDX == 31
    def test_lambda_at_31(self):        assert INDEP_LAMBDA_AT_31 == S_EIG
    def test_lambda_at_1(self):         assert INDEP_LAMBDA_AT_1 == K
    def test_interlaces(self):          assert INDEP_INTERLACES is True
    def test_lower_le_zero(self):       assert INDEP_LAMBDA_AT_31 <= 0
    def test_zero_le_upper(self):       assert 0 <= INDEP_LAMBDA_AT_1


class TestClique:
    def test_clique_m(self):            assert CLIQUE_M == OMEGA
    def test_clique_eig_max(self):      assert CLIQUE_EIG_MAX == 3
    def test_clique_eig_min(self):      assert CLIQUE_EIG_MIN == -1
    def test_clique_lower_idx(self):    assert CLIQUE_LOWER_IDX == 37
    def test_clique_upper_idx(self):    assert CLIQUE_UPPER_IDX == 4
    def test_lambda_at_37(self):        assert CLIQUE_LAMBDA_AT_37 == S_EIG
    def test_lambda_at_4(self):         assert CLIQUE_LAMBDA_AT_4 == R_EIG
    def test_clique_interlaces(self):   assert CLIQUE_INTERLACES is True
    def test_lower_le_min(self):        assert CLIQUE_LAMBDA_AT_37 <= CLIQUE_EIG_MIN
    def test_min_le_upper(self):        assert CLIQUE_EIG_MIN <= CLIQUE_LAMBDA_AT_4


class TestBounds:
    def test_upper(self):               assert INTERLACING_UPPER == K
    def test_lower(self):               assert INTERLACING_LOWER == S_EIG
    def test_clique_deg(self):          assert CLIQUE_DEGREE_IN_H == OMEGA - 1
    def test_clique_deg_le_k(self):     assert CLIQUE_DEGREE_LE_K is True
    def test_clique_eig_le_k(self):     assert CLIQUE_EIG_MAX_LE_K is True


class TestPositionArithmetic:
    def test_split_pos(self):           assert SPLIT_POS == 25
    def test_v_minus_mult_s(self):      assert V_MINUS_MULT_S == 25
    def test_split_eq(self):            assert SPLIT_EQ_V_MINUS_MULT_S is True
    def test_at_split(self):            assert AT_SPLIT == R_EIG
    def test_at_first_s(self):          assert AT_FIRST_S == S_EIG
    def test_lambda_at_alpha(self):     assert LAMBDA_AT_ALPHA == R_EIG
    def test_lambda_alpha_eq(self):     assert LAMBDA_AT_ALPHA_EQ_REIG is True


class TestRamanujan:
    def test_lhs_sq(self):              assert RAMANUJAN_LHS_SQ == R_EIG ** 2
    def test_rhs(self):                 assert RAMANUJAN_RHS == 4 * (K - 1)
    def test_is_ramanujan(self):        assert IS_RAMANUJAN is True
    def test_4_le_44(self):             assert RAMANUJAN_LHS_SQ <= RAMANUJAN_RHS


class TestSpreadProduct:
    def test_spread(self):              assert EIG_SPREAD == 16
    def test_spread_eq_denom(self):     assert EIG_SPREAD_EQ_DENOM is True
    def test_spread_ew_sq(self):        assert EIG_SPREAD == EW_GAUGE_4 ** 2
    def test_product(self):             assert EIG_PRODUCT == 48
    def test_product_value(self):       assert EIG_PRODUCT_VALUE == 48
    def test_product_check(self):       assert EIG_PRODUCT_CHECK is True
    def test_product_from_edges(self):  assert EIG_PRODUCT_FROM_EDGES == 48
    def test_product_edges_div5(self):  assert EIG_PRODUCT_FROM_EDGES == EDGES // 5


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_27_pass(self):
        _, passed, _ = verify_all()
        assert passed == 27

    def test_no_failures(self):
        checks, _, _ = verify_all()
        failed = [name for name, ok, _ in checks if not ok]
        assert failed == [], f"Failed: {failed}"


class TestBuildSummary:
    def setup_method(self):
        self.s = build_ccxcvii_summary()

    def test_part(self):           assert self.s["part"] == "CCXCVII"
    def test_title(self):          assert "Interlacing" in self.s["title"]
    def test_checks_pass(self):    assert self.s["checks_pass"] == 27
    def test_checks_total(self):   assert self.s["checks_total"] == 27
    def test_status(self):         assert self.s["status"] == "ALL_PASS"
    def test_interlacing_upper(self): assert self.s["interlacing_upper"] == K
    def test_interlacing_lower(self): assert self.s["interlacing_lower"] == S_EIG
    def test_eig_spread(self):     assert self.s["eig_spread"] == 16
    def test_eig_product(self):    assert self.s["eig_product"] == 48
    def test_ramanujan(self):      assert self.s["is_ramanujan"] is True
    def test_split_pos(self):      assert self.s["split_pos"] == 25
    def test_clique_eig_max(self): assert self.s["clique_eig_max"] == 3
    def test_discoveries(self):
        assert isinstance(self.s["discoveries"], list)
        assert len(self.s["discoveries"]) >= 5
