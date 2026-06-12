#!/usr/bin/env python3
"""
BT848 - The amalgamation ladder: why the 11-cell and 57-cell are the
        universal completions of the substrate's compass geometry.

Background (research, June 2026): the 11-cell and 57-cell are UNIVERSAL
abstract polytopes - the unique polytopes with hemi-icosahedral facets
/ hemi-dodecahedral vertex figures (group L2(11), no proper quotients)
and vice versa (group L2(19)).  Hartley's classification: exactly 17
universal rank-4 locally projective polytopes, 441 quotients in all.
The mixed amalgam {{5,3},{3,5}_5} is finite with group J1 x L2(19)
(|.| = 600415200; facets = /60 = 10006920, vertices = /120 = 5003460 -
the Wikipedia numbers), J1 = first Janko sporadic, whose involution
centralizer is 2 x A5: icosahedral.

GAP witnesses (.tmp/gap_bt848_amalgam.g, gap_bt848b_amalgam_closure.g):

  A5-class intersection profiles (all three groups have TWO A5 classes):
    L2(11): within {6:10}; cross {10:6, 12:5}
       -> 11-cell vertex-facet incidence = D10-intersection (6/facet)
    L2(19): within {2:30, 3:20, 10:6}; cross {2:30, 5:12, 6:10, 12:5}
       -> PERKEL graph (57-cell facet adjacency) = within-class D10 (6-reg)
       -> vertex-on-facet = cross S3 (10/facet)
    U4(2): cross {1:60, 2:150, 10:6} - SAME D10 signature, 6-regular
       both ways: bipartite incidence on 216+216 with 216x6 = 1296 = 6^4
       edges = 36 schedules x 36 core pairs.

  THE TRIPLE CLOSURE (D10-pair subgroup closures):
    L2(11) cross D10 pair  generates  PSL(2,11) = 660   (the 11-cell)
    L2(19) Perkel D10 pair generates  PSL(2,19) = 3420  (the 57-cell)
    U4(2)  cross D10 pair  generates  A6 = PSL(2,9) = 360, inside
           EXACTLY ONE spread stabilizer (incidence = cohabiting a
           unique schedule; closure = the schedule's core).

  One icosahedral amalgam A5 *_{D10} A5, three completions:
       L2(9) = A6   (substrate, q = 3)
       L2(11)       (11-cell, the Ihara prime k-1)
       L2(19)       (57-cell, the Heawood prime, H(19) = 20)
  and the universal cover of the mixed amalgam adjoins J1.

Python here: the face-completion witness.  The compass Petersen
15-orbit is not just the hemi-dodecahedron SKELETON - under the
compass A5 its 12 pentagons split into two orbits of 6, EACH a valid
hemi-dodecahedral face set (every edge in exactly 2 faces): every
compass needle carries TWO chiral hemi-dodecahedra, fully faced.
"""
from __future__ import annotations

from itertools import combinations, product
import json
import random


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    line_index = {l: i for i, l in enumerate(lines)}
    line_sets = [set(l) for l in lines]

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[t] + w * v[t]) % 3 for t in range(4)))])
        return tuple(out)

    gens = [transvection_perm(v) for v in pts]
    ident = tuple(range(n))

    def compose(a, b):
        return tuple(a[b[i]] for i in range(n))

    psp = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for gp in frontier:
            for h in gens:
                gh = compose(h, gp)
                if gh not in psp:
                    psp.add(gh)
                    nxt.append(gh)
        frontier = nxt
    assert len(psp) == 25920

    def line_perm(gp):
        return tuple(line_index[frozenset(gp[x] for x in lines[li])]
                     for li in range(40))

    def order_of(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    spread = None

    def bt(used, chosen, start):
        nonlocal spread
        if spread:
            return
        if len(chosen) == 10:
            spread = list(chosen)
            return
        for li in range(start, 40):
            if not (line_sets[li] & used):
                bt(used | line_sets[li], chosen + [li], li + 1)

    bt(set(), [], 0)
    sset = frozenset(spread)
    lperms = {gp: line_perm(gp) for gp in psp}
    stab = [gp for gp in psp
            if frozenset(lperms[gp][li] for li in spread) == sset]

    rng = random.Random(5)
    fives = [gp for gp in stab if order_of(gp) == 5]
    threes = [gp for gp in stab if order_of(gp) == 3]
    A5, o15 = None, None
    while A5 is None:
        g5, g3 = rng.choice(fives), rng.choice(threes)
        sub = {ident}
        fr = [ident]
        while fr and len(sub) <= 60:
            nxt = []
            for x in fr:
                for h in (g5, g3):
                    y = compose(h, x)
                    if y not in sub:
                        sub.add(y)
                        nxt.append(y)
            fr = nxt
        if len(sub) != 60:
            continue
        cand = frozenset(sub)
        # need a duad core: pair orbits [15,30] with Petersen 15
        pairs = {frozenset(p) for p in combinations(sorted(spread), 2)}
        rem = set(pairs)
        got = None
        while rem:
            seed = next(iter(rem))
            orb = set()
            a0, b0 = tuple(seed)
            for gp in cand:
                lp = lperms[gp]
                orb.add(frozenset((lp[a0], lp[b0])))
            if len(orb) == 15:
                got = orb
            rem -= orb
        if got:
            A5, o15 = cand, got
    print("compass + Petersen 15-orbit found")

    # Petersen graph on the 10 spread lines
    G = {li: set() for li in spread}
    for pr in o15:
        a, b = tuple(pr)
        G[a].add(b)
        G[b].add(a)

    # enumerate 5-cycles
    pents = set()
    verts = sorted(spread)
    for v0 in verts:
        stack = [(v0, [v0])]
        while stack:
            cur, path = stack.pop()
            if len(path) == 5:
                if v0 in G[cur]:
                    pents.add(frozenset(
                        frozenset((path[i], path[(i+1) % 5]))
                        for i in range(5)))
                continue
            for w in G[cur]:
                if w not in path and w > v0:
                    stack.append((w, path + [w]))
    # frozenset of edges identifies a pentagon
    pents = list(pents)
    print(f"pentagons in the compass Petersen graph: {len(pents)}")
    assert len(pents) == 12

    # A5-orbits on the pentagons
    def act_pent(gp, pe):
        lp = lperms[gp]
        return frozenset(frozenset((lp[a], lp[b])) for a, b in
                         (tuple(e) for e in pe))

    orbs = []
    rem = set(pents)
    while rem:
        seed = next(iter(rem))
        orb = set()
        for gp in A5:
            orb.add(act_pent(gp, seed))
        orbs.append(orb)
        rem -= orb
    sizes = sorted(len(o) for o in orbs)
    print(f"A5-orbits on the 12 pentagons: {sizes}")
    assert sizes == [6, 6]

    # each orbit = hemi-dodecahedral face set (every edge in exactly 2)
    ok = []
    for orb in orbs:
        cover = {}
        for pe in orb:
            for e in pe:
                cover[e] = cover.get(e, 0) + 1
        ok.append(set(cover.values()) == {2} and len(cover) == 15)
    print(f"each 6-orbit covers each of the 15 edges exactly twice: {ok}")
    assert all(ok)
    print("=> every compass needle carries TWO CHIRAL fully-faced")
    print("   hemi-dodecahedra {5,3}_5 (not merely the skeleton)")

    out = {
        "theorem": "BT848 universal amalgam ladder",
        "research": {
            "universal_rank4_locally_projective": 17,
            "quotients_total": 441,
            "eleven_cell": "universal, no proper quotients, L2(11)",
            "fifty_seven_cell": "universal, L2(19); skeleton = Perkel",
            "mixed_universal_group": "J1 x L2(19), order 600415200",
            "mixed_facets": 10006920,
            "J1_involution_centralizer": "2 x A5",
        },
        "gap": {
            "L2_11_cross_profile": {"10": 6, "12": 5},
            "L2_19_within_profile": {"2": 30, "3": 20, "10": 6},
            "U4_2_cross_profile": {"1": 60, "2": 150, "10": 6},
            "closures": {
                "L2(11) cross D10": 660,
                "L2(19) within D10 (Perkel)": 3420,
                "U4(2) cross D10": 360,
            },
            "U4_2_closure_in_spread_stabs": 1,
        },
        "python": {"pentagons": 12, "a5_orbits": sizes,
                   "chiral_face_sets": True},
    }
    with open("data/bt848_universal_amalgam_ladder.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt848_universal_amalgam_ladder.json")


if __name__ == "__main__":
    main()
