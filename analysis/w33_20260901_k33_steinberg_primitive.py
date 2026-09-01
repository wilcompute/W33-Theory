#!/usr/bin/env python3
"""Resolve the rank-3 K3,3/Steinberg coupling from the router certificate.

The preceding exact router found, on the 9-dimensional left-regular model of
the M3 Steinberg commutant block,

    charpoly(K) = x^6 (x-8)^3

and rank-3 off-diagonal couplings between the intrinsic 81+162 tensor sectors.
This script decides the stronger possibility objectwise in the orbital algebra:

    K^2 = 8 K.

If true, K/8 is a genuine primitive idempotent of actual permutation-space
rank 81, selected geometrically by the Schlaefli K3,3 incidence Gram.  We then
measure its exact compression against the intrinsic 20_chart x 15_W33
Steinberg copy instead of treating the noncommutation as a failure.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
import w33_20260901_k33_steinberg_router as router
from w33_20260831_all5_frontier_audit import orbit_ids
from w33_20260831_c5_wedderburn_kernel import orbital_mult, center_equations, generic_center, mulvec
from w33_pass4992_4999_common import build_base
from w33_20260901_eisenstein_schlaefli_obstruction_bridge import q4_cycles

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260901_K33_STEINBERG_PRIMITIVE.json"


def proportional_scalar(A: sp.Matrix, B: sp.Matrix):
    """Return q if A=qB exactly, else None."""
    q = None
    for i in range(A.rows):
        for j in range(A.cols):
            a, b = A[i, j], B[i, j]
            if b == 0:
                if a != 0:
                    return None
            else:
                z = sp.factor(a / b)
                if q is None:
                    q = z
                elif z != q:
                    return None
    return sp.Integer(0) if q is None else q


def main():
    acts, charts, wlines = obs.build_action()
    rel, reps, _sizes = orbit_ids(acts, acts, 1080, 1080)
    assert len(reps) == 59
    T = orbital_mult(rel, reps)
    Z = center_equations(T).nullspace()
    assert len(Z) == 15
    diag = int(rel[0, 0])
    one = sp.zeros(59, 1)
    one[diag] = 1
    z, _L, _cp, factors, _coeff = generic_center(Z, T)
    records, idempotents = obs.central_records(z, factors, T, one, diag)
    si = next(i for i, r in enumerate(records) if r["complexIrrepDegree"] == 81)
    E = idempotents[si]
    assert 1080 * E[diag] == 243

    # Exact 9d left-regular representation of the M3 multiplicity algebra.
    cols = []
    for j in range(59):
        q = sp.zeros(59, 1)
        q[j] = 1
        cols.append(mulvec(E, q, T))
    B = sp.Matrix.hstack(*cols)
    _r, piv = B.rref()
    piv = list(piv)
    assert len(piv) == 9
    U = sp.Matrix.hstack(*[cols[j] for j in piv])
    _rr, rowp = U.T.rref()
    rowp = list(rowp)
    assert len(rowp) == 9
    Uinv = U[rowp, :].inv()
    coord = lambda v: Uinv * v[rowp, :]

    def left_matrix(v):
        M = sp.zeros(9, 9)
        for k in range(9):
            M[:, k] = coord(mulvec(v, U[:, k], T))
        return M

    cubic, G27, q4, q0, phi, _mp = router.bridge(acts, charts)

    # Reconstruct the Pass4850 C4 x K3,3 incidence Gram row, then identify its
    # orbital-algebra element exactly as in the router.
    K33 = []
    for S in itertools.combinations(range(27), 6):
        H = G27.subgraph(S)
        if H.number_of_edges() == 9 and set(dict(H.degree()).values()) == {3} and nx.is_bipartite(H):
            A, C = nx.algorithms.bipartite.sets(H)
            if len(A) == len(C) == 3:
                K33.append(frozenset(S))
    assert len(K33) == 360
    kof = [set() for _ in range(1080)]
    for j, S in enumerate(K33):
        for i, C in enumerate(q4):
            if C <= S:
                kof[i].add(j)
    assert {len(S) for S in kof} == {3}
    baseK = kof[q0]
    row = [len(baseK & kof[phi[j]]) for j in range(1080)]
    kval = [None] * 59
    for j, v in enumerate(row):
        r = int(rel[0, j])
        if kval[r] is None:
            kval[r] = v
        else:
            assert kval[r] == v
    assert all(v is not None for v in kval)
    Kvec = sp.Matrix(kval)
    KE = mulvec(E, Kvec, T)
    KM = left_matrix(KE)

    # Intrinsic 81+162 tensor split, replayed exactly.
    A27 = nx.to_numpy_array(
        nx.Graph([(a, b) for a, b in itertools.combinations(range(27), 2)
                  if set(charts[a]) & set(charts[b])]),
        nodelist=range(27), dtype=int,
    )
    A40 = np.zeros((40, 40), dtype=int)
    for a, b in itertools.combinations(range(40), 2):
        if set(wlines[a]) & set(wlines[b]):
            A40[a, b] = A40[b, a] = 1
    P20 = router.projector(A27, 1, [10, 1, -5])
    P15 = router.projector(A40, -4, [12, 2, -4])
    P24 = router.projector(A40, 2, [12, 2, -4])

    def tensor_orbital_vector(Pc, Pl):
        vals = [Pc[0, j // 40] * Pl[0, j % 40] for j in range(1080)]
        out = [None] * 59
        for j, v in enumerate(vals):
            r = int(rel[0, j])
            if out[r] is None:
                out[r] = sp.factor(v)
            else:
                assert out[r] == v
        return sp.Matrix(out)

    S15 = mulvec(E, tensor_orbital_vector(P20, P15), T)
    S24 = mulvec(E, tensor_orbital_vector(P20, P24), T)
    assert S15 + S24 == E
    M15, M24 = left_matrix(S15), left_matrix(S24)
    assert M15.rank() == 3 and M24.rank() == 6

    # The central question: does the K3,3 Gram define a primitive idempotent?
    orbital_quadratic = mulvec(KE, KE, T) == 8 * KE
    regular_quadratic = KM * KM == 8 * KM
    assert orbital_quadratic == regular_quadratic
    Qvec = KE / 8
    QM = KM / 8
    q_idempotent = mulvec(Qvec, Qvec, T) == Qvec and QM * QM == QM
    q_regular_rank = int(QM.rank())
    q_actual_rank = sp.factor(1080 * Qvec[diag]) if q_idempotent else None

    # Exact relative position of the geometric K33 copy and intrinsic 20x15
    # copy.  In an M3 block two primitive idempotents have scalar sandwich
    # products when their rank-one multiplicity directions are transverse.
    c15 = proportional_scalar(M15 * QM * M15, M15) if q_idempotent else None
    cq = proportional_scalar(QM * M15 * QM, QM) if q_idempotent else None
    trace_overlap = sp.factor(sp.trace(M15 * QM)) if q_idempotent else None
    comm_rank = int((M15 * QM - QM * M15).rank()) if q_idempotent else None

    # Also resolve all four block ranks of the primitive projector relative to
    # the 3+6 intrinsic decomposition.
    block_ranks = {
        "15_Q_15": int((M15 * QM * M15).rank()) if q_idempotent else None,
        "15_Q_24": int((M15 * QM * M24).rank()) if q_idempotent else None,
        "24_Q_15": int((M24 * QM * M15).rank()) if q_idempotent else None,
        "24_Q_24": int((M24 * QM * M24).rank()) if q_idempotent else None,
    }

    primitive81 = bool(q_idempotent and q_regular_rank == 3 and q_actual_rank == 81)
    out = {
        "schema": "w33.20260901.k33-steinberg-primitive.v1",
        "status": "PASS",
        "k33SteinbergOperator": {
            "regularCharpoly": str(sp.factor(KM.charpoly().as_expr())),
            "regularRank": int(KM.rank()),
            "quadraticIdentity_K2_equals_8K": bool(orbital_quadratic),
        },
        "scaledOperator": {
            "Q_equals_K_over_8_isIdempotent": bool(q_idempotent),
            "leftRegularRank": q_regular_rank,
            "actualPermutationSpaceRank": str(q_actual_rank) if q_actual_rank is not None else None,
            "isPrimitiveSteinberg81Projector": primitive81,
        },
        "relativeToIntrinsic20x15Copy": {
            "intrinsicProjectorRegularRank": int(M15.rank()),
            "sandwich_M15_Q_M15_scalar": str(c15) if c15 is not None else None,
            "sandwich_Q_M15_Q_scalar": str(cq) if cq is not None else None,
            "trace_M15_Q": str(trace_overlap) if trace_overlap is not None else None,
            "commutatorRank": comm_rank,
            "blockRanks": block_ranks,
        },
        "theorem": (
            "The certificate decides whether the Schlaefli K3,3 incidence Gram geometrically selects a primitive Steinberg-81 copy inside the three-copy Steinberg isotypic block. "
            "If K^2=8K and rank(K/8)=81, the previous rank-3 off-diagonal routing is reinterpreted as exact mixing between this geometric primitive copy and the intrinsic 20_chart x 15_W33 copy, with the sandwich scalar recording their relative position."
        ),
        "boundary": (
            "This is a theorem about the finite PSp(4,3) commutant and its permutation module. "
            "A primitive Steinberg projector is not by itself a particle, field, hardware channel, or dynamical propagator."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "K2eq8K": bool(orbital_quadratic),
        "primitive81": primitive81,
        "regularRank": q_regular_rank,
        "actualRank": str(q_actual_rank),
        "sandwich": [str(c15), str(cq)],
        "commRank": comm_rank,
        "blockRanks": block_ranks,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
