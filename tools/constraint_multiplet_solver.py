#!/usr/bin/env python3
"""Constraint-based solver for mapping pattern classes to E6 nodes.

We fix A2 classes = {6,7}. For E6, we map classes 0..5 to E6 nodes 0..5.
We minimize a weighted least-squares cost that compares observed class adjacency
counts with an ideal E6 adjacency (binary) scaled by alpha.

Outputs artifacts/constraint_multiplet_solver.json
"""

from __future__ import annotations

import json
import math
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# E6 adjacency (undirected) nodes 0..5
E6_edges = set()
for a, b in [(0, 2), (1, 2), (2, 3), (3, 4), (4, 5)]:
    E6_edges.add((a, b))
    E6_edges.add((b, a))


def main():
    q = json.loads((ROOT / "artifacts" / "pattern_quotient_graph.json").read_text())
    A = q["adjacency_counts"]

    e6_classes = [0, 1, 2, 3, 4, 5]
    # Observed adjacency counts for classes 0..5
    obs = [[A[i][j] for j in e6_classes] for i in e6_classes]

    results = []

    for perm in permutations(range(6)):
        # perm maps class index -> node
        # Compute alpha = mean observed edge weight on mapped E6 edges
        edge_vals = []
        for i, ci in enumerate(e6_classes):
            for j, cj in enumerate(e6_classes):
                if i == j:
                    continue
                node_i = perm[i]
                node_j = perm[j]
                if (node_i, node_j) in E6_edges:
                    edge_vals.append(obs[i][j])
        alpha = sum(edge_vals) / len(edge_vals) if edge_vals else 0.0

        # Cost: sum over all pairs
        cost = 0.0
        for i, ci in enumerate(e6_classes):
            for j, cj in enumerate(e6_classes):
                if i == j:
                    continue
                node_i = perm[i]
                node_j = perm[j]
                expected = alpha if (node_i, node_j) in E6_edges else 0.0
                diff = obs[i][j] - expected
                cost += diff * diff

        results.append(
            {
                "perm": perm,
                "alpha": alpha,
                "cost": cost,
            }
        )

    results.sort(key=lambda x: x["cost"])

    top = results[:10]
    best = top[0]
    mapping = {str(e6_classes[i]): int(best["perm"][i]) for i in range(6)}

    out = {
        "a2_classes": [6, 7],
        "e6_classes": e6_classes,
        "best_cost": best["cost"],
        "best_alpha": best["alpha"],
        "best_mapping": mapping,
        "top10": [
            {
                "cost": r["cost"],
                "alpha": r["alpha"],
                "mapping": {str(e6_classes[i]): int(r["perm"][i]) for i in range(6)},
            }
            for r in top
        ],
        "note": "Least-squares fit of class adjacency counts to E6 edges. Heuristic.",
    }

    (ROOT / "artifacts" / "constraint_multiplet_solver.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/constraint_multiplet_solver.json")
    print("best_cost", best["cost"], "alpha", best["alpha"], "mapping", mapping)


if __name__ == "__main__":
    main()
