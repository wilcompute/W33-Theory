#!/usr/bin/env python3
"""Compute the Z2 cocycle induced by generator action on root lines.

Given root permutations (from edge->root mapping), define eps(L,g)=+1 if g maps
line representative to line representative, else -1. Then the cocycle is
c(L,g,h)=eps(L,g)*eps(gL,h)/eps(L,gh). Nontriviality witnesses the sign-lift
obstruction.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
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

    # Load generator perms
    data = json.loads((ROOT / "artifacts" / "sp43_we6_generator_map.json").read_text())
    gens = [g["root_perm"] for g in data["generator_maps"]]

    # Precompute line permutation and eps for each generator
    gen_line_perm = []
    gen_eps = []  # list of arrays eps[line]

    for g in gens:
        perm = [0] * len(line_reps)
        eps = [1] * len(line_reps)
        for lid, rep in enumerate(line_reps):
            img = g[rep]
            lid2 = line_id[img]
            perm[lid] = lid2
            rep2 = line_reps[lid2]
            eps[lid] = 1 if img == rep2 else -1
        gen_line_perm.append(perm)
        gen_eps.append(eps)

    # Compose perms
    def compose_perm(a, b):
        return [a[i] for i in b]

    # Compose root perms too
    def compose_root_perm(a, b):
        return [a[i] for i in b]

    # Compute cocycle values
    cocycle_counts = Counter()
    cocycle_pairs = []

    for gi, g in enumerate(gens):
        for hj, h in enumerate(gens):
            gh = compose_root_perm(g, h)
            # compute eps for gh on each line
            eps_gh = [1] * len(line_reps)
            for lid, rep in enumerate(line_reps):
                img = gh[rep]
                lid2 = line_id[img]
                rep2 = line_reps[lid2]
                eps_gh[lid] = 1 if img == rep2 else -1

            # cocycle per line
            neg_lines = []
            for lid in range(len(line_reps)):
                lid_g = gen_line_perm[gi][lid]
                c = (
                    gen_eps[gi][lid]
                    * gen_eps[hj][lid_g]
                    * (1 if eps_gh[lid] == 1 else -1)
                )
                if c == -1:
                    neg_lines.append(lid)
            cocycle_counts[len(neg_lines)] += 1
            if neg_lines:
                cocycle_pairs.append(
                    {
                        "g": gi,
                        "h": hj,
                        "neg_lines": neg_lines[:10],
                        "neg_count": len(neg_lines),
                    }
                )

    # Summarize
    out = {
        "num_generators": len(gens),
        "line_count": len(line_reps),
        "cocycle_neg_line_hist": dict(cocycle_counts),
        "sample_nontrivial_pairs": cocycle_pairs[:20],
    }
    out_path = ROOT / "artifacts" / "root_line_sign_cocycle_stats.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
