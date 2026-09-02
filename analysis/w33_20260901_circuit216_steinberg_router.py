#!/usr/bin/env python3
"""Route the unique Steinberg copy of the 216 five-circuit shell into St^3.

Holotrade's exact permutation-character audit proves that the 216 sentinel
five-circuit action contains Steinberg-81 with multiplicity one, whereas the
1080 obstruction carrier contains it with multiplicity three.  Therefore the
Steinberg part of Hom_G(Q[216],Q[1080]) has dimension three.

This script constructs the complete Hom space objectwise.  For the transitive
circuit carrier G/H, its orbital incidence maps to the 1080 target are indexed
by H-orbits on the target.  We enumerate all of them under the same four native
PSp(4,3) generators, build their target Grams and cross-Grams, project into the
exact St^3 central idempotent, and determine:

  * exactly which orbital maps see the circuit Steinberg;
  * the rank of each image inside the 243-dimensional target St^3 block;
  * whether cross-Grams from this 216 carrier span all nine dimensions of
    End_G(St^3) ~= M3(Q);
  * exact rational expansions of P,R,S_dark,Q_K33,E_St3 in an independent
    cross-Gram basis when the span is full.

Thus a PASS with span 9 gives an explicit small Steinberg router; it is not a
claim that circuit states are physical particles or a dark sector.
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
from w33_20260901_steinberg_frame_common import build as build_frame, proportional_scalar
from w33_20260831_c5_wedderburn_kernel import mulvec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_20260901_CIRCUIT216_STEINBERG_ROUTER.json"


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


def main():
    F = build_frame()
    D = shell.build()
    acts, rel, T, E = F["acts"], F["rel"], F["T"], F["E"]
    P, R, S = F["frame"]
    Qk = F["Qvec"]

    # Rebuild the 216 five-circuit carrier in the exact support ordering used
    # by the common native PSp generators.
    pts, idx, lines, N = base.geometry()
    supports, masks = base.supports_from_N(N)
    assert supports == D["supports"]
    circuits = []
    for C in itertools.combinations(range(45), 5):
        w = 0
        for i in C:
            w ^= masks[i]
        if w == 0:
            circuits.append(C)
    assert len(circuits) == 216
    cidx = {C: i for i, C in enumerate(circuits)}

    circuit_gens = []
    for p45 in D["g45"]:
        circuit_gens.append(tuple(cidx[tuple(sorted(p45[x] for x in C))] for C in circuits))

    G = paired_closure(circuit_gens, acts, 216, 1080)
    base_circuit = 0
    H = [(gc, gt) for gc, gt in G if gc[base_circuit] == base_circuit]
    assert len(H) == 120

    # H-orbits on the obstruction target are the complete orbital basis of Hom.
    unseen = set(range(1080))
    orbits = []
    while unseen:
        x = min(unseen)
        O = {gt[x] for _gc, gt in H}
        unseen -= O
        orbits.append(sorted(O))
    orbits.sort(key=lambda O: (len(O), O[0]))

    # One target transporter for each circuit state. H-invariance of each orbit
    # makes the propagated row independent of transporter choice.
    tr = [None] * 216
    for gc, gt in G:
        c = gc[base_circuit]
        if tr[c] is None:
            tr[c] = gt
    assert all(x is not None for x in tr)

    propagated = []
    for O in orbits:
        rows = []
        for c in range(216):
            rows.append(frozenset(tr[c][x] for x in O))
        propagated.append(rows)

    zero = sp.zeros(59, 1)

    def target_cross(i, j):
        # Row 0 of A_i^T A_j; only circuit rows containing target point 0
        # contribute.  Equivariance guarantees constancy on target orbitals.
        row = np.zeros(1080, dtype=np.int64)
        for c in range(216):
            if 0 in propagated[i][c]:
                for y in propagated[j][c]:
                    row[y] += 1
        oval = [None] * 59
        for y, v in enumerate(row.tolist()):
            r = int(rel[0, y])
            if oval[r] is None:
                oval[r] = v
            else:
                assert oval[r] == v
        v = sp.Matrix(oval)
        return mulvec(E, mulvec(v, E, T), T)

    def sandwich(A, B, C):
        return mulvec(A, mulvec(B, C, T), T)

    records = []
    st_hits = []
    for i, O in enumerate(orbits):
        X = target_cross(i, i)
        rr = F["left_matrix"](X).rank()
        assert rr % 3 == 0
        actual = int(rr // 3 * 81)
        # Source contains Steinberg once, so A_i^T A_i can only have target
        # Steinberg rank 0 or 81.
        assert actual in (0, 81)
        scal = {}
        for name, Z in [("P", P), ("R", R), ("S", S), ("Q", Qk)]:
            q = proportional_scalar(sandwich(Z, X, Z), Z)
            scal[name] = None if q is None else str(sp.factor(q))
        if actual == 81:
            st_hits.append(i)
        records.append({
            "orbit": i,
            "targetOrbitSize": len(O),
            "steinbergImageRank": actual,
            "primitiveSandwichScalars": scal,
        })

    # Cross-Grams of different circuit->target maps are rank-one operators on
    # the three-dimensional Steinberg multiplicity space.  Scan until their
    # span reaches the full 9-dimensional matrix algebra.
    indep = []
    basis = sp.zeros(59, 0)
    rank = 0
    for i in range(len(orbits)):
        if rank == 9:
            break
        for j in range(len(orbits)):
            X = target_cross(i, j)
            if X == zero:
                continue
            C = sp.Matrix.hstack(basis, X)
            r = C.rank()
            if r > rank:
                indep.append((i, j, X))
                basis = C
                rank = r
                if rank == 9:
                    break

    solutions = {}
    if rank == 9:
        for name, Z in [("P", P), ("R", R), ("S_dark", S), ("Q_K33", Qk), ("E_St3", E)]:
            sol, _ = basis.gauss_jordan_solve(Z)
            assert basis * sol == Z
            terms = []
            for k, coeff in enumerate(sol):
                if coeff != 0:
                    terms.append({
                        "crossOrbitPair": [indep[k][0], indep[k][1]],
                        "coefficient": str(sp.factor(coeff)),
                    })
            solutions[name] = terms

    out = {
        "schema": "w33.20260901.circuit216-steinberg-router.v1",
        "status": "PASS",
        "groupOrder": 25920,
        "sourceCarrier": 216,
        "sourceStabilizerOrder": 120,
        "sourceSteinbergMultiplicity": 1,
        "targetCarrier": 1080,
        "targetSteinbergMultiplicity": 3,
        "equivariantHomDimension": len(orbits),
        "targetOrbitSizes": [len(O) for O in orbits],
        "orbitalMaps": records,
        "steinbergSeeingOrbitalMaps": st_hits,
        "steinbergCrossGramSpanDimension": rank,
        "independentCrossOrbitPairs": [[i, j] for i, j, _X in indep],
        "fullM3Realized": bool(rank == 9),
        "exactProjectorExpansions": solutions,
        "theorem": (
            "The complete PSp-equivariant Hom space from the 216 five-circuit "
            "permutation carrier to the 1080 obstruction carrier is enumerated by "
            "the recorded S5-stabilizer orbits.  Every nonzero Steinberg image has "
            "rank 81, as forced by the unique source Steinberg.  If the recorded "
            "cross-Gram span is nine, these maps from the 216 carrier alone realize "
            "the full M3(Q) multiplicity algebra of the target St^3 block, with "
            "explicit rational formulas for all three primitive projectors."
        ),
        "boundary": (
            "This is finite characteristic-zero representation theory.  It neither "
            "identifies the Steinberg module with a physical particle sector nor "
            "assigns dynamics or observables to the circuit states."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "HomDim": len(orbits),
        "StHits": len(st_hits),
        "crossSpan": rank,
        "fullM3": rank == 9,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
