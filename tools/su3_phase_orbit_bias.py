#!/usr/bin/env python3
"""Analyze SU(3) phase bias per W(E6) 27-orbit.

For each 27-orbit (size=27) in W(E6) acting on E8 roots, compute
phase-pair distributions of W33 edges that map into that orbit.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
import json

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

    n = len(proj_points)

    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def main():
    # Load edge->root map and root->orbit labels
    edge_map = json.loads((ROOT / 'artifacts' / 'explicit_bijection_decomposition.json').read_text())
    edge_to_root_idx = {int(k): v for k, v in edge_map['edge_to_root_index'].items()}
    root_coords = [tuple(r) for r in edge_map['root_coords']]

    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}

    # W33 points and edges
    points, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    v_phase = {i: points[i][3] % 3 for i in range(len(points))}

    # per orbit statistics
    orbit_pairs = defaultdict(lambda: Counter())
    orbit_sums = defaultdict(lambda: Counter())

    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info is None:
            continue
        orbit_id = info['orbit_id']
        orbit_size = info['orbit_size']
        if orbit_size != 27:
            continue
        key = f"27_{orbit_id}"

        a, b = v_phase[e[0]], v_phase[e[1]]
        pair = tuple(sorted((a, b)))
        orbit_pairs[key][pair] += 1
        orbit_sums[key][(a + b) % 3] += 1

    results = {
        'orbit_pairs': {k: {str(p): v for p, v in cnt.items()} for k, cnt in orbit_pairs.items()},
        'orbit_sums': {k: {str(s): v for s, v in cnt.items()} for k, cnt in orbit_sums.items()},
    }

    out_path = ROOT / 'artifacts' / 'su3_phase_orbit_bias.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print({k: dict(v) for k, v in orbit_sums.items()})
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
