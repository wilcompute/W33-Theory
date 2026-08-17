#!/usr/bin/env python3
"""Collision-recovered runner for the exact eight-probe M2(F2) packet.

The finite verifier first landed under Pass5832--5839 after this lane had reserved that
range, but a separate parallel theorem packet had also committed under those numbers.
This runner reissues the already-verified mathematics under the clean Pass5848--5855
namespace. It deliberately imports the original exact finite routines so the rename
cannot silently change the computation.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "analysis" / "w33_pass5832_5839_normalizer_code_pauli_allq.py"
OUTPUT = ROOT / "data" / "PART_W33_PASS5848_5855_NORMALIZER_CODE_PAULI_ALLQ.json"


def load_legacy():
    spec = importlib.util.spec_from_file_location("w33_matrix_eight_probe_core", LEGACY)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import exact core from {LEGACY}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def publication_packet() -> dict:
    return {
        "canonical_public_index": "docs/index.html",
        "cards_to_register_and_materialize": [
            ["pass-5776-5783-reye-latin-common-core", "analysis/PASS5776_5783_index_insert.html"],
            ["pass-5792-5799-matrix-ring-transpose-outer", "analysis/PASS5792_5799_index_insert.html"],
            ["pass-5816-5823-matrix-fourier-rank", "analysis/PASS5816_5823_index_insert.html"],
            ["pass-5824-5831-integral-w9-lattices", "analysis/PASS5824_5831_index_insert.html"],
            ["pass-5848-5855-normalizer-code-pauli-allq", "analysis/PASS5848_5855_index_insert.html"],
        ],
        "stale_collision_card": "pass-5832-5839-normalizer-code-pauli-allq",
        "materialization_rule": (
            "Remove the stale collision card if it was materialized by a queued legacy run; "
            "then insert each corrected card independently into docs/index.html and index.html, "
            "rejecting duplicates without requiring the two surfaces to be byte-identical."
        ),
        "manuscript_rule": (
            "The shared frontier must include PASS5848_5855 and must not include the "
            "superseded PASS5832_5839 matrix insert."
        ),
    }


def main() -> None:
    m = load_legacy()
    gl4 = m.gl4_perms()
    p5848 = m.normalizer_packet(gl4)
    naff = p5848.pop("_normalizer_affine_perms")
    out = {
        "schema": "w33.pass5848_5855.normalizer_code_pauli_allq.v1",
        "status": "PASS",
        "renumbered_from_contaminated_range": [5832, 5839],
        "pass_5848_full_normalizer": p5848,
        "pass_5849_code_snf_interface": m.code_packet(),
        "pass_5850_two_qubit_object_isometry": m.pauli_packet(gl4),
        "pass_5851_all_field_matrix_fourier_radon": m.allq_packet(),
        "pass_5852_publication_front_doors": publication_packet(),
        "pass_5853_determinant_bent_chirp": m.bent_packet(),
        "pass_5854_unit_cayley_rook_graph": m.rook_packet(naff),
        "pass_5855_simplex_line_puncture": m.simplex_packet(),
        "boundary": (
            "Exact finite algebra, coding, Fourier analysis, graph theory and publication "
            "plumbing. The two-qubit bridge is an isomorphism of the nonzero dual Fourier "
            "label geometry to the Pauli-point geometry; it is not a q=5 physical-state "
            "embedding. The old Pass5832-5839 labels are superseded solely because of a "
            "namespace collision, not because the mathematics changed."
        ),
    }
    OUTPUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
