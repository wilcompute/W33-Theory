#!/usr/bin/env python3
"""
BT745 - The presentation space is (almost) a torsor: chirality orbits.

BT696/BT744 arithmetic:  2160 rectangles x 24 valid lifts = 51840
= |Sp(4,3)|, and 1620 apartments x 32 = 51840.  BT745 asks whether this is
an accident or a TORSOR statement.

Objects: presentation pairs (R, L) where R is a centered K33 rectangle (with
its host chart) and L one of its 24 valid center-gauge lifts (an apartment
with gauge data).  |pairs| = 51840.  The group PSp(4,3) (order 25920) acts.

Questions:
  Q1. Is the action FREE (trivial stabilizers)?
  Q2. How many orbits?  (If free: 51840/25920 = 2 - a chirality split.)
  Q3. Is the BT718 selected sheet (2160 pairs) contained in one orbit
      (chiral) or split between both?
  Q4. Do the 8 masks / 3 channels correlate with the orbit label?

Encoding of a pair: (chart_center p, frozenset of rect points, gauge tuple
as a map nonedge -> center).  The action of g: apply g to all data.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json


def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y) -> int:
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def main() -> None:
    pts = points()
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def transvection_perm(v):
        perm = []
        for x in pts:
            w = symp(x, v)
            img = canon(tuple((x[k] + w * v[k]) % 3 for k in range(4)))
            perm.append(pt_index[img])
        return tuple(perm)

    gens = [transvection_perm(v) for v in pts]

    adj = [[False] * n for _ in range(n)]
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
            cs = tuple(sorted(c for c in range(n) if adj[x][c] and adj[y][c]))
            centers[(x, y)] = cs

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
            a = ("p", p)
            b = ("l", li)
            deg[a] += 1
            deg[b] += 1
            graph[a].append(b)
            graph[b].append(a)
        if len(deg) != 8 or any(d != 2 for d in deg.values()):
            return False
        start = next(iter(deg))
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v2 in graph[u]:
                if v2 not in seen:
                    seen.add(v2)
                    stack.append(v2)
        return len(seen) == 8

    # ---- enumerate all presentation pairs --------------------------------
    # pair key: (p, frozenset rect points, frozenset (nonedge, gauge))
    pairs = {}
    pair_meta = {}    # key -> (mask_str, channel)
    all_masks = [
        (1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1),
        (1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1),
    ]
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
                    per_mask = defaultdict(list)
                    for gauges in product(*(centers[e] for e in rect_edges)):
                        paths = [path_edges(x, y, g)
                                 for (x, y), g in zip(rect_edges, gauges)]
                        cyc = xor_paths(paths)
                        if is_octagon(cyc):
                            mask = tuple(1 if g == p else 0 for g in gauges)
                            per_mask[mask].append((gauges, cyc))
                    for mask in all_masks:
                        entries = sorted(
                            per_mask[mask],
                            key=lambda t: tuple(sorted(t[1])))
                        assert len(entries) == 3
                        for ch, (gauges, cyc) in enumerate(entries):
                            key = (p, frozenset(aa) | frozenset(bb),
                                   frozenset(zip(rect_edges, gauges)))
                            pairs[key] = len(pairs)
                            pair_meta[key] = ("".join(map(str, mask)), ch)
    print(f"presentation pairs = {len(pairs)}")
    assert len(pairs) == 51840

    # ---- group action on pairs -------------------------------------------
    def act(g, key):
        p, rect_pts, gauge_set = key
        new_gauges = []
        for (e, c) in gauge_set:
            x, y = e
            new_e = tuple(sorted((g[x], g[y])))
            new_gauges.append((new_e, g[c]))
        return (g[p], frozenset(g[i] for i in rect_pts),
                frozenset(new_gauges))

    # Q1/Q2: orbit decomposition by BFS from seeds.
    unassigned = set(pairs)
    orbits = []
    while unassigned:
        seed = next(iter(unassigned))
        orb = {seed}
        frontier = [seed]
        while frontier:
            nxt = []
            for k in frontier:
                for g in gens:
                    kg = act(g, k)
                    assert kg in pairs, "action does not preserve pair set"
                    if kg not in orb:
                        orb.add(kg)
                        nxt.append(kg)
            frontier = nxt
        orbits.append(orb)
        unassigned -= orb
    sizes = sorted(len(o) for o in orbits)
    print(f"Q2 orbit sizes = {Counter(sizes)}")
    free = all(s == 25920 for s in sizes)
    print(f"Q1 free action (all stabilizers trivial): {free}")

    # Q3/Q4: orbit label vs mask/channel of each pair.
    orbit_of = {}
    for oi, orb in enumerate(orbits):
        for k in orb:
            orbit_of[k] = oi
    sheet_orbit = Counter()
    mask_orbit = defaultdict(Counter)
    for key, (mask, ch) in pair_meta.items():
        oi = orbit_of[key]
        mask_orbit[(mask, ch)][oi] += 1
        if mask == "1110" and ch == 0:
            sheet_orbit[oi] += 1
    print(f"Q3 BT718 sheet orbit distribution = {dict(sheet_orbit)}")
    print("Q4 per-(mask,channel) orbit distribution:")
    for (mask, ch), cnt in sorted(mask_orbit.items()):
        print(f"   {mask} ch{ch}: {dict(cnt)}")

    out = {
        "theorem": "BT745 presentation torsor chirality",
        "pairs": len(pairs),
        "orbit_sizes": {str(k): v for k, v in Counter(sizes).items()},
        "free_action": bool(free),
        "bt718_sheet_orbits": {str(k): v for k, v in sheet_orbit.items()},
        "mask_channel_orbits": {
            f"{m}_ch{c}": dict(cnt) for (m, c), cnt in mask_orbit.items()},
    }
    with open("data/bt745_presentation_torsor_chirality.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\nwrote data/bt745_presentation_torsor_chirality.json")


if __name__ == "__main__":
    main()
