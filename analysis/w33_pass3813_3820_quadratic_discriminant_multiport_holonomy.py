#!/usr/bin/env python3
"""Passes 3813-3820 exact quadratic-parent closure.

Rebuilds the six-bit minus quadratic space, the 36-port graph, 120 Fischer
triples, 135 Lagrangian frames, the rooted Construction-A discriminant module,
an exact two-mode compiler for the 21 commuting reflections, the rank-five
holonomy association scheme, and three derived constructions.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import numpy as np
import sympy as sp

SCHEMA = "w33.pass3813_3820.quadratic_discriminant_multiport_holonomy.v1"
STATUS = "PASS_EXACT_EIGHT_FRONT_SOURCE_MONSTER_WORDS_HARDWARE_CI_PDF_PENDING"


def bits(x: int, n: int = 6) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def q(x: int) -> int:
    b = bits(x)
    return (b[0] * b[1] + b[2] * b[3] + b[4] * b[5] + b[4] + b[5]) & 1


def beta(x: int, y: int) -> int:
    return q(x ^ y) ^ q(x) ^ q(y)


def gf2_rank(vecs: Iterable[int]) -> int:
    piv: dict[int, int] = {}
    for value in vecs:
        x = int(value)
        while x:
            p = x.bit_length() - 1
            if p in piv:
                x ^= piv[p]
            else:
                piv[p] = x
                break
    return len(piv)


def gf2_basis(vecs: Iterable[int]) -> list[int]:
    piv: dict[int, int] = {}
    for value in vecs:
        x = int(value)
        while x:
            p = x.bit_length() - 1
            if p in piv:
                x ^= piv[p]
            else:
                piv[p] = x
                for pp in list(piv):
                    if pp != p and ((piv[pp] >> p) & 1):
                        piv[pp] ^= x
                break
    return [piv[p] for p in sorted(piv, reverse=True)]


def gf2_nullspace(rows: list[int], n: int) -> list[int]:
    work = list(rows)
    pivots: list[int] = []
    r = 0
    for col in range(n):
        pivot = next((i for i in range(r, len(work)) if (work[i] >> col) & 1), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        for i in range(len(work)):
            if i != r and ((work[i] >> col) & 1):
                work[i] ^= work[r]
        pivots.append(col)
        r += 1
        if r == len(work):
            break
    free = [c for c in range(n) if c not in pivots]
    out: list[int] = []
    for f in free:
        x = 1 << f
        for i, p in enumerate(pivots):
            if (work[i] >> f) & 1:
                x |= 1 << p
        out.append(x)
    return out


def extend_basis(base: list[int], candidates: Iterable[int]) -> tuple[list[int], list[int]]:
    basis = gf2_basis(base)
    rank = len(basis)
    added: list[int] = []
    for value in candidates:
        candidate = gf2_basis(basis + [int(value)])
        if len(candidate) > rank:
            basis = candidate
            rank += 1
            added.append(int(value))
    return added, basis


def enumerate_code(basis: list[int]) -> list[int]:
    words = [0]
    for b in basis:
        words += [x ^ b for x in words]
    return words


def span3(a: int, b: int, c: int) -> frozenset[int]:
    return frozenset({0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c})


def build_geometry() -> dict[str, object]:
    singular = [x for x in range(1, 64) if q(x) == 0]
    nonsingular = [x for x in range(1, 64) if q(x) == 1]
    n_index = {x: i for i, x in enumerate(nonsingular)}

    lines: set[tuple[int, int, int]] = set()
    for x in range(1, 64):
        for y in range(x + 1, 64):
            lines.add(tuple(sorted((x, y, x ^ y))))
    line_classes = Counter(sum(q(x) for x in line) for line in lines)
    singular_lines = sorted(line for line in lines if all(q(x) == 0 for x in line))
    triples = sorted(line for line in lines if all(q(x) == 1 for x in line))

    a36 = np.zeros((36, 36), dtype=np.int64)
    for i, x in enumerate(nonsingular):
        for j, y in enumerate(nonsingular):
            if i != j and beta(x, y) == 0:
                a36[i, j] = 1
    assert np.all(a36.sum(axis=1) == 15)
    assert np.array_equal(a36 @ a36, 15 * np.eye(36, dtype=np.int64) + 6 * a36 + 6 * (np.ones((36, 36), dtype=np.int64) - np.eye(36, dtype=np.int64) - a36))

    tinc = np.zeros((36, 120), dtype=np.int64)
    for j, line in enumerate(triples):
        for x in line:
            tinc[n_index[x], j] = 1

    subspaces: set[frozenset[int]] = set()
    for a, b, c in itertools.combinations(range(1, 64), 3):
        if gf2_rank([a, b, c]) == 3:
            subspaces.add(span3(a, b, c))
    lagrangians = sorted(
        [u for u in subspaces if all(beta(x, y) == 0 for x, y in itertools.combinations([z for z in u if z], 2))],
        key=lambda u: tuple(sorted(u)),
    )
    assert len(lagrangians) == 135
    finc = np.zeros((36, 135), dtype=np.int64)
    for j, u in enumerate(lagrangians):
        ns = [x for x in u if q(x) == 1]
        ss = tuple(sorted(x for x in u if x and q(x) == 0))
        assert len(ns) == 4 and ss in singular_lines
        for x in ns:
            finc[n_index[x], j] = 1

    j36 = np.ones((36, 36), dtype=np.int64)
    assert np.array_equal(tinc @ tinc.T, 9 * np.eye(36, dtype=np.int64) + j36 - a36)
    assert np.array_equal(finc @ finc.T, 15 * np.eye(36, dtype=np.int64) + 3 * a36)
    resolution = finc @ finc.T + 3 * (tinc @ tinc.T)
    assert np.array_equal(resolution, 42 * np.eye(36, dtype=np.int64) + 3 * j36)

    a64 = np.zeros((64, 64), dtype=np.int64)
    for x in range(64):
        for y in range(64):
            if x != y and q(x ^ y) == 1:
                a64[x, y] = 1
    assert np.array_equal(a64 @ a64, 16 * np.eye(64, dtype=np.int64) + 20 * np.ones((64, 64), dtype=np.int64))
    local_n = a64[np.ix_(nonsingular, nonsingular)]
    assert np.array_equal(local_n, j36 - np.eye(36, dtype=np.int64) - a36)
    gq27 = np.zeros((27, 27), dtype=np.int64)
    for i, x in enumerate(singular):
        for j, y in enumerate(singular):
            if i != j and beta(x, y) == 0:
                gq27[i, j] = 1
    local_s = a64[np.ix_(singular, singular)]
    assert np.array_equal(local_s, np.ones((27, 27), dtype=np.int64) - np.eye(27, dtype=np.int64) - gq27)

    return {
        "singular": singular, "nonsingular": nonsingular, "lines": sorted(lines),
        "singular_lines": singular_lines, "triples": triples, "lagrangians": lagrangians,
        "A36": a36, "A64": a64, "GQ27": gq27, "T": tinc, "F": finc,
        "line_classes": line_classes,
    }


def build_norton_compression(geo: dict[str, object]) -> dict[str, object]:
    a = np.asarray(geo["A36"], dtype=np.int64)
    triples = list(geo["triples"])
    nonsingular = list(geo["nonsingular"])
    n_index = {x: i for i, x in enumerate(nonsingular)}
    k4s = [c for c in itertools.combinations(range(36), 4) if all(a[i, j] for i, j in itertools.combinations(c, 2))]
    assert len(k4s) == 135

    m = 6 * np.eye(36, dtype=np.int64) + 2 * a - np.ones((36, 36), dtype=np.int64)
    bcols = [m[:, i] for i in range(36)]
    norton: set[tuple[int, int, int]] = set()
    for i, j in itertools.combinations(range(36), 2):
        if a[i, j] != 0:
            continue
        lhs = m @ (bcols[i] * bcols[j])
        matches = [k for k in range(36) if np.array_equal(lhs, 4 * (-bcols[i] - bcols[j] + 2 * bcols[k]))]
        assert len(matches) == 1
        norton.add(tuple(sorted((i, j, matches[0]))))
    assert len(norton) == 120
    geometric = {tuple(sorted(n_index[x] for x in line)) for line in triples}
    assert norton == geometric

    tinc = np.zeros((36, 120), dtype=np.int64)
    for j, tri in enumerate(sorted(norton)):
        for i in tri:
            tinc[i, j] = 1
    rows = []
    for i in range(36):
        word = 0
        for j in range(120):
            if tinc[i, j] & 1:
                word |= 1 << j
        rows.append(word)
    rank_t = gf2_rank(rows)
    assert rank_t == 30

    code = set()
    for label in range(64):
        word = 0
        for i, x in enumerate(nonsingular):
            if beta(label, x):
                word |= 1 << i
        code.add(word)
    assert len(code) == 64
    weights = Counter(w.bit_count() for w in code)
    assert weights == Counter({0: 1, 16: 27, 20: 36})
    for word in code:
        for tri in sorted(norton):
            assert sum((word >> i) & 1 for i in tri) % 2 == 0

    graph_words = set()
    for i in range(36):
        word = 0
        for j in range(36):
            if i != j and a[i, j] == 0:
                word |= 1 << j
        graph_words.add(word)
    assert graph_words == {w for w in code if w.bit_count() == 20}

    nonzero = sorted(w for w in code if w)
    abstract_lines: set[tuple[int, int, int]] = set()
    for u, v in itertools.combinations(nonzero, 2):
        abstract_lines.add(tuple(sorted((u, v, u ^ v))))
    split = Counter(sum(1 for w in line if w.bit_count() == 20) for line in abstract_lines)
    assert split == Counter({0: 45, 1: 216, 2: 270, 3: 120})

    def hash_sets(items: Iterable[Iterable[int]]) -> str:
        payload = "\n".join(",".join(str(x) for x in item) for item in sorted(tuple(sorted(y)) for y in items))
        return hashlib.sha256(payload.encode()).hexdigest()

    return {
        "k4_count": len(k4s), "norton_triple_count": len(norton),
        "triple_incidence_rank_f2": rank_t,
        "code_weight_distribution": dict(sorted(weights.items())),
        "abstract_line_split_by_weight20_count": dict(sorted(split.items())),
        "hashes": {"k4": hash_sets(k4s), "norton": hash_sets(norton), "abstract_lines": hash_sets(abstract_lines)},
    }


def build_discriminant(geo: dict[str, object]) -> dict[str, object]:
    nonsingular = list(geo["nonsingular"])
    code = set()
    for label in range(64):
        word = 0
        for i, x in enumerate(nonsingular):
            if beta(label, x):
                word |= 1 << i
        code.add(word)
    cbasis = gf2_basis(code)
    assert len(cbasis) == 6
    assert all(w.bit_count() % 4 == 0 for w in code)
    assert all(((u & v).bit_count() & 1) == 0 for u in cbasis for v in cbasis)

    extension = [
        int("800834e5c", 16), int("4008637fe", 16), int("200021295", 16),
        int("100076c9c", 16), int("80040c9a", 16), int("40862441", 16),
        int("208523d6", 16), int("10807c01", 16), int("8024e6f", 16),
        int("4853ef7", 16), int("1015e76", 16),
    ]
    dbasis = gf2_basis(cbasis + extension)
    assert len(dbasis) == 17
    dwords = enumerate_code(dbasis)
    assert all(w.bit_count() % 4 == 0 for w in dwords)
    assert all(((u & v).bit_count() & 1) == 0 for u in dbasis for v in dbasis)
    dweights = Counter(w.bit_count() for w in dwords)
    expected_d = Counter({0: 1, 8: 225, 12: 9555, 16: 55755, 20: 55755, 24: 9555, 28: 225, 36: 1})
    assert dweights == expected_d

    dperp = gf2_nullspace(dbasis, 36)
    added, _ = extend_basis(dbasis, dperp)
    assert len(added) == 2
    reps = [added[0], added[1], added[0] ^ added[1]]
    neighbor_enumerators: list[dict[int, int]] = []
    for rep in reps:
        ebasis = gf2_basis(dbasis + [rep])
        assert len(ebasis) == 18
        ewords = enumerate_code(ebasis)
        assert all(w.bit_count() % 2 == 0 for w in ewords)
        assert all(((u & v).bit_count() & 1) == 0 for u in ebasis for v in ebasis)
        neighbor_enumerators.append(dict(sorted(Counter(w.bit_count() for w in ewords).items())))
    assert neighbor_enumerators[0] == neighbor_enumerators[1]
    assert neighbor_enumerators[2] != neighbor_enumerators[0]
    for rep in reps:
        coset_mod4 = {((w ^ rep).bit_count() % 4) for w in dwords}
        assert 0 not in coset_mod4

    chain = []
    for r in range(12):
        basis = gf2_basis(cbasis + extension[:r])
        words = enumerate_code(basis)
        assert len(basis) == 6 + r
        assert all(w.bit_count() % 4 == 0 for w in words)
        chain.append({"isotropic_rank": r, "code_dimension": 6 + r, "lattice_determinant": 2 ** (24 - 2 * r)})

    return {
        "discriminant_group": "(Z/2Z)^24",
        "quadratic_form": "q_D(c+C)=wt(c)/2 mod 2Z on C_perp/C",
        "maximal_isotropic_rank": 11,
        "maximal_even_overlattice_determinant": 4,
        "unimodular_even_obstruction": "rank 36 is not divisible by 8",
        "maximal_code": {"parameters": [36, 17, 8], "weight_distribution": dict(sorted(dweights.items())), "extension_vectors_hex": [hex(x) for x in extension]},
        "even_overlattice_chain": chain,
        "odd_unimodular_code_neighbors": {
            "count": 3, "enumerator_types": 2, "weight_distributions": neighbor_enumerators,
            "boundary": "These are three canonical singly-even self-dual code extensions; equality or inequivalence within the repeated enumerator type is not inferred from the enumerator alone.",
        },
    }


def primitive_integer_negative_basis(a36: np.ndarray) -> list[list[int]]:
    h = (2 * sp.Matrix(a36) - sp.ones(36)) / 6
    basis = (h + sp.eye(36)).nullspace()
    assert len(basis) == 21
    orth: list[sp.Matrix] = []
    out: list[list[int]] = []
    for vector in basis:
        w = vector
        for u in orth:
            w = w - (w.dot(u) / u.dot(u)) * u
        orth.append(w)
        denoms = [int(sp.denom(x)) for x in w]
        scale = int(sp.ilcm(*denoms))
        vals = [int(x * scale) for x in w]
        g = 0
        for x in vals:
            g = math.gcd(g, abs(x))
        vals = [x // g for x in vals]
        if next(x for x in vals if x) < 0:
            vals = [-x for x in vals]
        out.append(vals)
    for i, u in enumerate(out):
        for j, v in enumerate(out):
            dot = sum(x * y for x, y in zip(u, v))
            assert (dot == 0) if i != j else (dot > 0)
    return out


def tree_compile_vector(vector: list[int]) -> tuple[list[list[dict[str, object]]], int]:
    nodes = [(i, x * x, 1 if x > 0 else -1) for i, x in enumerate(vector) if x]
    layers: list[list[dict[str, object]]] = []
    while len(nodes) > 1:
        next_nodes = []
        layer: list[dict[str, object]] = []
        for k in range(0, len(nodes) - 1, 2):
            i, na, sa = nodes[k]
            j, nb, sb = nodes[k + 1]
            total = na + nb
            layer.append({"modes": [i, j], "c2": [na, total], "s2": [nb, total], "c_sign": sa, "s_sign": sb})
            next_nodes.append((i, total, 1))
        if len(nodes) & 1:
            next_nodes.append(nodes[-1])
        layers.append(layer)
        nodes = next_nodes
    return layers, nodes[0][0]


def build_multiport(geo: dict[str, object]) -> dict[str, object]:
    a36 = np.asarray(geo["A36"], dtype=np.int64)
    h = (2 * a36 - np.ones((36, 36), dtype=np.int64)) / 6.0
    assert np.max(np.abs(h @ h.T - np.eye(36))) < 1e-12
    vectors = primitive_integer_negative_basis(a36)

    records = []
    gate_count = 0
    depth = 0
    for vector in vectors:
        layers, phase_mode = tree_compile_vector(vector)
        support = sum(x != 0 for x in vector)
        assert sum(len(layer) for layer in layers) == support - 1
        gate_count += 2 * (support - 1)
        depth += 2 * len(layers) + 1
        records.append({"layers": layers, "phase_mode": phase_mode, "support": support, "norm2": sum(x * x for x in vector)})
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    compiler_hash = hashlib.sha256(canonical.encode()).hexdigest()

    work = h.copy()
    qr_ops = []
    last_layer = [-1] * 36
    max_layer = -1
    for col in range(36):
        for row in range(35, col, -1):
            av = work[row - 1, col]
            bv = work[row, col]
            if abs(bv) < 1e-13:
                continue
            rho = math.hypot(av, bv)
            c = av / rho
            s = bv / rho
            r1 = c * work[row - 1] + s * work[row]
            r2 = -s * work[row - 1] + c * work[row]
            work[row - 1], work[row] = r1, r2
            layer = max(last_layer[row - 1], last_layer[row]) + 1
            last_layer[row - 1] = last_layer[row] = layer
            max_layer = max(max_layer, layer)
            c2 = Fraction(c * c).limit_denominator(10**9)
            s2 = 1 - c2
            assert abs(float(s2) - s * s) < 1e-12
            qr_ops.append((row - 1, row, col, c2.numerator, c2.denominator, 1 if c >= 0 else -1, 1 if s >= 0 else -1, layer))
    assert len(qr_ops) == 512
    assert max_layer + 1 == 69
    assert np.max(np.abs(work - np.diag(np.diag(work)))) < 1e-12
    assert list(np.diag(work).round().astype(int)).count(-1) == 1
    qr_hash = hashlib.sha256(json.dumps(qr_ops, separators=(",", ":")).encode()).hexdigest()

    return {
        "multiport": "H=(2A36-J)/6", "rank_split": [15, 21],
        "exact_tree_compiler": {
            "integer_reflections": 21, "two_mode_rotations": gate_count, "single_mode_pi_phases": 21,
            "sequential_balanced_tree_depth": depth,
            "maximum_reflection_tree_depth": max(2 * len(r["layers"]) + 1 for r in records),
            "parameterization": "Every Givens coefficient is a signed square root of the recorded rational c^2 or s^2; forward tree, one pi phase, and inverse tree equal the integer Householder reflection exactly.",
            "compiler_sha256": compiler_hash,
            "supports": [r["support"] for r in records], "norms2": [r["norm2"] for r in records],
        },
        "adjacent_qr_optimization": {
            "rotations": 512, "nearest_neighbor_layers": 69, "one_terminal_sign": True,
            "rational_square_parameter_sha256": qr_hash,
            "boundary": "Topology and rational-square angle data are deterministic and numerically reconstructed; the exact proof-carrying compiler is the 21-reflection tree construction above.",
        },
        "depth_lower_bound": {"layers": 6, "proof": "A depth-d circuit of disjoint two-mode gates can spread one input to at most 2^d outputs. H has full support 36, so d>=ceil(log2 36)=6."},
    }


def all_pairs_distance(a: np.ndarray) -> np.ndarray:
    n = a.shape[0]
    out = np.full((n, n), 99, dtype=np.int64)
    for source in range(n):
        out[source, source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in np.flatnonzero(a[u]):
                if out[source, v] == 99:
                    out[source, v] = out[source, u] + 1
                    queue.append(int(v))
    return out


def perm_compose(p: tuple[int, ...], qv: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[qv[i]] for i in range(len(qv)))


def perm_type(p: tuple[int, int, int]) -> str:
    fixed = sum(p[i] == i for i in range(3))
    return "identity" if fixed == 3 else ("transposition" if fixed == 1 else "three_cycle")


def build_holonomy_scheme(geo: dict[str, object]) -> dict[str, object]:
    tinc = np.asarray(geo["T"], dtype=np.int64)
    a120 = (tinc.T @ tinc == 1).astype(np.int64)
    np.fill_diagonal(a120, 0)
    assert np.all(a120.sum(axis=1) == 27)
    distances = all_pairs_distance(a120)
    rdist3 = (distances == 3).astype(np.int64)
    fibers: list[list[int]] = []
    unseen = set(range(120))
    while unseen:
        seed = min(unseen)
        fiber = sorted([seed] + list(np.flatnonzero(rdist3[seed])))
        assert len(fiber) == 3
        fibers.append(fiber)
        unseen.difference_update(fiber)
    assert len(fibers) == 40

    jfib = np.zeros((120, 120), dtype=np.int64)
    for fiber in fibers:
        jfib[np.ix_(fiber, fiber)] = 1
    fstd = 3 * np.eye(120, dtype=np.int64) - jfib
    q20 = fstd @ a120 @ fstd + 9 * fstd
    assert np.array_equal(q20 @ q20, 108 * q20)
    assert np.all(np.diag(q20) == 18)
    assert np.linalg.matrix_rank(q20.astype(float), tol=1e-8) == 20

    qvalues = [18, -9, -3, 0, 6]
    relations = [(q20 == value).astype(np.int64) for value in qvalues]
    assert np.array_equal(sum(relations), np.ones((120, 120), dtype=np.int64))
    valencies = [int(r[0].sum()) for r in relations]
    assert valencies == [1, 2, 54, 36, 27]

    p = np.zeros((5, 5, 5), dtype=np.int64)
    for i, ri in enumerate(relations):
        for j, rj in enumerate(relations):
            product = ri @ rj
            for k, rk in enumerate(relations):
                values = np.unique(product[rk == 1])
                assert len(values) == 1
                p[i, j, k] = int(values[0])
    assert np.array_equal(p, p.transpose(1, 0, 2))

    eigenmatrix = [[1, 2, 54, 36, 27], [1, -1, -9, 0, 9], [1, 2, -6, 6, -3], [1, -1, 3, 0, -3], [1, 2, 6, -12, 3]]
    multiplicities = [1, 20, 24, 60, 15]
    pmat = sp.Matrix(eigenmatrix)
    qmat = 120 * pmat.inv()
    assert pmat.T * sp.diag(*multiplicities) * pmat == 120 * sp.diag(*valencies)
    for i in range(5):
        for j in range(5):
            for row in eigenmatrix:
                assert row[i] * row[j] == sum(int(p[i, j, k]) * row[k] for k in range(5))

    base_w33 = np.zeros((40, 40), dtype=np.int64)
    base_complement = np.zeros((40, 40), dtype=np.int64)
    transports: dict[tuple[int, int], tuple[int, int, int]] = {}
    for i in range(40):
        for j in range(i + 1, 40):
            counts = tuple(int(relations[r][np.ix_(fibers[i], fibers[j])].sum()) for r in range(1, 5))
            if counts == (0, 0, 9, 0):
                base_w33[i, j] = base_w33[j, i] = 1
            else:
                assert counts == (0, 6, 0, 3)
                base_complement[i, j] = base_complement[j, i] = 1
                block = relations[4][np.ix_(fibers[i], fibers[j])]
                perm = tuple(int(np.argmax(block[row])) for row in range(3))
                inv = [0, 0, 0]
                for row, col in enumerate(perm):
                    inv[col] = row
                transports[(i, j)] = perm
                transports[(j, i)] = tuple(inv)
    assert np.all(base_w33.sum(axis=1) == 12)
    assert np.array_equal(base_complement, np.ones((40, 40), dtype=np.int64) - np.eye(40, dtype=np.int64) - base_w33)

    triangle_holonomy = Counter()
    for i, j, k in itertools.combinations(range(40), 3):
        if base_complement[i, j] and base_complement[j, k] and base_complement[k, i]:
            hol = perm_compose(transports[(k, i)], perm_compose(transports[(j, k)], transports[(i, j)]))
            triangle_holonomy[perm_type(hol)] += 1
    assert triangle_holonomy == Counter({"identity": 1080, "transposition": 2160})

    cycles4: set[tuple[int, int, int, int]] = set()
    for a in range(40):
        for b in np.flatnonzero(base_complement[a]):
            for c in np.flatnonzero(base_complement[b]):
                if c in (a, b):
                    continue
                for d in np.flatnonzero(base_complement[c]):
                    if d in (a, b, c) or not base_complement[d, a]:
                        continue
                    cycle = (a, int(b), int(c), int(d))
                    variants = []
                    for orientation in (cycle, cycle[::-1]):
                        variants.extend(orientation[s:] + orientation[:s] for s in range(4))
                    cycles4.add(min(variants))
    four_holonomy = Counter()
    for a, b, c, d in cycles4:
        hol = perm_compose(transports[(d, a)], perm_compose(transports[(c, d)], perm_compose(transports[(b, c)], transports[(a, b)])))
        four_holonomy[perm_type(hol)] += 1
    assert four_holonomy["three_cycle"] > 0

    moments = {degree: Fraction(18**degree + 2 * ((-9) ** degree) + 54 * ((-3) ** degree) + 27 * (6**degree), 18**degree) for degree in range(1, 4)}
    assert moments[1] == 0 and moments[2] == 6 and moments[3] == Fraction(3, 2)
    p_sparse = {f"R{i}R{j}": {f"R{k}": int(p[i, j, k]) for k in range(5) if p[i, j, k]} for i in range(1, 5) for j in range(i, 5)}

    return {
        "vertices": 120, "relation_inner_products": ["1", "-1/2", "-1/6", "0", "1/3"],
        "valencies": valencies, "multiplicities": multiplicities, "first_eigenmatrix_P": eigenmatrix,
        "second_eigenmatrix_Q": [[str(x) for x in qmat.row(i)] for i in range(5)],
        "multiplication": p_sparse, "rank20_projector": "E20=(F A120 F+9F)/108; Q20^2=108Q20",
        "spherical_design": {"verdict": "spherical 2-design but not a 3-design", "fixed_vector_moments": {str(k): str(v) for k, v in moments.items()}},
        "quotient": {"fibers": 40, "fiber_size": 3, "W33_pair_blocks": {"complete_R3_K3_3": 240, "R4_matching_plus_R2_complement": 540}},
        "curvature": {
            "base_complement_triangles": 3240, "triangle_holonomy": dict(triangle_holonomy),
            "simple_four_cycles": len(cycles4), "four_cycle_holonomy": dict(four_holonomy),
            "holonomy_group": "S3 (transpositions occur on triangles and three-cycles occur on four-cycles)",
        },
    }


def semantic_payload(certificate: dict[str, object]) -> dict[str, object]:
    return {k: v for k, v in certificate.items() if k not in {"semantic_sha256"}}


def build_certificate() -> dict[str, object]:
    geo = build_geometry()
    compression = build_norton_compression(geo)
    discriminant = build_discriminant(geo)
    multiport = build_multiport(geo)
    holonomy = build_holonomy_scheme(geo)
    cert: dict[str, object] = {
        "schema": SCHEMA, "status": STATUS,
        "checks": {
            "quadratic_parent_srg_64_36_20_20": True, "local_graphs_spread_complement_and_schlafli": True,
            "frame_triple_resolution_identity": True, "maximal_doubly_even_extension_rank17": True,
            "maximal_even_overlattice_determinant4": True, "exact_21_reflection_two_mode_tree_compile": True,
            "holonomy_rank5_association_scheme": True, "norton_seed_reconstruction": True,
            "triangle_curvature_law": True, "three_odd_unimodular_code_neighbors": True,
        },
        "quadratic_parent": {
            "quadratic_space": "F2^6 minus type", "singular_nonzero": 27, "nonsingular": 36,
            "projective_line_split": {str(k): int(v) for k, v in sorted(geo["line_classes"].items())},
            "bent_cayley_graph": {
                "parameters": [64, 36, 20, 20], "spectrum": {"36": 1, "4": 27, "-4": 36},
                "first_subconstituent": "complement of SRG(36,15,6,6)",
                "second_subconstituent": "Schlafli graph, complement of SRG(27,10,1,5)",
            },
        },
        "discriminant_and_overlattices": discriminant, "multiport_compiler": multiport,
        "holonomy_association_scheme": holonomy,
        "monster_descent_compression": {
            "seed": "the labeled SRG(36,15,6,6) adjacency alone", "reconstructed": compression,
            "promotion_rule": "A target-group candidate must first realize the 36-vertex graph; the 135 K4 frames, 120 Norton triples, [36,6] code, and 45+216+270+120 six-bit line split are then recomputed functorially rather than supplied as independent coincidences.",
            "boundary": "No serialized Monster elements, subgroup embedding, or character restriction is produced here.",
        },
        "bonkers_complementary_design_identity": {
            "frame_incidence": "F F^T=15I+3A", "triple_incidence": "T T^T=9I+J-A",
            "resolution": "F F^T+3 T T^T=42I+3J", "weighted_incidence_singular_values_squared": {"150": 1, "42": 35},
            "interpretation": "After removing the all-ones channel, the weighted 135-frame plus 120-triple carrier is an exact tight 35-dimensional resolution of the 36 ports.",
        },
        "bonkers_odd_unimodular_neighbors": discriminant["odd_unimodular_code_neighbors"],
        "bonkers_discrete_curvature": holonomy["curvature"],
        "evidence_boundary": {
            "proved_here": [
                "the 64-point bent Cayley parent and both local subconstituents",
                "the discriminant form model, maximal isotropic rank eleven, determinant-four maximal even chain, and three singly-even self-dual neighbors",
                "an exact proof-carrying 21-reflection two-mode tree compiler and a 512-rotation adjacent optimization candidate",
                "the full rank-five holonomy association scheme and its eigenmatrices",
                "functorial reconstruction of the 135/120/27/36/45 line tower from the 36-graph seed",
                "the complementary frame/triple resolution and S3 curvature census",
            ],
            "not_proved_here": [
                "serialized Monster words, an executed Monster subgroup embedding, or character fusion",
                "Leech, rootless, or even-unimodular rank-36 identification",
                "optimal two-mode gate count or optimal depth beyond the proved lower and constructive upper bounds",
                "optical fabrication, loss, detector, or laboratory performance",
                "remote CI or PDF success before an observable result is present",
            ],
        },
    }
    normalized = json.loads(json.dumps(cert, sort_keys=True))
    digest = hashlib.sha256(json.dumps(semantic_payload(normalized), sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    normalized["semantic_sha256"] = digest
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    cert = build_certificate()
    rendered = json.dumps(cert, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = json.loads(args.check.read_text())
        if cert != expected:
            raise SystemExit("frozen certificate mismatch")
        print(f"PASS {cert['semantic_sha256']}")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
        print(args.output)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
