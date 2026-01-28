#!/usr/bin/env python3
"""Analyze geometry of the balanced 27-orbit (by SU(3) phase)."""
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

    adj = [[0]*n for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
                edges.append((i, j))

    return proj_points, adj, edges


def main():
    # Load orbit bias
    bias = json.loads((ROOT / 'artifacts' / 'su3_phase_orbit_bias.json').read_text())
    balanced_orbit = None
    for k, v in bias['orbit_sums'].items():
        if v == {'0': 9, '1': 9, '2': 9} or v == {0:9,1:9,2:9}:
            balanced_orbit = int(k.split('_')[1])
    if balanced_orbit is None:
        print('No balanced orbit found')
        return

    # Load W(E6) root->orbit labels
    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}

    # Load explicit edge map and edge list
    edge_map = json.loads((ROOT / 'artifacts' / 'explicit_bijection_decomposition.json').read_text())
    edge_to_root_idx = {int(k): v for k, v in edge_map['edge_to_root_index'].items()}
    root_coords = [tuple(r) for r in edge_map['root_coords']]

    points, adj, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    # Identify edges in balanced orbit
    edges_balanced = []
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info and info['orbit_size'] == 27 and info['orbit_id'] == balanced_orbit:
            edges_balanced.append(e)

    # Vertex incidence
    vertex_counts = Counter()
    for i, j in edges_balanced:
        vertex_counts[i] += 1
        vertex_counts[j] += 1

    # Support-size distribution of vertices touched
    support_sizes = Counter()
    for v, count in vertex_counts.items():
        nz = sum(1 for x in points[v] if x != 0)
        support_sizes[nz] += 1

    # Are balanced edges mostly within H27 or cross? compute incidence relative to v0=0
    v0 = 0
    H12 = {j for j in range(40) if adj[v0][j] == 1}
    H27 = {j for j in range(40) if j != v0 and adj[v0][j] == 0}

    partition_counts = Counter()
    for i, j in edges_balanced:
        if i in H27 and j in H27:
            partition_counts['H27-H27'] += 1
        elif (i in H12 and j in H27) or (i in H27 and j in H12):
            partition_counts['H12-H27'] += 1
        elif i in H12 and j in H12:
            partition_counts['H12-H12'] += 1
        elif i == v0 or j == v0:
            partition_counts['v0'] += 1
        else:
            partition_counts['other'] += 1

    results = {
        'balanced_orbit_id': balanced_orbit,
        'balanced_edge_count': len(edges_balanced),
        'vertex_incidence_hist': dict(vertex_counts),
        'support_size_distribution': dict(support_sizes),
        'partition_counts': dict(partition_counts),
    }

    out_path = ROOT / 'artifacts' / 'balanced_orbit_geometry.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
