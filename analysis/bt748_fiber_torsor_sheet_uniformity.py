#!/usr/bin/env python3
"""
BT748 - Root-triple fibers are centralizer torsors; BT718 sheet uniformity.

BT747: pairs -> 540 tri-orthogonal root triples, 96-pair fibers (48+48 by
chirality).  Two precise questions:

  Q1. The centralizer C = C_{W(E6)}(t) has order 51840/540 = 96 = fiber
      size.  Does C act freely-transitively on the fiber of t?  Then each
      fiber is a C-TORSOR and the whole presentation space is the
      associated bundle W(E6) x_C (C) over the 540 triples - a complete
      equivariant coordinate system (triple, chirality, C-coordinate).
  Q2. The BT718 canonical sheet has 2160 pairs and 2160/540 = 4.  Does the
      sheet meet every fiber exactly 4 times (uniform), making the
      canonical selector a uniform transversal of the root fibration?

Both answered exactly below.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json


def inv3(a):
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


def main():
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
        s2 = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v2 in graph[u]:
                if v2 not in s2:
                    s2.add(v2)
                    stack.append(v2)
        return len(s2) == 8

    pairs = {}
    pair_parity = {}
    sheet = []   # BT718 sheet: mask 1110, channel 0 (lex sort of 3 cycles)
    for p in range(n):
        for li, lj in combinations(through[p], 2):
            A = tuple(sorted(lines[li] - {p}))
            B = tuple(sorted(lines[lj] - {p}))
            for aa in combinations(A, 2):
                for bb in combinations(B, 2):
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]), (aa[1], bb[0]),
                        (aa[1], bb[1]), (aa[0], bb[1]),
                    ]]
                    mask_entries = []
                    for gauges in product(*(centers[e] for e in rect_edges)):
                        paths = [path_edges(x, y, g)
                                 for (x, y), g in zip(rect_edges, gauges)]
                        cyc = xor_paths(paths)
                        if is_octagon(cyc):
                            mask = tuple(1 if g == p else 0 for g in gauges)
                            key = (p, frozenset(aa) | frozenset(bb),
                                   frozenset(zip(rect_edges, gauges)))
                            pairs[key] = len(pairs)
                            pair_parity[key] = sum(mask) % 2
                            if mask == (1, 1, 1, 0):
                                mask_entries.append(
                                    (tuple(sorted(cyc)), key))
                    mask_entries.sort()
                    sheet.append(mask_entries[0][1])
    assert len(pairs) == 51840
    assert len(sheet) == 2160

    def act(g, key):
        p, rect_pts, gauge_set = key
        ng = []
        for (e, c) in gauge_set:
            x, y = e
            ng.append((tuple(sorted((g[x], g[y]))), g[c]))
        return (g[p], frozenset(g[i] for i in rect_pts), frozenset(ng))

    # canonical involution of a seed pair
    seed = next(iter(pairs))
    t0 = None
    for h in psp:
        t = compose(h, g_sim)
        if act(t, seed) == seed:
            t0 = t
            break
    assert t0 is not None and compose(t0, t0) == ident

    # 540-class of t0 under PGSp
    def inverse(a):
        out = [0]*n
        for i in range(n):
            out[a[i]] = i
        return tuple(out)

    cls = {t0}
    frontier = [t0]
    allg = gens_psp + [g_sim]
    ginv = [inverse(g) for g in allg]
    while frontier:
        nxt = []
        for x in frontier:
            for g, gi in zip(allg, ginv):
                y = compose(gi, compose(x, g))
                if y not in cls:
                    cls.add(y)
                    nxt.append(y)
        frontier = nxt
    assert len(cls) == 540

    # ---- Q1: centralizer torsor ------------------------------------------
    cent = [h for h in psp if compose(h, t0) == compose(t0, h)]
    cent_out = [compose(h, g_sim) for h in psp
                if compose(compose(h, g_sim), t0)
                == compose(t0, compose(h, g_sim))]
    C = cent + cent_out
    print(f"Q1 |C_PGSp(t0)| = {len(C)} (inner {len(cent)} + outer "
          f"{len(cent_out)}); expect 96")
    assert len(C) == 96

    fiber = [k for k in pairs if act(t0, k) == k]
    assert len(fiber) == 96
    # orbit of one fiber point under C
    k0 = fiber[0]
    orbC = {k0}
    frontier = [k0]
    while frontier:
        nxt = []
        for k in frontier:
            for g in C:
                kg = act(g, k)
                if kg not in orbC:
                    orbC.add(kg)
                    nxt.append(kg)
        frontier = nxt
    fiber_set = set(fiber)
    print(f"Q1 C-orbit of one fiber pair = {len(orbC)}; "
          f"orbit inside fiber: {orbC <= fiber_set}")
    transitive = (len(orbC) == 96 and orbC == fiber_set)
    # freeness: |C| = fiber size and transitive => free
    print(f"Q1 fiber is a C-torsor: {transitive}")

    # chirality split of the C-action: orbit of k0 under C ∩ PSp (order 48)
    orbC_in = {k0}
    frontier = [k0]
    for _ in range(60):
        nxt = []
        for k in frontier:
            for g in cent:
                kg = act(g, k)
                if kg not in orbC_in:
                    orbC_in.add(kg)
                    nxt.append(kg)
        if not nxt:
            break
        frontier = nxt
    par_orb = Counter(pair_parity[k] for k in orbC_in)
    print(f"Q1 inner-centralizer orbit size = {len(orbC_in)}, "
          f"parity profile = {dict(par_orb)}")

    # ---- Q2: BT718 sheet uniformity over the 540 fibers --------------------
    sheet_set = set(sheet)
    per_t = []
    for t in cls:
        c = sum(1 for k in sheet_set if act(t, k) == k)
        per_t.append(c)
    dist = Counter(per_t)
    print(f"Q2 sheet hits per root-triple fiber: {dict(sorted(dist.items()))}")
    uniform = (set(per_t) == {4})
    print(f"Q2 uniform transversal (4 per fiber): {uniform}")

    out = {
        "theorem": "BT748 fiber torsor + sheet uniformity",
        "centralizer_order": len(C),
        "fiber_size": len(fiber),
        "fiber_is_C_torsor": bool(transitive),
        "inner_centralizer_orbit": len(orbC_in),
        "inner_orbit_parity": {str(k): v for k, v in par_orb.items()},
        "sheet_per_fiber_distribution": {str(k): v
                                         for k, v in sorted(dist.items())},
        "sheet_uniform_4": bool(uniform),
    }
    with open("data/bt748_fiber_torsor_sheet_uniformity.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt748_fiber_torsor_sheet_uniformity.json")


if __name__ == "__main__":
    main()
