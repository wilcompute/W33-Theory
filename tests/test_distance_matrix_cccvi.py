"""Tests for PART CCCVI — Distance Matrix Spectrum of W(3,3)"""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCVI_DISTANCE_MATRIX_BRIDGE import (
    V, K, K2, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    D_EIG_0, D_EIG_1, D_EIG_2,
    D_MULT_SUM,
    D_EIG_1_EQ_S, D_EIG_2_EQ_R,
    D_SPEC_SUM,
    D_TRACE_SQ_EIG, D_TRACE_SQ_STRUCT,
    D_TRACE_SQ_SM1, D_TRACE_SQ_SM2,
    D_EIG_0_EQ_2GUT_K, D_EIG_0_EQ_VM1_GUT,
    D_ABS_EIG1_EQ_EW, D_ABS_EIG1_EQ_MU,
    D_EIG_2_EQ_LAM,
    WIENER, WIENER_ALT, WIENER_SM1, WIENER_SM2, WIENER_SM3,
    D_SPREAD, D_SPREAD_SM,
    D_FINALE, D_FINALE_SM,
    DIAMETER, DIAMETER_EQ_LAM,
    verify_all, build_cccvi_summary,
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


class TestDistanceEigenvalues:
    def test_perron_formula(self):
        assert D_EIG_0 == 2 * V - 2 - K == 66

    def test_d1_formula(self):
        assert D_EIG_1 == -2 - R_EIG == -4

    def test_d2_formula(self):
        assert D_EIG_2 == -2 - S_EIG == 2

    def test_d1_eq_s_eig(self):
        assert D_EIG_1_EQ_S is True
        assert D_EIG_1 == S_EIG

    def test_d2_eq_r_eig(self):
        assert D_EIG_2_EQ_R is True
        assert D_EIG_2 == R_EIG

    def test_ordering(self):
        assert D_EIG_0 > D_EIG_2 > 0 > D_EIG_1

    def test_multiplicity_sum(self):
        assert D_MULT_SUM == V == 40


class TestSpectralIdentities:
    def test_trace_zero(self):
        assert D_SPEC_SUM == 0

    def test_trace_sq_eigenvalues(self):
        assert D_TRACE_SQ_EIG == 4800

    def test_trace_sq_structure(self):
        assert D_TRACE_SQ_STRUCT == 4800

    def test_trace_sq_agree(self):
        assert D_TRACE_SQ_EIG == D_TRACE_SQ_STRUCT

    def test_trace_sq_sm1(self):
        assert D_TRACE_SQ_SM1 == 4800
        assert D_TRACE_SQ_SM1 == V * ALPHA * K

    def test_trace_sq_sm2(self):
        assert D_TRACE_SQ_SM2 == 4800
        assert D_TRACE_SQ_SM2 == 2 * EDGES * ALPHA


class TestPerronSMEncodings:
    def test_d0_2gut_k(self):
        assert D_EIG_0_EQ_2GUT_K is True
        assert D_EIG_0 == 2 * GUT_DIM + K

    def test_d0_vm1_gut(self):
        assert D_EIG_0_EQ_VM1_GUT is True
        assert D_EIG_0 == (V - 1) + GUT_DIM

    def test_abs_d1_ew(self):
        assert D_ABS_EIG1_EQ_EW is True
        assert abs(D_EIG_1) == EW_GAUGE_4

    def test_abs_d1_mu(self):
        assert D_ABS_EIG1_EQ_MU is True
        assert abs(D_EIG_1) == MU

    def test_d2_lam(self):
        assert D_EIG_2_EQ_LAM is True
        assert D_EIG_2 == LAM


class TestWienerIndex:
    def test_wiener_value(self):
        assert WIENER == 1320

    def test_wiener_alt(self):
        assert WIENER_ALT == 1320
        assert WIENER == WIENER_ALT

    def test_wiener_sm1(self):
        assert WIENER_SM1 == 1320
        assert WIENER_SM1 == GUT_DIM * V + EDGES

    def test_wiener_sm2(self):
        assert WIENER_SM2 == 1320
        assert WIENER_SM2 == MULT_R * MULT_S + 4 * EDGES

    def test_wiener_sm3(self):
        assert WIENER_SM3 == 1320
        assert WIENER_SM3 == V * (GUT_DIM + K // 2)


class TestSMFinale:
    def test_d_spread(self):
        assert D_SPREAD == D_EIG_0 - D_EIG_1 == 70

    def test_d_spread_sm(self):
        assert D_SPREAD_SM is True
        assert D_SPREAD == MULT_R + MULT_S + MU + GUT_DIM

    def test_d_finale(self):
        assert D_FINALE == D_EIG_0 - abs(D_EIG_1) - D_EIG_2 == 60

    def test_d_finale_sm(self):
        assert D_FINALE_SM is True
        assert D_FINALE == 2 * ALPHA * GENERATIONS

    def test_diameter(self):
        assert DIAMETER == 2

    def test_diameter_eq_lam(self):
        assert DIAMETER_EQ_LAM is True
        assert DIAMETER == LAM


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
        self.s = build_cccvi_summary()

    def test_part(self):
        assert self.s["part"] == "CCCVI"

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_checks(self):
        assert self.s["checks_pass"] == 27
        assert self.s["checks_total"] == 27

    def test_title(self):
        assert "Distance" in self.s["title"]

    def test_fields(self):
        f = self.s["fields"]
        assert f["D_EIG_0"] == 66
        assert f["D_EIG_1"] == -4
        assert f["D_EIG_2"] == 2
        assert f["WIENER"] == 1320

    def test_discoveries(self):
        assert len(self.s["discoveries"]) >= 5
