#!/usr/bin/env python3
"""Fit explicit label functions for H12 triangles in Heisenberg coordinates.

We label H27 vertices by (u,z) in F3^2 × Z3 (Heisenberg model).
For each of the 4 H12 triangles, each H27 vertex is adjacent to exactly
one of the three triangle vertices. We attempt to express that vertex label
as a low-degree polynomial in (u1,u2,z).

Outputs:
- artifacts/h12_triangle_label_functions.json
- artifacts/h12_triangle_label_functions.md
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h12_triangle_label_functions.json"
OUT_MD = ROOT / "artifacts" / "h12_triangle_label_functions.md"


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
    return tuple_map, triangles


def row_reduce_mod3(mat, vec=None):
    m = [list(row) for row in mat]
    b = list(vec) if vec is not None else None
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
        if b is not None:
            b[rank], b[pivot] = b[pivot], b[rank]
        inv = 1 if m[rank][col] == 1 else 2
        m[rank] = [(inv * x) % 3 for x in m[rank]]
        if b is not None:
            b[rank] = (inv * b[rank]) % 3
        for r in range(n_rows):
            if r == rank:
                continue
            factor = m[r][col] % 3
            if factor != 0:
                m[r] = [(m[r][c] - factor * m[rank][c]) % 3 for c in range(n_cols)]
                if b is not None:
                    b[r] = (b[r] - factor * b[rank]) % 3
        pivots.append(col)
        rank += 1
        col += 1
    return rank, m, b, pivots


def solve_linear_mod3(A, b):
    rank, rref, b2, pivots = row_reduce_mod3(A, b)
    for i in range(rank, len(A)):
        if b2[i] % 3 != 0:
            return None
    n_cols = len(A[0])
    x = [0] * n_cols
    for i, col in enumerate(pivots):
        x[col] = b2[i]
    return x


def generate_monomials(max_degree):
    exps = []
    for e0 in range(max_degree + 1):
        for e1 in range(max_degree + 1):
            for e2 in range(max_degree + 1):
                if e0 + e1 + e2 <= max_degree:
                    exps.append((e0, e1, e2))
    return exps


def eval_monomial(exp, vars3):
    val = 1
    for e, v in zip(exp, vars3):
        val = (val * pow(v, e, 3)) % 3
    return val


def fit_polynomial(samples, degree):
    exps = generate_monomials(degree)
    A = []
    b = []
    for (u1, u2, z), label in samples:
        A.append([eval_monomial(exp, (u1, u2, z)) for exp in exps])
        b.append(label)
    sol = solve_linear_mod3(A, b)
    return sol, exps


def poly_to_string(sol, exps):
    if sol is None:
        return None
    terms = []
    for coeff, exp in zip(sol, exps):
        if coeff % 3 == 0:
            continue
        name = []
        vars3 = ["u1", "u2", "z"]
        for var, e in zip(vars3, exp):
            if e == 1:
                name.append(var)
            elif e == 2:
                name.append(f"{var}^2")
        term = "*".join(name) if name else "1"
        if coeff % 3 == 2:
            term = f"2*{term}"
        terms.append(term)
    return " + ".join(terms) if terms else "0"


def main():
    adj = construct_w33()
    v0 = 0
    tuple_map, triangles = h27_tuple_map(adj, v0)
    nonneighbors = [i for i in range(adj.shape[0]) if i != v0 and adj[v0, i] == 0]

    # fixed Heisenberg labeling from earlier model
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

    # build Z3 labeling for each fiber (reuse a fixed solution)
    # fiber positions are ordered by vertex index within each fiber (3 vertices)
    # and permuted by the found translation labeling
    # We'll reuse the labeling from the Heisenberg verification by recomputing it.
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

    labeling = {}
    for i, key in enumerate(fiber_keys):
        perm = solution[i]
        for pos, v in enumerate(fibers[key]):
            z = perm[pos]
            labeling[v] = (coords[key], z)

    # now fit label functions for each triangle
    triangle_fits = []
    for t_idx, tri in enumerate(triangles):
        samples = []
        for u in nonneighbors:
            (u1, u2), z = labeling[u]
            # which vertex in triangle does u connect to?
            label = None
            for li, v in enumerate(tri):
                if adj[u, v]:
                    label = li
                    break
            samples.append(((u1, u2, z), label))
        # fit degree 1 and degree 2
        sol1, exps1 = fit_polynomial(samples, 1)
        sol2, exps2 = fit_polynomial(samples, 2)
        triangle_fits.append(
            {
                "triangle": tri,
                "degree1": {
                    "solvable": sol1 is not None,
                    "formula": poly_to_string(sol1, exps1),
                },
                "degree2": {
                    "solvable": sol2 is not None,
                    "formula": poly_to_string(sol2, exps2),
                },
            }
        )

    results = {
        "base_vertex": v0,
        "triangle_fits": triangle_fits,
    }

    lines = []
    lines.append("# H12 Triangle Label Functions")
    lines.append("")
    for entry in triangle_fits:
        lines.append(f"## Triangle {entry['triangle']}")
        lines.append(
            f"- degree 1: solvable={entry['degree1']['solvable']} formula={entry['degree1']['formula']}"
        )
        lines.append(
            f"- degree 2: solvable={entry['degree2']['solvable']} formula={entry['degree2']['formula']}"
        )
        lines.append("")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
