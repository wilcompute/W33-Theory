#!/usr/bin/env python3
"""
BT858 - The 27 of 1+12+27: Heisenberg torsors and the Schlafli SRG,
        on both sides of the duality.

User hint honored: the 27 also comes from the repo's Heisenberg layer
(Pillar 69 Hessian H27 = F3^2 x F3; Pillar 72 [K,K] = extraspecial
3^{1+2} regular on 27 twin-pairs; Pillar 84 cocycle-Heisenberg bridge;
docs index 'Heisenberg/MUB shell': 27 non-neighbours = F3^3 shell with
9 fibres of 3, derived graph = Schlafli) and from an SRG related to
SRG(40,12,2,4).  Computed here, exactly:

  T1  POINT shell: the 27 points non-collinear with a base point p0.
      Suborbits of Stab(p0) on the shell; the fibre relation (same
      projective line through p0, 9 fibres of 3); induced collinearity
      (8-regular); the union = SRG(27,10,1,5) = GQ(2,4) collinearity
      (the 27 lines / E6 geometry), complement = SCHLAFLI
      SRG(27,16,10,8).
  T2  LINE shell (the Bell shell of the single-photon paper): the 27
      lines disjoint from a base line L0 - same analysis through the
      duality (line graph is again SRG(40,12,2,4)).
  T3  TORSOR THEOREM: in each shell, the normal 3-subgroup O_3 (order
      27) of the stabilizer acts REGULARLY - the shell is a torsor.
      Identify which shell carries the extraspecial Heisenberg
      3^{1+2} (exponent 3, |Z|=3) and which the elementary F3^3:
      the two dual parabolics 3^{1+2}:2A4 vs 3^3:S4.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
import random


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def srg_params(adjset, verts):
    Gd = {v: set() for v in verts}
    for a, b in adjset:
        Gd[a].add(b)
        Gd[b].add(a)
    degs = {len(Gd[v]) for v in verts}
    lam = {len(Gd[a] & Gd[b]) for a, b in combinations(verts, 2)
           if b in Gd[a]}
    mu = {len(Gd[a] & Gd[b]) for a, b in combinations(verts, 2)
          if b not in Gd[a]}
    return degs, lam, mu


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

    def order_of_perm(gp):
        o, cur = 1, gp
        while cur != ident:
            cur = compose(gp, cur)
            o += 1
        return o

    rng = random.Random(41)

    def group_type(H):
        ords = Counter(order_of_perm(gp) for gp in H)
        Hl = list(H)
        center = [g for g in Hl
                  if all(compose(g, x) == compose(x, g) for x in Hl)]
        if len(center) == 27:
            return ("elementary F3^3" if ords[9] == 0
                    else "abelian with 9s"), ords
        return (f"extraspecial 3^(1+2) exp "
                f"{'3 (Heisenberg)' if ords[9] == 0 else '9'}"), ords

    def shell_analysis(name, shell, stab, act):
        print(f"--- {name}: shell size {len(shell)}, "
              f"|stab| = {len(stab)} ---")
        s0 = shell[0]
        stab_s0 = [gp for gp in stab if act(gp, s0) == s0]
        # suborbits of Stab(s0)
        suborbs = []
        rem = set(shell) - {s0}
        while rem:
            seed = next(iter(rem))
            orb = {seed}
            fr = [seed]
            while fr:
                nx2 = []
                for x in fr:
                    for gp in stab_s0:
                        y = act(gp, x)
                        if y not in orb:
                            orb.add(y)
                            nx2.append(y)
                fr = nx2
            suborbs.append(sorted(orb))
            rem -= set(orb)
        sizes = sorted(len(o) for o in suborbs)
        print(f"  suborbits of Stab(base): {sizes}")

        # orbital graphs (symmetrized)
        orbitals = []
        for o in suborbs:
            edges = set()
            y0 = o[0]
            for gp in stab:
                a, b = act(gp, s0), act(gp, y0)
                edges.add(frozenset((a, b)))
            orbitals.append((len(o), edges))

        # all unions: find SRGs
        from itertools import chain, combinations as comb2
        found = []
        idxs = range(len(orbitals))
        for rset in chain.from_iterable(
                comb2(idxs, k) for k in range(1, len(orbitals))):
            E = set()
            for i in rset:
                E |= orbitals[i][1]
            edges = {tuple(sorted(e)) for e in E if len(e) == 2}
            degs, lam, mu = srg_params(edges, shell)
            if len(degs) == 1 and len(lam) <= 1 and len(mu) == 1:
                k_ = next(iter(degs))
                l_ = next(iter(lam)) if lam else 0
                m_ = next(iter(mu))
                sub_sizes = [orbitals[i][0] for i in rset]
                found.append((k_, l_, m_, sub_sizes))
                print(f"  SRG(27,{k_},{l_},{m_}) from suborbits "
                      f"{sub_sizes}")
        results = {"suborbits": sizes, "srgs": found}

        # canonical O_3: normal order-27 subgroup of stab
        threes = [gp for gp in stab if order_of_perm(gp) in (3, 9)]
        stab_set = set(stab)
        H_norm = None
        tries = 0
        while H_norm is None and tries < 6000:
            tries += 1
            gens3 = [rng.choice(threes) for _ in range(3 if tries % 2
                                                       else 2)]
            sub = {ident}
            fr = [ident]
            while fr and len(sub) <= 27:
                nx2 = []
                for x in fr:
                    for h in gens3:
                        y = compose(h, x)
                        if y not in sub:
                            sub.add(y)
                            nx2.append(y)
                fr = nx2
            if len(sub) != 27:
                continue
            # normality check against generators of stab (sample)
            ok = True
            for c in stab[:60]:
                inv = [0]*n
                for i in range(n):
                    inv[c[i]] = i
                inv = tuple(inv)
                if any(compose(compose(c, x), inv) not in sub
                       for x in list(sub)[:9]):
                    ok = False
                    break
            if ok:
                # complete normality check
                full = True
                for c in stab:
                    inv = [0]*n
                    for i in range(n):
                        inv[c[i]] = i
                    inv = tuple(inv)
                    if any(compose(compose(c, x), inv) not in sub
                           for x in sub):
                        full = False
                        break
                if full:
                    H_norm = sub
        if H_norm is not None:
            typ, ords = group_type(H_norm)
            orb0 = {act(gp, s0) for gp in H_norm}
            free = all(act(gp, s0) != s0
                       for gp in H_norm if gp != ident)
            reg = len(orb0) == 27 and free
            print(f"  O_3(stab) = {typ}, orders "
                  f"{dict(sorted(ords.items()))}, regular on shell: {reg}")
            results["O3_type"] = typ
            results["O3_regular"] = reg
        return results

    # ----- T1: point shell -----
    p0 = 0
    shell_pts = [x for x in range(n) if x != p0 and not adj[p0][x]]
    assert len(shell_pts) == 27
    stab_p = [gp for gp in psp if gp[p0] == p0]

    def act_pt(gp, x):
        return gp[x]

    r1 = shell_analysis("POINT shell (1+12+27 on points)",
                        shell_pts, stab_p, act_pt)

    # ----- T2: line shell (the Bell shell) -----
    L0 = 0
    shell_ln = [m for m in range(40) if m != L0
                and not (line_sets[m] & line_sets[L0])]
    assert len(shell_ln) == 27
    sl0 = lines[L0]
    stab_l = [gp for gp in psp
              if frozenset(gp[x] for x in sl0) == sl0]

    def act_ln(gp, m):
        return lperms[gp][m]

    r2 = shell_analysis("LINE shell (the Bell shell, 1+12+27 on lines)",
                        shell_ln, stab_l, act_ln)

    out = {"theorem": "BT858 Heisenberg shell torsors",
           "point_shell": r1, "line_shell": r2}
    with open("data/bt858_heisenberg_shell_torsors.json", "w") as fj:
        json.dump(out, fj, indent=2, default=str)
    print("\nwrote data/bt858_heisenberg_shell_torsors.json")


if __name__ == "__main__":
    main()
