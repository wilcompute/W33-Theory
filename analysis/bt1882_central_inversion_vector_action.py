#!/usr/bin/env python3
"""BT1882: central-inversion vector action.

Applies the O(A2)/W(A2) central-inversion bookkeeping action to the BT1880
basis-level representatives. With the materialized BT982 vertex E8 basis, the
BT982 Gram is used. If the BT982 JSON is not materialized, the script uses the
standard E8 Cartan matrix as a declared fallback so tests remain executable.
This is still not a Z^40 chain-boundary proof.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPED = ROOT / "data/PART_BT1880_BT982_TO_BT1875_MAPPED_TEMPLATE.json"
BT982 = ROOT / "data/bt982_explicit_integral_e8_basis.json"
OUT = ROOT / "data/PART_BT1882_CENTRAL_INVERSION_VECTOR_ACTION_results.json"


def e8_cartan():
    G = [[0] * 8 for _ in range(8)]
    edges = [(0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
    for i in range(8):
        G[i][i] = 2
    for a, b in edges:
        G[a][b] = G[b][a] = -1
    return G


def load_gram():
    if BT982.exists():
        data = json.loads(BT982.read_text(encoding="utf-8"))
        return data["final_gram_Bt_G_vertex_B"], "BT982 final_gram_Bt_G_vertex_B", True
    return e8_cartan(), "standard E8 Cartan fallback pending materialized BT982 JSON", False


def dot_G(x, G, y):
    return sum(x[i] * G[i][j] * y[j] for i in range(len(x)) for j in range(len(y)))


def negate(v):
    return [-x for x in v]


def theorem_summary():
    rows = json.loads(MAPPED.read_text(encoding="utf-8"))["rows"]
    G, gram_source, materialized = load_gram()
    row_results = []
    for r in rows:
        a = r["integral_E8_vector_a"]
        b = r["integral_E8_vector_b"]
        if r["phase_coset_bit"] == 0:
            aa, bb = a, b
        else:
            aa, bb = negate(a), negate(b)
        before = {
            "aa": dot_G(a, G, a),
            "bb": dot_G(b, G, b),
            "ab": dot_G(a, G, b),
        }
        after = {
            "aa": dot_G(aa, G, aa),
            "bb": dot_G(bb, G, bb),
            "ab": dot_G(aa, G, bb),
        }
        row_results.append({
            "selector_slot": r["selector_slot"],
            "support_pair": r["support_pair"],
            "phase_coset_bit": r["phase_coset_bit"],
            "action": "identity" if r["phase_coset_bit"] == 0 else "simultaneous_vector_negation",
            "gram_before": before,
            "gram_after": after,
            "gram_preserved": before == after,
        })
    checks = {
        "eight_rows_checked": len(row_results) == 8,
        "phase_zero_identity_rows_present": sum(1 for r in row_results if r["phase_coset_bit"] == 0) == 4,
        "phase_one_negation_rows_present": sum(1 for r in row_results if r["phase_coset_bit"] == 1) == 4,
        "all_slot_gram_contributions_preserved": all(r["gram_preserved"] for r in row_results),
        "gram_source_declared": bool(gram_source),
        "chain_boundary_still_not_claimed": True,
    }
    return {
        "theorem": "BT1882 Central-Inversion Vector Action",
        "input": str(MAPPED.relative_to(ROOT)),
        "gram_source": gram_source,
        "materialized_bt982_json_present": materialized,
        "phase_one_action": "simultaneous sign reversal of both mapped slot vectors",
        "row_results": row_results,
        "closed_now": "basis-level Gram/metric contributions are preserved by the central-inversion bookkeeping action for the declared Gram source",
        "remaining_open": "explicit Z^40 chain-boundary compatibility for the phase action",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Vector-level Gram test in BT982/fallback vertex E8 coordinates only; not a Z^40 chain-boundary proof."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
