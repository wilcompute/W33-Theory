#!/usr/bin/env python3
"""Solve a weighted assignment of pattern classes to E6 Dynkin nodes.

We use adjacency counts between pattern classes and compare to the E6 Dynkin
adjacency (unweighted). Score = sum_{edges} A[i][j] - sum_{non-edges} A[i][j].
Higher is better. We search all permutations of classes 0..5.

Outputs artifacts/multiplet_assignment_solver.json
"""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# E6 Dynkin adjacency for nodes 0..5
E6_adj = {
    0: {2},
    1: {2},
    2: {0, 1, 3},
    3: {2, 4},
    4: {3, 5},
    5: {4},
}


def score_mapping(A, e6_classes, perm):
    # perm maps class idx -> node label
    score = 0
    for i, ci in enumerate(e6_classes):
        for j, cj in enumerate(e6_classes):
            if i >= j:
                continue
            node_i = perm[i]
            node_j = perm[j]
            expected = 1 if node_j in E6_adj[node_i] else 0
            w = A[ci][cj]
            score += w if expected else -w
    return score


def main():
    q = json.loads((ROOT / "artifacts" / "pattern_quotient_graph.json").read_text())
    A = q["adjacency_counts"]

    # Fix A2 block as classes 6,7
    e6_classes = [0, 1, 2, 3, 4, 5]

    best = None
    best_perm = None
    for perm in permutations(range(6)):
        s = score_mapping(A, e6_classes, perm)
        if best is None or s > best:
            best = s
            best_perm = perm

    mapping = {str(e6_classes[i]): int(best_perm[i]) for i in range(6)}
    out = {
        "a2_classes": [6, 7],
        "e6_classes": e6_classes,
        "best_score": best,
        "best_mapping": mapping,
        "note": "Weighted adjacency fit only; heuristic.",
    }

    (ROOT / "artifacts" / "multiplet_assignment_solver.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/multiplet_assignment_solver.json")
    print("best_score", best, "mapping", mapping)


if __name__ == "__main__":
    main()
