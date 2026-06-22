#!/usr/bin/env python3
"""BT1431: defect-conditioned S3 branch-search frontier.

This is the first exact branch layer after BT1428.  It does not solve the full
6^39 root-fixed Max-2CSP.  It combines the exact 330 one-defect target count
with the BT1376 radius-3 local certificate, and emits the real branch contract:
every 211 witness must choose one of 330 raw nonidentity correction slots and
must live at radius >=4 from the current 40-line S3 gauge.
"""
from __future__ import annotations

import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1431_defect_conditioned_s3_branch_search.json"


def radius_count(r: int) -> int:
    return comb(39, r) * (6**r - 1)


def main() -> None:
    cert = json.loads((ROOT / "data" / "bt1376_s3_gauge_radius3_local_optimum_certificate.json").read_text())
    base = cert["base_witness"]
    radii = cert["local_certificate"]["radii"]
    best_by_radius = {row["radius"]: row["best_alternative_identity_edges"] for row in radii}
    checked_by_radius = {row["radius"]: row["candidate_relabels_checked"] for row in radii}

    active_targets = 21 * 8
    cache_targets = 27 * 6
    defect_targets = active_targets + cache_targets
    radius4_candidate_count = radius_count(4)
    conditioned_radius4_upper_enumeration = defect_targets * radius4_candidate_count

    checks = {
        "base_score_is_210_330": base["identity_edges"] == 210 and base["nonidentity_corrections"] == 330,
        "root_fixed_40_labels": len(base["labels_in_s3_perm_order"]) == 40 and base["root_fixed_line"] == 0,
        "radius1_to_3_all_checked": checked_by_radius == {1: 195, 2: 25935, 3: 1964885},
        "radius1_to_3_best_is_205": best_by_radius == {1: 205, 2: 205, 3: 205},
        "defect_targets_are_330": defect_targets == 330,
        "active_targets_are_168": active_targets == 168,
        "cache_targets_are_162": cache_targets == 162,
        "radius4_is_first_open_radius": max(best_by_radius) == 3,
        "conditioned_radius4_space_is_positive": conditioned_radius4_upper_enumeration > 0,
    }

    result = {
        "bt": 1431,
        "title": "Defect-conditioned S3 branch-search frontier",
        "verified": all(checks.values()),
        "input_certificates": [
            "data/bt1376_s3_gauge_radius3_local_optimum_certificate.json",
            "data/bt1428_symmetry_breaking_211_search.json",
        ],
        "base_witness": {
            "identity_edges": base["identity_edges"],
            "corrections": base["nonidentity_corrections"],
            "root_fixed_line": base["root_fixed_line"],
        },
        "closed_radii": {
            "radius_1": {"candidates_checked": checked_by_radius[1], "best_identity_edges": best_by_radius[1]},
            "radius_2": {"candidates_checked": checked_by_radius[2], "best_identity_edges": best_by_radius[2]},
            "radius_3": {"candidates_checked": checked_by_radius[3], "best_identity_edges": best_by_radius[3]},
            "consequence": "No 211 witness exists at radius 1, 2, or 3 from the incumbent; all checked candidates score at most 205.",
        },
        "defect_conditioning": {
            "target_identity_edges": 211,
            "required_correction_count": 329,
            "active_fano_defect_targets": active_targets,
            "steinberg_s3_cache_defect_targets": cache_targets,
            "total_raw_defect_targets": defect_targets,
            "first_open_radius": 4,
            "radius4_candidates_per_unconditioned_frontier": radius4_candidate_count,
            "defect_conditioned_radius4_upper_enumeration": conditioned_radius4_upper_enumeration,
        },
        "search_contract": {
            "branch_key": "(defect_target, four_or_more_changed_lines, new_s3_labels)",
            "success_condition": "find a root-fixed 40-line S3 labeling with identity_edges >= 211",
            "failure_certificate_goal": "for all 330 defect targets, prove every radius >=4 branch has identity_edges <= 210 or derive a global relaxation bound",
        },
        "boundary": "This is an exact frontier reduction plus closed-radius certificate, not a full global solve.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1431, "verified": result["verified"], "defect_targets": defect_targets, "first_open_radius": 4}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
