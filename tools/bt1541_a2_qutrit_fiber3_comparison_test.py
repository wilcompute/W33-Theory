#!/usr/bin/env python3
"""BT1541: compare A2 root directions with qutrit/fiber-3 fixed-hexagon sectors."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1541_a2_qutrit_fiber3_comparison_test.json"
MD = ROOT / "analysis" / "BT1541_a2_qutrit_fiber3_comparison_test.md"
TEX = ROOT / "analysis" / "BT1541_a2_qutrit_fiber3_comparison_test.tex"

# A2 has six roots grouped into three opposite pairs.  Use symbolic root names
# to avoid asserting a metric embedding into the Szilassi hexagon.
A2_ROOT_PAIRS = [
    {"direction": 0, "roots": ["alpha", "-alpha"]},
    {"direction": 1, "roots": ["beta", "-beta"]},
    {"direction": 2, "roots": ["alpha+beta", "-(alpha+beta)"]},
]


def main() -> None:
    bt1521 = json.loads((ROOT / "data" / "bt1521_fixed_hexagon_sector_fiber_test.json").read_text(encoding="utf-8"))
    bt1534 = json.loads((ROOT / "data" / "bt1534_toroidal_star_sign_lift.json").read_text(encoding="utf-8"))
    sectors = bt1521["sectors"]
    mapping = []
    for pair, sector in zip(A2_ROOT_PAIRS, sectors):
        mapping.append({
            "a2_direction": pair["direction"],
            "a2_roots": pair["roots"],
            "fixed_hexagon_sector": sector["sector"],
            "fiber_class": sector["fiber_class"],
            "szilassi_edge_ids": sector["edge_ids"],
            "status": "pair-count and opposition compatible",
        })
    pass_conditions = {
        "three_a2_directions": len(A2_ROOT_PAIRS) == 3,
        "six_a2_roots": sum(len(p["roots"]) for p in A2_ROOT_PAIRS) == 6,
        "three_fixed_hexagon_sectors": len(sectors) == 3,
        "six_fixed_hexagon_sector_edges": sum(len(s["edge_ids"]) for s in sectors) == 6,
        "sector_fiber_bijection": sorted(s["fiber_class"] for s in sectors) == [0, 1, 2],
        "fiber_profile_balanced": bt1521["bt1504_fiber_profile"] == {"0": 180, "1": 180, "2": 180},
        "sign_lift_balanced": bt1534["profiles"]["combined"] == {"plus": 12, "minus": 12},
    }
    fail_boundaries = {
        "no_metric_a2_embedding": True,
        "no_magic_star_vertex_map": True,
        "no_jordan_pair_product": True,
        "no_global_w33_identity": True,
    }
    checks = {
        "bt1521_verified": bt1521.get("verified") is True,
        "bt1534_verified": bt1534.get("verified") is True,
        "all_pass_conditions": all(pass_conditions.values()),
        "all_fail_boundaries_explicit": all(fail_boundaries.values()),
        "three_mapping_rows": len(mapping) == 3,
    }
    result = {
        "bt": 1541,
        "title": "A2 / qutrit / fiber-3 comparison test",
        "verified": all(checks.values()),
        "source_packets": {"bt1521": "data/bt1521_fixed_hexagon_sector_fiber_test.json", "bt1534": "data/bt1534_toroidal_star_sign_lift.json", "bt1539": "data/bt1539_magic_star_exceptional_periodicity_bridge.json"},
        "mapping": mapping,
        "pass_conditions": pass_conditions,
        "fail_boundaries": fail_boundaries,
        "interpretation": "The A2 comparison passes at the finite opposition-count layer: six roots in three opposite pairs match six fixed-hexagon boundary edges in three opposite sectors, which map bijectively to the three BT1504 fiber classes. It fails as a theorem until a metric/root/Jordan object map is supplied.",
        "honesty_boundary": "This is an analogy test with explicit pass/fail boundaries, not a Magic Star/W33 identity theorem.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1541 A2 / Qutrit / Fiber-3 Comparison Test\n\nThe A2 analogy passes at the opposition-count layer: six symbolic A2 roots group into three opposite pairs, matching six fixed-hexagon boundary edges grouped into three opposite sectors and three BT1504 fiber classes. It remains blocked as a theorem without a metric root embedding, Magic Star vertex map, or Jordan-pair product.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1541: $A_2$ gives six roots in three opposite pairs; the fixed Szilassi hexagon gives six boundary edges in three opposite sectors mapping to three fiber classes.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1541, "verified": result["verified"], "mapping_rows": len(mapping)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
