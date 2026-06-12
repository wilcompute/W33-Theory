#!/usr/bin/env python3
"""
BT860 - Bell-shell register arithmetic: the [4,4,6,12] relations are
        the S4-orbits of difference vectors in the F3^3 torsor.

BT858 made the Bell shell (27 lines disjoint from L0) a torsor under
the elementary F3^3 = O_3 of the line parabolic 3^3:S4, with Stab
suborbits [4,4,6,12] and no invariant SRG.  Here the relations are
NAMED, three ways at once:

  T1  REGISTER: fixing a base context M0 and an O_3-basis, every
      shell context gets a 3-trit address; the four relations are
      exactly the four S4-orbits of nonzero difference vectors in
      F3^3 (conjugation action of Stab(L0)/O_3 = S4) - pair relations
      = register-difference classes.
  T2  GEOMETRY: per relation, the census of (meet vs skew,
      |T(M) cap T(M')|) where T(M) is M's transversal tetrad onto L0
      (GQ axiom: T(M) is in bijection with L0's 4 points).
  T3  SHAPE: identify each S4-orbit on F3^3 by vector shape.
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

    L0 = 0
    sl0 = lines[L0]
    shell = [m for m in range(40) if m != L0
             and not (line_sets[m] & line_sets[L0])]
    assert len(shell) == 27
    stab = [gp for gp in psp if frozenset(gp[x] for x in sl0) == sl0]
    assert len(stab) == 648

    # find the normal elementary O_3 (3-generator random search)
    rng = random.Random(47)
    threes = [gp for gp in stab if order_of(gp) == 3]
    O3 = None
    while O3 is None:
        gs = [rng.choice(threes) for _ in range(3)]
        sub = {ident}
        fr = [ident]
        while fr and len(sub) <= 27:
            nx2 = []
            for x in fr:
                for h in gs:
                    y = compose(h, x)
                    if y not in sub:
                        sub.add(y)
                        nx2.append(y)
            fr = nx2
        if len(sub) != 27:
            continue
        if any(order_of(g) != 3 for g in sub if g != ident):
            continue
        if not all(compose(a, b) == compose(b, a)
                   for a, b in combinations(list(sub)[:6], 2)):
            continue
        # normality (complete)
        ok = True
        for c in stab:
            inv = [0]*n
            for i in range(n):
                inv[c[i]] = i
            inv = tuple(inv)
            if any(compose(compose(c, x), inv) not in sub for x in sub):
                ok = False
                break
        if ok:
            O3 = sub
    print("O_3 (elementary F3^3, normal) found")

    # basis and coordinates
    O3l = sorted(O3)
    basis = []
    span = {ident}
    for g in O3l:
        if g in span:
            continue
        basis.append(g)
        newspan = set()
        for x in span:
            cur = x
            for _ in range(3):
                newspan.add(cur)
                cur = compose(g, cur)
        span = newspan
        if len(span) == 27:
            break
    assert len(basis) == 3

    def coords(g):
        # brute force: g = a^i b^j c^k
        a, b, c = basis
        cur_i = ident
        for i in range(3):
            cur_j = cur_i
            for j in range(3):
                cur_k = cur_j
                for k in range(3):
                    if cur_k == g:
                        return (i, j, k)
                    cur_k = compose(c, cur_k)
                cur_j = compose(b, cur_j)
            cur_i = compose(a, cur_i)
        raise AssertionError

    # torsor addresses: shell context <- O3 element
    M0 = shell[0]
    addr = {}
    for g in O3:
        m = lperms[g][M0]
        addr[m] = coords(g)
    assert len(addr) == 27 and set(addr) == set(shell)
    print("T1 3-trit addresses assigned to all 27 Bell-shell contexts")

    # S4-orbits of nonzero vectors: conjugation action of stab on O3
    # difference classes via suborbits of Stab(M0)
    stab_M0 = [gp for gp in stab if lperms[gp][M0] == M0]
    suborbs = []
    rem = set(shell) - {M0}
    while rem:
        seed = next(iter(rem))
        orb = {seed}
        fr = [seed]
        while fr:
            nx2 = []
            for x in fr:
                for gp in stab_M0:
                    y = lperms[gp][x]
                    if y not in orb:
                        orb.add(y)
                        nx2.append(y)
            fr = nx2
        suborbs.append(sorted(orb))
        rem -= set(orb)
    suborbs.sort(key=len)
    print(f"T1 suborbit sizes: {[len(o) for o in suborbs]}")

    # difference classes: vector addresses of suborbit members
    def vsub(u, v):
        return tuple((u[i] - v[i]) % 3 for i in range(3))

    a0 = addr[M0]
    classes = []
    for o in suborbs:
        vecs = sorted(vsub(addr[m], a0) for m in o)
        classes.append(vecs)

    # T3: shapes (use weight = number of nonzero trits, up to sign)
    def shape(v):
        nz = sum(1 for x in v if x)
        return nz

    for o, vecs in zip(suborbs, classes):
        shapes = Counter(shape(v) for v in vecs)
        print(f"T3 suborbit {len(o)}: difference vectors {vecs[:4]}... "
              f"weights {dict(shapes)}")

    # verify: relation depends ONLY on difference class (test on all
    # pairs, not just base pairs): build class lookup by S4-orbit of
    # the difference
    vec_class = {}
    for ci, vecs in enumerate(classes):
        for v in vecs:
            vec_class[v] = ci
    ok_all = True
    # pair relation from geometry must be constant per class
    def tetrad(m):
        return frozenset(t for t in range(40)
                         if t not in (L0, m)
                         and line_sets[t] & line_sets[m]
                         and line_sets[t] & line_sets[L0])

    T = {m: tetrad(m) for m in shell}
    geo = defaultdict(Counter)
    for m1, m2 in combinations(shell, 2):
        d = vsub(addr[m1], addr[m2])
        ci = vec_class.get(d, vec_class.get(vsub(addr[m2], addr[m1])))
        meets = bool(line_sets[m1] & line_sets[m2])
        tt = len(T[m1] & T[m2])
        geo[ci][(meets, tt)] += 1
    print("T2 geometric census per register class:")
    summary = {}
    for ci in sorted(geo):
        size = len(classes[ci])
        cen = dict(geo[ci])
        uniform = len(cen) == 1
        print(f"   class {ci} (size {size}): {cen} "
              f"{'UNIFORM' if uniform else 'mixed'}")
        summary[f"class_{size}_{ci}"] = {str(k): v for k, v in cen.items()}
        if not uniform:
            ok_all = False

    out = {
        "theorem": "BT860 Bell-shell register arithmetic",
        "suborbit_sizes": [len(o) for o in suborbs],
        "geometry_uniform_per_class": ok_all,
        "census": summary,
    }
    with open("data/bt860_bell_shell_register_arithmetic.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt860_bell_shell_register_arithmetic.json")


if __name__ == "__main__":
    main()
