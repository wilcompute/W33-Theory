#!/usr/bin/env python3
"""BT1540: guarded Magic Star object-map scaffold.

This turns BT1539 from a literature bridge into an objectwise map scaffold.  Rows
are deliberately tiered as exact, candidate, or blocked.  No Magic Star/W33
identity theorem is asserted.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1540_magic_star_object_map_scaffold.json"
MD = ROOT / "analysis" / "BT1540_magic_star_object_map_scaffold.md"
TEX = ROOT / "analysis" / "BT1540_magic_star_object_map_scaffold.tex"

ROWS = [
    {
        "magic_star_anchor": "A2 star projection",
        "candidate_w33_object": "fixed-hexagon three-sector/fiber split",
        "support": "BT1521, BT1539",
        "tier": "candidate",
        "test_needed": "objectwise A2 root-direction map to the three sector pairs",
    },
    {
        "magic_star_anchor": "six A2 root directions",
        "candidate_w33_object": "six fixed Szilassi boundary edges grouped into three opposite pairs",
        "support": "BT1521",
        "tier": "candidate",
        "test_needed": "verify sign/opposite-pair compatibility with BT1534 sign lift",
    },
    {
        "magic_star_anchor": "Jordan pair structure",
        "candidate_w33_object": "paired Csaszar/Szilassi pointed 12-star carriers plus K4 24-flag carrier",
        "support": "BT1527, BT1528, BT1534",
        "tier": "candidate",
        "test_needed": "construct an algebraic pair operation, not just a flag-pair analogy",
    },
    {
        "magic_star_anchor": "extended roots beyond E8",
        "candidate_w33_object": "toroidal/tomotope packet carriers beyond the W33 substrate counts",
        "support": "BT1529, BT1538, BT1539",
        "tier": "external_comparison",
        "test_needed": "define a root-like incidence coordinate, otherwise keep comparison only",
    },
    {
        "magic_star_anchor": "finite non-Lie EP levels",
        "candidate_w33_object": "fixed-ground stabilized carrier law and non-regular packet action",
        "support": "BT1531, BT1533, BT1537",
        "tier": "external_comparison",
        "test_needed": "compare algebra closure defects; do not call this EP without Jacobi/closure data",
    },
    {
        "magic_star_anchor": "Magic Star equals W33",
        "candidate_w33_object": "global identity theorem",
        "support": "none",
        "tier": "blocked",
        "test_needed": "blocked until vertices, roots, products, and automorphism actions are mapped objectwise",
    },
]


def main() -> None:
    src = json.loads((ROOT / "data" / "bt1539_magic_star_exceptional_periodicity_bridge.json").read_text(encoding="utf-8"))
    tier_counts = {tier: sum(1 for r in ROWS if r["tier"] == tier) for tier in sorted({r["tier"] for r in ROWS})}
    checks = {
        "bt1539_verified": src.get("verified") is True,
        "six_rows": len(ROWS) == 6,
        "has_candidate_rows": tier_counts.get("candidate", 0) == 3,
        "has_external_rows": tier_counts.get("external_comparison", 0) == 2,
        "has_blocked_row": tier_counts.get("blocked", 0) == 1,
        "no_exact_identity_claim": tier_counts.get("exact", 0) == 0,
        "all_rows_have_test_needed": all(r["test_needed"] for r in ROWS),
    }
    result = {
        "bt": 1540,
        "title": "Magic Star object map scaffold",
        "verified": all(checks.values()),
        "source": "data/bt1539_magic_star_exceptional_periodicity_bridge.json",
        "tier_counts": tier_counts,
        "rows": ROWS,
        "interpretation": "Magic Star anchors are mapped to W33/toroidal packet objects only as candidate or external-comparison rows. The global identity theorem is explicitly blocked.",
        "honesty_boundary": "This is an object-map scaffold, not a proof. It creates test targets for A2 roots, Jordan pairs, and extended-root analogies.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    lines = ["# BT1540 Magic Star Object Map Scaffold", ""]
    for r in ROWS:
        lines.append(f"- **{r['tier']}**: {r['magic_star_anchor']} -> {r['candidate_w33_object']} ({r['support']})")
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1540: Magic Star anchors are candidate/external comparison rows; no W33 identity theorem is promoted.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1540, "verified": result["verified"], "tier_counts": tier_counts}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
