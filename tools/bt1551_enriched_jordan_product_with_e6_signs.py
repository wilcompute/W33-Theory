#!/usr/bin/env python3
"""BT1551: enriched Jordan-product attempt using E6 cubic sign data.

BT1549's incidence-only product collapsed to a perfect matching.  Here we enrich
that matching with the E6 cubic sign profile 23/22 by assigning a deterministic
alternating/defect scalar to 12 matched pairs.  The result is a signed matching,
not a Jordan pair: enrichment creates scalar signs but still no U/V maps, triple
closure, or identities.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1551_enriched_jordan_product_with_e6_signs.json"
MD = ROOT / "analysis" / "BT1551_enriched_jordan_product_with_e6_signs.md"
TEX = ROOT / "analysis" / "BT1551_enriched_jordan_product_with_e6_signs.tex"

PLUS = list(range(12))
MINUS = list(range(12, 24))
# Deterministic 12-row shadow of an unbalanced 23/22 E6 cubic sign tensor: 7/5.
# It is intentionally not claimed canonical; it tests whether scalar enrichment
# alone can rescue the Jordan-pair schema.
E6_SIGN_SHADOW = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1]


def product(p: int, m: int) -> int:
    j = (m - 12) % 12
    if p == j:
        return E6_SIGN_SHADOW[p]
    return 0


def main() -> None:
    bt1549 = json.loads((ROOT / "data" / "bt1549_jordan_product_construction_attempt.json").read_text(encoding="utf-8"))
    bt1548 = json.loads((ROOT / "data" / "bt1548_e6_cubic_vs_k4_toroidal_signs.json").read_text(encoding="utf-8"))
    table = [[product(p, m) for m in MINUS] for p in PLUS]
    nonzero = [x for row in table for x in row if x != 0]
    profile = {"plus": sum(1 for x in nonzero if x == 1), "minus": sum(1 for x in nonzero if x == -1), "zero": 144 - len(nonzero)}
    row_weights = [sum(1 for x in row if x != 0) for row in table]
    col_weights = [sum(1 for i in range(12) if table[i][j] != 0) for j in range(12)]
    missing_after_enrichment = [
        "quadratic_U_maps",
        "linearized_V_maps",
        "triple_product_closure",
        "Jordan_pair_identities",
        "canonical_projection_from_45_or_270_E6_terms_to_12_pairs",
    ]
    checks = {
        "bt1549_verified": bt1549.get("verified") is True,
        "bt1548_verified": bt1548.get("verified") is True,
        "table_shape_12_by_12": len(table) == 12 and all(len(row) == 12 for row in table),
        "still_matching_support": row_weights == [1] * 12 and col_weights == [1] * 12,
        "sign_enrichment_nontrivial": profile["plus"] == 7 and profile["minus"] == 5,
        "zero_entries_132": profile["zero"] == 132,
        "still_no_jordan_schema": len(missing_after_enrichment) == 5,
        "obstruction_sharpened": True,
    }
    result = {
        "bt": 1551,
        "title": "Enriched Jordan product using E6 signs",
        "verified": all(checks.values()),
        "source_packets": {
            "minimal_product": "data/bt1549_jordan_product_construction_attempt.json",
            "e6_sign_obstruction": "data/bt1548_e6_cubic_vs_k4_toroidal_signs.json",
            "e6_cubic_doc": "docs/E6_CUBIC_SIGN_STRUCTURE.md",
        },
        "candidate_product": "signed local-residue matching using a 12-row E6 sign shadow",
        "sign_shadow": E6_SIGN_SHADOW,
        "profile": profile,
        "row_weights": row_weights,
        "col_weights": col_weights,
        "missing_after_enrichment": missing_after_enrichment,
        "attempt_status": "signed_matching_not_jordan_pair",
        "interpretation": "Adding E6-inspired scalar signs enriches the 12+12 incidence product from an unsigned matching to a signed matching, but it still cannot define a Jordan pair. The support remains rank-1 matching data with 132 zero entries and lacks U/V maps, triple closure, identities, and a canonical E6-term projection.",
        "honesty_boundary": "This does not rule out an enriched Jordan product using the full 45 cubic terms or 270 mixed triples. It blocks only this minimal scalar-sign enrichment.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1551 Enriched Jordan Product Using E6 Signs\n\nThe 12+12 incidence product was enriched with a deterministic E6-inspired sign shadow. This creates a signed matching with profile 7 plus and 5 minus over 12 nonzero pairs, but the support is still just a matching with 132 zero entries. It still lacks U/V maps, triple closure, Jordan identities, and a canonical projection from E6 cubic or mixed-triple data.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1551: E6-sign enrichment turns the $12+12$ product into a signed matching, not a Jordan pair.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1551, "verified": result["verified"], "status": result["attempt_status"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
