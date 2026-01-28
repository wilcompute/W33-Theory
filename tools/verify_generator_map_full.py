#!/usr/bin/env python3
"""Full verification of Sp(4,3) generator map on E8 roots.

Checks for each generator:
- Gram matrix invariance: G[p][:,p] == G
- W(E6) orbit-size preservation (72 / 27 / 1)

Outputs: artifacts/sp43_we6_generator_map_full_verify.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def build_e8_roots():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (1, -1):
                for sj in (1, -1):
                    r = [0.0] * 8
                    r[i] = float(si)
                    r[j] = float(sj)
                    roots.append(tuple(r))
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(0.5 * s for s in signs))
    return roots


def main():
    data = json.loads((ROOT / 'artifacts' / 'sp43_we6_generator_map.json').read_text())
    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}

    roots = build_e8_roots()
    R = np.array(roots, dtype=float)
    G = R @ R.T

    # orbit sizes for E8 roots in this ordering
    orbit_sizes = []
    for r in roots:
        key = tuple(int(2 * x) for x in r)
        info = root_to_orbit.get(key)
        orbit_sizes.append(info['orbit_size'] if info else None)

    results = []
    for gen in data['generator_maps']:
        perm = gen['root_perm']
        perm = np.array(perm, dtype=int)

        Gp = G[np.ix_(perm, perm)]
        gram_ok = np.array_equal(G, Gp)

        orbit_ok = True
        for i, j in enumerate(perm):
            if orbit_sizes[i] != orbit_sizes[j]:
                orbit_ok = False
                break

        results.append({
            'gen_index': gen['gen_index'],
            'gram_invariant': bool(gram_ok),
            'orbit_size_invariant': bool(orbit_ok),
        })

    out = {
        'generator_checks': results,
        'all_gram_ok': all(r['gram_invariant'] for r in results),
        'all_orbit_ok': all(r['orbit_size_invariant'] for r in results),
    }

    out_path = ROOT / 'artifacts' / 'sp43_we6_generator_map_full_verify.json'
    out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
