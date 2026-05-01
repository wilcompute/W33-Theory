from __future__ import annotations

from scripts.w33_q8_spectral_action_master_audit import (
    q8_spectral_action_master_audit,
)


def test_q8_selector_packet_keeps_all_exact_q3_routes_visible() -> None:
    summary = q8_spectral_action_master_audit()

    assert summary["q3_selection_packet"] == {
        "symplectic_equation": "(q+1)^2 = 2(q+1)(q-1)",
        "symplectic_positive_integer_hits_1_to_20": (3,),
        "e8_root_equation": "q^5 - q = 240",
        "e8_root_positive_integer_hits_1_to_20": (3,),
        "atmospheric_sum_rule_polynomial": "q(q-3)",
        "atmospheric_positive_integer_hits_1_to_20": (3,),
        "fibonacci_square_hits_1_to_30": (1, 12),
        "nontrivial_fibonacci_square_hits_1_to_30": (12,),
    }


def test_master_variable_reconstructs_promoted_q8_closures() -> None:
    summary = q8_spectral_action_master_audit()

    assert summary["master_variable_packet"] == {
        "x": "3/13",
        "x_from_w33": {
            "q_over_Phi3": "3/13",
            "lambda_plus_1_over_k_plus_1": "3/13",
        },
        "closures": {
            "sin2_theta_W": "3/13",
            "tan_theta_C": "3/13",
            "sin2_theta_12": "4/13",
            "sin2_theta_23": "7/13",
            "sin2_theta_13": "2/91",
            "mH2_over_v2": "14/55",
            "a2_over_a0": "14/3",
            "a4_over_a0": "110/3",
            "c6_over_a0": "26",
            "c6_over_cEH_cont": "39",
        },
    }


def test_spectral_action_arithmetic_and_exceptional_dimensions_lock() -> None:
    summary = q8_spectral_action_master_audit()

    assert summary["spectral_action_arithmetic_packet"] == {
        "internal_ko_dimension": 6,
        "product_ko_dimension": 10,
        "product_ko_dimension_mod_8": 2,
        "standard_model_ko_signature_mod_8": 2,
        "qcd_beta0": 7,
        "qcd_beta0_text": "7",
        "qcd_beta0_equals_Phi6": True,
        "higgs_ratio_mH2_over_v2": "14/55",
    }
    assert {
        key: row["value"]
        for key, row in summary["exceptional_dimension_packet"].items()
    } == {
        "dim_G2": 14,
        "dim_F4": 52,
        "dim_E6": 78,
        "dim_E7": 133,
        "dim_E8": 248,
        "D_bosonic": 26,
        "D_super": 10,
        "D_M_theory": 11,
    }


def test_hierarchy_monster_and_leech_packets_are_exact() -> None:
    summary = q8_spectral_action_master_audit()

    assert summary["hierarchy_packet"] == {
        "exponent_2Phi6": 14,
        "dim_SO32": 496,
        "dim_E8": 248,
        "exact_496_decompositions": {
            "2_dim_E8": 496,
            "2E_plus_16": 496,
            "SO32_adjoint": 496,
        },
        "hierarchy_expression": "1/(10^(2Phi6) * 496)",
        "hierarchy_denominator_without_power": 496,
    }
    assert summary["monster_leech_packet"] == {
        "monster_nontrivial_rep": 196883,
        "monster_factorization": {
            "v_plus_Phi6": 47,
            "v_plus_k_plus_Phi6": 59,
            "Phi12_minus_lambda": 71,
        },
        "mckay_coefficient": 196884,
        "leech_kissing": 196560,
        "mckay_minus_leech": 324,
        "mu_q4_gap": 324,
    }


def test_boundary_conflicts_are_explicit_instead_of_silently_absorbed() -> None:
    summary = q8_spectral_action_master_audit()
    conflicts = summary["boundary_conflicts"]

    assert conflicts["omega_lambda_generator_vs_cosmo_table"] == {
        "generator_formula": "Omega_Lambda = 3x",
        "generator_value": "9/13",
        "cosmo_table_formula": "(v+1)/60",
        "cosmo_table_value": "41/60",
        "equal": False,
    }
    assert conflicts["cabibbo_sin_vs_tan_shorthand"] == {
        "exact_generator_statement": "tan(theta_C) = x",
        "sin2_if_theta_C_is_arctan_x": "9/178",
        "x_squared": "9/169",
        "sin_theta_C_equals_x_is_exact": False,
    }
    assert conflicts["legacy_pmns_theta12_formula"] == {
        "promoted_value_mu_over_Phi3": "4/13",
        "legacy_value_q_over_k_minus_lambda": "3/10",
        "equal": False,
    }
    assert conflicts["so32_label_misprint"] == {
        "exact_2E_plus_16": 496,
        "exact_2_dim_E8": 496,
        "literal_2E_plus_2_dim_E8": 976,
        "literal_equals_496": False,
    }
    assert conflicts["alpha_table_rounding_or_formula_conflict"] == {
        "paper_exact_fraction": "669969/4889",
        "paper_exact_decimal_12": "137.035999181837",
        "index_q8_table_value": "137.036004",
        "same_as_index_q8_table_to_6_decimals": False,
    }


def test_q8_master_theorem_flags_are_all_true() -> None:
    summary = q8_spectral_action_master_audit()

    assert summary["theorem"] == {
        "symplectic_equation_selects_q3": True,
        "e8_root_count_selects_q3": True,
        "atmospheric_sum_rule_selects_q3_among_positive_integers": True,
        "nontrivial_fibonacci_square_selector_is_12": True,
        "master_variable_closures_match_promoted_pmns_values": True,
        "spectral_action_ko_dimension_matches_sm_signature": True,
        "qcd_beta0_is_Phi6": True,
        "exceptional_dimension_table_is_exact": True,
        "monster_and_leech_factorizations_are_exact": True,
        "boundary_conflicts_are_explicit_not_absorbed": True,
    }
