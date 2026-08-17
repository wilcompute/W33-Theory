#!/usr/bin/env python3
"""Passes 7001--7016: bent extension, 16-point biplane, and Klein-polar bridge.

This packet is deliberately self-contained.  It starts from V=F_2^4 with the
standard symplectic form

    B(x,y)=x0*y1+x1*y0+x2*y3+x3*y2

and q0(x)=x0*x1+x2*x3.  It reconstructs the 15-coordinate quadratic-evaluation
code C from Pass6533, extends it over the missing zero vector, and derives the
16-point design and Klein-quadric consequences without importing any previous
certificate.

Main exact checks:
  * C is self-orthogonal [15,5,6], W_C=1+10 y^6+15 y^8+6 y^10.
  * C^perp is [15,10,3] with the previously recorded weight enumerator.
  * generalized Hamming weights(C)=(6,10,12,14,15), covering radius(C)=6.
  * D=<RM(1,4),q0> is self-orthogonal [16,6,6],
      W_D=1+16 y^6+30 y^8+16 y^10+y^16.
  * D^perp is [16,10,4],
      W=1+60y^4+256y^6+390y^8+256y^10+60y^12+y^16.
  * generalized Hamming weights(D)=(6,10,12,14,15,16), covering radius(D)=6.
  * the 16 weight-6 supports of D form a symmetric 2-(16,6,2) biplane.
  * fixing coordinate 0 splits those blocks 10+6:
      - 10 avoiding 0 = the ten weight-6 supports of C (grid complements),
      - 6 through 0, with 0 deleted = zero sets of the six weight-10 C words
        (the six doily ovoids).
    The 30 weight-8 D words pair by complement and shorten to the 15 weight-8 C
    words (the fifteen perps).
  * Aut(C)=Sp(4,2)=S6 has order 720; the biplane has full automorphism group
    2^4:Sp(4,2), order 11520.
  * the 35 PG(3,2) lines map bijectively to the 35 F_2-rational points of the
    Klein quadric Q^+(5,2); the symplectic isotropy equation is the hyperplane
    p01+p23=0, giving the exact 15+20 split.
  * the 20 exterior Klein points are paired by symplectic polarity into ten
    skew line pairs.  Their six-point unions are exactly the ten grid-complement
    supports and have constant mutual intersection 2.  The 10x15 incidence
    matrix M therefore satisfies M M^T = 4 I + 2 J and has spectrum 24^1,4^9.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS7001_7016_BENT_BIPLANE_KLEIN.json"

V0 = [tuple((i >> j) & 1 for j in range(4)) for i in range(16)]
ZERO = (0, 0, 0, 0)
V = [x for x in V0 if x != ZERO]


def add(a, b):
    return tuple(int(x) ^ int(y) for x, y in zip(a, b))


def B(a, b):
    return (a[0]*b[1] + a[1]*b[0] + a[2]*b[3] + a[3]*b[2]) % 2


def q0(x):
    return (x[0]*x[1] + x[2]*x[3]) % 2


def dot(u, v):
    return sum(int(a)*int(b) for a, b in zip(u, v)) % 2


def rank_binary_words(words: list[tuple[int, ...]]) -> int:
    if not words:
        return 0
    rows = [sum(int(b) << i for i, b in enumerate(w)) for w in words]
    piv: dict[int, int] = {}
    for x in rows:
        y = int(x)
        while y:
            p = y.bit_length() - 1
            if p in piv:
                y ^= piv[p]
            else:
                piv[p] = y
                break
    return len(piv)


def code_C():
    out = set()
    for a in V0:
        for t in (0, 1):
            out.add(tuple(B(a, x) ^ (t*q0(x)) for x in V))
    return out


def code_D():
    # all affine linear functions plus optional q0, evaluated on all 16 points
    out = set()
    for a in V0:
        for c in (0, 1):
            for t in (0, 1):
                out.add(tuple(B(a, x) ^ c ^ (t*q0(x)) for x in V0))
    return out


def basis_of_code(code):
    n = len(next(iter(code)))
    basis: list[int] = []
    piv: list[int] = []
    for w in code:
        x = sum(int(b) << i for i, b in enumerate(w))
        if not x:
            continue
        y = x
        for b, p in zip(basis, piv):
            if (y >> p) & 1:
                y ^= b
        if y:
            p = (y & -y).bit_length() - 1
            basis.append(y)
            piv.append(p)
    return basis, n


def dual(code):
    basis, n = basis_of_code(code)
    out = []
    for mask in range(1 << n):
        w = tuple((mask >> i) & 1 for i in range(n))
        if all(dot(w, tuple((b >> i) & 1 for i in range(n))) == 0 for b in basis):
            out.append(w)
    return set(out)


def covering_profile(code):
    n = len(next(iter(code)))
    ints = [sum(int(b) << i for i, b in enumerate(w)) for w in code]
    profile = Counter()
    for x in range(1 << n):
        d = min((x ^ c).bit_count() for c in ints)
        profile[d] += 1
    return max(profile), dict(sorted(profile.items()))


def all_subspaces_abstract(k: int):
    subs = {0: {frozenset({0})}}
    ambient = set(range(1 << k))
    for r in range(k):
        nxt = set()
        for S in subs[r]:
            base = set(S)
            for v in ambient - base:
                T = frozenset(base | {x ^ v for x in base})
                if len(T) == 1 << (r+1):
                    nxt.add(T)
        subs[r+1] = nxt
    return subs


def generalized_hamming_weights(code):
    basis, n = basis_of_code(code)
    k = len(basis)
    vec = {}
    for a in range(1 << k):
        w = 0
        for i, b in enumerate(basis):
            if (a >> i) & 1:
                w ^= b
        vec[a] = w
    subs = all_subspaces_abstract(k)
    out = []
    counts = {}
    for r in range(1, k+1):
        counts[r] = len(subs[r])
        best = n + 1
        for S in subs[r]:
            support = 0
            for a in S:
                support |= vec[a]
            best = min(best, support.bit_count())
        out.append(best)
    return out, counts


def weight_enum(code):
    return dict(sorted(Counter(sum(w) for w in code).items()))


def all_pg32_lines():
    lines = set()
    for x, y in combinations(V, 2):
        z = add(x, y)
        lines.add(frozenset((x, y, z)))
    assert len(lines) == 35
    return lines

PLUCKER_PAIRS = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))


def plucker(line):
    x, y, _ = tuple(line)
    return tuple((x[i]*y[j] + x[j]*y[i]) % 2 for i, j in PLUCKER_PAIRS)


def orth_line(line):
    return frozenset(x for x in V if all(B(x, y) == 0 for y in line))


def sp4_matrices():
    J = np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]], dtype=np.uint8)
    out = []
    for mask in range(1 << 16):
        M = np.array([[(mask >> (4*i+j)) & 1 for j in range(4)] for i in range(4)], dtype=np.uint8)
        if np.array_equal((M.T @ J @ M) % 2, J):
            out.append(M)
    assert len(out) == 720
    return out


def apply_matrix(M, x):
    y = (M @ np.array(x, dtype=np.uint8)) % 2
    return tuple(int(a) for a in y)


def main():
    C = code_C(); D = code_D()
    Cd = dual(C); Dd = dual(D)
    assert (len(C), len(D), len(Cd), len(Dd)) == (32, 64, 1024, 1024)
    assert weight_enum(C) == {0:1, 6:10, 8:15, 10:6}
    assert weight_enum(D) == {0:1, 6:16, 8:30, 10:16, 16:1}
    assert weight_enum(Cd) == {0:1,3:15,4:45,5:96,6:160,7:195,8:195,9:160,10:96,11:45,12:15,15:1}
    assert weight_enum(Dd) == {0:1,4:60,6:256,8:390,10:256,12:60,16:1}
    assert C <= Cd and D <= Dd

    gC, subC = generalized_hamming_weights(C)
    gD, subD = generalized_hamming_weights(D)
    assert gC == [6,10,12,14,15]
    assert gD == [6,10,12,14,15,16]
    covC, profC = covering_profile(C)
    covD, profD = covering_profile(D)
    assert covC == covD == 6

    # 16 weight-6 supports form a symmetric 2-(16,6,2) design.
    D6 = [w for w in D if sum(w) == 6]
    blocks = [frozenset(i for i, b in enumerate(w) if b) for w in D6]
    assert len(set(blocks)) == 16 and all(len(Bk) == 6 for Bk in blocks)
    assert Counter(len(A & Bk) for A, Bk in combinations(blocks, 2)) == Counter({2:120})
    point_degrees = Counter(i for Bk in blocks for i in Bk)
    assert set(point_degrees.values()) == {6} and len(point_degrees) == 16
    pair_degrees = Counter(tuple(sorted((i,j))) for Bk in blocks for i,j in combinations(Bk,2))
    assert set(pair_degrees.values()) == {2} and len(pair_degrees) == 120

    C6 = {w for w in C if sum(w) == 6}
    C10 = [w for w in C if sum(w) == 10]
    avoiding = {tuple(w[1:]) for w in D6 if w[0] == 0}
    through_deleted = {
        frozenset(i-1 for i,b in enumerate(w) if i and b)
        for w in D6 if w[0] == 1
    }
    ovoid_zero_sets = {
        frozenset(i for i,b in enumerate(w) if b == 0)
        for w in C10
    }
    assert len(avoiding) == 10 and avoiding == C6
    assert len(through_deleted) == 6 and through_deleted == ovoid_zero_sets
    D8 = [w for w in D if sum(w) == 8]
    shortened_D8 = {tuple(w[1:]) for w in D8 if w[0] == 0}
    assert len(D8) == 30 and shortened_D8 == {w for w in C if sum(w) == 8}
    assert rank_binary_words(list(C6)) == 5

    # Recover Aut(C)=720 and exact biplane automorphism group order 11520.
    sp = sp4_matrices()
    pidx15 = {x:i for i,x in enumerate(V)}
    sp_perms15 = set()
    for M in sp:
        sp_perms15.add(tuple(pidx15[apply_matrix(M,x)] for x in V))
    assert len(sp_perms15) == 720
    # Six ovoid zero sets pairwise meet in one point and recover all 15 coordinates,
    # giving Aut(C) <= S6; the Sp(4,2) subgroup attains this bound.
    oz = list(ovoid_zero_sets)
    intersections = [A & Bk for A,Bk in combinations(oz,2)]
    assert len(intersections) == 15 and all(len(x) == 1 for x in intersections)
    assert len({next(iter(x)) for x in intersections}) == 15

    pidx16 = {x:i for i,x in enumerate(V0)}
    blockset = set(blocks)
    affine_perms = set()
    for M in sp:
        for a in V0:
            p = tuple(pidx16[add(apply_matrix(M,x), a)] for x in V0)
            assert all(frozenset(p[i] for i in Bk) in blockset for Bk in blockset)
            affine_perms.add(p)
    assert len(affine_perms) == 16*720
    # A point stabilizer of any biplane automorphism acts faithfully on the 15
    # remaining points and preserves the ten nonincident blocks, whose binary
    # span is C.  Hence |Stab(point)| <= |Aut(C)|=720 and |Aut(biplane)|<=16*720.
    # The affine symplectic subgroup attains the bound.

    # Klein quadric and symplectic hyperplane section.
    lines = all_pg32_lines()
    P = {L:plucker(L) for L in lines}
    assert len(set(P.values())) == 35
    assert all((p[0]*p[5] + p[1]*p[4] + p[2]*p[3]) % 2 == 0 for p in P.values())
    isotropic = [L for L in lines if all(B(x,y)==0 for x,y in combinations(L,2))]
    noniso = [L for L in lines if L not in isotropic]
    assert (len(isotropic), len(noniso)) == (15,20)
    # For p=(p01,p02,p03,p12,p13,p23), B(x,y)=p01+p23.
    assert all((P[L][0] ^ P[L][5]) == (0 if L in isotropic else 1) for L in lines)

    seen = set(); polar_pairs = []
    for L in noniso:
        if L in seen:
            continue
        Lp = orth_line(L)
        assert Lp in noniso and orth_line(Lp) == L and L.isdisjoint(Lp)
        polar_pairs.append((L,Lp)); seen.add(L); seen.add(Lp)
    assert len(polar_pairs) == 10
    unions = [frozenset(set(L)|set(Lp)) for L,Lp in polar_pairs]
    assert Counter(len(A&Bk) for A,Bk in combinations(unions,2)) == Counter({2:45})
    c6_supports = {frozenset(i for i,b in enumerate(w) if b) for w in C6}
    unions_idx = {frozenset(pidx15[x] for x in U) for U in unions}
    assert unions_idx == c6_supports
    Minc = np.zeros((10,15), dtype=int)
    for r,U in enumerate(unions_idx):
        for c in U:
            Minc[r,c] = 1
    assert np.array_equal(Minc @ Minc.T, 4*np.eye(10,dtype=int)+2*np.ones((10,10),dtype=int))
    assert np.all(Minc.sum(axis=0) == 4)
    gram_eigs = sorted(round(float(x),10) for x in np.linalg.eigvalsh(Minc @ Minc.T))
    assert gram_eigs == [4.0]*9 + [24.0]

    report = {
        "passes": list(range(7001,7017)),
        "C15": {
            "parameters": [15,5,6], "self_orthogonal": True,
            "weight_enumerator": weight_enum(C),
            "dual_parameters": [15,10,3], "dual_weight_enumerator": weight_enum(Cd),
            "generalized_hamming_weights": gC,
            "covering_radius": covC, "covering_profile": profC,
            "aut_group_order": 720,
        },
        "D16_bent_extension": {
            "construction": "<RM(1,4), q0>, q0=x0*x1+x2*x3",
            "parameters": [16,6,6], "self_orthogonal": True,
            "weight_enumerator": weight_enum(D),
            "dual_parameters": [16,10,4], "dual_weight_enumerator": weight_enum(Dd),
            "generalized_hamming_weights": gD,
            "covering_radius": covD, "covering_profile": profD,
            "weight6_design": "symmetric 2-(16,6,2) biplane",
            "aut_group": "2^4:Sp(4,2) ~= 2^4:S6",
            "aut_group_order": 11520,
        },
        "point_derivation": {
            "blocks_avoiding_distinguished_point": 10,
            "blocks_through_distinguished_point": 6,
            "avoiding_equal_grid_complement_supports": True,
            "through_deleted_equal_ovoid_zero_sets": True,
            "weight8_complement_pairs": 15,
            "weight8_shortening_equal_perp_words": True,
        },
        "klein_polar": {
            "pg32_lines": 35,
            "klein_equation": "p01*p23+p02*p13+p03*p12=0",
            "symplectic_hyperplane": "p01+p23=0",
            "isotropic": 15, "nonisotropic": 20,
            "nonisotropic_polar_pairs": 10,
            "polar_pair_unions_equal_grid_complement_supports": True,
            "union_pair_intersection": 2,
            "incidence_gram": "M M^T = 4 I_10 + 2 J_10",
            "gram_spectrum": {"24":1,"4":9},
            "column_degree": 4,
        },
        "boundary": "Finite binary coding/design/projective geometry only; no physical identification is inferred.",
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"wrote {OUT}")
    return report


if __name__ == "__main__":
    main()
