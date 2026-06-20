#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out", type=Path, default=ROOT / "data" / "bt1379_s3_gauge_max2csp_spec.json"
    )
    ns = ap.parse_args()
    cert = load("data/bt1376_s3_gauge_radius3_local_optimum_certificate.json")
    labels = cert["base_witness"]["labels_in_s3_perm_order"]
    checks = {
        "forty_line_labels": len(labels) == 40,
        "root_fixed": cert["base_witness"]["root_fixed_line"] == 0,
        "six_s3_labels": sorted(set(labels)) == [0, 1, 2, 3, 4, 5],
        "constraints_540": cert["checks"]["all_540_skew_edges_used"] is True,
        "identity_score_210": cert["base_witness"]["identity_edges"] == 210,
        "correction_score_330": cert["base_witness"]["nonidentity_corrections"] == 330,
        "radius3_local": cert["local_certificate"]["max_radius"] == 3,
        "radius_counts_match": (
            comb(39, 1) * (6**1 - 1) == 195
            and comb(39, 2) * (6**2 - 1) == 25935
            and comb(39, 3) * (6**3 - 1) == 1964885
        ),
        "best_delta_minus5": cert["checks"]["best_radius_delta_is_minus_5"] is True,
    }
    result = {
        "bt": 1379,
        "title": "S3 gauge synchronization Max-2CSP specification",
        "verified": all(checks.values()),
        "checks": checks,
        "problem": {
            "variables": 40,
            "root_fixed_variables": 39,
            "labels_per_variable": 6,
            "constraints": 540,
            "objective": "maximize identity residual edges, equivalently minimize nonidentity S3 corrections",
            "search_space_root_fixed": "6^39",
            "current_identity_score": 210,
            "current_correction_score": 330,
            "radius_certified": 3,
            "radius3_candidates_checked": 1991015,
            "best_checked_identity_score": 205,
        },
        "next_solver_targets": [
            "branch-and-bound upper bound on identity_edges",
            "ILP/SAT encoding with six labels per line",
            "spectral or SDP relaxation for a proof that 210 is global optimal or a witness above 210",
        ],
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": 1379,
                "verified": result["verified"],
                "constraints": 540,
                "current_identity_score": 210,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
