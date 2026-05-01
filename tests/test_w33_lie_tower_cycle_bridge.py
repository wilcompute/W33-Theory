from __future__ import annotations

from w33_lie_tower_cycle_bridge import build_lie_tower_cycle_bridge_summary


def test_raw_tower_profiles_realize_the_exact_z3_cycle() -> None:
    summary = build_lie_tower_cycle_bridge_summary()
    profiles = summary["raw_tower_profiles"]
    theorem = summary["z3_grade_cycle_theorem"]

    assert [(row["level"], row["support_size"]) for row in profiles] == [
        (3, 72),
        (4, 81),
        (5, 81),
        (6, 86),
    ]
    assert profiles[0]["entry_count"] == 2592
    assert profiles[0]["single_entry_count"] == 2592
    assert profiles[0]["multi_entry_count"] == 0
    assert profiles[0]["uniform_output_term_count"] == 36
    assert profiles[1]["entry_count"] == 25920
    assert profiles[1]["uniform_output_term_count"] == 320
    assert profiles[2]["entry_count"] == 285120
    assert profiles[2]["uniform_output_term_count"] == 3520
    assert profiles[3]["entry_count"] == 2457864
    assert profiles[3]["single_entry_count"] == 2389824
    assert profiles[3]["multi_entry_count"] == 68040
    assert theorem["pure_single_term_layers_before_l6"] is True
    assert theorem["l3_uniform_e6_only"] is True
    assert theorem["l4_uniform_g1_only"] is True
    assert theorem["l5_uniform_g2_only"] is True
    assert theorem["l6_first_full_gauge_return"] is True


def test_tower_patterns_progress_exactly_from_balanced_to_democratic_plus_six_asymmetric() -> (
    None
):
    summary = build_lie_tower_cycle_bridge_summary()
    theorem = summary["pattern_progression_theorem"]

    assert theorem["l3_patterns"] == [[0, 1, 2]]
    assert theorem["l4_patterns"] == [[0, 0, 1, 2], [0, 1, 1, 2], [0, 1, 2, 2]]
    assert theorem["l5_patterns"] == [[0, 0, 1, 1, 2], [0, 0, 1, 2, 2], [0, 1, 1, 2, 2]]
    assert theorem["l6_patterns"] == [
        [0, 0, 0, 1, 1, 2],
        [0, 0, 0, 1, 2, 2],
        [0, 0, 1, 1, 1, 2],
        [0, 0, 1, 1, 2, 2],
        [0, 0, 1, 2, 2, 2],
        [0, 1, 1, 1, 2, 2],
        [0, 1, 1, 2, 2, 2],
    ]
    assert theorem["l3_balanced_triples_only"] is True
    assert theorem["l4_three_211_patterns_only"] is True
    assert theorem["l5_three_221_patterns_only"] is True
    assert theorem["l6_democratic_plus_six_asymmetric_patterns"] is True
    assert theorem["l6_multi_terms_only_cartan_only_democratic"] is True


def test_l4_to_l6_bridge_strengthens_exactly_at_the_first_gauge_return() -> None:
    summary = build_lie_tower_cycle_bridge_summary()
    bridge = summary["l4_to_l6_quark_bridge_escalation"]

    assert bridge["l4_full27_cubic_screen_nullity"] == 0
    assert bridge["l4_clean_quark_subspace_dimension"] == 4
    assert bridge["l4_effective_mode_count"] == 6
    assert bridge["l4_response_rank"] == 6
    assert bridge["l4_augmented_rank"] == 7
    assert bridge["l4_up_rank_lift"] == [2, 3]
    assert bridge["l4_down_rank_lift"] == [2, 3]
    assert bridge["l6_total_chiral_mode_count"] == 14
    assert bridge["l6_a2_mode_count"] == 6
    assert bridge["l6_cartan_mode_count"] == 8
    assert bridge["l6_response_rank"] == 9
    assert bridge["l6_augmented_rank"] == 10
    assert bridge["l6_up_rank_lift"] == [6, 9]
    assert bridge["l6_down_rank_lift"] == [6, 9]
    assert bridge["l6_currently_activates_only_cartan"] is True
    assert bridge["first_exact_gauge_return_is_l6"] is True
    assert (
        bridge["l6_residual_improvement_factor"]
        > bridge["l4_residual_improvement_factor"]
    )


def test_bridge_verdict_mentions_both_tower_cycle_and_quark_escalation() -> None:
    summary = build_lie_tower_cycle_bridge_summary()
    verdict = summary["bridge_verdict"]
    assert "Z3 grading exactly" in verdict
    assert "first multi-term layer" in verdict
    assert "six A2 channels" in verdict
    assert "six-effective-mode bridge family" in verdict
