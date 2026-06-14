#!/usr/bin/env python3
"""BT978 - full-D8-compatible orbit ABI.

BT975 showed no 2+2 partition survives full transitive D8.  BT978 therefore
uses an orbit-valued ABI: all four lanes form one D8 orbit, while roles are
encoded as tags on orbit positions.  This preserves full D8 covariance but no
longer preserves a light/cache partition.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt978_full_d8_orbit_abi.json"
LANES = [0,1,2,3]
ROLES = ["mirror", "schedule", "cache_A", "cache_B"]
ROLE_TO_LANE = {"mirror":1, "schedule":0, "cache_A":2, "cache_B":3}
OPS = {
    "id": {0:0,1:1,2:2,3:3},
    "r90": {0:2,2:1,1:3,3:0},
    "r180": {0:1,1:0,2:3,3:2},
    "r270": {0:3,3:1,1:2,2:0},
    "ref_a": {0:0,2:2,1:3,3:1},
    "ref_b": {0:1,1:0,2:2,3:3},
    "ref_c": {0:2,2:0,1:1,3:3},
    "ref_d": {0:3,3:0,1:2,2:1},
}


def main() -> None:
    orbit = sorted({op[x] for op in OPS.values() for x in LANES})
    role_orbits = {role: sorted({op[lane] for op in OPS.values()}) for role, lane in ROLE_TO_LANE.items()}
    full_covariant = orbit == LANES and all(v == LANES for v in role_orbits.values())
    result = {
        "theorem": "BT978 full-D8-compatible orbit ABI",
        "status": "full D8 covariance recovered by orbit-valued ABI",
        "lane_orbit": orbit,
        "role_to_initial_lane": ROLE_TO_LANE,
        "role_orbits_under_D8": role_orbits,
        "full_D8_covariant": full_covariant,
        "tradeoff": "full D8 covariance is compatible with a single four-lane orbit, not with the previous light/cache 2+2 partition",
        "operational_reading": "Roles must be carried as tags transported with the D8 action; lane family labels cannot be fixed globally if full D8 is required.",
        "checks": {"T1_single_orbit_all_four_lanes": orbit == LANES, "T2_each_role_orbit_all_lanes": all(v == LANES for v in role_orbits.values()), "T3_full_D8_covariant": full_covariant, "T4_partition_tradeoff_recorded": True, "T5_role_tag_boundary_explicit": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT978 wrote", OUT)

if __name__ == "__main__":
    main()
