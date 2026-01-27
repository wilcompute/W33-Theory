#!/usr/bin/env python3
"""Produce a table of W33 vertices in the local Heisenberg coordinates.

Outputs:
- artifacts/w33_local_heisenberg_table.json
- artifacts/w33_local_heisenberg_table.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "w33_local_heisenberg_table.json"
OUT_MD = ROOT / "artifacts" / "w33_local_heisenberg_table.md"


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

    hz_label = {}
    for i, key in enumerate(fiber_keys):
        perm = solution[i]
        for pos, v in enumerate(fibers[key]):
            z = perm[pos]
            hz_label[v] = (coords[key], z)

    rows = []
    # base
    rows.append({"vertex": v0, "class": "base"})
    # H12
    for t_idx, tri in enumerate(triangles):
        for label, v in enumerate(tri):
            rows.append({"vertex": v, "class": "H12", "triangle": t_idx, "label": label})
    # H27
    for v in nonneighbors:
        (u1, u2), z = hz_label[v]
        rows.append({"vertex": v, "class": "H27", "u1": u1, "u2": u2, "z": z})

    rows = sorted(rows, key=lambda r: r["vertex"])
    OUT_JSON.write_text(json.dumps(rows, indent=2))

    lines = []
    lines.append("# W33 Local Heisenberg Coordinates Table")
    lines.append("")
    lines.append("| vertex | class | triangle | label | u1 | u2 | z |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append(
            f"| {r.get('vertex')} | {r.get('class')} | "
            f"{r.get('triangle', '')} | {r.get('label', '')} | "
            f"{r.get('u1', '')} | {r.get('u2', '')} | {r.get('z', '')} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
