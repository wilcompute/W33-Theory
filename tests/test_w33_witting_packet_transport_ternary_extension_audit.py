from __future__ import annotations

from scripts.w33_witting_packet_transport_ternary_extension_audit import analyze


def test_packet_reduced_transport_module_is_nonsplit_extension() -> None:
    payload = analyze()
    theorem = payload["packet_transport_ternary_extension_theorem"]
    module = payload["reduced_transport_module"]
    extension = payload["matter_flavour_extension"]

    assert theorem["the_packet_reduced_transport_module_is_a_nonsplit_extension_of_sign_by_trivial"] is True
    assert theorem["the_packet_quotient_character_equals_the_determinant_sign_shadow"] is True
    assert theorem["the_packet_matter_flavour_extension_has_dimensions_81_162_81"] is True
    assert (
        theorem["the_packet_extension_recovers_the_same_exact_nonsplit_162sector_as_the_centerquad_route"] is True
    )
    assert theorem["the_witting_packet_layer_carries_the_exact_nonsplit_ternary_transport_extension"] is True

    assert module["field"] == "F3"
    assert module["holonomy_group_order"] == 6
    assert module["projective_line_count"] == 4
    assert module["unique_invariant_line"] == [1, 2]
    assert module["invariant_projective_line_count"] == 1
    assert module["invariant_complement_count"] == 0
    assert module["adapted_group_is_upper_triangular"] is True
    assert module["top_character_values"] == [1]
    assert module["quotient_character_values"] == [1, 2]
    assert module["quotient_character_equals_determinant_character"] is True
    assert module["nonsplit_extension_witness_count"] == 4
    assert module["is_nonsplit_extension_of_sign_by_trivial"] is True

    assert extension == {
        "base_logical_qutrits": 81,
        "submodule_dimension": 81,
        "total_dimension": 162,
        "quotient_dimension": 81,
        "short_exact_sequence_dimensions": [81, 162, 81],
        "matches_flat_internal_dimension_exactly": True,
    }
