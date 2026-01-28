#!/usr/bin/env python3
"""Compare balanced-orbit root graph to the Schlaefli (skew) graph."""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def build_w33_edges():
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

    return edges


def balanced_root_graph():
    edges = build_w33_edges()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    bias = json.loads((ROOT / 'artifacts' / 'su3_phase_orbit_bias.json').read_text())
    balanced_orbit = None
    for k, v in bias['orbit_sums'].items():
        if v == {'0': 9, '1': 9, '2': 9} or v == {0: 9, 1: 9, 2: 9}:
            balanced_orbit = int(k.split('_')[1])
    if balanced_orbit is None:
        raise RuntimeError("No balanced orbit found")

    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}
    edge_map = json.loads((ROOT / 'artifacts' / 'explicit_bijection_decomposition.json').read_text())
    edge_to_root_idx = {int(k): v for k, v in edge_map['edge_to_root_index'].items()}
    root_coords = [tuple(r) for r in edge_map['root_coords']]

    roots = []
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info and info['orbit_size'] == 27 and info['orbit_id'] == balanced_orbit:
            roots.append(np.array([x / 2.0 for x in r], dtype=float))

    n = len(roots)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            ip = float(np.dot(roots[i], roots[j]))
            if abs(ip - 1.0) < 1e-6:
                adj[i, j] = adj[j, i] = 1
    return adj


def build_schlafli_graphs():
    # Schlaefli intersection graph on 27 lines
    lines = []
    for i in range(1, 7):
        lines.append(('E', i))
    for i in range(1, 7):
        lines.append(('C', i))
    for i in range(1, 7):
        for j in range(i+1, 7):
            lines.append(('L', i, j))

    def intersect(L1, L2):
        if L1 == L2:
            return False
        t1, t2 = L1[0], L2[0]
        if t1 == 'E' and t2 == 'E':
            return False
        if t1 == 'C' and t2 == 'C':
            return False
        if t1 == 'E' and t2 == 'C':
            return L1[1] != L2[1]
        if t1 == 'C' and t2 == 'E':
            return L1[1] != L2[1]
        if t1 == 'E' and t2 == 'L':
            return L1[1] in L2[1:]
        if t1 == 'L' and t2 == 'E':
            return L2[1] in L1[1:]
        if t1 == 'C' and t2 == 'L':
            return L1[1] in L2[1:]
        if t1 == 'L' and t2 == 'C':
            return L2[1] in L1[1:]
        if t1 == 'L' and t2 == 'L':
            return len(set(L1[1:]) & set(L2[1:])) == 0
        return False

    n = len(lines)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if intersect(lines[i], lines[j]):
                adj[i, j] = adj[j, i] = 1
    comp = np.ones_like(adj) - np.eye(n, dtype=int) - adj
    return adj, comp


def seidel_spectrum(adj):
    n = adj.shape[0]
    J = np.ones((n, n), dtype=int)
    S = J - np.eye(n, dtype=int) - 2 * adj
    eigs = np.linalg.eigvalsh(S)
    return [round(float(x), 6) for x in eigs]


def triangle_count(adj):
    A = adj.astype(int)
    return int(np.trace(A @ A @ A) // 6)


def main():
    bal_adj = balanced_root_graph()
    sch_adj, sch_comp = build_schlafli_graphs()

    bal_seidel = seidel_spectrum(bal_adj)
    sch_seidel = seidel_spectrum(sch_comp)

    results = {
        "balanced_degree": int(bal_adj.sum(axis=1)[0]),
        "schlafli_degree": int(sch_comp.sum(axis=1)[0]),
        "balanced_triangles": triangle_count(bal_adj),
        "schlafli_triangles": triangle_count(sch_comp),
        "balanced_seidel_spectrum": Counter(bal_seidel),
        "schlafli_seidel_spectrum": Counter(sch_seidel),
        "seidel_match": Counter(bal_seidel) == Counter(sch_seidel),
    }

    out_path = ROOT / 'artifacts' / 'balanced_vs_schlafli.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
