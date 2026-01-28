#!/usr/bin/env python3
"""Extend generator set to full W(E6) action on E8 roots (size 51840).

We add the central sign flip (r -> -r) to the PSp(4,3) generator images
and verify the group order doubles to 51840.

Outputs:
- artifacts/sp43_we6_generator_map_full_we6.json
- artifacts/sp43_we6_generator_map_full_we6_verify.json
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
    roots = build_e8_roots()
    n = len(roots)

    # central sign flip permutation
    root_to_idx = {r: i for i, r in enumerate(roots)}
    flip_perm = [root_to_idx[tuple(-x for x in r)] for r in roots]

    full_generators = []
    for g in data['generator_maps']:
        full_generators.append(g['root_perm'])
    full_generators.append(flip_perm)

    out = {
        'generator_count': len(full_generators),
        'generators': full_generators,
    }
    out_path = ROOT / 'artifacts' / 'sp43_we6_generator_map_full_we6.json'
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")

    # Verify group order via Sage (libgap)
    try:
        from sage.libs.gap.libgap import libgap
        gap_perms = [libgap.PermList([x + 1 for x in perm]) for perm in full_generators]
        G = libgap.Group(gap_perms)
        order = int(libgap.Order(G))
    except Exception as e:
        order = None
        err = str(e)
    else:
        err = None

    verify = {
        'order': order,
        'error': err,
    }
    verify_path = ROOT / 'artifacts' / 'sp43_we6_generator_map_full_we6_verify.json'
    verify_path.write_text(json.dumps(verify, indent=2))
    print(f"Wrote {verify_path}")


if __name__ == '__main__':
    main()
