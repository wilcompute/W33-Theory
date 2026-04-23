from __future__ import annotations

from scripts.w33_witting_packet_transport_ternary_line_audit import analyze


def test_packet_transport_ternary_line_selects_canonical_qutrit_sector() -> None:
    payload = analyze()
    theorem = payload["packet_transport_ternary_line_theorem"]
    transport = payload["transport_side"]
    matter = payload["matter_side"]
    combined = payload["combined_sector"]

    assert theorem["the_packet_transport_shadow_has_a_unique_ternary_invariant_line"] is True
    assert theorem["the_w33_ternary_homological_code_has_exactly_81_logical_qutrits"] is True
    assert (
        theorem[
            "tensoring_the_packet_transport_line_with_the_homological_code_gives_a_canonical_81dimensional_sector"
        ]
        is True
    )
    assert (
        theorem["keeping_the_full_reduced_a2_fiber_gives_162_matching_the_flat_internal_dimension"] is True
    )
    assert theorem["the_witting_packet_transport_shadow_selects_the_canonical_ternary_matter_line"] is True

    assert transport == {
        "real_flat_section_dimension": 0,
        "ternary_flat_section_dimension": 1,
        "invariant_line": [1, 2],
        "quotient_character_values": [1, 2],
    }
    assert matter == {
        "homological_field": "F3",
        "logical_qutrits": 81,
        "canonical_transport_stable_sector_dimension": 81,
    }
    assert combined == {
        "full_reduced_a2_fiber_rank": 2,
        "matter_flavour_dimension": 162,
        "flat_internal_dimension": 162,
        "matches_flat_internal_dimension_exactly": True,
    }
