#!/usr/bin/env python3
"""
BT776 - Corner vertex = chart center; the Type-B octahedron mirror;
        cube-edge slot transitivity (4 anchors per edge).

Closes the three BT775 boundary questions.

  T1. The duo corner vertex (shared cube vertex of the two duo-partner
      anchor edges, BT775) is the CHART CENTER p0 itself.  Note p0 is
      fixed by every lift involution t_k (t_k stabilizes the chart), so
      p0 is always one of the 8 cube vertices - i.e. p0 lies on one of
      the two skew lines of Fix(t_k).
  T2. Type-B mirror: classify the 12 L-anchor line pairs of a rectangle
      against the fixed-line taxonomy of their own involution
      (2 special skew lines + 4 transversals): composition and whether
      the two anchor lines meet in a fixed point (octahedron-edge test).
  T3. PSp(4,3) acts transitively on the 6480 = 540 x 12 (cube, edge)
      slots; since the 25920 Type-A anchor-uses are equivariant, every
      cube edge is anchored by EXACTLY 25920/6480 = 4 lifts.
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
        s2 = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v2 in graph[u]:
                if v2 not in s2:
                    s2.add(v2)
                    stack.append(v2)
        return len(s2) == 8

    p0 = 0
    li0, lj0 = sorted(through[p0])[:2]
    A = tuple(sorted(lines[li0] - {p0}))
    B = tuple(sorted(lines[lj0] - {p0}))
    aa = (A[0], A[1])
    bb = (B[0], B[1])
    rect_edges = [tuple(sorted(e)) for e in [
        (aa[0], bb[0]), (aa[1], bb[0]), (aa[1], bb[1]), (aa[0], bb[1])]]
    rect_pts = frozenset(aa) | frozenset(bb)

    def act(g, key):
        p, rp, gs = key
        ng = []
        for (e, c) in gs:
            x, y = e
            ng.append((tuple(sorted((g[x], g[y]))), g[c]))
        return (g[p], frozenset(g[i] for i in rp), frozenset(ng))

    lifts = {}
    for gauges in product(*(centers[e] for e in rect_edges)):
        cyc = xor_paths([path_edges(x, y, g)
                         for (x, y), g in zip(rect_edges, gauges)])
        if is_octagon(cyc):
            mask = tuple(1 if g == p0 else 0 for g in gauges)
            key = (p0, rect_pts, frozenset(zip(rect_edges, gauges)))
            lifts[key] = (mask, frozenset(cyc))
    assert len(lifts) == 24

    def involution_of(key):
        for h in psp:
            cand = compose(h, g_sim)
            if act(cand, key) == key:
                return cand
        raise RuntimeError

    # ---- T1: corner vertex = p0? -----------------------------------------
    corner_is_p0 = 0
    duo_pairs = 0
    seenA = set()
    inv_cache = {}
    for key, (mask, cyc) in lifts.items():
        if sum(mask) % 2 != 1 or key in seenA:
            continue
        tk = involution_of(key)
        inv_cache[key] = tk
        # find duo partner: same reflection, other lift
        partner = None
        for k2, (m2, c2) in lifts.items():
            if k2 == key or sum(m2) % 2 != 1:
                continue
            if act(tk, k2) == k2:
                partner = k2
                break
        assert partner is not None
        seenA.add(key)
        seenA.add(partner)
        duo_pairs += 1

        def anchor(k):
            cyc_pts = {p for (p, _) in lifts[k][1]}
            return frozenset(p for p in cyc_pts if tk[p] == p)

        a1 = anchor(key)
        a2 = anchor(partner)
        shared = a1 & a2
        if shared == {p0}:
            corner_is_p0 += 1
    print(f"T1 duo pairs whose shared corner vertex = chart center p0: "
          f"{corner_is_p0}/{duo_pairs}")

    # ---- T2: Type-B L-anchor composition ----------------------------------
    comp = Counter()
    meets_fixed = Counter()
    for key, (mask, cyc) in lifts.items():
        if sum(mask) % 2 != 0:
            continue
        tk = involution_of(key)
        fPk = {i for i in range(n) if tk[i] == i}
        fLk = [li for li, l in enumerate(lines)
               if frozenset(tk[i] for i in l) == l]
        special = {li for li in fLk
                   if len(set(lines[li]) & fPk) == 4}
        cyc_lns = {l for (_, l) in cyc}
        anc = [l for l in cyc_lns
               if frozenset(tk[i] for i in lines[l]) == lines[l]]
        assert len(anc) == 2
        kinds = tuple(sorted("S" if l in special else "T" for l in anc))
        comp["".join(kinds)] += 1
        inter = set(lines[anc[0]]) & set(lines[anc[1]])
        if inter:
            x = next(iter(inter))
            meets_fixed["meet@" + ("fixedpt" if x in fPk else "movingpt")] += 1
        else:
            meets_fixed["disjoint"] += 1
    print(f"T2 L-anchor composition (S=special skew line, T=transversal): "
          f"{dict(comp)}")
    print(f"T2 L-anchor pair intersection: {dict(meets_fixed)}")

    # ---- T3: transitivity on (skew-pair, cube-edge) slots ------------------
    # represent slot as (frozenset{line_i, line_j}, frozenset{pt_a, pt_b})
    # seed from the T1 cube
    k0 = next(k for k, (m, c) in lifts.items() if sum(m) % 2 == 1)
    t0 = inv_cache.get(k0) or involution_of(k0)
    fP0 = {i for i in range(n) if t0[i] == i}
    fL0 = [li for li, l in enumerate(lines)
           if frozenset(t0[i] for i in l) == l
           and len(set(lines[li]) & fP0) == 4]
    L1, L2 = set(lines[fL0[0]]), set(lines[fL0[1]])
    e0 = None
    for a in L1:
        for b in L2:
            if not adj[a][b]:
                e0 = frozenset((a, b))
                break
        if e0:
            break
    slot0 = (frozenset(fL0), e0)

    def act_slot(g, slot):
        lp, ep = slot
        nl = frozenset(line_index[frozenset(g[i] for i in lines[li])]
                       for li in lp)
        ne = frozenset(g[i] for i in ep)
        return (nl, ne)

    orbit = {slot0}
    frontier = [slot0]
    while frontier:
        nxt = []
        for s in frontier:
            for g in gens_psp:
                sg = act_slot(g, s)
                if sg not in orbit:
                    orbit.add(sg)
                    nxt.append(sg)
        frontier = nxt
    print(f"T3 orbit of (skew-pair, cube-edge) slot = {len(orbit)} "
          f"(expect 6480 = 540 x 12)")
    transitive = (len(orbit) == 6480)
    if transitive:
        print("T3 transitive => every cube edge is anchored by exactly "
              "25920/6480 = 4 Type-A lifts globally")

    out = {
        "theorem": "BT776 corner center + octahedron mirror + slot count",
        "corner_is_chart_center": f"{corner_is_p0}/{duo_pairs}",
        "L_anchor_composition": dict(comp),
        "L_anchor_intersection": dict(meets_fixed),
        "slot_orbit": len(orbit),
        "slots_transitive": bool(transitive),
        "anchors_per_cube_edge": 4 if transitive else None,
    }
    with open("data/bt776_corner_center_octahedron_mirror.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt776_corner_center_octahedron_mirror.json")


if __name__ == "__main__":
    main()
