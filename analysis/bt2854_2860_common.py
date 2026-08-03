#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "data"

MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
MASKS = tuple(range(1, 16))
TAU = (2, 3, 0, 1)
S4_CLASSES = ("1^4", "2,1,1", "2,2", "3,1", "4")
S4_CLASS_SIZES = (1, 6, 3, 8, 6)
S4_IRREPS = {
    "[4]": (1, 1, 1, 1, 1),
    "[31]": (3, 1, -1, 0, -1),
    "[22]": (2, 0, 2, -1, 0),
    "[211]": (3, -1, -1, 0, 1),
    "[1111]": (1, -1, 1, 1, -1),
}


def canon_json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha(obj: object) -> str:
    return hashlib.sha256(canon_json(obj).encode()).hexdigest()


def matmul_mod(a, b, p=3):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b))) % p for j in range(len(b[0])))
        for i in range(len(a))
    )


def transpose(a):
    return tuple(tuple(a[i][j] for i in range(len(a))) for j in range(len(a[0])))


def scalar_mod(c, a, p=3):
    return tuple(tuple(c * x % p for x in row) for row in a)


def permutation_matrix(p):
    out = [[0] * 4 for _ in range(4)]
    for i in range(4):
        out[p[i]][i] = 1
    return tuple(tuple(row) for row in out)


def diagonal(signs):
    return tuple(tuple(signs[i] if i == j else 0 for j in range(4)) for i in range(4))


def j_matrix(matching):
    out = [[0] * 4 for _ in range(4)]
    for a, b in matching:
        out[a][b] = 1
        out[b][a] = 2
    return tuple(tuple(row) for row in out)


def projective_matrix(a):
    flat = [x % 3 for row in a for x in row]
    first = next(x for x in flat if x)
    scale = 1 if first == 1 else 2
    return scalar_mod(scale, a)


def matching_image(p, matching):
    return tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in matching))


def matching_index(matching):
    canonical = tuple(sorted(tuple(sorted(edge)) for edge in matching))
    return {tuple(sorted(tuple(sorted(e)) for e in m)): i for i, m in enumerate(MATCHINGS)}[canonical]


def character_decompose(char, irreps, sizes, order):
    out = {}
    for name, irr in irreps.items():
        mult = sum(s * c * x for s, c, x in zip(sizes, char, irr)) // order
        if mult:
            out[name] = mult
    return out


def gf_rank_vectors(vectors, prime=1_000_003):
    pivots = {}
    for vec in vectors:
        row = {i: int(x) % prime for i, x in enumerate(vec) if int(x) % prime}
        while row:
            c = min(row)
            if c not in pivots:
                inv = pow(row[c], prime - 2, prime)
                pivots[c] = {k: v * inv % prime for k, v in row.items()}
                break
            factor = row[c]
            for k, v in pivots[c].items():
                nv = (row.get(k, 0) - factor * v) % prime
                if nv:
                    row[k] = nv
                elif k in row:
                    del row[k]
    return len(pivots)


def flatten_matrix(m):
    return tuple(x for row in m for x in row)


def mm_int(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def encode_affine(v):
    if not any(v):
        return 0
    mask = sum((v[i] != 0) << i for i in range(4))
    pivot_index = next(i for i, x in enumerate(v) if x)
    pivot = v[pivot_index]
    phase = 0
    slot = 0
    for i in range(pivot_index + 1, 4):
        if v[i]:
            if v[i] != pivot:
                phase |= 1 << slot
            slot += 1
    bases = {1:0,2:1,3:2,4:4,5:5,6:7,7:9,8:13,9:14,10:16,11:18,12:22,13:24,14:28,15:32}
    addr = bases[mask] + phase
    polarity = int(pivot == 2)
    return 1 + 2 * addr + polarity


def decode_affine(code):
    if code == 0:
        return (0, 0, 0, 0)
    addr = (code - 1) // 2
    polarity = (code - 1) & 1
    ranges = [(1,1,0),(2,2,1),(4,3,2),(5,4,4),(7,5,5),(9,6,7),(13,7,9),(14,8,13),(16,9,14),(18,10,16),(22,11,18),(24,12,22),(28,13,24),(32,14,28),(40,15,32)]
    for stop, mask, base in ranges:
        if addr < stop:
            break
    phase = addr - base
    vals = [0, 0, 0, 0]
    pivot = next(i for i in range(4) if mask & (1 << i))
    vals[pivot] = 1
    slot = 0
    for i in range(pivot + 1, 4):
        if mask & (1 << i):
            vals[i] = 2 if (phase >> slot) & 1 else 1
            slot += 1
    if polarity:
        vals = [0 if x == 0 else 3 - x for x in vals]
    return tuple(vals)


def minority_coordinate(word):
    signs = (1,) + tuple(-1 if bit else 1 for bit in word)
    counts = Counter(signs)
    minority_sign = min(counts, key=counts.get)
    inds = [i for i, s in enumerate(signs) if s == minority_sign]
    return inds[0] if len(inds) == 1 else None


def rank_mod(rows, p=1_000_003):
    pivots = {}
    for values in rows:
        row = {i: v % p for i, v in enumerate(values) if v % p}
        while row:
            c = min(row)
            if c not in pivots:
                inv = pow(row[c], p - 2, p)
                pivots[c] = {k: v * inv % p for k, v in row.items()}
                break
            factor = row[c]
            for k, v in pivots[c].items():
                nv = (row.get(k, 0) - factor * v) % p
                if nv:
                    row[k] = nv
                elif k in row:
                    del row[k]
    return len(pivots)


def nonzero_zero_sum(q, r):
    return ((q - 1) ** r + (q - 1) * ((-1) ** r)) // q


def q_entry(q, S, T):
    Sm = {i for i in range(4) if S & (1 << i)}
    Tm = {i for i in range(4) if T & (1 << i)}
    r = len(Tm & {TAU[i] for i in Sm})
    t = len(Tm)
    return (q - 1) ** (t - r) * nonzero_zero_sum(q, r) // (q - 1) - int(S == T)


def fundamental_coefficients(q):
    alpha = Fraction(q * (q * q + q + 2), (q + 1) * (q * q + 1))
    beta = Fraction(q * q, q * q + 1)
    gamma = Fraction(-(q ** 3 + q * q + q - 1), (q + 1) * (q * q + 1))
    return alpha, beta, gamma


def mfpt(q, S, T):
    if S == T:
        return Fraction(0)
    k = q * (q + 1)
    alpha, beta, _ = fundamental_coefficients(q)
    pi_t = Fraction((q - 1) ** (T.bit_count() - 1), (q + 1) * (q * q + 1))
    return (alpha + beta * (Fraction(q_entry(q, T, T), k) - Fraction(q_entry(q, S, T), k))) / pi_t


def matrix_fraction_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matrix_fraction_inv(a):
    return sp.Matrix(a).inv()
