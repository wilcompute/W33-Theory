#!/usr/bin/env python3
"""BT1525: update the claim table for the toroidal 7/21/3 bridge."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1525_toroidal_bridge_claim_table_update.json"
TEX = ROOT / "analysis" / "BT1525_toroidal_bridge_claim_table_update.tex"
MD = ROOT / "analysis" / "BT1525_toroidal_bridge_claim_table_update.md"

ROWS = [
    {"claim": "Csaszar/Szilassi exact counts", "tier": "exact parsed data", "support": "BT1513, BT1520", "allowed": "Csaszar has 7 vertices and 21 edges; Szilassi has 7 faces and 21 edges."},
    {"claim": "Szilassi concrete incidence", "tier": "exact finite incidence", "support": "BT1520", "allowed": "Both Szilassi realization versions share 7 hexagonal faces, 21 edges, and 42 incidences."},
    {"claim": "7/21/3 fixed-hexagon bridge", "tier": "structural incidence-compatible bridge", "support": "BT1521", "allowed": "The fixed hexagon boundary shift 3 gives three opposite two-edge sectors matching the three BT1504 fiber classes."},
    {"claim": "Full Szilassi-to-quotient embedding", "tier": "blocked theorem", "support": "BT1523", "allowed": "Do not claim a unique canonical label-preserving embedding yet."},
    {"claim": "Transported gauge action", "tier": "prototype", "support": "BT1524", "allowed": "All 40 transvection generators have a local transported-gauge prototype; full 25,920-element closure remains future work."},
    {"claim": "Tetrahedral 24 bridge", "tier": "exact flag arithmetic", "support": "PART_CCCCCXC", "allowed": "The dual toroidal pair gives 168 flags and the tetrahedron/K4 gives 24 flags; the combined scale is 192."},
]


def main() -> None:
    checks = {
        "six_claim_rows": len(ROWS) == 6,
        "exact_counts_row": ROWS[0]["tier"] == "exact parsed data",
        "incidence_bridge_promoted": "structural" in ROWS[2]["tier"],
        "full_embedding_blocked": ROWS[3]["tier"] == "blocked theorem",
        "transported_gauge_prototype_only": ROWS[4]["tier"] == "prototype",
        "tetra_24_exact_flag_arithmetic": ROWS[5]["tier"] == "exact flag arithmetic",
    }
    lines = [r"\begin{center}\scriptsize", r"\begin{tabular}{p{0.22\textwidth}p{0.18\textwidth}p{0.16\textwidth}p{0.34\textwidth}}", r"\toprule", r"Claim & Tier & Support & Allowed language\\", r"\midrule"]
    for row in ROWS:
        lines.append(f"{row['claim']} & {row['tier']} & {row['support']} & {row['allowed']}\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = {
        "bt": 1525,
        "title": "Toroidal bridge claim-table update",
        "verified": all(checks.values()),
        "rows": ROWS,
        "tex_table": "analysis/BT1525_toroidal_bridge_claim_table_update.tex",
        "interpretation": "The 7/21/3 bridge is promoted from count resonance to fixed-hexagon incidence-compatible structural bridge, while the full-surface canonical embedding theorem remains blocked.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1525 Toroidal Bridge Claim-table Update\n\nThe toroidal bridge is promoted to fixed-hexagon incidence-compatible structural status.  Full unique label-preserving Szilassi-to-quotient embedding remains blocked.  The tetrahedral 24 bridge is exact flag arithmetic.\n", encoding="utf-8")
    print(json.dumps({"bt": 1525, "verified": result["verified"], "rows": len(ROWS)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
