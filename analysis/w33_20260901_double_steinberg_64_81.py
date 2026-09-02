#!/usr/bin/env python3
"""Exceptional-isomorphism audit: the two 216 S5 shells select two Steinbergs.

External group theory gives the exceptional isomorphism

    U4(2) ~= PSp4(3), |G| = 25920.

The same abstract group consequently carries two defining-characteristic
Steinberg characters: degree 2^6=64 from the unitary q=2 BN-pair and degree
3^4=81 from the symplectic q=3 BN-pair.  ATLAS lists ordinary irreducibles of
both dimensions.  The 1080 obstruction permutation module contains each with
multiplicity three.

Holotrade's exact character comparison of the two nonconjugate index-216 S5
actions gives the complementary source pattern:

  five-circuit 216 : contains degree-81 once, degree-64 zero times;
  hemisystem 216   : contains degree-64 once, degree-81 zero times.

This script turns that observation into explicit obstruction-carrier maps.
It reconstructs and primitively splits the 3*64 isotypic block, enumerates the
complete equivariant Hom space from the hemisystem 216 carrier to the 1080
target, and tests whether its cross-Grams span End_G(64^3)=M3(Q).  It also
checks the complementary no-couplings: circuit->64 and hemisystem->81.

References for the external interpretation only (the finite computations are
self-contained in the repo):
  https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/
  https://www.math.rwth-aachen.de/homes/sam/ctbllib/ctbltoc/data/U4%282%29.html
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260901_packet48_bt796_crossid as shell
import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
from w33_20260901_steinberg_frame_common import build as build_frame
from w33_20260831_all5_frontier_audit import orbit_ids
from w33_20260831_c5_wedderburn_kernel import (
    orbital_mult, center_equations, generic_center, mulvec,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260901_DOUBLE_STEINBERG_64_81.json"
T0 = frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL = frozenset(range(40))
x = sp.Symbol("x")


def comp(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def paired_closure(A, B, n, m):
    I = (tuple(range(n)), tuple(range(m)))
    G = {I}
    Q = deque([I])
    while Q:
        a, b = Q.popleft()
        for ga, gb in zip(A, B):
            z = (comp(ga, a), comp(gb, b))
            if z not in G:
                G.add(z)
                Q.append(z)
    assert len(G) == 25920
    return list(G)


def canon_pair(T):
    C = ALL - T
    a, b = tuple(sorted(T)), tuple(sorted(C))
    return (a, b) if a < b else (b, a)


def ideal_coordinates(E, T):
    cols = []
    for j in range(len(E)):
        q = sp.zeros(len(E), 1)
        q[j] = 1
        cols.append(mulvec(E, q, T))
    B = sp.Matrix.hstack(*cols)
    _r, piv = B.rref()
    piv = list(piv)
    assert len(piv) == 9
    U = sp.Matrix.hstack(*[cols[j] for j in piv])
    _rr, rowp = U.T.rref()
    rowp = list(rowp)
    Uinv = U[rowp, :].inv()
    coord = lambda v: Uinv * v[rowp, :]

    def left_matrix(v):
        M = sp.zeros(9, 9)
        for k in range(9):
            M[:, k] = coord(mulvec(v, U[:, k], T))
        return M
    return left_matrix


def split_three_copies(E, rel, reps, T, actual_degree, diag):
    left = ideal_coordinates(E, T)
    tr = []
    for seed in reps:
        a, b = divmod(seed, 1080)
        tr.append(int(rel[b, a]))

    candidates = []
    for j in range(len(reps)):
        q = sp.zeros(len(reps), 1)
        q[j] = 1
        if tr[j] != j:
            q[tr[j]] += 1
        candidates.append((f"orbital:{j}+{tr[j]}", mulvec(E, q, T)))

    # If no single symmetric orbital separates the multiplicity space, add a
    # deterministic small family of rational combinations.
    for a in range(min(20, len(candidates))):
        for b in range(a + 1, min(20, len(candidates))):
            candidates.append((f"pair:{a}+2*{b}", candidates[a][1] + 2*candidates[b][1]))

    chosen = None
    for label, B in candidates:
        if B == sp.zeros(len(E), 1):
            continue
        M = left(B)
        fac = sp.factor_list(sp.Poly(M.charpoly(x).as_expr(), x, domain=sp.QQ))[1]
        if len(fac) != 3:
            continue
        vals = []
        ok = True
        for f, ex in fac:
            if sp.degree(f, x) != 1 or int(ex) != 3:
                ok = False
                break
            p = sp.Poly(f, x, domain=sp.QQ)
            vals.append(sp.factor(-p.nth(0) / p.nth(1)))
        if ok and len(set(vals)) == 3:
            chosen = (label, B, sorted(vals, key=sp.default_sort_key))
            break
    assert chosen is not None

    label, B, vals = chosen
    frame = []
    for lam in vals:
        P = E
        den = sp.Integer(1)
        for mu in vals:
            if mu == lam:
                continue
            P = mulvec(P, B - mu * E, T)
            den *= lam - mu
        P /= den
        assert mulvec(P, P, T) == P
        assert sp.Rational(1080) * P[diag] == actual_degree
        frame.append(P)
    z = sp.zeros(len(E), 1)
    assert sum(frame, z) == E
    for a, b in itertools.combinations(range(3), 2):
        assert mulvec(frame[a], frame[b], T) == z
        assert mulvec(frame[b], frame[a], T) == z
    return label, vals, frame, left


def source_orbital_router(source_gens, target_gens, source_n, target_n, rel, T, E, left, degree):
    G = paired_closure(source_gens, target_gens, source_n, target_n)
    H = [(gs, gt) for gs, gt in G if gs[0] == 0]
    assert len(H) == 25920 // source_n

    unseen = set(range(target_n))
    orbits = []
    while unseen:
        y = min(unseen)
        O = {gt[y] for _gs, gt in H}
        unseen -= O
        orbits.append(sorted(O))
    orbits.sort(key=lambda O: (len(O), O[0]))

    tr = [None] * source_n
    for gs, gt in G:
        s = gs[0]
        if tr[s] is None:
            tr[s] = gt
    assert all(v is not None for v in tr)

    rows = []
    for O in orbits:
        rows.append([frozenset(tr[s][y] for y in O) for s in range(source_n)])

    def cross(i, j):
        row = np.zeros(target_n, dtype=np.int64)
        for s in range(source_n):
            if 0 in rows[i][s]:
                for y in rows[j][s]:
                    row[y] += 1
        oval = [None] * len(E)
        for y, v in enumerate(row.tolist()):
            r = int(rel[0, y])
            if oval[r] is None:
                oval[r] = v
            else:
                assert oval[r] == v
        V = sp.Matrix(oval)
        return mulvec(E, mulvec(V, E, T), T)

    hits = []
    for i in range(len(orbits)):
        X = cross(i, i)
        rr = left(X).rank()
        assert rr % 3 == 0
        actual = int(rr // 3 * degree)
        if actual:
            hits.append((i, actual))

    indep = []
    B = sp.zeros(len(E), 0)
    rank = 0
    for i in range(len(orbits)):
        if rank == 9:
            break
        for j in range(len(orbits)):
            X = cross(i, j)
            if X == sp.zeros(len(E), 1):
                continue
            C = sp.Matrix.hstack(B, X)
            r = C.rank()
            if r > rank:
                indep.append((i, j, X))
                B = C
                rank = r
                if rank == 9:
                    break
    return {
        "homDimension": len(orbits),
        "orbitSizes": [len(O) for O in orbits],
        "selfGramHits": hits,
        "crossSpan": rank,
        "independent": indep,
        "basis": B,
    }


def main():
    F = build_frame()
    acts, rel, reps, T, diag = F["acts"], F["rel"], F["reps"], F["T"], F["diag"]
    E81 = F["E"]

    # Recover the ordinary degree-64 central idempotent from the same exact
    # 59-dimensional orbital algebra.
    Z = center_equations(T).nullspace()
    one = sp.zeros(59, 1)
    one[diag] = 1
    z, _L, _cp, factors, _coeff = generic_center(Z, T)
    records, idempotents = obs.central_records(z, factors, T, one, diag)
    i64 = next(i for i, r in enumerate(records) if r["complexIrrepDegree"] == 64)
    r64 = records[i64]
    assert r64["permutationMultiplicity"] == 3 and r64["carrierDimension"] == 192
    E64 = idempotents[i64]
    assert sp.Rational(1080) * E64[diag] == 192
    split_label, split_vals, frame64, left64 = split_three_copies(E64, rel, reps, T, 64, diag)
    left81 = F["left_matrix"]

    D = shell.build()
    pts, idx, lines, N = base.geometry()
    supports, masks = base.supports_from_N(N)
    assert supports == D["supports"]

    # Circuit 216 action.
    circuits = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            circuits.append(C)
    assert len(circuits) == 216
    cidx = {C: i for i, C in enumerate(circuits)}
    cgens = [tuple(cidx[tuple(sorted(g[x] for x in C))] for C in circuits) for g in D["g45"]]

    # Hemisystem projective-line 216 action.
    orbit432 = {frozenset(p40[x] for x in T0) for p40, _p45, _p27 in D["G"]}
    assert len(orbit432) == 432
    hpairs = sorted({canon_pair(T) for T in orbit432})
    assert len(hpairs) == 216
    hidx = {P: i for i, P in enumerate(hpairs)}
    def hact_perm(p40):
        out = []
        for P in hpairs:
            T0p = frozenset(P[0])
            image = frozenset(p40[x] for x in T0p)
            out.append(hidx[canon_pair(image)])
        return tuple(out)
    hgens = [hact_perm(g) for g in D["g40"]]

    # Main positive router: hemisystem unique 64 -> target 64^3.
    H64 = source_orbital_router(hgens, acts, 216, 1080, rel, T, E64, left64, 64)
    assert all(rank in (64,) for _i, rank in H64["selfGramHits"])

    # Complementary no-couplings are tested via all self-Grams.  For a positive
    # Gram A^T A, vanishing on the central block iff A vanishes on that irrep.
    C64 = source_orbital_router(cgens, acts, 216, 1080, rel, T, E64, left64, 64)
    H81 = source_orbital_router(hgens, acts, 216, 1080, rel, T, E81, left81, 81)
    assert C64["selfGramHits"] == []
    assert H81["selfGramHits"] == []

    solutions64 = {}
    if H64["crossSpan"] == 9:
        B = H64["basis"]
        for k, P64 in enumerate(frame64):
            sol, _ = B.gauss_jordan_solve(P64)
            assert B * sol == P64
            terms = []
            for j, coeff in enumerate(sol):
                if coeff != 0:
                    i0, i1, _X = H64["independent"][j]
                    terms.append({"crossOrbitPair": [i0, i1], "coefficient": str(sp.factor(coeff))})
            solutions64[f"U4Steinberg64_{k}"] = terms

    out = {
        "schema": "w33.20260901.double-steinberg-64-81.v1",
        "status": "PASS",
        "exceptionalIsomorphism": "U4(2) ~= PSp4(3)",
        "externalSteinbergInterpretation": {
            "U4(2)_q2": {"definingCharacteristic": 2, "pPartOrder": 64, "ordinarySteinbergDegree": 64},
            "PSp4(3)_q3": {"definingCharacteristic": 3, "pPartOrder": 81, "ordinarySteinbergDegree": 81},
            "references": [
                "https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/",
                "https://www.math.rwth-aachen.de/homes/sam/ctbllib/ctbltoc/data/U4%282%29.html",
            ],
        },
        "obstruction1080": {
            "U4Steinberg64Multiplicity": 3,
            "U4Steinberg64CarrierDimension": 192,
            "PSpSteinberg81Multiplicity": 3,
            "PSpSteinberg81CarrierDimension": 243,
            "split64Operator": split_label,
            "split64Eigenvalues": [str(v) for v in split_vals],
            "primitive64Ranks": [64, 64, 64],
        },
        "sourceSelectors": {
            "circuit216": {"64SelfGramHits": C64["selfGramHits"], "interpretation": "64 absent"},
            "hemisystem216": {
                "81SelfGramHits": H81["selfGramHits"],
                "interpretation81": "81 absent",
                "64HomDimension": H64["homDimension"],
                "64SelfGramHits": H64["selfGramHits"],
                "64CrossGramSpan": H64["crossSpan"],
                "fullM3_64": H64["crossSpan"] == 9,
            },
        },
        "exact64ProjectorExpansions": solutions64,
        "theorem": (
            "Under the exceptional isomorphism U4(2)~=PSp4(3), the 1080 obstruction "
            "module contains three copies of each defining-characteristic Steinberg "
            "character, degrees 64 and 81.  The two nonconjugate index-216 S5 carriers "
            "select them complementarily: the five-circuit shell has no 64 coupling, "
            "while the hemisystem shell has no 81 coupling.  The hemisystem orbital "
            "maps route its unique 64-dimensional constituent into the target 64^3 "
            "block; if fullM3_64 is true their cross-Grams realize all M3(Q), exactly "
            "mirroring the circuit-to-81 router."
        ),
        "boundary": (
            "'Dual Steinberg selectors' is a representation-theoretic description of "
            "two BN-pair structures on the same abstract finite group.  It is not a "
            "physical duality, particle assignment, or dynamical equivalence."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "split64": split_label,
        "eig64": [str(v) for v in split_vals],
        "H64Hom": H64["homDimension"],
        "H64hits": len(H64["selfGramHits"]),
        "H64span": H64["crossSpan"],
        "C64zero": C64["selfGramHits"] == [],
        "H81zero": H81["selfGramHits"] == [],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
