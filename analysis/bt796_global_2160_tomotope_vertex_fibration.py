#!/usr/bin/env python3
"""
BT796 - Global 2160 chart-transversal fibration.

A slot is (skew chart, common isotropic transversal).  Since W(3,3) has
540 skew charts and each chart has four common transversals, there are 2160
slots.  Under PSp(4,3), this is one transitive G-set with stabilizer order 12.
Each W33 line appears as a transversal in exactly 54 slots.
"""
from __future__ import annotations
from itertools import product, combinations
from collections import Counter, deque
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def points():
    return sorted({canon(v) for v in product(range(3), repeat=4) if v != (0, 0, 0, 0)})


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def transvection_perm(v, pts, pt_index):
    out = []
    for x in pts:
        w = symp(x, v)
        out.append(pt_index[canon(tuple((x[k] + w*v[k]) % 3 for k in range(4)))])
    return tuple(out)


def build_psp(pts, pt_index):
    seeds = [
        canon((1,0,0,0)), canon((0,1,0,0)), canon((0,0,1,0)), canon((0,0,0,1)),
        canon((1,1,0,0)), canon((1,0,1,0)), canon((1,0,0,1)), canon((0,1,1,0)),
    ]
    gens = [transvection_perm(v, pts, pt_index) for v in seeds]
    ident = tuple(range(len(pts)))
    group = {ident}
    q = deque([ident])
    while q:
        g = q.popleft()
        for h in gens:
            gh = compose(h, g)
            if gh not in group:
                group.add(gh)
                q.append(gh)
    assert len(group) == 25920
    return list(group), gens


def order_perm(p):
    ident = tuple(range(len(p)))
    cur = p
    k = 1
    while cur != ident:
        cur = compose(p, cur)
        k += 1
    return k


def main():
    pts = points()
    pt_index = {p: i for i, p in enumerate(pts)}
    adj = [[False]*40 for _ in range(40)]
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(40), 4) if all(adj[i][j] for i, j in combinations(q, 2))]
    lines.sort(key=lambda L: sorted(L))
    line_sets = [set(L) for L in lines]
    line_key = {tuple(sorted(L)): i for i, L in enumerate(lines)}
    skew = [(i, j) for i, j in combinations(range(40), 2) if not (line_sets[i] & line_sets[j])]
    skew_index = {frozenset(p): k for k, p in enumerate(skew)}

    def line_perm(g):
        return tuple(line_key[tuple(sorted(g[x] for x in L))] for L in lines)

    trans = []
    for a, b in skew:
        tv = tuple(k for k in range(40) if k not in (a, b) and line_sets[k] & line_sets[a] and line_sets[k] & line_sets[b])
        assert len(tv) == 4
        trans.append(tv)
    slots = [(s, t) for s, tv in enumerate(trans) for t in tv]
    assert len(slots) == 2160
    multiplicity = Counter(t for s, t in slots)
    assert Counter(multiplicity.values()) == {54: 40}

    group, gens = build_psp(pts, pt_index)
    gen_lps = [line_perm(g) for g in gens]
    base = slots[0]

    seen = {base}
    q = deque([base])
    while q:
        s, t = q.popleft()
        a, b = skew[s]
        for lp in gen_lps:
            ns = skew_index[frozenset((lp[a], lp[b]))]
            nt = lp[t]
            y = (ns, nt)
            if y not in seen:
                seen.add(y)
                q.append(y)
    assert len(seen) == 2160

    stabilizer = []
    base_s, base_t = base
    base_a, base_b = skew[base_s]
    for g in group:
        lp = line_perm(g)
        if {lp[base_a], lp[base_b]} == {base_a, base_b} and lp[base_t] == base_t:
            stabilizer.append(lp)
    assert len(stabilizer) == 12
    order_profile = {str(k): v for k, v in sorted(Counter(order_perm(g) for g in stabilizer).items())}
    assert order_profile == {"1": 1, "2": 7, "3": 2, "6": 2}

    out = {
        "theorem": "BT796 global 2160 chart-transversal fibration",
        "charts": len(skew),
        "transversal_slots_per_chart": 4,
        "slot_count": len(slots),
        "line_multiplicity_profile": {str(k): v for k, v in sorted(Counter(multiplicity.values()).items())},
        "group_order": len(group),
        "orbit_count_under_generators": len(seen),
        "is_transitive_G_set": True,
        "slot_stabilizer_order": len(stabilizer),
        "slot_stabilizer_order_profile": order_profile,
        "orbit_stabilizer_check": "25920 = 2160 * 12",
        "interpretation": "The 2160 chart-transversal slots are a single PSp(4,3) fibration object; every W33 line occurs as transversal in exactly 54 slots."
    }
    path = ROOT / "data" / "bt796_global_2160_tomotope_vertex_fibration.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
