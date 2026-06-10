#!/usr/bin/env python3
"""BT750 — duo bit equals the central half-turn, but not a pure apartment gauge.

Extends BT749.  For one centered rectangle R, the inner stabilizer is Z12 and
has a unique central involution z=r^6.  BT749 showed the full rectangle
stabilizer is D12 and each reflection fixes exactly two lifts.  This verifier
checks that those two lifts are precisely z-partners, and then tests the sharp
follow-up conjecture: do z-partners present the same Levi octagon/apartment?

Answer: no.  The duo bit is real geometry: the two lifts fixed by the same
reflection are different Levi octagons, though z preserves chirality.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json


def inv3(a: int) -> int:
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def main() -> None:
    pts = points()
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def matrix_perm(M):
        return tuple(pt_index[canon(tuple(
            sum(M[r][c] * x[c] for c in range(4)) % 3 for r in range(4)))]
            for x in pts)

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[k] + w * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    gens_psp = [transvection_perm(v) for v in pts]
    g_sim = matrix_perm([[1,0,0,0],[0,1,0,0],[0,0,2,0],[0,0,0,2]])
    ident = tuple(range(n))

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    psp = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens_psp:
                gh = compose(h, g)
                if gh not in psp:
                    psp.add(gh)
                    nxt.append(gh)
        frontier = nxt
    assert len(psp) == 25920

    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    line_index = {l: i for i, l in enumerate(lines)}
    through = defaultdict(list)
    edge_line = {}
    for li, l in enumerate(lines):
        for p in l:
            through[p].append(li)
        for a, b in combinations(sorted(l), 2):
            edge_line[(a, b)] = li
    centers = {}
    for x, y in combinations(range(n), 2):
        if not adj[x][y]:
            centers[(x, y)] = tuple(sorted(
                c for c in range(n) if adj[x][c] and adj[y][c]))

    def path_edges(x, y, c):
        lxc = edge_line[tuple(sorted((x, c)))]
        lcy = edge_line[tuple(sorted((c, y)))]
        return [(x, lxc), (c, lxc), (c, lcy), (y, lcy)]

    def xor_paths(paths):
        cnt = Counter()
        for path in paths:
            for e in path:
                cnt[e] ^= 1
        return frozenset(e for e, v in cnt.items() if v)

    def is_octagon(es):
        if len(es) != 8:
            return False
        deg = Counter()
        graph = defaultdict(list)
        for p, li in es:
            deg[("p", p)] += 1
            deg[("l", li)] += 1
            graph[("p", p)].append(("l", li))
            graph[("l", li)].append(("p", p))
        if len(deg) != 8 or any(d != 2 for d in deg.values()):
            return False
        start = next(iter(deg))
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return len(seen) == 8

    # Seed rectangle, as in BT749.
    p0 = 0
    li0, lj0 = sorted(through[p0])[:2]
    A = tuple(sorted(lines[li0] - {p0}))
    B = tuple(sorted(lines[lj0] - {p0}))
    aa = (A[0], A[1])
    bb = (B[0], B[1])
    rect_edges = [tuple(sorted(e)) for e in [
        (aa[0], bb[0]), (aa[1], bb[0]),
        (aa[1], bb[1]), (aa[0], bb[1])]]
    rect_pts = frozenset(aa) | frozenset(bb)

    lifts = []
    per_mask = defaultdict(list)
    for gauges in product(*(centers[e] for e in rect_edges)):
        cyc = xor_paths([path_edges(x, y, g)
                         for (x, y), g in zip(rect_edges, gauges)])
        if is_octagon(cyc):
            mask = tuple(1 if g == p0 else 0 for g in gauges)
            per_mask[mask].append((tuple(sorted(cyc)), gauges))
    for mask, entries in per_mask.items():
        entries.sort()
        for ch, (_, gauges) in enumerate(entries):
            key = (p0, rect_pts, frozenset(zip(rect_edges, gauges)))
            lifts.append((key, mask, ch))
    assert len(lifts) == 24

    def act(g, key):
        p, rp, gs = key
        ng = []
        for (e, c) in gs:
            x, y = e
            ng.append((tuple(sorted((g[x], g[y]))), g[c]))
        return (g[p], frozenset(g[i] for i in rp), frozenset(ng))

    def stab_rect(g):
        if g[p0] != p0:
            return False
        if frozenset(g[i] for i in rect_pts) != rect_pts:
            return False
        imgl = frozenset(line_index[frozenset(g[i] for i in lines[li])]
                         for li in (li0, lj0))
        return imgl == frozenset((li0, lj0))

    stabP = [g for g in psp if stab_rect(g)]
    stabO = [compose(h, g_sim) for h in psp if stab_rect(compose(h, g_sim))]
    assert len(stabP) == 12 and len(stabO) == 12

    def order_of(g):
        o = 1
        cur = g
        while cur != ident:
            cur = compose(g, cur)
            o += 1
        return o

    z_candidates = [g for g in stabP if order_of(g) == 2]
    assert len(z_candidates) == 1
    z = z_candidates[0]

    lift_info = {}
    label_info = {}
    for key, mask, ch in lifts:
        gs = dict(key[2])
        gauges = [gs[e] for e in rect_edges]
        cyc = xor_paths([path_edges(x, y, g)
                         for (x, y), g in zip(rect_edges, gauges)])
        assert is_octagon(cyc)
        lift_info[key] = (mask, ch, frozenset(cyc))
        label_info[key] = {
            "mask": "".join(map(str, mask)),
            "channel": ch,
            "weight": sum(mask),
        }

    share_cycle = 0
    diff_cycle = 0
    parity_kept = 0
    same_mask = 0
    same_channel = 0
    for key, (mask, ch, cyc) in lift_info.items():
        partner = act(z, key)
        assert partner in lift_info and partner != key
        pm, pch, pc = lift_info[partner]
        parity_kept += (sum(pm) % 2 == sum(mask) % 2)
        same_mask += (pm == mask)
        same_channel += (pch == ch)
        share_cycle += (pc == cyc)
        diff_cycle += (pc != cyc)

    invols = [g for g in stabO if order_of(g) == 2]
    fixed_counts = []
    inv_duo_z_ok = 0
    fixed_mask_pairs = []
    for t in invols:
        fixed = [key for key in lift_info if act(t, key) == key]
        fixed_counts.append(len(fixed))
        if len(fixed) == 2 and act(z, fixed[0]) == fixed[1] and act(z, fixed[1]) == fixed[0]:
            inv_duo_z_ok += 1
        fixed_mask_pairs.append(tuple(sorted(label_info[k]["mask"] for k in fixed)))

    cycA = {c for _, (m, _, c) in lift_info.items() if sum(m) % 2 == 1}
    cycB = {c for _, (m, _, c) in lift_info.items() if sum(m) % 2 == 0}
    allcyc = {c for _, (_, _, c) in lift_info.items()}

    duo_orbits = set()
    duo_share = []
    duo_label_profile = Counter()
    for key in lift_info:
        partner = act(z, key)
        orbit = frozenset([key, partner])
        if orbit in duo_orbits:
            continue
        duo_orbits.add(orbit)
        _, _, c1 = lift_info[key]
        _, _, c2 = lift_info[partner]
        duo_share.append(c1 == c2)
        duo_label_profile[tuple(sorted((label_info[key]["mask"], label_info[partner]["mask"])))] += 1

    out = {
        "theorem": "BT750 duo bit central half-turn",
        "stab_inner_order": len(stabP),
        "stab_outer_order": len(stabO),
        "central_half_turn_order": order_of(z),
        "z_partner_keeps_chirality": parity_kept,
        "z_partner_same_mask": same_mask,
        "z_partner_same_channel": same_channel,
        "duo_share_octagon": share_cycle,
        "duo_differ_octagon": diff_cycle,
        "duo_orbits": len(duo_orbits),
        "duo_orbits_share_octagon": sum(duo_share),
        "outer_involutions": len(invols),
        "outer_involution_fixed_lift_counts": {str(k): v for k, v in Counter(fixed_counts).items()},
        "outer_involution_duo_equals_z_pair": inv_duo_z_ok,
        "distinct_octagons_typeA": len(cycA),
        "distinct_octagons_typeB": len(cycB),
        "distinct_octagons_total": len(allcyc),
        "duo_label_profile": {str(k): v for k, v in sorted(duo_label_profile.items(), key=lambda kv: str(kv[0]))},
        "fixed_mask_pair_profile": {str(k): v for k, v in Counter(fixed_mask_pairs).items()},
    }

    assert out["z_partner_keeps_chirality"] == 24
    assert out["outer_involution_duo_equals_z_pair"] == 12
    assert out["duo_share_octagon"] == 0
    assert out["distinct_octagons_total"] == 24

    with open("data/bt750_duo_bit_half_turn.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
