#!/usr/bin/env python3
"""BT1539: Magic Star / Exceptional Periodicity bridge ledger.

This is a literature bridge, not a theorem about W33.  It records why the Magic
Star material is relevant to the toroidal/tetra/tomotope packet: A2 projection,
Jordan pairs, finite non-Lie levels beyond E8, and a disciplined claim boundary.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1539_magic_star_exceptional_periodicity_bridge.json"
MD = ROOT / "analysis" / "BT1539_magic_star_exceptional_periodicity_bridge.md"
TEX = ROOT / "analysis" / "BT1539_magic_star_exceptional_periodicity_bridge.tex"

ROWS = [
    {"anchor": "Magic Star projection", "literature": "special star-like projection of E8 under A2", "w33_bridge": "compare to the 7+1 packet/star split, not as identity"},
    {"anchor": "Jordan pairs", "literature": "triple of Jordan pairs at the core of E8", "w33_bridge": "compare to paired Csaszar/Szilassi pointed 12-stars plus K4 carrier"},
    {"anchor": "Exceptional Periodicity", "literature": "finite-dimensional non-Lie levels beyond E8", "w33_bridge": "claim boundary: useful beyond-E8 analogy, not a W33 proof"},
    {"anchor": "Extended roots", "literature": "EP uses extended root systems rather than ordinary root lattices", "w33_bridge": "compare to toroidal/tomotope packet carriers as extended incidence carriers"},
    {"anchor": "A2/3-grading clue", "literature": "Magic Star emphasizes A2 projection and 3/5 gradings", "w33_bridge": "compare to qutrit, fiber-3, and fixed-hexagon 3-sector bridges"},
]


def main() -> None:
    checks = {
        "five_bridge_rows": len(ROWS) == 5,
        "has_a2_anchor": any("A2" in r["literature"] or "A2" in r["anchor"] for r in ROWS),
        "has_jordan_pairs": any("Jordan" in r["anchor"] for r in ROWS),
        "has_beyond_e8_boundary": any("beyond" in r["literature"] for r in ROWS),
        "no_identity_claim": all("not" in r["w33_bridge"] or "compare" in r["w33_bridge"] or "boundary" in r["w33_bridge"] for r in ROWS),
    }
    result = {
        "bt": 1539,
        "title": "Magic Star / Exceptional Periodicity bridge",
        "verified": all(checks.values()),
        "external_sources": ["arXiv:1711.07881", "arXiv:1811.11202", "arXiv:1909.00357", "arXiv:1910.07914"],
        "repo_source": "archive/data/The Magic Star of Exceptional Periodicity 2017.txt",
        "rows": ROWS,
        "interpretation": "Magic Star / Exceptional Periodicity is relevant as an A2-star, Jordan-pair, extended-root, finite non-Lie beyond-E8 comparison layer for the toroidal/tetra/tomotope packet. It is not asserted to be identical to W33 or to prove the packet.",
        "honesty_boundary": "Literature bridge only. No theorem is claimed without an objectwise map between Magic Star vertices/pairs/extended roots and W33/toroidal packet objects.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1539 Magic Star / Exceptional Periodicity Bridge\n\nMagic Star / Exceptional Periodicity is relevant as a comparison layer: A2-star projection, Jordan pairs, extended roots, and finite non-Lie levels beyond E8.  The bridge is not an identity claim.  Next objectwise target: map Magic Star vertices/pairs to W33/toroidal/tomotope packet objects or block the comparison.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1539: Magic Star / Exceptional Periodicity is recorded as an A2-star/Jordan-pair/extended-root comparison layer, not as a W33 identity theorem.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1539, "verified": result["verified"], "rows": len(ROWS)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
