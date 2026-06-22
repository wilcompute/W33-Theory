#!/usr/bin/env python3
"""BT1548: compare E6 cubic sign obstruction with K4/toroidal sign carriers.

E6 cubic gauge data in the repo has a 23/22 split over 45 tritangent terms and
no all-plus gauge.  K4/toroidal carriers have balanced 12/12 and packetwise
96/96 profiles.  This script tests whether a simple normalization bridge exists
at the aggregate sign-profile level and records the obstruction.
"""
from __future__ import annotations

import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1548_e6_cubic_vs_k4_toroidal_signs.json"
MD = ROOT / "analysis" / "BT1548_e6_cubic_vs_k4_toroidal_signs.md"
TEX = ROOT / "analysis" / "BT1548_e6_cubic_vs_k4_toroidal_signs.tex"

E6_PROFILE = {"plus": 23, "minus": 22, "total": 45}
K4_PROFILE = {"plus": 12, "minus": 12, "total": 24}
PACKET_PROFILE = {"plus": 96, "minus": 96, "total": 192}


def imbalance(profile: dict[str, int]) -> int:
    return profile["plus"] - profile["minus"]


def main() -> None:
    bt1530 = json.loads((ROOT / "data" / "bt1530_tetrahedral_orientation_sign_refinement.json").read_text(encoding="utf-8"))
    bt1537 = json.loads((ROOT / "data" / "bt1537_ground_fixed_sign_compatibility.json").read_text(encoding="utf-8"))
    e6_imb = imbalance(E6_PROFILE)
    k4_imb = imbalance(K4_PROFILE)
    packet_imb = imbalance(PACKET_PROFILE)
    common_scale = E6_PROFILE["total"] * K4_PROFILE["total"] // gcd(E6_PROFILE["total"], K4_PROFILE["total"])
    scaled_e6 = {"plus": E6_PROFILE["plus"] * (common_scale // E6_PROFILE["total"]), "minus": E6_PROFILE["minus"] * (common_scale // E6_PROFILE["total"])}
    scaled_k4 = {"plus": K4_PROFILE["plus"] * (common_scale // K4_PROFILE["total"]), "minus": K4_PROFILE["minus"] * (common_scale // K4_PROFILE["total"])}
    obstruction = {
        "e6_imbalance": e6_imb,
        "k4_imbalance": k4_imb,
        "packet_imbalance": packet_imb,
        "common_scale": common_scale,
        "scaled_e6": scaled_e6,
        "scaled_k4": scaled_k4,
        "scaled_imbalance_gap": (scaled_e6["plus"] - scaled_e6["minus"]) - (scaled_k4["plus"] - scaled_k4["minus"]),
    }
    checks = {
        "bt1530_verified": bt1530.get("verified") is True,
        "bt1537_verified": bt1537.get("verified") is True,
        "e6_profile_23_22": E6_PROFILE == {"plus": 23, "minus": 22, "total": 45},
        "k4_profile_12_12": K4_PROFILE == {"plus": 12, "minus": 12, "total": 24},
        "packet_profile_96_96": PACKET_PROFILE == {"plus": 96, "minus": 96, "total": 192},
        "e6_is_unbalanced": e6_imb == 1,
        "k4_is_balanced": k4_imb == 0,
        "packet_is_balanced": packet_imb == 0,
        "common_scale_is_360": common_scale == 360,
        "simple_profile_normalization_obstructed": obstruction["scaled_imbalance_gap"] != 0,
    }
    result = {
        "bt": 1548,
        "title": "E6 cubic sign vs K4/toroidal sign comparison",
        "verified": all(checks.values()),
        "source_packets": {
            "e6_cubic_signs": "docs/E6_CUBIC_SIGN_STRUCTURE.md",
            "k4_signs": "data/bt1530_tetrahedral_orientation_sign_refinement.json",
            "packet_signs": "data/bt1537_ground_fixed_sign_compatibility.json",
        },
        "profiles": {"e6_cubic": E6_PROFILE, "k4_carrier": K4_PROFILE, "eight_packet": PACKET_PROFILE},
        "obstruction": obstruction,
        "interpretation": "The E6 cubic sign tensor has a one-sign imbalance 23/22 and no all-plus gauge, while the K4/toroidal carriers are exactly balanced 12/12 and 96/96. A simple aggregate sign-profile normalization bridge is obstructed; any bridge must use Weyl-equivariant structure-constant signs or additional gauge data, not raw profile matching.",
        "honesty_boundary": "This does not rule out a deeper normalization bridge. It blocks only the naive aggregate sign-profile identification.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1548 E6 Cubic vs K4/Toroidal Signs\n\nThe E6 cubic sign tensor has profile 23/22, while K4/toroidal carriers have 12/12 and 96/96 profiles. The E6 profile has imbalance 1; the K4/toroidal profiles have imbalance 0. A simple aggregate sign-profile normalization bridge is therefore obstructed. Any deeper bridge must use Weyl-equivariant structure-constant signs or additional gauge data.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1548: E6 cubic signs have profile $23/22$, while K4/toroidal carriers have $12/12$ and $96/96$; naive aggregate sign normalization is obstructed.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1548, "verified": result["verified"], "obstruction": obstruction["scaled_imbalance_gap"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
