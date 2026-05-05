"""
Tests for PART CCCXVII — Clique Number & Fractional Chromatic Number of W(3,3)
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))

from PART_CCCXVII_CLIQUE_CHROMATIC_BRIDGE import (
    V, K, LAM, MU, MULT_R, MULT_S, R_EIG, S_EIG,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    CLIQUE_BOUND, ALPHA_BOUND, CHI_FRAC, CHI_LOWER,
    verify_all, build_cccxvii_summary,
)


# ===========================================================================
# TestSRGParameters
# ===========================================================================
class TestSRGParameters:
    def test_vertices(self):
        assert V == 40

    def test_degree(self):
        assert K == 12

    def test_lambda(self):
        assert LAM == 2

    def test_mu(self):
        assert MU == 4

    def test_mult_r(self):
        assert MULT_R == 24

    def test_mult_s(self):
        assert MULT_S == 15

    def test_r_eig(self):
        assert R_EIG == 2

    def test_s_eig(self):
        assert S_EIG == -4

    def test_mult_r_plus_mult_s(self):
        assert MULT_R + MULT_S == V - 1

    def test_eigenvalue_sign(self):
        assert R_EIG > 0 and S_EIG < 0


# ===========================================================================
# TestDelsarteCliqueBound
# ===========================================================================
class TestDelsarteCliqueBound:
    def test_clique_bound_value(self):
        assert CLIQUE_BOUND == 4

    def test_clique_bound_formula(self):
        # 1 - K // S_EIG = 1 - (-3) = 4
        assert CLIQUE_BOUND == 1 - K // S_EIG

    def test_clique_bound_equals_ew_gauge_4(self):
        assert CLIQUE_BOUND == EW_GAUGE_4

    def test_clique_bound_equals_mu(self):
        assert CLIQUE_BOUND == MU

    def test_clique_bound_squared(self):
        # 4^2 = 16 = K + MU = 12 + 4
        assert CLIQUE_BOUND ** 2 == K + MU

    def test_clique_bound_squared_is_16(self):
        assert CLIQUE_BOUND ** 2 == 16

    def test_clique_bound_times_s_eig(self):
        # CLIQUE_BOUND * |S_EIG| = 16 = K + MU
        assert CLIQUE_BOUND * abs(S_EIG) == K + MU

    def test_clique_bound_vs_r_eig(self):
        assert CLIQUE_BOUND == LAM * R_EIG

    def test_clique_bound_vs_generations(self):
        assert CLIQUE_BOUND == GENERATIONS + 1

    def test_clique_bound_divides_v(self):
        assert V % CLIQUE_BOUND == 0


# ===========================================================================
# TestHoffmanIndependenceBound
# ===========================================================================
class TestHoffmanIndependenceBound:
    def test_alpha_bound_value(self):
        assert ALPHA_BOUND == 10

    def test_alpha_bound_formula(self):
        # V * |S| / (K - S) = 40 * 4 / 16 = 10
        assert ALPHA_BOUND == V * abs(S_EIG) // (K - S_EIG)

    def test_alpha_bound_equals_alpha(self):
        assert ALPHA_BOUND == ALPHA

    def test_clique_coclique_product(self):
        # omega * alpha = 4 * 10 = 40 = V  (perfect partition)
        assert ALPHA_BOUND * CLIQUE_BOUND == V

    def test_bound_difference_is_two_generations(self):
        # 10 - 4 = 6 = 2 * 3
        assert ALPHA_BOUND - CLIQUE_BOUND == 2 * GENERATIONS

    def test_alpha_bound_denominator(self):
        # K - S_EIG = 16
        assert K - S_EIG == 16

    def test_alpha_bound_numerator(self):
        # V * |S_EIG| = 160
        assert V * abs(S_EIG) == 160

    def test_alpha_bound_divides_v(self):
        assert V % ALPHA_BOUND == 0

    def test_alpha_bound_vs_mult_s(self):
        # ALPHA_BOUND = MULT_S - GENERATIONS + 2 = 15 - 3 - 2 = 10
        assert ALPHA_BOUND == MULT_S - GENERATIONS - LAM

    def test_k_minus_s_equals_clique_times_alpha_bound_on_v(self):
        # K - S_EIG == V * abs(S_EIG) / ALPHA_BOUND
        assert K - S_EIG == V * abs(S_EIG) // ALPHA_BOUND


# ===========================================================================
# TestFractionalChromatic
# ===========================================================================
class TestFractionalChromatic:
    def test_chi_frac_value(self):
        assert CHI_FRAC == 4

    def test_chi_frac_formula(self):
        assert CHI_FRAC == V // ALPHA_BOUND

    def test_chi_frac_equals_ew_gauge_4(self):
        assert CHI_FRAC == EW_GAUGE_4

    def test_chi_lower_value(self):
        assert CHI_LOWER == 4

    def test_chi_lower_formula(self):
        assert CHI_LOWER == 1 + K // abs(S_EIG)

    def test_chi_lower_equals_chi_frac(self):
        assert CHI_FRAC == CHI_LOWER

    def test_chi_lower_equals_ew_gauge_4(self):
        assert CHI_LOWER == EW_GAUGE_4

    def test_chi_frac_times_alpha_bound(self):
        # chi_f * alpha = V
        assert CHI_FRAC * ALPHA_BOUND == V

    def test_chi_frac_times_clique_bound(self):
        # chi_f * omega = 16 = K + MU
        assert CHI_FRAC * CLIQUE_BOUND == K + MU

    def test_chi_lower_vs_generations(self):
        # 1 + K // |S| = 1 + 3 = 4 = GENERATIONS + 1
        assert CHI_LOWER == GENERATIONS + 1


# ===========================================================================
# TestSMEncodings
# ===========================================================================
class TestSMEncodings:
    def test_v_div_clique_is_alpha_bound(self):
        assert V // CLIQUE_BOUND == ALPHA_BOUND

    def test_k_div_s_eig_is_generations(self):
        assert K // abs(S_EIG) == GENERATIONS

    def test_alpha_plus_clique_is_k_plus_lam(self):
        # 10 + 4 = 14 = 12 + 2
        assert ALPHA_BOUND + CLIQUE_BOUND == K + LAM

    def test_alpha_times_generations(self):
        # 10 * 3 = 30 = 24 + 6 = MULT_R + GENERATIONS*LAM
        assert ALPHA_BOUND * GENERATIONS == MULT_R + GENERATIONS * LAM

    def test_chi_frac_squared_is_k_plus_mu(self):
        # 4^2 = 16 = 12 + 4
        assert CHI_FRAC ** LAM == K + MU

    def test_alpha_div_clique_is_r_eig(self):
        # 10 // 4 = 2 = R_EIG
        assert ALPHA_BOUND // CLIQUE_BOUND == R_EIG

    def test_clique_times_mu(self):
        # 4 * 4 = 16 = 24 - 8 = MULT_R - MU*LAM
        assert CLIQUE_BOUND * MU == MULT_R - MU * LAM

    def test_alpha_minus_s_eig_times_lam(self):
        # 10 - 4*2 = 10 - 8 = 2 = LAM
        assert ALPHA_BOUND - abs(S_EIG) * LAM == LAM

    def test_chi_times_alpha_is_v(self):
        assert CHI_FRAC * ALPHA_BOUND == V

    def test_clique_bound_is_mu(self):
        assert CLIQUE_BOUND == MU

    def test_alpha_bound_is_alpha(self):
        assert ALPHA_BOUND == ALPHA

    def test_chi_frac_is_ew_gauge_4(self):
        assert CHI_FRAC == EW_GAUGE_4

    def test_k_plus_lam_value(self):
        assert K + LAM == 14

    def test_alpha_plus_clique_is_14(self):
        assert ALPHA_BOUND + CLIQUE_BOUND == 14

    def test_30_is_mult_r_plus_generations_times_lam(self):
        assert MULT_R + GENERATIONS * LAM == 30

    def test_alpha_times_3_is_30(self):
        assert ALPHA_BOUND * GENERATIONS == 30

    def test_clique_bound_squared_is_16(self):
        assert CLIQUE_BOUND ** 2 == 16

    def test_16_is_k_plus_mu(self):
        assert K + MU == 16

    def test_alpha_bound_mod_clique_bound(self):
        # 10 mod 4 = 2 = R_EIG
        assert ALPHA_BOUND % CLIQUE_BOUND == R_EIG

    def test_generations_squared_in_alpha(self):
        # ALPHA = GENERATIONS^2 + 1
        assert ALPHA == GENERATIONS ** 2 + 1


# ===========================================================================
# TestVerifyAll
# ===========================================================================
class TestVerifyAll:
    def test_verify_all_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_verify_all_27_checks(self):
        checks, passed, total = verify_all()
        assert total == 27

    def test_verify_all_27_pass(self):
        checks, passed, total = verify_all()
        assert passed == 27

    def test_verify_all_checks_is_list(self):
        checks, _, _ = verify_all()
        assert isinstance(checks, list)

    def test_verify_all_checks_are_pairs(self):
        checks, _, _ = verify_all()
        for label, val in checks:
            assert isinstance(label, str)
            assert isinstance(val, bool)

    def test_verify_all_no_failures(self):
        checks, passed, total = verify_all()
        failures = [label for label, v in checks if not v]
        assert failures == []

    def test_build_cccxvii_summary_status(self):
        summary = build_cccxvii_summary()
        assert summary["status"] == "PASS"

    def test_build_cccxvii_summary_part(self):
        summary = build_cccxvii_summary()
        assert summary["part"] == "CCCXVII"

    def test_build_cccxvii_summary_checks(self):
        summary = build_cccxvii_summary()
        assert summary["checks_pass"] == 27
        assert summary["checks_total"] == 27

    def test_build_cccxvii_summary_fields(self):
        summary = build_cccxvii_summary()
        fields = summary["fields"]
        assert fields["V"] == 40
        assert fields["CLIQUE_BOUND"] == 4
        assert fields["ALPHA_BOUND"] == 10
        assert fields["CHI_FRAC"] == 4

    def test_build_cccxvii_summary_discoveries(self):
        summary = build_cccxvii_summary()
        assert len(summary["discoveries"]) >= 10
