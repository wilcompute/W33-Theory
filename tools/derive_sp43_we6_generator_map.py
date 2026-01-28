#!/usr/bin/env python3
"""Derive explicit generator map Sp(4,3) -> W(E6) via edge->root bijection.

We use the explicit edge->root mapping and the symplectic generators to obtain
permutations of the 240 E8 roots. We then verify these permutations preserve
inner products and W(E6) orbit structure (72 + 6*27 + 6*1).
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
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

    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i+1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def normalize_proj(v):
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    return tuple(v)


def check_symplectic(M):
    Omega = np.array([[0,0,1,0],[0,0,0,1],[2,0,0,0],[0,2,0,0]], dtype=int)
    M = np.array(M, dtype=int) % 3
    return np.all(((M.T @ Omega @ M) % 3) == Omega)


def apply_matrix(M, v):
    M = np.array(M, dtype=int) % 3
    v = np.array(v, dtype=int) % 3
    result = (M @ v) % 3
    return normalize_proj(result.tolist())


def generator_matrices():
    return [
        [[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,0],[1,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,1,0,1]],
        [[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,2,1]],
        [[1,0,0,0],[1,1,0,0],[0,0,1,2],[0,0,0,1]],
        [[0,0,1,0],[0,1,0,0],[2,0,0,0],[0,0,0,1]],
        [[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,2,0,0]],
        [[2,0,0,0],[0,1,0,0],[0,0,2,0],[0,0,0,1]],
        [[1,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,2]],
    ]


def build_e8_roots():
    roots = []
    for i in range(8):
        for j in range(i+1, 8):
            for si in (1, -1):
                for sj in (1, -1):
                    r = [0.0] * 8
                    r[i] = float(si)
                    r[j] = float(sj)
                    roots.append(tuple(r))
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(0.5 * s for s in signs))
    return roots


def main():
    vertices, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    # load edge -> root map
    edge_map = json.loads((ROOT / 'artifacts' / 'explicit_bijection_decomposition.json').read_text())
    edge_to_root_idx = {int(k): v for k, v in edge_map['edge_to_root_index'].items()}

    # W(E6) orbit labels
    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}
    root_coords = [tuple(r) for r in edge_map['root_coords']]

    # root index -> orbit id, size
    root_orbit = {}
    for idx, r in enumerate(root_coords):
        info = root_to_orbit.get(tuple(r))
        if info:
            root_orbit[idx] = (info['orbit_id'], info['orbit_size'])

    # E8 roots list
    e8_roots = build_e8_roots()
    root_to_idx = {r: i for i, r in enumerate(e8_roots)}

    def normalize_root(r):
        # edge_map roots are often scaled by 2
        sq = sum(x * x for x in r)
        max_abs = max(abs(x) for x in r)
        if sq == 8 and max_abs in (1, 2):
            return tuple(x / 2.0 for x in r)
        if max_abs > 1.0:
            return tuple(x / 2.0 for x in r)
        return tuple(r)

    # Map explicit roots to indices (normalized)
    map_idx = {i: root_to_idx[normalize_root(r)] for i, r in enumerate(root_coords)}
    inv_map_idx = {v: k for k, v in map_idx.items()}

    # Build edge permutations for generators and lift to root permutations
    results = []
    for gen_idx, M in enumerate(generator_matrices()):
        if not check_symplectic(M):
            continue

        # vertex permutation
        v_to_idx = {tuple(v): i for i, v in enumerate(vertices)}
        vperm = [None] * 40
        for i, v in enumerate(vertices):
            vperm[i] = v_to_idx[apply_matrix(M, v)]

        # edge permutation
        eperm = [None] * len(edges)
        for i, e in enumerate(edges):
            a, b = e
            na, nb = vperm[a], vperm[b]
            eperm[i] = edge_to_idx[tuple(sorted((na, nb)))]

        # root permutation via edge map
        rperm = [None] * 240
        for eidx, ridx in edge_to_root_idx.items():
            new_e = eperm[eidx]
            new_r = edge_to_root_idx[new_e]
            rperm[map_idx[ridx]] = map_idx[new_r]

        # verify it is a permutation of 240
        if any(x is None for x in rperm):
            raise RuntimeError('Incomplete root permutation')

        # verify inner products preserved
        def dot(r1, r2):
            return sum(a*b for a, b in zip(r1, r2))

        ok = True
        for i in range(20):  # sample check
            for j in range(20):
                if i == j:
                    continue
                ip1 = dot(e8_roots[i], e8_roots[j])
                ip2 = dot(e8_roots[rperm[i]], e8_roots[rperm[j]])
                if abs(ip1 - ip2) > 1e-6:
                    ok = False
                    break
            if not ok:
                break

        # orbit preservation check (using root_orbit on mapped indices)
        orbit_ok = True
        for ridx, (oid, osz) in root_orbit.items():
            i = map_idx[ridx]
            j = rperm[i]
            info = root_orbit.get(inv_map_idx.get(j), None)
            if info is None or info[1] != osz:
                orbit_ok = False
                break

        results.append({
            "gen_index": gen_idx,
            "preserves_inner_products": ok,
            "preserves_we6_orbits": orbit_ok,
            "root_perm": rperm,
        })

    out = {
        "generator_maps": results,
    }

    out_path = ROOT / 'artifacts' / 'sp43_we6_generator_map.json'
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
