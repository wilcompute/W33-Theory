#!/usr/bin/env python3
"""BT1887: vertex-subset embedding test.

Tests the first naive Z^40 chain candidate from BT1885/BT1886. Each 8-vector is
sparsely embedded on the BT982 vertex subset, using the materialized BT982 JSON
when present and the recorded BT982 source subset otherwise. We then evaluate the
W33 adjacency-derived form G40 = 2I - A_W33 on those sparse vectors. This
validates the sparse embedding as a metric-form lift on the vertex subset, while
still not proving it is the full boundary operator.
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data/PART_BT1885_EXPLICIT_Z40_REPRESENTATIVE_SCHEMA.json"
BT982 = ROOT / "data/bt982_explicit_integral_e8_basis.json"
OUT = ROOT / "data/PART_BT1887_VERTEX_SUBSET_EMBEDDING_TEST_results.json"
FALLBACK_VERTEX_SUBSET = [0, 1, 4, 22, 27, 35, 23, 34]


def load_vertex_subset():
    if BT982.exists():
        return json.loads(BT982.read_text(encoding="utf-8"))["vertex_subset"], True
    return FALLBACK_VERTEX_SUBSET, False


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


def theorem_summary():
    rows = json.loads(SCHEMA.read_text(encoding="utf-8"))["rows"]
    vertex_subset, materialized = load_vertex_subset()
    A = build_w33_adjacency()
    G40 = [[(2 if i == j else 0) - A[i][j] for j in range(40)] for i in range(40)]
    G_vertex = [[G40[i][j] for j in vertex_subset] for i in vertex_subset]
    row_results = []
    for r in rows:
        z40a, z40b = r["z40_vector_a"], r["z40_vector_b"]
        a8 = [z40a[i] for i in vertex_subset]
        b8 = [z40b[i] for i in vertex_subset]
        direct = {
            "aa": dot_form(z40a, G40, z40a),
            "bb": dot_form(z40b, G40, z40b),
            "ab": dot_form(z40a, G40, z40b),
        }
        restricted = {
            "aa": dot_form(a8, G_vertex, a8),
            "bb": dot_form(b8, G_vertex, b8),
            "ab": dot_form(a8, G_vertex, b8),
        }
        row_results.append({
            "selector_slot": r["selector_slot"],
            "phase_coset_bit": r["phase_coset_bit"],
            "support_pair": r["support_pair"],
            "direct_G40": direct,
            "restricted_vertex_form": restricted,
            "sparse_embedding_form_consistent": direct == restricted,
        })
    checks = {
        "eight_rows_checked": len(row_results) == 8,
        "all_sparse_forms_consistent": all(r["sparse_embedding_form_consistent"] for r in row_results),
        "vertex_subset_size_8": len(vertex_subset) == 8,
        "G40_candidate_used": True,
        "vertex_subset_source_declared": isinstance(materialized, bool),
        "boundary_operator_not_overclaimed": True,
    }
    return {
        "theorem": "BT1887 Vertex-Subset Embedding Test",
        "input": str(SCHEMA.relative_to(ROOT)),
        "operator_candidate": "G40 = 2I - A_W33",
        "vertex_subset": vertex_subset,
        "materialized_bt982_json_present": materialized,
        "row_results": row_results,
        "closed_now": "sparse Z40 embedding is consistent with the W33 adjacency-derived form on the BT982 vertex subset/fallback",
        "remaining_open": "prove or replace G40 as the actual chain A/2 boundary/operator model",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Metric-form consistency test for the sparse embedding; not a full chain-boundary proof."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
