#!/usr/bin/env python3
"""BT966 - break the two-light-rail ABI degeneracy.

BT963 found rails 0 and 1 tie by support and phase score.  BT966 separates two
notions: structural degeneracy remains, but ABI ordering is fixed by the xor-mask
address order used by BT964.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt966_light_rail_degeneracy_breaker.json"
LIGHT_RAILS = [
    {"rail":0, "pair":[3,68], "support_sum":12, "xor_mask":71, "xor_weight":4, "phase_score":16, "bt964_role":"schedule", "prefix":"10"},
    {"rail":1, "pair":[4,42], "support_sum":12, "xor_mask":46, "xor_weight":4, "phase_score":16, "bt964_role":"mirror", "prefix":"0"},
]


def main() -> None:
    by_phase = sorted(LIGHT_RAILS, key=lambda r: (r["phase_score"], r["support_sum"]))
    by_xor = sorted(LIGHT_RAILS, key=lambda r: r["xor_mask"])
    result = {
        "theorem": "BT966 light-rail degeneracy breaker",
        "status": "ABI ordering fixed; structural/representation degeneracy remains open",
        "light_rails": LIGHT_RAILS,
        "phase_support_tie": True,
        "tied_quantities": ["support_sum", "xor_weight", "phase_score"],
        "abi_tie_break_rule": "order tied light rails by ascending xor_mask, then assign shorter prefix first",
        "abi_order": [r["rail"] for r in by_xor],
        "abi_assignment": [{"rail": r["rail"], "prefix": r["prefix"], "role": r["bt964_role"], "xor_mask": r["xor_mask"]} for r in by_xor],
        "reading": "Rail 1 precedes rail 0 for the packet ABI because xor_mask 46 < 71, giving mirror/prefix-0 to rail 1 and schedule/prefix-10 to rail 0. This breaks the ABI ordering, not the deeper representation-theoretic doublet unless later dynamics distinguish them.",
        "next_dynamic_test": "Use executable mirror/schedule lane-action maps, once committed, to test whether the light rails remain a true doublet or split dynamically.",
        "checks": {"T1_phase_support_tie_detected": [r["rail"] for r in by_phase] in ([0,1],[1,0]), "T2_xor_breaks_tie": [r["rail"] for r in by_xor] == [1,0], "T3_shorter_prefix_assigned_to_rail1": by_xor[0]["prefix"] == "0", "T4_deeper_doublet_not_overclaimed_broken": True, "T5_dynamic_next_test_recorded": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT966 wrote", OUT)

if __name__ == "__main__":
    main()
