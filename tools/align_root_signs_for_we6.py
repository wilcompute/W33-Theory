#!/usr/bin/env python3
"""Align root sign choices so generator permutations commute with sign flip.

We solve for a sign assignment on the 120 root lines so that each generator
maps line representatives to line representatives (no sign ambiguity).

Outputs:
- artifacts/root_line_sign_assignment.json
- artifacts/sp43_we6_generator_map_aligned.json
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


def main():
    roots = build_e8_roots()
    root_to_idx = {r: i for i, r in enumerate(roots)}

    # Build line mapping: line_id for each root
    line_id = [-1] * len(roots)
    line_reps = []  # representative index for each line
    for i, r in enumerate(roots):
        if line_id[i] != -1:
            continue
        j = root_to_idx[tuple(-x for x in r)]
        lid = len(line_reps)
        line_id[i] = lid
        line_id[j] = lid
        # choose canonical rep as smaller index
        rep = i if i < j else j
        line_reps.append(rep)

    # Load generator perms
    data = json.loads((ROOT / "artifacts" / "sp43_we6_generator_map.json").read_text())
    gens = [g["root_perm"] for g in data["generator_maps"]]

    # Build constraints: sigma(line') = eps * sigma(line)
    # where eps = +1 if g maps rep(line) to rep(line'), else -1
    constraints = []
    for g in gens:
        for lid, rep in enumerate(line_reps):
            img = g[rep]
            lid2 = line_id[img]
            rep2 = line_reps[lid2]
            eps = 1 if img == rep2 else -1
            constraints.append((lid, lid2, eps))

    # Solve via BFS
    sigma = [None] * len(line_reps)
    for start in range(len(line_reps)):
        if sigma[start] is not None:
            continue
        sigma[start] = 1
        q = deque([start])
        while q:
            u = q.popleft()
            for a, b, eps in constraints:
                if a != u:
                    continue
                if sigma[b] is None:
                    sigma[b] = eps * sigma[a]
                    q.append(b)
                else:
                    if sigma[b] != eps * sigma[a]:
                        print("Inconsistency detected")
                        out = {
                            "status": "inconsistent",
                        }
                        (
                            ROOT / "artifacts" / "root_line_sign_assignment.json"
                        ).write_text(json.dumps(out, indent=2))
                        return

    # Build relabeling permutation P on 240 roots: swap reps on lines with sigma=-1
    P = list(range(len(roots)))
    for lid, rep in enumerate(line_reps):
        if sigma[lid] == -1:
            other = root_to_idx[tuple(-x for x in roots[rep])]
            P[rep], P[other] = P[other], P[rep]

    # Conjugate generators by P
    def apply_perm(perm, idx_map):
        return [idx_map[perm[i]] for i in range(len(perm))]

    # Build inverse of P
    Pinv = [0] * len(P)
    for i, v in enumerate(P):
        Pinv[v] = i

    aligned = []
    for g in gens:
        # P^{-1} g P
        gp = [g[P[i]] for i in range(len(g))]
        g_aligned = [Pinv[x] for x in gp]
        aligned.append(g_aligned)

    out = {
        "status": "ok",
        "line_signs": sigma,
        "relabel_perm": P,
        "aligned_generators": aligned,
    }
    (ROOT / "artifacts" / "root_line_sign_assignment.json").write_text(
        json.dumps(out, indent=2)
    )
    (ROOT / "artifacts" / "sp43_we6_generator_map_aligned.json").write_text(
        json.dumps(out, indent=2)
    )
    print("Wrote artifacts/root_line_sign_assignment.json")
    print("Wrote artifacts/sp43_we6_generator_map_aligned.json")


if __name__ == "__main__":
    main()
