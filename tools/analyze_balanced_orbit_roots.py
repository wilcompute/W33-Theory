#!/usr/bin/env python3
"""Analyze the 27 E8 roots corresponding to the balanced 27-edge orbit."""
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


def main():
    edges = build_w33_edges()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    bias = json.loads((ROOT / 'artifacts' / 'su3_phase_orbit_bias.json').read_text())
    balanced_orbit = None
    for k, v in bias['orbit_sums'].items():
        if v == {'0': 9, '1': 9, '2': 9} or v == {0: 9, 1: 9, 2: 9}:
            balanced_orbit = int(k.split('_')[1])
    if balanced_orbit is None:
        print("No balanced orbit found")
        return

    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}
    edge_map = json.loads((ROOT / 'artifacts' / 'explicit_bijection_decomposition.json').read_text())
    edge_to_root_idx = {int(k): v for k, v in edge_map['edge_to_root_index'].items()}
    root_coords = [tuple(r) for r in edge_map['root_coords']]

    # Collect 27 roots (scaled down by 2)
    roots = []
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info and info['orbit_size'] == 27 and info['orbit_id'] == balanced_orbit:
            roots.append(np.array([x / 2.0 for x in r], dtype=float))

    if len(roots) != 27:
        print("Unexpected root count:", len(roots))

    # Pairwise inner products
    ip_counts = Counter()
    for i, j in combinations(range(len(roots)), 2):
        ip = round(float(np.dot(roots[i], roots[j])), 6)
        ip_counts[ip] += 1

    # Build adjacency graph for ip = 1 (root neighbors)
    n = len(roots)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            ip = float(np.dot(roots[i], roots[j]))
            if abs(ip - 1.0) < 1e-6:
                adj[i, j] = adj[j, i] = 1
    degrees = Counter(int(x) for x in adj.sum(axis=1))

    # Common neighbor counts for adjacent vs non-adjacent pairs
    cn_adj = Counter()
    cn_non = Counter()
    for i in range(n):
        for j in range(i+1, n):
            cn = int(np.dot(adj[i], adj[j]))
            if adj[i, j] == 1:
                cn_adj[cn] += 1
            else:
                cn_non[cn] += 1

    # Count A2 triangles: triples with pairwise ip = -1
    a2_count = 0
    for i, j, k in combinations(range(n), 3):
        ip_ij = float(np.dot(roots[i], roots[j]))
        ip_ik = float(np.dot(roots[i], roots[k]))
        ip_jk = float(np.dot(roots[j], roots[k]))
        if abs(ip_ij + 1) < 1e-6 and abs(ip_ik + 1) < 1e-6 and abs(ip_jk + 1) < 1e-6:
            a2_count += 1

    results = {
        "balanced_orbit_id": balanced_orbit,
        "root_count": len(roots),
        "inner_product_counts": {str(k): v for k, v in sorted(ip_counts.items())},
        "root_neighbor_degree_distribution": dict(degrees),
        "common_neighbors_adjacent": {str(k): v for k, v in sorted(cn_adj.items())},
        "common_neighbors_nondjacent": {str(k): v for k, v in sorted(cn_non.items())},
        "a2_triangle_count": a2_count,
    }

    out_path = ROOT / 'artifacts' / 'balanced_orbit_roots.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
