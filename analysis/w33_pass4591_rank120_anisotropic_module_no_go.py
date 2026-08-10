#!/usr/bin/env python3
"""Pass 4591 -- exact 120-vs-120 PSp(4,3) module no-go.

Pass 4589 found rank_Q(N)=120 for the 135x270 apartment-selected singular-line
incidence matrix.  The same protected O+(8,2) quotient has 120 anisotropic
points.  This script tests the tempting identification as a representation,
not by cardinality.

Result: they are not isomorphic Q[PSp(4,3)]-modules.  A deterministic short
order-six group element has character -1 on row_Q(N) and permutation character
3 on the 120 anisotropic points.
"""
from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, transvection_matrix,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
from w33_pass4588_apartment_triality_obstruction_spread_bridge import compose, perm_group, pmask

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4591_RANK120_ANISOTROPIC_MODULE_NO_GO.json"
P = 1_000_003


def independent_rows_mod(M, p=P):
    A = np.asarray(M, dtype=np.int64).copy() % p
    m, n = A.shape
    row_ids = list(range(m))
    r = 0
    selected = []
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i, c]), None)
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        row_ids[r], row_ids[piv] = row_ids[piv], row_ids[r]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for i in range(m):
            if i != r and A[i, c]:
                A[i] = (A[i] - int(A[i, c]) * A[r]) % p
        selected.append(row_ids[r])
        r += 1
        if r == m:
            break
    return selected, r


def inv_mod(M, p=P):
    M = np.asarray(M, dtype=np.int64).copy() % p
    n = M.shape[0]
    A = np.hstack((M, np.eye(n, dtype=np.int64)))
    for c in range(n):
        piv = next(i for i in range(c, n) if A[i, c])
        if piv != c:
            A[[c, piv]] = A[[piv, c]]
        A[c] = (A[c] * pow(int(A[c, c]), -1, p)) % p
        for i in range(n):
            if i != c and A[i, c]:
                A[i] = (A[i] - int(A[i, c]) * A[c]) % p
    return A[:, n:]


def perm_order(p):
    from math import lcm
    seen = set()
    out = 1
    for i in range(len(p)):
        if i in seen:
            continue
        j = i
        ell = 0
        while j not in seen:
            seen.add(j)
            ell += 1
            j = p[j]
        out = lcm(out, ell)
    return out


def main() -> int:
    pts, pidx, lines, lidx, _, Astar, _, apartments, _ = build_geometry()
    Astar = np.asarray(Astar, dtype=np.uint8)
    n = 40
    j = (1 << n) - 1

    cols = []
    for c in range(n):
        m = 0
        for r in np.flatnonzero(Astar[:, c]):
            m |= 1 << int(r)
        cols.append(m)
    edges = [(a, b) for a in range(n) for b in range(a + 1, n) if Astar[a, b]]
    B9 = rank_basis_int([cols[a] ^ cols[b] for a, b in edges])
    V9 = set(span(B9))
    assert len(B9) == 9 and len(V9) == 512 and j in V9
    reps = {min(x, x ^ j) for x in V9}

    def rep(x):
        return min(int(x), int(x) ^ j)

    def q(x):
        return (rep(x).bit_count() // 4) & 1

    singular = sorted(x for x in reps if x and q(x) == 0)
    anisotropic = sorted(x for x in reps if x and q(x) == 1)
    assert (len(singular), len(anisotropic)) == (135, 120)

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
        assert rep(s ^ t) == x
        return tuple(sorted((s, t, x)))

    fibers = defaultdict(list)
    for ap in apartments:
        fibers[apartment_line(ap)].append(ap)
    selected = sorted(fibers)
    assert len(selected) == 270
    sidx = {x: i for i, x in enumerate(singular)}
    lsel = {L: i for i, L in enumerate(selected)}

    N = np.zeros((135, 270), dtype=np.int64)
    for c, L in enumerate(selected):
        for x in L:
            N[sidx[x], c] = 1

    rows, rank = independent_rows_mod(N)
    assert rank == 120
    B = N[rows] % P
    pivcols, crank = independent_rows_mod(B.T)
    assert crank == 120
    BCinv = inv_mod(B[:, pivcols])

    cand = [build_line_perm(transvection_matrix(v), pts, pidx, lines, lidx) for v in pts]
    gens = []
    G = {tuple(range(40))}
    for g in cand:
        if g in G:
            continue
        gens.append(g)
        G = perm_group(gens)
        if len(G) == 25920:
            break
    assert len(gens) == 5 and len(G) == 25920

    def act_v(x, g):
        return rep(pmask(rep(x), g))

    def act_line(L, g):
        return tuple(sorted(act_v(x, g) for x in L))

    def line_perm(g):
        return np.asarray([lsel[act_line(L, g)] for L in selected], dtype=int)

    def rowspace_trace(g):
        p270 = line_perm(g)
        Bp = np.zeros_like(B)
        Bp[:, p270] = B
        C = (Bp[:, pivcols] @ BCinv) % P
        tr = int(np.trace(C) % P)
        if tr > P // 2:
            tr -= P
        # The characteristic-zero trace is an integer with |tr| <= dim=120,
        # so reduction modulo this prime determines it uniquely.
        assert abs(tr) <= 120
        return tr

    def anisotropic_trace(g):
        return sum(act_v(x, g) == x for x in anisotropic)

    # The individual chosen generators all agree at trace 3, which is why a
    # shallow check is misleading.
    generator_pairs = [(rowspace_trace(g), anisotropic_trace(g)) for g in gens]
    assert generator_pairs == [(3, 3)] * 5

    # The short word g0*g4 is already decisive.
    witness = compose(gens[4], gens[0])
    assert perm_order(witness) == 6
    row_tr = rowspace_trace(witness)
    ani_tr = anisotropic_trace(witness)
    assert (row_tr, ani_tr) == (-1, 3)

    out = {
        "pass": 4591,
        "modules": {
            "selected_line_incidence_rowspace_dimension_Q": 120,
            "anisotropic_permutation_degree": 120,
        },
        "shallow_generator_trace_pairs": generator_pairs,
        "separating_element": {
            "word": "g4*g0 in the deterministic five-transvection generating set",
            "order": 6,
            "selected_incidence_rowspace_character": row_tr,
            "anisotropic_permutation_character": ani_tr,
        },
        "theorem": "The 120-dimensional rational rowspace of the apartment-selected 135x270 incidence matrix is not isomorphic to the 120-point anisotropic permutation module of PSp(4,3).",
        "boundary": "This is a representation-theoretic non-identification. It does not preclude nonlinear correspondences, subquotient relations, or maps after changing groups/fields.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
