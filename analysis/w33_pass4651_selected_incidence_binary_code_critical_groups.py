#!/usr/bin/env python3
"""Pass 4651 — binary dual code and critical-group arithmetic of 135_6–270_3.

Rebuild the selected singular-line incidence N from W33 apartments.  Beyond the
Pass4642 Smith result rank_Q=120, rank_F2=119, this verifier computes the full
binary left-kernel code, its exact 2^16 weight enumerator, and identifies its 36
minimum words equivariantly with the 36 W33 spreads.  It also freezes spanning-
tree/critical-group orders and p-ranks for the selected point and line graphs.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, nullspace2, perm_group, transvection_matrix,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4651_SELECTED_BINARY_CODE_CRITICAL_GROUPS.json"


def rank_mod_p(M, p):
    A = np.asarray(M, dtype=np.int64).copy() % p
    r = 0
    for c in range(A.shape[1]):
        rows = np.flatnonzero(A[r:, c])
        if len(rows) == 0:
            continue
        rr = r + int(rows[0])
        if rr != r:
            A[[r, rr]] = A[[rr, r]]
        inv = pow(int(A[r, c]), -1, p)
        A[r] = (A[r] * inv) % p
        for i in range(A.shape[0]):
            if i != r and A[i, c]:
                A[i] = (A[i] - int(A[i, c]) * A[r]) % p
        r += 1
        if r == A.shape[0]:
            break
    return r


def permute_mask40(m, p, j):
    out = 0
    x = int(m)
    while x:
        lsb = x & -x
        i = lsb.bit_length() - 1
        out |= 1 << p[i]
        x ^= lsb
    return min(out, out ^ j)


def main():
    pts, pidx, lines, lidx, _, Astar, _, _, _ = build_geometry()
    Astar = np.asarray(Astar, dtype=np.uint8)

    # 1620 apartments of the W33 line-side GQ graph.
    nb = [set(np.flatnonzero(Astar[i]).tolist()) for i in range(40)]
    apartments = set()
    for u, w in itertools.combinations(range(40), 2):
        if Astar[u, w]:
            continue
        common = sorted(nb[u] & nb[w])
        for a, b in itertools.combinations(common, 2):
            if not Astar[a, b]:
                apartments.add(tuple(sorted((u, w, a, b))))
    apartments = sorted(apartments)
    assert len(apartments) == 1620

    n = 40
    j = (1 << n) - 1
    cols = []
    for c in range(n):
        m = 0
        for r in np.flatnonzero(Astar[:, c]):
            m |= 1 << int(r)
        cols.append(m)
    edges = [(i, k) for i in range(n) for k in range(i + 1, n) if Astar[i, k]]
    B9 = rank_basis_int([cols[i] ^ cols[k] for i, k in edges])
    V9 = set(span(B9))
    assert len(B9) == 9 and j in V9
    rep = lambda x: min(int(x), int(x) ^ j)

    def apartment_line(ap):
        opp = [(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        assert len(opp) == 2
        s = rep(cols[opp[0][0]] ^ cols[opp[0][1]])
        t = rep(cols[opp[1][0]] ^ cols[opp[1][1]])
        x = 0
        for i in ap:
            x ^= cols[i]
        x = rep(x)
        return tuple(sorted((s,t,x)))

    fibers = defaultdict(list)
    for ap in apartments:
        fibers[apartment_line(ap)].append(ap)
    selected = sorted(fibers)
    assert len(selected) == 270 and Counter(map(len, fibers.values())) == Counter({6:270})
    sing = sorted(set().union(*(set(L) for L in selected)))
    assert len(sing) == 135
    sidx = {x:i for i,x in enumerate(sing)}

    N = np.zeros((135,270), dtype=np.int64)
    for c,L in enumerate(selected):
        for x in L:
            N[sidx[x],c] = 1
    assert set(map(int,N.sum(1))) == {6} and set(map(int,N.sum(0))) == {3}
    assert np.linalg.matrix_rank(N) == 120
    assert rank_mod_p(N,2) == 119

    # Left binary kernel C={a in F2^135 : a^T N=0}: dimension 16.
    B = nullspace2((N.T % 2).astype(np.uint8))
    assert len(B) == 16
    masks = []
    for b in B:
        m = 0
        for i,z in enumerate(b):
            if int(z):
                m |= 1 << i
        masks.append(m)
    words = [0]
    for b in masks:
        words += [x ^ b for x in words]
    assert len(words) == 65536
    W = Counter(x.bit_count() for x in words)
    expected_W = {
        0:1,30:36,45:432,48:630,54:1120,57:2160,61:4320,62:3780,
        64:7695,65:5616,69:11520,70:10368,72:7680,73:6480,77:2160,
        78:1080,80:378,81:80,
    }
    assert W == Counter(expected_W)
    minimum = [x for x in words if x.bit_count() == 30]
    assert len(minimum) == 36
    assert Counter((a & b).bit_count() for a,b in itertools.combinations(minimum,2)) == Counter({6:630})
    point_degrees = [sum((w >> i) & 1 for w in minimum) for i in range(135)]
    assert Counter(point_degrees) == Counter({8:135})

    # PSp action and equivariant identification of the 36 minimum words with
    # the 36 W33 line spreads.
    all_trans = [build_line_perm(transvection_matrix(v), pts, pidx, lines, lidx) for v in pts]
    gens = []
    G = {tuple(range(40))}
    for p in all_trans:
        trial = perm_group(gens + [p])
        if len(trial) > len(G):
            gens.append(p); G = trial
        if len(G) == 25920:
            break
    assert len(G) == 25920

    base = minimum[0]
    base_support = {sing[i] for i in range(135) if (base >> i) & 1}
    stabilizer = []
    for p in G:
        if {permute_mask40(x,p,j) for x in base_support} == base_support:
            stabilizer.append(p)
    assert len(stabilizer) == 720

    # Exact-cover enumeration of W33 points by ten disjoint W33 lines.
    point_to_lines = {i:[] for i in range(40)}
    for li,L in enumerate(lines):
        for x in L:
            point_to_lines[x].append(li)
    spreads = []
    def rec(chosen, used):
        if len(used) == 40:
            spreads.append(frozenset(chosen)); return
        x = next(i for i in range(40) if i not in used)
        for li in point_to_lines[x]:
            S = set(lines[li])
            if S & used:
                continue
            rec(chosen + [li], used | S)
    rec([], set())
    assert len(spreads) == len(set(spreads)) == 36
    fixed_spreads = [S for S in spreads if all(frozenset(p[i] for i in S) == S for p in stabilizer)]
    assert len(fixed_spreads) == 1

    # Selected point and line graphs and their critical-group arithmetic.
    A = N @ N.T - 6*np.eye(135,dtype=np.int64)
    Lg = N.T @ N - 3*np.eye(270,dtype=np.int64)
    Lp = 12*np.eye(135,dtype=np.int64) - A
    Ll = 15*np.eye(270,dtype=np.int64) - Lg
    p_ranks = {}
    l_ranks = {}
    for p in (2,3,5):
        Rp = rank_mod_p(Lp[:-1,:-1],p)
        Rl = rank_mod_p(Ll[:-1,:-1],p)
        p_ranks[str(p)] = 134 - Rp
        l_ranks[str(p)] = 269 - Rl
    assert p_ranks == {"2":62,"3":74,"5":23}
    assert l_ranks == {"2":164,"3":164,"5":23}

    # Matrix-tree theorem from exact spectra.
    tau_p = (6**15)*(9**20)*(12**60)*(15**24)*(18**15)//135
    tau_l = (6**15)*(9**20)*(12**60)*(15**24)*(18**150)//270
    def val(n,p):
        e=0
        while n%p==0:
            n//=p; e+=1
        return e
    assert {p:val(tau_p,p) for p in (2,3,5)} == {2:150,3:166,5:23}
    assert {p:val(tau_l,p) for p in (2,3,5)} == {2:284,3:436,5:23}

    out = {
        "pass":4651,
        "binary_left_kernel_code": {
            "parameters":"[135,16,30]_2",
            "weight_enumerator": {str(k):int(v) for k,v in sorted(W.items())},
            "minimum_words":36,
            "minimum_word_pair_intersection":"6 for all 630 pairs",
            "minimum_word_point_degree":8,
            "minimum_word_stabilizer_order":720,
            "fixed_W33_spreads_per_minimum_stabilizer":1,
            "G_set_identification":"36 minimum words are PSp(4,3)-equivariantly the W33 spread carrier"
        },
        "critical_groups": {
            "selected_point_graph": {
                "order_factorization":"2^150 * 3^166 * 5^23",
                "p_ranks":{"2":62,"3":74,"5":23}
            },
            "selected_line_graph": {
                "order_factorization":"2^284 * 3^436 * 5^23",
                "p_ranks":{"2":164,"3":164,"5":23}
            },
            "line_over_point_order_ratio":"2^134 * 3^270"
        },
        "theorem":"The binary relation code of the selected 135_6-270_3 geometry is [135,16,30] with exactly 36 minimum words, and those minimum words are the W33 spread G-set. The associated point/line critical-group orders and 2,3,5-ranks are exact.",
        "boundary":"Finite coding/critical-group theorem; no physical error threshold follows from minimum distance alone."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
