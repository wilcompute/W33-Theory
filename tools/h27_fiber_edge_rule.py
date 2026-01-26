#!/usr/bin/env python3
"""Derive explicit edge rule for H27 as F3^2 × Z3 using fiber matchings.

Steps:
1) Build 9 fibers (triplets) from triangle-choice tuples.
2) Find labelings of each fiber by Z3 so every inter-fiber matching
   is a translation (i -> i + c).
3) Record the translation constants c(u,v) for ordered fiber pairs.
4) Attempt to fit c(u,v) as a low-degree polynomial in u=(u1,u2), v=(v1,v2).
5) Test if c(u,v) = f(u)+g(v) or c(u,v) = f(u)+g(v)+u^T M v fits.

Outputs:
- artifacts/h27_fiber_edge_rule.json
- artifacts/h27_fiber_edge_rule.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_fiber_edge_rule.json"
OUT_MD = ROOT / "artifacts" / "h27_fiber_edge_rule.md"


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


def row_reduce_mod3(mat, vec=None):
    """Row reduce matrix (and optional rhs) over F3."""
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
    """Solve A x = b over F3. Return one solution or None."""
    rank, rref, b2, pivots = row_reduce_mod3(A, b)
    # check consistency
    for i in range(rank, len(A)):
        if b2[i] % 3 != 0:
            return None
    n_cols = len(A[0])
    x = [0] * n_cols
    # set free vars to 0
    for i, col in enumerate(pivots):
        x[col] = b2[i]
    return x


def generate_monomials(max_degree):
    """Return list of exponent tuples for 4 variables with total degree <= max_degree."""
    exps = []
    for e0 in range(max_degree + 1):
        for e1 in range(max_degree + 1):
            for e2 in range(max_degree + 1):
                for e3 in range(max_degree + 1):
                    if e0 + e1 + e2 + e3 <= max_degree:
                        exps.append((e0, e1, e2, e3))
    return exps


def eval_monomial(exp, vars4):
    val = 1
    for e, v in zip(exp, vars4):
        val = (val * pow(v, e, 3)) % 3
    return val


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

    # compute affine F3^2 coords for fibers
    # hardcode from prior basis calculation (deterministic from v0)
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

    # build matching permutations P_{A,B}
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

    # search for fiber labelings in S3 so all matchings become translations
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

    def ok_with(i, perm_i):
        for j, perm_j in assignments.items():
            Pij = P[j][i]
            if Pij is None:
                continue
            eff = perm_compose(perm_inverse(perm_i), perm_compose(Pij, perm_j))
            if eff not in c3:
                return False
        return True

    solution = None

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

    # build translation constants c(u,v)
    translation = {}
    if solution is not None:
        for i in range(len(fiber_keys)):
            for j in range(len(fiber_keys)):
                if i == j:
                    continue
                LA = solution[i]
                LB = solution[j]
                eff = perm_compose(perm_inverse(LB), perm_compose(P[i][j], LA))
                if eff == (0, 1, 2):
                    c = 0
                elif eff == (1, 2, 0):
                    c = 1
                elif eff == (2, 0, 1):
                    c = 2
                else:
                    c = None
                translation[(i, j)] = c

    # build dataset for c(u,v)
    data = []
    for i, a in enumerate(fiber_keys):
        for j, b in enumerate(fiber_keys):
            if i == j:
                continue
            u = coords[a]
            v = coords[b]
            c = translation[(i, j)]
            data.append((u, v, c))

    # fit polynomial c(u,v)
    fit_results = []
    degree2_formula = None
    for degree in [1, 2, 3]:
        exps = generate_monomials(degree)
        A = []
        b = []
        for (u, v, c) in data:
            x = (u[0], u[1], v[0], v[1])
            A.append([eval_monomial(e, x) for e in exps])
            b.append(c)
        sol = solve_linear_mod3(A, b)
        fit_results.append({
            "degree": degree,
            "solvable": sol is not None,
            "num_monomials": len(exps),
        })
        if sol is not None:
            fit_results[-1]["coeffs"] = sol
            fit_results[-1]["exps"] = exps
            if degree == 2 and degree2_formula is None:
                # build a human-readable polynomial string
                terms = []
                for coeff, exp in zip(sol, exps):
                    if coeff % 3 == 0:
                        continue
                    name = []
                    vars4 = ["u1", "u2", "v1", "v2"]
                    for var, e in zip(vars4, exp):
                        if e == 1:
                            name.append(var)
                        elif e == 2:
                            name.append(f"{var}^2")
                        elif e > 2:
                            name.append(f"{var}^{e}")
                    term = "*".join(name) if name else "1"
                    if coeff % 3 == 2:
                        term = f"2*{term}"
                    terms.append(term)
                degree2_formula = " + ".join(terms) if terms else "0"

    # try c(u,v) = f(u)+g(v)
    # variables: f(u) for 9 u's, g(v) for 9 v's
    u_list = sorted(set([u for (u, _, _) in data]))
    v_list = sorted(set([v for (_, v, _) in data]))
    u_idx = {u: i for i, u in enumerate(u_list)}
    v_idx = {v: i for i, v in enumerate(v_list)}
    A = []
    b = []
    for (u, v, c) in data:
        row = [0] * (len(u_list) + len(v_list))
        row[u_idx[u]] = 1
        row[len(u_list) + v_idx[v]] = 1
        A.append(row)
        b.append(c)
    sol_f = solve_linear_mod3(A, b)

    # try c(u,v) = f(u)+g(v)+u^T M v (bilinear)
    # variables: f(u) (9), g(v) (9), M (2x2 =4)
    A = []
    b = []
    for (u, v, c) in data:
        row = [0] * (len(u_list) + len(v_list) + 4)
        row[u_idx[u]] = 1
        row[len(u_list) + v_idx[v]] = 1
        # bilinear terms: u1 v1, u1 v2, u2 v1, u2 v2
        row[len(u_list) + len(v_list) + 0] = (u[0] * v[0]) % 3
        row[len(u_list) + len(v_list) + 1] = (u[0] * v[1]) % 3
        row[len(u_list) + len(v_list) + 2] = (u[1] * v[0]) % 3
        row[len(u_list) + len(v_list) + 3] = (u[1] * v[1]) % 3
        A.append(row)
        b.append(c)
    sol_bilin = solve_linear_mod3(A, b)

    results = {
        "solution_found": solution is not None,
        "fiber_coords": {str(k): v for k, v in coords.items()},
        "translation_constants": {str(k): v for k, v in translation.items()},
        "polynomial_fits": fit_results,
        "degree2_formula": degree2_formula,
        "f_plus_g_solvable": sol_f is not None,
        "f_g_bilinear_solvable": sol_bilin is not None,
    }

    lines = []
    lines.append("# H27 Fiber Edge Rule")
    lines.append("")
    lines.append(f"- translation labeling found: {solution is not None}")
    lines.append(f"- f(u)+g(v) solvable: {sol_f is not None}")
    lines.append(f"- f(u)+g(v)+u^T M v solvable: {sol_bilin is not None}")
    lines.append("")
    lines.append("## Polynomial fit for c(u,v)")
    for fit in fit_results:
        lines.append(f"- degree {fit['degree']} (monomials={fit['num_monomials']}): solvable={fit['solvable']}")
    if degree2_formula is not None:
        lines.append("")
        lines.append(f"- degree-2 formula: c(u,v) = {degree2_formula} (mod 3)")
    lines.append("")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
