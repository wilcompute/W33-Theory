#!/usr/bin/env python3
"""Compute group order with/without global sign flip on roots.

Verifies whether adding r->-r doubles the order (expected 51840) and
whether the sign flip commutes with generator permutations.
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


def perm_inverse(p):
    inv = [0] * len(p)
    for i, v in enumerate(p):
        inv[v] = i
    return inv


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
    data = json.loads((ROOT / 'artifacts' / 'sp43_we6_generator_map.json').read_text())
    gens = [g['root_perm'] for g in data['generator_maps']]

    roots = build_e8_roots()
    root_to_idx = {r: i for i, r in enumerate(roots)}
    signflip = [0] * len(roots)
    for i, r in enumerate(roots):
        signflip[i] = root_to_idx[tuple(-x for x in r)]

    # Check commutation
    commutes = True
    for g in gens:
        if perm_compose(g, signflip) != perm_compose(signflip, g):
            commutes = False
            break

    print(f"Sign flip commutes with generators: {commutes}")

    order_base = bfs_group(gens)
    print(f"Group order (generators only): {order_base}")

    # Check if sign flip in group by orbit from id
    # (If commutes and not in group, adding it should double the order)
    gens_plus = gens + [signflip]
    order_plus = bfs_group(gens_plus, max_size=300000)
    print(f"Group order (with sign flip): {order_plus}")

    out = {
        "commutes": commutes,
        "order_base": order_base,
        "order_with_sign": order_plus,
    }
    out_path = ROOT / 'artifacts' / 'signflip_group_order.json'
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
