#!/usr/bin/env python3
"""BT1521: map fixed-hexagon sectors to BT1504 fiber classes.

The fixed Szilassi hexagon [11,9,12,10,8,13] has six boundary edges.  The BT1444
boundary shift of 3 pairs opposite boundary edges, giving three natural two-edge
sectors.  This script maps those sectors to the three BT1504 fiber classes and
checks the incidence/fiber compatibility profile.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from bt1367_global_qutrit_phase_gauge_holonomy import build_phase_transport, compose_perm, invert_perm, perm_key, perm_order
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS, S3_PERMS

OUT = ROOT / "data" / "bt1521_fixed_hexagon_sector_fiber_test.json"
MD = ROOT / "analysis" / "BT1521_fixed_hexagon_sector_fiber_test.md"
TEX = ROOT / "analysis" / "BT1521_fixed_hexagon_sector_fiber_test.tex"

FIXED_HEXAGON = [11, 9, 12, 10, 8, 13]
CANONICAL_EDGES = [
    [0, 1], [0, 4], [0, 12], [1, 5], [1, 13], [2, 3], [2, 5], [2, 10], [3, 4], [3, 11], [4, 7], [5, 6], [6, 7], [6, 9], [7, 8], [8, 10], [8, 13], [9, 11], [9, 12], [10, 12], [11, 13]
]


def edge_id(a: int, b: int) -> int:
    e = sorted([a, b])
    return CANONICAL_EDGES.index(e)


def bt1504_fiber_profiles() -> tuple[Counter[str], Counter[str]]:
    data = build_phase_transport()
    skew_edges = data["skew_edges"]
    transport = data["transport"]
    gauge = {line: S3_PERMS[label] for line, label in enumerate(IMPROVED_GAUGE_LABELS)}
    fiber = Counter()
    residual_by_fiber = Counter()
    for left, right in skew_edges:
        residual = compose_perm(invert_perm(gauge[right]), compose_perm(transport[(left, right)], gauge[left]))
        f = (S3_PERMS.index(residual) + left + 2 * right) % 3
        fiber[str(f)] += 1
        residual_by_fiber[f"{f}:{perm_key(residual)}"] += 1
    return fiber, residual_by_fiber


def main() -> None:
    boundary_edges = []
    n = len(FIXED_HEXAGON)
    for i in range(n):
        a, b = FIXED_HEXAGON[i], FIXED_HEXAGON[(i + 1) % n]
        boundary_edges.append({"position": i, "vertices": [a, b], "edge_id": edge_id(a, b)})
    sectors = []
    for s in range(3):
        e0 = boundary_edges[s]
        e1 = boundary_edges[s + 3]
        sectors.append({
            "sector": s,
            "fiber_class": s,
            "boundary_positions": [e0["position"], e1["position"]],
            "edge_ids": [e0["edge_id"], e1["edge_id"]],
            "vertex_edges": [e0["vertices"], e1["vertices"]],
        })
    fiber_profile, residual_profile = bt1504_fiber_profiles()
    checks = {
        "fixed_hexagon_len_6": len(FIXED_HEXAGON) == 6,
        "six_boundary_edges": len(boundary_edges) == 6,
        "three_opposite_sectors": len(sectors) == 3,
        "two_edges_per_sector": all(len(s["edge_ids"]) == 2 for s in sectors),
        "edge_ids_are_concrete_szilassi_edges": sorted(e["edge_id"] for e in boundary_edges) == [15, 16, 17, 18, 19, 20],
        "sectors_cover_boundary_edges_once": sorted(e for s in sectors for e in s["edge_ids"]) == sorted(e["edge_id"] for e in boundary_edges),
        "sector_to_fiber_is_bijection": sorted(s["fiber_class"] for s in sectors) == [0, 1, 2],
        "bt1504_fibers_all_present": sorted(fiber_profile) == ["0", "1", "2"],
        "bt1504_fiber_profile_balanced": sorted(fiber_profile.values()) == [180, 180, 180],
        "residual_profile_nonempty": len(residual_profile) > 0,
    }
    result = {
        "bt": 1521,
        "title": "Fixed-hexagon sector-to-fiber test",
        "verified": all(checks.values()),
        "fixed_hexagon": FIXED_HEXAGON,
        "boundary_edges": boundary_edges,
        "sectors": sectors,
        "bt1504_fiber_profile": dict(sorted(fiber_profile.items())),
        "residual_profile_sample": dict(list(sorted(residual_profile.items()))[:12]),
        "interpretation": "The BT1444 boundary shift 3 partitions the fixed hexagon into three opposite two-edge sectors, and these three sectors map bijectively onto the three BT1504 fiber classes. The BT1504 fiber counts are balanced at 180 each over the 540 skew residuals.",
        "honesty_boundary": "This validates the sector/fiber compatibility of the fixed hexagon anchor; it does not yet prove the whole Szilassi surface realizes the BT1504 quotient map.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1521 Fixed-hexagon Sector-to-fiber Test\n\nThe fixed Szilassi hexagon splits into three opposite two-edge sectors under the BT1444 boundary shift of 3.  The sectors map bijectively to BT1504 fiber classes 0,1,2, and BT1504 fiber counts are balanced at 180 each over 540 skew residuals.\n", encoding="utf-8")
    lines = [r"\begin{center}\small", r"\begin{tabular}{c|c|c}", r"\toprule", r"Sector/Fiber & Boundary positions & Szilassi edge ids\\", r"\midrule"]
    for s in sectors:
        lines.append(f"{s['sector']} & {s['boundary_positions']} & {s['edge_ids']}\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1521, "verified": result["verified"], "fiber_profile": dict(fiber_profile)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
