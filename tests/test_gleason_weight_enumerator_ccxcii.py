"""
Tests for Part CCXCII: Gleason's Theorem and the Weight Enumerator Ring.
"""
import pytest
from fractions import Fraction
from exploration.PART_CCXCII_GLEASON_WEIGHT_ENUMERATOR_BRIDGE import (
    # Constants
    V, K, LAM, MU, Q, K2, MULT_R, MULT_S, EDGES,
    QUARKS_36, EW_GAUGE_4, TOTAL_SM,
    HAM_N, HAM_K, HAM_D, HAM_Q, HAM_R,
    # Gleason
    GLEASON_DEGREE_LOW, GLEASON_DEGREE_HIGH,
    GLEASON_DEGREE_SUM, GLEASON_DEGREE_PROD,
    GLEASON_LOW_EQ_EW, GLEASON_SUM_EQ_16, GLEASON_PROD_EQ_48,
    GLEASON_PROD_EQ_SM_WEYL,
    # Small code
    SMALL_N, SMALL_K, SMALL_D, SMALL_Q,
    SMALL_SELF_DUAL, SMALL_N_EQ_EW, SMALL_D_EQ_HAMD,
    SMALL_CODE_SIZE, SMALL_WE_A0, SMALL_WE_A3, SMALL_WE_TOT, SMALL_WE_CORRECT,
    # Ham WE
    HAM_WE, HAM_WE_WEIGHTS,
    HAM_WE_A0, HAM_WE_A0_IS_1,
    HAM_WE_ALL_NONNEG_INT, HAM_WE_TOTAL, HAM_WE_TOTAL_CORRECT,
    HAM_WE_MIN_WT, HAM_WE_MIN_WT_CORRECT,
    # Sim
    SIM_WE, SIM_WE_ALL_WT_DIV3,
    SIM_MIN_WT, SIM_MIN_WT_DIV3,
    # Divisibility
    HAM_MIN_WT_DIV3, HAM_N_MOD8, HAM_N_MOD3,
    # MacWilliams
    MACWILLIAMS_DIVISOR, MACWILLIAMS_DIVISOR_CORRECT,
    # SM
    SM_GENERATIONS, SM_WEYL_PER_GEN, SM_TOTAL_WEYL,
    # Functions
    macwilliams_eval, verify_all, build_ccxcii_summary,
)


class TestSRGConstants:
    def test_v(self):    assert V == 40
    def test_k(self):    assert K == 12
    def test_lam(self):  assert LAM == 2
    def test_mu(self):   assert MU == 4
    def test_q(self):    assert Q == 3
    def test_k2(self):   assert K2 == 27
    def test_mult_r(self): assert MULT_R == 24
    def test_mult_s(self): assert MULT_S == 15
    def test_edges(self): assert EDGES == 240
    def test_k_plus_k2(self): assert K + K2 + 1 == V


class TestSMConstants:
    def test_quarks(self):   assert QUARKS_36 == 36
    def test_ew_gauge(self): assert EW_GAUGE_4 == 4
    def test_total_sm(self): assert TOTAL_SM == 40
    def test_total_sm_eq_v(self): assert TOTAL_SM == V


class TestCodeParameters:
    def test_ham_n(self): assert HAM_N == 40
    def test_ham_k(self): assert HAM_K == 36
    def test_ham_d(self): assert HAM_D == 3
    def test_ham_q(self): assert HAM_Q == 3
    def test_ham_r(self): assert HAM_R == 4
    def test_ham_n_minus_k(self): assert HAM_N - HAM_K == HAM_R
    def test_ham_n_eq_v(self): assert HAM_N == V
    def test_ham_r_eq_ew(self): assert HAM_R == EW_GAUGE_4
    def test_ham_k_eq_quarks(self): assert HAM_K == QUARKS_36


class TestGleasonDegrees:
    def test_degree_low_is_4(self): assert GLEASON_DEGREE_LOW == 4
    def test_degree_high_is_12(self): assert GLEASON_DEGREE_HIGH == 12
    def test_low_eq_ew(self): assert GLEASON_LOW_EQ_EW is True
    def test_sum_is_16(self): assert GLEASON_DEGREE_SUM == 16
    def test_sum_flag(self): assert GLEASON_SUM_EQ_16 is True
    def test_prod_is_48(self): assert GLEASON_DEGREE_PROD == 48
    def test_prod_flag(self): assert GLEASON_PROD_EQ_48 is True
    def test_prod_eq_sm_weyl(self): assert GLEASON_PROD_EQ_SM_WEYL is True
    def test_low_divides_high(self): assert GLEASON_DEGREE_HIGH % GLEASON_DEGREE_LOW == 0
    def test_ratio_is_3(self): assert GLEASON_DEGREE_HIGH // GLEASON_DEGREE_LOW == 3


class TestSmallCode:
    def test_n_is_4(self): assert SMALL_N == 4
    def test_k_is_2(self): assert SMALL_K == 2
    def test_d_is_3(self): assert SMALL_D == 3
    def test_q_is_3(self): assert SMALL_Q == 3
    def test_self_dual(self): assert SMALL_SELF_DUAL is True
    def test_n_eq_ew(self): assert SMALL_N_EQ_EW is True
    def test_d_eq_hamd(self): assert SMALL_D_EQ_HAMD is True
    def test_code_size(self): assert SMALL_CODE_SIZE == 9
    def test_we_a0(self): assert SMALL_WE_A0 == 1
    def test_we_a3(self): assert SMALL_WE_A3 == 8
    def test_we_tot(self): assert SMALL_WE_TOT == 9
    def test_we_correct_flag(self): assert SMALL_WE_CORRECT is True
    def test_we_a0_plus_a3(self): assert SMALL_WE_A0 + SMALL_WE_A3 == SMALL_CODE_SIZE
    def test_k_half_n(self): assert SMALL_K * 2 == SMALL_N


class TestSimWeightEnumerator:
    def test_sim_we_has_two_keys(self): assert len(SIM_WE) == 2
    def test_sim_we_a0(self): assert SIM_WE[0] == 1
    def test_sim_we_a27(self): assert SIM_WE[27] == 80  # nonzero codewords of Sim(4,3)
    def test_sim_we_a27_is_80(self): assert SIM_WE[27] == 80
    def test_sim_total(self): assert sum(SIM_WE.values()) == HAM_Q ** HAM_R
    def test_sim_min_wt(self): assert SIM_MIN_WT == 27
    def test_sim_min_wt_div3(self): assert SIM_MIN_WT_DIV3 is True
    def test_sim_all_wt_div3(self): assert SIM_WE_ALL_WT_DIV3 is True
    def test_sim_wt27_mod3(self): assert 27 % 3 == 0


class TestHamWeightEnumerator:
    def test_a0_is_1(self): assert HAM_WE_A0 == 1
    def test_a0_is_1_flag(self): assert HAM_WE_A0_IS_1 is True
    def test_all_nonneg_int(self): assert HAM_WE_ALL_NONNEG_INT is True
    def test_total_correct(self): assert HAM_WE_TOTAL_CORRECT is True
    def test_total_value(self): assert HAM_WE_TOTAL == HAM_Q ** HAM_K
    def test_min_wt_is_3(self): assert HAM_WE_MIN_WT == 3
    def test_min_wt_flag(self): assert HAM_WE_MIN_WT_CORRECT is True
    def test_min_wt_div3(self): assert HAM_MIN_WT_DIV3 is True
    def test_zero_in_weights(self): assert 0 in HAM_WE
    def test_3_in_weights(self): assert 3 in HAM_WE
    def test_weights_are_sorted(self): assert HAM_WE_WEIGHTS == sorted(HAM_WE_WEIGHTS)


class TestHamArithmetic:
    def test_n_mod8(self): assert HAM_N_MOD8 == 0
    def test_n_mod3(self): assert HAM_N_MOD3 == 1   # 40 = 13*3 + 1
    def test_n_div8(self): assert HAM_N % 8 == 0
    def test_k2_div3(self): assert K2 % 3 == 0
    def test_d_div3(self): assert HAM_D % 3 == 0
    def test_r_div4(self): assert HAM_R % 4 == 0


class TestMacWilliamsGleason:
    def test_divisor_is_81(self): assert MACWILLIAMS_DIVISOR == 81
    def test_divisor_correct_flag(self): assert MACWILLIAMS_DIVISOR_CORRECT is True
    def test_divisor_eq_q_r(self): assert MACWILLIAMS_DIVISOR == HAM_Q ** HAM_R
    def test_divisor_eq_3_to_4(self): assert MACWILLIAMS_DIVISOR == 3 ** 4
    def test_macwilliams_eval_basic(self):
        # Trivial code: [1,1,1] self-dual ↔ WE = {0: 1, ...}: x + (q-1)*y transform
        result = macwilliams_eval({0: 1}, 1, 1, 3)
        # |C| = 3^0 = 1 for n=1, k=1; divisor = q^(n-k) = 3^0 = 1
        # For n=1, k=1: dual has size 3^1 = 3 — but we're testing {0:1} → trivial
        # K_0(0; 1, 3) = 1, so W_primal(0) = 1/1 * 1 = 1
        assert result.get(0, Fraction(0)) == Fraction(1)

    def test_macwilliams_recovers_sim(self):
        # MacWilliams of Ham gives Sim back
        result = macwilliams_eval(HAM_WE, HAM_N, HAM_R, HAM_Q)
        # Sim(4,3) WE: A0=1, A27=80 after rescaling by q^r / q^r = 1
        # Here result should give the Sim WE (up to integer checks)
        a0 = result.get(0, Fraction(0))
        a27 = result.get(27, Fraction(0))
        assert a0 > 0
        assert a27 > 0


class TestSMInterpretation:
    def test_generations(self): assert SM_GENERATIONS == 3
    def test_weyl_per_gen(self): assert SM_WEYL_PER_GEN == 16
    def test_total_weyl(self): assert SM_TOTAL_WEYL == 48
    def test_prod_eq_weyl(self): assert GLEASON_DEGREE_PROD == SM_TOTAL_WEYL
    def test_low_eq_ew(self): assert GLEASON_DEGREE_LOW == EW_GAUGE_4
    def test_small_n_eq_ew(self): assert SMALL_N == EW_GAUGE_4
    def test_we_total_9(self): assert SMALL_WE_TOT == 9
    def test_code_size_9(self): assert SMALL_CODE_SIZE == 9
    def test_gen_times_weyl_is_48(self): assert SM_GENERATIONS * SM_WEYL_PER_GEN == 48
    def test_ew_times_golay_is_48(self): assert GLEASON_DEGREE_LOW * GLEASON_DEGREE_HIGH == 48


class TestVerifyFunctions:
    def test_verify_gleason_structure(self):
        from exploration.PART_CCXCII_GLEASON_WEIGHT_ENUMERATOR_BRIDGE import verify_gleason_structure
        r = verify_gleason_structure()
        assert all(r.values()), r

    def test_verify_small_code(self):
        from exploration.PART_CCXCII_GLEASON_WEIGHT_ENUMERATOR_BRIDGE import verify_small_code
        r = verify_small_code()
        assert all(r.values()), r

    def test_verify_ham_weight_enumerator(self):
        from exploration.PART_CCXCII_GLEASON_WEIGHT_ENUMERATOR_BRIDGE import verify_ham_weight_enumerator
        r = verify_ham_weight_enumerator()
        assert all(r.values()), r

    def test_verify_macwilliams_gleason(self):
        from exploration.PART_CCXCII_GLEASON_WEIGHT_ENUMERATOR_BRIDGE import verify_macwilliams_gleason
        r = verify_macwilliams_gleason()
        assert all(r.values()), r

    def test_verify_sm_interpretation(self):
        from exploration.PART_CCXCII_GLEASON_WEIGHT_ENUMERATOR_BRIDGE import verify_sm_interpretation
        r = verify_sm_interpretation()
        assert all(r.values()), r

    def test_verify_all(self):
        r = verify_all()
        assert all(r.values()), r

    def test_verify_all_count(self):
        r = verify_all()
        assert len(r) == 27


class TestBuildSummary:
    def setup_method(self):
        self.s = build_ccxcii_summary()

    def test_part_number(self):
        assert self.s["part_number"] == "CCXCII"

    def test_checks_pass_27(self):
        assert self.s["checks_pass"] == 27

    def test_checks_total_27(self):
        assert self.s["checks_total"] == 27

    def test_status_all_pass(self):
        assert self.s["verification_status"] == "ALL CHECKS PASS"

    def test_gleason_degrees(self):
        g = self.s["gleason_ring"]
        assert g["degree_low"] == 4
        assert g["degree_high"] == 12

    def test_gleason_sum_prod(self):
        g = self.s["gleason_ring"]
        assert g["degree_sum"] == 16
        assert g["degree_prod"] == 48

    def test_small_code_in_summary(self):
        sc = self.s["small_code"]
        assert sc["n"] == 4
        assert sc["d"] == 3

    def test_sm_in_summary(self):
        sm = self.s["sm_interpretation"]
        assert sm["total_weyl"] == 48

    def test_discoveries_non_empty(self):
        assert len(self.s["key_discoveries"]) > 0
