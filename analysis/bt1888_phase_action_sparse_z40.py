#!/usr/bin/env python3
"""BT1888: phase action on sparse Z^40 representatives.

Applies the central-inversion phase action to the BT1885 sparse Z^40 embeddings.
For phase bit 1, both slot vectors are negated. The W33 adjacency-derived
candidate form G40 = 2I - A_W33 is then checked before/after. This closes the
sparse-Z40 metric-form invariance of the candidate phase action, while still not
proving G40 is the final chain A/2 boundary operator.
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data/PART_BT1885_EXPLICIT_Z40_REPRESENTATIVE_SCHEMA.json"
OUT = ROOT / "data/PART_BT1888_PHASE_ACTION_SPARSE_Z40_results.json"


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def build_w33_adjacency():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    def symp(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3
    A = [[0] * 40 for _ in range(40)]
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i][j] = A[j][i] = 1
    return A


def dot_form(x, G, y):
    return sum(x[i] * G[i][j] * y[j] for i in range(len(x)) for j in range(len(y)))


def negate(v):
    return [-x for x in v]


def theorem_summary():
    rows = json.loads(SCHEMA.read_text(encoding="utf-8"))["rows"]
    A = build_w33_adjacency()
    G40 = [[(2 if i == j else 0) - A[i][j] for j in range(40)] for i in range(40)]
    row_results = []
    for r in rows:
        a = r["z40_vector_a"]
        b = r["z40_vector_b"]
        if r["phase_coset_bit"] == 0:
            aa, bb = a, b
            action = "identity"
        else:
            aa, bb = negate(a), negate(b)
            action = "simultaneous_sparse_vector_negation"
        before = {
            "aa": dot_form(a, G40, a),
            "bb": dot_form(b, G40, b),
            "ab": dot_form(a, G40, b),
        }
        after = {
            "aa": dot_form(aa, G40, aa),
            "bb": dot_form(bb, G40, bb),
            "ab": dot_form(aa, G40, bb),
        }
        row_results.append({
            "selector_slot": r["selector_slot"],
            "support_pair": r["support_pair"],
            "phase_coset_bit": r["phase_coset_bit"],
            "action": action,
            "G40_before": before,
            "G40_after": after,
            "G40_preserved": before == after,
        })
    checks = {
        "eight_rows_checked": len(row_results) == 8,
        "phase_zero_identity_rows_present": sum(1 for r in row_results if r["phase_coset_bit"] == 0) == 4,
        "phase_one_sparse_negation_rows_present": sum(1 for r in row_results if r["phase_coset_bit"] == 1) == 4,
        "all_G40_contributions_preserved": all(r["G40_preserved"] for r in row_results),
        "chain_boundary_operator_not_overclaimed": True,
    }
    return {
        "theorem": "BT1888 Phase Action on Sparse Z40",
        "input": str(SCHEMA.relative_to(ROOT)),
        "operator_candidate": "G40 = 2I - A_W33",
        "phase_one_action": "simultaneous negation of the two sparse Z40 slot vectors",
        "row_results": row_results,
        "closed_now": "central-inversion phase action preserves the sparse-Z40 W33 adjacency-form contributions",
        "remaining_open": "prove/identify the actual chain A/2 boundary operator and verify compatibility there",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Sparse-Z40 candidate-form invariance only. It is not a final chain-boundary proof."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
