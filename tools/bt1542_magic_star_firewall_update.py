#!/usr/bin/env python3
"""BT1542: add Magic Star as an external-comparison tier in the release firewall."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1542_magic_star_firewall_update.json"
MD = ROOT / "analysis" / "BT1542_magic_star_firewall_update.md"
TEX = ROOT / "analysis" / "BT1542_magic_star_firewall_update.tex"

EXTERNAL_ROWS = [
    {"tier": "external_comparison", "claim": "Magic Star A2 projection compared to fixed-hexagon 3-sector structure", "support": "BT1539/BT1541"},
    {"tier": "external_comparison", "claim": "Jordan-pair language compared to paired toroidal pointed stars plus K4 carrier", "support": "BT1539/BT1540"},
    {"tier": "external_comparison", "claim": "Exceptional Periodicity extended roots compared to packet carriers beyond W33 counts", "support": "BT1539/BT1540"},
]
BLOCKED_ROWS = [
    {"tier": "blocked", "claim": "Magic Star equals W33", "support": "BT1540"},
    {"tier": "blocked", "claim": "A2 sector analogy proves a root embedding", "support": "BT1541"},
    {"tier": "blocked", "claim": "Jordan-pair product exists on the toroidal star packet", "support": "BT1541"},
]


def main() -> None:
    ledger = json.loads((ROOT / "data" / "bt1538_release_claim_ledger.json").read_text(encoding="utf-8"))
    rows = ledger["rows"] + EXTERNAL_ROWS + BLOCKED_ROWS
    tier_counts = {tier: sum(1 for r in rows if r["tier"] == tier) for tier in sorted({r["tier"] for r in rows})}
    checks = {
        "bt1538_verified": ledger.get("verified") is True,
        "adds_three_external_rows": len(EXTERNAL_ROWS) == 3,
        "adds_three_blocked_rows": len(BLOCKED_ROWS) == 3,
        "has_external_comparison_tier": tier_counts.get("external_comparison", 0) == 3,
        "blocked_increases_to_seven": tier_counts.get("blocked", 0) == 7,
        "exact_count_unchanged_four": tier_counts.get("exact", 0) == 4,
        "no_magic_star_exact_claim": all(not (r["tier"] == "exact" and "Magic Star" in r["claim"]) for r in rows),
    }
    result = {
        "bt": 1542,
        "title": "Magic Star firewall update",
        "verified": all(checks.values()),
        "source": "data/bt1538_release_claim_ledger.json",
        "tier_counts": tier_counts,
        "external_rows": EXTERNAL_ROWS,
        "blocked_rows": BLOCKED_ROWS,
        "interpretation": "Magic Star / Exceptional Periodicity is included in the release firewall as an external-comparison tier only. Exact theorem tiers remain unchanged.",
        "honesty_boundary": "No Magic Star row is promoted to exact or structural theorem status without an objectwise map and algebraic product/closure tests.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1542 Magic Star Firewall Update\n\nMagic Star / Exceptional Periodicity is added to the release firewall as an external-comparison tier. Three external rows and three blocked rows are added. Exact theorem count remains unchanged.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1542: Magic Star / Exceptional Periodicity enters the release firewall as external comparison only; exact theorem tiers are unchanged.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1542, "verified": result["verified"], "tier_counts": tier_counts}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
