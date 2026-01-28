#!/usr/bin/env python3
"""Construct an explicit SU(3)/A2 root mapping from Z3 phase assignment.

We use the canonical Z3 phase (x4 coordinate) on the 27 lines, induce a
phase on the 9 Schläfli triangles, and interpret the 3 phase classes as
A2 weights. We then build the A2 root system and map phases to weights.
"""
from __future__ import annotations

from collections import defaultdict, Counter
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

    adj = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i][j] = adj[j][i] = 1

    return adj, proj_points


def h27_from_w33(adj, v0=0):
    n = len(adj)
    non_neighbors = [j for j in range(n) if j != v0 and adj[v0][j] == 0]
    return non_neighbors


def build_27_lines():
    lines = []
    for i in range(1, 7):
        lines.append(('E', i))
    for i in range(1, 7):
        lines.append(('C', i))
    for i in range(1, 7):
        for j in range(i+1, 7):
            lines.append(('L', i, j))
    return lines


def main():
    # Load H27 embedding and triangle list
    tri_data = json.loads((ROOT / 'artifacts' / 'h27_schlafli_leftover_cycles.json').read_text())
    triangles = [[tuple(x) for x in tri] for tri in tri_data['cycle_labels']]

    embed = json.loads((ROOT / 'artifacts' / 'h27_in_schlafli_intersection.json').read_text())
    if not embed.get('found_embedding'):
        print('No H27 embedding found.')
        return
    h_to_s = {int(k): int(v) for k, v in embed['mapping'].items()}
    s_to_h = {v: k for k, v in h_to_s.items()}

    # Build W33 and map line -> W33 vertex coordinate
    adj, points = build_w33()
    nn = h27_from_w33(adj, v0=0)

    lines = build_27_lines()
    line_to_idx = {lines[i]: i for i in range(27)}

    line_to_point = {}
    for line, idx in line_to_idx.items():
        h_idx = s_to_h[idx]
        w33_idx = nn[h_idx]
        line_to_point[line] = points[w33_idx]

    # Canonical Z3 phase: x4 coordinate (index 3)
    line_phase = {line: (pt[3] % 3) for line, pt in line_to_point.items()}

    # Each triangle -> phase multiset
    tri_phase = []
    for tri in triangles:
        tri_phase.append(tuple(sorted(line_phase[tuple(t)] for t in tri)))

    phase_counts = Counter(tri_phase)

    # Define A2 weight mapping for phases 0,1,2
    # We use fundamental weights in 2D: w0=(1,0), w1=(-1,1), w2=(0,-1)
    # (sum to 0)
    weights = {
        0: (1, 0),
        1: (-1, 1),
        2: (0, -1),
    }

    # For each triangle, compute weight sum (should be 0 if rainbow)
    tri_weight_sums = []
    for tri in triangles:
        wsum = [0, 0]
        for t in tri:
            ph = line_phase[tuple(t)]
            w = weights[ph]
            wsum[0] += w[0]
            wsum[1] += w[1]
        tri_weight_sums.append(tuple(wsum))

    weight_sum_counts = Counter(tri_weight_sums)

    results = {
        'line_phase_counts': dict(Counter(line_phase.values())),
        'triangle_phase_multisets': {str(k): v for k, v in phase_counts.items()},
        'triangle_weight_sums': {str(k): v for k, v in weight_sum_counts.items()},
        'weights': weights,
        'line_phase': {str(k): v for k, v in line_phase.items()},
    }

    out_path = ROOT / 'artifacts' / 'su3_a2_root_mapping.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results['line_phase_counts'])
    print(results['triangle_phase_multisets'])
    print(results['triangle_weight_sums'])
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
