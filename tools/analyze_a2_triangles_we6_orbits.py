#!/usr/bin/env python3
"""Analyze Schläfli A2 triangles against W(E6) orbit decomposition.

For each triangle (3 Schläfli lines), compute the sum of their Coxeter-6
intersection vectors with the 13 W(E6) orbits (72 + 6x27 + 6x1).
This yields a 13-vector totaling 18 roots per triangle (3 lines x 6 roots).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def load_json(name):
    return json.loads((ROOT / 'artifacts' / name).read_text(encoding='utf-8'))


def main():
    # line -> coxeter orbit map
    a2 = load_json('a2_triangles_vs_coxeter_patterns.json')
    line_to_orbit = {eval(k): v for k, v in a2['line_to_orbit'].items()}

    # triangles
    tri_data = load_json('h27_schlafli_leftover_cycles.json')
    triangles = [[tuple(x) for x in tri] for tri in tri_data['cycle_labels']]

    # W(E6) intersection matrix (40 x 13)
    inter = load_json('we6_coxeter6_intersection.json')
    matrix = inter['matrix']  # rows = coxeter orbits, cols = WE6 orbits
    we6_sizes = inter['we6_orbit_sizes']

    # label columns: 0=72, 1..6=27-orbits, 7..12=1-orbits
    col_labels = ['72'] + [f'27_{i}' for i in range(1,7)] + [f'1_{i}' for i in range(1,7)]

    tri_vectors = []
    for tri in triangles:
        vec = [0]*13
        for line in tri:
            o = line_to_orbit[line]
            row = matrix[o]
            vec = [vec[i] + row[i] for i in range(13)]
        tri_vectors.append(vec)

    # summarize unique vectors
    vec_counts = Counter(tuple(v) for v in tri_vectors)

    # also summarize totals over 72 / 27s / 1s
    tri_summaries = []
    for vec in tri_vectors:
        total72 = vec[0]
        total27 = sum(vec[1:7])
        total1 = sum(vec[7:])
        tri_summaries.append((total72, total27, total1))

    summary_counts = Counter(tri_summaries)

    results = {
        'col_labels': col_labels,
        'triangle_vectors': tri_vectors,
        'vector_counts': {str(k): v for k, v in vec_counts.items()},
        'summary_counts': {str(k): v for k, v in summary_counts.items()},
    }

    out_path = ROOT / 'artifacts' / 'a2_triangles_we6_orbits.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')

    print('summary counts:', summary_counts)
    print('vector counts:', vec_counts)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
