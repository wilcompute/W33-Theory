#!/usr/bin/env python3
"""Align the 9 Schläfli A2 triangles with Coxeter-6 pattern classes.

Pipeline:
1) Load H27->Schläfli embedding and triangle list (line labels).
2) Build Schläfli line index order and invert embedding.
3) Build W33 vertex list (non-neighbors of v0) to map H27 index -> W33 vertex index.
4) Load Coxeter orbit -> W33 vertex map and invert to W33 vertex -> orbit.
5) Load pattern classes (8 classes) and map orbit -> class.
6) For each triangle, compute the pattern-class triple.
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
    # Load triangles (labels)
    tri_data = json.loads((ROOT / 'artifacts' / 'h27_schlafli_leftover_cycles.json').read_text())
    triangles = tri_data['cycle_labels']

    # Load embedding H27 index -> Schläfli index
    embed = json.loads((ROOT / 'artifacts' / 'h27_in_schlafli_intersection.json').read_text())
    if not embed.get('found_embedding'):
        print('No embedding found in artifact.')
        return
    h_to_s = {int(k): int(v) for k, v in embed['mapping'].items()}
    s_to_h = {v: k for k, v in h_to_s.items()}

    # Build Schläfli line index map
    lines = build_27_lines()
    line_to_idx = {lines[i]: i for i in range(len(lines))}

    # Build W33 non-neighbors of vertex 0
    adj, _ = build_w33()
    nn = h27_from_w33(adj, v0=0)  # list of W33 vertex indices for H27 order

    # Load Coxeter orbit -> W33 vertex mapping
    orb_map = json.loads((ROOT / 'artifacts' / 'e8_root_to_w33_edge.json').read_text())
    orbit_to_w33 = {int(k): int(v) for k, v in orb_map['orbit_to_w33_vertex'].items()}
    w33_to_orbit = {v: k for k, v in orbit_to_w33.items()}

    # Load pattern classes (orbit -> class)
    patt = json.loads((ROOT / 'artifacts' / 'vertex_type_vs_we6_pattern.json').read_text())
    orbit_to_class = {}
    for cls_idx, entry in enumerate(patt['patterns']):
        for o in entry['orbits']:
            orbit_to_class[o] = cls_idx

    # Map each Schläfli line to pattern class via H27->W33->orbit
    line_to_class = {}
    line_to_orbit = {}
    line_to_w33 = {}
    for line, idx in line_to_idx.items():
        h_idx = s_to_h[idx]
        w33_idx = nn[h_idx]
        orbit = w33_to_orbit[w33_idx]
        cls = orbit_to_class[orbit]
        line_to_class[line] = cls
        line_to_orbit[line] = orbit
        line_to_w33[line] = w33_idx

    # Analyze triangles
    tri_class_patterns = []
    for tri in triangles:
        classes = [line_to_class[tuple(t)] for t in tri]
        tri_class_patterns.append(tuple(sorted(classes)))

    tri_pattern_counts = Counter(tri_class_patterns)

    # Group triangles by pattern
    pattern_to_tris = defaultdict(list)
    for tri, pat in zip(triangles, tri_class_patterns):
        pattern_to_tris[tuple(sorted(pat))].append(tri)

    results = {
        'triangle_class_pattern_counts': {str(k): v for k, v in tri_pattern_counts.items()},
        'pattern_to_triangles': {str(k): v for k, v in pattern_to_tris.items()},
        'line_to_class': {str(k): v for k, v in line_to_class.items()},
        'line_to_orbit': {str(k): v for k, v in line_to_orbit.items()},
        'line_to_w33_vertex': {str(k): v for k, v in line_to_w33.items()},
    }

    out_path = ROOT / 'artifacts' / 'a2_triangles_vs_coxeter_patterns.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results['triangle_class_pattern_counts'])
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
