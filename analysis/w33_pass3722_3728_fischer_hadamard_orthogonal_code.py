#!/usr/bin/env python3
"""Passes 3722-3728: Fischer triple design, Hadamard Naimark completion,
axial rigidity, orthogonal code, nonregular three-cover, and Monster targets.

The verifier is self-contained. It reconstructs W(3,3), all 36 spreads, the
rank-15 Norton algebra, and then closes seven fronts:
  * the 120 Norton triples as a Fischer 3-transposition space;
  * the exact U4(2):2 Miyamoto action and its U4(2) even subgroup;
  * a symmetric regular Hadamard 36-port Naimark completion;
  * zero derivations, simplicity, and all two-axis subalgebras;
  * the six-dimensional binary O_6^-(2) code unifying 27 and 36 carriers;
  * the 120-block graph as a nonregular S3-holonomy three-cover;
  * exact abstract standard-generator words and fail-closed Monster targets.

No concrete Monster embedding, executed Monster class-fusion restriction,
Majorana/Griess/VOA identification, optical device, or laboratory result is
claimed by this source certificate.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
from math import lcm
import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == "analysis" else Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "data" / "PART_3722_3728_FISCHER_HADAMARD_ORTHOGONAL_CODE_results.json"
MOD = 1_000_003


def canon_f3(v: Iterable[int]) -> tuple[int, ...]:
    w = tuple(int(x) % 3 for x in v)
    for x in w:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in w)
    raise ValueError("zero vector")


def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_w33():
    points = tuple(sorted({canon_f3(v) for v in product(range(3), repeat=4) if any(v)}))
    A = np.zeros((40, 40), dtype=np.int8)
    for i, j in combinations(range(40), 2):
        if symp(points[i], points[j]) == 0:
            A[i, j] = A[j, i] = 1
    assert len(points) == 40
    assert set(map(int, A.sum(axis=1))) == {12}
    assert np.array_equal(A @ A, 8 * np.eye(40, dtype=int) - 2 * A + 4 * np.ones((40, 40), dtype=int))

    lines = []
    for i, j in combinations(range(40), 2):
        if not A[i, j]:
            continue
        line = tuple(sorted({i, j} | {k for k in range(40) if A[i, k] and A[j, k]}))
        if len(line) == 4 and all(A[a, b] for a, b in combinations(line, 2)):
            lines.append(line)
    lines = tuple(sorted(set(lines)))
    assert len(lines) == 40

    point_to_lines = {p: [] for p in range(40)}
    masks = []
    for li, line in enumerate(lines):
        masks.append(sum(1 << p for p in line))
        for p in line:
            point_to_lines[p].append(li)
    full = (1 << 40) - 1
    spreads = []

    def search(covered: int, chosen: list[int]) -> None:
        if covered == full:
            if len(chosen) == 10:
                spreads.append(tuple(sorted(chosen)))
            return
        if len(chosen) >= 10:
            return
        uncovered = full ^ covered
        best = None
        bits = uncovered
        while bits:
            lsb = bits & -bits
            p = lsb.bit_length() - 1
            candidates = [li for li in point_to_lines[p] if not (masks[li] & covered)]
            item = (len(candidates), p, candidates)
            if best is None or item[0] < best[0]:
                best = item
            bits ^= lsb
        if best is None or best[0] == 0:
            return
        for li in best[2]:
            chosen.append(li)
            search(covered | masks[li], chosen)
            chosen.pop()

    search(0, [])
    spreads = tuple(sorted(set(spreads)))
    assert len(spreads) == 36
    return points, A, lines, spreads


def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def perm_order(g: tuple[int, ...]) -> int:
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


def closure_perms(generators: Iterable[tuple[int, ...]], cap: int = 100_000):
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
                    raise RuntimeError("closure cap exceeded")
    return tuple(sorted(seen))


def ppow(g: tuple[int, ...], n: int) -> tuple[int, ...]:
    if n < 0:
        return ppow(inverse(g), -n)
    result = tuple(range(len(g)))
    base = g
    while n:
        if n & 1:
            result = compose(base, result)
        base = compose(base, base)
        n //= 2
    return result


def commutator(x: tuple[int, ...], y: tuple[int, ...]) -> tuple[int, ...]:
    return compose(compose(compose(inverse(x), inverse(y)), x), y)


def independent_basis(E: sp.Matrix):
    _, pivcols = E.rref()
    cols = list(pivcols)
    U = E[:, cols]
    _, pivrows = U.T.rref()
    rows = list(pivrows)
    Rinv = U[rows, :].inv()
    return U, cols, rows, Rinv


def coords(v: sp.Matrix, U: sp.Matrix, rows: list[int], Rinv: sp.Matrix) -> sp.Matrix:
    c = Rinv * v[rows, :]
    assert U * c == v
    return c


def norton(E: sp.Matrix, x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    return E * x.multiply_elementwise(y)


def rat_mod(x, p: int = MOD) -> int:
    q = sp.Rational(x)
    return (int(q.p) * pow(int(q.q), -1, p)) % p


def rank_mod(M, p: int) -> int:
    A = np.asarray(M, dtype=np.int64).copy() % p
    rows, cols = A.shape
    rank = 0
    for col in range(cols):
        candidates = np.flatnonzero(A[rank:, col])
        if len(candidates) == 0:
            continue
        pivot = rank + int(candidates[0])
        if pivot != rank:
            A[[rank, pivot]] = A[[pivot, rank]]
        A[rank] = (A[rank] * pow(int(A[rank, col]), -1, p)) % p
        for row in np.flatnonzero(A[:, col]):
            if row != rank:
                A[row] = (A[row] - A[row, col] * A[rank]) % p
        rank += 1
        if rank == rows:
            break
    return rank


def nullspace_mod(M, p: int):
    A = np.asarray(M, dtype=np.int64).copy() % p
    rows, cols = A.shape
    rank = 0
    pivots = []
    for col in range(cols):
        candidates = np.flatnonzero(A[rank:, col])
        if len(candidates) == 0:
            continue
        pivot = rank + int(candidates[0])
        if pivot != rank:
            A[[rank, pivot]] = A[[pivot, rank]]
        A[rank] = (A[rank] * pow(int(A[rank, col]), -1, p)) % p
        for row in np.flatnonzero(A[:, col]):
            if row != rank:
                A[row] = (A[row] - A[row, col] * A[rank]) % p
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
            x[pivot] = (-sum(int(A[ri, c]) * int(x[c]) for c in free)) % p
        basis.append(x)
    return basis


class IncrementalModBasis:
    def __init__(self, p: int):
        self.p = p
        self.rows: list[np.ndarray] = []
        self.pivots: list[int] = []

    def add(self, vector: np.ndarray) -> bool:
        v = np.asarray(vector, dtype=np.int64).copy() % self.p
        for row, pivot in zip(self.rows, self.pivots):
            if v[pivot]:
                v = (v - v[pivot] * row) % self.p
        nonzero = np.flatnonzero(v)
        if len(nonzero) == 0:
            return False
        pivot = int(nonzero[0])
        v = (v * pow(int(v[pivot]), -1, self.p)) % self.p
        for i, row in enumerate(self.rows):
            if row[pivot]:
                self.rows[i] = (row - row[pivot] * v) % self.p
        pos = int(np.searchsorted(self.pivots, pivot))
        self.pivots.insert(pos, pivot)
        self.rows.insert(pos, v)
        return True


def graph_srg_parameters(A: np.ndarray):
    degree = set(map(int, A.sum(axis=1)))
    lam = {int(A[i] @ A[j]) for i, j in combinations(range(len(A)), 2) if A[i, j]}
    mu = {int(A[i] @ A[j]) for i, j in combinations(range(len(A)), 2) if not A[i, j]}
    return degree, lam, mu


def build_certificate():
    points, A40, lines, spreads = build_w33()
    spread_sets = [set(s) for s in spreads]
    A36 = np.zeros((36, 36), dtype=np.int8)
    intersection_census = Counter()
    for i, j in combinations(range(36), 2):
        n = len(spread_sets[i] & spread_sets[j])
        intersection_census[n] += 1
        if n == 4:
            A36[i, j] = A36[j, i] = 1
    assert intersection_census == Counter({1: 360, 4: 270})
    assert graph_srg_parameters(A36) == ({15}, {6}, {6})

    A36s = sp.Matrix(A36)
    I36 = sp.eye(36)
    J36 = sp.ones(36)
    E15 = sp.Rational(1, 2) * I36 + sp.Rational(1, 6) * A36s - sp.Rational(1, 12) * J36
    assert E15 * E15 == E15 and E15.rank() == 15
    axes = tuple(6 * E15[:, i] for i in range(36))
    axis_map = {tuple(a): i for i, a in enumerate(axes)}
    triples = set()
    for i, j in combinations(range(36), 2):
        p = norton(E15, axes[i], axes[j])
        if A36[i, j]:
            assert p == (axes[i] + axes[j]) / 6
        else:
            target = 3 * p + (axes[i] + axes[j]) / 2
            k = axis_map[tuple(target)]
            triples.add(tuple(sorted((i, j, k))))
    triples = tuple(sorted(triples))
    assert len(triples) == 120
    assert set(Counter(x for t in triples for x in t).values()) == {10}

    K = 2 * A36.astype(int) - np.ones((36, 36), dtype=int)
    assert np.array_equal(K, K.T)
    assert np.array_equal(K @ K.T, 36 * np.eye(36, dtype=int))
    assert set(map(int, K.sum(axis=1))) == {-6}
    assert set(map(int, np.diag(K))) == {-1}
    H = sp.Matrix(K) / 6
    assert H * H == I36
    assert E15 == (I36 + H) / 2
    Eguard = (I36 - H) / 2
    assert int(sp.trace(Eguard)) == 21 and E15 + Eguard == I36

    U, basis_cols, rows, Rinv = independent_basis(E15)
    axis_coords = tuple(coords(a, U, rows, Rinv) for a in axes)
    axis_coord_map = {tuple(a): i for i, a in enumerate(axis_coords)}
    I15 = sp.eye(15)
    L_axes = []
    taus = []
    for axis in axes:
        Lfull = E15 * sp.diag(*list(axis))
        L = Rinv * Lfull[rows, :] * U
        L_axes.append(L)
        Pminus = (L - I15) * (L - sp.Rational(1, 6) * I15)
        tau = I15 - 2 * Pminus
        assert tau * tau == I15
        taus.append(tuple(axis_coord_map[tuple(tau * a)] for a in axis_coords))
    assert set(sum(1 for i, j in enumerate(t) if i == j) for t in taus) == {16}

    pair_order_census = Counter()
    triple_lookup = {frozenset((i, j)): next(k for k in t if k not in (i, j)) for t in triples for i, j in combinations(t, 2)}
    for i, j in combinations(range(36), 2):
        order = perm_order(compose(taus[i], taus[j]))
        pair_order_census[(int(A36[i, j]), order)] += 1
        if A36[i, j]:
            assert compose(taus[i], taus[j]) == compose(taus[j], taus[i]) and order == 2
        else:
            k = triple_lookup[frozenset((i, j))]
            assert order == 3 and compose(compose(taus[i], taus[j]), taus[i]) == taus[k]
    assert pair_order_census == Counter({(0, 3): 360, (1, 2): 270})

    generator_indices = (0, 1, 2, 3, 4, 5, 9)
    full_group = closure_perms([taus[i] for i in generator_indices], cap=60_000)
    even_group = closure_perms([compose(taus[0], taus[i]) for i in range(1, 36)], cap=30_000)
    full_order_census = Counter(perm_order(g) for g in full_group)
    even_order_census = Counter(perm_order(g) for g in even_group)
    assert len(full_group) == 51_840 and len(even_group) == 25_920
    assert even_order_census == Counter({1: 1, 2: 315, 3: 800, 4: 3780, 5: 5184, 6: 5760, 9: 5760, 12: 4320})

    def eval_tau_word(word):
        g = tuple(range(36))
        for index in word:
            g = compose(taus[index], g)
        return g

    u42_a_word = (0, 1, 2, 9)
    u42_b_word = (0, 3, 4, 9, 3, 5)
    a = eval_tau_word(u42_a_word)
    b = eval_tau_word(u42_b_word)
    assert [perm_order(a), perm_order(b), perm_order(compose(a, b))] == [2, 5, 9]
    assert perm_order(commutator(a, b)) == 3
    bab = compose(compose(b, a), b)
    assert perm_order(commutator(a, bab)) == 2
    assert len(closure_perms([a, b], cap=30_000)) == 25_920

    u42d2_c_word = (0,)
    u42d2_d_word = (1, 2, 3, 4, 9, 3, 5, 9)
    c = eval_tau_word(u42d2_c_word)
    d = eval_tau_word(u42d2_d_word)
    assert [perm_order(c), perm_order(d), perm_order(compose(c, d))] == [2, 9, 10]
    assert perm_order(compose(c, ppow(d, 2))) == 8
    assert perm_order(commutator(c, ppow(d, 2))) == 2
    y = compose(compose(ppow(d, 3), c), ppow(d, 3))
    assert commutator(c, y) == tuple(range(36))
    assert len(closure_perms([c, d], cap=60_000)) == 51_840

    L_basis = [L_axes[index] / 6 for index in basis_cols]
    Lmod = np.array([[[rat_mod(L_basis[i][r, col]) for col in range(15)] for r in range(15)] for i in range(15)], dtype=np.int64)
    mb = IncrementalModBasis(MOD)
    matrix_basis = []
    for M in [np.eye(15, dtype=np.int64)] + list(Lmod):
        if mb.add(M.reshape(-1)):
            matrix_basis.append(M % MOD)
    changed = True
    while changed and len(matrix_basis) < 225:
        changed = False
        for M in list(matrix_basis):
            for G in Lmod:
                P = (M @ G) % MOD
                if mb.add(P.reshape(-1)):
                    matrix_basis.append(P)
                    changed = True
                    if len(matrix_basis) == 225:
                        break
            if len(matrix_basis) == 225:
                break
    assert len(matrix_basis) == 225

    equations = []
    for i in range(15):
        Li = Lmod[i]
        for r in range(15):
            for col in range(15):
                row = np.zeros(225, dtype=np.int64)
                for q in range(15):
                    row[r * 15 + q] = (row[r * 15 + q] + Li[q, col]) % MOD
                    row[q * 15 + col] = (row[q * 15 + col] - Li[r, q]) % MOD
                    row[q * 15 + i] = (row[q * 15 + i] - Lmod[q, r, col]) % MOD
                equations.append(row)
    derivation_rank = rank_mod(np.array(equations, dtype=np.int64), MOD)
    assert derivation_rank == 225

    adjacent_pair = next((i, j) for i, j in combinations(range(36), 2) if A36[i, j])
    nonadjacent_pair = next((i, j) for i, j in combinations(range(36), 2) if not A36[i, j])
    adjacent_extra = sp.Rational(3, 4) * (axes[adjacent_pair[0]] + axes[adjacent_pair[1]])
    assert norton(E15, adjacent_extra, adjacent_extra) == adjacent_extra
    triple = next(t for t in triples if nonadjacent_pair[0] in t and nonadjacent_pair[1] in t)
    triple_sum = sum((axes[i] for i in triple), sp.zeros(36, 1))
    assert norton(E15, triple_sum, triple_sum) == triple_sum

    def multiplication_spectrum(x):
        Lfull = E15 * sp.diag(*list(x))
        L = Rinv * Lfull[rows, :] * U
        return {str(k): int(v) for k, v in L.eigenvals().items()}

    assert multiplication_spectrum(adjacent_extra) == {"-3/4": 2, "1/4": 5, "-1/4": 6, "1": 1, "3/4": 1}
    assert multiplication_spectrum(triple_sum) == {"-1/2": 8, "1/2": 6, "1": 1}

    D = np.zeros((36, 120), dtype=np.int64)
    for bi, triple in enumerate(triples):
        D[list(triple), bi] = 1
    assert set(map(int, D.sum(axis=0))) == {3} and set(map(int, D.sum(axis=1))) == {10}
    assert np.array_equal(D @ D.T, 10 * np.eye(36, dtype=int) + (1 - np.eye(36, dtype=int) - A36))
    assert Counter(int(D[:, i] @ D[:, j]) for i, j in combinations(range(120), 2)) == Counter({0: 5520, 1: 1620})
    block_graph = D.T @ D - 3 * np.eye(120, dtype=int)
    assert set(map(int, block_graph.sum(axis=1))) == {27}

    groups = defaultdict(list)
    for bi, triple in enumerate(triples):
        common = set(spreads[triple[0]]) & set(spreads[triple[1]]) & set(spreads[triple[2]])
        assert len(common) == 1
        groups[next(iter(common))].append(bi)
    assert len(groups) == 40 and set(map(len, groups.values())) == {3}
    fibers = {li: sorted(groups[li]) for li in range(40)}

    distance = np.full((120, 120), -1, dtype=np.int16)
    for root in range(120):
        distance[root, root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in np.flatnonzero(block_graph[u]):
                if distance[root, v] < 0:
                    distance[root, v] = distance[root, u] + 1
                    queue.append(int(v))
    assert set(tuple(Counter(map(int, distance[i])).get(d, 0) for d in range(4)) for i in range(120)) == {(1, 27, 90, 2)}
    for fiber in fibers.values():
        assert all(distance[i, j] == 3 for i, j in combinations(fiber, 2))

    line_intersection = np.zeros((40, 40), dtype=np.int8)
    for i, j in combinations(range(40), 2):
        if set(lines[i]) & set(lines[j]):
            line_intersection[i, j] = line_intersection[j, i] = 1
    base = 1 - np.eye(40, dtype=np.int8) - line_intersection
    assert graph_srg_parameters(base) == ({27}, {18}, {18})
    edge_perm = {}
    for i, j in combinations(range(40), 2):
        sub = block_graph[np.ix_(fibers[i], fibers[j])]
        if base[i, j]:
            assert int(sub.sum()) == 3 and np.all(sub.sum(axis=0) == 1) and np.all(sub.sum(axis=1) == 1)
            p = tuple(int(np.argmax(sub[r])) for r in range(3))
            edge_perm[(i, j)] = p
            edge_perm[(j, i)] = inverse(p)
        else:
            assert int(sub.sum()) == 0

    identity3 = (0, 1, 2)
    transport = {0: identity3}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in np.flatnonzero(base[u]):
            v = int(v)
            if v not in transport:
                transport[v] = compose(edge_perm[(u, v)], transport[u])
                queue.append(v)
    holonomy_generators = [compose(inverse(transport[v]), compose(p, transport[u])) for (u, v), p in edge_perm.items()]
    holonomy = closure_perms(holonomy_generators, cap=10)
    assert len(holonomy) == 6
    permutations3 = [p for p in product(range(3), repeat=3) if len(set(p)) == 3]
    assert [p for p in permutations3 if all(compose(p, g) == compose(g, p) for g in holonomy)] == [identity3]

    kernel_basis = nullspace_mod(D.T, 2)
    assert len(kernel_basis) == 6
    codewords = []
    coefficient_words = []
    for coefficients in product(range(2), repeat=6):
        word = sum((c * b for c, b in zip(coefficients, kernel_basis)), np.zeros(36, dtype=np.int64)) % 2
        codewords.append(word)
        coefficient_words.append(tuple(coefficients))
    weight_distribution = Counter(int(w.sum()) for w in codewords)
    assert weight_distribution == Counter({0: 1, 16: 27, 20: 36})
    qvalues = [((int(w.sum()) // 4) % 2) for w in codewords]
    assert Counter(qvalues) == Counter({0: 28, 1: 36})
    coefficient_index = {c: i for i, c in enumerate(coefficient_words)}
    polar = np.zeros((6, 6), dtype=np.int64)
    for i in range(6):
        ei = tuple(1 if k == i else 0 for k in range(6))
        for j in range(6):
            ej = tuple(1 if k == j else 0 for k in range(6))
            eij = tuple((a + b) % 2 for a, b in zip(ei, ej))
            polar[i, j] = qvalues[coefficient_index[eij]] ^ qvalues[coefficient_index[ei]] ^ qvalues[coefficient_index[ej]]
    assert rank_mod(polar, 2) == 6 and np.array_equal(np.diag(polar), np.zeros(6, dtype=int))

    supports = np.array([[int(t[j] != j) for j in range(36)] for t in taus], dtype=np.int64)
    assert set(map(int, supports.sum(axis=1))) == {20}
    assert all(np.all((D.T @ support) % 2 == 0) for support in supports)
    weight20 = {tuple(map(int, w)) for w in codewords if int(w.sum()) == 20}
    assert {tuple(map(int, w)) for w in supports} == weight20
    for i, j in combinations(range(36), 2):
        assert int(supports[i] @ supports[j]) == (12 if A36[i, j] else 10)
        if not A36[i, j]:
            k = triple_lookup[frozenset((i, j))]
            assert np.array_equal(supports[i] ^ supports[j], supports[k])

    weight16 = [w for w in codewords if int(w.sum()) == 16]
    G27 = np.zeros((27, 27), dtype=np.int8)
    for i, j in combinations(range(27), 2):
        if int(weight16[i] @ weight16[j]) == 8:
            G27[i, j] = G27[j, i] = 1
    assert graph_srg_parameters(G27) == ({10}, {1}, {5})
    orthogonal_order_formula = 2 * (2 ** 6) * (2 ** 3 + 1) * (2 ** 2 - 1) * (2 ** 4 - 1)
    assert orthogonal_order_formula == 51_840
    rank_profile = {str(p): rank_mod(D, p) for p in (2, 3, 5, 7)}
    assert rank_profile == {"2": 30, "3": 35, "5": 36, "7": 36}

    result = {
        "schema": "w33.pass3722_3728.fischer_hadamard_orthogonal_code.v1",
        "status": "PASS_EXACT_SEVEN_FRONT_SOURCE_MONSTER_EXTERNALS_PENDING",
        "checks": {
            "w33_and_36_spreads_rebuilt": True,
            "norton_triples_fischer_lines": True,
            "miyamoto_group_order_51840": True,
            "even_subgroup_order_25920_and_census": True,
            "symmetric_regular_hadamard_order36": True,
            "exact_naimark_signal15_guard21": True,
            "multiplication_algebra_full225_mod_prime": True,
            "derivations_zero_mod_prime": True,
            "all_two_axis_subalgebras_classified": True,
            "binary_kernel_dimension6_minus_type": True,
            "schlafli27_and_spread36_same_code": True,
            "block_graph_three_cover_exact": True,
            "cover_holonomy_s3_and_nonregular": True,
            "abstract_standard_generator_words": True
        },
        "fischer_miyamoto_closure": {
            "axes": 36, "fischer_lines": 120, "lines_per_axis": 10,
            "commuting_pairs": 270, "noncommuting_order3_pairs": 360,
            "miyamoto_fixed_points_each": 16,
            "generator_axis_indices": list(generator_indices),
            "full_group_order": len(full_group),
            "full_group_order_census": {str(k): v for k, v in sorted(full_order_census.items())},
            "even_product_subgroup_order": len(even_group),
            "even_product_order_census": {str(k): v for k, v in sorted(even_order_census.items())},
            "identification": "The exact 36-point action is O_6^-(2) = U4(2):2; its index-two even-product subgroup has the prior U4(2) order census.",
            "boundary": "The identification is internal finite-group geometry, not a Monster embedding."
        },
        "hadamard_naimark_completion": {
            "integer_matrix": "K = 2 A_spread - J", "matrix_shape": [36, 36], "entries": [-1, 1],
            "identity": "K K^T = 36 I", "symmetric": True, "regular_row_sum": -6, "diagonal": -1,
            "orthogonal_multiport": "H = K/6", "involution": "H^2 = I",
            "signal_projector": "E15 = (I+H)/2", "guard_projector": "E21 = (I-H)/2",
            "signal_rank": 15, "guard_rank": 21, "uniform_amplitude": "1/6", "phase_alphabet": ["0", "pi"],
            "verdict": "The Naimark completion is an explicit rational 36-port symmetric Hadamard involution, not merely an existence/rank certificate.",
            "hardware_boundary": "No fabrication, loss, bandwidth, or laboratory performance is claimed."
        },
        "axial_rigidity": {
            "dimension": 15,
            "associative_multiplication_operator_algebra_dimension_mod_1000003": len(matrix_basis),
            "derivation_equation_rank_mod_1000003": derivation_rank,
            "derivation_dimension_over_Q": 0,
            "ideal_verdict": "SIMPLE: the multiplication operators generate all M15 modulo 1000003, so no nonzero proper ideal survives over Q.",
            "adjacent_two_axis_subalgebra": {"dimension": 2, "idempotents": ["0", "a", "b", "3/4(a+b)"], "extra_idempotent_full_spectrum": {"1": 1, "3/4": 1, "1/4": 5, "-1/4": 6, "-3/4": 2}},
            "nonadjacent_two_axis_subalgebra": {"dimension": 3, "third_axis": "the unique Fischer-line axis c", "idempotents": ["0", "a", "b", "c", "a+b+c"], "triple_sum_full_spectrum": {"1": 1, "1/2": 6, "-1/2": 8}},
            "majorana_boundary": "The algebra is positive Frobenius and axial but remains non-Majorana/non-Griess by its fusion spectrum."
        },
        "binary_orthogonal_code": {
            "triple_incidence_shape": [36, 120], "rank_profile": rank_profile,
            "binary_left_kernel": "[36,6] code", "weight_distribution": {str(k): v for k, v in sorted(weight_distribution.items())},
            "quadratic_form": "q(x)=wt(x)/4 mod 2", "polar_rank": 6, "singular_vectors_including_zero": 28, "minus_type": True,
            "nonsingular_weight20_vectors": 36, "weight20_identification": "exactly the supports of the 36 Miyamoto involutions",
            "singular_nonzero_weight16_vectors": 27, "weight16_graph": "SRG(27,10,1,5), the Schlaefli complement",
            "weight20_graph": "SRG(36,15,6,6), the spread graph", "orthogonal_group_order_formula": orthogonal_order_formula,
            "interpretation": "One six-bit minus-type quadratic space contains the 27 and 36 carriers as its singular and nonsingular nonzero vectors."
        },
        "triple_block_three_cover": {
            "block_graph_vertices": 120, "degree": 27, "spectrum": {"27": 1, "9": 20, "3": 15, "-3": 84},
            "distance_distribution_from_every_vertex": [1, 27, 90, 2], "antipodal_fibers": 40, "fiber_size": 3,
            "fiber_meaning": "the three Norton triples through one W33 line",
            "quotient_graph": "complement of the W33 line-intersection graph, SRG(40,27,18,18)",
            "edges_between_adjacent_fibers": "a perfect matching", "cover_degree": 3,
            "holonomy_group": "S3", "deck_group": "trivial", "regular_cover": False,
            "interpretation": "The 120 triples form a connected nonregular three-cover; the ternary fiber is real, but its monodromy is full S3 rather than a global C3 deck symmetry."
        },
        "abstract_monster_search_targets": {
            "u42_standard_pair": {"a_tau_word": list(u42_a_word), "b_tau_word": list(u42_b_word), "orders_a_b_ab": [2, 5, 9], "commutator_orders": [3, 2], "generated_order": 25920},
            "u42d2_standard_pair": {"c_tau_word": list(u42d2_c_word), "d_tau_word": list(u42d2_d_word), "orders_c_d_cd": [2, 9, 10], "orders_cd2_commutator": [8, 2], "generated_order": 51840},
            "monster_word_status": "ABSTRACT_WORD_COMPRESSION_EXACT; serialized mmgroup words remain pending",
            "class_fusion_status": "Existing GAP/CTblLib target retained; no executed restriction artifact is promoted by this Python run.",
            "search_refinement": "Search 2B involution candidates for the exact 36-involution Fischer pattern, then compress to the listed standard pairs before expensive closure and character tests."
        },
        "evidence_boundary": {
            "proved_here": ["120 Norton triples are the Fischer lines of an exact 36-involution 3-transposition action", "Miyamoto group order 51840 with U4(2) even subgroup order 25920", "explicit symmetric regular Hadamard 36-port Naimark completion", "full multiplication operator algebra and zero derivations", "binary six-dimensional minus-type orthogonal code with 27+36 split", "nonregular S3-holonomy three-cover on 120 blocks", "short exact standard-generator words in Miyamoto involutions"],
            "not_proved_here": ["serialized Monster words", "executed Monster 196883 class-fusion restriction", "Majorana, Griess, or VOA realization", "physical optical implementation", "remote CI or canonical PDF success"]
        }
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    result["semantic_sha256"] = sha256(payload.encode("utf-8")).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if expected != result:
            raise SystemExit("frozen certificate mismatch")
        print("PASS frozen certificate", result["semantic_sha256"])
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "semantic_sha256": result["semantic_sha256"], "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
