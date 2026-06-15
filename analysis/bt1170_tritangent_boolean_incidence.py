#!/usr/bin/env python3
"""BT1170 -- incidence graph for the 45 tritangent/Boolean relation objects.

Classical model: cubic-surface lines are a_i, b_i, c_ij.  Tritangent planes are
  T_ij = {a_i, b_j, c_ij}, i != j       (30 objects)
  T_m  = {c_ij, c_kl, c_mn}, matching m (15 objects)
Edges mean: two planes share a line.  The graph is SRG(45,12,3,3).

Boolean model: pull this 15+15+15 layer incidence back along a fixed lexicographic
bijection between the 15 nonzero F2^4 masks and the 15 duads of a six-set.
This proves an explicit incidence isomorphism after labels are fixed; intrinsic
S6/outer-automorphism naturality is intentionally not claimed here.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter

import numpy as np

SIX = tuple(range(6))
MASKS = tuple(range(1, 16))
DUADS = tuple(itertools.combinations(SIX, 2))
MASK_TO_DUAD = dict(zip(MASKS, DUADS))
DUAD_TO_MASK = {d: m for m, d in MASK_TO_DUAD.items()}


def matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    first = items[0]
    for k in range(1, len(items)):
        second = items[k]
        rest = items[1:k] + items[k+1:]
        for tail in matchings(rest):
            yield tuple(sorted((tuple(sorted((first, second))),) + tail))

MATCHINGS = tuple(sorted(set(matchings(SIX))))


def build_tritangent_lines():
    vertices = []
    lines = []
    for i in SIX:
        for j in SIX:
            if i == j:
                continue
            d = tuple(sorted((i, j)))
            vertices.append(("L", i, j))
            lines.append({("a", i), ("b", j), ("c", d)})
    for m in MATCHINGS:
        vertices.append(("M", m))
        lines.append({("c", d) for d in m})
    return vertices, lines


def graph_from_lines(lines):
    n = len(lines)
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if lines[i] & lines[j]:
                A[i, j] = A[j, i] = 1
    return A


def srg_stats(A):
    n = A.shape[0]
    degs = A.sum(axis=1)
    adj, non = [], []
    for i in range(n):
        for j in range(i + 1, n):
            c = int(A[i] @ A[j])
            if A[i, j]:
                adj.append(c)
            else:
                non.append(c)
    evals, counts = np.unique(np.round(np.linalg.eigvalsh(A), 8), return_counts=True)
    return {
        "vertices": int(n),
        "edges": int(A.sum() // 2),
        "degree_set": sorted(map(int, set(degs))),
        "adjacent_common": dict(Counter(map(int, adj))),
        "nonadjacent_common": dict(Counter(map(int, non))),
        "spectrum": {str(float(e)): int(c) for e, c in zip(evals, counts)},
    }


def main():
    vertices, lines = build_tritangent_lines()
    A = graph_from_lines(lines)
    stats = srg_stats(A)

    # Boolean relation objects are the same three-layer model pulled back to masks.
    bool_vertices = []
    for i in SIX:
        for j in SIX:
            if i == j:
                continue
            bool_vertices.append(("oriented_mask", DUAD_TO_MASK[tuple(sorted((i, j)))], i < j))
    for m in MATCHINGS:
        bool_vertices.append(("matching_masks", tuple(DUAD_TO_MASK[d] for d in m)))

    payload = {
        "bt": 1170,
        "title": "tritangent Boolean incidence graph",
        "mask_to_duad": {str(k): list(v) for k, v in MASK_TO_DUAD.items()},
        "tritangent_stats": stats,
        "boolean_layer_vertices": len(bool_vertices),
        "incidence_isomorphism": "explicit after lexicographic mask-duad labeling",
        "naturality_caveat": "intrinsic S6 outer-automorphism naturality not claimed",
        "checks": {
            "vertices_45": stats["vertices"] == 45,
            "edges_270": stats["edges"] == 270,
            "degree_12": stats["degree_set"] == [12],
            "lambda_3": stats["adjacent_common"] == {3: 270},
            "mu_3": stats["nonadjacent_common"] == {3: 720},
            "boolean_vertices_45": len(bool_vertices) == 45,
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
