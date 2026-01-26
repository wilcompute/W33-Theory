#!/usr/bin/env python3
"""Compute invariants of the H27 triangle-choice code.

Builds the 27 tuples in F3^4 from a base vertex v0 using the 4 H12 triangles,
with a deterministic labeling (triangle order + vertex order). Then computes:
  - Hamming distance distribution
  - Span rank over F3 (affine dimension)
  - Line/plane counts inside the 27-point set
  - Automorphism group under S3^4 ⋊ S4 (symbol/coordinate permutations)

Outputs:
- artifacts/h27_code_invariants.json
- artifacts/h27_code_invariants.md
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import permutations, product, combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_code_invariants.json"
OUT_MD = ROOT / "artifacts" / "h27_code_invariants.md"


def construct_w33():
    """Construct W33 from F_3^4 symplectic geometry."""
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
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
            proj_points.append(v)

    n = len(proj_points)

    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return adj, proj_points


def find_h12_triangles(adj, v0):
    """Return the 4 disjoint triangles inside H12 (neighbors of v0)."""
    n = adj.shape[0]
    neighbors = [i for i in range(n) if adj[v0, i] == 1]

    visited = set()
    triangles = []
    for start in neighbors:
        if start in visited:
            continue
        stack = [start]
        comp = []
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            comp.append(v)
            for u in neighbors:
                if u not in visited and adj[v, u]:
                    stack.append(u)
        triangles.append(tuple(sorted(comp)))

    return sorted(triangles)


def h27_tuple_set(adj, v0):
    """Return the 27 tuples in F3^4 based on triangle labels."""
    triangles = find_h12_triangles(adj, v0)
    tri_index = [{v: i for i, v in enumerate(tri)} for tri in triangles]

    nonneighbors = [i for i in range(adj.shape[0]) if i != v0 and adj[v0, i] == 0]
    tuples = []
    for u in nonneighbors:
        tup = []
        for t in range(4):
            found = None
            for v in triangles[t]:
                if adj[u, v]:
                    found = tri_index[t][v]
                    break
            if found is None:
                found = -1
            tup.append(found)
        tuples.append(tuple(tup))
    return tuples


def row_reduce_mod3(mat):
    """Row-reduce a matrix over F3 and return rank."""
    m = [list(row) for row in mat]
    n_rows = len(m)
    n_cols = len(m[0]) if n_rows else 0
    rank = 0
    col = 0
    while rank < n_rows and col < n_cols:
        pivot = None
        for r in range(rank, n_rows):
            if m[r][col] % 3 != 0:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        inv = 1 if m[rank][col] == 1 else 2
        m[rank] = [(inv * x) % 3 for x in m[rank]]
        for r in range(n_rows):
            if r == rank:
                continue
            factor = m[r][col] % 3
            if factor != 0:
                m[r] = [(m[r][c] - factor * m[rank][c]) % 3 for c in range(n_cols)]
        rank += 1
        col += 1
    return rank


def all_affine_lines():
    """Return all affine lines in F3^4 as sorted tuples of 3 points."""
    points = list(product([0, 1, 2], repeat=4))
    lines = set()
    for a in points:
        for d in points:
            if d == (0, 0, 0, 0):
                continue
            b = tuple((a[i] + d[i]) % 3 for i in range(4))
            c = tuple((a[i] + 2 * d[i]) % 3 for i in range(4))
            line = tuple(sorted([a, b, c]))
            lines.add(line)
    return list(lines)


def all_affine_planes():
    """Return all affine 2-planes in F3^4 as sorted tuples of 9 points."""
    points = list(product([0, 1, 2], repeat=4))
    planes = set()
    for a in points:
        for d1 in points:
            if d1 == (0, 0, 0, 0):
                continue
            for d2 in points:
                if d2 == (0, 0, 0, 0):
                    continue
                # check independence: d2 not in span(d1)
                if d2 == d1 or d2 == tuple((2 * x) % 3 for x in d1):
                    continue
                plane = []
                for s in [0, 1, 2]:
                    for t in [0, 1, 2]:
                        pt = tuple((a[i] + s * d1[i] + t * d2[i]) % 3 for i in range(4))
                        plane.append(pt)
                plane = tuple(sorted(plane))
                planes.add(plane)
    return list(planes)


def automorphism_group_size(tuples):
    """Compute size of automorphism group under S3^4 ⋊ S4."""
    s3 = list(permutations([0, 1, 2]))
    s4 = list(permutations([0, 1, 2, 3]))
    tuple_set = set(tuples)

    count = 0
    for perm_coords in s4:
        for p0 in s3:
            for p1 in s3:
                for p2 in s3:
                    for p3 in s3:
                        perms = [p0, p1, p2, p3]
                        mapped = []
                        for x in tuples:
                            y = []
                            for i in range(4):
                                y.append(perms[i][x[perm_coords[i]]])
                            mapped.append(tuple(y))
                        if set(mapped) == tuple_set:
                            count += 1
    return count


def main():
    adj, _ = construct_w33()
    v0 = 0
    tuples = h27_tuple_set(adj, v0)
    tuple_set = set(tuples)

    lines = []
    results = {}

    lines.append("# H27 Code Invariants")
    lines.append("")
    lines.append(f"- Base vertex: v{v0}")
    lines.append(f"- Tuples: {len(tuples)} (unique {len(tuple_set)})")
    lines.append("")

    # Hamming distance distribution
    dist_counts = Counter()
    for a, b in combinations(tuples, 2):
        dist = sum(1 for i in range(4) if a[i] != b[i])
        dist_counts[dist] += 1
    results["hamming_distance_distribution"] = dict(dist_counts)

    lines.append("## Hamming Distance Distribution")
    for d, c in sorted(dist_counts.items()):
        lines.append(f"- d={d}: {c}")
    lines.append("")

    # Span rank (affine dimension)
    base = tuples[0]
    diffs = []
    for x in tuples[1:]:
        diffs.append([(x[i] - base[i]) % 3 for i in range(4)])
    rank = row_reduce_mod3(diffs)
    results["affine_span_rank"] = rank
    lines.append(f"## Affine Span Rank (over F3)")
    lines.append(f"- rank = {rank}")
    lines.append("")

    # Count affine lines contained
    all_lines = all_affine_lines()
    contained_lines = [L for L in all_lines if all(p in tuple_set for p in L)]
    results["affine_lines_in_code"] = len(contained_lines)
    lines.append("## Affine Lines")
    lines.append(f"- lines contained: {len(contained_lines)}")
    lines.append("")

    # Count affine planes contained (size 9)
    all_planes = all_affine_planes()
    contained_planes = [P for P in all_planes if all(p in tuple_set for p in P)]
    results["affine_planes_in_code"] = len(contained_planes)
    lines.append("## Affine 2-Planes (size 9)")
    lines.append(f"- planes contained: {len(contained_planes)}")
    lines.append("")

    # Automorphism group size
    auto_size = automorphism_group_size(tuples)
    results["automorphism_group_size_s3s4"] = auto_size
    lines.append("## Automorphism Group under S3^4 ⋊ S4")
    lines.append(f"- size: {auto_size}")
    lines.append("")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
