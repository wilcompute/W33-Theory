#!/usr/bin/env python3
"""Signed line extension for true W(E6) action (Sage ordering)."""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def perm_compose(a, b):
    return [a[i] for i in b]


def bfs_group(gens, max_size=200000):
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
    we6 = json.loads((ROOT / "artifacts" / "we6_true_action.json").read_text())
    roots = [tuple(r) for r in we6["roots_int2"]]
    root_to_idx = {r: i for i, r in enumerate(roots)}

    # build root lines using integer coordinates
    line_id = [-1] * len(roots)
    line_reps = []
    for i, r in enumerate(roots):
        if line_id[i] != -1:
            continue
        neg = tuple(-x for x in r)
        j = root_to_idx[neg]
        lid = len(line_reps)
        line_id[i] = lid
        line_id[j] = lid
        rep = i if i < j else j
        line_reps.append(rep)

    gens = we6["we6_even_generators"]  # 1-based perms
    gens0 = [[x - 1 for x in p] for p in gens]

    # verify antipodal preservation
    ok = True
    for g in gens0:
        for i, r in enumerate(roots):
            j = root_to_idx[tuple(-x for x in r)]
            s = g[i]
            sj = g[j]
            expected = root_to_idx[tuple(-x for x in roots[s])]
            if sj != expected:
                ok = False
                break
        if not ok:
            break
    print(f"Antipodal preserved for all gens: {ok}")

    # build signed perms
    signed_gens = []
    for g in gens0:
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
        if len(set(perm)) != len(perm):
            raise RuntimeError("Signed perm not bijective")
        signed_gens.append(perm)

    order = bfs_group(signed_gens, max_size=200000)

    flip = []
    for lid in range(len(line_reps)):
        flip.append(2 * lid + 1)
        flip.append(2 * lid)

    order_plus = bfs_group(signed_gens + [flip], max_size=400000)

    out = {
        "signed_group_order": order,
        "order_with_flip": order_plus,
        "line_count": len(line_reps),
        "state_count": len(line_reps) * 2,
        "antipodal_preserved": ok,
    }
    out_path = ROOT / "artifacts" / "signed_line_extension_we6_true.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
