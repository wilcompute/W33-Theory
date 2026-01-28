#!/usr/bin/env python3
"""Compute subgroup of PSp(4,3) that preserves W(E6) pattern classes on W33 vertices.

Uses:
- artifacts/we6_coxeter6_intersection.json (pattern rows for 40 orbit indices)
- artifacts/e8_orbit_to_f3_point.json (orbit -> F3^4 point)

Outputs:
- artifacts/pattern_preserving_subgroup.json
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def construct_w33_points():
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
    return proj_points


def normalize_proj(v):
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    return tuple(v)


def mat_mult_mod3(A, B):
    n, k, m = len(A), len(B), len(B[0])
    out = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0
            for l in range(k):
                s = (s + A[i][l] * B[l][j]) % 3
            out[i][j] = s
    return out


def check_symplectic(M):
    Omega = [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]]
    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    return mat_mult_mod3(mat_mult_mod3(MT, Omega), M) == Omega


def apply_matrix(M, v):
    res = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    return normalize_proj(res)


def matrix_to_perm(M, points):
    idx = {p: i for i, p in enumerate(points)}
    perm = []
    for p in points:
        q = apply_matrix(M, p)
        perm.append(idx[q])
    return tuple(perm)


def build_generators(points):
    gen_matrices = [
        [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 2, 1]],
        [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 2], [0, 0, 0, 1]],
        [[0, 0, 1, 0], [0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0]],
        [[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 2]],
    ]
    gens = []
    for M in gen_matrices:
        if check_symplectic(M):
            gens.append(matrix_to_perm(M, points))
    return gens


def perm_comp(p, q):
    # composition p∘q (apply q then p)
    return tuple(p[i] for i in q)


def perm_inv(p):
    inv = [0] * len(p)
    for i, v in enumerate(p):
        inv[v] = i
    return tuple(inv)


def subgroup_order(gens, color):
    # BFS over generated subgroup that preserves colors
    identity = tuple(range(len(color)))
    good_gens = []
    for g in gens:
        if all(color[i] == color[g[i]] for i in range(len(color))):
            good_gens.append(g)
    seen = {identity}
    q = deque([identity])
    while q:
        cur = q.popleft()
        for g in good_gens:
            nxt = perm_comp(g, cur)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return len(seen), good_gens


def main():
    points = construct_w33_points()

    # Orbit->point mapping (Coxeter6 orbit index -> F3 point)
    orbit_map = json.loads(
        (ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text()
    )
    orbit_to_point = {int(k): tuple(v) for k, v in orbit_map["mapping"].items()}
    point_to_orbit = {v: k for k, v in orbit_to_point.items()}

    # Pattern class for each orbit (row tuple)
    inter = json.loads(
        (ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text()
    )
    patterns = [tuple(row) for row in inter["matrix"]]
    pat_ids = {}
    for row in patterns:
        if row not in pat_ids:
            pat_ids[row] = len(pat_ids)

    # Color each W33 vertex by its pattern id
    colors = []
    for p in points:
        orb = point_to_orbit[p]
        colors.append(pat_ids[patterns[orb]])

    gens = build_generators(points)

    order, good_gens = subgroup_order(gens, colors)

    # Orbit sizes on vertices under the color‑preserving subgroup
    # Build subgroup explicitly (small enough) to compute orbits
    identity = tuple(range(40))
    seen = {identity}
    q = deque([identity])
    while q:
        cur = q.popleft()
        for g in good_gens:
            nxt = perm_comp(g, cur)
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    group = list(seen)

    # Orbits on vertices
    un = set(range(40))
    orbits = []
    while un:
        v = next(iter(un))
        orb = set(p[v] for p in group)
        orbits.append(sorted(orb))
        un -= orb

    out = {
        "generator_count": len(gens),
        "color_preserving_generators": len(good_gens),
        "subgroup_order": order,
        "vertex_orbit_sizes": sorted([len(o) for o in orbits], reverse=True),
        "pattern_class_count": len(pat_ids),
        "class_sizes": {str(i): colors.count(i) for i in set(colors)},
    }

    (ROOT / "artifacts" / "pattern_preserving_subgroup.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    print(out)
    print("Wrote artifacts/pattern_preserving_subgroup.json")


if __name__ == "__main__":
    main()
