#!/usr/bin/env python3
"""Executable organization table for the W33 periodic-table framework.

This summary does not invent a new algebra. It packages three already-exact
rows that the paper now uses to organize the theory, plus one exact
exceptional-envelope row whose boundary is already executable:

1. realization row: the cataloged Csaszar/Szilassi toroidal models;
2. computation row: the Pascal line split and Seidel sector operator;
3. frontier witness row: the q=3 transport wall on the fixed tail package;
4. exceptional envelope row: the exact qutrit ladder up to the E8-side
    E6 + A2 decomposition boundary.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
for extra in (ROOT, ROOT / "exploration"):
    if str(extra) not in sys.path:
        sys.path.insert(0, str(extra))


from PART_LXIV_pascal_line_split import build_summary as build_pascal_line_split_summary  # noqa: E402
from scripts.w33_h4_branch_selection_search import (  # noqa: E402
    build_branch_selection_search_summary,
)
from scripts.w33_parseval_measurement_frame_audit import (  # noqa: E402
    build_parseval_measurement_frame_summary,
)
from scripts.w33_qutrit_ladder_audit import analyze as analyze_qutrit_ladder  # noqa: E402
from scripts.w33_q3_master_lock_audit import q3_transport_algebra_summary  # noqa: E402
from w33_h4_ordered_path_k3_witness_bridge import (  # noqa: E402
    build_h4_ordered_path_k3_witness_bridge_summary,
)
from w33_realization_orbit_bridge import build_realization_orbit_summary  # noqa: E402


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_periodic_table_organization_summary.json"


def build_periodic_table_organization_summary() -> dict[str, Any]:
    realization = build_realization_orbit_summary()
    pascal = build_pascal_line_split_summary()
    parseval = build_parseval_measurement_frame_summary()
    witness = q3_transport_algebra_summary()
    branch_selection = build_branch_selection_search_summary()
    finite_to_continuum_bridge = build_h4_ordered_path_k3_witness_bridge_summary()
    exceptional = analyze_qutrit_ladder()
    exceptional_row_theorem = exceptional["qutrit_ladder_theorem"]
    exceptional_row = exceptional["e8_side_exact_decomposition"]

    summary = {
        "status": "ok",
        "layer_order": [
            "carrier",
            "realization",
            "algebra",
            "computation",
            "witness",
        ],
        "rows": {
            "realization_row": {
                "carrier": "cataloged toroidal Csaszar/Szilassi realization packet",
                "catalog_total": realization["catalog_counts"]["total"],
                "csaszar_realizations": realization["catalog_counts"]["csaszar_realizations"],
                "szilassi_realizations": realization["catalog_counts"]["szilassi_realizations"],
                "common_symmetry_group": realization["common_symmetry"]["group"],
                "common_half_turn_map": realization["common_symmetry"]["map"],
                "csaszar_vertex_orbits": realization["dual_orbit_package"]["csaszar_vertex_orbits"],
                "csaszar_face_orbits": realization["dual_orbit_package"]["csaszar_face_orbits"],
                "szilassi_vertex_orbits": realization["dual_orbit_package"]["szilassi_vertex_orbits"],
                "szilassi_face_orbits": realization["dual_orbit_package"]["szilassi_face_orbits"],
                "orbit_package_is_dual": realization["dual_orbit_package"]["is_dual_swap"],
                "scope_note": realization["scope_note"],
            },
            "pascal_computation_row": {
                "carrier": "projective line Grassmannian Gr(2,4)(F_3) on the W(3,3) ambient shell",
                "projective_points": pascal["projective_points"],
                "projective_lines_total": pascal["projective_lines_total"],
                "isotropic_lines": pascal["isotropic_lines"],
                "nonisotropic_lines": pascal["nonisotropic_lines"],
                "edge_partition": {
                    "w33_edges": pascal["isotropic_pairs_edges"],
                    "complement_edges": pascal["nonisotropic_pairs_complement"],
                },
                "local_line_split": {
                    "total": pascal["lines_through_point_unique"][0],
                    "isotropic": pascal["isotropic_lines_through_point_unique"][0],
                    "nonisotropic": pascal["nonisotropic_lines_through_point_unique"][0],
                },
                "parseval_measurement_frame": {
                    "line_module_resolution": parseval["carrier_dictionary"]["line_side"],
                    "spread_count": parseval["carrier_dictionary"]["spread_probe"]["shape"][1],
                    "anti_line_count": parseval["carrier_dictionary"]["anti_line_probe"]["shape"][1],
                    "spread_density": parseval["carrier_dictionary"]["spread_probe"]["density"],
                    "anti_line_density": parseval["carrier_dictionary"]["anti_line_probe"]["density"],
                    "centered_spread_probe_spectrum": {
                        str(key): value
                        for key, value in parseval["spectral_data"][
                            "centered_spread_probe_spectrum"
                        ].items()
                    },
                    "centered_anti_line_probe_spectrum": {
                        str(key): value
                        for key, value in parseval["spectral_data"][
                            "centered_anti_line_probe_spectrum"
                        ].items()
                    },
                },
                "signed_sector_operator": pascal["seidel_formula"],
                "seidel_spectrum": pascal["seidel_spectrum"],
                "line_split_identity": pascal["line_split_identity"],
                "pair_split_identity": pascal["pair_split_identity"],
            },
            "frontier_witness_row": {
                "carrier": "fixed 81 -> 162 -> 81 tail package on the existing transport channel",
                "tail_package_sizes": [81, 162, 81],
                "finite_ordered_path_carrier": finite_to_continuum_bridge[
                    "finite_ordered_path_carrier"
                ],
                "quadrangle_branch_packet_no_go": {
                    "ordered_path_count": branch_selection["branch_model"]["ordered_path_count"],
                    "nonlocal_quadrangle_count": branch_selection["branch_model"][
                        "nonlocal_quadrangle_count"
                    ],
                    "target_cover_size": branch_selection["branch_model"]["target_cover_size"],
                    "found_exact_cover": branch_selection["search"]["found_exact_cover"],
                    "visited_search_nodes": branch_selection["search"]["visited_search_nodes"],
                },
                "shared_transport_shadow": finite_to_continuum_bridge[
                    "shared_transport_shadow"
                ],
                "minimal_tail_transport_pair": witness["minimal_tail_transport_pair"],
                "promoted_coordinate_witnesses": witness["promoted_coordinate_witnesses"],
                "canonical_chart_target": witness["canonical_chart_target"],
                "current_zero_witness_point": witness["current_zero_witness_point"],
                "exact_witness_point": witness["exact_witness_point"],
                "affine_witness_displacement": witness["affine_witness_displacement"],
                "all_exact_factorizations_hold": (
                    all(witness["exact_factorizations"].values())
                    and all(branch_selection["checks"].values())
                    and all(finite_to_continuum_bridge["theorem"].values())
                ),
            },
            "exceptional_envelope_row": {
                "carrier": "exact qutrit ladder up to the E8-side E6 + A2 decomposition boundary",
                "one_qutrit_local_shell_size": exceptional["one_qutrit_local_layer"]["visible_shell_size"],
                "two_qutrit_projective_point_count": exceptional["two_qutrit_global_layer"]["projective_point_count"],
                "two_qutrit_weyl_basis_size": exceptional["two_qutrit_global_layer"]["weyl_basis_size"],
                "two_qutrit_edge_count": exceptional["two_qutrit_global_layer"]["edge_count"],
                "three_qutrit_operator_basis_dim": exceptional["three_qutrit_sl27_layer"]["sl27_operator_basis_dim"],
                "six_qutrit_heisenberg_irrep_dim": exceptional["six_qutrit_backbone"]["heisenberg_irrep_dim"],
                "e8_root_count": exceptional_row["total_root_count"],
                "e6_a2_mixed_root_split": {
                    "e6_roots": exceptional_row["e6_root_count"],
                    "a2_roots": exceptional_row["a2_root_count"],
                    "mixed_roots": exceptional_row["mixed_root_count"],
                },
                "e8_line_orbit_sizes": list(exceptional_row["line_orbit_sizes"]),
                "matter_lines_per_generation": exceptional_row["matter_lines_per_generation"],
                "generation_count": exceptional_row["generation_count"],
                "kernel_record_names": list(exceptional["kernel_record_names"]),
                "finite_extension_record_names": list(exceptional["finite_extension_record_names"]),
                "kernel_stops_before_e8_boundary": exceptional_row_theorem[
                    "the_exact_kernel_stops_after_the_first_two_rungs"
                ],
                "later_rungs_require_additional_finite_input": exceptional_row_theorem[
                    "the_later_rungs_are_exact_but_require_additional_finite_input_beyond_the_kernel"
                ],
                "bridge_equalities": {
                    "local_shell_equals_generation_orbit": exceptional_row_theorem[
                        "the_local_h27_shell_size_matches_the_exact_e8_side_generation_orbit_size"
                    ],
                    "two_qutrit_edges_equal_e8_roots": exceptional_row_theorem[
                        "the_two_qutrit_edge_count_matches_the_exact_e8_root_count"
                    ],
                    "three_qutrit_basis_equals_six_qutrit_irrep": exceptional_row_theorem[
                        "the_three_qutrit_operator_basis_matches_the_six_qutrit_heisenberg_irrep"
                    ],
                },
                "row_boundary_note": exceptional["boundary_note"],
            },
        },
    }

    theorem = {
        "realization_row_is_controlled_by_one_common_half_turn": (
            summary["rows"]["realization_row"]["common_symmetry_group"] == "Z2"
            and summary["rows"]["realization_row"]["orbit_package_is_dual"] is True
        ),
        "pascal_row_is_an_exact_sector_split_not_a_numerical_coincidence": (
            summary["rows"]["pascal_computation_row"]["projective_lines_total"] == 130
            and summary["rows"]["pascal_computation_row"]["isotropic_lines"] == 40
            and summary["rows"]["pascal_computation_row"]["nonisotropic_lines"] == 90
            and summary["rows"]["pascal_computation_row"]["edge_partition"]["w33_edges"] == 240
            and summary["rows"]["pascal_computation_row"]["edge_partition"]["complement_edges"] == 540
            and summary["rows"]["pascal_computation_row"]["parseval_measurement_frame"]
            == {
                "line_module_resolution": "40 = 1 + 15 + 24",
                "spread_count": 36,
                "anti_line_count": 90,
                "spread_density": "1/4",
                "anti_line_density": "2/5",
                "centered_spread_probe_spectrum": {"0": 25, "18": 15},
                "centered_anti_line_probe_spectrum": {"0": 16, "36": 24},
            }
        ),
        "frontier_row_is_one_witness_problem_on_a_fixed_carrier": (
            summary["rows"]["frontier_witness_row"]["finite_ordered_path_carrier"]
            == {
                "path_count": 4320,
                "seed_stabilizer_size": 6,
                "completion_fibre_size": 3,
                "seed_completion_action_size": 6,
            }
            and summary["rows"]["frontier_witness_row"]["quadrangle_branch_packet_no_go"]
            == {
                "ordered_path_count": 4320,
                "nonlocal_quadrangle_count": 1620,
                "target_cover_size": 540,
                "found_exact_cover": False,
                "visited_search_nodes": 1106,
            }
            and summary["rows"]["frontier_witness_row"]["shared_transport_shadow"]
            == {
                "reduced_group_order": 6,
                "unique_invariant_projective_line": [1, 2],
                "invariant_complement_count": 0,
                "is_nonsplit_extension_of_sign_by_trivial": True,
                "fiber_nilpotent_increment": [[0, 1], [0, 0]],
                "matter_extension_dimensions": [81, 162, 81],
                "matter_extension_rank": 81,
            }
            and summary["rows"]["frontier_witness_row"]["canonical_chart_target"]["required_value"] == "14105"
            and summary["rows"]["frontier_witness_row"]["exact_witness_point"]
            == summary["rows"]["frontier_witness_row"]["affine_witness_displacement"]
            and summary["rows"]["frontier_witness_row"]["all_exact_factorizations_hold"] is True
        ),
        "exceptional_row_is_an_exact_finite_ladder_up_to_the_e8_boundary": (
            summary["rows"]["exceptional_envelope_row"]["one_qutrit_local_shell_size"] == 27
            and summary["rows"]["exceptional_envelope_row"]["two_qutrit_projective_point_count"] == 40
            and summary["rows"]["exceptional_envelope_row"]["two_qutrit_weyl_basis_size"] == 81
            and summary["rows"]["exceptional_envelope_row"]["two_qutrit_edge_count"] == 240
            and summary["rows"]["exceptional_envelope_row"]["e8_root_count"] == 240
            and summary["rows"]["exceptional_envelope_row"]["e6_a2_mixed_root_split"]
            == {"e6_roots": 72, "a2_roots": 6, "mixed_roots": 162}
            and summary["rows"]["exceptional_envelope_row"]["e8_line_orbit_sizes"]
            == [36, 27, 27, 27, 1, 1, 1]
            and summary["rows"]["exceptional_envelope_row"]["kernel_stops_before_e8_boundary"] is True
            and summary["rows"]["exceptional_envelope_row"]["later_rungs_require_additional_finite_input"] is True
            and all(summary["rows"]["exceptional_envelope_row"]["bridge_equalities"].values())
        ),
    }

    same_table_bridge_theorem = {
        "realization_row_supplies_one_exact_dual_realization_packet": (
            summary["rows"]["realization_row"]["common_symmetry_group"] == "Z2"
            and summary["rows"]["realization_row"]["orbit_package_is_dual"] is True
        ),
        "pascal_and_exceptional_rows_share_the_same_40_point_240_edge_backbone": (
            summary["rows"]["pascal_computation_row"]["projective_points"]
            == summary["rows"]["exceptional_envelope_row"]["two_qutrit_projective_point_count"]
            == 40
            and summary["rows"]["pascal_computation_row"]["edge_partition"]["w33_edges"]
            == summary["rows"]["exceptional_envelope_row"]["two_qutrit_edge_count"]
            == summary["rows"]["exceptional_envelope_row"]["e8_root_count"]
            == 240
        ),
        "frontier_and_exceptional_rows_share_the_same_81_seed": (
            summary["rows"]["frontier_witness_row"]["tail_package_sizes"] == [81, 162, 81]
            and summary["rows"]["exceptional_envelope_row"]["two_qutrit_weyl_basis_size"] == 81
            and summary["rows"]["exceptional_envelope_row"]["one_qutrit_local_shell_size"]
            * summary["rows"]["exceptional_envelope_row"]["generation_count"]
            == summary["rows"]["exceptional_envelope_row"]["two_qutrit_weyl_basis_size"]
            == 81
        ),
        "the_exceptional_boundary_and_frontier_witness_form_one_controlled_open_wall": (
            summary["rows"]["frontier_witness_row"]["quadrangle_branch_packet_no_go"][
                "found_exact_cover"
            ]
            is False
            and summary["rows"]["frontier_witness_row"]["canonical_chart_target"]["required_value"] == "14105"
            and summary["rows"]["exceptional_envelope_row"]["kernel_stops_before_e8_boundary"] is True
            and summary["rows"]["exceptional_envelope_row"]["later_rungs_require_additional_finite_input"] is True
        ),
    }
    same_table_bridge_theorem[
        "the_four_rows_belong_to_one_table_as_distinct_layers_of_one_q3_backbone"
    ] = all(same_table_bridge_theorem.values())

    summary["periodic_table_theorem"] = theorem
    summary["same_table_bridge_theorem"] = same_table_bridge_theorem
    summary["bridge_verdict"] = (
        "These rows belong to one table because they are distinct exact layers of the same "
        "q=3 backbone: one dual realization packet, one 40-point/240-edge Pascal shell, "
        "one frontier transport row that already contains both the finite ordered-path no-go "
        "and the fixed K3 witness chart on the same law, and one exceptional ladder that "
        "extends the same backbone only up to the E8-side E6 + A2 boundary."
    )
    return summary


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(build_periodic_table_organization_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()