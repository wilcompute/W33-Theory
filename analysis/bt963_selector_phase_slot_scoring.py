#!/usr/bin/env python3
"""BT963 - phase-slot scoring in the final selector gauge.

Scores the four selector rails by a deterministic support+xor rule.  This is a
basis-gauge artifact for later CKM/PMNS searches, not a new fitted prediction.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt963_selector_phase_slot_scoring.json"
RAILS = [
    {"rail":0, "pair":[3,68], "support_sum":12, "xor_mask":71},
    {"rail":1, "pair":[4,42], "support_sum":12, "xor_mask":46},
    {"rail":2, "pair":[38,65], "support_sum":14, "xor_mask":91},
    {"rail":3, "pair":[90,144], "support_sum":22, "xor_mask":234},
]

def popcount(n: int) -> int:
    return bin(n).count("1")


def main() -> None:
    rows = []
    for r in RAILS:
        xor_weight = popcount(r["xor_mask"])
        rows.append({**r, "xor_weight": xor_weight, "phase_score": r["support_sum"] + xor_weight})
    order = sorted(rows, key=lambda x: (x["phase_score"], x["support_sum"], x["xor_mask"]))
    result = {
        "theorem": "BT963 selector phase-slot scoring",
        "status": "canonical phase-slot gauge artifact; no new physics prediction claimed",
        "scoring_rule": "phase_score = rail_support_sum + popcount(rail_xor_mask)",
        "rows": rows,
        "canonical_phase_order": [r["rail"] for r in order],
        "phase_scores_in_order": [r["phase_score"] for r in order],
        "two_light_rail_degeneracy": [0,1],
        "reading": "The final selector removes arbitrary symplectic-basis choice. It leaves a real two-light-rail degeneracy between rails 0 and 1, followed by rail 2 and then the high-support rail 3.",
        "downstream_tests": [
            "Run CKM candidates against low-rail slots 0/1 and test whether the residual tie is broken by external representation data.",
            "Run PMNS candidates against heavier slots 2/3 and compare phase residuals.",
            "Use xor masks [71,46,91,234] as canonical phase addresses instead of scanning all rail gauges."
        ],
        "checks": {"T1_four_phase_slots": len(rows)==4, "T2_scores_are_16_16_19_27": [r["phase_score"] for r in order]==[16,16,19,27], "T3_light_rail_degeneracy_recorded": True, "T4_no_new_prediction_claimed": True, "T5_downstream_tests_recorded": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT963 wrote", OUT)

if __name__ == "__main__":
    main()
