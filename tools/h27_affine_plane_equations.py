#!/usr/bin/env python3
"""Compute linear equations defining the 9-point affine plane inside H27 tuples.

The triangle-choice encoding yields 9 distinct tuples in F3^4. These form
an affine 2-plane, hence are the solution set of two independent linear
equations a·x = c over F3.

Outputs:
- artifacts/h27_affine_plane_equations.json
- artifacts/h27_affine_plane_equations.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_affine_plane_equations.json"
OUT_MD = ROOT / "artifacts" / "h27_affine_plane_equations.md"


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
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
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


def h27_unique_tuples(adj, v0):
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
    return sorted(set(tuples))


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


def nullspace_basis_mod3(mat):
    """Return a basis for nullspace of mat over F3."""
    rank, rref, pivots = row_reduce_mod3(mat)
    n_cols = len(rref[0])
    free_cols = [c for c in range(n_cols) if c not in pivots]
    basis = []
    for free in free_cols:
        v = [0] * n_cols
        v[free] = 1
        for i in range(rank):
            pivot_col = pivots[i]
            v[pivot_col] = (-rref[i][free]) % 3
        basis.append(v)
    return basis


def main():
    adj, _ = construct_w33()
    v0 = 0
    tuples = h27_unique_tuples(adj, v0)

    base = tuples[0]
    diffs = [[(p[i] - base[i]) % 3 for i in range(4)] for p in tuples[1:]]
    # find nullspace of diffs matrix
    basis = nullspace_basis_mod3(diffs)

    equations = []
    for alpha in basis:
        c = sum(alpha[i] * base[i] for i in range(4)) % 3
        equations.append({"alpha": alpha, "c": c})

    results = {
        "base_vertex": v0,
        "unique_tuple_count": len(tuples),
        "equations": equations,
        "tuples": tuples,
    }

    lines = []
    lines.append("# H27 Affine Plane Equations")
    lines.append("")
    lines.append(f"- Base vertex: v{v0}")
    lines.append(f"- Unique tuples: {len(tuples)}")
    lines.append("")

    lines.append("## Linear equations a·x = c (over F3)")
    for eq in equations:
        lines.append(f"- alpha={eq['alpha']}, c={eq['c']}")
    lines.append("")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
