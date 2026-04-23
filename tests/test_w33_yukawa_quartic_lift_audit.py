from __future__ import annotations

from scripts.w33_yukawa_quartic_lift_audit import analyze


def test_residual_active_quartics_are_exact_even_lifts_of_base_packets() -> None:
    summary = analyze()
    packet = summary["quartic_lift_packet"]
    theorem = summary["quartic_lift_theorem"]
    records = packet["records"]

    h2 = records["H_2:-+"]
    hbar2 = records["Hbar_2:+-"]

    assert packet["scaled_signed_variable"] == "x = 240 * sigma"
    assert packet["scaled_squared_variable"] == "u = x^2 = 57600 * sigma^2"
    assert packet["packet_size"] == 2

    assert h2["base_squared_polynomial"] == "u**2 - 542*u + 61200"
    assert h2["active_squared_factor"] == "y**2 - 542*y + 61200"
    assert h2["quartic_polynomial"] == "x**4 - 542*x**2 + 61200"
    assert h2["base_root_packet"] == ["271 - sqrt(12241)", "sqrt(12241) + 271"]
    assert h2["positive_root_packet"] == [
        "sqrt(271 - sqrt(12241))",
        "sqrt(sqrt(12241) + 271)",
    ]
    assert h2["lift_theorem"]["active_squared_factor_occurs_in_recorded_slot"] is True
    assert h2["lift_theorem"]["quartic_is_even_lift_of_base_quadratic_packet"] is True
    assert h2["lift_theorem"]["positive_roots_square_to_base_root_packet"] is True

    assert hbar2["base_squared_polynomial"] == "u**2 - 982*u + 137232"
    assert hbar2["active_squared_factor"] == "y**2 - 982*y + 137232"
    assert hbar2["quartic_polynomial"] == "x**4 - 982*x**2 + 137232"
    assert hbar2["base_root_packet"] == ["491 - sqrt(103849)", "sqrt(103849) + 491"]
    assert hbar2["positive_root_packet"] == [
        "sqrt(491 - sqrt(103849))",
        "sqrt(sqrt(103849) + 491)",
    ]
    assert hbar2["lift_theorem"]["active_squared_factor_occurs_in_recorded_slot"] is True
    assert hbar2["lift_theorem"]["quartic_is_even_lift_of_base_quadratic_packet"] is True
    assert hbar2["lift_theorem"]["positive_roots_square_to_base_root_packet"] is True

    assert theorem["residual_active_quartics_are_exact_even_lifts_of_base_quadratic_packets"] is True
    assert summary["quartic_record_names"] == ("H_2:-+", "Hbar_2:+-")


def test_residual_active_quartics_are_irreducible_d4_packets() -> None:
    summary = analyze()
    theorem = summary["quartic_lift_theorem"]
    relation = summary["quartic_pair_relation"]
    root_field_relation = summary["quartic_root_field_relation"]
    splitting_field_relation = summary["quartic_splitting_field_relation"]
    mixed_relation = summary["mixed_positive_root_relation"]
    records = summary["quartic_lift_packet"]["records"]

    h2 = records["H_2:-+"]
    hbar2 = records["Hbar_2:+-"]

    assert h2["base_discriminant"] == 48964
    assert h2["quartic_discriminant"] == 2347605851443200
    assert h2["galois_group_label"] == "D4"
    assert h2["galois_group_order"] == 8
    assert h2["galois_group_is_alternating_subgroup"] is False
    assert h2["quadratic_subfield_squarefree_parts"] == {
        "sqrt_determinant": 17,
        "sqrt_base_discriminant": 12241,
        "sqrt_determinant_times_base_discriminant": 208097,
    }
    assert h2["lift_theorem"]["quartic_is_irreducible_over_q"] is True
    assert h2["lift_theorem"]["quartic_has_d4_galois_group"] is True

    assert hbar2["base_discriminant"] == 415396
    assert hbar2["quartic_discriminant"] == 378878530142932992
    assert hbar2["galois_group_label"] == "D4"
    assert hbar2["galois_group_order"] == 8
    assert hbar2["galois_group_is_alternating_subgroup"] is False
    assert hbar2["quadratic_subfield_squarefree_parts"] == {
        "sqrt_determinant": 953,
        "sqrt_base_discriminant": 103849,
        "sqrt_determinant_times_base_discriminant": 98968097,
    }
    assert hbar2["lift_theorem"]["quartic_is_irreducible_over_q"] is True
    assert hbar2["lift_theorem"]["quartic_has_d4_galois_group"] is True

    assert relation == {
        "h2_minus_plus_quadratic_subfield_squarefree_parts": [17, 12241, 208097],
        "hbar2_plus_minus_quadratic_subfield_squarefree_parts": [953, 103849, 98968097],
        "shared_quadratic_subfield_squarefree_parts": [],
    }
    assert root_field_relation == {
        "hbar2_plus_minus_factor_over_h2_minus_plus_root_field": "x**4 - 982*x**2 + 137232",
        "h2_minus_plus_factor_over_hbar2_plus_minus_root_field": "x**4 - 542*x**2 + 61200",
        "compositum_degree": 16,
        "relation_theorem": {
            "each_quartic_remains_irreducible_over_the_other_root_field": True,
            "quartic_root_field_compositum_has_degree_16": True,
            "quartic_root_fields_are_linearly_disjoint_over_q": True,
        },
    }
    assert splitting_field_relation == {
        "shared_quadratic_subfield_squarefree_parts": [],
        "individual_splitting_field_degree": 8,
        "compositum_degree": 64,
        "compositum_galois_group": "D4 x D4",
        "compositum_galois_group_order": 64,
        "relation_theorem": {
            "d4_splitting_fields_have_no_common_nontrivial_galois_subextension": True,
            "d4_splitting_fields_are_linearly_disjoint_over_q": True,
            "splitting_field_compositum_has_degree_64": True,
            "splitting_field_compositum_has_galois_group_d4_times_d4": True,
        },
    }
    assert mixed_relation == {
        "branch_choice_counts": {
            "h2_minus_plus_positive_branches": 2,
            "hbar2_plus_minus_positive_branches": 2,
        },
        "product_squared_packet": {
            "minpoly": "u**4 - 532244*u**3 + 82533253248*u**2 - 4470103606809600*u + 70536455084482560000",
            "degree": 4,
            "irreducible_over_q": True,
            "branch_stable_across_positive_root_choices": True,
        },
        "ratio_squared_packet": {
            "minpoly": "32695524*u**4 - 126807133*u**3 + 143286898*u**2 - 56550925*u + 6502500",
            "degree": 4,
            "irreducible_over_q": True,
            "branch_stable_across_positive_root_choices": True,
        },
        "product_squared_resultant_packet": {
            "primitive_resultant_minpoly": "u**4 - 532244*u**3 + 82533253248*u**2 - 4470103606809600*u + 70536455084482560000",
            "matches_product_squared_packet": True,
        },
        "ratio_squared_resultant_packet": {
            "primitive_resultant_minpoly": "32695524*u**4 - 126807133*u**3 + 143286898*u**2 - 56550925*u + 6502500",
            "matches_ratio_squared_packet": True,
        },
        "shared_biquadratic_field_packet": {
            "base_discriminant_squarefree_parts": [12241, 103849, 1271215609],
            "product_squared_galois_group_label": "V",
            "product_squared_galois_group_order": 4,
            "product_squared_galois_group_is_alternating_subgroup": True,
            "ratio_squared_galois_group_label": "V",
            "ratio_squared_galois_group_order": 4,
            "ratio_squared_galois_group_is_alternating_subgroup": True,
            "product_squared_factor_degree_pattern_over_sqrt_left_discriminant": [2, 2],
            "product_squared_factor_degree_pattern_over_sqrt_right_discriminant": [2, 2],
            "ratio_squared_factor_degree_pattern_over_sqrt_left_discriminant": [2, 2],
            "ratio_squared_factor_degree_pattern_over_sqrt_right_discriminant": [2, 2],
        },
        "product_packet": {
            "minpoly": "t**8 - 532244*t**6 + 82533253248*t**4 - 4470103606809600*t**2 + 70536455084482560000",
            "degree": 8,
            "irreducible_over_q": True,
            "branch_stable_across_positive_root_choices": True,
        },
        "ratio_packet": {
            "minpoly": "32695524*t**8 - 126807133*t**6 + 143286898*t**4 - 56550925*t**2 + 6502500",
            "degree": 8,
            "irreducible_over_q": True,
            "branch_stable_across_positive_root_choices": True,
        },
        "sum_packet": {
            "minpoly": "t**16 - 6096*t**14 + 13664696*t**12 - 14013417696*t**10 + 6693570534032*t**8 - 1360830623068800*t**6 + 102477901777835008*t**4 - 2379624174401126400*t**2 + 252934899442384896",
            "degree": 16,
            "irreducible_over_q": True,
            "branch_stable_across_positive_root_choices": True,
        },
        "difference_shares_sum_minpoly": True,
        "theorem": {
            "mixed_positive_root_product_packet_is_branch_stable_irreducible_octic": True,
            "mixed_positive_root_product_packet_is_exact_even_lift_of_irreducible_quartic": True,
            "mixed_positive_root_product_squared_packet_is_exact_product_resultant_of_base_quadratics": True,
            "mixed_positive_root_squared_product_packet_is_irreducible_v4_quartic": True,
            "mixed_positive_root_ratio_packet_is_branch_stable_irreducible_octic": True,
            "mixed_positive_root_ratio_packet_is_exact_even_lift_of_irreducible_quartic": True,
            "mixed_positive_root_ratio_squared_packet_is_exact_primitive_quotient_resultant_of_base_quadratics": True,
            "mixed_positive_root_squared_ratio_packet_is_irreducible_v4_quartic": True,
            "mixed_positive_root_squared_packets_split_over_either_base_discriminant_field_as_two_quadratics": True,
            "mixed_positive_root_squared_packets_share_the_common_biquadratic_field_of_the_two_base_discriminants": True,
            "mixed_positive_root_sum_packet_is_branch_stable_irreducible_degree_16": True,
            "mixed_positive_root_sum_generates_full_degree_16_root_field_compositum": True,
        },
    }
    assert theorem["both_even_lifts_are_irreducible_d4_quartics"] is True
    assert theorem["the_two_d4_lifts_have_disjoint_quadratic_subfield_packets"] is True
    assert theorem["the_two_quartic_root_fields_are_linearly_disjoint_over_q"] is True
    assert theorem["the_two_d4_splitting_fields_are_linearly_disjoint_over_q"] is True
    assert theorem["the_signed_packet_splitting_field_has_galois_group_d4_times_d4"] is True
    assert theorem["the_canonical_mixed_product_and_ratio_packets_are_branch_stable_irreducible_octics"] is True
    assert theorem["the_canonical_mixed_product_and_ratio_packets_are_even_lifts_of_branch_stable_irreducible_quartics"] is True
    assert theorem["the_canonical_mixed_squared_packets_are_exact_product_quotient_resultants_of_the_base_quadratic_pair"] is True
    assert theorem["the_canonical_mixed_squared_packets_are_common_v4_biquadratic_carriers_inside_the_base_discriminant_compositum"] is True
    assert theorem["a_canonical_mixed_positive_root_sum_generates_the_full_degree_16_root_field_compositum"] is True
    assert theorem["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True