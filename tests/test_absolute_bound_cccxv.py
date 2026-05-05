"""Tests for PART CCCXV — Absolute Bound & Polynomial Method for W(3,3)."""

import pytest
from fractions import Fraction
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))
from PART_CCCXV_ABSOLUTE_BOUND_BRIDGE import (
    V, K, LAM, MU, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    K0, K1, K2, M0, M1, M2,
    BOUND_R, BOUND_S, AB_V_LE_BOUND_R, AB_V_LE_BOUND_S,
    SLACK_R, SLACK_S,
    BOUND_S_SM, BOUND_R_SM, V_OVER_BOUND_S, V_OVER_BOUND_S_SM, SLACK_S_SM,
    KR_11_0, KR_11_1, KR_11_2, KR_12_0, KR_12_1, KR_12_2,
    KR_22_0, KR_22_1, KR_22_2, ALL_KREIN,
    KR_12_0_ZERO, KR_ALL_NONNEG, KR_22_2_SM, KR_11_2_SM, KR_11_0_EQ_M1, KR_22_0_EQ_M2,
    OMEGA_HOFFMAN, ALPHA_HOFFMAN, ABS_S,
    OMEGA_EQ_GENERATIONS_PLUS_1, ALPHA_EQ_ALPHA_SM,
    OMEGA_X_ALPHA, CLIQUE_COCLIQUE_EQ_V, K_OVER_ABS_S, K_OVER_ABS_S_SM,
    verify_all, build_cccxv_summary,
)


# ---------------------------------------------------------------------------
# Group 1: SRG parameters
# ---------------------------------------------------------------------------
class TestSRGParameters:
    def test_V_and_K(self):
        assert V == 40
        assert K == 12

    def test_lam_mu(self):
        assert LAM == 2
        assert MU == 4

    def test_eigenvalues(self):
        assert R_EIG == 2
        assert S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24
        assert MULT_S == 15

    def test_mults_sum_to_V(self):
        assert 1 + MULT_R + MULT_S == V

    def test_SM_constants(self):
        assert ALPHA == 10
        assert GENERATIONS == 3
        assert GUT_DIM == 27
        assert EW_GAUGE_4 == 4

    def test_class_sizes(self):
        assert K0 == 1
        assert K1 == 12
        assert K2 == 27
        assert K0 + K1 + K2 == V


# ---------------------------------------------------------------------------
# Group 2: Absolute bound values
# ---------------------------------------------------------------------------
class TestAbsoluteBounds:
    def test_bound_R_formula(self):
        assert BOUND_R == Fraction(MULT_R * (MULT_R + 1), 2)

    def test_bound_R_value(self):
        assert BOUND_R == 300

    def test_bound_S_formula(self):
        assert BOUND_S == Fraction(MULT_S * (MULT_S + 1), 2)

    def test_bound_S_value(self):
        assert BOUND_S == 120

    def test_V_satisfies_bound_R(self):
        assert AB_V_LE_BOUND_R is True
        assert V <= BOUND_R

    def test_V_satisfies_bound_S(self):
        assert AB_V_LE_BOUND_S is True
        assert V <= BOUND_S

    def test_slack_R_positive(self):
        assert SLACK_R > 0

    def test_slack_S_positive(self):
        assert SLACK_S > 0

    def test_slack_R_value(self):
        assert SLACK_R == 260

    def test_slack_S_value(self):
        assert SLACK_S == 80


# ---------------------------------------------------------------------------
# Group 3: SM encodings of bounds
# ---------------------------------------------------------------------------
class TestSMEncodingsBounds:
    def test_bound_S_eq_V_times_generations(self):
        assert BOUND_S == V * GENERATIONS
        assert BOUND_S_SM is True

    def test_bound_R_eq_V_times_mult_S_over_lam(self):
        assert BOUND_R == Fraction(V * MULT_S, LAM)
        assert BOUND_R_SM is True

    def test_V_over_bound_S_is_1_over_generations(self):
        assert V_OVER_BOUND_S == Fraction(1, GENERATIONS)
        assert V_OVER_BOUND_S_SM is True

    def test_slack_S_eq_LAM_times_V(self):
        assert SLACK_S == LAM * V
        assert SLACK_S_SM is True

    def test_bound_S_is_120(self):
        assert int(BOUND_S) == 120

    def test_bound_R_is_300(self):
        assert int(BOUND_R) == 300

    def test_bound_ratio(self):
        # Bound_R / Bound_S = 300/120 = 5/2
        assert Fraction(int(BOUND_R), int(BOUND_S)) == Fraction(5, 2)


# ---------------------------------------------------------------------------
# Group 4: Krein feasibility
# ---------------------------------------------------------------------------
class TestKreinFeasibility:
    def test_kr_11_0_exact(self):
        assert KR_11_0 == Fraction(24)

    def test_kr_11_1_exact(self):
        assert KR_11_1 == Fraction(44, 3)

    def test_kr_11_2_exact(self):
        assert KR_11_2 == Fraction(40, 3)

    def test_kr_12_0_zero(self):
        assert KR_12_0 == Fraction(0)
        assert KR_12_0_ZERO is True

    def test_kr_12_1_exact(self):
        assert KR_12_1 == Fraction(25, 3)

    def test_kr_12_2_exact(self):
        assert KR_12_2 == Fraction(32, 3)

    def test_kr_22_0_exact(self):
        assert KR_22_0 == Fraction(15)

    def test_kr_22_1_exact(self):
        assert KR_22_1 == Fraction(20, 3)

    def test_kr_22_2_exact(self):
        assert KR_22_2 == Fraction(10, 3)

    def test_all_krein_nonneg(self):
        assert KR_ALL_NONNEG is True
        for q in ALL_KREIN:
            assert q >= 0

    def test_kr_22_2_SM(self):
        assert KR_22_2 * GENERATIONS == ALPHA
        assert KR_22_2_SM is True

    def test_kr_11_2_SM(self):
        assert KR_11_2 * GENERATIONS == V
        assert KR_11_2_SM is True

    def test_kr_11_0_eq_mult_R(self):
        assert KR_11_0 == MULT_R
        assert KR_11_0_EQ_M1 is True

    def test_kr_22_0_eq_mult_S(self):
        assert KR_22_0 == MULT_S
        assert KR_22_0_EQ_M2 is True

    def test_kr_count(self):
        assert len(ALL_KREIN) == 9


# ---------------------------------------------------------------------------
# Group 5: Hoffman / LP bounds
# ---------------------------------------------------------------------------
class TestHoffmanBounds:
    def test_abs_S(self):
        assert ABS_S == 4

    def test_omega_hoffman_formula(self):
        expected = Fraction(1) - Fraction(K, S_EIG)
        assert OMEGA_HOFFMAN == expected

    def test_omega_hoffman_value(self):
        assert OMEGA_HOFFMAN == 4

    def test_omega_eq_generations_plus_1(self):
        assert OMEGA_HOFFMAN == GENERATIONS + 1
        assert OMEGA_EQ_GENERATIONS_PLUS_1 is True

    def test_alpha_hoffman_formula(self):
        expected = Fraction(V * ABS_S, K + ABS_S)
        assert ALPHA_HOFFMAN == expected

    def test_alpha_hoffman_value(self):
        assert ALPHA_HOFFMAN == 10

    def test_alpha_eq_ALPHA(self):
        assert ALPHA_HOFFMAN == ALPHA
        assert ALPHA_EQ_ALPHA_SM is True

    def test_clique_coclique_product(self):
        assert OMEGA_X_ALPHA == V
        assert CLIQUE_COCLIQUE_EQ_V is True

    def test_k_over_abs_s_eq_generations(self):
        assert K_OVER_ABS_S == GENERATIONS
        assert K_OVER_ABS_S_SM is True

    def test_hoffman_denominator(self):
        # k + |s| = 12 + 4 = 16 = 4 * GENERATIONS + EW_GAUGE_4
        assert K + ABS_S == 16

    def test_hoffman_numerator(self):
        # v * |s| = 40 * 4 = 160 = 4 * ALPHA * EW_GAUGE_4
        assert V * ABS_S == 160


# ---------------------------------------------------------------------------
# Group 6: verify_all and build_cccxv_summary
# ---------------------------------------------------------------------------
class TestVerifyAll:
    def test_verify_all_returns_27(self):
        checks, passed, total = verify_all()
        assert total == 27

    def test_all_checks_pass(self):
        checks, passed, total = verify_all()
        assert passed == total

    def test_check_names_unique(self):
        checks, _, _ = verify_all()
        names = [c["name"] for c in checks]
        assert len(names) == len(set(names))

    def test_all_checks_have_ok_bool(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert isinstance(c["ok"], bool), f"check {c['name']} has non-bool ok"

    def test_summary_part_label(self):
        s = build_cccxv_summary()
        assert s["part"] == "CCCXV"

    def test_summary_status_pass(self):
        s = build_cccxv_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_pass_27(self):
        s = build_cccxv_summary()
        assert s["checks_pass"] == 27
        assert s["checks_total"] == 27

    def test_summary_fields_present(self):
        s = build_cccxv_summary()
        for key in ["V", "K", "BOUND_R", "BOUND_S", "SLACK_R", "SLACK_S",
                    "omega_hoffman", "alpha_hoffman"]:
            assert key in s["fields"]

    def test_summary_discoveries_nonempty(self):
        s = build_cccxv_summary()
        assert len(s["discoveries"]) >= 5

    def test_summary_bound_fields(self):
        s = build_cccxv_summary()
        assert s["fields"]["BOUND_R"] == 300
        assert s["fields"]["BOUND_S"] == 120
        assert s["fields"]["SLACK_R"] == 260
        assert s["fields"]["SLACK_S"] == 80

    def test_summary_hoffman_fields(self):
        s = build_cccxv_summary()
        assert s["fields"]["omega_hoffman"] == 4
        assert s["fields"]["alpha_hoffman"] == 10
