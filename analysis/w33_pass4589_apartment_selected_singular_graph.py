#!/usr/bin/env python3
"""Pass 4589 -- graph/incidence factorization of the apartment-selected singular lines.

Pass 4588 showed that the 1620 W33 apartments map 6-to-1 onto a distinguished
PSp(4,3)-orbit of 270 totally singular projective lines in the W33-derived
O+(8,2) quotient.  This pass studies only that 135-point/270-line incidence
structure.

Evidence boundary: the rational rank 120 below is NOT used to identify its row
space with the separate 120-element anisotropic point set.  Equal integers are
not an intertwiner.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from fractions import Fraction

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4589_APARTMENT_SELECTED_SINGULAR_GRAPH.json"


def rank_mod2(M):
    A = np.asarray(M, dtype=np.uint8).copy() & 1
    r = 0
    for c in range(A.shape[1]):
        piv = np.flatnonzero(A[r:, c])
        if len(piv) == 0:
            continue
        rr = r + int(piv[0])
        if rr != r:
            A[[r, rr]] = A[[rr, r]]
        for i in range(A.shape[0]):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        r += 1
        if r == A.shape[0]:
            break
    return r


def main() -> int:
    _, _, _, _, _, Astar, _, apartments, _ = build_geometry()
    Astar = np.asarray(Astar, dtype=np.uint8)
    n = 40
    j = (1 << n) - 1

    cols = []
    for c in range(n):
        m = 0
        for r in np.flatnonzero(Astar[:, c]):
            m |= 1 << int(r)
        cols.append(m)
    edges = [(i, k) for i in range(n) for k in range(i + 1, n) if Astar[i, k]]
    B9 = rank_basis_int([cols[i] ^ cols[k] for i, k in edges])
    V9 = set(span(B9))
    assert len(B9) == 9 and len(V9) == 512 and j in V9
    reps = {min(x, x ^ j) for x in V9}

    def rep(x):
        return min(int(x), int(x) ^ j)

    def q(x):
        return (rep(x).bit_count() // 4) & 1

    singular = sorted(x for x in reps if x and q(x) == 0)
    assert len(singular) == 135
    pidx = {x: i for i, x in enumerate(singular)}

    def apartment_fiber(ap):
        x = 0
        for i in ap:
            x ^= cols[int(i)]
        return rep(x)

    def apartment_line(ap):
        opp = [(a, b) for a, b in combinations(ap, 2) if not Astar[a, b]]
        assert len(opp) == 2
        s = rep(cols[opp[0][0]] ^ cols[opp[0][1]])
        t = rep(cols[opp[1][0]] ^ cols[opp[1][1]])
        x = apartment_fiber(ap)
        assert q(s) == q(t) == q(x) == 0 and rep(s ^ t) == x
        return tuple(sorted((s, t, x)))

    fibers = defaultdict(list)
    for ap in apartments:
        fibers[apartment_line(ap)].append(ap)
    selected = sorted(fibers)
    assert len(selected) == 270
    assert Counter(map(len, fibers.values())) == Counter({6: 270})

    N = np.zeros((135, 270), dtype=np.int64)
    for c, L in enumerate(selected):
        for x in L:
            N[pidx[x], c] = 1
    assert set(map(int, N.sum(axis=1))) == {6}
    assert set(map(int, N.sum(axis=0))) == {3}

    # Two selected projective lines meet in at most one singular point, so the
    # point Gram is exactly 6I plus a simple graph adjacency matrix.
    NN = N @ N.T
    A = NN - 6 * np.eye(135, dtype=np.int64)
    assert set(np.unique(A)).issubset({0, 1})
    assert np.all(np.diag(A) == 0)
    assert set(map(int, A.sum(axis=1))) == {12}
    assert int(A.sum() // 2) == 810

    common_adj = Counter()
    common_non = Counter()
    for i in range(135):
        for k in range(i + 1, 135):
            c = int(A[i] @ A[k])
            (common_adj if A[i, k] else common_non)[c] += 1
    assert common_adj == Counter({1: 810})
    assert common_non == Counter({0: 4455, 3: 2160, 1: 1620})

    # Exact spectrum certificate without a floating eigensolver.  The displayed
    # degree-six squarefree polynomial annihilates A.  Trace moments 0..5 then
    # uniquely determine the multiplicities by the Vandermonde system.
    I = np.eye(135, dtype=np.int64)
    P = I.copy()
    for root in (12, 6, 3, 0, -3, -6):
        P = P @ (A - root * I)
    assert not P.any()

    expected = {12: 1, 6: 15, 3: 20, 0: 60, -3: 24, -6: 15}
    moments = []
    Ak = I.copy()
    for k in range(6):
        moments.append(int(np.trace(Ak)))
        assert moments[-1] == sum(m * (lam ** k) for lam, m in expected.items())
        Ak = Ak @ A
    assert sum(expected.values()) == 135

    # Since N N^T = 6I+A, its nonzero eigenvalues are
    # 18^1,12^15,9^20,6^60,3^24 and its nullity is 15.
    # Hence rank_Q(N)=120 exactly.  Over F2 the rank drops by one more.
    rank_q = 120
    rank_f2 = rank_mod2(N)
    assert rank_f2 == 119

    # The 270 selected lines themselves form the intersection graph
    # L=N^T N - 3I.  Its spectrum follows from the same singular values plus
    # the 150-dimensional column-kernel of N.
    L = N.T @ N - 3 * np.eye(270, dtype=np.int64)
    assert set(np.unique(L)).issubset({0, 1})
    assert set(map(int, L.sum(axis=1))) == {15}
    line_spectrum = {15: 1, 9: 15, 6: 20, 3: 60, 0: 24, -3: 150 + 15}

    # Every edge of A has exactly one common neighbor.  Therefore every edge is
    # in one triangle; 810/3=270 triangles.  Since each selected projective line
    # is visibly a triangle, these are all the triangles and no extras exist.
    assert int(np.trace(A @ A @ A) // 6) == 270

    out = {
        "pass": 4589,
        "incidence": {
            "points": 135,
            "selected_lines": 270,
            "point_degree": 6,
            "line_size": 3,
            "apartment_lifts_per_line": 6,
            "rank_Q": rank_q,
            "rank_F2": rank_f2,
        },
        "point_graph": {
            "vertices": 135,
            "degree": 12,
            "edges": 810,
            "triangles": 270,
            "triangles_are_exactly_selected_lines": True,
            "adjacent_common_neighbors": {"1": 810},
            "nonadjacent_common_neighbors": {"0": 4455, "1": 1620, "3": 2160},
            "spectrum": {str(k): v for k, v in expected.items()},
            "annihilator": "(x-12)(x-6)(x-3)x(x+3)(x+6)",
            "gram": "N N^T = 6 I + A",
        },
        "selected_line_intersection_graph": {
            "vertices": 270,
            "degree": 15,
            "edges": 2025,
            "spectrum": {str(k): v for k, v in line_spectrum.items()},
            "gram": "N^T N = 3 I + L",
        },
        "theorem": "The apartment image is recoverable from a 135-vertex 12-regular graph: its 270 selected singular lines are exactly that graph's triangles. The 135x270 incidence matrix has exact rational rank 120 and binary rank 119.",
        "boundary": "The rational rank 120 is not an identification with the separate 120 anisotropic quotient classes. No such G-set or module isomorphism is claimed without an explicit intertwiner.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
