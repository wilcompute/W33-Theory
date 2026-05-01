from __future__ import annotations

from w33_yukawa_scaffold_bridge import build_yukawa_scaffold_summary


def test_yukawa_scaffold_records_exact_texture_and_projector_data() -> None:
    summary = build_yukawa_scaffold_summary()
    anchor = summary["sm_backbone_anchor"]
    texture = summary["canonical_texture"]
    projectors = summary["v4_projector_scaffold"]

    assert anchor["clean_higgs_slots"] == ["H_2", "Hbar_2"]
    assert anchor["clean_higgs_pair_is_h2_hbar2"] is True
    assert anchor["one_generation_spinor_dimension"] == 16
    assert anchor["three_generation_matter_dimension"] == 48

    assert texture["label_matrix"] == [
        ["AB", "I", "A"],
        ["AB", "I", "A"],
        ["A", "B", "0"],
    ]
    assert texture["label_matrix_is_slot_independent"] is True
    assert texture["reconstructs_exactly_for_both_slots"] is True
    assert texture["generation_0_diagonal_delta_equals_offdiag_1_to_0"] is True
    assert texture["generation_1_diagonal_delta_equals_offdiag_0_to_1"] is True
    assert texture["generation_2_diagonal_block_unchanged"] is True

    assert projectors["minus_minus_projector_vanishes"] is True
    assert projectors["plus_plus_is_inactive_support"] is True
    assert projectors["h2_split"] == {
        "minus_plus": ["u_c_1", "u_c_3"],
        "plus_minus": ["u_c_2", "nu_c"],
    }
    assert projectors["hbar2_split"] == {
        "minus_plus": ["d_c_1"],
        "plus_minus": ["d_c_2", "d_c_3", "e_c"],
    }
    assert projectors["h2_active_support_splits_as_2_plus_2"] is True
    assert projectors["hbar2_active_support_splits_as_1_plus_3"] is True


def test_yukawa_scaffold_records_a2_activation_and_ce2_boundary() -> None:
    summary = build_yukawa_scaffold_summary()
    a2 = summary["a2_activation_scaffold"]
    ce2 = summary["ce2_boundary"]
    frontier = summary["frontier_boundary"]

    assert a2["minimal_full_a2_activation_seed_modes"] == [[8, 9], [246, 247]]
    assert a2["minimal_full_activation_is_exactly_fan_type"] is True
    assert a2["minimal_rank_lift_seed_modes"] == [
        [8, 246],
        [8, 247],
        [9, 246],
        [9, 247],
    ]
    assert a2["minimal_rank_lift_seed_size"] == 2
    assert a2["max_response_rank_within_unit_seed_family"] == 11
    assert a2["max_augmented_rank_within_unit_seed_family"] == 12
    assert a2["fan_closure_has_full_3x3_support"] is True
    assert a2["fan_closure_has_isotropic_offdiag_shell"] is True

    assert ce2["generated_source_unit_count"] == 144
    assert ce2["projected_mode_count"] == 54
    assert ce2["response_rank"] == 28
    assert ce2["augmented_rank"] == 28
    assert ce2["arbitrary_quark_screen_rank"] == 36
    assert ce2["arbitrary_quark_screen_nullity"] == 0
    assert ce2["trivial_closure_total_residual_norm"] == 0.0
    assert ce2["zero_is_unique_clean_point"] is True
    assert ce2["l4_response_contained_in_ce2"] is True

    assert frontier["yukawa_scaffold_is_exact"] is True
    assert frontier["nonzero_yukawa_eigenvalues_still_open"] is True
    assert frontier["exact_open_problem_is_spectrum_not_support_or_symmetry"] is True
