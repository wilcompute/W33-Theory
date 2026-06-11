#!/usr/bin/env python3
"""
BT775 - Cube bipartition: Fix(t) = two pointwise-fixed disjoint lines;
        anchors are cube edges; the duo bit is the antipodal edge map.

Refines BT773 (involution cube) using its open boundary (the two special
4-point fixed lines) and BT774 (clock shadow).

CLAIMS:
  T1. The two fixed lines carrying 4 fixed points each are POINTWISE fixed,
      disjoint, and together contain all 8 fixed points.  They are the two
      sides of the cube-graph bipartition (lines are collinearity cliques,
      hence independent sets of the non-collinearity cube).
  T2. The other four fixed lines are transversals: each carries exactly one
      fixed point from each special line (the 4 collinear cross-pairs).
      Pair profile check: 12 within-line pairs + 4 transversal cross-pairs
      = 16 share-1 pairs; 12 non-collinear cross-pairs = cube edges.
  T3. Each Type-A lift's P-anchor is a CUBE EDGE of its own involution's
      cube (a non-collinear cross-pair of Fix(t_k)).
  T4. Duo partners (r^6-related lifts, same reflection) use anchor edges
      exchanged by the cube's ANTIPODAL map: the duo bit = antipodal edge
      choice.  (Antipodal in Q3: both endpoints at graph distance 3.)
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

    # rectangle, lifts, involutions
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

    def stab_rect(g):
        if g[p0] != p0:
            return False
        if frozenset(g[i] for i in rect_pts) != rect_pts:
            return False
        imgl = frozenset(line_index[frozenset(g[i] for i in lines[li])]
                         for li in (li0, lj0))
        return imgl == frozenset((li0, lj0))

    stabP = [g for g in psp if stab_rect(g)]

    def order_of(g):
        o = 1
        cur = g
        while cur != ident:
            cur = compose(g, cur)
            o += 1
        return o

    z = next(g for g in stabP if order_of(g) == 2)   # duo half-turn r^6

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

    # ---- T1/T2 on one involution's cube ----------------------------------
    seed = next(k for k, (m, c) in lifts.items() if sum(m) % 2 == 1)
    t = involution_of(seed)
    fixP = [i for i in range(n) if t[i] == i]
    fixL = [li for li, l in enumerate(lines)
            if frozenset(t[i] for i in l) == l]
    fixPset = set(fixP)
    special = [li for li in fixL
               if len(set(lines[li]) & fixPset) == 4]
    transv = [li for li in fixL
              if len(set(lines[li]) & fixPset) == 2]
    assert len(special) == 2 and len(transv) == 4
    L1, L2 = (set(lines[special[0]]), set(lines[special[1]]))
    disjoint = not (L1 & L2)
    cover = (L1 | L2) == fixPset
    pointwise = all(t[i] == i for i in L1 | L2)
    print(f"T1 special lines disjoint: {disjoint}, cover all 8 fixed "
          f"points: {cover}, pointwise fixed: {pointwise}")
    assert disjoint and cover and pointwise

    cross_coll = 0
    for li in transv:
        on = set(lines[li]) & fixPset
        assert len(on & L1) == 1 and len(on & L2) == 1
        cross_coll += 1
    print(f"T2 transversals each meet both special lines in one fixed "
          f"point: {cross_coll}/4")
    # cube edges = non-collinear cross pairs
    cube_edges = set()
    for a in L1:
        for b in L2:
            if not adj[a][b]:
                cube_edges.add(frozenset((a, b)))
    print(f"T2 non-collinear cross-pairs (cube edges): {len(cube_edges)} "
          f"(expect 12)")
    assert len(cube_edges) == 12

    # ---- T3/T4: anchors of the 12 Type-A lifts ----------------------------
    # anchor of lift = its involution's 2 fixed points on its octagon
    anchor = {}
    invof = {}
    for key, (mask, cyc) in lifts.items():
        if sum(mask) % 2 != 1:
            continue
        tk = involution_of(key)
        invof[key] = tk
        cyc_pts = {p for (p, _) in cyc}
        fp = frozenset(p for p in cyc_pts if tk[p] == p)
        assert len(fp) == 2
        anchor[key] = fp

    t3_ok = 0
    for key, fp in anchor.items():
        tk = invof[key]
        fPk = {i for i in range(n) if tk[i] == i}
        sp = [li for li, l in enumerate(lines)
              if frozenset(tk[i] for i in l) == l
              and len(set(lines[li]) & fPk) == 4]
        S1, S2 = (set(lines[sp[0]]), set(lines[sp[1]]))
        a, b = tuple(fp)
        cross = (a in S1 and b in S2) or (a in S2 and b in S1)
        noncoll = not adj[a][b]
        if cross and noncoll:
            t3_ok += 1
    print(f"T3 Type-A anchors that are cube edges (non-collinear "
          f"cross-pairs): {t3_ok}/12")

    # T4: duo partners' anchors antipodal in their shared cube
    import networkx as nx
    t4_results = []
    seen = set()
    for key, fp in anchor.items():
        if key in seen:
            continue
        partner = act(z, key)
        seen.add(key)
        seen.add(partner)
        fp2 = anchor[partner]
        tk = invof[key]
        # build the cube graph of tk
        fPk = sorted(i for i in range(n) if tk[i] == i)
        G = nx.Graph()
        G.add_nodes_from(fPk)
        fLk = [li for li, l in enumerate(lines)
               if frozenset(tk[i] for i in l) == l]
        collk = {p: set() for p in fPk}
        for li in fLk:
            on = [p for p in lines[li] if p in set(fPk)]
            for x2, y2 in combinations(on, 2):
                collk[x2].add(y2)
                collk[y2].add(x2)
        for x2, y2 in combinations(fPk, 2):
            if y2 not in collk[x2]:
                G.add_edge(x2, y2)
        a1, b1 = tuple(fp)
        a2, b2 = tuple(fp2)
        d = sorted([nx.shortest_path_length(G, a1, a2),
                    nx.shortest_path_length(G, a1, b2),
                    nx.shortest_path_length(G, b1, a2),
                    nx.shortest_path_length(G, b1, b2)])
        # antipodal edge pair: endpoint distances {3,3} for the matched ends
        t4_results.append(tuple(d))
    profile = Counter(t4_results)
    print(f"T4 duo-anchor endpoint distance profiles: {dict(profile)}")
    antipodal = all(d == (2, 3, 3, 2) or d == (3, 3, 3, 3)
                    or d == (2, 2, 3, 3) for d in t4_results)
    print(f"   (antipodal edge map iff distances include the 3,3 pattern)")

    out = {
        "theorem": "BT775 cube bipartition + anchor edges",
        "special_lines_disjoint_cover_pointwise": True,
        "transversal_cross": cross_coll,
        "cube_edges": len(cube_edges),
        "anchors_are_cube_edges": t3_ok,
        "duo_anchor_distance_profiles": {str(k): v
                                         for k, v in profile.items()},
    }
    with open("data/bt775_cube_bipartition_anchor_edges.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt775_cube_bipartition_anchor_edges.json")


if __name__ == "__main__":
    main()
