#!/usr/bin/env python3
"""Exact Clifford decomposition of the 24-dimensional circuit spectral sector.

The bicolour C5--C6 spectral algebra has a unique 24-dimensional joint sector,
namely the A20-eigenspace with eigenvalue 8.  This audit restricts that rational
PSp(4,3)-module to the order-648 W33 point stabilizer K and proves:

  24|_K = 12_0 + 6_omega + 6_omega^2,

where Z(K)=C3 acts trivially on the 12-space and by the two nontrivial central
characters on the conjugate six-spaces.  The two six-spaces are irreducible.

The 12-dimensional quotient module descends to Q=K/Z ~= ASL(2,3).  Its exact
character on every one of the 216 quotient elements equals the permutation
character for conjugation on the 12 fixed-line cyclic C3 subgroups.  In the
affine model these are the 12 affine lines.  That rank-3 action has subdegrees
1+2+9, with the size-2 relation equal to four disjoint triangles, so

  12 = 1 + 3 + 8

multiplicity-free.  Thus the complete restriction is

  24|_K = 1 + 3 + 8 + 6_omega + 6_omega^2.

All traces are computed from an exact rational spectral projector; no numerical
eigenvectors or floating-point character matching are used.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260830_CIRCUIT24_CLIFFORD_LINE_MODULE.json"


def invperm(p):
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def orbit_partition(G, n):
    rem = set(range(n)); out = []
    while rem:
        s = min(rem); O = {g[s] for g in G}
        out.append(sorted(O)); rem -= O
    return sorted(out, key=lambda O: (-len(O), O))


def main():
    pts, idx, _lines, N = base.geometry()
    supports, masks = base.supports_from_N(N)

    c5 = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            c5.append(C)
    c6 = six_circuits(masks)
    assert len(c5) == 216 and len(c6) == 540
    i5 = {C: i for i, C in enumerate(c5)}
    i6 = {C: i for i, C in enumerate(c6)}

    # Native PSp generators on 40 W33 points and 45 sentinel minima.
    gens40 = []
    for v in pts:
        for alpha in (1, 2):
            p = []
            for x in pts:
                z = alpha * base.form(x, v) % 3
                y = base.norm(tuple((x[k] + z * v[k]) % 3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si = {S: i for i, S in enumerate(supports)}
    gens45 = [tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    chosen = (18, 62, 77, 10)
    g40 = [gens40[i] for i in chosen]
    g45 = [gens45[i] for i in chosen]
    Gpaired = base.closure_paired(g40, g45)
    assert len(Gpaired) == 25920

    # Rebuild the two maximal-overlap colours and their 20-regular cross graph.
    act5 = [tuple(i5[tuple(sorted(g[x] for x in C))] for C in c5) for g in g45]
    act6 = [tuple(i6[tuple(sorted(g[x] for x in C))] for C in c6) for g in g45]
    M = np.zeros((216, 540), dtype=np.int64)
    s5 = [set(C) for C in c5]; s6 = [set(C) for C in c6]
    for a in range(216):
        for b in range(540):
            if len(s5[a] & s6[b]) == 3:
                M[a, b] = 1
    seed = next(a * 540 + b for a in range(216) for b in range(540) if M[a, b])
    O = {seed}; Qwork = deque([seed])
    while Qwork:
        z0 = Qwork.popleft(); a, b = divmod(z0, 540)
        for p5, p6 in zip(act5, act6):
            nz = p5[a] * 540 + p6[b]
            if nz not in O:
                O.add(nz); Qwork.append(nz)
    assert len(O) == 2160
    Mp = np.zeros_like(M)
    for z0 in O:
        a, b = divmod(z0, 540); Mp[a, b] = 1
    Mm = M - Mp
    A20 = (Mp @ Mm.T + Mm @ Mp.T) // 4
    assert set(map(int, A20.sum(axis=1))) == {20}

    # Exact rational projector onto the unique A20-eigenvalue-8 sector.
    # P24 = Q24/D with D=-155520 and Q24 integral.
    I = np.eye(216, dtype=np.int64)
    other = [-10, -4, -2, 2, 20]
    D = 1
    Q24 = I.copy()
    for r in other:
        D *= 8 - r
        Q24 = Q24 @ (A20 - r * I)
    assert D == -155520
    assert int(np.trace(Q24)) == 24 * D

    cidx = i5
    def circuit_perm(g45):
        return tuple(cidx[tuple(sorted(g45[x] for x in C))] for C in c5)

    # Point stabilizer K, its central deck C3, and quotient action on 72 fibres.
    K = {p45 for p40, p45 in Gpaired if p40[0] == 0}
    assert len(K) == 648
    kgens = base.deterministic_generators(K, 45)
    Z = [z for z in K if all(base.compose(z, g) == base.compose(g, z) for g in kgens)]
    assert len(Z) == 3
    e45 = tuple(range(45))
    z = next(x for x in Z if x != e45)
    z2 = base.compose(z, z)
    Kperm = {g: circuit_perm(g) for g in K}

    def char24(g):
        p = Kperm[g]
        num = sum(int(Q24[i, p[i]]) for i in range(216))
        assert num % D == 0
        return num // D

    assert sorted(char24(g) for g in Z) == [6, 6, 24]
    # From 24=a+2b and 6=a-b, the central eigen-dimensions are 12,6,6.
    central_dims = {"1": 12, "omega": 6, "omega2": 6}

    zperm = Kperm[z]
    zfibres = []; seen = set()
    for i in range(216):
        if i in seen:
            continue
        cyc = []; j = i
        while j not in seen:
            seen.add(j); cyc.append(j); j = zperm[j]
        zfibres.append(tuple(sorted(cyc)))
    assert len(zfibres) == 72 and {len(x) for x in zfibres} == {3}
    fibre_of = {x: i for i, F in enumerate(zfibres) for x in F}

    def qperm(g):
        p = Kperm[g]
        return tuple(fibre_of[p[F[0]]] for F in zfibres)

    Q = {qperm(g) for g in K}
    assert len(Q) == 216
    lifts = defaultdict(list)
    for g in K:
        lifts[qperm(g)].append(g)
    assert {len(v) for v in lifts.values()} == {3}

    qorbits = orbit_partition(Q, 72)
    assert [len(O) for O in qorbits] == [36, 36]
    e72 = tuple(range(72))

    def qsub(q):
        return frozenset((e72, q, base.compose(q, q)))

    order3subs = {qsub(q) for q in Q if base.porder(q) == 3}
    assert len(order3subs) == 40
    species = defaultdict(list)
    for H in order3subs:
        q = next(x for x in H if x != e72)
        fixed = tuple(sum(q[i] == i for i in O) for O in qorbits)
        species[fixed].append(H)
    assert sorted(map(len, species.values())) == [4, 12, 24]
    fixedline_key = next(k for k, v in species.items() if len(v) == 12)
    translation_key = next(k for k, v in species.items() if len(v) == 4)
    nonsplit_key = next(k for k, v in species.items() if len(v) == 24)
    H12 = species[fixedline_key]

    # The central-trivial character is the average over the three lifts.
    def char12(q):
        s = sum(char24(g) for g in lifts[q])
        assert s % 3 == 0
        return s // 3

    # Conjugation permutation action on the 12 fixed-line C3 subgroups.
    Hidx = {H: i for i, H in enumerate(H12)}
    invQ = {q: invperm(q) for q in Q}
    def conj_sub(q, H):
        qi = invQ[q]
        return frozenset(base.compose(base.compose(q, h), qi) for h in H)
    def act12(q, i):
        return Hidx[conj_sub(q, H12[i])]

    char_match = Counter()
    for q in Q:
        fixed12 = sum(act12(q, i) == i for i in range(12))
        c = char12(q)
        assert fixed12 == c
        char_match[(base.porder(q), c)] += 1
    assert char_match == Counter({(1,12):1,(2,4):9,(3,3):32,(3,0):48,(4,0):54,(6,1):72})

    # Split the order-3 character rows into the 4+12+24 affine species.
    species_rows = []
    for key, subgroups in sorted(species.items(), key=lambda kv: len(kv[1])):
        elems = [q for H in subgroups for q in H if q != e72]
        c12 = {char12(q) for q in elems}
        lift_orders = {tuple(sorted(base.porder(g) for g in lifts[q])) for q in elems}
        lift_char24 = {tuple(sorted(char24(g) for g in lifts[q])) for q in elems}
        assert len(c12) == len(lift_orders) == len(lift_char24) == 1
        species_rows.append({
            "subgroups": len(subgroups),
            "elements": len(elems),
            "fixedFibresOn36Plus36": list(key),
            "char12": next(iter(c12)),
            "liftOrders": list(next(iter(lift_orders))),
            "sortedChar24AcrossThreeLifts": list(next(iter(lift_char24))),
        })
    assert [r["subgroups"] for r in species_rows] == [4,12,24]
    assert species_rows[0]["char12"] == 3
    assert species_rows[1]["char12"] == 3
    assert species_rows[2]["char12"] == 0
    assert species_rows[2]["liftOrders"] == [9,9,9]
    assert species_rows[2]["sortedChar24AcrossThreeLifts"] == [0,0,0]

    # Rank-3 action and the four parallel triples.
    stab0 = [q for q in Q if act12(q, 0) == 0]
    rem = set(range(12)); suborbits = []
    while rem:
        s = min(rem); OO = {act12(q, s) for q in stab0}
        suborbits.append(sorted(OO)); rem -= OO
    assert sorted(map(len, suborbits)) == [1,2,9]
    parallel_seed = next(O for O in suborbits if len(O) == 2)
    parallel_edges = set()
    for q in Q:
        a = act12(q, 0)
        for j in parallel_seed:
            b = act12(q, j)
            if a != b:
                parallel_edges.add(tuple(sorted((a,b))))
    deg = Counter(x for e in parallel_edges for x in e)
    assert len(parallel_edges) == 12 and set(deg.values()) == {2}
    # Degree 2 plus 12 edges could include longer cycles; certify four triangles.
    adj = {i:set() for i in range(12)}
    for a,b in parallel_edges:
        adj[a].add(b); adj[b].add(a)
    comps=[]; unseen=set(range(12))
    while unseen:
        s=min(unseen); C={s}; QQ=deque([s])
        while QQ:
            a=QQ.popleft()
            for b in adj[a]:
                if b not in C:
                    C.add(b); QQ.append(b)
        comps.append(sorted(C)); unseen-=C
    assert sorted(map(len, comps)) == [3,3,3,3]

    # Exact character norms of the three central isotypic pieces.  If
    # c0=chi(g), c1=chi(zg), c2=chi(z^2 g), then
    # |c0+omega^2 c1+omega c2|^2 = c0^2+c1^2+c2^2-c0c1-c0c2-c1c2.
    sum0 = 0; sumw = 0
    for g in K:
        c0 = char24(g)
        c1 = char24(base.compose(z, g))
        c2 = char24(base.compose(z2, g))
        s = c0 + c1 + c2
        assert s % 3 == 0
        sum0 += (s // 3) ** 2
        norm_num = c0*c0 + c1*c1 + c2*c2 - c0*c1 - c0*c2 - c1*c2
        assert norm_num % 9 == 0
        sumw += norm_num // 9
    assert sum0 == 3 * len(K)   # rank-3 12-point permutation character
    assert sumw == len(K)       # each nontrivial central-character six is irreducible

    out = {
        "schema":"w33.20260830.circuit24-clifford-line-module.v1",
        "status":"PASS",
        "spectralSector":{"ambientDimension":216,"A20Eigenvalue":8,"dimension":24,
          "projectorDenominator":D,"proof":"exact rational polynomial projector"},
        "centralC3":{"nontrivialTraceOn24":6,"eigenspaceDimensions":central_dims,
          "restriction":"24 = 12_1 + 6_omega + 6_omega2"},
        "quotientLineModule":{"quotient":"K/C3 = ASL(2,3)","dimension":12,
          "model":"conjugation permutation module on the 12 fixed-line cyclic C3 subgroups",
          "characterEqualityCheckedOnAll216Elements":True,
          "characterByOrder":[{"order":o,"character":c,"elements":n} for (o,c),n in sorted(char_match.items())],
          "rank":3,"subdegrees":[1,2,9],"parallelRelation":"4 K3",
          "irreducibleDimensions":[1,3,8],"decomposition":"1 + 3 + 8"},
        "order3Species":species_rows,
        "sixDimensionalPieces":{"dimensions":[6,6],"centralCharacters":["omega","omega2"],
          "characterNorms":[1,1],"irreducible":True,"complexConjugate":True},
        "theorem":"The 24-dimensional bicolour circuit sector restricts to the W33 point stabilizer as 1+3+8+6_omega+6_omega2. Its central-trivial 12-space is exactly the ASL(2,3) affine-line permutation module; every nonsplit C9 order-three direction has character zero on it and all three order-nine lifts have trace zero on the full 24-sector.",
        "boundary":"This identifies an exact Clifford quotient module inside the circuit spectral sector. It does not identify the 24-dimensional sector with the 24 nonsplit cyclic subgroups; the actual bridge is the 12-line quotient module plus two irreducible central-character sixes."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","Krestriction":[1,3,8,6,6],"lineActionSubdegrees":[1,2,9],"nonsplitChar12":0,"sixIrreducible":True},sort_keys=True))


if __name__ == "__main__":
    main()
