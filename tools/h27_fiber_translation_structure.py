#!/usr/bin/env python3
"""Check if H27 fibers admit a Z3-translation structure across matchings.

H27 splits into 9 fibers (triplets) by identical triangle-choice tuples.
Between any two fibers, adjacency is a perfect matching (3 edges).

We attempt to label each fiber with Z3 so that every inter-fiber matching
is a translation (i -> i + c). This is a constraint satisfaction problem
over S3 labelings per fiber.

If successful, we compute translation constants c(A,B) and test whether
they depend only on the affine F3^2 difference between fibers.

Outputs:
- artifacts/h27_fiber_translation_structure.json
- artifacts/h27_fiber_translation_structure.md
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_fiber_translation_structure.json"
OUT_MD = ROOT / "artifacts" / "h27_fiber_translation_structure.md"


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


def basis_coords(points):
    base = points[0]
    diffs = [[(p[i] - base[i]) % 3 for i in range(4)] for p in points[1:]]
    # choose two independent diff vectors as basis
    basis = []
    for row in diffs:
        if len(basis) == 0:
            basis.append(row)
        else:
            mat = basis + [row]
            if row_reduce_mod3(mat) > len(basis):
                basis.append(row)
        if len(basis) == 2:
            break
    if len(basis) < 2:
        return None, None
    b1, b2 = basis
    coords = {}
    for p in points:
        target = [(p[i] - base[i]) % 3 for i in range(4)]
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


def perm_compose(p, q):
    """Return p ∘ q (apply q then p), permutations as tuples."""
    return tuple(p[i] for i in q)


def perm_inverse(p):
    inv = [0, 0, 0]
    for i, j in enumerate(p):
        inv[j] = i
    return tuple(inv)


def main():
    adj, _ = construct_w33()
    v0 = 0
    tuple_map = h27_tuple_map(adj, v0)
    nonneighbors = sorted(tuple_map.keys())

    # group vertices into fibers by tuple
    fibers = {}
    for v in nonneighbors:
        fibers.setdefault(tuple_map[v], []).append(v)
    fiber_keys = sorted(fibers.keys())
    fibers = {k: sorted(vs) for k, vs in fibers.items()}

    # build matching permutations P_{A,B} between fibers
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

    # group constraints: want LB^{-1} P_{A,B} LA in C3
    s3 = [
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    ]
    c3 = {
        (0, 1, 2),  # +0
        (1, 2, 0),  # +1
        (2, 0, 1),  # +2
    }

    assignments = {0: (0, 1, 2)}  # fix first fiber labeling
    order = list(range(1, len(fiber_keys)))

    def ok_with(i, perm_i):
        for j, perm_j in assignments.items():
            Pij = P[j][i]
            if Pij is None:
                continue
            # LB^{-1} P_{A,B} LA
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

    results = {
        "solution_found": solution is not None,
    }

    lines = []
    lines.append("# H27 Fiber Translation Structure")
    lines.append("")
    lines.append(f"- solution found: {solution is not None}")
    lines.append("")

    if solution is not None:
        # compute translation constants
        translation = {}
        for i in range(len(fiber_keys)):
            for j in range(len(fiber_keys)):
                if i == j:
                    continue
                LA = solution[i]
                LB = solution[j]
                eff = perm_compose(perm_inverse(LB), perm_compose(P[i][j], LA))
                # map eff to c in Z3
                if eff == (0, 1, 2):
                    c = 0
                elif eff == (1, 2, 0):
                    c = 1
                elif eff == (2, 0, 1):
                    c = 2
                else:
                    c = None
                translation[(i, j)] = c

        # fiber coordinates in F3^2
        basis_info, coords = basis_coords(fiber_keys)
        results["fiber_coords"] = (
            {str(k): v for k, v in coords.items()} if coords else None
        )

        # check if translation depends only on coord difference
        diff_map = {}
        diff_counts = {}
        consistent = True
        for i in range(len(fiber_keys)):
            for j in range(len(fiber_keys)):
                if i == j:
                    continue
                ti = fiber_keys[i]
                tj = fiber_keys[j]
                ci = coords[ti]
                cj = coords[tj]
                diff = ((cj[0] - ci[0]) % 3, (cj[1] - ci[1]) % 3)
                val = translation[(i, j)]
                diff_counts.setdefault(diff, []).append(val)
                if diff in diff_map and diff_map[diff] != val:
                    consistent = False
                diff_map[diff] = val

        results["translation_consistent_by_diff"] = consistent
        results["translation_by_diff"] = {str(k): v for k, v in diff_map.items()}
        results["translation_by_diff_counts"] = {
            str(k): diff_counts[k] for k in diff_counts
        }

        lines.append("## Translation-by-difference check")
        lines.append(f"- consistent: {consistent}")
        if diff_map:
            lines.append("- mapping (dx,dy) -> c:")
            for k, v in sorted(diff_map.items()):
                lines.append(f"  - {k}: {v}")
            if not consistent:
                lines.append("- conflicts (values seen per diff):")
                for k, vals in sorted(diff_counts.items()):
                    lines.append(f"  - {k}: {vals}")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
