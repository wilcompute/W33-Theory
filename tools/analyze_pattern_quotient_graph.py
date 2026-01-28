#!/usr/bin/env python3
"""Compute adjacency counts between W33 vertex pattern classes.

Pattern classes are defined by WE6-Coxeter intersection rows.
Uses:
- artifacts/we6_coxeter6_intersection.json (patterns for 40 orbits)
- artifacts/e8_orbit_to_f3_point.json (orbit -> F3^4 projective point)
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def omega(p, q):
    return (p[0] * q[2] - p[2] * q[0] + p[1] * q[3] - p[3] * q[1]) % 3


def build_adjacency(points):
    n = len(points)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
    return adj


def main():
    inter = json.loads(
        (ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text()
    )
    orbit_map = json.loads(
        (ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text()
    )
    mapping = orbit_map["mapping"]

    matrix = inter["matrix"]  # 40 rows
    patterns = [tuple(row) for row in matrix]

    # Build points list in orbit order 0..39
    points = [tuple(mapping[str(i)]) for i in range(40)]
    adj = build_adjacency(points)

    # Class id for each orbit
    pat_ids = {}
    pat_list = []
    for p in patterns:
        if p not in pat_ids:
            pat_ids[p] = len(pat_ids)
            pat_list.append(p)

    vertex_class = [pat_ids[p] for p in patterns]

    # Count edges between classes
    counts = defaultdict(int)
    class_sizes = defaultdict(int)
    for v in range(40):
        class_sizes[vertex_class[v]] += 1
    for i in range(40):
        for j in range(i + 1, 40):
            if adj[i][j]:
                a = vertex_class[i]
                b = vertex_class[j]
                counts[(a, b)] += 1

    # Build matrix
    k = len(pat_list)
    mat = [[0] * k for _ in range(k)]
    for (a, b), c in counts.items():
        mat[a][b] += c
        if a != b:
            mat[b][a] += c

    out = {
        "num_classes": k,
        "class_sizes": dict(class_sizes),
        "patterns": {str(i): pat_list[i] for i in range(k)},
        "adjacency_counts": mat,
    }

    (ROOT / "artifacts" / "pattern_quotient_graph.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    print(f"Classes: {k}")
    print("Class sizes:")
    for i in range(k):
        print(f"  {i}: size {class_sizes[i]} pattern={pat_list[i]}")
    print("Adjacency matrix written to artifacts/pattern_quotient_graph.json")


if __name__ == "__main__":
    main()
