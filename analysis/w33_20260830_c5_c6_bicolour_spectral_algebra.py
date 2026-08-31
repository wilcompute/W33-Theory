#!/usr/bin/env python3
"""Exact spectral algebra of the two maximal-overlap C5--C6 orbitals.

The 216x540 maximal-overlap incidence relation |C5 intersect C6|=3 splits into
two PSp(4,3)-orbitals of size 2160.  Write their 0/1 biadjacency matrices as
M+ and M-.  This audit proves exact Gram/cross-Gram identities and the complete
joint spectrum of the resulting two commuting relation graphs on the 216
five-circuits.

No floating-point diagonalization is used for the theorem.  Candidate integer
spectra are certified by exact matrix annihilating polynomials and trace
multiplicities.  A+7B has seven separated eigenvalues, excluding all other
cartesian pairings and forcing seven joint spectral sectors.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260830_C5_C6_BICOLOUR_SPECTRAL_ALGEBRA.json"


def annihilates(A: np.ndarray, roots: list[int]) -> bool:
    """Check prod_r (A-rI)=0 exactly in int64 arithmetic."""
    n = A.shape[0]
    I = np.eye(n, dtype=np.int64)
    P = I.copy()
    for r in roots:
        P = P @ (A - r * I)
    return not np.any(P)


def multiplicities_from_traces(A: np.ndarray, roots: list[int]) -> dict[int, int]:
    """Recover exact spectral multiplicities from traces 0..m-1."""
    n = A.shape[0]
    traces = [n]
    P = np.eye(n, dtype=np.int64)
    for _ in range(1, len(roots)):
        P = P @ A
        traces.append(int(np.trace(P)))
    V = sp.Matrix([[sp.Integer(r) ** k for r in roots] for k in range(len(roots))])
    sol = V.LUsolve(sp.Matrix(traces))
    out = {r: int(sol[i]) for i, r in enumerate(roots)}
    assert all(sp.Integer(sol[i]).q == 1 for i in range(len(roots)))
    assert sum(out.values()) == n and all(v >= 0 for v in out.values())
    return out


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
    gg = [gens45[i] for i in chosen]
    act5 = [tuple(i5[tuple(sorted(g[x] for x in C))] for C in c5) for g in gg]
    act6 = [tuple(i6[tuple(sorted(g[x] for x in C))] for C in c6) for g in gg]

    # Full maximal-overlap incidence matrix.
    M = np.zeros((216, 540), dtype=np.int64)
    s5 = [set(C) for C in c5]
    s6 = [set(C) for C in c6]
    for a in range(216):
        for b in range(540):
            if len(s5[a] & s6[b]) == 3:
                M[a, b] = 1
    assert set(map(int, M.sum(axis=1))) == {20}
    assert set(map(int, M.sum(axis=0))) == {8}

    # Generate one of the two PSp orbitals; the complement inside M is the other.
    seed = next(a * 540 + b for a in range(216) for b in range(540) if M[a, b])
    O = {seed}; Q = deque([seed])
    while Q:
        z = Q.popleft(); a, b = divmod(z, 540)
        for p5, p6 in zip(act5, act6):
            nz = p5[a] * 540 + p6[b]
            if nz not in O:
                O.add(nz); Q.append(nz)
    assert len(O) == 2160
    Mp = np.zeros_like(M)
    for z in O:
        a, b = divmod(z, 540); Mp[a, b] = 1
    Mm = M - Mp
    assert np.all((Mm == 0) | (Mm == 1))
    for X in (Mp, Mm):
        assert set(map(int, X.sum(axis=1))) == {10}
        assert set(map(int, X.sum(axis=0))) == {4}

    I = np.eye(216, dtype=np.int64)
    Gp = Mp @ Mp.T
    Gm = Mm @ Mm.T
    assert np.array_equal(Gp, Gm)
    A30 = Gp - 10 * I
    assert np.all(np.diag(A30) == 0)
    assert set(np.unique(A30)).issubset({0, 1})
    assert set(map(int, A30.sum(axis=1))) == {30}
    assert int(A30.sum()) // 2 == 3240

    cross = Mp @ Mm.T + Mm @ Mp.T
    assert np.all(np.diag(cross) == 0)
    assert set(np.unique(cross)).issubset({0, 4})
    A20 = cross // 4
    assert set(map(int, A20.sum(axis=1))) == {20}
    assert int(A20.sum()) // 2 == 2160
    assert not np.any(A30 * A20)
    assert np.array_equal(A30 @ A20, A20 @ A30)

    # The union Gram operator is an exact linear combination of the two relations.
    Gram = M @ M.T
    assert np.array_equal(Gram, 20 * I + 2 * A30 + 4 * A20)

    roots30 = [-6, -4, 0, 6, 12, 30]
    roots20 = [-10, -4, -2, 2, 8, 20]
    assert annihilates(A30, roots30)
    assert annihilates(A20, roots20)
    mult30 = multiplicities_from_traces(A30, roots30)
    mult20 = multiplicities_from_traces(A20, roots20)
    assert mult30 == {-6:20, -4:81, 0:60, 6:39, 12:15, 30:1}
    assert mult20 == {-10:15, -4:15, -2:81, 2:80, 8:24, 20:1}

    # A30+7 A20 separates the seven actual joint eigencharacters.  Because
    # A30 and A20 commute and their individual spectra are certified above,
    # annihilation by these seven roots excludes every other cartesian pairing.
    joint = [
        (-4, -2, 81),
        (0, 2, 60),
        (6, 8, 24),
        (-6, 2, 20),
        (12, -10, 15),
        (6, -4, 15),
        (30, 20, 1),
    ]
    sep_roots = sorted({a + 7*b for a, b, _m in joint})
    assert sep_roots == [-58, -22, -18, 8, 14, 62, 170]
    all_pairs = [(a,b) for a in roots30 for b in roots20]
    allowed = {(a,b) for a,b,_ in joint}
    assert not [(a,b) for a,b in all_pairs if (a + 7*b) in sep_roots and (a,b) not in allowed]
    C = A30 + 7 * A20
    assert annihilates(C, sep_roots)

    # Individual multiplicities force the split of the only repeated A30
    # eigenvalue: lambda=6 decomposes as 24+15 under A20=8,-4.
    assert sum(m for _a,_b,m in joint) == 216
    assert Counter({a: sum(m for aa,_b,m in joint if aa==a) for a in roots30}) == Counter(mult30)
    assert Counter({b: sum(m for _a,bb,m in joint if bb==b) for b in roots20}) == Counter(mult20)

    gram_mult = Counter()
    for a,b,m in joint:
        gram_mult[20 + 2*a + 4*b] += m
    assert dict(sorted(gram_mult.items())) == {4:96, 16:35, 28:60, 64:24, 160:1}
    assert all(x > 0 for x in gram_mult)

    out = {
        "schema": "w33.20260830.c5-c6-bicolour-spectral-algebra.v1",
        "status": "PASS",
        "incidence": {
            "shape": [216,540],
            "unionDegrees": [20,8],
            "colourDegrees": [10,4],
            "colourOrbitalSizes": [2160,2160],
        },
        "exactGramIdentities": {
            "sameColour": "M+ M+^T = M- M-^T = 10 I + A30",
            "crossColour": "M+ M-^T + M- M+^T = 4 A20",
            "union": "M M^T = 20 I + 2 A30 + 4 A20",
            "A30Degree": 30,
            "A20Degree": 20,
            "A30A20Commute": True,
            "supportsDisjoint": True,
        },
        "spectra": {
            "A30": {str(k):v for k,v in sorted(mult30.items())},
            "A20": {str(k):v for k,v in sorted(mult20.items())},
            "jointSectors": [
                {"A30":a,"A20":b,"dimension":m,"unionGramEigenvalue":20+2*a+4*b}
                for a,b,m in joint
            ],
            "jointSectorDimensions": sorted(m for _a,_b,m in joint),
            "unionGram": {str(k):v for k,v in sorted(gram_mult.items())},
            "bipartiteAdjacency": "0^324 plus +/-sqrt(lambda) for lambda in {160^1,64^24,28^60,16^35,4^96}",
        },
        "algebra": {
            "dimensionGeneratedByA30A20": 7,
            "separatingOperator": "A30 + 7 A20",
            "separatingSpectrum": sep_roots,
            "proofMode": "exact integer annihilating polynomials plus trace multiplicities; no floating-point diagonalization",
        },
        "theorem": "The two maximal-overlap colours are isospectral (10,4)-biregular incidence systems. Their same-colour and cross-colour Gram operators generate a 7-sector commutative spectral algebra on the 216 five-circuits, and the union incidence has Gram spectrum 160^1+64^24+28^60+16^35+4^96.",
        "boundary": "The seven joint sectors are exact PSp-invariant spectral sectors of this incidence algebra; irreducibility as complex PSp(4,3) modules is not asserted here.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":"PASS","jointDimensions":sorted(m for _a,_b,m in joint),"gramSpectrum":dict(sorted(gram_mult.items()))},sort_keys=True))


if __name__ == "__main__":
    main()
