#!/usr/bin/env python3
"""
BT773 - The involution cube: Fix(t) is a combinatorial cube in W(3,3),
        the order-48 centralizer is its full symmetry group, and chirality
        is the cube/octahedron duality direction.

CONNECTIONS HUNTED (octahedron + mod12 corpus):
  * w33_local_pencil_octahedra / BT508: every W33 point carries a pencil
    octahedron L(K4); 40 x (6,12,8) = (240,480,320).
  * BT510/BT517/BT524: octa-cube packet (6,12,8)+(8,12,6) = (14,24,14)
    attached to each of the 30 nows.
  * BT746/BT749: Z12 rectangle clock, D12 = Z12 x Z2 stabilizer.
  * BT747: every presentation pair's canonical involution t (3A1 class)
    fixes 8 points + 6 lines.   <-- 8 vertices + 6 faces of a CUBE?
  * BT748: inner centralizer order 48 = |full cube symmetry group O_h|.
  * BT772: chirality = P-axis vs L-axis anchoring.

CLAIMS TESTED:
  T1. Each of the 6 fixed lines contains exactly 4 fixed points; each of
      the 8 fixed points lies on exactly 3 fixed lines: the (8,6) fixed
      geometry has the vertex-face incidence of a CUBE.
  T2. Collinearity graph on the 8 fixed points (via fixed lines) is the
      cocktail-party graph K_{4x2}: every point collinear with all but a
      unique ANTIPODE (4 space diagonals).  The 6 fixed lines fall into 3
      antipodal pairs (opposite faces share no point).
  T3. The inner centralizer C = C_PSp(t) (order 48) acts faithfully on the
      8 fixed points with image of order 48 preserving the 6-line set:
      C IS the full cube symmetry group (order 48).
  T4. Chirality anchors (BT772): P-axis anchors are antipodal point pairs
      = cube space diagonals (4 of them); L-axis anchors are antipodal
      line pairs = octahedron axes (3 of them).  Count the t-invariant
      apartments anchored on each.
  T5. The cube's 12 edges (point pairs sharing exactly 2 fixed lines... in
      cube terms: count pairs by shared-line profile) - the mod-12 layer.
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

    # canonical involution from the test rectangle (BT747 conventions)
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

    seed = None
    for gauges in product(*(centers[e] for e in rect_edges)):
        cyc = xor_paths([path_edges(x, y, g)
                         for (x, y), g in zip(rect_edges, gauges)])
        if is_octagon(cyc):
            seed = (p0, rect_pts, frozenset(zip(rect_edges, gauges)))
            break
    t = None
    for h in psp:
        cand = compose(h, g_sim)
        if act(cand, seed) == seed:
            t = cand
            break
    assert t is not None and compose(t, t) == ident

    fixP = [i for i in range(n) if t[i] == i]
    fixL = [li for li, l in enumerate(lines)
            if frozenset(t[i] for i in l) == l]
    print(f"Fix(t): {len(fixP)} points, {len(fixL)} lines")
    assert len(fixP) == 8 and len(fixL) == 6

    # T1: incidence counts
    pts_per_line = [len([p for p in lines[li] if p in set(fixP)])
                    for li in fixL]
    lines_per_pt = [len([li for li in fixL if p in lines[li]])
                    for p in fixP]
    print(f"T1 fixed points per fixed line: {Counter(pts_per_line)}")
    print(f"T1 fixed lines per fixed point: {Counter(lines_per_pt)}")
    cube_incidence = (set(pts_per_line) == {4} and set(lines_per_pt) == {3})
    print(f"T1 cube vertex-face incidence (4 per face, 3 per vertex): "
          f"{cube_incidence}")

    # T2: collinearity graph on fixP via fixed lines
    fixPset = set(fixP)
    coll = {p: set() for p in fixP}
    for li in fixL:
        on = [p for p in lines[li] if p in fixPset]
        for a, b in combinations(on, 2):
            coll[a].add(b)
            coll[b].add(a)
    degs = Counter(len(v) for v in coll.values())
    print(f"T2 collinearity degrees: {dict(degs)} (cocktail K_4x2 iff all 6)")
    antipodes = {p: [q for q in fixP if q != p and q not in coll[p]]
                 for p in fixP}
    n_anti = Counter(len(v) for v in antipodes.values())
    print(f"T2 non-collinear partners per point: {dict(n_anti)} "
          f"(unique antipode iff all 1)")
    # line antipodal pairs: opposite faces share no fixed point
    line_pairs_disjoint = 0
    for la, lb in combinations(fixL, 2):
        if not (set(lines[la]) & set(lines[lb]) & fixPset):
            line_pairs_disjoint += 1
    print(f"T2 disjoint fixed-line pairs: {line_pairs_disjoint} (expect 3)")

    # T3: centralizer action on the cube
    cent = [h for h in psp if compose(h, t) == compose(t, h)]
    print(f"T3 |C_PSp(t)| = {len(cent)}")
    images = {tuple(h[p] for p in fixP) for h in cent}
    print(f"T3 distinct images on 8 fixed points = {len(images)} "
          f"(faithful + order 48 = full cube group iff 48)")

    # T4: t-invariant apartments through the rectangle, by anchor
    # enumerate ALL 24 lifts of the rectangle and their anchors under t
    anchors = Counter()
    for gauges in product(*(centers[e] for e in rect_edges)):
        cyc = xor_paths([path_edges(x, y, g)
                         for (x, y), g in zip(rect_edges, gauges)])
        if not is_octagon(cyc):
            continue
        key = (p0, rect_pts, frozenset(zip(rect_edges, gauges)))
        # involution of this lift
        tk = None
        for h in psp:
            cand = compose(h, g_sim)
            if act(cand, key) == key:
                tk = cand
                break
        cyc_pts = {p for (p, _) in cyc}
        cyc_lns = {l for (_, l) in cyc}
        fp = tuple(sorted(p for p in cyc_pts if tk[p] == p))
        fl = tuple(sorted(l for l in cyc_lns
                          if frozenset(tk[i] for i in lines[l]) == lines[l]))
        if len(fp) == 2:
            anchors[("P", fp)] += 1
        elif len(fl) == 2:
            anchors[("L", fl)] += 1
    p_anchors = [(k, v) for k, v in anchors.items() if k[0] == "P"]
    l_anchors = [(k, v) for k, v in anchors.items() if k[0] == "L"]
    print(f"T4 distinct P-anchors used: {len(p_anchors)} "
          f"(multiplicities {sorted(v for _, v in p_anchors)})")
    print(f"T4 distinct L-anchors used: {len(l_anchors)} "
          f"(multiplicities {sorted(v for _, v in l_anchors)})")

    # T2b: the NON-collinearity graph on the 8 fixed points = cube graph Q3?
    import networkx as nx
    NC = nx.Graph()
    NC.add_nodes_from(fixP)
    for a, b in combinations(fixP, 2):
        if b not in coll[a]:
            NC.add_edge(a, b)
    is_cube = nx.is_isomorphic(NC, nx.cubical_graph())
    print(f"T2b non-collinearity graph on Fix(t) points = cube graph Q3: "
          f"{is_cube}")

    # T5: edge profile - pairs of fixed points by number of shared fixed lines
    share = Counter()
    for a, b in combinations(fixP, 2):
        s = sum(1 for li in fixL
                if a in lines[li] and b in lines[li])
        share[s] += 1
    print(f"T5 point-pair shared-line profile: {dict(sorted(share.items()))}")
    print("   (cube: 12 edges share 2 faces, 12 face-diagonals share 1, "
          "4 space diagonals share 0)")

    out = {
        "theorem": "BT773 involution cube",
        "fixed_points": len(fixP),
        "fixed_lines": len(fixL),
        "cube_incidence": bool(cube_incidence),
        "collinearity_degrees": {str(k): v for k, v in degs.items()},
        "disjoint_line_pairs": line_pairs_disjoint,
        "non_collinearity_is_cube_graph": bool(is_cube),
        "centralizer_order": len(cent),
        "centralizer_image_on_cube": len(images),
        "p_anchor_count": len(p_anchors),
        "l_anchor_count": len(l_anchors),
        "pair_shared_line_profile": {str(k): v
                                     for k, v in sorted(share.items())},
    }
    with open("data/bt773_involution_cube_theorem.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt773_involution_cube_theorem.json")


if __name__ == "__main__":
    main()
