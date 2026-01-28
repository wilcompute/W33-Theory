#!/usr/bin/env python3
"""Analyze structure of linear functionals c producing rainbow triangles.

Determines whether the solution set (canonicalized c in F3^4) forms
an affine subspace; finds linear constraints if any.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def mod3(x):
    return x % 3


def canonical_c(c):
    # scale so first nonzero entry is 1
    if c == (0,0,0,0):
        return c
    for i, v in enumerate(c):
        if v != 0:
            inv = 1 if v == 1 else 2  # inverse of 2 mod3 is 2
            return tuple((inv * x) % 3 for x in c)
    return c


def solve_linear_constraints(S):
    # Find linear relations a·c = 0 for all c in S over F3
    # brute force all a in F3^4
    rels = []
    for a in product([0,1,2], repeat=4):
        if a == (0,0,0,0):
            continue
        ok = True
        for c in S:
            val = sum(a[i]*c[i] for i in range(4)) % 3
            if val != 0:
                ok = False
                break
        if ok:
            rels.append(a)
    return rels


def main():
    data = json.loads((ROOT / 'artifacts' / 'z3_phase_linear_search.json').read_text())
    sols = data['solutions']

    # collect c vectors (canonicalized)
    c_set = set()
    for s in sols:
        c = tuple(s['c'])
        c_set.add(canonical_c(c))

    c_list = sorted(c_set)

    # check if size is 27
    size = len(c_list)

    # compute linear relations
    rels = solve_linear_constraints(c_list)

    results = {
        'num_canonical_c': size,
        'canonical_c': c_list,
        'linear_relations': rels,
        'num_relations': len(rels),
    }

    out_path = ROOT / 'artifacts' / 'z3_phase_linear_analysis.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
