#!/usr/bin/env python3
"""Analyze the 3-to-1 collapse of H27 triangle-choice tuples.

Each H27 vertex chooses one vertex in each of the 4 H12 triangles. This yields
only 9 distinct 4-tuples in F3^4, each realized by 3 H27 vertices.

This tool:
- groups H27 vertices into 9 triplets by identical tuple
- analyzes adjacency within/between triplets
- builds the 9-class quotient graph
- expresses the 9 tuples in an F3^2 basis (rank-2 affine plane)

Outputs:
- artifacts/h27_triplet_structure.json
- artifacts/h27_triplet_structure.md
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_triplet_structure.json"
OUT_MD = ROOT / "artifacts" / "h27_triplet_structure.md"


def construct_w33():
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
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1
    return adj, proj_points


def find_h12_triangles(adj, v0):
    neighbors = [i for i in range(adj.shape[0]) if adj[v0, i] == 1]
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


def h27_tuple_map(adj, v0):
    triangles = find_h12_triangles(adj, v0)
    tri_index = [{v: i for i, v in enumerate(tri)} for tri in triangles]
    nonneighbors = [i for i in range(adj.shape[0]) if i != v0 and adj[v0, i] == 0]
    tuple_map = {}
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
        tuple_map[u] = tuple(tup)
    return tuple_map


def row_reduce_mod3(mat):
    m = [list(row) for row in mat]
    n_rows = len(m)
    n_cols = len(m[0]) if n_rows else 0
    rank = 0
    col = 0
    pivots = []
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
        pivots.append(col)
        rank += 1
        col += 1
    return rank, m, pivots


def basis_coords(points):
    """Express points in an F3^2 basis for their affine span."""
    base = points[0]
    diffs = [[(p[i] - base[i]) % 3 for i in range(4)] for p in points[1:]]
    rank, rref, pivots = row_reduce_mod3(diffs)
    # choose two independent diff vectors as basis
    basis = []
    for row in diffs:
        if len(basis) == 0:
            basis.append(row)
        else:
            mat = basis + [row]
            if row_reduce_mod3(mat)[0] > len(basis):
                basis.append(row)
        if len(basis) == 2:
            break
    if len(basis) < 2:
        return None, None
    b1, b2 = basis

    # solve for each point p: p = base + s*b1 + t*b2
    coords = {}
    for p in points:
        target = [(p[i] - base[i]) % 3 for i in range(4)]
        # brute force solve s,t in F3
        found = None
        for s in [0, 1, 2]:
            for t in [0, 1, 2]:
                cand = [(s * b1[i] + t * b2[i]) % 3 for i in range(4)]
                if cand == target:
                    found = (s, t)
                    break
            if found is not None:
                break
        coords[p] = found
    return (base, b1, b2), coords


def main():
    adj, _ = construct_w33()
    v0 = 0
    tuple_map = h27_tuple_map(adj, v0)
    nonneighbors = sorted(tuple_map.keys())

    # group by tuple
    groups = defaultdict(list)
    for u, tup in tuple_map.items():
        groups[tup].append(u)

    unique_tuples = sorted(groups.keys())
    group_sizes = sorted(len(v) for v in groups.values())

    # adjacency within/between groups
    group_list = list(unique_tuples)
    idx = {t: i for i, t in enumerate(group_list)}
    between_counts = np.zeros((len(group_list), len(group_list)), dtype=int)
    within_counts = []
    for t, verts in groups.items():
        # within
        edges = 0
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                if adj[verts[i], verts[j]]:
                    edges += 1
        within_counts.append(edges)
    for i, t1 in enumerate(group_list):
        for j, t2 in enumerate(group_list):
            if j <= i:
                continue
            count = 0
            for a in groups[t1]:
                for b in groups[t2]:
                    if adj[a, b]:
                        count += 1
            between_counts[i, j] = between_counts[j, i] = count

    # quotient graph (edge if any adjacency between groups)
    q_adj = (between_counts > 0).astype(int)
    q_edges = int(q_adj.sum() // 2)
    q_degrees = list(q_adj.sum(axis=1))

    # affine span coords of 9 tuples
    basis_info, coords = basis_coords(unique_tuples)

    def to_native(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {str(k): to_native(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [to_native(x) for x in obj]
        return obj

    results = {
        "base_vertex": v0,
        "unique_tuple_count": len(unique_tuples),
        "group_sizes": group_sizes,
        "within_group_edge_counts": within_counts,
        "between_group_edge_counts": between_counts.tolist(),
        "quotient_edges": q_edges,
        "quotient_degree_set": sorted(set(q_degrees)),
        "basis_info": basis_info,
        "coords": {str(k): v for k, v in coords.items()} if coords else None,
    }

    lines = []
    lines.append("# H27 Triplet Structure")
    lines.append("")
    lines.append(f"- Base vertex: v{v0}")
    lines.append(f"- Unique tuples: {len(unique_tuples)}")
    lines.append(f"- Group sizes: {group_sizes}")
    lines.append("")

    lines.append("## Within-group adjacency")
    for count in sorted(within_counts):
        lines.append(f"- edges in a group of 3: {count}")
    lines.append("")

    lines.append("## Between-group adjacency (counts per 3×3 block)")
    lines.append(f"- quotient edges: {q_edges}")
    lines.append(f"- quotient degree set: {sorted(set(q_degrees))}")
    lines.append("")

    if coords:
        lines.append("## Affine F3^2 Coordinates (for the 9 tuples)")
        base, b1, b2 = basis_info
        lines.append(f"- base = {base}")
        lines.append(f"- b1 = {b1}")
        lines.append(f"- b2 = {b2}")
        lines.append("")
        for t in unique_tuples:
            lines.append(f"- {t} -> {coords[t]}")
        lines.append("")

    OUT_JSON.write_text(json.dumps(to_native(results), indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
