#!/usr/bin/env python3
"""Exhaustive search over S6 and E<->C swap for triangle pattern homogenization.

Checks all 6! * 2 = 1440 automorphisms from permuting indices 1..6 and
optionally swapping E<->C, to see if triangle class patterns can be made
more homogeneous.
"""
from __future__ import annotations

from collections import Counter
from itertools import permutations
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


def load_triangles():
    tri_data = json.loads((ROOT / 'artifacts' / 'h27_schlafli_leftover_cycles.json').read_text())
    triangles = [[tuple(x) for x in tri] for tri in tri_data['cycle_labels']]
    return triangles


def load_line_to_class():
    a2 = json.loads((ROOT / 'artifacts' / 'a2_triangles_vs_coxeter_patterns.json').read_text())
    line_to_class = {eval(k): v for k, v in a2['line_to_class'].items()}
    return line_to_class


def triangle_pattern(tri, line_to_class):
    return tuple(sorted(line_to_class[tuple(t)] for t in tri))


def apply_perm_to_line(line, perm, swap_ec=False):
    t = line[0]
    if t == 'E':
        t2 = 'C' if swap_ec else 'E'
        return (t2, perm[line[1]-1] + 1)
    if t == 'C':
        t2 = 'E' if swap_ec else 'C'
        return (t2, perm[line[1]-1] + 1)
    i, j = line[1], line[2]
    i2 = perm[i-1] + 1
    j2 = perm[j-1] + 1
    if i2 > j2:
        i2, j2 = j2, i2
    return ('L', i2, j2)


def apply_perm_to_triangle(tri, perm, swap_ec=False):
    return [apply_perm_to_line(line, perm, swap_ec) for line in tri]


def main():
    lines = build_27_lines()
    triangles = load_triangles()
    line_to_class = load_line_to_class()

    base_patterns = [triangle_pattern(tri, line_to_class) for tri in triangles]
    base_counts = Counter(base_patterns)

    best_count = len(base_counts)
    best_configs = []

    for perm in permutations(range(6)):
        for swap_ec in (False, True):
            line_to_class_perm = {}
            for line in lines:
                line_p = apply_perm_to_line(line, perm, swap_ec)
                line_to_class_perm[line_p] = line_to_class[line]

            patterns = []
            for tri in triangles:
                tri_p = apply_perm_to_triangle(tri, perm, swap_ec)
                patterns.append(triangle_pattern(tri_p, line_to_class_perm))

            counts = Counter(patterns)
            if len(counts) < best_count:
                best_count = len(counts)
                best_configs = [((perm, swap_ec), counts)]
            elif len(counts) == best_count:
                best_configs.append(((perm, swap_ec), counts))

    results = {
        'base_pattern_counts': {str(k): v for k, v in base_counts.items()},
        'best_pattern_count': best_count,
        'best_configs_count': len(best_configs),
        'best_configs_sample': [
            {
                'perm': cfg[0][0],
                'swap_ec': cfg[0][1],
                'pattern_counts': {str(k): v for k, v in cfg[1].items()},
            }
            for cfg in best_configs[:5]
        ],
    }

    out_path = ROOT / 'artifacts' / 'triangle_relabeling_search_exhaustive.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
