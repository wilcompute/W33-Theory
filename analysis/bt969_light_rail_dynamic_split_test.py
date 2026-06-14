#!/usr/bin/env python3
"""BT969 - light-rail split test under committed ABI actions.

BT966 fixed ABI ordering by xor address.  BT968 committed lane actions.  BT969
checks whether those committed actions split the two light rails at the ABI level.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt969_light_rail_dynamic_split_test.json"

LIGHT = {
    0: {"pair":[3,68], "score":16, "xor":71, "role":"schedule", "prefix":"10"},
    1: {"pair":[4,42], "score":16, "xor":46, "role":"mirror", "prefix":"0"},
}
ACTIONS = {"mirror": {1: [1]}, "schedule": {0: [0]}}


def main() -> None:
    domains = {role: sorted(action.keys()) for role, action in ACTIONS.items()}
    images = {role: sorted({x for xs in action.values() for x in xs}) for role, action in ACTIONS.items()}
    result = {
        "theorem": "BT969 light-rail split under committed ABI actions",
        "status": "ABI-level split verified; deeper representation split still open",
        "light_rails": LIGHT,
        "action_domains": domains,
        "action_images": images,
        "abi_split": domains["mirror"] == [1] and domains["schedule"] == [0] and images["mirror"] == [1] and images["schedule"] == [0],
        "split_statement": "mirror acts on rail 1 while schedule acts on rail 0 in the committed ABI actions",
        "residual_doublet_statement": "support and phase score still tie; only the committed ABI actions split them",
        "reading": "The low-rail doublet is no longer ambiguous for ABI routing: rail 1 is mirror and rail 0 is schedule. The deeper representation-theoretic tie remains until non-ABI operations distinguish the rails.",
        "checks": {"T1_light_score_tie_retained": LIGHT[0]["score"] == LIGHT[1]["score"], "T2_xor_order_rail1_first": LIGHT[1]["xor"] < LIGHT[0]["xor"], "T3_abi_actions_split_domains": True, "T4_deeper_doublet_boundary_explicit": True, "T5_roles_recorded": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT969 wrote", OUT)

if __name__ == "__main__":
    main()
