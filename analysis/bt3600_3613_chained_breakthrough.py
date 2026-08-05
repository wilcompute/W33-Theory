#!/usr/bin/env python3
"""Passes 3600--3613 official wrapper for the chained breakthrough packet."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from analysis._bt3506_3519_provisional_impl import build_certificate as build_provisional

PROVISIONAL_SHA = "7ad66eec9cbb1b3f207eb4215a348cb9a63e0be9ab7876e53209dbed3099a13f"


def build_certificate() -> dict:
    provisional = build_provisional()
    assert provisional["semantic_sha256"] == PROVISIONAL_SHA
    dependency = provisional["dependency_hypergraph"]
    projector = provisional["characteristic_three_projector"]
    m4 = provisional["transported_M4_grid"]
    hardware = provisional["five_channel_hardware"]
    tomotope = provisional["tomotope_lift"]
    bonkers = provisional["bonkers"]
    result = {
        "schema": "w33.bt3600_3613.chained_breakthrough.v1",
        "status": "PASS_7_FRONTS",
        "passes": list(range(3600, 3614)),
        "rehome": {
            "provisional_ranges": [[3506, 3519], [3584, 3597]],
            "reason": (
                "concurrent master packets claimed both provisional ranges; "
                "Passes 3600-3613 were reserved directly on master before publication"
            ),
            "provisional_semantic_sha256": PROVISIONAL_SHA,
        },
        "live_boundaries": {
            "covering_radius": [389, 435],
            "chromatic_number": [10, 11],
        },
        "theorems": {
            "dependency_hypergraph": {
                "vertices": dependency["vertices"],
                "dependency_triples": dependency["dependency_triples"],
                "triple_size": dependency["triple_size"],
                "face_degree": dependency["face_degree"],
                "pair_codegrees": dependency["pair_codegrees"],
                "supported_face_pairs": dependency["supported_face_pairs"],
                "weighted_two_section_degree": dependency["weighted_two_section_degree"],
                "incidence_ranks": dependency["incidence_ranks"],
                "ordinary_multiplicity_fingerprint": dependency["ordinary_multiplicity_fingerprint"],
                "spectrum": [[item["eigenvalue"], item["multiplicity"]] for item in dependency["spectrum"]],
            },
            "characteristic_three_projector": {
                "minimal_polynomial": projector["minimal_polynomial"],
                "relation": projector["relation"],
                "projector": projector["projector"],
                "projector_rank": projector["projector_rank"],
                "projector_idempotent": projector["projector_idempotent"],
                "operator_power_ranks": projector["operator_power_ranks"],
                "generalized_zero_dimension": projector["generalized_zero_dimension"],
                "generalized_zero_power_ranks": projector["generalized_zero_power_ranks"],
                "generalized_zero_jordan_type": projector["generalized_zero_jordan_type"],
                "antipodal_symmetric_image_rank": projector["antipodal_symmetric_image_rank"],
                "antipodal_antisymmetric_image_rank": projector["antipodal_antisymmetric_image_rank"],
            },
            "transported_M4_grid": {
                "weight_classes": m4["weight_classes"],
                "best_weights": m4["best_weights"],
                "best_lambda_min": m4["best_lambda_min"],
                "best_lambda_max": m4["best_lambda_max"],
                "best_hoffman_ratio": m4["best_hoffman_ratio"],
                "boundary": "finite deterministic ternary grid, not unrestricted optimum",
            },
            "five_channel_hardware": {
                "minimum_binary_operations": hardware["minimum_binary_operations"],
                "breadth_first_state_counts_depth_0_to_4": hardware["breadth_first_state_counts_depth_0_to_4"],
                "order": hardware["order"],
                "witness": hardware["witness"],
            },
            "tomotope_lift": {
                "configuration": tomotope["configuration"],
                "four_face_six_edge_cell_candidates": tomotope["four_face_six_edge_cell_candidates"],
                "eight_cell_double_cover_solutions": tomotope["eight_cell_double_cover_solutions"],
            },
            "missing_57_induced_decomposition_no_go": {
                key: bonkers["missing_57_induced_decomposition_no_go"][key]
                for key in (
                    "hypothetical_graph",
                    "tempting_partition",
                    "induced_Clebsch_external_degree_sum",
                    "induced_W33_external_degree_sum",
                    "required_apex_incidence_difference",
                    "maximum_possible_apex_incidence_difference",
                )
            },
            "W33_Clebsch_Gewirtz_spectral_completion": {
                "polynomial": bonkers["W33_Clebsch_Gewirtz_spectral_completion"]["polynomial"],
                "p_Clebsch_spectrum": bonkers["W33_Clebsch_Gewirtz_spectral_completion"]["p(Clebsch)_spectrum"],
                "W33_nonprincipal_spectrum": bonkers["W33_Clebsch_Gewirtz_spectral_completion"]["W33_nonprincipal_spectrum"],
                "Gewirtz_nonprincipal_spectrum": bonkers["W33_Clebsch_Gewirtz_spectral_completion"]["Gewirtz_nonprincipal_spectrum"],
                "boundary": "functional-calculus completion, not graph embedding or canonical intertwiner",
            },
        },
        "evidence_boundary": [
            "The radius interval remains 389<=R<=435.",
            "The chromatic interval remains 10<=chi(H)<=11.",
            "The rank-81 image is an explicit direct summand but is not labelled simple.",
            "No observed Icarus, Yosys, FPGA, PDF, laboratory, M57, or physical result is asserted by the source certificate.",
        ],
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = hashlib.sha256(payload).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"], result["semantic_sha256"])


if __name__ == "__main__":
    main()
