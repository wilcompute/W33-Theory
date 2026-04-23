from __future__ import annotations

import json
from pathlib import Path

from scripts.w33_witting_packet_transport_path_groupoid_audit import analyze


def test_packet_transport_path_groupoid_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_transport_path_groupoid_theorem"]

    assert theorem["the_packet_transport_a2_data_defines_an_exact_path_groupoid_representation"] is True
    assert (
        theorem[
            "the_packet_spanning_tree_gauge_trivializes_all_tree_edges_and_realizes_full_weyl_a2_on_fundamental_cycles"
        ]
        is True
    )
    assert theorem["the_packet_path_groupoid_has_no_nonzero_real_flat_section"] is True
    assert theorem["the_packet_path_groupoid_has_a_unique_invariant_projective_line_12_over_f3"] is True
    assert theorem["the_packet_mod3_quotient_character_is_the_exact_binary_shadow"] is True
    assert theorem[
        "the_packet_path_groupoid_recovers_the_same_mod3_transport_shadow_as_the_centerquad_route"
    ] is True
    assert theorem["the_witting_packet_layer_carries_the_exact_transport_path_groupoid_shadow"] is True


def test_packet_transport_path_groupoid_records_match_expected_counts() -> None:
    payload = analyze()
    groupoid = payload["path_groupoid"]
    gauge = payload["spanning_tree_gauge"]
    real_local = payload["real_local_system"]
    ternary = payload["ternary_reduction"]
    crosswalk = payload["invariant_crosswalk"]

    assert groupoid["objects"] == 45
    assert groupoid["undirected_generating_edges"] == 720
    assert groupoid["directed_generating_morphisms"] == 1440
    assert groupoid["path_transport_respects_inversion"] is True
    assert gauge == {
        "root_vertex": 0,
        "tree_edges": 44,
        "fundamental_cycles": 676,
        "all_tree_edges_gauge_trivialized": True,
        "fundamental_cycle_holonomy_group_order": 6,
        "fundamental_cycle_holonomies_realize_full_weyl_a2": True,
    }
    assert real_local == {
        "common_fixed_subspace_dimension": 0,
        "has_nonzero_flat_section": False,
    }
    assert ternary["modulus"] == 3
    assert ternary["common_fixed_subspace_dimension"] == 1
    assert ternary["unique_invariant_projective_line"] == [1, 2]
    assert ternary["adapted_group_is_upper_triangular"] is True
    assert ternary["quotient_character_values"] == [1, 2]
    assert ternary["quotient_character_is_exact_binary_shadow"] is True
    assert crosswalk == {
        "real_flat_section_dimension_matches_centerquad": True,
        "ternary_flat_section_dimension_matches_centerquad": True,
        "invariant_line_matches_centerquad": True,
        "binary_shadow_matches_centerquad": True,
    }


def test_packet_transport_path_groupoid_json_shape(tmp_path: Path) -> None:
    from scripts.w33_witting_packet_transport_path_groupoid_audit import main

    assert callable(main)
    out = tmp_path / "packet_transport_path_groupoid.json"
    out.write_text(json.dumps(analyze(), indent=2, default=int), encoding="utf-8")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["ternary_reduction"]["unique_invariant_projective_line"] == [1, 2]
