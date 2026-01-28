#!/usr/bin/env python3
"""Construct the signed line action (central extension) and compute its order.

We use line permutation + sign cocycle (eps) to define permutations on
120*2 oriented line elements. This yields a concrete central extension of the
line action by Z2.
"""
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

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


def perm_compose(a, b):
    return [a[i] for i in b]


def bfs_group(gens, max_size=600000):
    n = len(gens[0])
    idp = list(range(n))
    seen = {tuple(idp)}
    q = deque([idp])
    while q:
        cur = q.popleft()
        for g in gens:
            nxt = perm_compose(g, cur)
            t = tuple(nxt)
            if t not in seen:
                seen.add(t)
                if len(seen) > max_size:
                    return None
                q.append(nxt)
    return len(seen)


def main():
    roots = build_e8_roots()
    root_to_idx = {r: i for i, r in enumerate(roots)}

    # Build root lines and canonical reps
    line_id = [-1] * len(roots)
    line_reps = []
    for i, r in enumerate(roots):
        if line_id[i] != -1:
            continue
        j = root_to_idx[tuple(-x for x in r)]
        lid = len(line_reps)
        line_id[i] = lid
        line_id[j] = lid
        rep = i if i < j else j
        line_reps.append(rep)

    # Load generator perms on roots
    data = json.loads((ROOT / 'artifacts' / 'sp43_we6_generator_map.json').read_text())
    gens = [g['root_perm'] for g in data['generator_maps']]

    # Build signed line permutations
    signed_gens = []
    for g in gens:
        perm = [0] * (len(line_reps) * 2)
        for lid, rep in enumerate(line_reps):
            img = g[rep]
            lid2 = line_id[img]
            rep2 = line_reps[lid2]
            eps = 1 if img == rep2 else -1
            for sign in (1, -1):
                idx = 2 * lid + (0 if sign == 1 else 1)
                sign2 = sign * eps
                idx2 = 2 * lid2 + (0 if sign2 == 1 else 1)
                perm[idx] = idx2
        signed_gens.append(perm)

    order = bfs_group(signed_gens, max_size=600000)

    # global flip
    flip = []
    for lid in range(len(line_reps)):
        flip.append(2 * lid + 1)
        flip.append(2 * lid)

    gens_plus = signed_gens + [flip]
    order_plus = bfs_group(gens_plus, max_size=600000)

    out = {
        "signed_group_order": order,
        "order_with_flip": order_plus,
        "line_count": len(line_reps),
        "state_count": len(line_reps) * 2,
        "max_size": 600000,
    }
    out_path = ROOT / 'artifacts' / 'signed_line_extension.json'
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
