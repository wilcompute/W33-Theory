#!/usr/bin/env python3
"""Compute pattern-class correlations with K4, triangles, and lines in W33.

Outputs artifacts/pattern_class_physics_profile.json
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_points():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]
    points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            points.append(v)
    return points


def build_adj(points):
    n = len(points)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
    return adj


def load_lines():
    path = ROOT / "data/_workbench/02_geometry/W33_line_phase_map.csv"
    lines = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pts = tuple(map(int, str(row["point_ids"]).split()))
            lines.append(pts)
    return lines


def pattern_class_by_vertex():
    inter = json.loads(
        (ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text()
    )
    orbit_map = json.loads(
        (ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text()
    )
    mapping = orbit_map["mapping"]

    patterns = [tuple(row) for row in inter["matrix"]]
    pat_ids = {}
    for row in patterns:
        if row not in pat_ids:
            pat_ids[row] = len(pat_ids)

    orbit_class = {i: pat_ids[patterns[i]] for i in range(40)}
    point_to_orbit = {tuple(v): int(k) for k, v in mapping.items()}

    points = build_points()
    class_by_vertex = []
    for p in points:
        oid = point_to_orbit[p]
        class_by_vertex.append(orbit_class[oid])
    return class_by_vertex, pat_ids


def compute_k4_components(adj, lines):
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    noncol = defaultdict(set)
    for p in range(40):
        for q in range(40):
            if p != q and q not in col[p]:
                noncol[p].add(q)

    k4_list = []
    for a in range(40):
        for b in noncol[a]:
            if b <= a:
                continue
            for c in noncol[a] & noncol[b]:
                if c <= b:
                    continue
                for d in noncol[a] & noncol[b] & noncol[c]:
                    if d <= c:
                        continue
                    common = col[a] & col[b] & col[c] & col[d]
                    if len(common) == 4:
                        k4_list.append(((a, b, c, d), tuple(sorted(common))))
    return k4_list


def all_triangles(adj):
    tris = []
    for i in range(40):
        for j in range(i + 1, 40):
            if not adj[i][j]:
                continue
            for k in range(j + 1, 40):
                if adj[i][k] and adj[j][k]:
                    tris.append((i, j, k))
    return tris


def main():
    points = build_points()
    adj = build_adj(points)
    lines = load_lines()
    class_by_vertex, pat_ids = pattern_class_by_vertex()
    k = len(pat_ids)

    # K4 profile
    k4_list = compute_k4_components(adj, lines)
    outer_class_counts = Counter()
    center_class_counts = Counter()
    outer_multisets = Counter()
    center_multisets = Counter()

    for outer, center in k4_list:
        o_classes = tuple(sorted([class_by_vertex[v] for v in outer]))
        c_classes = tuple(sorted([class_by_vertex[v] for v in center]))
        outer_multisets[o_classes] += 1
        center_multisets[c_classes] += 1
        for v in outer:
            outer_class_counts[class_by_vertex[v]] += 1
        for v in center:
            center_class_counts[class_by_vertex[v]] += 1

    # Triangle profile
    tris = all_triangles(adj)
    tri_multisets = Counter()
    for a, b, c in tris:
        tri_multisets[
            tuple(sorted([class_by_vertex[a], class_by_vertex[b], class_by_vertex[c]]))
        ] += 1

    # Line profile
    line_multisets = Counter()
    for L in lines:
        line_multisets[tuple(sorted([class_by_vertex[v] for v in L]))] += 1

    out = {
        "class_count": k,
        "class_sizes": dict(Counter(class_by_vertex)),
        "k4_count": len(k4_list),
        "outer_class_counts": dict(outer_class_counts),
        "center_class_counts": dict(center_class_counts),
        "outer_class_multisets": {str(k): v for k, v in outer_multisets.items()},
        "center_class_multisets": {str(k): v for k, v in center_multisets.items()},
        "triangle_class_multisets": {str(k): v for k, v in tri_multisets.items()},
        "line_class_multisets": {str(k): v for k, v in line_multisets.items()},
    }

    (ROOT / "artifacts" / "pattern_class_physics_profile.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/pattern_class_physics_profile.json")


if __name__ == "__main__":
    main()
