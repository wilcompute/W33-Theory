#!/usr/bin/env python3
"""Infer candidate mapping of pattern classes to an E6 Dynkin labeling.

We use the 8-class quotient graph. Based on prior analysis, classes 6 and 7 are
selected as A2 (SU(3)) candidates; classes 0..5 are mapped to E6 nodes.

We search permutations of classes 0..5 to match the E6 adjacency pattern.
Two scores are computed:
- mismatch count (unweighted)
- weighted score: sum(edges) - sum(nonedges)

Outputs artifacts/pattern_class_multiplet_inference.json
"""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# E6 Dynkin (Bourbaki) adjacency for 6 nodes labeled 0..5
# Structure: 0-2-3-4-5 and 1 attached to 2
E6_adj = {
    0: {2},
    1: {2},
    2: {0, 1, 3},
    3: {2, 4},
    4: {3, 5},
    5: {4},
}


def main():
    q = json.loads((ROOT / "artifacts" / "pattern_quotient_graph.json").read_text())
    A = q["adjacency_counts"]

    # Unweighted adjacency among classes 0..7
    adj = [[1 if A[i][j] > 0 else 0 for j in range(8)] for i in range(8)]

    # Fix A2 block
    a2_classes = [6, 7]
    e6_classes = [0, 1, 2, 3, 4, 5]

    best_mismatch = None
    best_perm_mismatch = None

    best_score = None
    best_perm_score = None

    for perm in permutations(range(6)):
        mismatches = 0
        score = 0
        for i, ci in enumerate(e6_classes):
            for j, cj in enumerate(e6_classes):
                if i == j:
                    continue
                node_i = perm[i]
                node_j = perm[j]
                expected = 1 if node_j in E6_adj[node_i] else 0
                observed = adj[ci][cj]
                if expected != observed:
                    mismatches += 1
                # weighted score using adjacency counts (symmetric)
                w = A[ci][cj]
                score += w if expected else -w
        if best_mismatch is None or mismatches < best_mismatch:
            best_mismatch = mismatches
            best_perm_mismatch = perm
        if best_score is None or score > best_score:
            best_score = score
            best_perm_score = perm

    def build_mapping(perm):
        mapping = {}
        for i, ci in enumerate(e6_classes):
            mapping[str(ci)] = {"assigned_e6_node": int(perm[i])}
        return mapping

    out = {
        "a2_classes": a2_classes,
        "e6_classes": e6_classes,
        "best_mismatch": best_mismatch,
        "best_mismatch_mapping": build_mapping(best_perm_mismatch),
        "best_weighted_score": best_score,
        "best_weighted_mapping": build_mapping(best_perm_score),
        "note": "Heuristic mapping using unweighted adjacency and weighted counts. Not canonical.",
    }

    (ROOT / "artifacts" / "pattern_class_multiplet_inference.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/pattern_class_multiplet_inference.json")
    print("best mismatches", best_mismatch, "best weighted score", best_score)


if __name__ == "__main__":
    main()
