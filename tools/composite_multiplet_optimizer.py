#!/usr/bin/env python3
"""Composite optimizer to map pattern classes to E6 nodes.

We build a feature vector for each of the 6 E6‑candidate classes (0..5) using:
- support size distribution (1..4)
- avg neighbor class counts (8)
- K4 outer/center counts (2)
- top triangle/line multisets frequencies (global) are not class-specific here

We then compare these features against a synthetic E6 node template derived
from graph distances in the E6 Dynkin diagram (as a proxy), and search over
permutations to minimize squared error.

Outputs artifacts/composite_multiplet_optimizer.json
"""
from __future__ import annotations

import json
import itertools
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# E6 adjacency
E6_adj = {
    0: {2},
    1: {2},
    2: {0,1,3},
    3: {2,4},
    4: {3,5},
    5: {4},
}


def e6_distance_matrix():
    # BFS distances between nodes 0..5
    dist = [[0]*6 for _ in range(6)]
    for i in range(6):
        # BFS
        q = [(i,0)]
        seen = {i}
        while q:
            v,d = q.pop(0)
            dist[i][v] = d
            for w in E6_adj[v]:
                if w not in seen:
                    seen.add(w)
                    q.append((w,d+1))
    return dist


def main():
    table = json.loads((ROOT / "artifacts" / "pattern_class_feature_table.json").read_text())
    support = json.loads((ROOT / "artifacts" / "pattern_class_support_sizes.json").read_text())

    classes = [0,1,2,3,4,5]

    # Build feature vectors for classes
    X = []
    for c in classes:
        s = table["class_summary"][str(c)]
        sup = support.get(str(c), {})
        sup_vec = np.array([sup.get(str(i), sup.get(i, 0)) for i in [1,2,3,4]], dtype=float)
        if s["size"] > 0:
            sup_vec = sup_vec / s["size"]
        nbr = np.array(s["avg_neighbor_class_counts"], dtype=float) / 12.0
        k4 = np.array([s["k4_outer_count"], s["k4_center_count"]], dtype=float)
        if s["size"] > 0:
            k4 = k4 / s["size"]
        X.append(np.concatenate([sup_vec, nbr, k4]))
    X = np.vstack(X)

    # Build E6 node template features from distance profiles
    dist = e6_distance_matrix()
    # Normalize distances into a vector (node i -> distances to all nodes)
    T = []
    for i in range(6):
        vec = np.array(dist[i], dtype=float)
        vec = vec / vec.max() if vec.max() > 0 else vec
        T.append(vec)
    T = np.vstack(T)

    # Pad template to match feature length (simple replication)
    # Use first 6 dims from X to compare with distance template
    # (This is heuristic; composite scoring is purely exploratory)
    Xh = X[:, :6]

    best = None
    best_perm = None
    for perm in itertools.permutations(range(6)):
        # perm maps class index -> node
        score = 0.0
        for ci, node in enumerate(perm):
            score += np.sum((Xh[ci] - T[node])**2)
        if best is None or score < best:
            best = score
            best_perm = perm

    mapping = {str(classes[i]): int(best_perm[i]) for i in range(6)}
    out = {
        "best_score": best,
        "mapping": mapping,
        "note": "Composite heuristic using support+neighbor vs E6 distance template. Non‑canonical.",
    }

    (ROOT / "artifacts" / "composite_multiplet_optimizer.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/composite_multiplet_optimizer.json")
    print("best_score", best, "mapping", mapping)


if __name__ == "__main__":
    main()
