"""Tests for PART CCCV — Signless Laplacian Spectrum of W(3,3)"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCV_SIGNLESS_LAPLACIAN_BRIDGE import (
    V, K, K2, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    Q_EIG_0, Q_EIG_1, Q_EIG_2,
    Q_SPEC_SUM, Q_SPEC_SUM_EQ_2E,
    Q_DISTINCT_SUM, Q_DISTINCT_SUM_FORMULA,
    Q_DISTINCT_PROD,
    Q_TRACE_SQ, Q_TRACE_SQ_EQ_VKK1,
    Q_SPEC_RADIUS, Q_RADIUS_EQ_MULT_R, Q_RADIUS_EQ_2ALPHA_EW,
    Q_MIN, Q_MIN_EQ_2EW, Q_MIN_EQ_MU_EW, Q_MIN_EQ_K_EW,
    Q_EIG_1_EQ_GUT_K, Q_EIG_1_EQ_KR,
    Q_AVERAGE,
    QLE, QLE_EQ_EDGES_HALF, QLE_EQ_KV_EW,
    Q_EIG_01_DIFF, Q_DIFF_01_EQ_ALPHA,
    Q_EIG_12_DIFF, Q_DIFF_12_EQ_K_HALF,
    Q_EIG_02_DIFF, Q_DIFF_02_EQ_K_EW,
    verify_all, build_cccv_summary,
)


class TestSRGConstants:
    def test_V_K(self):
        assert V == 40 and K == 12

    def test_adj_eigenvalues(self):
        assert R_EIG == 2 and S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24 and MULT_S == 15

    def test_sm_constants(self):
        assert ALPHA == 10 and EW_GAUGE_4 == 4
        assert GUT_DIM == 27 and GENERATIONS == 3

    def test_edges(self):
        assert EDGES == 240


class TestSignlessLaplacianEigenvalues:
    def test_q0(self):
        assert Q_EIG_0 == K + K == 24

    def test_q1(self):
        assert Q_EIG_1 == K + R_EIG == 14

    def test_q2(self):
        assert Q_EIG_2 == K + S_EIG == 8

    def test_q_spectrum_order(self):
        assert Q_EIG_0 > Q_EIG_1 > Q_EIG_2 > 0

    def test_eigenvalue_count(self):
        # Three distinct eigenvalues with total multiplicity V
        total_mult = 1 + MULT_R + MULT_S
        assert total_mult == V


class TestSpectralSums:
    def test_spec_sum_eq_2_edges(self):
        assert Q_SPEC_SUM_EQ_2E is True
        assert Q_SPEC_SUM == 2 * EDGES == 480

    def test_trace_q2(self):
        assert Q_TRACE_SQ_EQ_VKK1 is True
        assert Q_TRACE_SQ == V * K * (K + 1) == 6240

    def test_distinct_sum(self):
        assert Q_DISTINCT_SUM == Q_EIG_0 + Q_EIG_1 + Q_EIG_2 == 46

    def test_distinct_sum_formula(self):
        assert Q_DISTINCT_SUM_FORMULA is True
        assert Q_DISTINCT_SUM == 4 * K + R_EIG + S_EIG

    def test_distinct_product(self):
        assert Q_DISTINCT_PROD == Q_EIG_0 * Q_EIG_1 * Q_EIG_2 == 2688


class TestSpectralRadius:
    def test_radius_value(self):
        assert Q_SPEC_RADIUS == 24

    def test_radius_eq_mult_r(self):
        assert Q_RADIUS_EQ_MULT_R is True
        assert Q_SPEC_RADIUS == MULT_R

    def test_radius_eq_2alpha_ew(self):
        assert Q_RADIUS_EQ_2ALPHA_EW is True
        assert Q_SPEC_RADIUS == 2 * ALPHA + EW_GAUGE_4


class TestSmallestEigenvalue:
    def test_q_min_value(self):
        assert Q_MIN == 8

    def test_q_min_2ew(self):
        assert Q_MIN_EQ_2EW is True
        assert Q_MIN == 2 * EW_GAUGE_4

    def test_q_min_mu_ew(self):
        assert Q_MIN_EQ_MU_EW is True
        assert Q_MIN == MU + EW_GAUGE_4

    def test_q_min_k_ew(self):
        assert Q_MIN_EQ_K_EW is True
        assert Q_MIN == K - EW_GAUGE_4

    def test_q_min_positive(self):
        # W(3,3) is not bipartite
        assert Q_MIN > 0


class TestEigenvalueDifferences:
    def test_q0_q1_diff(self):
        assert Q_EIG_01_DIFF == Q_EIG_0 - Q_EIG_1 == 10

    def test_q0_q1_eq_alpha(self):
        assert Q_DIFF_01_EQ_ALPHA is True
        assert Q_EIG_01_DIFF == ALPHA

    def test_q1_q2_diff(self):
        assert Q_EIG_12_DIFF == Q_EIG_1 - Q_EIG_2 == 6

    def test_q1_q2_eq_k_half(self):
        assert Q_DIFF_12_EQ_K_HALF is True
        assert Q_EIG_12_DIFF == K // 2

    def test_q0_q2_diff(self):
        assert Q_EIG_02_DIFF == Q_EIG_0 - Q_EIG_2 == 16

    def test_q0_q2_eq_k_ew(self):
        assert Q_DIFF_02_EQ_K_EW is True
        assert Q_EIG_02_DIFF == K + EW_GAUGE_4


class TestSMLEncoding:
    def test_q1_gut_k(self):
        assert Q_EIG_1_EQ_GUT_K is True
        assert Q_EIG_1 == GUT_DIM - K - 1

    def test_q_average(self):
        from fractions import Fraction
        assert Q_AVERAGE == Fraction(2 * EDGES, V) == K


class TestSignlessEnergy:
    def test_qle_value(self):
        assert QLE == 120

    def test_qle_eq_edges_half(self):
        assert QLE_EQ_EDGES_HALF is True
        assert QLE == EDGES // 2

    def test_qle_eq_kv_ew(self):
        assert QLE_EQ_KV_EW is True
        assert QLE == K * V // EW_GAUGE_4


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
        self.s = build_cccv_summary()

    def test_part(self):
        assert self.s["part"] == "CCCV"

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_checks(self):
        assert self.s["checks_pass"] == 27
        assert self.s["checks_total"] == 27

    def test_title(self):
        assert "Signless" in self.s["title"]

    def test_fields(self):
        f = self.s["fields"]
        assert f["Q_EIG_0"] == 24
        assert f["Q_EIG_1"] == 14
        assert f["Q_EIG_2"] == 8
        assert f["QLE"] == 120

    def test_discoveries(self):
        assert len(self.s["discoveries"]) >= 5
