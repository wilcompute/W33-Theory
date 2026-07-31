#!/usr/bin/env python3
"""Assemble the compact Passes 1500--1504 certificate from exact worker JSON."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "1500": "ccdc1e773121897bf87c03d7eaf40dd46b9daf0272f45b779c76fba643f6f3e6",
    "1501": "45ffc89206d187b1d6ed8bf6d74f19580ec6aaf8e89fe76d2145b1e53bd4add2",
    "1502": "cf30ef9d35441f22a1cb39380fb3bcdd00ae73cf592d2b7b337a0d4823b1b564",
    "1503": "c96cd9f52681256db4795e1c17fc8352951fa11f02a0d354d2b0efe52611328d",
    "1504": "60105b7a9d3b73cc714d5b828c5a9a6296af0fa383247884ba109ee60c137956",
}


def load(input_dir: Path, worker: str) -> dict:
    data = json.loads((input_dir / f"pass{worker}.json").read_text())
    assert data["sha256"] == EXPECTED[worker]
    assert data["theorem"].startswith(f"Pass {worker} ")
    return data


def assemble(input_dir: Path, source_root: Path) -> dict:
    w = {worker: load(input_dir, worker) for worker in EXPECTED}
    source_paths = [
        source_root / "analysis" / "w33_pass1500_1504_five_frontiers.py",
        *sorted((source_root / "analysis" / "pass1500_1504").glob("*.py")),
    ]
    source_sha = {
        str(path.relative_to(source_root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in source_paths
    }
    p2, p3 = w["1500"]["primes"]["2"], w["1500"]["primes"]["3"]
    relation = w["1504"]["unique_linear_relation_among_76_bridges"]
    return {
        "schema": "w33.pass1500_1504.five_frontiers.v1",
        "status": "PASS",
        "range": "1500-1504",
        "worker_sha256": EXPECTED,
        "source_sha256": source_sha,
        "pass1500_modular_ext_quivers": {
            "p2_vertex_count": p2["vertex_count"],
            "p2_ext1_matrix": p2["ext1_matrix_source_rows_target_columns"],
            "p2_arrow_dimension_sum": p2["arrow_dimension_sum"],
            "p2_radical_power_dimensions": p2["radical_power_dimensions"],
            "p2_loewy_layers": p2["loewy_layers_top_to_socle"],
            "p3_vertex_count": p3["vertex_count"],
            "p3_ext1_matrix": p3["ext1_matrix_source_rows_target_columns"],
            "p3_arrow_dimension_sum": p3["arrow_dimension_sum"],
            "p3_radical_power_dimensions": p3["radical_power_dimensions"],
            "p3_loewy_layers": p3["loewy_layers_top_to_socle"],
            "all_simple_endomorphism_fields_split": {
                "2": p2["all_simple_endomorphism_fields_split"],
                "3": p3["all_simple_endomorphism_fields_split"],
            },
        },
        "pass1501_tensor_fourier": {
            "block_dimensions": w["1501"]["block_dimensions"],
            "multiplicity_irreducible_pairs": [
                [b["multiplicity_space_dimension"], b["irreducible_degree"]]
                for b in w["1501"]["blocks"]
            ],
            "tensor_basis_U": w["1501"]["tensor_basis_U"],
            "tensor_inverse_Uinv": w["1501"]["tensor_inverse_Uinv"],
            "all_83_actions_sha256": w["1501"]["all_83_orbital_multiplicity_actions_sha256"],
            "exact_inverse_verified": w["1501"]["exact_inverse_verified"],
            "inverse_constructed_blockwise": w["1501"]["inverse_constructed_blockwise_from_central_projectors"],
        },
        "pass1502_bridge_classification": {
            "family_size": w["1502"]["family_size"],
            "sheet_rank_distribution": w["1502"]["sheet_rank_distribution"],
            "bridge_rank_distribution": w["1502"]["bridge_rank_distribution"],
            "rank81_sheet_count": w["1502"]["rank81_sheet_count"],
            "rank81_bridge_count": w["1502"]["rank81_bridge_count"],
            "rank81_full_on_all_14_sources": w["1502"]["rank81_bridges_full_on_all_14_mackey_sources"],
            "rank81_terminal_dimension_loss": w["1502"]["rank81_bridges_with_one_dimension_lost_in_terminal_5_space"],
            "sign_characters_preserve_rank": w["1502"]["sign_characters_preserve_sheet_rank_for_all_96_bridges"],
            "all_rank81_sheets_equal_steinberg": w["1502"]["all_rank81_sheets_equal_full_levi_cycle_space"],
        },
        "pass1503_maximal_overorder": {
            "orbital_order_contained": w["1503"]["orbital_order_contained_in_maximal_overorder"],
            "global_index": w["1503"]["global_index_maximal_over_orbital"],
            "global_index_factorization": w["1503"]["global_index_factorization"],
            "local_indices": w["1503"]["local_indices"],
            "maximal_discriminant": w["1503"]["maximal_order_reduced_trace_discriminant"],
            "orbital_discriminant": w["1503"]["orbital_reduced_trace_discriminant"],
            "discriminant_index_identity_verified": w["1503"]["discriminant_index_identity_verified"],
            "p_maximal_at_2_and_3": w["1503"]["p_maximal_at_2_and_3"],
            "maximal_basis_sha256": w["1503"]["transition_maximal_basis_in_orbital_coordinates"]["sha256"],
            "orbital_coordinates_sha256": w["1503"]["orbital_in_maximal_coordinates"]["sha256"],
        },
        "pass1504_linking_algebra": {
            "rank81_gauge_bridges": w["1504"]["rank81_gauge_bridges_input"],
            "independent_bridge_dimension": w["1504"]["independent_offdiagonal_bridge_dimension"],
            "relation_dimension": relation["dimension"],
            "relation_support": relation["support"],
            "relation_sha256": relation["sha256"],
            "relation_exact_over_Z": relation["exact_over_Z"],
            "collective_selector_image_rank": w["1504"]["collective_selector_image_rank"],
            "collective_cycle_detection_rank": w["1504"]["collective_cycle_detection_rank"],
            "left_corner_dimension": w["1504"]["left_generated_algebra_dimension"],
            "right_corner_dimension": w["1504"]["right_generated_algebra_dimension"],
            "left_common_commutant_dimension": w["1504"]["left_corner_certificate"]["common_commutant_dimension"],
            "right_common_commutant_dimension": w["1504"]["right_corner_certificate"]["common_commutant_dimension"],
            "bridge_bimodule_dimension": w["1504"]["closed_bridge_bimodule_dimension"],
            "linking_envelope_dimension": w["1504"]["linking_envelope_dimension"],
            "full_M201_dimension": w["1504"]["full_linking_matrix_algebra_dimension"],
            "strict_morita_context": w["1504"]["strict_morita_context"],
        },
        "boundaries": {worker: w[worker]["boundary"] for worker in EXPECTED},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = assemble(args.input_dir, args.source_root)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert args.output.read_text() == encoded
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print("PASS assemble 1500-1504", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
