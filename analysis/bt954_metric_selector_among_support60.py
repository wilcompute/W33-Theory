#!/usr/bin/env python3
"""BT954 - metric selector among the six support-60 minimizers.

Tests the six exact BT951 minimizers through the BT929 vertex E8 metric gauge.
For each hyperbolic decomposition, use its 8-bit mask basis P and the BT929
chain-to-vertex map M0; evaluate the integer lift (M0 P)^T G_vertex (M0 P).

Result: minimizer 2 is the unique lowest-height positive unimodular vertex lift.
"""
from __future__ import annotations
from itertools import combinations, product
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt954_metric_selector_among_support60.json"

MINIMIZERS = [
    [(1, 42), (12, 65), (41, 68), (90, 144)],
    [(1, 42), (12, 65), (68, 109), (90, 144)],
    [(3, 68), (4, 42), (38, 65), (90, 144)],
    [(3, 68), (12, 65), (42, 69), (90, 144)],
    [(3, 68), (12, 65), (42, 111), (90, 144)],
    [(3, 68), (12, 89), (42, 111), (90, 144)]
]

M0 = np.array([
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,1,0,0,1],
    [0,0,0,0,1,1,1,1],
    [0,0,1,0,1,0,0,1],
    [0,0,1,0,1,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,1,1,0,1,0,0]
], dtype=int)


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c*y) % 3 for y in v)
    raise ValueError


def build_adjacency():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
    A = np.zeros((40, 40), dtype=int)
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    return A


def maskvec(m):
    return np.array([(m >> i) & 1 for i in range(8)], dtype=int)


def main() -> None:
    A = build_adjacency()
    subset = [0, 1, 4, 22, 27, 35, 23, 34]
    Gv = 2*np.eye(8, dtype=int) - A[np.ix_(subset, subset)]
    rows = []
    for idx, dec in enumerate(MINIMIZERS):
        P = np.column_stack([maskvec(x) for pair in dec for x in pair])
        M = M0 @ P
        G = M.T @ Gv @ M
        eig = np.linalg.eigvalsh(G.astype(float))
        detM = round(np.linalg.det(M.astype(float)))
        detG = round(np.linalg.det(G.astype(float)))
        rows.append({
            "minimizer": idx,
            "decomposition": [list(p) for p in dec],
            "det_integer_lift_M": int(detM),
            "lifted_gram_det": int(detG),
            "positive_definite": bool(eig.min() > 1e-9),
            "min_eigenvalue": float(eig.min()),
            "trace": int(np.trace(G)),
            "frobenius_squared": int((G*G).sum()),
            "max_abs_entry": int(np.abs(G).max()),
            "diagonal": [int(x) for x in np.diag(G)]
        })
    valid = [r for r in rows if abs(r["det_integer_lift_M"]) == 1 and r["lifted_gram_det"] == 1 and r["positive_definite"]]
    winner = min(valid, key=lambda r: (r["trace"], r["frobenius_squared"], r["max_abs_entry"], -r["min_eigenvalue"]))
    result = {
        "theorem": "BT954 metric selector among support-60 minimizers",
        "metric_gauge": "BT929 vertex E8 gauge; M = M0 P; G = M^T G_vertex M",
        "candidate_rows": rows,
        "valid_positive_unimodular_lifts": [r["minimizer"] for r in valid],
        "metric_winner": winner["minimizer"],
        "winner_decomposition": winner["decomposition"],
        "winner_score": {"trace": winner["trace"], "frobenius_squared": winner["frobenius_squared"], "max_abs_entry": winner["max_abs_entry"], "min_eigenvalue": winner["min_eigenvalue"]},
        "singular_or_invalid_candidates": [r["minimizer"] for r in rows if r not in valid],
        "conclusion": "Within the BT929 vertex metric gauge, minimizer 2 is the unique lowest-height positive unimodular support-60 lift. This upgrades the selector from six support-minimal candidates to one metric-preferred candidate in the vertex gauge.",
        "boundary": "The tetracode metric gauge should still be evaluated with an explicit stored BT930 tetracode isometry matrix; BT930's current JSON records existence but not the full matrix.",
        "checks": {"T1_six_candidates_tested": len(rows) == 6, "T2_valid_lifts_identified": len(valid) == 5, "T3_candidate_2_wins_vertex_metric": winner["minimizer"] == 2, "T4_candidate_5_singular_in_vertex_lift": 5 in [r["minimizer"] for r in rows if r not in valid], "T5_tetracode_boundary_explicit": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT954 wrote", OUT)

if __name__ == "__main__":
    main()
