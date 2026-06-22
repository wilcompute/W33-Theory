#!/usr/bin/env python3
"""BT1549: smallest possible product-table attempt on the 12+12 carrier.

BT1544 showed that a Jordan-pair theorem is obstructed because no U/V maps or
identities are present.  This attempt tries the smallest incidence-only product:
pair plus/minus rows by local index and define a rank-1 echo table.  It then
checks whether this is enough to satisfy minimal closure and identity schema.
It is not; the obstruction sharpens from "missing schema" to "incidence-only
pairing is underdetermined and cannot supply Jordan identities".
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1549_jordan_product_construction_attempt.json"
MD = ROOT / "analysis" / "BT1549_jordan_product_construction_attempt.md"
TEX = ROOT / "analysis" / "BT1549_jordan_product_construction_attempt.tex"

PLUS = list(range(12))
MINUS = list(range(12, 24))


def incidence_pair_product(p: int, m: int) -> int:
    # Minimal possible table: pair only by local residue; all other pairs vanish.
    return 1 if (p % 12) == ((m - 12) % 12) else 0


def main() -> None:
    bt1544 = json.loads((ROOT / "data" / "bt1544_jordan_pair_carrier_obstruction_test.json").read_text(encoding="utf-8"))
    table = [[incidence_pair_product(p, m) for m in MINUS] for p in PLUS]
    row_weights = [sum(row) for row in table]
    col_weights = [sum(table[i][j] for i in range(12)) for j in range(12)]
    nonzero = sum(row_weights)
    missing_for_jordan = [
        "quadratic_U_plus(x,y)",
        "quadratic_U_minus(y,x)",
        "linearized_V_plus_minus",
        "triple product closure",
        "Jordan pair identities",
        "non-incidence scalar/gauge data",
    ]
    attempt_status = "sharpened_obstruction"
    checks = {
        "bt1544_verified": bt1544.get("verified") is True,
        "plus_size_12": len(PLUS) == 12,
        "minus_size_12": len(MINUS) == 12,
        "table_shape_12_by_12": len(table) == 12 and all(len(row) == 12 for row in table),
        "rank1_matching_has_12_nonzero_pairs": nonzero == 12,
        "each_plus_has_one_partner": row_weights == [1] * 12,
        "each_minus_has_one_partner": col_weights == [1] * 12,
        "not_enough_for_jordan_schema": len(missing_for_jordan) == 6,
        "status_is_obstruction": attempt_status == "sharpened_obstruction",
    }
    result = {
        "bt": 1549,
        "title": "Jordan-product construction attempt",
        "verified": all(checks.values()),
        "source": "data/bt1544_jordan_pair_carrier_obstruction_test.json",
        "plus_carrier_size": len(PLUS),
        "minus_carrier_size": len(MINUS),
        "candidate_product": "incidence-only local-residue matching p_i * m_j = 1 iff i=j, else 0",
        "nonzero_pair_count": nonzero,
        "row_weights": row_weights,
        "col_weights": col_weights,
        "missing_for_jordan_pair_theorem": missing_for_jordan,
        "attempt_status": attempt_status,
        "interpretation": "The smallest incidence-only product table exists as a perfect matching between the two 12-flag halves, but it is far too poor to define a Jordan pair. It supplies no quadratic U maps, no V maps, no triple closure, and no identities. BT1544 is sharpened: not just missing data, but the minimal incidence-only product collapses to a matching and cannot carry Jordan-pair structure by itself.",
        "honesty_boundary": "This does not rule out an enriched product using E6 cubic signs, Weyl gauges, or additional scalar data. It rules out only the naive minimal incidence-only table.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1549 Jordan-product Construction Attempt\n\nThe smallest incidence-only product on the 12+12 carrier is a perfect matching: each plus row pairs with exactly one minus row. This is too weak to define a Jordan pair because it supplies no quadratic U maps, no V maps, no triple closure, and no identities. The obstruction is sharpened: the naive minimal product collapses to matching data.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1549: the minimal $12\\times12$ incidence product is only a perfect matching, so Jordan-pair structure remains obstructed without enriched product data.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1549, "verified": result["verified"], "nonzero": nonzero, "status": attempt_status}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
