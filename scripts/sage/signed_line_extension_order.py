#!/usr/bin/env sage
"""Compute order of signed line action using Sage permutation groups."""
from __future__ import annotations

import json
from sage.all import Permutation, PermutationGroup


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
    roots = build_e8_roots()
    root_to_idx = {r: i for i, r in enumerate(roots)}

    # lines
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

    data = json.loads(open('artifacts/sp43_we6_generator_map.json').read())
    gens = [g['root_perm'] for g in data['generator_maps']]

    signed_perms = []
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
        # convert to 1-based
        signed_perms.append([x + 1 for x in perm])

    G = PermutationGroup([Permutation(p) for p in signed_perms])
    print(f"Signed line extension order: {G.order()}")

    # global flip
    flip = []
    for lid in range(len(line_reps)):
        flip.append(2 * lid + 2)  # 1-based index for (line,+)->(line,-)
        flip.append(2 * lid + 1)  # (line,-)->(line,+)
    G2 = PermutationGroup([Permutation(p) for p in signed_perms + [flip]])
    print(f"With global flip order: {G2.order()}")

    out = {
        "signed_order": int(G.order()),
        "with_flip_order": int(G2.order()),
    }
    with open('artifacts/signed_line_extension_order.json', 'w') as f:
        json.dump(out, f, indent=2)
    print("Wrote artifacts/signed_line_extension_order.json")


if __name__ == '__main__':
    main()
