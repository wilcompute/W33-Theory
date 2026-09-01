#!/usr/bin/env python3
"""Resolve the K3,3-selected primitive Steinberg copy and its exact frame.

The preceding router found, on the 9-dimensional left-regular model of the M3
Steinberg commutant block,

    charpoly(K) = x^6 (x-8)^3

and rank-3 off-diagonal couplings between the intrinsic 81+162 tensor sectors.
This script proves the stronger identity K^2=8K, so Q=K/8 is a primitive
rank-81 Steinberg projector, and then resolves its exact position relative to
the intrinsic 20_chart x 15_W33 Steinberg copy P.

The observed sandwich P Q P = Q P Q = P/3,Q/3 is not left as a numerical
angle coincidence.  We construct the normalized projection R of Q into the
intrinsic 162-sector and the residual S.  The exact projector frame P,R,S then
splits the 243-dimensional Steinberg isotypic component into three mutually
orthogonal 81-dimensional copies; Q lies entirely in the P+R plane and is
orthogonal to S.  Thus the K3,3 incidence channel has an exact 81-dimensional
Steinberg-dark complement.
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
    for SS in itertools.combinations(range(27), 6):
        H = G27.subgraph(SS)
        if H.number_of_edges() == 9 and set(dict(H.degree()).values()) == {3} and nx.is_bipartite(H):
            A, C = nx.algorithms.bipartite.sets(H)
            if len(A) == len(C) == 3:
                K33.append(frozenset(SS))
    assert len(K33) == 360
    kof = [set() for _ in range(1080)]
    for j, SS in enumerate(K33):
        for i, C in enumerate(q4):
            if C <= SS:
                kof[i].add(j)
    assert {len(SS) for SS in kof} == {3}
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

    # The central question: the K3,3 Gram is eight times a primitive idempotent.
    orbital_quadratic = mulvec(KE, KE, T) == 8 * KE
    regular_quadratic = KM * KM == 8 * KM
    assert orbital_quadratic == regular_quadratic
    Qvec = KE / 8
    QM = KM / 8
    q_idempotent = mulvec(Qvec, Qvec, T) == Qvec and QM * QM == QM
    q_regular_rank = int(QM.rank())
    q_actual_rank = sp.factor(1080 * Qvec[diag]) if q_idempotent else None

    # Exact relative position of the geometric K33 copy and intrinsic 20x15
    # copy.  Both are symmetric orthogonal projectors in the permutation model,
    # so the scalar 1/3 is the squared multiplicity-space overlap.
    c15 = proportional_scalar(M15 * QM * M15, M15) if q_idempotent else None
    cq = proportional_scalar(QM * M15 * QM, QM) if q_idempotent else None
    trace_overlap = sp.factor(sp.trace(M15 * QM)) if q_idempotent else None
    comm_rank = int((M15 * QM - QM * M15).rank()) if q_idempotent else None

    block_ranks = {
        "15_Q_15": int((M15 * QM * M15).rank()) if q_idempotent else None,
        "15_Q_24": int((M15 * QM * M24).rank()) if q_idempotent else None,
        "24_Q_15": int((M24 * QM * M15).rank()) if q_idempotent else None,
        "24_Q_24": int((M24 * QM * M24).rank()) if q_idempotent else None,
    }

    primitive81 = bool(q_idempotent and q_regular_rank == 3 and q_actual_rank == 81)
    assert primitive81 and c15 == cq == sp.Rational(1, 3)

    # NEW: normalize Q's component inside the intrinsic rank-162 complement.
    # For a rank-one projector q with |<p,q>|^2=1/3, the complementary norm is
    # 2/3, hence R=(3/2)(I-P)Q(I-P) is the rank-one projector onto that component.
    Rvec = sp.Rational(3, 2) * mulvec(S24, mulvec(Qvec, S24, T), T)
    Svec = S24 - Rvec
    RM, SM = left_matrix(Rvec), left_matrix(Svec)
    frame = [M15, RM, SM]
    frame_vec = [S15, Rvec, Svec]
    assert [int(M.rank()) for M in frame] == [3, 3, 3]
    assert all(M * M == M for M in frame)
    assert all(mulvec(v, v, T) == v for v in frame_vec)
    assert all(frame[i] * frame[j] == sp.zeros(9) and frame[j] * frame[i] == sp.zeros(9)
               for i, j in itertools.combinations(range(3), 2))
    assert M15 + RM + SM == sp.eye(9)
    assert S15 + Rvec + Svec == E
    actual_frame_ranks = [sp.factor(1080 * v[diag]) for v in frame_vec]
    assert actual_frame_ranks == [81, 81, 81]

    # Q is supported entirely on the P+R multiplicity plane; S is exactly dark.
    assert SM * QM == sp.zeros(9) and QM * SM == sp.zeros(9)
    rqr = proportional_scalar(RM * QM * RM, RM)
    qrq = proportional_scalar(QM * RM * QM, QM)
    assert rqr == qrq == sp.Rational(2, 3)
    q_on_pr = M15 * QM * M15 + M15 * QM * RM + RM * QM * M15 + RM * QM * RM
    assert q_on_pr == QM
    dark_rank_actual = actual_frame_ranks[2]

    out = {
        "schema": "w33.20260901.k33-steinberg-primitive.v2",
        "status": "PASS",
        "k33SteinbergOperator": {
            "regularCharpoly": str(sp.factor(KM.charpoly().as_expr())),
            "regularRank": int(KM.rank()),
            "quadraticIdentity_K2_equals_8K": bool(orbital_quadratic),
        },
        "scaledOperator": {
            "Q_equals_K_over_8_isIdempotent": bool(q_idempotent),
            "leftRegularRank": q_regular_rank,
            "actualPermutationSpaceRank": str(q_actual_rank),
            "isPrimitiveSteinberg81Projector": primitive81,
        },
        "relativeToIntrinsic20x15Copy": {
            "intrinsicProjectorRegularRank": int(M15.rank()),
            "sandwich_M15_Q_M15_scalar": str(c15),
            "sandwich_Q_M15_Q_scalar": str(cq),
            "squaredOverlap": "1/3",
            "multiplicitySpaceAngle": "arccos(1/sqrt(3))",
            "trace_M15_Q": str(trace_overlap),
            "commutatorRank": comm_rank,
            "blockRanks": block_ranks,
        },
        "orthogonalSteinbergFrame": {
            "regularRanks": [3, 3, 3],
            "actualRanks": [str(x) for x in actual_frame_ranks],
            "sumIsCentralSteinbergProjector": True,
            "pairwiseOrthogonal": True,
            "R_definition": "(3/2) (E-P) Q (E-P)",
            "S_definition": "(E-P)-R",
            "R_Q_R_scalar": str(rqr),
            "Q_R_Q_scalar": str(qrq),
            "Q_supportedEntirelyOn_P_plus_R": True,
            "S_isK33Dark": True,
            "darkActualRank": str(dark_rank_actual),
        },
        "theorem": (
            "The Schlaefli K3,3 incidence Gram is exactly 8Q for a primitive rank-81 Steinberg projector Q. "
            "Its squared overlap with the intrinsic 20_chart x 15_W33 Steinberg copy P is exactly 1/3. "
            "Normalizing Q's component in the intrinsic 162-sector produces a second primitive projector R, and the residual S completes an exact mutually orthogonal 81+81+81 Steinberg frame. "
            "Q lives entirely in the P+R plane and annihilates S, so the K3,3 incidence channel has an exact rank-81 Steinberg-dark complement."
        ),
        "boundary": (
            "This is a theorem about the finite PSp(4,3) commutant and its permutation module. "
            "The 1/3 overlap and dark 81-space are exact representation-theoretic facts, not by themselves particle mixing angles, physical fields, or dynamical propagation laws."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "K2eq8K": True,
        "primitive81": True,
        "sandwich": ["1/3", "1/3"],
        "frameActualRanks": [str(x) for x in actual_frame_ranks],
        "Roverlap": str(rqr),
        "darkRank": str(dark_rank_actual),
        "Qdark": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
