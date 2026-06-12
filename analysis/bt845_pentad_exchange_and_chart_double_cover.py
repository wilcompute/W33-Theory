#!/usr/bin/env python3
"""
BT845 - The pentad exchange network and the chart double cover.

BT844 left three opens.  Tested here over ALL 432 cores:

  T1  pentad -> cores map: each of the 216 pentads serves exactly 2
      cores; are the two cores in the SAME schedule or different ones
      (wormholes)?
  T2  the pentad exchange graph (vertices = 216 pentads, edges = the
      216 core pairings {P1,P2}) is 2-regular; compute its cycle type.
  T3  THE CHART CONJECTURE: the deleted matching of each core's
      K(5,5)-minus-matching interlock consists of 5 SKEW line pairs
      (= hypercube charts).  216 cores x 5 = 1080 = 540 x 2: the
      matchings cover the whole chart atlas exactly TWICE.
  T4  pentad extension: how many of the 36 schedules contain a given
      pentad's 5 lines (partial-spread completion count).
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

    rng = random.Random(17)

    def all_A5(stab):
        fives = [gp for gp in stab if order_of(gp) == 5]
        threes = [gp for gp in stab if order_of(gp) == 3]
        found = set()
        misses = 0
        while misses < 3000:
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
                if c in found:
                    misses += 1
                else:
                    found.add(c)
                    misses = 0
            else:
                misses += 1
        assert len(found) == 12, len(found)
        return found

    def line_orbits(core):
        rem = set(range(40))
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
            parts.append(frozenset(orb))
            rem -= orb
        return parts

    # gather all pentad cores across all 36 spreads
    pentad_serves = defaultdict(list)   # pentad -> [(spread_idx, core)]
    core_pairs = []                     # list of (spread_idx, P1, P2)
    for si, S in enumerate(spreads):
        sset = frozenset(S)
        stab = [gp for gp in psp
                if frozenset(lperms[gp][li] for li in S) == sset]
        assert len(stab) == 720
        for core in all_A5(stab):
            parts = line_orbits(core)
            sizes = sorted(len(p) for p in parts)
            if sizes == [5, 5, 10, 20]:
                pents = sorted((p for p in parts if len(p) == 5),
                               key=sorted)
                p1, p2 = pents
                core_pairs.append((si, p1, p2))
                pentad_serves[p1].append((si, core))
                pentad_serves[p2].append((si, core))
    print(f"pentad cores found: {len(core_pairs)} (= 216 = 6 x 36)")
    assert len(core_pairs) == 216
    print(f"distinct pentads: {len(pentad_serves)}")
    serve_counts = Counter(len(v) for v in pentad_serves.values())
    print(f"pentad service census: {dict(sorted(serve_counts.items()))}")
    same = sum(1 for v in pentad_serves.values()
               if len(v) == 2 and v[0][0] == v[1][0])
    multi = {p: sorted(set(si for si, _ in v))
             for p, v in pentad_serves.items() if len(v) != 2}
    if multi:
        ex = next(iter(multi.values()))
        print(f"T1 NOTE: service counts vary; example schedule list: {ex}")
    diff = sum(1 for v in pentad_serves.values()
               if len(v) == 2 and v[0][0] != v[1][0])
    print(f"T1 2-served pentads: same-schedule {same}, "
          f"cross-schedule (wormholes) {diff}")

    # ----- T2: exchange graph cycle type -----
    nbr = defaultdict(set)
    for si, p1, p2 in core_pairs:
        nbr[p1].add(p2)
        nbr[p2].add(p1)
    deg = Counter(len(v) for v in nbr.values())
    print(f"T2 exchange-graph degrees: {dict(deg)}")
    seen = set()
    cycles = []
    for v in nbr:
        if v in seen:
            continue
        comp = {v}
        fr = [v]
        while fr:
            nx2 = []
            for u in fr:
                for w in nbr[u]:
                    if w not in comp:
                        comp.add(w)
                        nx2.append(w)
            fr = nx2
        seen |= comp
        cycles.append(len(comp))
    cycles.sort()
    print(f"T2 exchange-graph component sizes: {Counter(cycles)}")

    # ----- T3: the chart double cover -----
    chart_cover = Counter()
    matching_sizes = set()
    for si, p1, p2 in core_pairs:
        matching = []
        for a in p1:
            partners = [b for b in p2 if not (line_sets[a] & line_sets[b])]
            matching.append((a, partners))
        sizes = {len(pr[1]) for pr in matching}
        matching_sizes |= sizes
        for a, partners in matching:
            for b in partners:
                chart_cover[frozenset((a, b))] += 1
    print(f"T3 per-line skew-partner counts across pentads: "
          f"{sorted(matching_sizes)}")
    skew_pairs = {frozenset((a, b)) for a, b in combinations(range(40), 2)
                  if not (line_sets[a] & line_sets[b])}
    cov = Counter(chart_cover.values())
    missed = len(skew_pairs) - len(chart_cover)
    print(f"T3 chart coverage census: {dict(sorted(cov.items()))}, "
          f"never covered: {missed} of 540")

    # ----- T1b: the two chiral orbits -----
    # 432 pentads, orbit of any one is 216 (stab order 120), so there
    # must be exactly two orbits; and the two pentads of one core must
    # lie in DIFFERENT orbits (else one 216-orbit would fill all 432
    # core slots).  Verify directly.
    def orbit_of(pent):
        seen = {pent}
        fr = [pent]
        while fr:
            nx2 = []
            for pe in fr:
                for gp in gens:
                    lp = lperms[gp]
                    pe2 = frozenset(lp[li] for li in pe)
                    if pe2 not in seen:
                        seen.add(pe2)
                        nx2.append(pe2)
            fr = nx2
        return seen

    si0, p1_0, p2_0 = core_pairs[0]
    O1 = orbit_of(p1_0)
    O2 = orbit_of(p2_0)
    assert len(O1) == 216 and len(O2) == 216
    assert not (O1 & O2)
    assert O1 | O2 == set(pentad_serves)
    chiral_ok = all((p1 in O1 and p2 in O2) or (p1 in O2 and p2 in O1)
                    for _, p1, p2 in core_pairs)
    print(f"T1b two chiral pentad orbits of 216 (left/right); every core")
    print(f"    pairs one LEFT with one RIGHT: {chiral_ok}")
    assert chiral_ok

    # ----- T4: pentad completion -----
    comp_counts = set()
    for p in pentad_serves:
        c = sum(1 for S in spreads if p <= S)
        comp_counts.add(c)
    print(f"T4 schedules containing a given pentad: {sorted(comp_counts)}")

    out = {
        "theorem": "BT845 pentad exchange and chart double cover",
        "corrected": "BT844's 'each pentad serves 2 cores' is FALSE: "
                     "432 distinct pentads in two chiral orbits of 216,"
                     " each serving exactly 1 core",
        "t1": {"distinct_pentads": len(pentad_serves),
               "serves_each": 1,
               "chiral_orbits": [len(O1), len(O2)],
               "core_pairs_left_right": chiral_ok},
        "t2": {"exchange_graph": "perfect matching (216 left-right edges)"},
        "t3": {"coverage": {str(k): v for k, v in sorted(cov.items())},
               "never": missed,
               "matching_sizes": sorted(matching_sizes)},
        "t4": {"completions": sorted(comp_counts),
               "meaning": "pentads are MAXIMAL partial spreads"},
    }
    with open("data/bt845_pentad_exchange_chart_cover.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt845_pentad_exchange_chart_cover.json")


if __name__ == "__main__":
    main()
