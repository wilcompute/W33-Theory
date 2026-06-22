#!/usr/bin/env python3
"""BT1435: radius-4 conditioned S3 solver harness.

This is the first branch-search harness after BT1431.  The radius-4 frontier is
large (106,515,045 unconditioned radius-4 relabelings, 35,149,964,850 if naively
paired with all 330 defect slots), so this tool creates a reproducible exact
branch manifest rather than pretending to have exhausted it.
"""
from __future__ import annotations

import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1435_radius4_conditioned_s3_solver.json"


def radius_count(r: int) -> int:
    return comb(39, r) * (6**r - 1)


def main() -> None:
    r4 = radius_count(4)
    defect_targets = 330
    active_targets = 168
    cache_targets = 162
    naive_pairs = r4 * defect_targets
    # Deterministic first branch batches: small enough for downstream exact scoring jobs.
    batches = [
        {"batch": 0, "family": "active_fano", "defect_start": 0, "defect_stop_exclusive": 21, "radius": 4},
        {"batch": 1, "family": "active_fano", "defect_start": 21, "defect_stop_exclusive": 42, "radius": 4},
        {"batch": 2, "family": "steinberg_s3_cache", "defect_start": 168, "defect_stop_exclusive": 195, "radius": 4},
        {"batch": 3, "family": "steinberg_s3_cache", "defect_start": 195, "defect_stop_exclusive": 222, "radius": 4},
    ]
    checks = {
        "radius4_count_exact": r4 == 106_515_045,
        "defect_targets_exact": defect_targets == active_targets + cache_targets == 330,
        "naive_conditioned_pairs_exact": naive_pairs == 35_149_964_850,
        "batch_manifest_nonempty": len(batches) == 4,
        "batches_are_radius4": all(b["radius"] == 4 for b in batches),
        "active_and_cache_families_present": {b["family"] for b in batches} == {"active_fano", "steinberg_s3_cache"},
    }
    result = {
        "bt": 1435,
        "title": "Radius-4 conditioned S3 solver harness",
        "verified": all(checks.values()),
        "frontier": {
            "first_open_radius": 4,
            "unconditioned_radius4_relabels": r4,
            "defect_targets": defect_targets,
            "active_fano_defects": active_targets,
            "steinberg_s3_cache_defects": cache_targets,
            "naive_defect_conditioned_radius4_pairs": naive_pairs,
        },
        "solver_batches": batches,
        "pruning_contract": {
            "primary_constraint": "defect target must become an identity residual edge",
            "secondary_constraint": "root line remains fixed to identity",
            "score_target": "identity_edges >= 211",
            "safe_stop": "any concrete 211 witness terminates the search; otherwise each batch must emit a no-witness certificate with max score <=210",
        },
        "boundary": "This is an exact branch-count and reproducible batch harness. It does not claim the 35.1B conditioned pairs have been exhausted.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1435, "verified": result["verified"], "radius4": r4, "conditioned_pairs": naive_pairs}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
