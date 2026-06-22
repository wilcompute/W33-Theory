#!/usr/bin/env python3
"""BT1538: consolidated toroidal/tetra/tomotope release claim ledger."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1538_toroid_tetra_release_claim_ledger.json"
MD = ROOT / "analysis" / "BT1538_toroid_tetra_release_claim_ledger.md"
TEX = ROOT / "analysis" / "BT1538_toroid_tetra_release_claim_ledger.tex"

ROWS = [
    ["exact", "Csaszar all-five K7 triangular torus", "BT1526"],
    ["exact", "Szilassi seven-face twenty-one-edge incidence", "BT1520/BT1523"],
    ["exact", "K4 tetrahedral 24-flag carrier", "BT1528"],
    ["exact", "168+24=192=8*24 packet count", "BT1529"],
    ["structural", "fixed hexagon sector-to-fiber bridge", "BT1521"],
    ["structural", "balanced toroidal star sign lift", "BT1530/BT1534"],
    ["prototype", "transported gauge over transvection generators", "BT1524"],
    ["prototype", "fixed-ground stabilized carrier action", "BT1533/BT1537"],
    ["blocked", "unique label-preserving Szilassi-to-BT1504 embedding", "BT1523"],
    ["blocked", "metric equivalence with K4", "BT1526/BT1528"],
    ["blocked", "abstract tomotope isomorphism", "BT1529"],
    ["blocked", "regular eight-packet action fixes ground", "BT1531"],
]


def main() -> None:
    tier_counts = {t: sum(1 for r in ROWS if r[0] == t) for t in ["exact", "structural", "prototype", "blocked"]}
    checks = {
        "twelve_rows": len(ROWS) == 12,
        "four_exact": tier_counts["exact"] == 4,
        "two_structural": tier_counts["structural"] == 2,
        "two_prototype": tier_counts["prototype"] == 2,
        "four_blocked": tier_counts["blocked"] == 4,
        "all_tiers_known": all(r[0] in tier_counts for r in ROWS),
    }
    result = {
        "bt": 1538,
        "title": "Toroid/tetra release claim ledger",
        "verified": all(checks.values()),
        "tier_counts": tier_counts,
        "rows": [{"tier": t, "claim": c, "support": s} for t, c, s in ROWS],
        "interpretation": "BT1538 consolidates the toroidal/tetra/tomotope packet into exact, structural, prototype, and blocked-theorem tiers for release use.",
        "honesty_boundary": "The ledger is a claim-control artifact; it does not promote prototype or blocked rows to exact theorems.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    lines = ["# BT1538 Toroid/Tetra Release Claim Ledger", ""]
    for t, c, s in ROWS:
        lines.append(f"- **{t}**: {c} ({s})")
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1538: release ledger tiers are exact, structural, prototype, and blocked; blocked claims remain blocked.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1538, "verified": result["verified"], "tier_counts": tier_counts}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
