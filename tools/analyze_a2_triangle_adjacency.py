#!/usr/bin/env python3
"""Compute adjacency matrix between the 9 Schläfli triangles (line intersection counts)."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


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


def lines_intersect(L1, L2):
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
        s1 = set(L1[1:])
        s2 = set(L2[1:])
        return len(s1 & s2) == 0

    return False


def main():
    tri_data = json.loads((ROOT / 'artifacts' / 'h27_schlafli_leftover_cycles.json').read_text())
    triangles = [[tuple(x) for x in tri] for tri in tri_data['cycle_labels']]

    # compute adjacency counts between triangles
    n = len(triangles)
    counts = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            cnt = 0
            for a in triangles[i]:
                for b in triangles[j]:
                    if lines_intersect(a, b):
                        cnt += 1
            counts[i][j] = cnt

    # summarize row patterns
    row_patterns = [tuple(counts[i]) for i in range(n)]
    pattern_counts = defaultdict(int)
    for p in row_patterns:
        pattern_counts[p] += 1

    results = {
        'triangle_adjacency_counts': counts,
        'row_pattern_counts': {str(k): v for k, v in pattern_counts.items()},
        'triangles': triangles,
    }

    out_path = ROOT / 'artifacts' / 'a2_triangle_adjacency.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print('row pattern counts:', pattern_counts)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
