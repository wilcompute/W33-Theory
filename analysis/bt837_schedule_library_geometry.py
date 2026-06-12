#!/usr/bin/env python3
"""
BT837 - The schedule library is itself a classical geometry.

BT836 put a Petersen graph (hemi-dodecahedron skeleton) inside every
schedule via the icosahedral core A5.  Three exact coincidences fall
out of the counting and are tested here:

  T1  36 schedules x 45 internal line pairs = 1620 = #apartments,
      and every skew line pair of W(3,3) lies in EXACTLY 3 schedules
      (540 x 3 = 1620).
  T2  the near-partner graph (two schedules sharing 4 lines) on the
      36 schedules is strongly regular SRG(36,15,6,6) - the OTHER
      classical rank-3 graph of U4(2) = PSp(4,3): the timetable
      library carries its own polar-space geometry.
  T3  Petersen homes: per spread, the icosahedral cores A5 give a
      set of distinct [15,30] splits; census of how many
      (schedule, core)-Petersen structures each skew pair belongs to.
      36 x 15 = 540 = #skew pairs = #hypercube charts.
"""
from __future__ import annotations

from itertools import combinations, product
from collections import Counter, defaultdict
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

    # all 36 spreads by exact cover
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
    print(f"schedules: {len(spreads)} (all regular spreads)")

    # ----- T1: skew pairs and the apartment count -----
    skew = [frozenset((a, b)) for a, b in combinations(range(40), 2)
            if not (line_sets[a] & line_sets[b])]
    assert len(skew) == 540
    in_spreads = Counter()
    for S in spreads:
        for pr in combinations(sorted(S), 2):
            in_spreads[frozenset(pr)] += 1
    census = Counter(in_spreads.values())
    assert set(in_spreads) == set(skew)
    assert census == {3: 540}
    print("T1 every skew line pair lies in EXACTLY 3 schedules;")
    print("   36 x 45 = 1620 (schedule,pair) flags = #apartments = 540 x 3")

    # ----- T2: near-partner graph is SRG(36,15,6,6) -----
    G = {i: set() for i in range(36)}
    for a, b in combinations(range(36), 2):
        ov = len(spreads[a] & spreads[b])
        assert ov in (1, 4)
        if ov == 4:
            G[a].add(b)
            G[b].add(a)
    degs = {len(G[v]) for v in G}
    assert degs == {15}
    lam = {
        len(G[u] & G[v])
        for u, v in combinations(range(36), 2)
        if v in G[u]
    }
    mu_ = {len(set(G[u]) & set(G[v]))
           for u, v in combinations(range(36), 2) if v not in G[u]}
    print(f"T2 near-graph: 36 vertices, 15-regular, lambda={lam}, mu={mu_}")
    assert lam == {6} and mu_ == {6}
    print("   => SRG(36,15,6,6): the U4(2) rank-3 graph - the timetable")
    print("      library is itself a classical strongly regular geometry")

    # ----- T3: Petersen homes -----
    # psp action on lines and spreads
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

    rng = random.Random(11)

    def find_A5(stab):
        fives = [gp for gp in stab if order_of(gp) == 5]
        threes = [gp for gp in stab if order_of(gp) == 3]
        while True:
            g5, g3 = rng.choice(fives), rng.choice(threes)
            sub = {ident}
            frontier = [ident]
            while frontier and len(sub) <= 60:
                nxt = []
                for x in frontier:
                    for h in (g5, g3):
                        y = compose(h, x)
                        if y not in sub:
                            sub.add(y)
                            nxt.append(y)
                frontier = nxt
            if len(sub) == 60:
                return frozenset(sub)

    def splits_of_spread(S):
        """distinct [15,30] pair-splits from all icosahedral A5 cores."""
        sset = frozenset(S)
        stab = [gp for gp in psp
                if frozenset(lperms[gp][li] for li in S) == sset]
        assert len(stab) == 720
        A5 = find_A5(stab)
        # all conjugates of A5 in stab
        stabset = set(stab)
        splits = set()
        seen_cores = set()
        for c in stab:
            cinv = tuple(sorted(range(n), key=lambda i: c[i]))
            cinv = [0]*n
            for i in range(n):
                cinv[c[i]] = i
            cinv = tuple(cinv)
            core = frozenset(compose(compose(c, a), cinv) for a in A5)
            if core in seen_cores:
                continue
            seen_cores.add(core)
            # 15-orbit of this core on pairs
            pairs = {frozenset(p) for p in combinations(sorted(S), 2)}
            orbits = []
            rem = set(pairs)
            while rem:
                seed = next(iter(rem))
                orb = set()
                a0, b0 = tuple(seed)
                for gp in core:
                    lp = lperms[gp]
                    orb.add(frozenset((lp[a0], lp[b0])))
                orbits.append(orb)
                rem -= orb
            sizes = sorted(len(o) for o in orbits)
            assert sizes == [15, 30], sizes
            o15 = next(o for o in orbits if len(o) == 15)
            splits.add(frozenset(o15))
        return seen_cores, splits

    cores0, splits0 = splits_of_spread(sorted(spreads[0]))
    print(f"T3 spread 0: {len(cores0)} icosahedral A5 cores, "
          f"{len(splits0)} distinct Petersen splits")

    # T3b: within one schedule each pair is Petersen under exactly 2 of
    # the 6 cores (forced: S6 permutes the cores and is transitive on
    # the 45 pairs, and 6 x 15 = 45 x 2)
    per_pair0 = Counter()
    for sp in splits0:
        for pr in sp:
            per_pair0[pr] += 1
    assert Counter(per_pair0.values()) == {2: 45}
    print("T3b within a schedule every pair is a Petersen edge under")
    print("    exactly 2 of the 6 cores (6x15 = 45x2); with T1 this gives")
    print("    the global census 3 schedules x 2 cores = 6 Petersen homes")

    # global census over all 36 spreads
    home = Counter()      # skew pair -> number of (spread,split) Petersen hits
    ncores, nsplits = [], []
    for si, S in enumerate(spreads):
        cs, sps = splits_of_spread(sorted(S))
        ncores.append(len(cs))
        nsplits.append(len(sps))
        for sp in sps:
            for pr in sp:
                home[pr] += 1
    print(f"T3 cores per spread: {sorted(set(ncores))}, "
          f"splits per spread: {sorted(set(nsplits))}")
    hcensus = Counter(home.values())
    nzero = 540 - len(home)
    print(f"T3 Petersen-home census over the 540 skew pairs: "
          f"{dict(sorted(hcensus.items()))}, never-Petersen: {nzero}")
    total_flags = sum(home.values())
    print(f"   total Petersen flags = {total_flags} "
          f"= 36 x {nsplits[0]} x 15" if len(set(nsplits)) == 1 else "")

    out = {
        "theorem": "BT837 schedule library geometry",
        "t1": {"skew_pairs": 540, "per_pair_schedules": 3,
               "flags": 1620, "apartments": 1620},
        "t2": {"srg": [36, 15, 6, 6]},
        "t3": {"cores_per_spread": sorted(set(ncores)),
               "splits_per_spread": sorted(set(nsplits)),
               "home_census": {str(k): v for k, v in sorted(hcensus.items())},
               "never_petersen": nzero,
               "total_flags": total_flags},
    }
    with open("data/bt837_schedule_library_geometry.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt837_schedule_library_geometry.json")


if __name__ == "__main__":
    main()
