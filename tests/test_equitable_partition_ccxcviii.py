"""
Tests for Part CCXCVIII: Equitable Partitions and Quotient Matrices in W(3,3).
"""

import pytest
from exploration.PART_CCXCVIII_EQUITABLE_PARTITION_BRIDGE import (
    V, K, LAM, MU, K2, EDGES, MULT_R, MULT_S,
    R_EIG, S_EIG,
    EW_GAUGE_4, Q, ALPHA,
    C0_SIZE, C1_SIZE, C2_SIZE, SIZE_CHECK,
    B3, B3_C1_C2, B3_C2_DIAG,
    B3_ROW0_SUM, B3_ROW1_SUM, B3_ROW2_SUM, ROW_SUM_EQ_K,
    QUOT3_TRACE, QUOT3_TRACE_EQ_SUM_EIGS,
    QUOT3_CHAR_K, QUOT3_CHAR_R, QUOT3_CHAR_S,
    INDEP_C0, INDEP_C1,
    B2, B2_00, B2_01, B2_10, B2_11,
    B2_ROW0_SUM, B2_ROW1_SUM, B2_ROW_SUMS_EQ_K,
    B2_TRACE, B2_DET, B2_DISC, B2_SQRT_DISC,
    B2_SQRT_DISC_EQ_EW_SQ, EIG2_PLUS, EIG2_MINUS,
    EIG2_PLUS_EQ_K, EIG2_MINUS_EQ_S,
    CROSS_EDGES, CROSS_EDGES_VALUE, CROSS_EQ_ALPHA_K, CROSS_EQ_3_EDGES_HALF,
    B2_10_EQ_MU, B2_11_EQ_K_MINUS_MU,
    char_poly_b3,
    verify_all, build_ccxcviii_summary,
)


class TestCellSizes:
    def test_c0(self):           assert C0_SIZE == 1
    def test_c1(self):           assert C1_SIZE == K
    def test_c2(self):           assert C2_SIZE == K2
    def test_total(self):        assert SIZE_CHECK is True
    def test_sum(self):          assert C0_SIZE + C1_SIZE + C2_SIZE == V


class TestQuot3Matrix:
    def test_row0(self):         assert B3[0] == [0, K, 0]
    def test_row1_c0(self):      assert B3[1][0] == 1
    def test_row1_c1(self):      assert B3[1][1] == LAM
    def test_row1_c2(self):      assert B3[1][2] == K - 1 - LAM
    def test_c1c2(self):         assert B3_C1_C2 == K - 1 - LAM
    def test_row2_c1(self):      assert B3[2][1] == MU
    def test_row2_c2(self):      assert B3[2][2] == K - MU


class TestQuot3RowSums:
    def test_row0(self):         assert B3_ROW0_SUM == K
    def test_row1(self):         assert B3_ROW1_SUM == K
    def test_row2(self):         assert B3_ROW2_SUM == K
    def test_all(self):          assert ROW_SUM_EQ_K is True


class TestQuot3Eigenvalues:
    def test_trace(self):        assert QUOT3_TRACE == K + R_EIG + S_EIG
    def test_trace_eq(self):     assert QUOT3_TRACE_EQ_SUM_EIGS is True
    def test_trace_value(self):  assert QUOT3_TRACE == 10

    def test_char_poly_k(self):  assert QUOT3_CHAR_K == 0
    def test_char_poly_r(self):  assert QUOT3_CHAR_R == 0
    def test_char_poly_s(self):  assert QUOT3_CHAR_S == 0

    def test_char_poly_fn_k(self):  assert char_poly_b3(K) == 0
    def test_char_poly_fn_r(self):  assert char_poly_b3(R_EIG) == 0
    def test_char_poly_fn_s(self):  assert char_poly_b3(S_EIG) == 0


class TestQuot2Matrix:
    def test_indep_c0(self):     assert INDEP_C0 == ALPHA
    def test_indep_c1(self):     assert INDEP_C1 == V - ALPHA
    def test_b2_00(self):        assert B2_00 == 0
    def test_b2_01(self):        assert B2_01 == K
    def test_b2_10(self):        assert B2_10 == MU
    def test_b2_10_ew(self):     assert B2_10 == EW_GAUGE_4
    def test_b2_11(self):        assert B2_11 == K - MU
    def test_row0_sum(self):     assert B2_ROW0_SUM == K
    def test_row1_sum(self):     assert B2_ROW1_SUM == K
    def test_row_sums(self):     assert B2_ROW_SUMS_EQ_K is True


class TestQuot2Eigenvalues:
    def test_trace(self):        assert B2_TRACE == K - MU
    def test_det(self):          assert B2_DET == -48
    def test_disc(self):         assert B2_DISC == 256
    def test_sqrt_disc(self):    assert B2_SQRT_DISC == 16
    def test_sqrt_ew_sq(self):   assert B2_SQRT_DISC_EQ_EW_SQ is True
    def test_sqrt_is_ew2(self):  assert B2_SQRT_DISC == EW_GAUGE_4 ** 2
    def test_eig_plus(self):     assert EIG2_PLUS == K
    def test_eig_minus(self):    assert EIG2_MINUS == S_EIG
    def test_plus_eq(self):      assert EIG2_PLUS_EQ_K is True
    def test_minus_eq(self):     assert EIG2_MINUS_EQ_S is True


class TestCrossEdges:
    def test_cross(self):        assert CROSS_EDGES == 120
    def test_value(self):        assert CROSS_EDGES_VALUE == 120
    def test_alpha_k(self):      assert CROSS_EQ_ALPHA_K is True
    def test_half_edges(self):   assert CROSS_EQ_3_EDGES_HALF is True
    def test_b2_10_mu(self):     assert B2_10_EQ_MU is True
    def test_b2_11_k_mu(self):   assert B2_11_EQ_K_MINUS_MU is True


class TestVerifyAll:
    def test_tuple(self):
        r = verify_all()
        assert isinstance(r, tuple) and len(r) == 3

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
        failed = [n for n, ok, _ in checks if not ok]
        assert failed == [], f"Failed: {failed}"


class TestBuildSummary:
    def setup_method(self):
        self.s = build_ccxcviii_summary()

    def test_part(self):           assert self.s["part"] == "CCXCVIII"
    def test_title(self):          assert "Equitable" in self.s["title"]
    def test_checks_pass(self):    assert self.s["checks_pass"] == 27
    def test_checks_total(self):   assert self.s["checks_total"] == 27
    def test_status(self):         assert self.s["status"] == "ALL_PASS"
    def test_quot3_trace(self):    assert self.s["quot3_trace"] == 10
    def test_cross_edges(self):    assert self.s["cross_edges"] == 120
    def test_disc(self):           assert self.s["b2_disc"] == 256
    def test_eig_plus(self):       assert self.s["eig2_plus"] == K
    def test_eig_minus(self):      assert self.s["eig2_minus"] == S_EIG
    def test_b2_10(self):          assert self.s["b2_10"] == MU
    def test_b2_11(self):          assert self.s["b2_11"] == K - MU
    def test_discoveries(self):
        assert isinstance(self.s["discoveries"], list)
        assert len(self.s["discoveries"]) >= 5
