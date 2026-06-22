#!/usr/bin/env python3
"""BT1533: fixed-ground stabilized D4 carrier law for the 8x24 packet assembly.

BT1531 showed the regular D4 action on eight packets does not fix the tetrahedral
ground packet.  This script formalizes the separate stabilized carrier action:
D4 acts on a square of four phase packets, leaves three residual phase packets
fixed, and fixes the tetrahedral ground packet.  The law is intentionally not
called the regular D4 action.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1533_fixed_ground_stabilized_d4_carrier_law.json"
MD = ROOT / "analysis" / "BT1533_fixed_ground_stabilized_d4_carrier_law.md"
TEX = ROOT / "analysis" / "BT1533_fixed_ground_stabilized_d4_carrier_law.tex"

D4 = [
    ("id", [0, 1, 2, 3]),
    ("r90", [1, 3, 0, 2]),
    ("r180", [3, 2, 1, 0]),
    ("r270", [2, 0, 3, 1]),
    ("sv", [1, 0, 3, 2]),
    ("sh", [2, 3, 0, 1]),
    ("sd", [0, 2, 1, 3]),
    ("sa", [3, 1, 2, 0]),
]


def compose(p, q):
    return [p[i] for i in q]


def perm_order(p):
    cur = list(range(len(p)))
    for k in range(1, 20):
        cur = compose(p, cur)
        if cur == list(range(len(p))):
            return k
    raise RuntimeError(p)


def lift_to_packets(square_perm):
    # Packet roles: 0..6 are toroidal/Fano phase packets; 7 is tetrahedral ground.
    # D4 acts only on the active square packets 0..3.  Packets 4..6 and 7 are stabilized.
    return square_perm + [4, 5, 6, 7]


def main() -> None:
    src = json.loads((ROOT / "data" / "bt1531_eight_packet_d4_action_model.json").read_text(encoding="utf-8"))
    actions = []
    for name, square in D4:
        p = lift_to_packets(square)
        phase_image = sorted(p[:7])
        actions.append({
            "name": name,
            "square_order": perm_order(square),
            "packet_perm": p,
            "phase_packets_preserved_as_set": phase_image == list(range(7)),
            "ground_packet_image": p[7],
            "ground_fixed": p[7] == 7,
            "residual_phase_packets_fixed": p[4:7] == [4, 5, 6],
        })
    checks = {
        "bt1531_verified": src.get("verified") is True,
        "eight_actions": len(actions) == 8,
        "order_profile_1_5_2": {"1": sum(1 for a in actions if a["square_order"] == 1), "2": sum(1 for a in actions if a["square_order"] == 2), "4": sum(1 for a in actions if a["square_order"] == 4)} == {"1": 1, "2": 5, "4": 2},
        "phase_set_preserved": all(a["phase_packets_preserved_as_set"] for a in actions),
        "ground_fixed_by_all": all(a["ground_fixed"] for a in actions),
        "residual_phase_fixed_by_all": all(a["residual_phase_packets_fixed"] for a in actions),
        "seven_plus_one_split_preserved": all(sorted(a["packet_perm"][:7]) == list(range(7)) and a["packet_perm"][7] == 7 for a in actions),
    }
    result = {
        "bt": 1533,
        "title": "Fixed-ground stabilized D4 carrier law",
        "verified": all(checks.values()),
        "source": "data/bt1531_eight_packet_d4_action_model.json",
        "packet_roles": {"0-6": "toroidal/Fano phase packets", "7": "tetrahedral ground packet"},
        "actions": actions,
        "interpretation": "The stabilized carrier law preserves the 7 phase + 1 ground packet decomposition.  It is a D4 action on the active square subpacket with residual phase packets and the tetrahedral ground packet fixed.",
        "honesty_boundary": "This is not the regular eight-packet D4 action; it is a stabilized carrier action selected for the fixed-ground release interpretation.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1533 Fixed-ground Stabilized D4 Carrier Law\n\nBT1533 formalizes the fixed-ground action separated in BT1531.  D4 acts on packets 0..3 as a square, fixes packets 4..6 as residual phase packets, and fixes packet 7 as the tetrahedral ground packet.  The 7+1 phase/ground split is preserved.  This is not the regular eight-packet D4 action.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1533: stabilized $D_4$ preserves $7\\cdot24+1\\cdot24$ by fixing the ground packet and acting on a four-packet square subcarrier.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1533, "verified": result["verified"], "actions": len(actions)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
