"""Tests for PART CCCVII — Line Graph Spectrum of W(3,3)"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCVII_LINE_GRAPH_BRIDGE import (
    V, K, K2, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    L_V, L_EDGES, L_VALENCY,
    L_EIG_0, L_EIG_1, L_EIG_2, L_EIG_3,
    MULT_L3, L_MULT_SUM,
    L_SPEC_SUM,
    L_TRACE_SQ_EIG, L_TRACE_SQ_EDGES, L_TRACE_SQ_SM1, L_TRACE_SQ_SM2,
    L_EIG_0_EQ_K_ALPHA, L_EIG_0_EQ_VALENCY,
    L_EIG_1_EQ_K, L_EIG_2_EQ_LAM_GEN, MULT_L3_SM,
    L_EIG_02_DIFF, L_EIG_02_DIFF_SM,
    L_EIG_03_SUM, L_EIG_03_SUM_SM,
    L_EIG_13_DIFF, L_EIG_13_DIFF_SM,
    verify_all, build_cccvii_summary,
)


class TestSRGConstants:
    def test_V_K(self):
        assert V == 40 and K == 12

    def test_edges(self):
        assert EDGES == 240

    def test_adj_eigenvalues(self):
        assert R_EIG == 2 and S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24 and MULT_S == 15

    def test_sm_constants(self):
        assert ALPHA == 10 and EW_GAUGE_4 == 4
        assert GUT_DIM == 27 and GENERATIONS == 3


class TestLineGraphStructure:
    def test_lv(self):
        assert L_V == 240 == EDGES

    def test_l_edges(self):
        assert L_EDGES == 2640
        assert L_EDGES == V * K * (K - 1) // 2

    def test_l_valency(self):
        assert L_VALENCY == 22
        assert L_VALENCY == 2 * (K - 1)

    def test_mult_l3(self):
        assert MULT_L3 == 200
        assert MULT_L3 == EDGES - V

    def test_total_multiplicity(self):
        assert L_MULT_SUM == L_V == 240


class TestLineEigenvalues:
    def test_l_eig_0(self):
        assert L_EIG_0 == 22
        assert L_EIG_0 == K + K - 2

    def test_l_eig_1(self):
        assert L_EIG_1 == 12
        assert L_EIG_1 == R_EIG + K - 2

    def test_l_eig_2(self):
        assert L_EIG_2 == 6
        assert L_EIG_2 == S_EIG + K - 2

    def test_l_eig_3(self):
        assert L_EIG_3 == -2

    def test_l_eig_0_eq_valency(self):
        assert L_EIG_0_EQ_VALENCY is True
        assert L_EIG_0 == L_VALENCY

    def test_ordering(self):
        assert L_EIG_0 > L_EIG_1 > L_EIG_2 > 0 > L_EIG_3


class TestTraceIdentities:
    def test_trace_zero(self):
        assert L_SPEC_SUM == 0

    def test_trace_sq_eig(self):
        assert L_TRACE_SQ_EIG == 5280

    def test_trace_sq_edges(self):
        assert L_TRACE_SQ_EDGES == 5280
        assert L_TRACE_SQ_EDGES == 2 * L_EDGES

    def test_trace_sq_sm1(self):
        assert L_TRACE_SQ_SM1 == 5280
        assert L_TRACE_SQ_SM1 == V * K * (K - 1)

    def test_trace_sq_sm2(self):
        assert L_TRACE_SQ_SM2 == 5280
        assert L_TRACE_SQ_SM2 == 2 * EDGES * (K - 1)

    def test_trace_sq_agree(self):
        assert L_TRACE_SQ_EIG == L_TRACE_SQ_EDGES == L_TRACE_SQ_SM1 == L_TRACE_SQ_SM2


class TestSMEncodings:
    def test_l_eig_0_k_alpha(self):
        assert L_EIG_0_EQ_K_ALPHA is True
        assert L_EIG_0 == K + ALPHA

    def test_l_eig_1_k(self):
        assert L_EIG_1_EQ_K is True
        assert L_EIG_1 == K

    def test_l_eig_2_lam_gen(self):
        assert L_EIG_2_EQ_LAM_GEN is True
        assert L_EIG_2 == LAM * GENERATIONS

    def test_mult_l3_sm(self):
        assert MULT_L3_SM is True
        assert MULT_L3 == (ALPHA // 2) * V


class TestSMFinale:
    def test_eig_02_diff(self):
        assert L_EIG_02_DIFF == 16
        assert L_EIG_02_DIFF == L_EIG_0 - L_EIG_2

    def test_eig_02_diff_sm(self):
        assert L_EIG_02_DIFF_SM is True
        assert L_EIG_02_DIFF == K + EW_GAUGE_4

    def test_eig_03_sum(self):
        assert L_EIG_03_SUM == 20
        assert L_EIG_03_SUM == L_EIG_0 + L_EIG_3

    def test_eig_03_sum_sm(self):
        assert L_EIG_03_SUM_SM is True
        assert L_EIG_03_SUM == 2 * ALPHA

    def test_eig_13_diff(self):
        assert L_EIG_13_DIFF == 10
        assert L_EIG_13_DIFF == L_EIG_1 - abs(L_EIG_3)

    def test_eig_13_diff_sm(self):
        assert L_EIG_13_DIFF_SM is True
        assert L_EIG_13_DIFF == ALPHA


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total == 27

    def test_each_check_ok(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert c["ok"] is True, f"Failed: {c['name']}"


class TestBuildSummary:
    def setup_method(self):
        self.s = build_cccvii_summary()

    def test_part(self):
        assert self.s["part"] == "CCCVII"

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_checks(self):
        assert self.s["checks_pass"] == 27
        assert self.s["checks_total"] == 27

    def test_title(self):
        assert "Line" in self.s["title"]

    def test_fields(self):
        f = self.s["fields"]
        assert f["L_EIG_0"] == 22
        assert f["L_EIG_1"] == 12
        assert f["L_EIG_2"] == 6
        assert f["L_EIG_3"] == -2
        assert f["MULT_L3"] == 200

    def test_discoveries(self):
        assert len(self.s["discoveries"]) >= 5
