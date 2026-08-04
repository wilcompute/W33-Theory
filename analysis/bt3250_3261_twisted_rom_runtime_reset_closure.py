#!/usr/bin/env python3
"""Coordinator for Passes 3250-3261 twisted/ROM/runtime/reset closure."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
OUT = ROOT / "data" / "PART_BT3250_BT3261_TWISTED_ROM_RUNTIME_RESET_CLOSURE.json"

from bt3250_3251_twisted_port_local_systems import compute as compute_twisted
from bt3252_3253_independent_curvature_verifier import construct_reference, reverse_numbering, verification_report
from bt3254_3255_typed_runtime_universes import compute as compute_runtime
from bt3256_3257_constrained_reset_semigroup import compute as compute_reset


def compute() -> dict:
    twisted = compute_twisted()
    reference = construct_reference()
    reverse_control = verification_report(reverse_numbering(reference), reference["semantic_sha256"])
    runtime = compute_runtime()
    reset = compute_reset()

    checks = {
        "free_rank_436": twisted["collapsed_complex"]["free_rank"] == 436,
        "D4_twisted_H1_870": next(row for row in twisted["local_systems"] if row["name"] == "D4_standard_F3_rank2")["twisted_H1_dimension"] == 870,
        "independent_876_states": reference["all_recursive_states"] == 876,
        "independent_770_initial": reference["unique_initial_states"] == 770,
        "numbering_invariant": reverse_control["accepted"] is True,
        "four_op_universe_24": runtime["universes"]["affine_universal_4op_v1"]["member_count"] == 24,
        "five_six_universe_194": runtime["universes"]["affine_universal_5_6op_v1"]["member_count"] == 194,
        "migration_one_plus_two": runtime["pass3195_migration"]["typed_census_joined"] == ["fast6"] and runtime["pass3195_migration"]["pending_194_census_records"] == 193,
        "passive_rank_three": reset["passive_result"]["minimum_rank"] == 3,
        "authorized_reset_length_two": reset["authorized_reset"]["shortest_rank_one_word_length"] == 2,
    }
    assert all(checks.values())

    payload = {
        "schema": "w33.pass3250_3261.twisted_rom_runtime_reset_closure.v1",
        "status": "PASS_EXACT_FIVE_FRONT_CLOSURE_SOURCE_EVIDENCE_PENDING",
        "pass3250_3251_twisted_local_systems": twisted,
        "pass3252_3253_independent_quotient": {
            "hypotheses": reference["hypotheses"],
            "raw_reachable_subsets": reference["raw_reachable_subsets"],
            "unique_initial_states": reference["unique_initial_states"],
            "all_recursive_states": reference["all_recursive_states"],
            "terminal_states": reference["terminal_states"],
            "semantic_sha256": reference["semantic_sha256"],
            "reversed_numbering_control": reverse_control,
        },
        "pass3254_3255_typed_runtime_universes": runtime,
        "pass3256_3257_constrained_reset": reset,
        "checks": checks,
        "evidence_boundary": {
            "exact_source": "finite-field local-system cohomology, independent finite-state quotient, exact affine-universe classification, passive transformation rank, and authorization-latch word length",
            "pending": "Icarus simulation, Yosys synthesis, HX8K placement, canonical front-door materialization, and three-PDF compilation",
            "physical": "No laboratory timing, energy, heat, optical loss, detector, coherence, fabrication, or fault-tolerance claim is made.",
        },
    }
    semantic = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["semantic_sha256"] = hashlib.sha256(semantic.encode()).hexdigest()
    return payload


def main() -> None:
    payload = compute()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "sha256": payload["semantic_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
