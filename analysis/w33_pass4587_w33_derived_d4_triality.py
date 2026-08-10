#!/usr/bin/env python3
"""Pass 4587 -- reconstruct finite D4 triality from the W33-derived O+(8,2) quotient.

Pass 4579 reconstructed the 8-dimensional plus-type quadratic space directly
from W33 apartment and opposite-edge lifts.  This pass uses only that same W33
reconstruction to recover the two half-spinor families of maximal totally
singular 4-spaces and the exact three-leg incidence algebra.

Nothing here identifies finite half-spinor objects with physical spinor fields.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

from w33_apartment_section_core import build_geometry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4587_D4_TRIALITY.json"


def rank_basis_int(vecs):
    piv = {}
    for x in map(int, vecs):
        y = x
        while y:
            p = y.bit_length() - 1
            if p in piv:
                y ^= piv[p]
            else:
                piv[p] = y
                break
    return list(piv.values())


def span(basis):
    out = [0]
    for b in basis:
        out += [x ^ b for x in list(out)]
    return out


def main() -> int:
    vals = build_geometry()
    A40 = np.asarray(vals[5], dtype=np.uint8)
    n = 40
    j = (1 << n) - 1

    cols = []
    for c in range(n):
        m = 0
        for r in np.flatnonzero(A40[:, c]):
            m |= 1 << int(r)
        cols.append(m)

    edges = [(i, k) for i in range(n) for k in range(i + 1, n) if A40[i, k]]
    edge_vec = [cols[i] ^ cols[k] for i, k in edges]
    B9 = rank_basis_int(edge_vec)
    assert len(B9) == 9
    V9 = set(span(B9))
    assert len(V9) == 512 and j in V9
    reps = {min(x, x ^ j) for x in V9}
    assert len(reps) == 256

    def rep(x):
        return min(int(x), int(x) ^ j)

    def q(x):
        return (rep(x).bit_count() // 4) & 1

    def polar(x, y):
        return q(x) ^ q(y) ^ q(rep(x) ^ rep(y))

    singular = sorted(x for x in reps if x and q(x) == 0)
    assert len(singular) == 135

    # Enumerate every totally singular linear subspace recursively.  A new
    # vector may extend S precisely when it is polar-orthogonal to S.
    levels = {0: {frozenset((0,))}}
    for d in range(4):
        nxt = set()
        for S in levels[d]:
            for v in singular:
                if v in S or any(polar(v, u) for u in S):
                    continue
                T = frozenset(set(S) | {rep(u ^ v) for u in S})
                if len(T) == (1 << (d + 1)) and all(q(u) == 0 for u in T):
                    nxt.add(T)
        levels[d + 1] = nxt

    assert [len(levels[d]) for d in range(1, 5)] == [135, 1575, 2025, 270]
    generators = sorted(levels[4], key=lambda S: tuple(sorted(S)))

    # In plus type dimension eight, the 270 maximal singular 4-spaces split
    # into two 135-families.  Relative to one generator, same-family
    # intersections have even vector-space dimension and opposite-family
    # intersections have odd dimension.
    G0 = generators[0]

    def idim(G, H):
        return (len(G & H)).bit_length() - 1

    fam_a = [G for G in generators if idim(G0, G) % 2 == 0]
    fam_b = [G for G in generators if idim(G0, G) % 2 == 1]
    assert (len(fam_a), len(fam_b)) == (135, 135)
    assert Counter(len(G0 & G) for G in generators) == Counter({1: 64, 2: 120, 4: 70, 8: 15, 16: 1})

    pidx = {x: i for i, x in enumerate(singular)}

    def point_generator_incidence(fam):
        M = np.zeros((135, 135), dtype=np.int16)
        for col, G in enumerate(fam):
            for x in G:
                if x:
                    M[pidx[x], col] = 1
        return M

    M_pa = point_generator_incidence(fam_a)
    M_pb = point_generator_incidence(fam_b)
    M_ab = np.zeros((135, 135), dtype=np.int16)
    for a, G in enumerate(fam_a):
        for b, H in enumerate(fam_b):
            # Adjacent outer D4 nodes: maximal singular spaces meet in a
            # 3-dimensional vector subspace (7 nonzero points).
            if len(G & H) == 8:
                M_ab[a, b] = 1

    for M in (M_pa, M_pb, M_ab):
        assert set(map(int, M.sum(axis=0))) == {15}
        assert set(map(int, M.sum(axis=1))) == {15}

    # Each outer type carries the same SRG(135,70,37,35) relation.
    A_p = np.zeros((135, 135), dtype=np.int16)
    for a, x in enumerate(singular):
        for b, y in enumerate(singular):
            if a != b and polar(x, y) == 0:
                A_p[a, b] = 1

    def generator_graph(fam):
        G = np.zeros((135, 135), dtype=np.int16)
        for a, X in enumerate(fam):
            for b in range(a + 1, 135):
                # Same-family distance one: 2-dimensional vector intersection.
                if len(X & fam[b]) == 4:
                    G[a, b] = G[b, a] = 1
        return G

    A_a = generator_graph(fam_a)
    A_b = generator_graph(fam_b)

    def assert_srg(A):
        assert np.all(np.diag(A) == 0)
        assert set(map(int, A.sum(axis=1))) == {70}
        lam = set()
        mu = set()
        for i in range(135):
            for k in range(i + 1, 135):
                c = int(A[i] @ A[k])
                (lam if A[i, k] else mu).add(c)
        assert lam == {37} and mu == {35}

    for G in (A_p, A_a, A_b):
        assert_srg(G)

    I = np.eye(135, dtype=np.int64)
    J = np.ones((135, 135), dtype=np.int64)

    # The three incidence matrices have identical Gram laws.
    for M, G in ((M_pa, A_p), (M_pb, A_p), (M_ab, A_a)):
        Mi = M.astype(np.int64)
        assert np.array_equal(Mi @ Mi.T, 15 * I + 3 * G)

    # Triality composition before centering: an incident endpoint has seven
    # middle objects; a nonincident endpoint has one.
    assert np.array_equal(M_pa.astype(np.int64) @ M_ab.astype(np.int64), J + 6 * M_pb)
    assert np.array_equal(M_pb.astype(np.int64) @ M_ab.astype(np.int64).T, J + 6 * M_pa)
    assert np.array_equal(M_pa.astype(np.int64).T @ M_pb.astype(np.int64), J + 6 * M_ab)

    # Remove the trivial all-ones constituent without fractions.  D=9M-J has
    # row/column sum zero and the exact triality algebra D12 D23 = 54 D13.
    D_pa = 9 * M_pa.astype(np.int64) - J
    D_pb = 9 * M_pb.astype(np.int64) - J
    D_ab = 9 * M_ab.astype(np.int64) - J
    assert np.array_equal(D_pa @ D_ab, 54 * D_pb)
    assert np.array_equal(D_pb @ D_ab.T, 54 * D_pa)
    assert np.array_equal(D_pa.T @ D_pb, 54 * D_ab)

    # SRG spectrum follows exactly from (v,k,lambda,mu):
    # 70^1, 7^50, (-5)^84.  Therefore
    # D D^T = 1215 I + 243 A - 135 J has eigenvalues 2916=54^2
    # on the 50-space and zero on the trivial plus 84-space.
    for D, G in ((D_pa, A_p), (D_pb, A_p), (D_ab, A_a)):
        assert np.array_equal(D @ D.T, 1215 * I + 243 * G - 135 * J)
        # Exact rank lower bound modulo a large prime; the displayed Gram law
        # gives the matching upper bound 50 over Q.
        X = (D % 1_000_003).copy()
        rank = 0
        for col in range(135):
            piv = next((r for r in range(rank, 135) if X[r, col]), None)
            if piv is None:
                continue
            X[[rank, piv]] = X[[piv, rank]]
            X[rank] = (X[rank] * pow(int(X[rank, col]), -1, 1_000_003)) % 1_000_003
            for r in range(135):
                if r != rank and X[r, col]:
                    X[r] = (X[r] - int(X[r, col]) * X[rank]) % 1_000_003
            rank += 1
        assert rank == 50

    out = {
        "pass": 4587,
        "source": "W33-derived V8 quotient reconstructed exactly as in Pass 4579",
        "totally_singular_subspaces": {
            "dimension_1": 135,
            "dimension_2": 1575,
            "dimension_3": 2025,
            "dimension_4": 270,
            "maximal_families": [135, 135],
        },
        "outer_D4_types": ["135 singular points", "135 maximal generators A", "135 maximal generators B"],
        "cross_incidence": {
            "row_degree": 15,
            "column_degree": 15,
            "raw_composition": "M_PA M_AB = J + 6 M_PB, cyclically",
            "centered_integer_matrices": "D=9M-J",
            "centered_triality": "D_PA D_AB = 54 D_PB, cyclically",
            "centered_rank_Q": 50,
        },
        "outer_relation_graph": {
            "parameters": "SRG(135,70,37,35)",
            "spectrum": {"70": 1, "7": 50, "-5": 84},
            "gram": "M M^T = 15 I + 3 A",
            "centered_gram": "D D^T = 1215 I + 243 A - 135 J = 54^2 E_50",
        },
        "theorem": "The W33-protected plus-type quotient reconstructs all three 135-element outer-node sets of finite D4 triality.  Their centered incidence maps are exact rank-50 intertwiners satisfying a cyclic multiplication law.",
        "boundary": "Finite O+(8,2)/D4 building triality only.  No identification with physical spinors, particle generations, or an E8 lattice shell is made here.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
