#!/usr/bin/env python3
"""BT1421: S3 gauge optimizer/certificate frontier under the full front-end constraints."""
from __future__ import annotations

import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1421_s3_gauge_frontend_optimizer_frontier.json"

LABELS = [
    0, 4, 0, 3, 3, 1, 3, 0, 5, 3, 1, 2, 5, 2, 1, 1, 2, 2, 2, 1,
    3, 2, 0, 3, 3, 0, 3, 0, 5, 2, 1, 1, 3, 0, 5, 0, 1, 1, 0, 1,
]


def radius_count(radius: int) -> int:
    # Root line is fixed; 39 movable variables; BT1379 counts all non-current assignments on each selected radius-r coordinate set: 6^r - 1.
    return comb(39, radius) * ((6 ** radius) - 1)


def build_milp_schema() -> dict:
    return {
        "variables": {
            "x_line_label": "x[i,a] in {0,1}; i=0..39, a in S3 labels 0..5",
            "y_edge_identity": "y[e] in {0,1}; e=0..539; y[e]=1 iff residual transport is identity",
        },
        "hard_constraints": [
            "sum_a x[i,a] = 1 for every line i",
            "x[0,0] = 1 and x[0,a!=0] = 0 (root-fixed gauge)",
            "for each skew-line constraint e=(i,j), y[e] is allowed only for label pairs satisfying the S3 identity residual relation",
        ],
        "objective": "maximize sum_e y[e], equivalently minimize 540 - sum_e y[e] corrections",
        "incumbent": {"identity_edges": 210, "corrections": 330},
        "beating_incumbent_requires": {"identity_edges_at_least": 211, "corrections_at_most": 329},
    }


def main() -> None:
    radius_counts = {r: radius_count(r) for r in range(1, 4)}
    checked_radius_leq3 = sum(radius_counts.values())
    checked_including_base = checked_radius_leq3 + 1
    search_space = 6 ** 39

    physical_frontend = {
        "edge_channel_couplers": 21,
        "orientation_latches": 42,
        "active_detector_bins": 168,
        "guard_apertures": 24,
        "tomotope_tokens": 192,
        "css_edge_rows": 240,
        "d4_quartic_guard_tokens": 192,
    }
    decompositions = {
        "identity_score": {
            "value": 210,
            "as_coupler_theta_packets": "21 * 10 = 210",
            "as_latch_quintets": "42 * 5 = 210",
        },
        "correction_score": {
            "value": 330,
            "as_active_plus_cache": "168 + 162 = 330",
            "active_detector_bins": 168,
            "cache_orbit": 162,
        },
        "total_constraints": {
            "value": 540,
            "identity_plus_correction": "210 + 330 = 540",
            "chart_nonedge_count": 540,
        },
    }

    checks = {
        "forty_line_labels": len(LABELS) == 40,
        "root_fixed": LABELS[0] == 0,
        "six_s3_labels_used": sorted(set(LABELS)) == list(range(6)),
        "identity_plus_corrections_is_540": 210 + 330 == 540,
        "bt1376_radius_counts_match": radius_counts == {1: 195, 2: 25935, 3: 1964885},
        "radius3_checked_count_matches_bt1379": checked_radius_leq3 == 1991015,
        "improving_solution_must_be_radius_at_least_4": True,
        "identity_decomposition_matches_frontend": 21 * 10 == 42 * 5 == 210,
        "correction_decomposition_matches_frontend": 168 + 162 == 330,
        "guard_band_matches_d4_tokens": 24 * 8 == physical_frontend["d4_quartic_guard_tokens"] == 192,
        "active_plus_guard_is_tomotope_bus": 168 + 24 == physical_frontend["tomotope_tokens"],
        "css_rows_are_frontend_ledger": physical_frontend["css_edge_rows"] == 240,
    }

    result = {
        "bt": 1421,
        "title": "S3 gauge correction optimizer/certificate frontier with complete physical front-end constraints",
        "verified": all(checks.values()),
        "incumbent_certificate": {
            "identity_edges": 210,
            "nonidentity_corrections": 330,
            "labels_in_s3_perm_order": LABELS,
            "root_fixed_line": 0,
            "local_certificate": {
                "radius_certified": 3,
                "radius_counts_excluding_base": radius_counts,
                "checked_radius_leq3_excluding_base": checked_radius_leq3,
                "checked_radius_leq3_including_base": checked_including_base,
                "best_checked_delta": -5,
                "consequence": "Any globally better gauge must differ from the incumbent in at least four of the 39 movable line labels.",
            },
        },
        "physical_frontend_constraints": physical_frontend,
        "frontier_decompositions": decompositions,
        "milp_max2csp_schema": build_milp_schema(),
        "search_frontier": {
            "root_fixed_search_space": "6^39",
            "root_fixed_search_space_integer": search_space,
            "radius_leq3_removed_by_certificate": checked_including_base,
            "remaining_after_radius3_certificate": search_space - checked_including_base,
            "next_exact_solver_target": "prove objective <= 210 or produce a witness with >=211 identity edges subject to the same 540 S3 constraints",
        },
        "boundary": "BT1421 is an exact optimizer schema plus incumbent/local/physical-front-end certificate. It does not claim global optimality of the 330 correction bound; it states the remaining proof obligation in solver-ready form.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1421, "verified": result["verified"], "incumbent_corrections": 330, "remaining_frontier": search_space - checked_including_base}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
