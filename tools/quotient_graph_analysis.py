#!/usr/bin/env python3
"""Analyze the 8-class quotient graph for potential E6 + A2 split.

We search for a partition of 8 classes into 6+2 that minimizes
inter-group adjacency and analyze adjacency patterns.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    q = json.loads((ROOT / "artifacts" / "pattern_quotient_graph.json").read_text())
    k = q["num_classes"]
    A = q["adjacency_counts"]
    sizes = q["class_sizes"]

    # Normalize adjacency by class sizes (approx probability)
    # Compute symmetric normalized adjacency
    An = [[0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            if i == j:
                An[i][j] = A[i][j] / max(1, sizes[str(i)])
            else:
                An[i][j] = A[i][j] / max(1, sizes[str(i)])

    # Search for 6+2 partition minimizing cross edges
    best = None
    for subset in combinations(range(k), 6):
        S = set(subset)
        T = set(range(k)) - S
        cross = 0
        for i in S:
            for j in T:
                cross += A[i][j]
        if best is None or cross < best[0]:
            best = (cross, sorted(S), sorted(T))

    out = {
        "best_partition_cross_edges": best[0],
        "best_partition": {"S6": best[1], "S2": best[2]},
        "adjacency_counts": A,
        "class_sizes": sizes,
    }

    (ROOT / "artifacts" / "quotient_graph_analysis.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Best 6+2 partition:", best)
    print("Wrote artifacts/quotient_graph_analysis.json")


if __name__ == "__main__":
    main()
