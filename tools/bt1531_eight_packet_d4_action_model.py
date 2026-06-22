#!/usr/bin/env python3
"""BT1531: D4-style action on the eight 24-flag packets of BT1529."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1531_eight_packet_d4_action_model.json"
MD = ROOT / "analysis" / "BT1531_eight_packet_d4_action_model.md"
TEX = ROOT / "analysis" / "BT1531_eight_packet_d4_action_model.tex"

D4 = [
    ("id", (0, 1, 2, 3)),
    ("r90", (1, 3, 0, 2)),
    ("r180", (3, 2, 1, 0)),
    ("r270", (2, 0, 3, 1)),
    ("sv", (1, 0, 3, 2)),
    ("sh", (2, 3, 0, 1)),
    ("sd", (0, 2, 1, 3)),
    ("sa", (3, 1, 2, 0)),
]


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[i] for i in q)


def perm_order(p: tuple[int, ...]) -> int:
    cur = tuple(range(len(p)))
    for k in range(1, 20):
        cur = compose(p, cur)
        if cur == tuple(range(len(p))):
            return k
    raise RuntimeError(p)


def main() -> None:
    src = json.loads((ROOT / "data" / "bt1529_tomotope_192_assembly_test.json").read_text(encoding="utf-8"))
    name_to_index = {p: i for i, (_name, p) in enumerate(D4)}
    regular_actions = []
    for name, g in D4:
        action = []
        for _hname, h in D4:
            action.append(name_to_index[compose(g, h)])
        regular_actions.append({"name": name, "order": perm_order(g), "packet_perm": action, "ground_image": action[7], "ground_fixed": action[7] == 7})
    ground_fixed_actions = []
    for name, g in D4:
        p = list(range(8))
        for i in range(4):
            p[i] = g[i]
        # packets 4,5,6 are residual phase packets; packet 7 is the tetra ground packet.
        p[4], p[5], p[6], p[7] = 4, 5, 6, 7
        ground_fixed_actions.append({"name": name, "order": perm_order(g), "packet_perm": p, "ground_image": p[7], "ground_fixed": True})
    checks = {
        "bt1529_verified": src.get("verified") is True,
        "d4_size_8": len(D4) == 8,
        "order_profile_1_5_2": {"1": sum(1 for _, g in D4 if perm_order(g) == 1), "2": sum(1 for _, g in D4 if perm_order(g) == 2), "4": sum(1 for _, g in D4 if perm_order(g) == 4)} == {"1": 1, "2": 5, "4": 2},
        "regular_action_permutes_ground": any(not a["ground_fixed"] for a in regular_actions),
        "regular_action_ground_orbit_all_8": sorted({a["ground_image"] for a in regular_actions}) == list(range(8)),
        "ground_fixed_model_fixes_ground": all(a["ground_fixed"] for a in ground_fixed_actions),
        "ground_fixed_model_has_valid_perms": all(sorted(a["packet_perm"]) == list(range(8)) for a in ground_fixed_actions),
    }
    result = {
        "bt": 1531,
        "title": "Eight-packet D4 action model",
        "verified": all(checks.values()),
        "source": "data/bt1529_tomotope_192_assembly_test.json",
        "regular_d4_action": regular_actions,
        "ground_fixed_d4_action": ground_fixed_actions,
        "interpretation": "The native regular D4 action on eight packets permutes the tetrahedral ground packet through all eight positions. A release/physics reading that keeps the tetrahedral ground packet fixed must use the separate ground-fixed packet action, where D4 acts on the square subpacket and leaves the ground packet external.",
        "honesty_boundary": "This distinguishes two packet actions. The regular D4 action does not preserve the ground packet; the ground-fixed action is an imposed carrier decomposition, not the regular D4 action.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1531 Eight-packet D4 Action Model\n\nThe regular D4 action on eight packets permutes the tetrahedral ground packet through all eight packet positions. Therefore a reading with a fixed tetrahedral ground packet must use a separate ground-fixed carrier action rather than the regular eight-packet D4 action.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1531: regular $D_4$ permutes the ground packet; a fixed-ground reading requires a separate stabilized carrier action.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1531, "verified": result["verified"], "regular_ground_orbit": sorted({a["ground_image"] for a in regular_actions})}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
