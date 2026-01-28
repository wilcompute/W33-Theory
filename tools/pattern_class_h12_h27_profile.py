#!/usr/bin/env python3
"""Profile W(E6) pattern classes by H12/H27 neighborhood structure.

For each W33 vertex, compute:
- its pattern class (from we6_coxeter6_intersection)
- counts of neighbors in each pattern class
- how its H12 triangles split across pattern classes

Outputs artifacts/pattern_class_h12_h27_profile.json
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def construct_w33_points_and_adj():
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

    n = len(points)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                adj[i][j] = adj[j][i] = 1

    return points, adj


def build_pattern_classes():
    inter = json.loads(
        (ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text()
    )
    orbit_map = json.loads(
        (ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text()
    )
    mapping = orbit_map["mapping"]

    # patterns per orbit id
    patterns = [tuple(row) for row in inter["matrix"]]
    pat_ids = {}
    for row in patterns:
        if row not in pat_ids:
            pat_ids[row] = len(pat_ids)

    # orbit id -> pattern class
    orbit_class = {i: pat_ids[patterns[i]] for i in range(40)}

    # point -> orbit id
    point_to_orbit = {tuple(v): int(k) for k, v in mapping.items()}

    # point index -> pattern class
    points, _ = construct_w33_points_and_adj()
    class_by_vertex = []
    for p in points:
        oid = point_to_orbit[p]
        class_by_vertex.append(orbit_class[oid])

    return class_by_vertex


def h12_triangles(adj, v):
    nbrs = [i for i, a in enumerate(adj[v]) if a]
    tris = []
    for a, b, c in combinations(nbrs, 3):
        if adj[a][b] and adj[a][c] and adj[b][c]:
            tris.append((a, b, c))
    return tris


def main():
    points, adj = construct_w33_points_and_adj()
    class_by_vertex = build_pattern_classes()
    k = max(class_by_vertex) + 1

    # Per-vertex profile
    vertex_profiles = []
    for v in range(40):
        nbrs = [i for i, a in enumerate(adj[v]) if a]
        # neighbor class counts
        counts = [0] * k
        for n in nbrs:
            counts[class_by_vertex[n]] += 1

        # H12 triangles and their class-multisets
        tris = h12_triangles(adj, v)
        tri_types = []
        for a, b, c in tris:
            tri_types.append(
                tuple(
                    sorted([class_by_vertex[a], class_by_vertex[b], class_by_vertex[c]])
                )
            )
        tri_counts = Counter(tri_types)

        vertex_profiles.append(
            {
                "vertex": v,
                "class": class_by_vertex[v],
                "neighbor_class_counts": counts,
                "triangle_class_multisets": {str(k): v for k, v in tri_counts.items()},
            }
        )

    # Aggregate per class
    class_profiles = defaultdict(list)
    for prof in vertex_profiles:
        class_profiles[prof["class"]].append(prof)

    class_summary = {}
    for c, profs in class_profiles.items():
        # average neighbor class counts
        avg = [0] * k
        for p in profs:
            for i, val in enumerate(p["neighbor_class_counts"]):
                avg[i] += val
        avg = [val / len(profs) for val in avg]

        # triangle multiset union
        tri_counter = Counter()
        for p in profs:
            for k2, v2 in p["triangle_class_multisets"].items():
                tri_counter[k2] += v2

        class_summary[str(c)] = {
            "size": len(profs),
            "avg_neighbor_class_counts": avg,
            "triangle_multiset_counts": dict(tri_counter),
        }

    out = {
        "class_count": k,
        "class_sizes": dict(Counter(class_by_vertex)),
        "class_summary": class_summary,
    }

    (ROOT / "artifacts" / "pattern_class_h12_h27_profile.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    print("Wrote artifacts/pattern_class_h12_h27_profile.json")


if __name__ == "__main__":
    main()
