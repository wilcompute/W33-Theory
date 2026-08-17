#!/usr/bin/env python3
"""Passes 5720--5724: exact integral homology and affine action of the Pass5691 face complex.

The finite 2-complex X has AG(2,3) as its nine vertices, K9 as its 1-skeleton,
54 translation-parallelogram 2-cells, and 12 affine-line triangular 2-cells.
Pass5691 found rank(d2)=28 over Q but 26 over F3.  Here we compute the integral
Smith form on an integral cycle basis and the induced AGL(2,3) action.

Main theorem:
  H0(X;Z)=Z,
  H1(X;Z)=(Z/3)^2,
  H2(X;Z)=Z^38.
The plaquette-only complex X_P has H1(X_P;Z)=Z^4 and H2(X_P;Z)=Z^30.
Attaching the 12 line triangles therefore maps onto a rank-4 sublattice of
H1(X_P;Z) with Smith invariants (1,1,3,3), converting four free modes into two
3-torsion classes.

The full affine group AGL(2,3) preserves X.  Its translation subgroup of order 9
acts trivially on H1(X;F3); the induced image has order 48 and is GL(2,3).  In the
explicit quotient basis below, the linear part M acts by a conjugate of
    det(M) M^T.

Physics boundary: the two F3 modes are torsion/Bockstein modes. They have no real
harmonic lift, do not fix the Yang--Mills coupling, and are not identified with
Pass5121's unrelated one-dimensional Z/3 saturation quotient.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5720_5724_AFFINE_TORSION_HOMOLOGY.json"
Q = 3
PTS = [(x, y) for x in range(Q) for y in range(Q)]
IDX = {p: i for i, p in enumerate(PTS)}
DIRS = [(1, 0), (0, 1), (1, 1), (1, 2)]
EDGES = list(itertools.combinations(range(9), 2))
EI = {e: i for i, e in enumerate(EDGES)}
TREE = [(0, i) for i in range(1, 9)]
CHORD_IDX = [j for j, e in enumerate(EDGES) if e not in TREE]
CHORD_EDGES = [EDGES[j] for j in CHORD_IDX]


def rank_mod(A, p):
    A = np.asarray(A, dtype=np.int64).copy() % p
    m, n = A.shape
    r = 0
    for c in range(n):
        nz = np.flatnonzero(A[r:, c])
        if not len(nz):
            continue
        i = r + int(nz[0])
        A[[r, i]] = A[[i, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        rows = np.flatnonzero(A[:, c])
        rows = rows[rows != r]
        if len(rows):
            A[rows] = (A[rows] - A[rows, c, None] * A[r, None, :]) % p
        r += 1
        if r == m:
            break
    return r


def rref_mod(A, p=3):
    A = np.asarray(A, dtype=np.int64).copy() % p
    m, n = A.shape
    r = 0
    pivots = []
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i, c] % p), None)
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for i in range(m):
            if i != r and A[i, c] % p:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        pivots.append(c)
        r += 1
        if r == m:
            break
    return A[:r], pivots


def edge_row(vertices):
    row = np.zeros(36, dtype=int)
    cyc = list(vertices) + [vertices[0]]
    for a, b in zip(cyc, cyc[1:]):
        e = tuple(sorted((a, b)))
        row[EI[e]] += 1 if a < b else -1
    return row


def canonical_sign(row):
    t = tuple(map(int, row))
    nt = tuple(-x for x in t)
    return min(t, nt)


def build_complex():
    b1 = np.zeros((9, 36), dtype=int)
    for j, (u, v) in enumerate(EDGES):
        b1[u, j] = -1
        b1[v, j] = 1

    plaquettes = []
    for d1, d2 in itertools.combinations(DIRS, 2):
        for p in PTS:
            p1 = ((p[0] + d1[0]) % 3, (p[1] + d1[1]) % 3)
            p12 = ((p1[0] + d2[0]) % 3, (p1[1] + d2[1]) % 3)
            p2 = ((p[0] + d2[0]) % 3, (p[1] + d2[1]) % 3)
            plaquettes.append(edge_row([IDX[p], IDX[p1], IDX[p12], IDX[p2]]))
    P = np.asarray(plaquettes, dtype=int)

    lines = set()
    for p in PTS:
        for d in DIRS:
            L = tuple(sorted(IDX[((p[0] + t * d[0]) % 3,
                                  (p[1] + t * d[1]) % 3)] for t in range(3)))
            lines.add(L)
    lines = sorted(lines)
    T = np.asarray([edge_row(list(L)) for L in lines], dtype=int)
    return b1, P, T, lines


def smith_nonzero(A):
    D = smith_normal_form(sp.Matrix(A.tolist()), domain=ZZ)
    return [abs(int(D[i, i])) for i in range(min(D.rows, D.cols)) if D[i, i] != 0]


def fundamental_cycles():
    F = np.zeros((28, 36), dtype=int)
    for a, (u, v) in enumerate(CHORD_EDGES):
        # 0 -> u -> v -> 0, with chord (u,v) coefficient +1.
        for x, y in [(0, u), (u, v), (v, 0)]:
            e = tuple(sorted((x, y)))
            F[a, EI[e]] += 1 if x < y else -1
    return F


def affine_perm(M, b):
    return [IDX[((int(M[0, 0]) * x + int(M[0, 1]) * y + b[0]) % 3,
                 (int(M[1, 0]) * x + int(M[1, 1]) * y + b[1]) % 3)]
            for x, y in PTS]


def transform_chain(row, perm):
    out = np.zeros(36, dtype=int)
    for j, coeff in enumerate(row):
        if not coeff:
            continue
        u, v = EDGES[j]
        pu, pv = perm[u], perm[v]
        e = tuple(sorted((pu, pv)))
        out[EI[e]] += int(coeff) * (1 if pu < pv else -1)
    return out


def invert2(A):
    A = np.asarray(A, dtype=int) % 3
    a, b, c, d = map(int, A.flat)
    det = (a * d - b * c) % 3
    invd = pow(det, -1, 3)
    return (invd * np.array([[d, -b], [-c, a]], dtype=int)) % 3


def main():
    b1, P, T, lines = build_complex()
    PT = np.vstack([P, T])
    F = fundamental_cycles()

    assert P.shape == (54, 36) and T.shape == (12, 36) and PT.shape == (66, 36)
    assert len({canonical_sign(r) for r in P}) == 54
    assert len({canonical_sign(r) for r in T}) == 12
    assert np.max(np.abs(P @ b1.T)) == 0
    assert np.max(np.abs(T @ b1.T)) == 0
    assert sp.Matrix(b1.tolist()).rank() == 8
    assert np.max(np.abs(F @ b1.T)) == 0
    assert np.array_equal(F[:, CHORD_IDX], np.eye(28, dtype=int))

    # Star-tree chord projection is an integral isomorphism Z_1 -> Z^28.
    Pcyc = P[:, CHORD_IDX]
    Tcyc = T[:, CHORD_IDX]
    PTcyc = PT[:, CHORD_IDX]
    snf_P = smith_nonzero(Pcyc.T)
    snf_PT = smith_nonzero(PTcyc.T)
    assert Counter(snf_P) == Counter({1: 24})
    assert Counter(snf_PT) == Counter({1: 26, 3: 2})

    rank_P_Q = sp.Matrix(Pcyc.tolist()).rank()
    rank_PT_Q = sp.Matrix(PTcyc.tolist()).rank()
    assert (rank_P_Q, rank_PT_Q) == (24, 28)

    # Integral homology.  With no 3-cells, H2=ker(d2) is free.
    H1_P_free = 28 - rank_P_Q
    H2_P_free = 54 - rank_P_Q
    H2_full_free = 66 - rank_PT_Q
    assert (H1_P_free, H2_P_free, H2_full_free) == (4, 30, 38)

    # Since the plaquette sublattice is primitive (all its nonzero SNF entries are 1),
    # the 12 triangle attachments induce a full-rank map Z^12 -> H1(X_P)=Z^4.
    # Its cokernel is H1(X)=(Z/3)^2, hence its four nonzero Smith invariants are 1,1,3,3.
    triangle_attachment_snf = [1, 1, 3, 3]

    field_table = {}
    for p in [2, 3, 5, 7, 11, 13]:
        rP = rank_mod(Pcyc, p)
        rPT = rank_mod(PTcyc, p)
        field_table[str(p)] = {
            "rank_translation_faces": rP,
            "rank_full_faces": rPT,
            "dim_H1_translation": 28 - rP,
            "dim_H1_full": 28 - rPT,
            "dim_H2_full": 66 - rPT,
        }
    assert field_table["3"]["dim_H1_full"] == 2
    assert field_table["3"]["dim_H2_full"] == 40
    for p in [2, 5, 7, 11, 13]:
        assert field_table[str(p)]["dim_H1_full"] == 0
        assert field_table[str(p)]["dim_H2_full"] == 38

    # Full AGL(2,3) action on the two-dimensional F3 homology.
    R, pivots = rref_mod(PTcyc, 3)
    nonp = [j for j in range(28) if j not in pivots]
    assert len(pivots) == 26 and len(nonp) == 2

    def quotient_coord(v):
        v = np.asarray(v, dtype=int).copy() % 3
        for i, p in enumerate(pivots):
            if v[p] % 3:
                v = (v - v[p] * R[i]) % 3
        assert all(v[p] % 3 == 0 for p in pivots)
        return v[nonp] % 3

    def quotient_action(M, b):
        perm = affine_perm(M, b)
        A = np.zeros((28, 28), dtype=int)
        for j in range(28):
            A[j] = transform_chain(F[j], perm)[CHORD_IDX] % 3
        Qm = np.zeros((2, 2), dtype=int)
        for i, j in enumerate(nonp):
            Qm[i] = quotient_coord(A[j])
        return Qm % 3

    GL = []
    for vals in itertools.product(range(3), repeat=4):
        M = np.array(vals, dtype=int).reshape(2, 2)
        det = (int(M[0, 0]) * int(M[1, 1]) - int(M[0, 1]) * int(M[1, 0])) % 3
        if det:
            GL.append(M)
    assert len(GL) == 48

    pset = {canonical_sign(r) for r in P}
    tset = {canonical_sign(r) for r in T}
    image = set()
    kernel = []
    all_face_preserving = True
    Pconj = np.array([[0, 1], [1, 1]], dtype=int)
    Pinv = invert2(Pconj)
    formula_ok = True
    for M in GL:
        det = (int(M[0, 0]) * int(M[1, 1]) - int(M[0, 1]) * int(M[1, 0])) % 3
        expected = (Pinv @ ((det * M.T) % 3) @ Pconj) % 3
        for b in PTS:
            perm = affine_perm(M, b)
            if any(canonical_sign(transform_chain(r, perm)) not in pset for r in P):
                all_face_preserving = False
            if any(canonical_sign(transform_chain(r, perm)) not in tset for r in T):
                all_face_preserving = False
            Qm = quotient_action(M, b)
            image.add(tuple(map(int, Qm.flat)))
            if np.array_equal(Qm, np.eye(2, dtype=int)):
                kernel.append((tuple(map(int, M.flat)), b))
            if not np.array_equal(Qm, expected):
                formula_ok = False
    assert all_face_preserving
    assert len(image) == 48
    assert len(kernel) == 9
    assert all(k[0] == (1, 0, 0, 1) for k in kernel)
    assert formula_ok

    # Distinguish this carrier from Pass5121's 81x108 rank-one Z/3 saturation quotient.
    out = {
        "passes": [5720, 5721, 5722, 5723, 5724],
        "status": "THEOREM_AFFINE_FACE_COMPLEX_HAS_Z3_SQUARED_H1_AND_GL23_TORSION_ACTION",
        "complex": {
            "vertices": 9,
            "edges": 36,
            "translation_plaquettes": 54,
            "affine_line_triangles": 12,
            "cycle_rank_integral": 28,
        },
        "pass5720_integral_homology": {
            "translation_only_snf_nonzero": snf_P,
            "full_snf_nonzero": snf_PT,
            "H0_Z": "Z",
            "H1_translation_Z": "Z^4",
            "H2_translation_Z": "Z^30",
            "H1_full_Z": "(Z/3)^2",
            "H2_full_Z": "Z^38",
        },
        "pass5721_triangle_attachment": {
            "induced_map_to_H1_translation_rank": 4,
            "induced_map_snf_nonzero": triangle_attachment_snf,
            "index_in_H1_translation": 9,
            "mechanism": "the 12 line triangles kill all four free real modes, but two attachment directions are 3-divisible in the integral quotient, leaving two order-3 classes",
        },
        "pass5722_field_and_bockstein": {
            "field_ranks": field_table,
            "H1_Z_cohomology": "0",
            "H2_Z_cohomology": "Z^38 + (Z/3)^2",
            "interpretation": "the F3-only H1/H^1 pair is a torsion/Bockstein effect; it has no R-valued harmonic lift",
        },
        "pass5723_affine_symmetry": {
            "AGL23_order": 432,
            "homology_action_kernel_order": len(kernel),
            "kernel": "translation subgroup F3^2",
            "homology_action_image_order": len(image),
            "image": "GL(2,3)",
            "explicit_basis_nonpivot_chords": [list(map(int, CHORD_EDGES[j])) for j in nonp],
            "action_formula": "Q(M,b)=P^{-1}(det(M) M^T)P over F3, P=[[0,1],[1,1]], independent of translation b",
        },
        "pass5724_firewall": {
            "pass5121_comparison": "distinct carrier: Pass5121 uses an 81x108 incidence matrix and a one-dimensional Z/3 saturation quotient; this complex uses the 9-vertex/36-edge affine face chain complex and has (Z/3)^2",
            "no_chain_map_claimed": True,
            "physics_boundary": "The torsion theorem does not determine the Yang-Mills coupling g, a continuum limit, confinement, matter content, or a physical discrete gauge symmetry. The old vertical Z3 connection remains adjoint-trivial as in Pass5691.",
        },
        "external_context": {
            "discrete_gauge_theory": "Graph/cell-complex Yang-Mills formalisms and homology-sensitive lattice gauge theories exist in the literature; this theorem is the exact integral homology of the repository's specific AG(2,3) face complex.",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
