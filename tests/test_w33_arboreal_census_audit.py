#!/usr/bin/env python3
"""Comprehensive test suite for W(3,3) Arboreal Census (Kirchhoff Spanning Tree Audit)"""

import math
import pytest
from scripts.w33_arboreal_census_audit import w33_arboreal_census_summary

TAU_EXACT = (2**81) * (5**23)


class TestT1KirchhoffFormula:
    """T1: Kirchhoff formula gives τ = 2^81 × 5^23 exactly"""

    def test_theorem_flag_true(self):
        s = w33_arboreal_census_summary()
        assert s["theorem"]["T1_kirchhoff_formula_gives_exact_integer_tau"] is True

    def test_tau_is_exact_integer(self):
        s = w33_arboreal_census_summary()
        tau = s["kirchhoff_exact_count"]["exact_tau"]
        assert isinstance(tau, int)
        assert tau > 0

    def test_tau_equals_2_81_times_5_23(self):
        s = w33_arboreal_census_summary()
        tau = s["kirchhoff_exact_count"]["exact_tau"]
        assert tau == TAU_EXACT

    def test_compact_form_label(self):
        s = w33_arboreal_census_summary()
        compact = s["kirchhoff_exact_count"]["compact_form"]
        assert "81" in compact
        assert "23" in compact


class TestT2SRGEigenvaluePacket:
    """T2: L₀ eigenvalues are exactly the SRG(40,12,2,4) packet"""

    def test_theorem_flag_true(self):
        s = w33_arboreal_census_summary()
        assert s["theorem"]["T2_L0_eigenvalues_are_exactly_srg_packet"] is True

    def test_srg_char_eqn_r_root(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["srg_char_eqn_r_check"] == 0

    def test_srg_char_eqn_s_root(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["srg_char_eqn_s_check"] == 0

    def test_multiplicity_sum(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["mult_sum_check"] is True

    def test_trace_check(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["trace_check"] is True

    def test_numerical_match(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["numerical_match_theory"] is True

    def test_eigenvalue_10_multiplicity_24(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["L0_eigenvalues"]["10"] == 24

    def test_eigenvalue_16_multiplicity_15(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["L0_eigenvalues"]["16"] == 15

    def test_eigenvalue_0_multiplicity_1(self):
        s = w33_arboreal_census_summary()
        assert s["srg_eigenvalue_verification"]["L0_eigenvalues"]["0"] == 1

    def test_srg_params(self):
        s = w33_arboreal_census_summary()
        params = s["srg_eigenvalue_verification"]["srg_params"]
        assert params["n"] == 40
        assert params["k"] == 12
        assert params["lambda"] == 2
        assert params["mu"] == 4


class TestT3KirchhoffReductionExact:
    """T3: (1/40) × 10^24 × 16^15 = 2^81 × 5^23 (exact reduction)"""

    def test_theorem_flag_true(self):
        s = w33_arboreal_census_summary()
        assert s["theorem"]["T3_kirchhoff_reduction_is_exact"] is True

    def test_exponent_2_is_81(self):
        s = w33_arboreal_census_summary()
        assert s["kirchhoff_exact_count"]["prime_factorisation"]["exp_2"] == 81

    def test_exponent_5_is_23(self):
        s = w33_arboreal_census_summary()
        assert s["kirchhoff_exact_count"]["prime_factorisation"]["exp_5"] == 23

    def test_reconstruction_exact(self):
        s = w33_arboreal_census_summary()
        assert s["kirchhoff_exact_count"]["reconstruction_exact"] is True

    def test_formula_string(self):
        s = w33_arboreal_census_summary()
        formula = s["kirchhoff_exact_count"]["formula"]
        assert "40" in formula
        assert "10^24" in formula
        assert "16^15" in formula


class TestT4PrimeFactorisationPurity:
    """T4: τ = 2^81 × 5^23 only (no factors of 3, 7, ...)"""

    def test_theorem_flag_true(self):
        s = w33_arboreal_census_summary()
        assert s["theorem"]["T4_prime_factorisation_is_2_and_5_only"] is True

    def test_no_factor_of_3(self):
        s = w33_arboreal_census_summary()
        assert s["kirchhoff_exact_count"]["prime_factorisation"]["exp_3"] == 0

    def test_no_factor_of_7(self):
        s = w33_arboreal_census_summary()
        assert s["kirchhoff_exact_count"]["prime_factorisation"]["exp_7"] == 0

    def test_tau_divisible_by_2_81(self):
        s = w33_arboreal_census_summary()
        tau = s["kirchhoff_exact_count"]["exact_tau"]
        assert tau % (2**81) == 0

    def test_tau_divisible_by_5_23(self):
        s = w33_arboreal_census_summary()
        tau = s["kirchhoff_exact_count"]["exact_tau"]
        assert tau % (5**23) == 0


class TestT5ExponentQ3Lock:
    """T5: Exponent 81 = q^4 at q=3 — arboreal census locks q=3"""

    def test_theorem_flag_true(self):
        s = w33_arboreal_census_summary()
        assert s["theorem"]["T5_exponent_81_equals_q4_at_q3"] is True

    def test_q_is_3(self):
        s = w33_arboreal_census_summary()
        assert s["q3_exponent_lock"]["q"] == 3

    def test_q4_equals_81(self):
        s = w33_arboreal_census_summary()
        assert s["q3_exponent_lock"]["q4"] == 81

    def test_exponent_2_matches_q4(self):
        s = w33_arboreal_census_summary()
        assert s["q3_exponent_lock"]["exponent_2_equals_q4"] is True

    def test_sum_exponents_is_104(self):
        s = w33_arboreal_census_summary()
        assert s["q3_exponent_lock"]["sum_exponents"] == 104

    def test_sum_equals_8_times_13(self):
        s = w33_arboreal_census_summary()
        assert s["q3_exponent_lock"]["sum_equals_8_times_13"] is True

    def test_n_equals_q_packet(self):
        s = w33_arboreal_census_summary()
        assert s["q3_exponent_lock"]["n_equals_q_packet"] is True


class TestT6TwoMethodsAgree:
    """T6: Eigenvalue product and matrix cofactor methods agree"""

    def test_theorem_flag_true(self):
        s = w33_arboreal_census_summary()
        assert s["theorem"]["T6_two_methods_agree"] is True

    def test_cofactor_sign_positive(self):
        s = w33_arboreal_census_summary()
        assert s["cofactor_numerical_verification"]["det_sign"] == 1

    def test_cofactor_log_det_matches_exact(self):
        s = w33_arboreal_census_summary()
        assert s["cofactor_numerical_verification"]["log_det_matches_exact"] is True

    def test_cofactor_log_det_close_to_expected(self):
        s = w33_arboreal_census_summary()
        diff = s["cofactor_numerical_verification"]["log_det_diff"]
        assert diff < 1e-3


class TestAllTheoremFlags:
    """Composite test: all six theorems are true"""

    def test_all_theorems_true(self):
        s = w33_arboreal_census_summary()
        flags = [
            "T1_kirchhoff_formula_gives_exact_integer_tau",
            "T2_L0_eigenvalues_are_exactly_srg_packet",
            "T3_kirchhoff_reduction_is_exact",
            "T4_prime_factorisation_is_2_and_5_only",
            "T5_exponent_81_equals_q4_at_q3",
            "T6_two_methods_agree",
        ]
        for flag in flags:
            assert s["theorem"][flag] is True, f"Flag {flag} is not True"

    def test_six_theorem_flags_present(self):
        s = w33_arboreal_census_summary()
        assert len(s["theorem"]) == 6

    def test_status_ok(self):
        s = w33_arboreal_census_summary()
        assert s["status"] == "ok"


class TestCarrierAndBoundaryLanguage:
    """Graph carrier + boundary note"""

    def test_graph_is_w33(self):
        s = w33_arboreal_census_summary()
        assert s["carrier"]["graph"] == "W(3,3)"

    def test_carrier_type_srg(self):
        s = w33_arboreal_census_summary()
        assert "SRG(40,12,2,4)" in s["carrier"]["type"]

    def test_carrier_vertices(self):
        s = w33_arboreal_census_summary()
        assert s["carrier"]["vertices"] == 40

    def test_carrier_edges(self):
        s = w33_arboreal_census_summary()
        assert s["carrier"]["edges"] == 240

    def test_boundary_note_mentions_exact(self):
        s = w33_arboreal_census_summary()
        assert "exact" in s["boundary_note"].lower()

    def test_boundary_note_mentions_q3_lock(self):
        s = w33_arboreal_census_summary()
        assert "q=3" in s["boundary_note"] or "q3" in s["boundary_note"].lower()

    def test_tau_scale(self):
        """τ is a ~40-digit number (> 10^39)"""
        s = w33_arboreal_census_summary()
        tau = s["kirchhoff_exact_count"]["exact_tau"]
        assert tau > 10**39

    def test_tau_exact_value(self):
        """Exact verification: τ = 2^81 × 5^23"""
        s = w33_arboreal_census_summary()
        tau = s["kirchhoff_exact_count"]["exact_tau"]
        assert tau == (2**81) * (5**23)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
