#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1393_ladder_consistency_audit.json")
    ns = ap.parse_args()
    gap = load("data/bt1352_n_quadrant_ramanujan_gap_law.json")
    q6 = load("data/bt1354_q6_confirmation_optical_audit.json")
    q7 = load("data/bt1356_q7_heptad_completion.json")
    period = load("data/bt1358_period_closure_audit.json")
    checks = {
        "bt1352_first_crossing_q6": gap["first_super_ramanujan_crossing"] == 6,
        "bt1354_q6_super_ramanujan": q6["task1_hashimoto_confirmation"]["super_ramanujan_confirmed"] is True,
        "bt1356_q7_certified": q7["status"] == "CERTIFIED" and q7["construction"]["heptad_period_closed"] is True,
        "bt1356_q7_still_no_amplification": q7["optical_budget_q7"]["requires_amplification"] is False,
        "bt1358_competitor_pool_falsified": period["final_uniqueness"]["total_falsified"] == 128,
        "bt1358_exact_matches_zero_is_competitor_pool": period["final_uniqueness"]["exact_W33_matches"] == 0,
    }
    result = {
        "bt": 1393,
        "title": "Q5-Q7 heptad ladder consistency audit",
        "verified": all(checks.values()),
        "checks": checks,
        "resolutions": {
            "q7_ceiling_vs_q7_completion": "The earlier Q7 ceiling note is a pre-ladder/W63-extension caution. BT1356 later certifies a Q7 heptad completion inside the heptad ladder, with Q8 beginning the second period.",
            "q6_vs_q7_ramanujan_crossing": "BT1352/BT1354 identify the first super-Ramanujan crossing at Q6. Q7 remains super-Ramanujan and period-closing; it is not the first crossing.",
            "exact_W33_matches_zero": "BT1358's exact_W33_matches=0 refers to the competitor/falsifier pool survivor search, not to absence of the W33 reference family. The W33 reference is handled separately in BT1354 as the physically realizable family."
        },
        "canonical_ladder": {
            "Q4": gap["gap_ladder"]["4"],
            "Q5": gap["gap_ladder"]["5"],
            "Q6": gap["gap_ladder"]["6"],
            "Q7": {"delta_direct_bt1356": q7["gap_q7_direct"], "params": {"n": q7["construction"]["n_qubits"], "k": q7["construction"]["k_logicals"], "d": q7["construction"]["d_distance"]}, "period_closed": q7["period_closure"]["heptad_period"] == 7}
        },
        "paper_patch_recommendation": "Add chronology language: BT1324 was an open/ceiling warning; BT1356 resolves the heptad-ladder Q7 case; BT1358 falsifies competitors, not the W33 reference."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1393, "verified": result["verified"], "first_crossing": gap["first_super_ramanujan_crossing"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
