"""Tests for PART CCCIV — Spanning Tree Count of W(3,3)"""
import pytest
import math
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCIV_SPANNING_TREE_COUNT_BRIDGE import (
    V, K, K2, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    LAP_EIG_1, LAP_EIG_2,
    LAP_PROD_RAW, SPANNING_TREE_COUNT, DIVISIBLE,
    EXPONENT_2, EXPONENT_5, SPANNING_TREE_FACTORED_STR, SPANNING_TREE_CHECK,
    EXPONENT_2_EQ_GEN4, EXPONENT_5_EQ_GUT_EW,
    EXPONENT_SUM, EXPONENT_DIFF,
    EXPONENT_SUM_EQ_8_KP1, EXPONENT_DIFF_EQ_V_MS_3, EXPONENT_DIFF_DECOMP,
    LOG2_TAU, LN_TAU, ST_ENTROPY, LOG2_TAU_FLOOR,
    SPANNING_TREE_ALT_CHECK, EXPONENT_2_ALT, EXPONENT_10_ALT,
    EXPONENT_2_EQ_3_GUT, EXPONENT_5_P1_EQ_MULT_R,
    verify_all, build_ccciv_summary,
)


class TestSRGConstants:
    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_laplacian_eigs(self):
        assert LAP_EIG_1 == 10 and LAP_EIG_2 == 16

    def test_multiplicities(self):
        assert MULT_R == 24 and MULT_S == 15

    def test_sm_constants(self):
        assert ALPHA == 10 and EW_GAUGE_4 == 4
        assert GUT_DIM == 27 and GENERATIONS == 3


class TestDivisibilityAndCount:
    def test_divisible_by_v(self):
        assert DIVISIBLE is True
        assert LAP_PROD_RAW % V == 0

    def test_count_equals_formula(self):
        assert SPANNING_TREE_COUNT == LAP_PROD_RAW // V

    def test_count_is_int(self):
        assert isinstance(SPANNING_TREE_COUNT, int)

    def test_count_positive(self):
        assert SPANNING_TREE_COUNT > 0

    def test_count_large(self):
        # Should have many digits — a huge number
        assert len(str(SPANNING_TREE_COUNT)) > 30


class TestPrimeFactorisation:
    def test_exponent_2(self):
        assert EXPONENT_2 == 81

    def test_exponent_5(self):
        assert EXPONENT_5 == 23

    def test_factored_form(self):
        assert SPANNING_TREE_CHECK is True
        assert 2 ** EXPONENT_2 * 5 ** EXPONENT_5 == SPANNING_TREE_COUNT

    def test_alt_factored_form(self):
        assert SPANNING_TREE_ALT_CHECK is True
        assert 2 ** EXPONENT_2_ALT * 10 ** EXPONENT_10_ALT == SPANNING_TREE_COUNT

    def test_alt_exponents(self):
        assert EXPONENT_2_ALT == 58
        assert EXPONENT_10_ALT == 23


class TestSMExponentEncodings:
    def test_exp2_gen4(self):
        assert EXPONENT_2_EQ_GEN4 is True
        assert EXPONENT_2 == GENERATIONS ** 4    # 81 = 3^4

    def test_exp2_3_gut(self):
        assert EXPONENT_2_EQ_3_GUT is True
        assert EXPONENT_2 == 3 * GUT_DIM         # 81 = 3*27

    def test_exp5_gut_ew(self):
        assert EXPONENT_5_EQ_GUT_EW is True
        assert EXPONENT_5 == GUT_DIM - EW_GAUGE_4    # 23 = 27-4

    def test_exp5_plus1_mult_r(self):
        assert EXPONENT_5_P1_EQ_MULT_R is True
        assert EXPONENT_5 + 1 == MULT_R    # 24


class TestExponentArithmetic:
    def test_exponent_sum(self):
        assert EXPONENT_SUM == EXPONENT_2 + EXPONENT_5
        assert EXPONENT_SUM == 104

    def test_exponent_sum_8kp1(self):
        assert EXPONENT_SUM_EQ_8_KP1 is True
        assert EXPONENT_SUM == 8 * (K + 1)

    def test_exponent_diff(self):
        assert EXPONENT_DIFF == EXPONENT_2 - EXPONENT_5
        assert EXPONENT_DIFF == 58

    def test_exponent_diff_v_ms_3(self):
        assert EXPONENT_DIFF_EQ_V_MS_3 is True
        assert EXPONENT_DIFF == V + MULT_S + 3

    def test_exponent_diff_decomp(self):
        assert EXPONENT_DIFF_DECOMP is True
        assert EXPONENT_DIFF == MULT_R + MULT_S + K + GENERATIONS + EW_GAUGE_4


class TestEntropyAndLog:
    def test_ln_tau_positive(self):
        assert LN_TAU > 0

    def test_ln_tau_value(self):
        expected = EXPONENT_2 * math.log(2) + EXPONENT_5 * math.log(5)
        assert abs(LN_TAU - expected) < 1e-10

    def test_log2_tau_floor(self):
        assert LOG2_TAU_FLOOR == 134

    def test_log2_tau_range(self):
        assert 134 < LOG2_TAU < 135

    def test_entropy_positive(self):
        assert ST_ENTROPY > 0

    def test_entropy_range(self):
        assert 2.0 < ST_ENTROPY < 3.0

    def test_entropy_value(self):
        assert abs(ST_ENTROPY - LN_TAU / V) < 1e-10


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
        self.s = build_ccciv_summary()

    def test_part(self):
        assert self.s["part"] == "CCCIV"

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_checks(self):
        assert self.s["checks_pass"] == 27
        assert self.s["checks_total"] == 27

    def test_title(self):
        assert "Spanning" in self.s["title"]

    def test_fields(self):
        f = self.s["fields"]
        assert f["EXPONENT_2"] == 81
        assert f["EXPONENT_5"] == 23
        assert f["SPANNING_TREE_FACTORED"] == "2^81 * 5^23"

    def test_discoveries(self):
        assert len(self.s["discoveries"]) >= 5
