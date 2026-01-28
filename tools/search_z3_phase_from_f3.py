#!/usr/bin/env python3
"""Search for Z3 phase assignments from F3^4 linear functionals.

We test linear (and affine) functionals f(x)=c·x + b (mod 3) on the 27 H27
vertices (non-neighbors of v0). Using the H27->Schläfli embedding, we check
if each of the 9 Schläfli triangles is rainbow (0,1,2).
"""
from __future__ import annotations

from itertools import product
from collections import Counter
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
    # Load triangle list and embedding
    tri_data = json.loads((ROOT / 'artifacts' / 'h27_schlafli_leftover_cycles.json').read_text())
    triangles = [[tuple(x) for x in tri] for tri in tri_data['cycle_labels']]

    embed = json.loads((ROOT / 'artifacts' / 'h27_in_schlafli_intersection.json').read_text())
    if not embed.get('found_embedding'):
        print('No embedding found.')
        return
    h_to_s = {int(k): int(v) for k, v in embed['mapping'].items()}
    s_to_h = {v: k for k, v in h_to_s.items()}

    lines = build_27_lines()
    line_to_idx = {lines[i]: i for i in range(27)}

    # W33 structure
    adj, points = build_w33()
    nn = h27_from_w33(adj, v0=0)  # H27 index -> W33 vertex index

    # Map each line to its W33 vertex coordinates
    line_to_point = {}
    for line, idx in line_to_idx.items():
        h_idx = s_to_h[idx]
        w33_idx = nn[h_idx]
        line_to_point[line] = points[w33_idx]

    # Precompute triangle line points
    tri_points = []
    for tri in triangles:
        tri_points.append([line_to_point[tuple(t)] for t in tri])

    solutions = []
    counts = []
    F3 = [0, 1, 2]
    # test linear and affine functionals
    for c in product(F3, repeat=4):
        if c == (0,0,0,0):
            continue
        for b in F3:
            ok = True
            for tri in tri_points:
                colors = [ (c[0]*p[0] + c[1]*p[1] + c[2]*p[2] + c[3]*p[3] + b) % 3 for p in tri]
                if set(colors) != {0,1,2}:
                    ok = False
                    break
            if ok:
                # color counts
                color_counts = [0, 0, 0]
                for p in [line_to_point[line] for line in line_to_point]:
                    col = (c[0]*p[0] + c[1]*p[1] + c[2]*p[2] + c[3]*p[3] + b) % 3
                    color_counts[col] += 1
                solutions.append({'c': c, 'b': b, 'color_counts': color_counts})

    # classify c up to scalar
    def normalize_c(cvec):
        if cvec == (0,0,0,0):
            return cvec
        # use smallest scalar among {1,2} to canonicalize
        c1 = cvec
        c2 = tuple((2*x) % 3 for x in cvec)
        return min(c1, c2)

    class_counts = Counter()
    b_counts = Counter()
    for sol in solutions:
        cn = normalize_c(sol['c'])
        class_counts[cn] += 1
        b_counts[sol['b']] += 1

    results = {
        'num_solutions_found': len(solutions),
        'num_c_classes': len(class_counts),
        'c_class_counts': {str(k): v for k, v in class_counts.items()},
        'b_counts': dict(b_counts),
        'solutions': solutions,
    }

    out_path = ROOT / 'artifacts' / 'z3_phase_linear_search.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
