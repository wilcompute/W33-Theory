#!/usr/bin/env python3
"""Passes 6533--6540: the doily quadratic-evaluation code and code-internal S6 outer automorphism.

This verifier packages the recent W(3,2) hyperplane census, quadratic-refinement
orbit, and explicit S6 dictionary into one canonical binary code.

Let V = F_2^4 with symplectic form
    B(x,z) = x1*z1 + z1*x1 + x2*z2 + z2*x2,
and q0(x)=x1*z1+x2*z2.  On the 15 nonzero vectors define
    C = { (B(a,x) + t q0(x))_{x != 0} : a in V, t in F_2 }.

The finite checks below prove:
  * C is [15,5,6]_2 with W_C(y)=1+10 y^6+15 y^8+6 y^10.
  * The 15 weight-8 words are exactly the nonzero words of the canonical
    [15,4,8] simplex subcode S={B(a,.)}; C=S + <q0>.
  * C^perp is [15,10,3], and its 15 minimum words are EXACTLY the 15
    W(3,2) lines {x,y,x+y} with B(x,y)=0.
  * The six weight-10 words have 5-point zero sets which are the six ovoids.
    The ten weight-6 words have 9-point zero sets which are the ten grids.
    The fifteen weight-8 words have 7-point zero sets which are the perps.
  * All 720 symplectic matrices preserve C. Conversely a coordinate
    automorphism of C permutes its six weight-10 words, and every coordinate
    is the unique intersection point of one pair of their 5-zero sets.
    Hence Aut(C) injects into S6 and therefore Aut(C)=Sp(4,2) ~= S6.
  * The 15 minimum dual words admit exactly six spreads. The action on the
    six weight-10 words and on these six spreads yields the exceptional
    outer automorphism of S6, with the complete cycle-class swap table.
  * q0 itself is a weight-6 word. Its 9 zeros are the singular/rank-1
    matrices and its 6 ones are the units, i.e. the recent determinant
    9+6 split is one distinguished 3+3-partition codeword.

Scope: finite binary geometry/coding only.  No physical Hilbert-space or
continuum claim is made.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS6533_6540_DOILY_QUADRATIC_EVALUATION_CODE.json"

ZERO = (0, 0, 0, 0)
V = [tuple((i >> j) & 1 for j in range(4)) for i in range(1, 16)]
VIDX = {v: i for i, v in enumerate(V)}
J = (
    (0, 1, 0, 0),
    (1, 0, 0, 0),
    (0, 0, 0, 1),
    (0, 0, 1, 0),
)

def add(u, v):
    return tuple(a ^ b for a, b in zip(u, v))

def B(u, v):
    return (u[0]*v[1] + u[1]*v[0] + u[2]*v[3] + u[3]*v[2]) & 1

def q0(v):
    return (v[0]*v[1] + v[2]*v[3]) & 1

def codeword(a, t):
    return tuple(B(a, x) ^ (t & q0(x)) for x in V)

def gf2_rank(rows):
    if not rows:
        return 0
    xs = [sum((b & 1) << i for i, b in enumerate(r)) for r in rows]
    rank = 0
    for col in range(len(rows[0]) - 1, -1, -1):
        p = next((i for i in range(rank, len(xs)) if (xs[i] >> col) & 1), None)
        if p is None:
            continue
        xs[rank], xs[p] = xs[p], xs[rank]
        for i in range(len(xs)):
            if i != rank and ((xs[i] >> col) & 1):
                xs[i] ^= xs[rank]
        rank += 1
    return rank

def dot(a, b):
    return sum(x*y for x, y in zip(a, b)) & 1

def support(w):
    return frozenset(i for i, b in enumerate(w) if b)

def zeros(w):
    return frozenset(i for i, b in enumerate(w) if not b)

def mat_from_mask(mask):
    return tuple(tuple((mask >> (4*r+c)) & 1 for c in range(4)) for r in range(4))

def matvec(M, v):
    return tuple(sum(M[r][c]*v[c] for c in range(4)) & 1 for r in range(4))

def is_symplectic(M):
    cols = [tuple(M[r][c] for r in range(4)) for c in range(4)]
    return all(B(cols[i], cols[j]) == J[i][j] for i in range(4) for j in range(4))

def coord_perm(M):
    return tuple(VIDX[matvec(M, v)] for v in V)

def permute_word(w, p):
    out = [0]*15
    for i, b in enumerate(w):
        out[p[i]] = b
    return tuple(out)

def cycle_type(p):
    seen = [False]*len(p)
    parts = []
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i
        n = 0
        while not seen[j]:
            seen[j] = True
            n += 1
            j = p[j]
        if n > 1:
            parts.append(n)
    return tuple(sorted(parts, reverse=True))

def ct_label(t):
    return "1" if not t else ".".join(map(str, t))

def main():
    all_a = [ZERO] + V
    C = {codeword(a, t) for a in all_a for t in (0, 1)}
    assert len(C) == 32
    assert gf2_rank(list(C)) == 5
    wdist = Counter(sum(w) for w in C)
    assert wdist == Counter({0:1, 6:10, 8:15, 10:6})

    S = {codeword(a, 0) for a in all_a}
    assert len(S) == 16
    assert gf2_rank(list(S)) == 4
    assert {w for w in C if sum(w) == 8} == (S - {tuple([0]*15)})

    qword = codeword(ZERO, 1)
    assert sum(qword) == 6
    assert zeros(qword) == frozenset(i for i, x in enumerate(V) if q0(x) == 0)
    assert support(qword) == frozenset(i for i, x in enumerate(V) if q0(x) == 1)

    basis = []
    for w in C:
        if gf2_rank(basis + [w]) > len(basis):
            basis.append(w)
    assert len(basis) == 5
    dual = []
    for mask in range(1 << 15):
        z = tuple((mask >> i) & 1 for i in range(15))
        if all(dot(b, z) == 0 for b in basis):
            dual.append(z)
    assert len(dual) == 1024
    dual_wdist = Counter(sum(z) for z in dual)
    assert min(k for k in dual_wdist if k) == 3
    assert dual_wdist == Counter({
        0:1, 3:15, 4:45, 5:96, 6:160, 7:195, 8:195,
        9:160, 10:96, 11:45, 12:15, 15:1,
    })

    lines = set()
    for i, x in enumerate(V):
        for y in V[i+1:]:
            if B(x, y) == 0:
                z = add(x, y)
                if z != ZERO:
                    lines.add(tuple(sorted((VIDX[x], VIDX[y], VIDX[z]))))
    assert len(lines) == 15
    dual3 = {tuple(sorted(support(z))) for z in dual if sum(z) == 3}
    assert dual3 == lines
    line_list = sorted(lines)
    line_index = {l:i for i,l in enumerate(line_list)}

    w6 = [w for w in C if sum(w) == 6]
    w8 = [w for w in C if sum(w) == 8]
    w10 = [w for w in C if sum(w) == 10]
    for w in w10:
        Z = zeros(w)
        assert len(Z) == 5
        assert all(len(Z & set(l)) == 1 for l in lines)
    for w in w8:
        Z = zeros(w)
        centers = [a for a in V if Z == frozenset(i for i,x in enumerate(V) if B(a,x) == 0)]
        assert len(centers) == 1
    for w in w6:
        Z = zeros(w)
        internal = [l for l in lines if set(l) <= Z]
        assert len(Z) == 9 and len(internal) == 6

    spreads = []
    for comb in itertools.combinations(range(15), 5):
        U = set()
        ok = True
        for j in comb:
            L = set(line_list[j])
            if U & L:
                ok = False
                break
            U |= L
        if ok and len(U) == 15:
            spreads.append(frozenset(comb))
    assert len(spreads) == 6
    spread_index = {s:i for i,s in enumerate(spreads)}

    ovoid_zero = [zeros(w) for w in w10]
    point_to_pair = {}
    for i, j in itertools.combinations(range(6), 2):
        I = ovoid_zero[i] & ovoid_zero[j]
        assert len(I) == 1
        p = next(iter(I))
        assert p not in point_to_pair
        point_to_pair[p] = (i,j)
    assert len(point_to_pair) == 15

    symps = [M for mask in range(1 << 16) if is_symplectic(M := mat_from_mask(mask))]
    assert len(symps) == 720
    Cset = set(C)
    oidx = {w:i for i,w in enumerate(w10)}
    class_pairs = Counter()
    coord_perms = set()
    for M in symps:
        p = coord_perm(M)
        coord_perms.add(p)
        assert {permute_word(w, p) for w in C} == Cset

        po = tuple(oidx[permute_word(w, p)] for w in w10)

        lp = []
        for l in line_list:
            nl = tuple(sorted(p[i] for i in l))
            lp.append(line_index[nl])
        ps = []
        for s in spreads:
            ns = frozenset(lp[j] for j in s)
            ps.append(spread_index[ns])
        class_pairs[(cycle_type(po), cycle_type(tuple(ps)))] += 1

    assert len(coord_perms) == 720
    aut_order = 720

    expected_pairs = Counter({
        ((), ()): 1,
        ((2,), (2,2,2)): 15,
        ((2,2,2), (2,)): 15,
        ((3,), (3,3)): 40,
        ((3,3), (3,)): 40,
        ((2,2), (2,2)): 45,
        ((4,), (4,)): 90,
        ((4,2), (4,2)): 90,
        ((3,2), (6,)): 120,
        ((6,), (3,2)): 120,
        ((5,), (5,)): 144,
    })
    assert class_pairs == expected_pairs

    result = {
        "passes": "6533-6540",
        "object": "doily quadratic-evaluation code",
        "code": {
            "parameters": [15, 5, 6],
            "size": len(C),
            "weight_enumerator": {str(k): wdist[k] for k in sorted(wdist)},
            "simplex_subcode": {
                "parameters": [15, 4, 8],
                "size": len(S),
                "all_nonzero_are_weight8": True,
            },
            "quadratic_coset_weights": {"6": 10, "10": 6},
        },
        "dual": {
            "parameters": [15, 10, 3],
            "weight_enumerator": {str(k): dual_wdist[k] for k in sorted(dual_wdist)},
            "minimum_words": 15,
            "minimum_supports_equal_doily_lines": True,
            "spreads_of_minimum_words": len(spreads),
        },
        "hyperplane_weight_dictionary": {
            "weight6": "10 grid complements / quadratic plus type",
            "weight8": "15 perp complements / nonzero symplectic linear forms",
            "weight10": "6 ovoid complements / quadratic minus type",
        },
        "determinant_word": {
            "weight": sum(qword),
            "zeros_singular_rank1_nonzero": len(zeros(qword)),
            "ones_units": len(support(qword)),
            "interpretation": "one distinguished 3+3-partition word",
        },
        "automorphism": {
            "symplectic_coordinate_actions": len(coord_perms),
            "upper_bound_from_six_weight10_words": 720,
            "order": aut_order,
            "isomorphism": "Sp(4,2) ~= S6",
            "coordinate_reconstruction": "15 coordinates are the 15 pairwise intersections of six ovoid zero-sets",
        },
        "outer_automorphism": {
            "six_set_A": "six weight-10 words / ovoid zero-sets",
            "six_set_B": "six spreads of the 15 minimum dual words",
            "cycle_type_pairs": [
                {"on_ovoids": ct_label(a), "on_spreads": ct_label(b), "count": n}
                for (a,b),n in sorted(class_pairs.items(), key=lambda kv:(kv[0][0],kv[0][1]))
            ],
            "swaps": [
                "2 <-> 2.2.2",
                "3 <-> 3.3",
                "3.2 <-> 6",
            ],
        },
        "scope": "finite binary geometry/coding only",
        "checks": "PASS",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
