#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

GATES = ["closure51840", "diameter14", "polar_path_P4P4", "unique_all_channel_endpoint", "labelled_nonzero_spread"]
CANDIDATES = {
    "exact_polar_path": {"closure51840":1, "diameter14":1, "polar_path_P4P4":1, "unique_all_channel_endpoint":1, "labelled_nonzero_spread":1},
    "wrong_full_order_diam12": {"closure51840":1, "diameter14":0, "polar_path_P4P4":0, "unique_all_channel_endpoint":0, "labelled_nonzero_spread":1},
    "fast_full_order_diam10_A": {"closure51840":1, "diameter14":0, "polar_path_P4P4":0, "unique_all_channel_endpoint":0, "labelled_nonzero_spread":1},
    "closure_only": {"closure51840":1, "diameter14":0, "polar_path_P4P4":0, "unique_all_channel_endpoint":0, "labelled_nonzero_spread":0},
    "not_full_order": {"closure51840":0, "diameter14":0, "polar_path_P4P4":0, "unique_all_channel_endpoint":0, "labelled_nonzero_spread":0}
}


def validate(name, gates):
    missing = [g for g in GATES if not gates.get(g, 0)]
    score = len(GATES) - len(missing)
    if score == 5:
        band = "pass"
    elif gates.get("closure51840", 0) and score >= 2:
        band = "review"
    else:
        band = "fail"
    return {"name": name, "band": band, "score": score, "missing_gates": missing, "gates": gates}


def build():
    rows = [validate(k, v) for k, v in CANDIDATES.items()]
    return {
        "bt": 1266,
        "title": "Tomography candidate validator",
        "gates": GATES,
        "rules": {
            "pass": "all five gates true",
            "review": "full closure plus at least one additional gate, but not all gates",
            "fail": "missing closure or score below review threshold"
        },
        "demo_candidates": rows,
        "interpretation": "The validator makes the ladder operational: closure-only candidates fail, full-order but wrong-regime candidates are review, and only the polar path target passes."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1266_tomography_candidate_validator_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1266, "pass_count":sum(r["band"]=="pass" for r in result["demo_candidates"]), "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
