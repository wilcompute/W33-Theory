"""
Tests for Part CCXCIV: Generalized Quadrangle GQ(3,3) and the W(3,3) Collinearity Graph.
"""

import pytest
from fractions import Fraction
from exploration.PART_CCXCIV_GQ_COLLINEARITY_BRIDGE import (
    # SRG constants
    V, K, LAM, MU, K2, EDGES, MULT_R, MULT_S,
    # SM constants
    EW_GAUGE_4, QUARKS_36, TOTAL_SM_40, Q,
    # GQ parameters
    S_GQ, T_GQ, SELF_DUAL, ST_PRODUCT,
    # Point/line counts
    POINTS, LINES, POINTS_PER_LINE, LINES_PER_POINT,
    INCIDENCES, INCIDENCES_LINES,
    # SRG recovered
    SRG_V, SRG_K, SRG_LAM, SRG_MU,
    # Ovoid/spread
    OVOID_SIZE, SPREAD_SIZE, SPREAD_COVERS,
    # Collinearity counts
    COLLINEAR_COMMON, NONCOLLINEAR_COMMON,
    # SM
    V_MINUS_EW, OVOID_IS_ALPHA, GQ_SELF_DUAL_V, GQ_ORDER, GQ_SQ_ORDER,
    # Functions
    verify_all, build_ccxciv_summary,
)


class TestSRGConstants:
    def test_v(self):           assert V == 40
    def test_k(self):           assert K == 12
    def test_lam(self):         assert LAM == 2
    def test_mu(self):          assert MU == 4
    def test_k2(self):          assert K2 == 27
    def test_edges(self):       assert EDGES == 240
    def test_mult_r(self):      assert MULT_R == 24
    def test_mult_s(self):      assert MULT_S == 15
    def test_edges_formula(self):  assert EDGES == V * K // 2
    def test_mult_sum(self):    assert MULT_R + MULT_S == V - 1


class TestSMConstants:
    def test_ew_gauge(self):    assert EW_GAUGE_4 == 4
    def test_quarks(self):      assert QUARKS_36 == 36
    def test_total_sm(self):    assert TOTAL_SM_40 == 40
    def test_q(self):           assert Q == 3


class TestGQParameters:
    def test_s_gq(self):        assert S_GQ == 3
    def test_t_gq(self):        assert T_GQ == 3
    def test_s_eq_q(self):      assert S_GQ == Q
    def test_t_eq_q(self):      assert T_GQ == Q
    def test_s_eq_t(self):      assert S_GQ == T_GQ
    def test_self_dual(self):   assert SELF_DUAL is True
    def test_st_product(self):  assert ST_PRODUCT == 9
    def test_st_is_q2(self):    assert ST_PRODUCT == Q ** 2
    def test_gq_order(self):    assert GQ_ORDER == Q
    def test_gq_sq_order(self): assert GQ_SQ_ORDER == Q ** 2


class TestPointLineCounts:
    def test_points_formula(self):
        assert POINTS == (S_GQ + 1) * (ST_PRODUCT + 1)

    def test_lines_formula(self):
        assert LINES == (T_GQ + 1) * (ST_PRODUCT + 1)

    def test_points_eq_v(self):      assert POINTS == V
    def test_lines_eq_v(self):       assert LINES == V
    def test_points_eq_lines(self):  assert POINTS == LINES
    def test_self_dual_flag(self):   assert GQ_SELF_DUAL_V is True

    def test_pts_per_line(self):     assert POINTS_PER_LINE == S_GQ + 1
    def test_lpp_value(self):        assert POINTS_PER_LINE == 4
    def test_lpp_eq_ew4(self):       assert POINTS_PER_LINE == EW_GAUGE_4

    def test_lines_per_pt(self):     assert LINES_PER_POINT == T_GQ + 1
    def test_lpp2_value(self):       assert LINES_PER_POINT == 4
    def test_lpp2_eq_ew4(self):      assert LINES_PER_POINT == EW_GAUGE_4

    def test_pts_per_line_eq_lpp(self):  assert POINTS_PER_LINE == LINES_PER_POINT


class TestIncidences:
    def test_incidences_value(self):  assert INCIDENCES == 160
    def test_incidences_formula(self): assert INCIDENCES == POINTS * LINES_PER_POINT
    def test_incidences_alt(self):    assert INCIDENCES_LINES == LINES * POINTS_PER_LINE
    def test_incidences_consistent(self): assert INCIDENCES == INCIDENCES_LINES
    def test_incidences_value2(self): assert INCIDENCES == 40 * 4


class TestSRGRecovery:
    """All four SRG parameters of W(3,3) recovered from s=t=3."""

    def test_srg_v(self):           assert SRG_V == 40
    def test_srg_k(self):           assert SRG_K == 12
    def test_srg_lam(self):         assert SRG_LAM == 2
    def test_srg_mu(self):          assert SRG_MU == 4

    def test_srg_v_eq_V(self):      assert SRG_V == V
    def test_srg_k_eq_K(self):      assert SRG_K == K
    def test_srg_lam_eq_LAM(self):  assert SRG_LAM == LAM
    def test_srg_mu_eq_MU(self):    assert SRG_MU == MU

    def test_srg_k_formula(self):   assert SRG_K == S_GQ * (T_GQ + 1)
    def test_srg_lam_formula(self): assert SRG_LAM == S_GQ - 1
    def test_srg_mu_formula(self):  assert SRG_MU == T_GQ + 1


class TestOvoidSpread:
    def test_ovoid_size(self):        assert OVOID_SIZE == 10
    def test_ovoid_formula(self):     assert OVOID_SIZE == ST_PRODUCT + 1
    def test_ovoid_is_alpha(self):    assert OVOID_IS_ALPHA is True
    def test_spread_size(self):       assert SPREAD_SIZE == 10
    def test_spread_formula(self):    assert SPREAD_SIZE == ST_PRODUCT + 1
    def test_spread_covers_all(self): assert SPREAD_COVERS == V
    def test_spread_covers_formula(self): assert SPREAD_COVERS == SPREAD_SIZE * POINTS_PER_LINE
    def test_ovoid_eq_spread(self):   assert OVOID_SIZE == SPREAD_SIZE


class TestCollinearity:
    def test_collinear_common(self):
        assert COLLINEAR_COMMON == 2

    def test_collinear_common_eq_lam(self):
        assert COLLINEAR_COMMON == LAM

    def test_collinear_common_formula(self):
        assert COLLINEAR_COMMON == S_GQ - 1

    def test_noncollinear_common(self):
        assert NONCOLLINEAR_COMMON == 4

    def test_noncollinear_common_eq_mu(self):
        assert NONCOLLINEAR_COMMON == MU

    def test_noncollinear_common_formula(self):
        assert NONCOLLINEAR_COMMON == T_GQ + 1

    def test_noncollinear_common_eq_ew4(self):
        assert NONCOLLINEAR_COMMON == EW_GAUGE_4


class TestSMConnections:
    def test_v_minus_ew4(self):
        assert V_MINUS_EW == 36

    def test_v_minus_ew4_eq_quarks(self):
        assert V_MINUS_EW == QUARKS_36

    def test_lines_per_pt_is_ew4(self):
        assert LINES_PER_POINT == EW_GAUGE_4

    def test_pts_per_line_is_ew4(self):
        assert POINTS_PER_LINE == EW_GAUGE_4

    def test_gq_order_is_Q(self):
        assert GQ_ORDER == Q

    def test_s_eq_t_eq_q(self):
        assert S_GQ == T_GQ == Q


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_passed_total(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_27_pass(self):
        _, passed, total = verify_all()
        assert passed == 27
        assert total == 27

    def test_checks_are_all_true(self):
        checks, _, _ = verify_all()
        failed = [name for name, ok, _ in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"


class TestBuildSummary:
    def setup_method(self):
        self.summary = build_ccxciv_summary()

    def test_part_label(self):
        assert self.summary["part"] == "CCXCIV"

    def test_title_contains_gq(self):
        assert "GQ" in self.summary["title"]

    def test_checks_pass(self):
        assert self.summary["checks_pass"] == 27

    def test_checks_total(self):
        assert self.summary["checks_total"] == 27

    def test_status_all_pass(self):
        assert self.summary["status"] == "ALL_PASS"

    def test_gq_s(self):
        assert self.summary["gq_s"] == 3

    def test_gq_t(self):
        assert self.summary["gq_t"] == 3

    def test_gq_points(self):
        assert self.summary["gq_points"] == 40

    def test_gq_lines(self):
        assert self.summary["gq_lines"] == 40

    def test_gq_ppl(self):
        assert self.summary["gq_points_per_line"] == 4

    def test_gq_lpp(self):
        assert self.summary["gq_lines_per_point"] == 4

    def test_ovoid(self):
        assert self.summary["ovoid_size"] == 10

    def test_spread(self):
        assert self.summary["spread_size"] == 10

    def test_srg_v(self):
        assert self.summary["srg_v"] == 40

    def test_srg_k(self):
        assert self.summary["srg_k"] == 12

    def test_srg_lam(self):
        assert self.summary["srg_lam"] == 2

    def test_srg_mu(self):
        assert self.summary["srg_mu"] == 4

    def test_discoveries_list(self):
        assert isinstance(self.summary["discoveries"], list)
        assert len(self.summary["discoveries"]) >= 5
