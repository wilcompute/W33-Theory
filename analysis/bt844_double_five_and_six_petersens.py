#!/usr/bin/env python3
"""
BT844 - The double-five: pentad cores bisect spreads, and the six
        Petersens doubly cover K10 (the Schwenk impossibility,
        circumvented by the substrate).

BT843 found the pentad compass: the second A5 class with line orbits
[5,5,10,20].  First guess (pentads bisect the spread) REFUTED: all 12
A5 subgroups of a spread stabilizer are transitive on the spread's 10
lines.  The truth is better:

  T2  each spread's stabilizer S6 contains exactly 12 A5 subgroups -
      the two S6-classes, which are exactly the two PSp-classes:
      6 duad cores (full line signature [10,30]: spread + the rest)
      and 6 pentad cores (signature [5,5,10,20]: the 10-orbit IS the
      spread, and the OTHER 30 lines split 5+5+20).  Hence BOTH
      216-compasses fiber over the SAME 36 schedules: 36 x 12 = 432
      icosahedral cores in all, 12 per schedule.
  T1  the two pentads of a pentad core are 5-line constellations
      OUTSIDE the spread - their internal incidence structure is
      computed (disjointness profile, point coverage).
  T3  the 6 duad Petersen edge-sets cover each of the 45 line pairs
      exactly TWICE: 2.K10 = union of 6 Petersens.  Classical theorem
      (Schwenk 1983): K10 CANNOT be edge-partitioned into 3 Petersen
      graphs - the substrate realizes the best alternative, the double
      cover.
  T4  pentad-core pair orbits on the 45 spread pairs (the second
      splitting law); global pentad orbit census under PSp.
"""
from __future__ import annotations

from itertools import combinations, product
from collections import Counter
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
    assert len(lines) == 40
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
    psp = list(psp)

    def line_perm(gp):
        return tuple(line_index[frozenset(gp[x] for x in lines[li])]
                     for li in range(40))

    lperms = {gp: line_perm(gp) for gp in psp}

    def order_of(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    # all 36 spreads
    pt_lines = [[li for li in range(40) if i in line_sets[li]]
                for i in range(n)]
    spreads = []

    def cover(used, chosen):
        if len(chosen) == 10:
            spreads.append(frozenset(chosen))
            return
        r = min(set(range(n)) - used)
        for li in pt_lines[r]:
            if not (line_sets[li] & used):
                cover(used | line_sets[li], chosen + [li])

    cover(set(), [])
    assert len(spreads) == 36
    spread_set = set(spreads)

    # ----- T2: all A5 subgroups of one spread stabilizer -----
    S0 = sorted(spreads[0])
    sset = frozenset(S0)
    stab = [gp for gp in psp
            if frozenset(lperms[gp][li] for li in S0) == sset]
    assert len(stab) == 720

    rng = random.Random(13)
    fives = [gp for gp in stab if order_of(gp) == 5]
    threes = [gp for gp in stab if order_of(gp) == 3]
    cores = set()
    misses = 0
    while misses < 4000:
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
        if len(sub) == 60:
            c = frozenset(sub)
            if c in cores:
                misses += 1
            else:
                cores.add(c)
                misses = 0
        else:
            misses += 1
    print(f"T2 A5 subgroups found in Stab(spread): {len(cores)}")
    assert len(cores) == 12

    def line_orbits(core):
        rem = set(range(40))
        sizes = []
        parts = []
        while rem:
            seed = next(iter(rem))
            orb = {seed}
            fr = [seed]
            while fr:
                nxt = []
                for li in fr:
                    for gp in core:
                        li2 = lperms[gp][li]
                        if li2 not in orb:
                            orb.add(li2)
                            nxt.append(li2)
                fr = nxt
            sizes.append(len(orb))
            parts.append(frozenset(orb))
            rem -= orb
        return sorted(sizes), parts

    duad_cores, pentad_cores = [], []
    pentad_pairs = []
    for c in cores:
        sizes, parts = line_orbits(c)
        if sizes == [10, 30]:
            duad_cores.append(c)
        elif sizes == [5, 5, 10, 20]:
            pentad_cores.append(c)
            pents = [p for p in parts if len(p) == 5]
            ten = next(p for p in parts if len(p) == 10)
            assert ten == sset      # the 10-orbit IS the spread
            pentad_pairs.append(frozenset(pents))
        else:
            raise AssertionError(sizes)
    print(f"T2 duad cores [10,30]: {len(duad_cores)}, "
          f"pentad cores [5,5,10,20]: {len(pentad_cores)}")
    assert len(duad_cores) == 6 and len(pentad_cores) == 6
    print("   both PSp classes stabilize the SAME spread: 12 cores per")
    print("   schedule, 432 = 36 x 12 icosahedral cores in all; the")
    print("   pentad core's 10-orbit IS the spread, pentads live OUTSIDE")

    # ----- T1: internal structure of a pentad -----
    prof_in = Counter()
    cover_sizes = set()
    skew_profile = Counter()
    for pp in pentad_pairs:
        for pent in pp:
            ls = sorted(pent)
            for a, b in combinations(ls, 2):
                skew_profile[len(line_sets[a] & line_sets[b])] += 1
            u = set()
            for li in ls:
                u |= line_sets[li]
            cover_sizes.add(len(u))
        p1, p2 = tuple(pp)
        prof_in[len(p1 & p2)] += 1
    print(f"T1 pentad internal line-meet profile: "
          f"{dict(sorted(skew_profile.items()))}, "
          f"point coverage sizes: {sorted(cover_sizes)}")

    # T1b: how do the two pentads of one core interlock?  (They cannot
    # be cross-disjoint: P1 u P2 would be a 10-line spread sharing 0
    # lines with S0, violating the BT835 overlap law 1-or-4.)
    cross = Counter()
    for pp in pentad_pairs:
        p1, p2 = tuple(pp)
        for a in p1:
            meets = sum(1 for b in p2 if line_sets[a] & line_sets[b])
            cross[meets] += 1
    print(f"T1b cross-pentad meet degrees (per line of P1 into P2): "
          f"{dict(sorted(cross.items()))}")

    # ----- T3: six Petersens doubly cover K10 -----
    pair_cover = Counter()
    for c in duad_cores:
        pairs = {frozenset(p) for p in combinations(S0, 2)}
        rem = set(pairs)
        while rem:
            seed = next(iter(rem))
            orb = set()
            a0, b0 = tuple(seed)
            for gp in c:
                lp = lperms[gp]
                orb.add(frozenset((lp[a0], lp[b0])))
            if len(orb) == 15:
                for pr in orb:
                    pair_cover[pr] += 1
            rem -= orb
    assert Counter(pair_cover.values()) == {2: 45}
    print("T3 the 6 duad Petersen edge-sets cover all 45 pairs EXACTLY")
    print("   twice: 2.K10 = 6 Petersens (Schwenk: 1.K10 = 3 Petersens")
    print("   is impossible - the substrate does the best possible)")

    # ----- T4: pentad-core pair orbits on the 45 spread pairs -----
    pent_splits = Counter()
    pent_pair_cover = Counter()
    for c in pentad_cores:
        pairs = {frozenset(p) for p in combinations(S0, 2)}
        rem = set(pairs)
        szs = []
        for_orbits = []
        while rem:
            seed = next(iter(rem))
            orb = set()
            a0, b0 = tuple(seed)
            for gp in c:
                lp = lperms[gp]
                orb.add(frozenset((lp[a0], lp[b0])))
            szs.append(len(orb))
            for_orbits.append(orb)
            rem -= orb
        pent_splits[tuple(sorted(szs))] += 1
        for orb in for_orbits:
            if len(orb) == min(szs):
                for pr in orb:
                    pent_pair_cover[pr] += 1
    print(f"T4 pentad-core pair-orbit signatures on the 45 spread pairs: "
          f"{dict(pent_splits)}")

    # T4b: is the pentad core's 15-orbit ALSO a Petersen graph, and do
    # the 12 cores' 15-orbits cover each pair exactly 4 = mu times?
    def srg_profile(edge_set, verts):
        Gd = {v: set() for v in verts}
        for pr in edge_set:
            a, b = tuple(pr)
            Gd[a].add(b)
            Gd[b].add(a)
        degs = {len(Gd[v]) for v in verts}
        lm = {len(Gd[a] & Gd[b]) for a, b in combinations(verts, 2)
              if b in Gd[a]}
        mm = {len(Gd[a] & Gd[b]) for a, b in combinations(verts, 2)
              if b not in Gd[a]}
        return degs, lm, mm

    all12_cover = Counter(pair_cover)   # start from the 6 duad Petersens
    pent_petersen = True
    for c in pentad_cores:
        pairs = {frozenset(p) for p in combinations(S0, 2)}
        rem = set(pairs)
        while rem:
            seed = next(iter(rem))
            orb = set()
            a0, b0 = tuple(seed)
            for gp in c:
                lp = lperms[gp]
                orb.add(frozenset((lp[a0], lp[b0])))
            if len(orb) == 15:
                degs, lm, mm = srg_profile(orb, S0)
                if not (degs == {3} and lm == {0} and mm == {1}):
                    pent_petersen = False
                for pr in orb:
                    all12_cover[pr] += 1
            rem -= orb
    print(f"T4b pentad-core 15-orbits are Petersen graphs: {pent_petersen}")
    assert pent_petersen
    cov12 = Counter(all12_cover.values())
    print(f"T4b coverage of the 45 pairs by ALL 12 Petersens: {dict(cov12)}")
    assert cov12 == {4: 45}
    print("    => 4.K10 = 12 Petersens: each pair covered exactly mu = 4")

    # global pentad orbit census under PSp
    pent0 = next(iter(next(iter(pentad_pairs))))
    seen = {pent0}
    fr = [pent0]
    while fr:
        nxt = []
        for pe in fr:
            for gp in gens:
                lp = lperms[gp]
                pe2 = frozenset(lp[li] for li in pe)
                if pe2 not in seen:
                    seen.add(pe2)
                    nxt.append(pe2)
        fr = nxt
    print(f"T4 pentad orbit size: {len(seen)} "
          f"(stab order {25920 // len(seen)})")
    # pentad-pair (the core's {P1,P2}) orbit
    pp0 = next(iter(pentad_pairs))
    bseen = {pp0}
    fr = [pp0]
    while fr:
        nxt = []
        for bs in fr:
            for gp in gens:
                lp = lperms[gp]
                bs2 = frozenset(frozenset(lp[li] for li in pe) for pe in bs)
                if bs2 not in bseen:
                    bseen.add(bs2)
                    nxt.append(bs2)
        fr = nxt
    print(f"T4 pentad-PAIR orbit size: {len(bseen)} "
          f"(stab order {25920 // len(bseen)})")
    # are the 6 pentad-pairs of one spread distinct?
    print(f"T4 distinct pentad-pairs in one spread: "
          f"{len(set(pentad_pairs))} of 6")

    out = {
        "theorem": "BT844 double-five and six Petersens",
        "refuted": "pentads bisect the spread - FALSE; pentads live on"
                   " the 30 lines outside",
        "t2": {"a5_in_stab": 12, "duad": 6, "pentad": 6,
               "total_cores": 432},
        "t1": {"pentad_meet_profile":
               {str(k): v for k, v in sorted(skew_profile.items())},
               "pentad_point_coverage": sorted(cover_sizes)},
        "t3": "2.K10 = 6 Petersens (each pair covered exactly 2x)",
        "t4": {"pair_orbit_signatures":
               {str(k): v for k, v in pent_splits.items()},
               "pentad_orbit": len(seen),
               "pentad_pair_orbit": len(bseen),
               "distinct_pairs_per_spread": len(set(pentad_pairs))},
    }
    with open("data/bt844_double_five_six_petersens.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt844_double_five_six_petersens.json")


if __name__ == "__main__":
    main()
