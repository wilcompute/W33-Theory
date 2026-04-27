from __future__ import annotations

import json
from pathlib import Path

from scripts.w33_periodic_table_organization import (
    build_periodic_table_organization_summary,
    write_summary,
)
from tools.export_w33_periodic_table_organization import build_payload


DOC_NOTE = Path("docs/W33_PERIODIC_TABLE_ORGANIZATION.md")
PAPER_TEX = Path("w33_paper.tex")


def test_periodic_table_organization_summary_tracks_four_exact_rows() -> None:
    summary = build_periodic_table_organization_summary()
    rows = summary["rows"]

    assert summary["status"] == "ok"
    assert summary["layer_order"] == [
        "carrier",
        "realization",
        "algebra",
        "computation",
        "witness",
    ]

    realization = rows["realization_row"]
    assert realization["catalog_total"] == 7
    assert realization["csaszar_realizations"] == 5
    assert realization["szilassi_realizations"] == 2
    assert realization["common_symmetry_group"] == "Z2"
    assert realization["common_half_turn_map"] == "(x, y, z) -> (-x, -y, z)"
    assert realization["csaszar_vertex_orbits"] == 4
    assert realization["csaszar_face_orbits"] == 7
    assert realization["szilassi_vertex_orbits"] == 7
    assert realization["szilassi_face_orbits"] == 4
    assert realization["orbit_package_is_dual"] is True

    pascal = rows["pascal_computation_row"]
    assert pascal["projective_points"] == 40
    assert pascal["projective_lines_total"] == 130
    assert pascal["isotropic_lines"] == 40
    assert pascal["nonisotropic_lines"] == 90
    assert pascal["edge_partition"] == {"w33_edges": 240, "complement_edges": 540}
    assert pascal["local_line_split"] == {"total": 13, "isotropic": 4, "nonisotropic": 9}
    assert pascal["parseval_measurement_frame"] == {
        "line_module_resolution": "40 = 1 + 15 + 24",
        "spread_count": 36,
        "anti_line_count": 90,
        "spread_density": "1/4",
        "anti_line_density": "2/5",
        "centered_spread_probe_spectrum": {"0": 25, "18": 15},
        "centered_anti_line_probe_spectrum": {"0": 16, "36": 24},
    }
    assert pascal["signed_sector_operator"] == "S = A_iso - A_non = 2A + I - J"
    assert pascal["seidel_spectrum"] == {"-15": 1, "-7": 15, "5": 24}

    witness = rows["frontier_witness_row"]
    assert witness["tail_package_sizes"] == [81, 162, 81]
    assert witness["finite_ordered_path_carrier"] == {
        "path_count": 4320,
        "seed_stabilizer_size": 6,
        "completion_fibre_size": 3,
        "seed_completion_action_size": 6,
    }
    assert witness["quadrangle_branch_packet_no_go"] == {
        "ordered_path_count": 4320,
        "nonlocal_quadrangle_count": 1620,
        "target_cover_size": 540,
        "found_exact_cover": False,
        "visited_search_nodes": 1106,
    }
    assert witness["shared_transport_shadow"] == {
        "reduced_group_order": 6,
        "unique_invariant_projective_line": [1, 2],
        "invariant_complement_count": 0,
        "is_nonsplit_extension_of_sign_by_trivial": True,
        "fiber_nilpotent_increment": [[0, 1], [0, 0]],
        "matter_extension_dimensions": [81, 162, 81],
        "matter_extension_rank": 81,
    }
    assert witness["minimal_tail_transport_pair"] == {
        "denominator_lcm": 12,
        "cleared_coordinate_gcd": 217,
        "recovered_scale": "217/12",
    }
    assert witness["canonical_chart_target"] == {
        "coordinate": "dC",
        "required_value": "14105",
        "primitive_c_direction": "780",
        "transport_scale": "217/12",
        "factorization": "780 * (217/12)",
    }
    assert witness["current_zero_witness_point"] == {
        "C": "0",
        "L": "0",
        "Q_seed": "0",
        "Q_sd1": "0",
    }
    assert witness["exact_witness_point"] == {
        "C": "14105",
        "L": "143654",
        "Q_seed": "3396050/3",
        "Q_sd1": "3904481/4",
    }
    assert witness["affine_witness_displacement"] == witness["exact_witness_point"]
    assert witness["all_exact_factorizations_hold"] is True

    exceptional = rows["exceptional_envelope_row"]
    assert exceptional["one_qutrit_local_shell_size"] == 27
    assert exceptional["two_qutrit_projective_point_count"] == 40
    assert exceptional["two_qutrit_weyl_basis_size"] == 81
    assert exceptional["two_qutrit_edge_count"] == 240
    assert exceptional["three_qutrit_operator_basis_dim"] == 729
    assert exceptional["six_qutrit_heisenberg_irrep_dim"] == 729
    assert exceptional["e8_root_count"] == 240
    assert exceptional["e6_a2_mixed_root_split"] == {
        "e6_roots": 72,
        "a2_roots": 6,
        "mixed_roots": 162,
    }
    assert exceptional["e8_line_orbit_sizes"] == [36, 27, 27, 27, 1, 1, 1]
    assert exceptional["matter_lines_per_generation"] == 27
    assert exceptional["generation_count"] == 3
    assert exceptional["kernel_record_names"] == [
        "local_one_qutrit_heisenberg_e6_shell",
        "global_two_qutrit_pauli_clifford_kernel",
    ]
    assert exceptional["finite_extension_record_names"] == [
        "three_qutrit_sl27_closure",
        "six_qutrit_sp12_clifford_backbone",
        "e8_side_e6_a2_decomposition",
    ]
    assert exceptional["kernel_stops_before_e8_boundary"] is True
    assert exceptional["later_rungs_require_additional_finite_input"] is True
    assert exceptional["bridge_equalities"] == {
        "local_shell_equals_generation_orbit": True,
        "two_qutrit_edges_equal_e8_roots": True,
        "three_qutrit_basis_equals_six_qutrit_irrep": True,
    }

    theorem = summary["periodic_table_theorem"]
    assert theorem == {
        "realization_row_is_controlled_by_one_common_half_turn": True,
        "pascal_row_is_an_exact_sector_split_not_a_numerical_coincidence": True,
        "frontier_row_is_one_witness_problem_on_a_fixed_carrier": True,
        "exceptional_row_is_an_exact_finite_ladder_up_to_the_e8_boundary": True,
    }

    bridge = summary["same_table_bridge_theorem"]
    assert bridge == {
        "realization_row_supplies_one_exact_dual_realization_packet": True,
        "pascal_and_exceptional_rows_share_the_same_40_point_240_edge_backbone": True,
        "frontier_and_exceptional_rows_share_the_same_81_seed": True,
        "the_exceptional_boundary_and_frontier_witness_form_one_controlled_open_wall": True,
        "the_four_rows_belong_to_one_table_as_distinct_layers_of_one_q3_backbone": True,
    }


def test_periodic_table_organization_summary_writes_json(tmp_path: Path) -> None:
    out = write_summary(tmp_path / "w33_periodic_table_organization_summary.json")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["rows"]["realization_row"]["catalog_total"] == 7
    assert data["rows"]["pascal_computation_row"]["projective_lines_total"] == 130
    assert data["rows"]["frontier_witness_row"]["canonical_chart_target"]["required_value"] == "14105"
    assert data["rows"]["frontier_witness_row"]["quadrangle_branch_packet_no_go"]["found_exact_cover"] is False
    assert data["rows"]["exceptional_envelope_row"]["two_qutrit_weyl_basis_size"] == 81
    assert data["rows"]["exceptional_envelope_row"]["e6_a2_mixed_root_split"] == {
        "e6_roots": 72,
        "a2_roots": 6,
        "mixed_roots": 162,
    }
    assert data["same_table_bridge_theorem"][
        "the_four_rows_belong_to_one_table_as_distinct_layers_of_one_q3_backbone"
    ] is True


def test_export_payload_freezes_the_same_checked_rows() -> None:
    payload = build_payload()

    assert payload["kind"] == "w33_periodic_table_organization_summary"
    assert payload["layer_order"] == [
        "carrier",
        "realization",
        "algebra",
        "computation",
        "witness",
    ]
    assert payload["rows"]["realization_row"]["catalog_total"] == 7
    assert payload["rows"]["pascal_computation_row"]["projective_lines_total"] == 130
    assert payload["rows"]["pascal_computation_row"]["parseval_measurement_frame"] == {
        "line_module_resolution": "40 = 1 + 15 + 24",
        "spread_count": 36,
        "anti_line_count": 90,
        "spread_density": "1/4",
        "anti_line_density": "2/5",
        "centered_spread_probe_spectrum": {"0": 25, "18": 15},
        "centered_anti_line_probe_spectrum": {"0": 16, "36": 24},
    }
    assert payload["rows"]["frontier_witness_row"]["canonical_chart_target"]["required_value"] == "14105"
    assert payload["rows"]["frontier_witness_row"]["tail_package_sizes"] == [81, 162, 81]
    assert payload["rows"]["frontier_witness_row"]["quadrangle_branch_packet_no_go"][
        "found_exact_cover"
    ] is False
    assert payload["rows"]["exceptional_envelope_row"]["e8_line_orbit_sizes"] == [
        36,
        27,
        27,
        27,
        1,
        1,
        1,
    ]
    assert payload["periodic_table_theorem"] == {
        "realization_row_is_controlled_by_one_common_half_turn": True,
        "pascal_row_is_an_exact_sector_split_not_a_numerical_coincidence": True,
        "frontier_row_is_one_witness_problem_on_a_fixed_carrier": True,
        "exceptional_row_is_an_exact_finite_ladder_up_to_the_e8_boundary": True,
    }
    assert payload["same_table_bridge_theorem"] == {
        "realization_row_supplies_one_exact_dual_realization_packet": True,
        "pascal_and_exceptional_rows_share_the_same_40_point_240_edge_backbone": True,
        "frontier_and_exceptional_rows_share_the_same_81_seed": True,
        "the_exceptional_boundary_and_frontier_witness_form_one_controlled_open_wall": True,
        "the_four_rows_belong_to_one_table_as_distinct_layers_of_one_q3_backbone": True,
    }


def test_committed_artifact_matches_export_payload() -> None:
    artifact_path = Path("artifacts/w33_periodic_table_organization_summary.json")
    committed = json.loads(artifact_path.read_text(encoding="utf-8"))

    assert committed == build_payload()


def test_docs_and_paper_keep_the_five_layer_executable_language() -> None:
    doc_text = DOC_NOTE.read_text(encoding="utf-8")
    paper_text = PAPER_TEX.read_text(encoding="utf-8")

    assert "mixing five different things under one label" in doc_text
    assert "1. carrier" in doc_text
    assert "2. realization" in doc_text
    assert "3. algebra" in doc_text
    assert "4. computation" in doc_text
    assert "5. witness" in doc_text
    assert "scripts/w33_periodic_table_organization.py" in doc_text
    assert "scripts/w33_qutrit_ladder_audit.py" in doc_text
    assert "scripts/w33_e8_correspondence_boundary_audit.py" in doc_text
    assert "tests/test_w33_periodic_table_organization.py" in doc_text
    assert "tests/test_w33_qutrit_ladder_audit.py" in doc_text
    assert "tests/test_w33_e8_correspondence_boundary_audit.py" in doc_text
    assert "artifacts/w33_periodic_table_organization_summary.json" in doc_text
    assert "checks it directly against" in doc_text
    assert "build_payload()" in doc_text
    assert "exact qutrit ladder with E8-side `E6 + A2` boundary" in doc_text
    assert "Same-table bridge theorem." in doc_text
    assert "same `40`-point / `240`-edge shell" in doc_text
    assert "share the same `81` seed" in doc_text
    assert "one exact finite backbone read at" in doc_text

    assert "Organizing Layers: Carrier, Realization, Algebra, Computation, Witness" in paper_text
    assert (
        r"\boxed{\text{carrier} \;\to\; \text{realization} \;\to\; \text{algebra} \;\to\; \text{computation} \;\to\; \text{witness}.}"
        in paper_text
    )
    assert "The organization table is now also executable." in paper_text
    assert "The same-table bridge theorem is now short enough to state cleanly" in paper_text
    assert "$40$-point/$240$-edge shell" in paper_text
    assert "the same $81$ seed" in paper_text
    assert "one finite backbone" in paper_text
    assert "Exceptional envelope" in paper_text
    assert "exact qutrit ladder up to the $E_8$-side $E_6+A_2$ boundary" in paper_text
    assert "exact finite ladder up to the $E_8$ boundary" in paper_text
    assert r"\texttt{scripts/w33\_periodic\_table\_organization.py}" in paper_text
    assert r"\texttt{scripts/w33\_qutrit\_ladder\_audit.py}" in paper_text
    assert r"\texttt{scripts/w33\_e8\_correspondence\_boundary\_audit.py}" in paper_text
    assert r"\texttt{tests/test\_w33\_periodic\_table\_organization.py}" in paper_text
    assert r"\texttt{artifacts/w33\_periodic\_table\_organization\_summary.json}" in paper_text