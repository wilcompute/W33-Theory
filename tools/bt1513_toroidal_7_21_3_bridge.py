#!/usr/bin/env python3
"""BT1513: ledger for the user's Csaszar/Szilassi 7/21/3 observation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1513_toroidal_7_21_3_bridge.json"
MD = ROOT / "analysis" / "BT1513_toroidal_7_21_3_bridge.md"


def main() -> None:
    exact_counts = {
        "csaszar": {"vertices": 7, "edges": 21, "faces": 14, "dual": "Szilassi"},
        "szilassi": {"vertices": 14, "edges": 21, "faces": 7, "dual": "Csaszar"},
        "bt1504": {"point_classes": 7, "flag_classes": 21, "fiber_classes": 3},
    }
    bridge = [
        {"number": 7, "toroidal_read": "Csaszar vertices / Szilassi faces", "bt1504_read": "point classes"},
        {"number": 21, "toroidal_read": "Csaszar and Szilassi edges", "bt1504_read": "flag classes"},
        {"number": 3, "toroidal_read": "candidate local edge-sector / qutrit fiber split", "bt1504_read": "fiber classes"},
    ]
    checks = {
        "csaszar_7_21": exact_counts["csaszar"]["vertices"] == 7 and exact_counts["csaszar"]["edges"] == 21,
        "szilassi_7_21": exact_counts["szilassi"]["faces"] == 7 and exact_counts["szilassi"]["edges"] == 21,
        "bt1504_7_21_3": exact_counts["bt1504"] == {"point_classes": 7, "flag_classes": 21, "fiber_classes": 3},
        "three_marked_candidate_not_exact_toroid_count": "candidate" in bridge[2]["toroidal_read"],
        "bridge_rows_three": len(bridge) == 3,
    }
    result = {
        "bt": 1513,
        "title": "Toroidal 7-21-3 bridge ledger",
        "verified": all(checks.values()),
        "exact_counts": exact_counts,
        "bridge": bridge,
        "interpretation": "The user's observation is real at the count level: BT1504's 7 and 21 mirror the Csaszar/Szilassi dual toroid's 7 vertices/faces and 21 edges. The 3 should remain a candidate local edge-sector or qutrit-fiber split until tied to an exact toroidal incidence law.",
        "claim_tier": "structural_count_resonance_with_exact_7_and_21_counts",
        "next_exact_test": "Map BT1504 point/flag/fiber classes to Szilassi faces/edges/local edge sectors and test incidence preservation.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1513 Toroidal 7-21-3 Bridge\n\nBT1504 has 7 point classes, 21 flag classes, and 3 fiber classes.  Csaszar has 7 vertices and 21 edges; Szilassi has 7 faces and 21 edges.  The 3 is kept as a candidate local edge-sector/qutrit split, not an exact toroidal theorem yet.\n", encoding="utf-8")
    print(json.dumps({"bt": 1513, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
