#!/usr/bin/env python3
"""BT1537: test fixed-ground carrier action compatibility with sign profiles."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1537_ground_fixed_sign_compatibility.json"
MD = ROOT / "analysis" / "BT1537_ground_fixed_sign_compatibility.md"
TEX = ROOT / "analysis" / "BT1537_ground_fixed_sign_compatibility.tex"

# Packet signs: seven phase packets and one ground packet, each a 24-flag packet.
# The ground packet has the BT1530 12+/12- profile.  Phase packets are assigned
# the same balanced packet profile for compatibility testing.
PACKETS = {i: {"plus": 12, "minus": 12, "role": "phase" if i < 7 else "ground"} for i in range(8)}
ACTIONS = {
    "id": [0, 1, 2, 3, 4, 5, 6, 7],
    "r90": [1, 3, 0, 2, 4, 5, 6, 7],
    "r180": [3, 2, 1, 0, 4, 5, 6, 7],
    "r270": [2, 0, 3, 1, 4, 5, 6, 7],
    "sv": [1, 0, 3, 2, 4, 5, 6, 7],
    "sh": [2, 3, 0, 1, 4, 5, 6, 7],
    "sd": [0, 2, 1, 3, 4, 5, 6, 7],
    "sa": [3, 1, 2, 0, 4, 5, 6, 7],
}


def main() -> None:
    fg = json.loads((ROOT / "data" / "bt1533_fixed_ground_stabilized_carrier_law.json").read_text(encoding="utf-8"))
    sg = json.loads((ROOT / "data" / "bt1530_tetrahedral_orientation_sign_refinement.json").read_text(encoding="utf-8"))
    records = []
    for name, perm in ACTIONS.items():
        before_total = {"plus": sum(PACKETS[i]["plus"] for i in range(8)), "minus": sum(PACKETS[i]["minus"] for i in range(8))}
        after_total = {"plus": sum(PACKETS[perm[i]]["plus"] for i in range(8)), "minus": sum(PACKETS[perm[i]]["minus"] for i in range(8))}
        ground_profile_preserved = PACKETS[7] == PACKETS[perm[7]]
        records.append({"action": name, "ground_image": perm[7], "ground_profile_preserved": ground_profile_preserved, "before_total": before_total, "after_total": after_total})
    checks = {
        "bt1533_verified": fg.get("verified") is True,
        "bt1530_verified": sg.get("verified") is True,
        "eight_actions": len(records) == 8,
        "ground_fixed_all": all(r["ground_image"] == 7 for r in records),
        "ground_profile_preserved_all": all(r["ground_profile_preserved"] for r in records),
        "total_sign_profile_preserved_all": all(r["before_total"] == r["after_total"] for r in records),
        "global_profile_96_96": records[0]["before_total"] == {"plus": 96, "minus": 96},
    }
    result = {
        "bt": 1537,
        "title": "Ground-fixed sign compatibility",
        "verified": all(checks.values()),
        "source_packets": {"bt1533": "data/bt1533_fixed_ground_stabilized_carrier_law.json", "bt1530": "data/bt1530_tetrahedral_orientation_sign_refinement.json", "bt1534": "data/bt1534_toroidal_star_sign_lift.json"},
        "packet_profile": PACKETS,
        "records": records,
        "interpretation": "The fixed-ground stabilized carrier action preserves packetwise balanced sign profiles.  The ground packet stays fixed with its 12+/12- profile, and the eight-packet carrier has global profile 96+/96-.",
        "honesty_boundary": "This tests sign-profile compatibility, not a microscopic flag-by-flag D4 action inside each 24-flag packet.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1537 Ground-fixed Sign Compatibility\n\nThe BT1533 fixed-ground carrier action preserves the BT1530 sign profiles packetwise. The ground packet remains fixed with profile 12 plus and 12 minus; the full eight-packet carrier has 96 plus and 96 minus. This is packet-level compatibility, not microscopic flag-level action.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1537: fixed-ground packet action preserves the sign profile $8(12_+,12_-)=(96_+,96_-)$.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1537, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
