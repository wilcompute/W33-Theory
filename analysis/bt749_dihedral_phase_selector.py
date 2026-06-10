#!/usr/bin/env python3
"""
BT749 - The dihedral phase structure: lifts are reflections of D12.

BT746: Stab_PSp(rectangle) = Z12.  BT747-748: every pair has a canonical
involution in the 540-class (3A1 triples), and the involution STABILIZES
its own pair, hence its rectangle.  Therefore the involutions of the 12
chiral lifts of a rectangle R all lie in the outer coset of

    Stab_PGSp(R)   (order 24, containing Z12).

If Stab_PGSp(R) is dihedral D12 (= Z12 with 12 reflections), then the 12
chiral lifts correspond to the 12 reflections, the BT705 hinge datum is
literally a DIHEDRAL PHASE choice, and Z12-conjugation splits the
reflections into two classes of 6 - a new invariant to compare with the
(mask, channel) labels.

COMPUTATIONS (one rectangle suffices, by transitivity):
  T1. Stab_PGSp(R): order, element orders, dihedral identification.
  T2. For each of the 12 Type-A lifts of R: its canonical involution; all
      12 lie in the outer coset of Stab_PGSp(R); the map lift -> involution
      is a BIJECTION onto the outer involutions.
  T3. The Z12-conjugation orbits on these 12 involutions (expect 6+6) and
      their correlation with the (mask, channel) labels of the lifts.
  T4. The 12 root triples of the lifts: distinct? (i.e. lift -> triple
      injective over one rectangle)
  T5. Same questions for the 12 Type-B lifts.
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

    # first rectangle and its 24 lifts with labels
    p0 = 0
    li0, lj0 = sorted(through[p0])[:2]
    A = tuple(sorted(lines[li0] - {p0}))
    B = tuple(sorted(lines[lj0] - {p0}))
    aa = (A[0], A[1])
    bb = (B[0], B[1])
    rect_edges = [tuple(sorted(e)) for e in [
        (aa[0], bb[0]), (aa[1], bb[0]), (aa[1], bb[1]), (aa[0], bb[1])]]
    rect_pts = frozenset(aa) | frozenset(bb)

    lifts = []   # (key, mask, channel)
    per_mask = defaultdict(list)
    for gauges in product(*(centers[e] for e in rect_edges)):
        paths = [path_edges(x, y, g)
                 for (x, y), g in zip(rect_edges, gauges)]
        cyc = xor_paths(paths)
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

    # T1: full stabilizer of the centered rectangle in PGSp.
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
    S = stabP + stabO
    print(f"T1 |Stab_PGSp(rect)| = {len(S)} = {len(stabP)} inner + "
          f"{len(stabO)} outer")
    assert len(stabP) == 12

    def order_of(g):
        o = 1
        cur = g
        while cur != ident:
            cur = compose(g, cur)
            o += 1
        return o

    orders_out = Counter(order_of(g) for g in stabO)
    print(f"T1 outer coset element orders: {dict(sorted(orders_out.items()))}")
    dihedral = (orders_out.get(2, 0) == 12)
    print(f"T1 Stab_PGSp(rect) = D12 (12 outer involutions): {dihedral}")

    # T2: canonical involutions of the 12 Type-A and 12 Type-B lifts.
    inv_of = {}
    for key, mask, ch in lifts:
        t = None
        for cand in stabO:
            if order_of(cand) == 2 and act(cand, key) == key:
                t = cand
                break
        inv_of[(mask, ch)] = t

    found = {k: v for k, v in inv_of.items() if v is not None}
    print(f"T2 lifts whose involution lies in Stab outer coset: "
          f"{len(found)}/24")
    distinct = len({tuple(v) for v in found.values()})
    print(f"T2 distinct involutions = {distinct}")

    # T3: Z12 conjugation orbits on the outer involutions + labels.
    invols = [g for g in stabO if order_of(g) == 2]
    print(f"T3 outer involutions available = {len(invols)}")
    # conjugation by stabP (Z12)
    orbits = []
    rest = {tuple(t) for t in invols}
    while rest:
        t = next(iter(rest))
        t = tuple(t)
        orb = set()
        for r in stabP:
            rinv = [0]*n
            for i in range(n):
                rinv[r[i]] = i
            orb.add(tuple(compose(tuple(rinv), compose(t, r))))
        orbits.append(orb)
        rest -= orb
    print(f"T3 Z12-conjugation orbit sizes on outer involutions: "
          f"{sorted(len(o) for o in orbits)}")
    # correlate orbit membership with (mask weight, channel)
    label_by_orbit = defaultdict(list)
    for (mask, ch), t in found.items():
        for oi, orb in enumerate(orbits):
            if tuple(t) in orb:
                label_by_orbit[oi].append((sum(mask), ch))
    for oi, labels in sorted(label_by_orbit.items()):
        print(f"T3 orbit {oi}: (maskweight, channel) labels = "
              f"{sorted(labels)}")

    # T4: distinct root triples per rectangle? (involutions distinct =>
    # triples distinct as group elements; report)
    print(f"T4 lift -> involution injective on found lifts: "
          f"{distinct == len(found)}")

    out = {
        "theorem": "BT749 dihedral phase structure",
        "stab_pgsp_order": len(S),
        "outer_orders": {str(k): v for k, v in sorted(orders_out.items())},
        "is_D12": bool(dihedral),
        "lifts_with_involution_in_stab": len(found),
        "distinct_involutions": distinct,
        "z12_orbit_sizes": sorted(len(o) for o in orbits),
        "orbit_labels": {str(k): sorted(v)
                         for k, v in label_by_orbit.items()},
    }
    with open("data/bt749_dihedral_phase_selector.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt749_dihedral_phase_selector.json")


if __name__ == "__main__":
    main()
