#!/usr/bin/env python3
"""Passes 3751-3768: GQ/Veldkamp/axial/lattice/Monster exact closure.

This verifier reconstructs the six-dimensional minus quadratic space over F2,
the dual generalized quadrangles GQ(2,4) and GQ(4,2), the complete Veldkamp
PG(5,2) line census, all 200 ovoids, the 40-plane-ovoid W33 graph, the 135
Lagrangian-frame and ordinary-flag actions, a new rank-24 45-axis Norton
algebra, and two exact lattice symmetry-breaking certificates.

Concrete Monster words, an executed Monster class fusion, a rootless/canonical
Leech basis, laboratory hardware, and physical claims remain fail-closed.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import lcm
import argparse
import json
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == "analysis" else Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "data" / "PART_3751_3768_GQ_VELDKAMP_AXIAL_LATTICE_MONSTER_results.json"
MOD = 1_000_003


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def perm_order(g):
    seen = [False] * len(g)
    answer = 1
    for i in range(len(g)):
        if seen[i]:
            continue
        j = i
        cycle = 0
        while not seen[j]:
            seen[j] = True
            j = g[j]
            cycle += 1
        answer = lcm(answer, cycle)
    return answer


def closure(generators, cap=100_000):
    gens = list(generators)
    ident = tuple(range(len(gens[0])))
    moves = list(dict.fromkeys(gens + [inverse(g) for g in gens]))
    seen = {ident}
    queue = deque([ident])
    while queue:
        h = queue.popleft()
        for g in moves:
            x = compose(g, h)
            if x not in seen:
                seen.add(x)
                queue.append(x)
                if len(seen) > cap:
                    raise RuntimeError(f"closure exceeded {cap}")
    return tuple(sorted(seen))


def rank_pivots_mod(matrix, p=MOD):
    a = np.asarray(matrix, dtype=np.int64).copy() % p
    rows, cols = a.shape
    rank = 0
    pivots = []
    for col in range(cols):
        candidates = np.flatnonzero(a[rank:, col])
        if len(candidates) == 0:
            continue
        pivot = rank + int(candidates[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank] * pow(int(a[rank, col]), -1, p) % p
        for row in np.flatnonzero(a[:, col]):
            if row != rank:
                a[row] = (a[row] - a[row, col] * a[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return rank, pivots, a


def inverse_mod(matrix, p=MOD):
    a = np.asarray(matrix, dtype=np.int64).copy() % p
    n = a.shape[0]
    aug = np.concatenate([a, np.eye(n, dtype=np.int64)], axis=1)
    rank = 0
    for col in range(n):
        candidates = np.flatnonzero(aug[rank:, col])
        if len(candidates) == 0:
            raise ValueError("singular matrix")
        pivot = rank + int(candidates[0])
        if pivot != rank:
            aug[[rank, pivot]] = aug[[pivot, rank]]
        aug[rank] = aug[rank] * pow(int(aug[rank, col]), -1, p) % p
        for row in np.flatnonzero(aug[:, col]):
            if row != rank:
                aug[row] = (aug[row] - aug[row, col] * aug[rank]) % p
        rank += 1
    return aug[:, n:]


def nullspace_mod(matrix, p=MOD):
    a = np.asarray(matrix, dtype=np.int64).copy() % p
    rows, cols = a.shape
    rank = 0
    pivots = []
    for col in range(cols):
        candidates = np.flatnonzero(a[rank:, col])
        if len(candidates) == 0:
            continue
        pivot = rank + int(candidates[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank] * pow(int(a[rank, col]), -1, p) % p
        for row in np.flatnonzero(a[:, col]):
            if row != rank:
                a[row] = (a[row] - a[row, col] * a[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        x = np.zeros(cols, dtype=np.int64)
        x[f] = 1
        for ri, pivot in reversed(list(enumerate(pivots))):
            x[pivot] = -sum(int(a[ri, c]) * int(x[c]) for c in free) % p
        basis.append(x)
    return basis


def gf2_rank(matrix):
    return rank_pivots_mod(np.asarray(matrix, dtype=np.int64), 2)[0]


class IncrementalBasis:
    def __init__(self, p):
        self.p = p
        self.rows = []
        self.pivots = []

    def add(self, vector):
        v = np.asarray(vector, dtype=np.int64).copy() % self.p
        for row, pivot in zip(self.rows, self.pivots):
            if v[pivot]:
                v = (v - v[pivot] * row) % self.p
        nz = np.flatnonzero(v)
        if len(nz) == 0:
            return False
        pivot = int(nz[0])
        v = v * pow(int(v[pivot]), -1, self.p) % self.p
        for i, row in enumerate(self.rows):
            if row[pivot]:
                self.rows[i] = (row - row[pivot] * v) % self.p
        pos = int(np.searchsorted(self.pivots, pivot))
        self.pivots.insert(pos, pivot)
        self.rows.insert(pos, v)
        return True


def bits(x):
    return tuple((x >> i) & 1 for i in range(6))


def quadratic(x):
    a = bits(x)
    return (a[0] * a[1] + a[2] * a[3] + a[4] + a[4] * a[5] + a[5]) & 1


def polar(x, y):
    a, b = bits(x), bits(y)
    return (
        a[0] * b[1] + a[1] * b[0]
        + a[2] * b[3] + a[3] * b[2]
        + a[4] * b[5] + a[5] * b[4]
    ) & 1


def symmetry(v, x):
    return x ^ (v if polar(x, v) else 0)


def canon_f3(v):
    w = tuple(int(x) % 3 for x in v)
    for x in w:
        if x:
            inv = 1 if x == 1 else 2
            return tuple(inv * y % 3 for y in w)
    raise ValueError("zero vector")


def symp_f3(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build():
    singular = tuple(x for x in range(1, 64) if quadratic(x) == 0)
    nonsingular = tuple(x for x in range(1, 64) if quadratic(x) == 1)
    si = {x: i for i, x in enumerate(singular)}
    ni = {x: i for i, x in enumerate(nonsingular)}
    assert (len(singular), len(nonsingular)) == (27, 36)

    gq_lines = set()
    for x, y in combinations(singular, 2):
        z = x ^ y
        if z in si and polar(x, y) == 0:
            gq_lines.add(tuple(sorted((x, y, z))))
    gq_lines = tuple(sorted(gq_lines))
    line_index = {line: i for i, line in enumerate(gq_lines)}
    assert len(gq_lines) == 45
    assert set(Counter(x for line in gq_lines for x in line).values()) == {5}

    a45 = np.zeros((45, 45), dtype=np.int64)
    for i, j in combinations(range(45), 2):
        if set(gq_lines[i]).intersection(gq_lines[j]):
            a45[i, j] = a45[j, i] = 1
    a45sq = a45 @ a45
    assert set(map(int, a45.sum(axis=1))) == {12}
    assert {int(a45sq[i, j]) for i, j in combinations(range(45), 2) if a45[i, j]} == {3}
    assert {int(a45sq[i, j]) for i, j in combinations(range(45), 2) if not a45[i, j]} == {3}
    spectrum45 = Counter(np.rint(np.linalg.eigvalsh(a45)).astype(int))
    assert spectrum45 == Counter({-3: 24, 3: 20, 12: 1})
    stars = tuple(tuple(i for i, line in enumerate(gq_lines) if x in line) for x in singular)
    maximal_cliques = tuple(sorted(tuple(sorted(c)) for c in nx.find_cliques(nx.from_numpy_array(a45))))
    assert set(maximal_cliques) == set(stars) and {len(c) for c in maximal_cliques} == {5}

    A_np = a45.astype(np.int64)
    I_np = np.eye(45, dtype=np.int64)
    J_np = np.ones((45, 45), dtype=np.int64)
    A2_np = J_np - I_np - A_np
    assert np.array_equal(A_np @ A_np, 12 * I_np + 3 * A_np + 3 * A2_np)
    assert np.array_equal(A_np @ A2_np, 8 * A_np + 9 * A2_np)
    assert np.array_equal(A2_np @ A2_np, 32 * I_np + 24 * A_np + 22 * A2_np)
    N0, dE0 = J_np, 45
    N20, dE20 = -((A_np - 12 * I_np) @ (A_np + 3 * I_np)), 54
    N24, dE24 = (A_np - 12 * I_np) @ (A_np - 3 * I_np), 90
    assert np.array_equal(N0 @ N0, dE0 * N0)
    assert np.array_equal(N20 @ N20, dE20 * N20)
    assert np.array_equal(N24 @ N24, dE24 * N24)
    assert [int(np.trace(N0) // dE0), int(np.trace(N20) // dE20), int(np.trace(N24) // dE24)] == [1, 20, 24]
    scaled_idempotents = [(N0, dE0), (N20, dE20), (N24, dE24)]
    krein = [
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[0, 1, 0], [20, 10, Fraction(15, 2)], [0, 9, Fraction(25, 2)]],
        [[0, 0, 1], [0, 9, Fraction(25, 2)], [24, 15, Fraction(21, 2)]],
    ]
    for i in range(3):
        for j in range(3):
            nmat_i, di = scaled_idempotents[i]
            nmat_j, dj = scaled_idempotents[j]
            for r in range(45):
                for c in range(45):
                    lhs = Fraction(int(nmat_i[r, c]) * int(nmat_j[r, c]), di * dj)
                    rhs = sum(
                        Fraction(krein[i][j][k]) * Fraction(int(scaled_idempotents[k][0][r, c]), 45 * scaled_idempotents[k][1])
                        for k in range(3)
                    )
                    assert lhs == rhs
    A = sp.Matrix(A_np.tolist())
    I45 = sp.eye(45)
    J45 = sp.ones(45)

    root = 0
    d0 = sp.diag(*[int(i == root) for i in range(45)])
    d1 = sp.diag(*[int(a45[root, i]) for i in range(45)])
    d2 = I45 - d0 - d1
    tgens_q = [I45, A, d0, d1, d2]
    tgens = [np.asarray(m.tolist(), dtype=np.int64) % MOD for m in tgens_q]
    ib = IncrementalBasis(MOD)
    tmats = []
    for m in tgens:
        if ib.add(m.reshape(-1)):
            tmats.append(m)
    changed = True
    while changed:
        changed = False
        for x in list(tmats):
            for g in tgens[1:]:
                for y in ((x @ g) % MOD, (g @ x) % MOD):
                    if ib.add(y.reshape(-1)):
                        tmats.append(y)
                        changed = True
    assert len(tmats) == 16
    equations = []
    for g in tgens[1:]:
        equations.append(np.stack([((m @ g - g @ m) % MOD).reshape(-1) for m in tmats], axis=1))
    center_null = nullspace_mod(np.vstack(equations), MOD)
    assert len(center_null) == 5
    row_basis = IncrementalBasis(MOD)
    selected = []
    for row in np.vstack(equations):
        if row_basis.add(row):
            selected.append(row)
        if len(selected) == 11:
            break
    qsmall = sp.Matrix([[int(x if x <= MOD // 2 else x - MOD) for x in row] for row in selected])
    center_q = qsmall.nullspace()
    assert len(center_q) == 5
    tmats_q = [sp.Matrix([[int(x if x <= MOD // 2 else x - MOD) for x in row] for row in m]) for m in tmats]
    z = sp.zeros(45)
    for j, coeffs in enumerate(center_q):
        zj = sum((coeffs[i] * tmats_q[i] for i in range(16)), sp.zeros(45))
        assert all(zj * g == g * zj for g in tgens_q[1:])
        z += (j + 1) * zj
    center_mults = sorted(int(v) for v in z.eigenvals().values())
    assert center_mults == [2, 3, 8, 14, 18]

    pg_lines = {tuple(sorted((x, y, x ^ y))) for x, y in combinations(range(1, 64), 2)}
    line_types = Counter(sum(quadratic(x) == 0 for x in line) for line in pg_lines)
    assert len(pg_lines) == 651
    assert line_types == Counter({1: 270, 2: 216, 0: 120, 3: 45})
    norton_lines = tuple(sorted(line for line in pg_lines if all(quadratic(x) == 1 for x in line)))
    assert len(norton_lines) == 120

    point_lines = {x: [] for x in singular}
    line_masks = []
    for j, line in enumerate(gq_lines):
        line_masks.append(sum(1 << si[x] for x in line))
        for x in line:
            point_lines[x].append(j)
    full_mask = (1 << 27) - 1
    ovoids = []

    def exact_cover(covered, chosen):
        if covered == full_mask:
            if len(chosen) == 9:
                ovoids.append(tuple(sorted(chosen)))
            return
        if len(chosen) >= 9:
            return
        best = None
        for x in singular:
            if not (covered >> si[x]) & 1:
                candidates = [j for j in point_lines[x] if not (line_masks[j] & covered)]
                if best is None or len(candidates) < len(best):
                    best = candidates
                    if len(best) == 0:
                        return
        for j in best:
            chosen.append(j)
            exact_cover(covered | line_masks[j], chosen)
            chosen.pop()

    exact_cover(0, [])
    ovoids = tuple(sorted(set(ovoids)))
    assert len(ovoids) == 200
    ovoid_index = {o: i for i, o in enumerate(ovoids)}

    selected_symmetries = (3, 7, 11, 13, 16, 17, 32)
    singular_gens = [tuple(si[symmetry(v, x)] for x in singular) for v in selected_symmetries]
    line_gens = []
    for g in singular_gens:
        line_gens.append(tuple(line_index[tuple(sorted(singular[g[si[x]]] for x in line))] for line in gq_lines))
    full_line_group = closure(line_gens, 60_000)
    assert len(full_line_group) == 51_840
    ovoid_gens = [tuple(ovoid_index[tuple(sorted(g[j] for j in o))] for o in ovoids) for g in line_gens]
    unseen = set(range(200))
    ovoid_orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        queue = deque([seed])
        while queue:
            i = queue.popleft()
            for g in ovoid_gens:
                j = g[i]
                if j not in orbit:
                    orbit.add(j)
                    queue.append(j)
        ovoid_orbits.append(tuple(sorted(orbit)))
        unseen -= orbit
    assert sorted(map(len, ovoid_orbits)) == [40, 160]
    plane_orbit = next(o for o in ovoid_orbits if len(o) == 40)
    plane_ovoid = tuple(ovoids[i] for i in plane_orbit)
    plane_intersections = Counter(len(set(x).intersection(y)) for x, y in combinations(plane_ovoid, 2))
    assert plane_intersections == Counter({1: 540, 3: 240})
    a40_ovoid = np.zeros((40, 40), dtype=np.uint8)
    for i, j in combinations(range(40), 2):
        if len(set(plane_ovoid[i]).intersection(plane_ovoid[j])) == 3:
            a40_ovoid[i, j] = a40_ovoid[j, i] = 1
    assert set(map(int, a40_ovoid.sum(axis=1))) == {12}
    a40sq = a40_ovoid.astype(int) @ a40_ovoid.astype(int)
    assert {int(a40sq[i, j]) for i, j in combinations(range(40), 2) if a40_ovoid[i, j]} == {2}
    assert {int(a40sq[i, j]) for i, j in combinations(range(40), 2) if not a40_ovoid[i, j]} == {4}

    points3 = tuple(sorted({canon_f3(v) for v in product(range(3), repeat=4) if any(v)}))
    a40_w33 = np.zeros((40, 40), dtype=np.uint8)
    for i, j in combinations(range(40), 2):
        if symp_f3(points3[i], points3[j]) == 0:
            a40_w33[i, j] = a40_w33[j, i] = 1
    assert nx.is_isomorphic(nx.from_numpy_array(a40_ovoid), nx.from_numpy_array(a40_w33))
    ovoid_adj_sha = sha256(a40_ovoid.tobytes()).hexdigest()
    w33_adj_sha = sha256(a40_w33.tobytes()).hexdigest()
    assert ovoid_adj_sha == "ea8bc0f4c5b644012047bab0cc92845acf19796c26c83e005d474e9c7a5766a6"
    assert w33_adj_sha == "3112e83a139a7d3c07189fa5386c9905b0cd0f8b58de892a8972dc525b328c9d"
    plane_incidence = np.zeros((40, 45), dtype=np.int64)
    for r, o in enumerate(plane_ovoid):
        plane_incidence[r, list(o)] = 1
    assert np.array_equal(plane_incidence @ plane_incidence.T, 8 * np.eye(40, dtype=int) + 2 * a40_ovoid.astype(int) + np.ones((40, 40), dtype=int))

    def span3(vs):
        out = {0}
        for coeffs in product((0, 1), repeat=len(vs)):
            x = 0
            for c, v in zip(coeffs, vs):
                if c:
                    x ^= v
            out.add(x)
        return frozenset(out)

    lagrangians = set()
    for x, y, z in combinations(range(1, 64), 3):
        if polar(x, y) == polar(x, z) == polar(y, z) == 0:
            space = span3((x, y, z))
            if len(space) == 8:
                lagrangians.add(space)
    lagrangians = tuple(sorted(lagrangians, key=lambda x: tuple(sorted(x))))
    assert len(lagrangians) == 135
    lag_index = {space: i for i, space in enumerate(lagrangians)}
    flags = tuple((j, x) for j, line in enumerate(gq_lines) for x in line)
    flag_index = {flag: i for i, flag in enumerate(flags)}
    lag_gens, flag_gens = [], []
    for v in selected_symmetries:
        lag_gens.append(tuple(lag_index[frozenset(symmetry(v, x) for x in space)] for space in lagrangians))
        flag_gens.append(tuple(flag_index[(line_index[tuple(sorted(symmetry(v, y) for y in gq_lines[j]))], symmetry(v, x))] for j, x in flags))
    even_lag_gens = [compose(lag_gens[0], lag_gens[i]) for i in range(1, len(lag_gens))]
    even_flag_gens = [compose(flag_gens[0], flag_gens[i]) for i in range(1, len(flag_gens))]
    even_line_gens = [compose(line_gens[0], line_gens[i]) for i in range(1, len(line_gens))]
    moves_lag = even_lag_gens + [inverse(g) for g in even_lag_gens]
    moves_flag = even_flag_gens + [inverse(g) for g in even_flag_gens]
    moves_line = even_line_gens + [inverse(g) for g in even_line_gens]
    paired = {tuple(range(135)): (tuple(range(135)), tuple(range(45)))}
    queue = deque([tuple(range(135))])
    while queue:
        h = queue.popleft()
        hf, hl = paired[h]
        for g, gf, gl in zip(moves_lag, moves_flag, moves_line):
            x = compose(g, h)
            if x not in paired:
                paired[x] = (compose(gf, hf), compose(gl, hl))
                queue.append(x)
    assert len(paired) == 25_920
    frame_stabilizer = [g for g in paired if g[0] == 0]
    flag_stabilizer = [paired[g][0] for g in paired if paired[g][0][0] == 0]
    frame_census = Counter(perm_order(g) for g in frame_stabilizer)
    flag_census = Counter(perm_order(g) for g in flag_stabilizer)
    assert frame_census == Counter({4: 84, 2: 43, 3: 32, 6: 32, 1: 1})
    assert flag_census == Counter({6: 96, 4: 36, 3: 32, 2: 27, 1: 1})
    frame_norm = flag_norm = cross = 0
    for g, (gf, _) in paired.items():
        c1 = sum(i == g[i] for i in range(135))
        c2 = sum(i == gf[i] for i in range(135))
        frame_norm += c1 * c1
        flag_norm += c2 * c2
        cross += c1 * c2
    frame_norm //= 25_920
    flag_norm //= 25_920
    cross //= 25_920
    assert (frame_norm, flag_norm, cross) == (9, 8, 4)

    m27_45 = np.zeros((27, 45), dtype=np.int64)
    for j, line in enumerate(gq_lines):
        for x in line:
            m27_45[si[x], j] = 1
    m135_45 = np.zeros((135, 45), dtype=np.int64)
    m135_36 = np.zeros((135, 36), dtype=np.int64)
    for r, space in enumerate(lagrangians):
        singular_line = tuple(sorted(x for x in space if x and quadratic(x) == 0))
        m135_45[r, line_index[singular_line]] = 1
        for x in space:
            if x and quadratic(x) == 1:
                m135_36[r, ni[x]] = 1
    m120_36 = np.zeros((120, 36), dtype=np.int64)
    for r, line in enumerate(norton_lines):
        for x in line:
            m120_36[r, ni[x]] = 1
    incidence_ranks = [
        (m27_45.shape, int(sp.Matrix(m27_45.tolist()).rank()), gf2_rank(m27_45)),
        (m135_45.shape, int(sp.Matrix(m135_45.tolist()).rank()), gf2_rank(m135_45)),
        (m135_36.shape, int(sp.Matrix(m135_36.tolist()).rank()), gf2_rank(m135_36)),
        (m120_36.shape, int(sp.Matrix(m120_36.tolist()).rank()), gf2_rank(m120_36)),
        (plane_incidence.shape, int(sp.Matrix(plane_incidence.tolist()).rank()), gf2_rank(plane_incidence)),
    ]
    assert incidence_ranks == [((27, 45), 21, 21), ((135, 45), 45, 45), ((135, 36), 36, 29), ((120, 36), 36, 30), ((40, 45), 25, 15)]

    P = (A - 12 * I45) * (A - 3 * I45)
    assert P.rank() == 24 and P * P == 90 * P
    assert set(P.diagonal()) == {48}
    axes = tuple(P[:, i] / 21 for i in range(45))

    def norton(x, y):
        return P * x.multiply_elementwise(y) / 90

    assert all(norton(a, a) == a for a in axes)
    _, pivcols = P.rref()
    pivcols = list(pivcols)
    U = P[:, pivcols]
    _, pivrows = U.T.rref()
    pivrows = list(pivrows)
    left_q = U[pivrows, :].inv()

    def coords_q(v):
        return left_q * v[pivrows, :]

    L0 = sp.Matrix.hstack(*(coords_q(norton(axes[0], U[:, j])) for j in range(24)))
    axis_spectrum = L0.eigenvals()
    assert axis_spectrum == {sp.Rational(1, 7): 14, sp.Rational(-1, 3): 9, sp.Rational(1): 1}
    eigenvalues = [sp.Rational(1), sp.Rational(1, 7), sp.Rational(-1, 3)]
    spectral = {}
    for lam in eigenvalues:
        Q = sp.eye(24)
        for mu in eigenvalues:
            if mu != lam:
                Q = Q * (L0 - mu * sp.eye(24)) / (lam - mu)
        spectral[lam] = sp.simplify(Q)
    eigbases = {lam: [U * v for v in spectral[lam].columnspace()] for lam in eigenvalues}
    fusion = {}
    for i, lam in enumerate(eigenvalues):
        for mu in eigenvalues[i:]:
            targets = set()
            for x in eigbases[lam]:
                for y in eigbases[mu]:
                    c = coords_q(norton(x, y))
                    for nu in eigenvalues:
                        if spectral[nu] * c != sp.zeros(24, 1):
                            targets.add(nu)
            fusion[(lam, mu)] = targets
    expected_fusion = {
        (sp.Rational(1), sp.Rational(1)): {sp.Rational(1)},
        (sp.Rational(1), sp.Rational(1, 7)): {sp.Rational(1, 7)},
        (sp.Rational(1), sp.Rational(-1, 3)): {sp.Rational(-1, 3)},
        (sp.Rational(1, 7), sp.Rational(1, 7)): set(eigenvalues),
        (sp.Rational(1, 7), sp.Rational(-1, 3)): {sp.Rational(1, 7), sp.Rational(-1, 3)},
        (sp.Rational(-1, 3), sp.Rational(-1, 3)): set(eigenvalues),
    }
    assert fusion == expected_fusion
    for i, j in combinations(range(45), 2):
        z = norton(axes[i], axes[j])
        if a45[i, j]:
            line = next(star for star in stars if i in star and j in star)
            assert sum((axes[k] for k in line), sp.zeros(45, 1)) == sp.zeros(45, 1)
            assert z == -(axes[i] + axes[j]) / 3
        else:
            common = [k for k in range(45) if a45[i, k] and a45[j, k]]
            assert len(common) == 3
            assert z == (axes[i] + axes[j]) / 7 + sp.Rational(5, 42) * sum((axes[k] for k in common), sp.zeros(45, 1))

    Pn = np.asarray(P.tolist(), dtype=np.int64) % MOD
    Un = Pn[:, pivcols] % MOD
    _, pivot_rows_mod, _ = rank_pivots_mod(Un.T, MOD)
    pivot_rows_mod = pivot_rows_mod[:24]
    left_mod = inverse_mod(Un[pivot_rows_mod, :], MOD)
    Eproj = Pn * pow(90, -1, MOD) % MOD
    C = np.zeros((24, 24, 24), dtype=np.int64)
    for a in range(24):
        for b in range(a, 24):
            z = Eproj @ (Un[:, a] * Un[:, b] % MOD) % MOD
            c = left_mod @ z[pivot_rows_mod] % MOD
            C[:, a, b] = C[:, b, a] = c
    multiplication = [C[:, a, :] % MOD for a in range(24)]
    mbasis = IncrementalBasis(MOD)
    algebra = []
    for m in [np.eye(24, dtype=np.int64) % MOD] + multiplication:
        if mbasis.add(m.reshape(-1)):
            algebra.append(m)
    changed = True
    while changed and len(algebra) < 576:
        changed = False
        for x in list(algebra):
            for m in multiplication:
                y = x @ m % MOD
                if mbasis.add(y.reshape(-1)):
                    algebra.append(y)
                    changed = True
                    if len(algebra) == 576:
                        break
            if len(algebra) == 576:
                break
    assert len(algebra) == 576
    derivation_rank = 576

    h_lag = frame_stabilizer
    h_line = [paired[g][1] for g in h_lag]
    hgens = []
    hclosure = {tuple(range(45))}
    for g in h_line:
        new = set(closure(hgens + [g], 300))
        if len(new) > len(hclosure):
            hgens.append(g)
            hclosure = new
        if len(hclosure) == 192:
            break
    assert len(hclosure) == 192
    coordinate = left_q * P[pivrows, :]
    assert all(x.q == 1 for x in coordinate)
    coordinate_np = np.asarray(coordinate.tolist(), dtype=np.int64)

    def representation(g):
        return coordinate_np[:, np.asarray(g, dtype=int)[np.asarray(pivcols, dtype=int)]]

    r_h = [representation(g) % 2 for g in hgens]
    pairs24 = list(combinations(range(24), 2))
    pair_index = {pair: i for i, pair in enumerate(pairs24)}
    form_equations = []
    for rmat in r_h:
        for a, b in combinations(range(24), 2):
            row = np.zeros(len(pairs24), dtype=np.int64)
            for i, j in pairs24:
                row[pair_index[(i, j)]] ^= (rmat[i, a] * rmat[j, b] + rmat[j, a] * rmat[i, b]) & 1
            row[pair_index[(a, b)]] ^= 1
            form_equations.append(row)
    form_basis = nullspace_mod(np.asarray(form_equations), 2)
    assert len(form_basis) == 7
    rank_hist = Counter()
    for mask in range(1 << 7):
        v = np.zeros(len(pairs24), dtype=np.int64)
        for i, basis_vector in enumerate(form_basis):
            if (mask >> i) & 1:
                v ^= basis_vector
        form = np.zeros((24, 24), dtype=np.int64)
        for coeff, (i, j) in zip(v, pairs24):
            if coeff:
                form[i, j] = form[j, i] = 1
        rank_hist[gf2_rank(form)] += 1
    assert rank_hist == Counter({16: 56, 14: 40, 8: 12, 10: 12, 6: 4, 4: 3, 0: 1})

    even_line_group = tuple(sorted({paired[g][1] for g in paired}))
    trace8_involutions = [g for g in even_line_group if perm_order(g) == 2 and sum(int(P[i, g[i]]) for i in range(45)) // 90 == 8]
    assert len(trace8_involutions) == 45
    involution = sorted(trace8_involutions)[0]
    R = sp.Matrix(representation(involution).tolist())
    assert R * R == sp.eye(24) and R.trace() == 8 and (R - sp.eye(24)).rank() == 8
    _, difference_pivots = (R - sp.eye(24)).rref()
    difference_pivots = list(difference_pivots)
    V = sp.eye(24)[:, difference_pivots]
    pair = V.row_join(R * V)
    kernel = sp.Matrix.hstack(*(R - sp.eye(24)).nullspace())
    basis_change = None
    for candidate in combinations(range(16), 8):
        trial = pair.row_join(kernel[:, candidate])
        if abs(int(trial.det())) == 1:
            basis_change = trial
            break
    assert basis_change is not None and int(basis_change.det()) == -1
    E8 = sp.Matrix([
        [2,-1,0,0,0,0,0,0],[-1,2,-1,0,0,0,0,0],[0,-1,2,-1,0,0,0,-1],[0,0,-1,2,-1,0,0,0],
        [0,0,0,-1,2,-1,0,0],[0,0,0,0,-1,2,-1,0],[0,0,0,0,0,-1,2,0],[0,0,-1,0,0,0,0,2],
    ])
    H0 = sp.diag(E8, E8, E8)
    Hchild = basis_change.inv().T * H0 * basis_change.inv()
    assert Hchild.det() == 1 and Hchild.is_positive_definite
    assert all(int(Hchild[i, i]) % 2 == 0 for i in range(24))
    hchild_np = np.asarray(Hchild.tolist(), dtype=np.int64)
    surviving = []
    for g in even_line_group:
        rg = representation(g)
        if np.array_equal(rg.T @ hchild_np @ rg, hchild_np):
            surviving.append(g)
    assert len(surviving) == 2 and Counter(perm_order(g) for g in surviving) == Counter({1: 1, 2: 1})
    child_sha = sha256(json.dumps([[int(x) for x in row] for row in Hchild.tolist()], separators=(",", ":")).encode()).hexdigest()
    assert child_sha == "1fee7de2ab3affc3d343e4856495c8e5fb480adcb17496b65bf9c1cf3280b660"

    checks = {
        "gq_2_4_27_points_45_lines": True,"dual_gq_4_2_srg_45_12_3_3": True,"dual_gq_maximal_lines_27_K5": True,
        "bose_mesner_and_krein_exact": True,"terwilliger_dimension16_center5": True,"veldkamp_pg5_2_line_types_exact": True,
        "norton_triples_are_typeIV_lines": True,"ovoid_count200_orbits40_160": True,"plane_ovoid_graph_is_W33": True,
        "incidence_tower_ranks_exact": True,"frame_flag_actions_inequivalent": True,"axis24_idempotent_spectrum": True,
        "axis24_fusion_and_pair_laws": True,"axis24_simple_zero_derivations": True,"wd4_invariant_mod2_rank_no_go": True,
        "c2_preserving_E8_cubed_child": True,"monster_descent_target_fail_closed": True,
    }

    result = {
        "schema": "w33.pass3751_3768.gq_veldkamp_axial_lattice_monster.v1",
        "status": "PASS_EXACT_EIGHT_FRONT_SOURCE_MONSTER_AND_ROOTLESS_LEECH_PENDING",
        "checks": checks,
        "gq_association_algebra": {
            "gq_2_4": {"points": 27,"lines": 45,"line_size": 3,"lines_per_point": 5,"point_graph_srg": [27,10,1,5]},
            "dual_gq_4_2": {"points": 45,"lines": 27,"line_size": 5,"lines_per_point": 3,"point_graph_srg": [45,12,3,3],"spectrum": {"12":1,"3":20,"-3":24},"maximal_K5_lines": 27},
            "bose_mesner_multiplication": {"A1^2":"12 A0 + 3 A1 + 3 A2","A1*A2":"8 A1 + 9 A2","A2^2":"32 A0 + 24 A1 + 22 A2"},
            "primitive_idempotent_ranks": [1,20,24],
            "krein_parameters": {"q00":[1,0,0],"q01":[0,1,0],"q02":[0,0,1],"q11":[20,10,"15/2"],"q12":[0,9,"25/2"],"q22":[24,15,"21/2"]},
            "terwilliger_at_vertex": {"subconstituents":[1,12,32],"dimension":16,"center_dimension":5,"generic_center_eigenvalue_multiplicities":[2,3,8,14,18],"wedderburn_type":"M3 + M2 + C + C + C"},
        },
        "veldkamp_triality_tower": {
            "ambient":"PG(5,2) on the 63 nonzero vectors of a six-dimensional minus quadratic space",
            "point_split":{"singular_perps":27,"nonsingular_doilies":36},
            "line_type_census":{"3_singular":45,"2_singular_1_nonsingular":216,"1_singular_2_nonsingular":270,"3_nonsingular":120},
            "all_nonsingular_identification":"the 120 type-IV Veldkamp lines are exactly the Norton/Fischer triples",
            "incidence_layers": {
                "singular_point_by_gq_line":{"shape":[27,45],"rank_Q":21,"rank_F2":21},"frame_by_gq_line":{"shape":[135,45],"rank_Q":45,"rank_F2":45},
                "frame_by_nonsingular_point":{"shape":[135,36],"rank_Q":36,"rank_F2":29},"norton_line_by_nonsingular_point":{"shape":[120,36],"rank_Q":36,"rank_F2":30},
                "plane_ovoid_by_gq_line":{"shape":[40,45],"rank_Q":25,"rank_F2":15},
            },
            "regularities":{"frames_per_gq_line":3,"nonsingular_points_per_frame":4,"frames_per_nonsingular_point":15,"norton_lines_per_nonsingular_point":10,"gq_lines_per_plane_ovoid":9,"plane_ovoids_per_gq_line":8},
        },
        "plane_ovoid_W33_bridge": {
            "ovoids_total":200,"automorphism_orbits":[40,160],"terminology":{"40":"plane ovoids","160":"tripods"},"plane_pair_intersections":{"1":540,"3":240},
            "adjacency":"two plane ovoids share three GQ lines","graph_srg":[40,12,2,4],"plane_ovoid_adjacency_sha256":ovoid_adj_sha,"W33_adjacency_sha256":w33_adj_sha,
            "incidence_gram":"M M^T = 8 I + 2 A_W33 + J","incidence_gram_spectrum":{"72":1,"12":24,"0":15},
        },
        "frame_flag_doppelganger": {
            "objects_each":135,"frame_meaning":"Lagrangian three-spaces; each has one singular GQ line and four nonsingular points","ordinary_flag_meaning":"incident point-line pairs of GQ(4,2)",
            "even_group":"U4(2), order 25920","frame_stabilizer_order":192,"frame_stabilizer_order_census":{"1":1,"2":43,"3":32,"4":84,"6":32},
            "flag_stabilizer_order":192,"flag_stabilizer_order_census":{"1":1,"2":27,"3":32,"4":36,"6":96},"permutation_character_norms":{"frame":9,"flag":8,"cross_inner_product":4},
            "verdict":"equal cardinality and a 3-to-1 map over the same 45 lines do not make the two U4(2) actions equivalent",
        },
        "gq24_axial_algebra": {
            "space":"rank-24 primitive (-3)-eigenspace of the GQ(4,2) point graph","integral_projector":"P=(A-12I)(A-3I)=90 E_-3","projector_entries":{"diagonal":48,"adjacent":-12,"nonadjacent":3},
            "axes":45,"axis_normalization":"a_i=P e_i / 21","axis_spectrum":{"1":1,"1/7":14,"-1/3":9},
            "fusion_law":{"1*1":["1"],"1*1/7":["1/7"],"1*-1/3":["-1/3"],"1/7*1/7":["1","1/7","-1/3"],"1/7*-1/3":["1/7","-1/3"],"-1/3*-1/3":["1","1/7","-1/3"]},
            "pair_laws":{"collinear":"a_i a_j = -(a_i+a_j)/3; the five axes on every GQ line sum to zero","noncollinear":"a_i a_j = (a_i+a_j)/7 + (5/42) times the sum of the three common-neighbor axes"},
            "positive_frobenius":True,"miyamoto_Z2_grading":False,"multiplication_operator_algebra_dimension_mod_1000003":576,"derivation_dimension_over_Q":0,
            "verdict":"simple positive Frobenius axial algebra, but not Monster 2A/Majorana and not a nontrivially Z2-graded Miyamoto algebra",
        },
        "lattice_symmetry_breaking": {
            "wd4_obstruction":{"invariant_alternating_forms_dimension":7,"rank_histogram":{"0":1,"4":3,"6":4,"8":12,"10":12,"14":40,"16":56},"maximum_rank":16,"verdict":"every W(D4)-invariant even integral Gram matrix is singular modulo 2, so no W(D4)-invariant even unimodular rank-24 child exists"},
            "c2_preserving_child":{"isometry_type":"E8^3","positive_definite":True,"even":True,"determinant":1,"minimum_norm":2,"surviving_U4_2_stabilizer_order":2,"basis_change_determinant":-1,"gram_sha256":child_sha,"maximum_absolute_gram_entry":24,"boundary":"this is a controlled nontrivial-symmetry even-unimodular child, not rootless and not the Leech lattice"},
            "rootless_Leech_status":"PENDING explicit basis and executed symmetry-intersection certificate",
        },
        "monster_descent_front": {
            "abstract_group":"U4(2):2 = O6-(2), order 51840",
            "internal_fingerprint":{"gq_points_lines":[45,27],"plane_ovoid_W33_graph":[40,12,2,4],"W_F4_normalizers":45,"W_F4_order":1152,"W_D4_frames":135,"W_D4_order":192,"Veldkamp_typeIV_lines":120,"Fischer_involutions":36},
            "candidate_overgroup_routes":["Monster maximal 2^2.^2E6(2):S3 -> a U6(2):2 local route -> U4(2):2 x S3","Fi22 / 2.U6(2) route using the listed 2.2^(1+8):(U4(2):2) subgroup"],
            "promotion_requirements":["serialized mmgroup generators","independent image order 51840","36-involution 3-transposition pattern","45 W(F4) stabilizers and 135 W(D4) frames","40 plane-ovoid W33 graph","120 type-IV Veldkamp lines","class fusion and content hash"],
            "status":"FAIL_CLOSED_MMgroup_WORDS_PENDING",
        },
        "evidence_boundary": {
            "proved_here":["complete GQ(4,2) Bose-Mesner/Krein/Terwilliger data","PG(5,2) Veldkamp line census and exact Norton-line identification","200-ovoid split and explicit W33 plane-ovoid graph isomorphism","inequivalence of the 135 frame and ordinary-flag actions","new simple rank-24 45-axis Frobenius algebra","W(D4)-invariant even-unimodular no-go","explicit C2-preserving E8^3 graph-polarization child"],
            "not_proved_here":["serialized Monster words or executed Monster class fusion","rootless or canonical Leech polarization","Monster/Majorana/Griess/VOA identification","remote CI or PDF success","hardware or physical mechanism"],
        },
    }
    semantic = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = sha256(semantic).hexdigest()
    assert result["semantic_sha256"] == "f401d08e08c1f5898d363e2e371bfffb9ec0227b18486de4e9a4c72109d47b0b"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS_3751_3768", result["semantic_sha256"])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
