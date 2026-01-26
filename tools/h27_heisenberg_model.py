#!/usr/bin/env python3
"""Verify H27 adjacency matches a Heisenberg-group model on F3^2 × Z3.

We use the bilinear rule:
  c(u,v) = u2*v1 + 2*u1*v2  (mod 3)
and adjacency:
  (u,z) ~ (v,w)  iff  u != v and w = z + c(u,v).

This yields a Cayley graph of the Heisenberg group H(3) with
generators {(t,0): t in F3^2\\{0}}.

Outputs:
- artifacts/h27_heisenberg_model.json
- artifacts/h27_heisenberg_model.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_heisenberg_model.json"
OUT_MD = ROOT / "artifacts" / "h27_heisenberg_model.md"


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
            if found is None:
                found = -1
            tup.append(found)
        tuple_map[u] = tuple(tup)
    return tuple_map


def main():
    adj = construct_w33()
    v0 = 0
    tuple_map = h27_tuple_map(adj, v0)
    nonneighbors = sorted(tuple_map.keys())

    # group vertices into fibers by tuple
    fibers = {}
    for v in nonneighbors:
        fibers.setdefault(tuple_map[v], []).append(v)
    fiber_keys = sorted(fibers.keys())
    fibers = {k: sorted(vs) for k, vs in fibers.items()}

    # fixed affine F3^2 coords for fibers (from earlier basis)
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

    # build matching permutations between fibers
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

    # find Z3 labelings for each fiber so matchings are translations
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

    # build labeling map: vertex -> (u,z)
    labeling = {}
    if solution is not None:
        for i, key in enumerate(fiber_keys):
            perm = solution[i]
            for pos, v in enumerate(fibers[key]):
                z = perm[pos]
                labeling[v] = (coords[key], z)

    def c(u, v):
        return (u[1] * v[0] + 2 * u[0] * v[1]) % 3

    # verify adjacency rule
    mismatches = 0
    total_pairs = 0
    for i, a in enumerate(nonneighbors):
        for j, b in enumerate(nonneighbors):
            if i == j:
                continue
            total_pairs += 1
            ua, za = labeling[a]
            ub, zb = labeling[b]
            model_adj = (ua != ub) and (zb == (za + c(ua, ub)) % 3)
            if model_adj != bool(adj[a, b]):
                mismatches += 1

    results = {
        "base_vertex": v0,
        "solution_found": solution is not None,
        "mismatches": mismatches,
        "total_pairs": total_pairs,
        "adjacency_matches": mismatches == 0,
    }

    lines = []
    lines.append("# H27 Heisenberg Model Verification")
    lines.append("")
    lines.append(f"- solution found: {solution is not None}")
    lines.append(f"- adjacency matches model: {mismatches == 0}")
    lines.append(f"- mismatches: {mismatches} / {total_pairs}")
    lines.append("")
    lines.append("Model rule: (u,z)~(v,w) iff w = z + (u2*v1 + 2*u1*v2) and u != v.")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
