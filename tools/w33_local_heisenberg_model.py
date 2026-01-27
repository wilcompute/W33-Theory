#!/usr/bin/env python3
"""Verify a full local model of W33 from Heisenberg + H12 linear forms.

We fix base vertex v0. Then:
- H12 (neighbors of v0) split into 4 triangles.
- H27 (non-neighbors) is modeled as F3^2 × Z3 with Heisenberg adjacency.
- Each H12 triangle corresponds to a linear form on F3^2:
    L0(u)=u2, L1(u)=u1, L2(u)=u1+u2, L3(u)=u1+2u2
  and the adjacent H12 vertex in triangle i has label L_i(u).

We build a model adjacency on all 40 vertices and compare with W33 adjacency.

Outputs:
- artifacts/w33_local_heisenberg_model.json
- artifacts/w33_local_heisenberg_model.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "w33_local_heisenberg_model.json"
OUT_MD = ROOT / "artifacts" / "w33_local_heisenberg_model.md"


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
    return adj


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
            tup.append(found if found is not None else -1)
        tuple_map[u] = tuple(tup)
    return tuple_map, triangles


def B(u, v):
    return (u[1] * v[0] + 2 * u[0] * v[1]) % 3


def main():
    adj = construct_w33()
    n = adj.shape[0]
    v0 = 0

    tuple_map, triangles = h27_tuple_map(adj, v0)
    nonneighbors = [i for i in range(n) if i != v0 and adj[v0, i] == 0]
    neighbors = [i for i in range(n) if adj[v0, i] == 1]

    # fiber coords for the 9 tuple types (from earlier basis)
    coords = {
        (0, 0, 0, 0): (0, 0),
        (0, 1, 1, 1): (1, 0),
        (0, 2, 2, 2): (2, 0),
        (1, 0, 1, 2): (0, 1),
        (1, 1, 2, 0): (1, 1),
        (1, 2, 0, 1): (2, 1),
        (2, 0, 2, 1): (0, 2),
        (2, 1, 0, 2): (1, 2),
        (2, 2, 1, 0): (2, 2),
    }

    # group vertices into fibers by tuple and build translation labeling
    fibers = {}
    for v in nonneighbors:
        fibers.setdefault(tuple_map[v], []).append(v)
    fiber_keys = sorted(fibers.keys())
    fibers = {k: sorted(vs) for k, vs in fibers.items()}

    # compute matching permutations between fibers
    idx = {k: i for i, k in enumerate(fiber_keys)}
    P = [[None for _ in fiber_keys] for _ in fiber_keys]
    for i, a in enumerate(fiber_keys):
        for j, b in enumerate(fiber_keys):
            if i == j:
                continue
            perm = []
            for va in fibers[a]:
                match = None
                for jb, vb in enumerate(fibers[b]):
                    if adj[va, vb]:
                        match = jb
                        break
                perm.append(match)
            P[i][j] = tuple(perm)

    s3 = [
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    ]
    c3 = {(0, 1, 2), (1, 2, 0), (2, 0, 1)}

    def perm_compose(p, q):
        return tuple(p[i] for i in q)

    def perm_inverse(p):
        inv = [0, 0, 0]
        for i, j in enumerate(p):
            inv[j] = i
        return tuple(inv)

    assignments = {0: (0, 1, 2)}
    order = list(range(1, len(fiber_keys)))
    solution = None

    def ok_with(i, perm_i):
        for j, perm_j in assignments.items():
            Pij = P[j][i]
            if Pij is None:
                continue
            eff = perm_compose(perm_inverse(perm_i), perm_compose(Pij, perm_j))
            if eff not in c3:
                return False
        return True

    def backtrack(k):
        nonlocal solution
        if k == len(order):
            solution = dict(assignments)
            return True
        i = order[k]
        for perm in s3:
            if ok_with(i, perm):
                assignments[i] = perm
                if backtrack(k + 1):
                    return True
                del assignments[i]
        return False

    backtrack(0)

    # build labeling for H27 vertices: (u,z)
    hz_label = {}
    for i, key in enumerate(fiber_keys):
        perm = solution[i]
        for pos, v in enumerate(fibers[key]):
            z = perm[pos]
            hz_label[v] = (coords[key], z)

    # linear forms for H12 triangles
    def L0(u): return u[1] % 3
    def L1(u): return u[0] % 3
    def L2(u): return (u[0] + u[1]) % 3
    def L3(u): return (u[0] + 2 * u[1]) % 3
    forms = [L0, L1, L2, L3]

    # model adjacency
    model = np.zeros((n, n), dtype=int)
    # base vertex adjacency to H12
    for v in neighbors:
        model[v0, v] = model[v, v0] = 1
    # H12 internal: triangles
    for tri in triangles:
        for i in range(3):
            for j in range(i + 1, 3):
                a, b = tri[i], tri[j]
                model[a, b] = model[b, a] = 1
    # H27 internal: Heisenberg rule
    for i, a in enumerate(nonneighbors):
        u, z = hz_label[a]
        for j, b in enumerate(nonneighbors):
            if i == j:
                continue
            v, w = hz_label[b]
            if u != v and (w - z) % 3 == B(u, v):
                model[a, b] = 1
    # H12-H27 via linear forms
    for t_idx, tri in enumerate(triangles):
        for a in tri:
            label = tri.index(a)
            for b in nonneighbors:
                u, _ = hz_label[b]
                if forms[t_idx](u) == label:
                    model[a, b] = model[b, a] = 1

    mismatches = int((model != adj).sum() // 2)
    results = {
        "base_vertex": v0,
        "mismatched_edges": mismatches,
        "model_matches_w33": mismatches == 0,
    }

    lines = []
    lines.append("# W33 Local Heisenberg Model Verification")
    lines.append("")
    lines.append(f"- base vertex: v{v0}")
    lines.append(f"- model matches W33: {mismatches == 0}")
    lines.append(f"- mismatched edges: {mismatches}")
    lines.append("")
    lines.append("Model components:")
    lines.append("- base vertex connected to all H12 vertices")
    lines.append("- H12 = 4 triangles (PG(1,3) × F3)")
    lines.append("- H27 = Heisenberg Cayley graph on F3^2 × Z3")
    lines.append("- H12–H27 via linear forms u2, u1, u1+u2, u1+2u2")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
