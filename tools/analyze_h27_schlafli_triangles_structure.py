#!/usr/bin/env python3
"""Analyze the 9 Schläfli triangles from H27 embedding for A2/SU(3) structure.

We test whether the 9 triangles split into 3 groups of 3 (A2^3),
compute incidence between triangles and line-types (E,C,L), and
check how triangles intersect the classical double-six structure.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_triangles():
    path = ROOT / "artifacts" / "h27_schlafli_leftover_cycles.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["cycle_labels"]


def triangle_types(tri):
    # count line types
    cnt = Counter([t[0] for t in tri])
    return tuple(sorted(cnt.items()))


def line_category(line):
    t = line[0]
    if t == "E":
        return "E"
    if t == "C":
        return "C"
    return "L"


def double_six_sets():
    # standard double six: a_i, b_i correspond to E_i and C_i
    # We'll treat E_i as a_i and C_i as b_i for indexing
    A = {("E", i) for i in range(1, 7)}
    B = {("C", i) for i in range(1, 7)}
    return A, B


def main():
    triangles = load_triangles()

    # basic stats
    type_counts = Counter()
    for tri in triangles:
        type_counts[triangle_types(tri)] += 1

    # count line usage
    line_usage = Counter()
    for tri in triangles:
        for line in tri:
            line_usage[tuple(line)] += 1

    # count usage by category
    category_usage = Counter()
    for tri in triangles:
        for line in tri:
            category_usage[line_category(line)] += 1

    # build triangle intersection graph (share a line)
    n = len(triangles)
    tri_adj = [[0] * n for _ in range(n)]
    for i in range(n):
        set_i = set(tuple(x) for x in triangles[i])
        for j in range(i + 1, n):
            set_j = set(tuple(x) for x in triangles[j])
            if set_i & set_j:
                tri_adj[i][j] = tri_adj[j][i] = 1

    tri_degrees = [sum(row) for row in tri_adj]
    tri_deg_counts = Counter(tri_degrees)

    # check partition into 3 groups of 3 with no shared lines
    # Build line-to-triangle index
    line_to_tris = defaultdict(list)
    for i, tri in enumerate(triangles):
        for line in tri:
            line_to_tris[tuple(line)].append(i)

    # triangles already disjoint in edges? check line-sharing
    disjoint_pairs = 0
    for i, j in combinations(range(n), 2):
        if not (
            set(tuple(x) for x in triangles[i]) & set(tuple(x) for x in triangles[j])
        ):
            disjoint_pairs += 1

    # double-six incidence
    A, B = double_six_sets()
    tri_double_six = []
    for tri in triangles:
        a = sum(1 for line in tri if tuple(line) in A)
        b = sum(1 for line in tri if tuple(line) in B)
        tri_double_six.append((a, b))

    results = {
        "triangle_type_counts": {str(k): v for k, v in type_counts.items()},
        "category_usage": dict(category_usage),
        "line_usage_counts": {
            "min": min(line_usage.values()),
            "max": max(line_usage.values()),
            "hist": dict(Counter(line_usage.values())),
        },
        "triangle_intersection_degree_counts": dict(tri_deg_counts),
        "disjoint_triangle_pairs": disjoint_pairs,
        "double_six_counts": tri_double_six,
        "triangles": triangles,
    }

    out_path = ROOT / "artifacts" / "h27_schlafli_triangle_structure.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
