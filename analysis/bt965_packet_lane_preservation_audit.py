#!/usr/bin/env python3
"""BT965 - packet lane preservation audit.

BT964 attached selector rails to the Holonet prefix table.  BT965 checks what is
actually provable today.  The prefix code and lane assignment are concrete, but
mirror/schedule/cache operations are not yet stored as executable lane maps, so
full preservation is a pending test rather than a theorem.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt965_packet_lane_preservation_audit.json"
PREFIXES = ["0", "10", "110", "111"]
LANES = [
    {"slot":0, "prefix":"0", "role":"mirror", "rail":1},
    {"slot":1, "prefix":"10", "role":"schedule", "rail":0},
    {"slot":2, "prefix":"110", "role":"cache_A", "rail":2},
    {"slot":3, "prefix":"111", "role":"cache_B", "rail":3},
]


def prefix_free(words):
    return all(not b.startswith(a) for i,a in enumerate(words) for j,b in enumerate(words) if i != j)


def main() -> None:
    operation_maps = {}
    result = {
        "theorem": "BT965 packet lane preservation audit",
        "status": "preservation theorem blocked by missing executable operation maps",
        "prefixes": PREFIXES,
        "prefix_free": prefix_free(PREFIXES),
        "lane_table": LANES,
        "available_operation_maps": operation_maps,
        "identity_lane_preservation": True,
        "mirror_schedule_cache_preservation_status": "not provable from current repository artifacts: roles exist, but lane-action maps are not yet encoded",
        "test_harness_contract": {
            "operation_map_shape": "role -> {source_lane: target_lane or set[target_lanes]}",
            "pass_condition": "every target lane remains within the packet role's assigned allowed lane set",
            "required_roles": [lane["role"] for lane in LANES]
        },
        "reading": "BT964 is a selector-backed ABI convention. BT965 verifies prefix-freeness and records the exact missing object needed for a true preservation theorem: executable lane-action maps for mirror, schedule, cache_A, and cache_B.",
        "checks": {"T1_prefix_code_prefix_free": prefix_free(PREFIXES), "T2_four_lanes_present": len(LANES)==4, "T3_roles_present": [lane["role"] for lane in LANES]==["mirror","schedule","cache_A","cache_B"], "T4_preservation_not_overclaimed": True, "T5_test_contract_recorded": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT965 wrote", OUT)

if __name__ == "__main__":
    main()
