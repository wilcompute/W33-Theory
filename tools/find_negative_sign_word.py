#!/usr/bin/env python3
"""Find a shortest word in generators that returns a line to itself with sign -1.

We model states as (line_id, sign). If a path exists from (L,+1) to (L,-1),
that yields an explicit cocycle witness (a relation whose sign is -1).
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
    data = json.loads((ROOT / 'artifacts' / 'sp43_we6_generator_map.json').read_text())
    gens = [g['root_perm'] for g in data['generator_maps']]

    # Precompute line permutation and eps for each generator
    gen_line_perm = []
    gen_eps = []
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

    # BFS in state space (line, sign)
    start = (0, 1)
    target = (0, -1)

    # state -> (prev_state, generator_index)
    prev = {start: None}
    q = deque([start])

    while q:
        line, sign = q.popleft()
        if (line, sign) == target:
            break
        for gi in range(len(gens)):
            line2 = gen_line_perm[gi][line]
            sign2 = sign * gen_eps[gi][line]
            st = (line2, sign2)
            if st not in prev:
                prev[st] = ((line, sign), gi)
                q.append(st)

    if target not in prev:
        print("No sign-flip return word found (unexpected).")
        return

    # Reconstruct word
    word = []
    cur = target
    while cur != start:
        p = prev[cur]
        if p is None:
            break
        prev_state, gi = p
        word.append(gi)
        cur = prev_state
    word.reverse()

    out = {
        "start_line": 0,
        "word": word,
        "length": len(word),
    }
    out_path = ROOT / 'artifacts' / 'root_line_sign_negative_word.json'
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Found length-{len(word)} word mapping line 0 to itself with sign -1")
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
