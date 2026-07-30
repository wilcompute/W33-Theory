#!/usr/bin/env python3
"""Exact support routines for Passes 1345--1349.

This module reconstructs the literal 26-dimensional W(E6)/S5 Hecke algebra
from the Pass-1321 rational matrix units, its modular quotient maps, and the
literal 480-directed-edge species-20 projector.  It contains no physical or
continuum claims.
"""
from __future__ import annotations
from collections import deque
from functools import reduce
from itertools import product
from pathlib import Path
from math import gcd
import hashlib
import json
import math
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass1330_1334_modular_triality_cycle_atlas as old

P = old.P
GROUP_ORDER = 51840
ONE = [1] + [0] * 25
BASIS = [[int(i == j) for i in range(26)] for j in range(26)]
FILES = old.FILES
ORDINARY = ["1", "6", "15", "15a", "20", "30", "60a", "64", "81_minus"]
ORDINARY_MULTIPLICITY_DIMS = [1, 2, 1, 1, 3, 2, 1, 2, 1]

DECOMP = {
    2: {
        "simples": ["M2_0", "F_0"],
        "dims": [2, 1],
        "D": [[0,1],[0,2],[0,1],[0,1],[0,3],[0,2],[0,1],[1,0],[0,1]],
    },
    3: {
        "simples": ["F_0", "F_1", "F_2", "F_3"],
        "dims": [1,1,1,1],
        "D": [[0,1,0,0],[0,1,1,0],[0,0,1,0],[1,0,0,0],[1,1,1,0],[1,0,1,0],[1,0,0,0],[1,0,1,0],[0,0,0,1]],
    },
    5: {
        "simples": ["M3_0", "M2_1", "F_0", "F_1", "F_2", "F_3", "F_4", "F_5", "F_6"],
        "dims": [3,2,1,1,1,1,1,1,1],
        "D": [[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,1,0],[0,0,0,1,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,0,1]],
    },
}

ATLAS = [
 ('1A','(cdcdcddcdcdddcdd)^4',1,51840),('2A','(cdd)^4',2,1152),('2B','(cdcdcddcdcdddcdd)^2',2,192),
 ('3A','(cdcdd)^4',3,648),('3C','(ccdcdddcddd)^2',3,216),('3D','(cddcdcdddcdd)^2',3,108),
 ('4A','(cdd)^2',4,96),('4B','cdcdcddcdcdddcdd',4,16),('5A','(cd)^2',5,10),
 ('6A','(cdcdd)^2',6,72),('6C','ccdcdddcddd',6,36),('6E','cddcdcdddcdd',6,36),
 ('6F','(cdcdcdd)^2',6,24),('9A','d',9,9),('12A','cdcdd',12,12),
 ('2C','(ccdcdcddcdcdddcddcddcdcdddcdd)^3',2,1440),('2D','(cdcdddcdd)^3',2,96),
 ('4C','(cdcdcdd)^3',4,96),('4D','dcdcdcdd',4,32),
 ('6G','ccdcdcddcdcdddcddcddcdcdddcdd',6,36),('6H','dcdd',6,36),('6I','cdcdddcdd',6,12),
 ('8A','cdd',8,8),('10A','cd',10,10),('12C','cdcdcdd',12,12)
]
CHI20 = np.array([20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,10,2,2,2,1,1,-1,0,0,-1], dtype=np.int64)


def sha_json(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def fstr(x) -> str:
    return str(sp.Rational(x))


def mul(x, y, modulus):
    z = [0] * 26
    for i, a in enumerate(x):
        if not a % modulus:
            continue
        for j, b in enumerate(y):
            if not b % modulus:
                continue
            for k, c in enumerate(P[i, j]):
                z[k] = (z[k] + a * b * int(c)) % modulus
    return z


def add(x, y, m):
    return [(a + b) % m for a, b in zip(x, y)]


def sub(x, y, m):
    return [(a - b) % m for a, b in zip(x, y)]


def scale(c, x, m):
    return [(c * a) % m for a in x]


def solve_field(A, b, p):
    M = [[int(x) % p for x in row] + [int(bb) % p] for row, bb in zip(A, b)]
    rows, cols, r, piv = len(M), len(M[0]) - 1, 0, []
    for c in range(cols):
        q = next((i for i in range(r, rows) if M[i][c]), None)
        if q is None:
            continue
        M[r], M[q] = M[q], M[r]
        inv = pow(M[r][c], -1, p)
        M[r] = [(inv * x) % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                z = M[i][c]
                M[i] = [(M[i][j] - z * M[r][j]) % p for j in range(cols + 1)]
        piv.append(c)
        r += 1
    for i in range(r, rows):
        assert not (all(M[i][c] == 0 for c in range(cols)) and M[i][cols] != 0)
    x = [0] * cols
    for i, c in enumerate(piv):
        x[c] = M[i][cols]
    return x


def lcm_many(values):
    out = 1
    for value in values:
        out = math.lcm(out, value)
    return out


def primitive_integer_vector(vector):
    den = lcm_many(sp.Rational(x).q for x in vector)
    ints = [int(sp.Rational(x) * den) for x in vector]
    nz = [abs(x) for x in ints if x]
    if not nz:
        return [0] * len(vector)
    common = reduce(gcd, nz)
    ints = [x // common for x in ints]
    first = next(x for x in ints if x)
    if first < 0:
        ints = [-x for x in ints]
    return ints


def span(vectors, p):
    return old.span(vectors, p)


def quotient_record(p):
    return json.loads((DATA / "w33_pass1330_modular_quotient_maps.json").read_text())["records"][str(p)]


def quotient_data(p):
    frozen = quotient_record(p)
    images = []
    for i in range(26):
        row = []
        for block in frozen["matrix_blocks"]:
            row += block["images"][i]
        row += [chi[i] for chi in frozen["scalar_characters"]]
        images.append([int(x) % p for x in row])
    qdim = len(images[0])
    targets = []
    off = 0
    for bi, block in enumerate(frozen["matrix_blocks"]):
        n = block["size"]
        for r in range(n):
            t = [0] * qdim
            t[off + r * n + r] = 1
            targets.append((f"M{n}_{bi}:{r}", t, bi))
        off += n * n
    for si, _ in enumerate(frozen["scalar_characters"]):
        t = [0] * qdim
        t[off + si] = 1
        targets.append((f"F_{si}", t, len(frozen["matrix_blocks"]) + si))
    return frozen, images, targets


def preimage(images, target, p):
    return solve_field([list(x) for x in zip(*images)], target, p)


def left_matrix(x, m):
    return sp.Matrix.hstack(*[sp.Matrix(mul(x, e, m)) for e in BASIS])


def inverse_element(x, m):
    return [int(v) % m for v in left_matrix(x, m).inv_mod(m) * sp.Matrix(ONE)]


def lift_idempotent(x, m):
    for step in range(30):
        err = sub(mul(x, x, m), x, m)
        if not any(err):
            return x, step
        unit = sub(scale(2, x, m), ONE, m)
        x = sub(x, mul(err, inverse_element(unit, m), m), m)
    raise RuntimeError("idempotent Newton lift did not converge")


def orthogonal_primitive_lifts(p, modulus=None):
    _, images, targets = quotient_data(p)
    m = p if modulus is None else modulus
    remainder = ONE[:]
    lifts = []
    for label, target, component in targets:
        x = preimage(images, target, p)
        x = mul(mul(remainder, x, m), remainder, m)
        x, steps = lift_idempotent(x, m)
        assert mul(x, x, m) == x
        for _, f, _, _ in lifts:
            assert not any(mul(x, f, m)) and not any(mul(f, x, m))
        lifts.append((label, x, component, steps))
        remainder = sub(remainder, x, m)
    assert not any(remainder)
    return lifts


def corner_dim(e, f, p):
    return len(span([mul(mul(e, b, p), f, p) for b in BASIS], p))


def left_ideal_dim(e, p):
    return len(span([mul(b, e, p) for b in BASIS], p))


def matrix_unit_change_of_basis():
    columns, labels = [], []
    for name, filename in FILES:
        block = json.loads((DATA / filename).read_text())["block"]["matrix_units"]
        for key, raw in block.items():
            i, j = map(int, key.split(","))
            labels.append((name, i, j))
            columns.append([sp.Rational(x) for x in raw])
    V = sp.Matrix.hstack(*map(sp.Matrix, columns))
    return V, V.inv(), labels


def ordinary_and_modular_traces(p):
    V, W, labels = matrix_unit_change_of_basis()
    ordinary = []
    for name in ORDINARY:
        idx = [k for k, (n, _, _) in enumerate(labels) if n == name]
        ordinary.append([
            int(sum(W[k, r] for k in idx if labels[k][1] == labels[k][2]))
            for r in range(26)
        ])
    rec = quotient_record(p)
    modular = []
    for block in rec["matrix_blocks"]:
        n = block["size"]
        modular.append([
            sum(block["images"][r][i * n + i] for i in range(n)) % p
            for r in range(26)
        ])
    modular += [[int(x) % p for x in chi] for chi in rec["scalar_characters"]]
    return ordinary, modular


def compose_np(a, b):
    return a[b]


def invperm(p):
    q = np.empty_like(p)
    q[p] = np.arange(len(p), dtype=p.dtype)
    return q


def perm_order(p):
    seen = np.zeros(len(p), bool)
    answer = 1
    for i in range(len(p)):
        if not seen[i]:
            j, n = i, 0
            while not seen[j]:
                seen[j] = True
                j = int(p[j])
                n += 1
            answer = math.lcm(answer, n)
    return answer


def ppower(p, n):
    r = np.arange(len(p), dtype=p.dtype)
    b = p
    while n:
        if n & 1:
            r = compose_np(r, b)
        b = compose_np(b, b)
        n //= 2
    return r


def enum_group(gens, toggles):
    identity = np.arange(len(gens[0]), dtype=gens[0].dtype)
    elements = [identity]
    index = {identity.tobytes(): 0}
    parity = [0]
    queue = deque([0])
    while queue:
        i = queue.popleft()
        x = elements[i]
        for k, generator in enumerate(gens):
            y = compose_np(generator, x)
            key = y.tobytes()
            py = parity[i] ^ toggles[k]
            if key not in index:
                index[key] = len(elements)
                elements.append(y.copy())
                parity.append(py)
                queue.append(len(elements) - 1)
            else:
                assert parity[index[key]] == py
    return np.stack(elements), index, np.array(parity, dtype=np.uint8)


def conjugacy_classes(arr, index, gens):
    maps = []
    for generator in gens:
        inverse = invperm(generator)
        conjugates = inverse[arr[:, generator]]
        maps.append(np.array([index[row.tobytes()] for row in conjugates], dtype=np.int32))
    unseen = np.ones(len(arr), bool)
    classes = []
    class_of = np.empty(len(arr), dtype=np.int16)
    for seed in range(len(arr)):
        if not unseen[seed]:
            continue
        unseen[seed] = False
        queue = deque([seed])
        orbit = []
        while queue:
            x = queue.popleft()
            orbit.append(x)
            for transform in maps:
                y = int(transform[x])
                if unseen[y]:
                    unseen[y] = False
                    queue.append(y)
        class_of[orbit] = len(classes)
        classes.append(tuple(orbit))
    return tuple(classes), class_of


def generated_size(gens):
    identity = np.arange(len(gens[0]), dtype=gens[0].dtype)
    seen = {identity.tobytes()}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for generator in gens:
            y = compose_np(generator, x)
            key = y.tobytes()
            if key not in seen:
                seen.add(key)
                queue.append(y)
    return len(seen)


def eval_word(expr, c, d):
    if expr.startswith("("):
        word, n = expr[1:].split(")^")
        n = int(n)
    else:
        word, n = expr, 1
    r = np.arange(len(c), dtype=c.dtype)
    for char in word:
        r = compose_np(r, c if char == "c" else d)
    return ppower(r, n)


def pivot_columns_mod(A, p, count):
    bases, pivots = {}, []
    for j in range(A.shape[1]):
        v = [int(x % p) for x in A[:, j]]
        for r in sorted(bases):
            if v[r]:
                z = v[r]
                v = [(x - z * y) % p for x, y in zip(v, bases[r])]
        if any(v):
            r = next(i for i, x in enumerate(v) if x)
            inv = pow(v[r], -1, p)
            bases[r] = [x * inv % p for x in v]
            pivots.append(j)
            if len(pivots) == count:
                return pivots
    raise RuntimeError("insufficient pivot columns")


def literal_species20_model():
    """Return the exact directed-edge projector, basis, dual, and ATLAS model."""
    points, raw_gens = old.point_model()
    gens = tuple(np.array(x, dtype=np.uint8) for x in raw_gens)
    group, index, parity = enum_group(gens, [0, 0, 0, 0, 0, 1])
    assert len(group) == GROUP_ORDER
    classes, class_of = conjugacy_classes(group, index, gens)
    assert len(classes) == 25
    records = []
    for cl in classes:
        representative = group[cl[0]]
        records.append((perm_order(representative), GROUP_ORDER // len(cl), bool(parity[cl[0]])))
    c_class = next(i for i, (order, centralizer, outer) in enumerate(records) if order == 2 and centralizer == 1440 and outer)
    d_class = next(i for i, (order, centralizer, outer) in enumerate(records) if order == 9 and centralizer == 9 and not outer)
    c = group[classes[c_class][0]]
    d = None
    for index_d in classes[d_class]:
        candidate = group[index_d]
        if perm_order(compose_np(c, candidate)) == 10 and generated_size((c, candidate)) == GROUP_ORDER:
            d = candidate
            break
    assert d is not None
    mapping, atlas_reps = [], []
    for _, word, order, centralizer in ATLAS:
        element = eval_word(word, c, d)
        ci = int(class_of[index[element.tobytes()]])
        assert records[ci][:2] == (order, centralizer)
        mapping.append(ci)
        atlas_reps.append(element)
    assert len(set(mapping)) == 25
    class_to_atlas = {ci: i for i, ci in enumerate(mapping)}
    atlas_of_element = np.array([class_to_atlas[int(class_of[i])] for i in range(GROUP_ORDER)], dtype=np.int8)

    adjacency = np.zeros((40, 40), dtype=np.int8)
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            adjacency[i, j] = int(i != j and old.symp(x, y) == 0)
    directed = [(i, j) for i in range(40) for j in range(40) if adjacency[i, j]]
    assert len(directed) == 480
    lookup = -np.ones((40, 40), dtype=np.int16)
    for k, edge in enumerate(directed):
        lookup[edge] = k
    src = np.array([x for x, _ in directed], dtype=np.int16)
    dst = np.array([y for _, y in directed], dtype=np.int16)

    numerator = np.zeros((480, 480), dtype=np.int64)
    columns = np.arange(480)
    for i, element in enumerate(group):
        value = int(CHI20[int(atlas_of_element[i])])
        if value:
            action = lookup[element[src], element[dst]]
            numerator[action, columns] += 20 * value
    assert np.array_equal(numerator, numerator.T)
    assert np.array_equal(numerator @ numerator, GROUP_ORDER * numerator)
    pivots = pivot_columns_mod(numerator, 1000003, 20)
    U = numerator[:, pivots]
    rows = pivot_columns_mod(U.T, 1000003, 20)
    minor = sp.Matrix(U[rows, :].tolist())
    coordinate_dual = minor.inv() * sp.Matrix(np.eye(480, dtype=np.int64)[rows, :].tolist())
    assert coordinate_dual * sp.Matrix(U.tolist()) == sp.eye(20)

    def afforded(element):
        action = lookup[element[src], element[dst]]
        GU = np.empty_like(U)
        GU[action, :] = U
        matrix = minor.inv() * sp.Matrix(GU[rows, :].tolist())
        assert sp.Matrix(GU.tolist()) == sp.Matrix(U.tolist()) * matrix
        return matrix

    Mc, Md = afforded(c), afforded(d)
    traces = [int(sp.trace(afforded(rep))) for rep in atlas_reps]
    assert traces == CHI20.tolist()
    return {
        "points": points,
        "adjacency": adjacency,
        "directed": directed,
        "lookup": lookup,
        "projector_numerator": numerator,
        "basis": U,
        "coordinate_dual": coordinate_dual,
        "basis_columns": pivots,
        "pivot_rows": rows,
        "standard_matrices": {"c": Mc, "d": Md},
        "class_traces": traces,
    }
