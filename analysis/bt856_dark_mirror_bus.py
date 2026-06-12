#!/usr/bin/env python3
"""
BT856 - The dark charts ARE the mirror bus: (core, dark chart) slots
        = the 2160-slot D12 antipode G-set of BT815.

Counting seed: each pentad core carries 10 dark charts (BT854 shadow
matching); 216 cores x 10 = 2160 = the D12 mirror-bus slot count
(BT815: chart-transversal slots = antipode slots, stabilizer D12 with
profile {1:1, 2:7, 3:2, 6:2}).  Tested here over ALL 216 cores:

  T1  census: every one of the 540 skew pairs occurs as a dark chart
      in exactly 4 cores (2160 = 540 x 4 - the SAME factorization as
      the BT815 repair atlas 2160 = 540 x 4).
  T2  the stabilizer of one (core, dark chart) slot has order 12 with
      the D12 profile {1:1, 2:7, 3:2, 6:2} (=> orbit 25920/12 = 2160,
      transitive).
  T3  G-SET ISOMORPHISM: the slot stabilizer is CONJUGATE in PSp to
      the BT815 antipode-slot stabilizer (stabilizer of a
      (chart, transversal) pair), proven by direct search.
"""
from __future__ import annotations

from collections import Counter, defaultdict
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

    rng = random.Random(31)

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

    def line_orbit_parts(core):
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

    # ----- gather all 216 pentad cores and their dark charts -----
    chart_count = Counter()
    slot0 = None
    total = 0
    for si, S in enumerate(spreads):
        sset = frozenset(S)
        stab = [gp for gp in psp
                if frozenset(lperms[gp][li] for li in S) == sset]
        for core in all_A5(stab):
            parts = line_orbit_parts(core)
            sizes = sorted(len(p) for p in parts)
            if sizes != [5, 5, 10, 20]:
                continue
            o20 = next(p for p in parts if len(p) == 20)
            # shadow matching -> 10 dark charts
            byshadow = defaultdict(list)
            for li in o20:
                sh = frozenset(m for m in sset
                               if line_sets[li] & line_sets[m])
                byshadow[sh].append(li)
            assert len(byshadow) == 10
            for sh, pairlines in byshadow.items():
                assert len(pairlines) == 2
                a, b = pairlines
                assert not (line_sets[a] & line_sets[b])
                pr = frozenset((a, b))
                chart_count[pr] += 1
                total += 1
                if slot0 is None:
                    slot0 = (core, pr)
    print(f"T1 slots: {total} (= 216 x 10 = 2160)")
    assert total == 2160
    census = Counter(chart_count.values())
    print(f"T1 per-skew-pair census: {dict(census)} "
          f"(540 x 4 = 2160, the BT815 factorization)")
    assert census == {4: 540}

    # ----- T2: slot stabilizer -----
    core0, pr0 = slot0
    a0, b0 = tuple(pr0)
    stab_slot = []
    core0set = core0
    for gp in psp:
        lp = lperms[gp]
        if frozenset((lp[a0], lp[b0])) != pr0:
            continue
        # conjugation check: gp core0 gp^-1 == core0
        inv = [0]*n
        for i in range(n):
            inv[gp[i]] = i
        inv = tuple(inv)
        if all(compose(compose(gp, x), inv) in core0set for x in core0set):
            stab_slot.append(gp)
    prof = Counter(order_of(gp) for gp in stab_slot)
    print(f"T2 slot stabilizer: order {len(stab_slot)}, profile "
          f"{dict(sorted(prof.items()))}")
    assert len(stab_slot) == 12
    assert dict(prof) == {1: 1, 2: 7, 3: 2, 6: 2}
    print("   = D12 profile {1:1,2:7,3:2,6:2} => transitive on 2160")

    # ----- T3: conjugate to the BT815 antipode-slot stabilizer -----
    # BT815 slot = (chart, transversal): a skew pair {l,m} plus one of
    # its 4 common transversals t.
    l0, m0 = None, None
    for a, b in combinations(range(40), 2):
        if not (line_sets[a] & line_sets[b]):
            l0, m0 = a, b
            break
    trans = [t for t in range(40)
             if t not in (l0, m0)
             and line_sets[t] & line_sets[l0]
             and line_sets[t] & line_sets[m0]]
    t0 = trans[0]
    stab_815 = []
    pr815 = frozenset((l0, m0))
    for gp in psp:
        lp = lperms[gp]
        if frozenset((lp[l0], lp[m0])) == pr815 and lp[t0] == t0:
            stab_815.append(gp)
    prof815 = Counter(order_of(gp) for gp in stab_815)
    print(f"T3 BT815 antipode-slot stabilizer: order {len(stab_815)}, "
          f"profile {dict(sorted(prof815.items()))}")
    assert len(stab_815) == 12

    S1 = frozenset(stab_slot)
    S2 = frozenset(stab_815)
    conj = False
    for gp in psp:
        inv = [0]*n
        for i in range(n):
            inv[gp[i]] = i
        inv = tuple(inv)
        if all(compose(compose(gp, x), inv) in S2 for x in S1):
            conj = True
            break
    print(f"T3 stabilizers conjugate in PSp: {conj}")
    assert conj
    print("   => G-SET ISOMORPHISM: (core, dark chart) slots = the")
    print("      2160-slot D12 mirror bus - the dark sector feeds the")
    print("      middleware directly")

    out = {
        "theorem": "BT856 dark mirror bus",
        "t1": {"slots": total, "census": {str(k): v
                                          for k, v in census.items()}},
        "t2": {"stab_order": len(stab_slot),
               "profile": {str(k): v for k, v in sorted(prof.items())}},
        "t3": {"conjugate": conj},
    }
    with open("data/bt856_dark_mirror_bus.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt856_dark_mirror_bus.json")


if __name__ == "__main__":
    main()
