from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

import _selector_five_frontiers_impl as ff
from pass1370_1374 import core, modular_radicals

GOOD = 1_000_003
ROOT = Path(__file__).resolve().parents[2]


def sha(payload) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode()).hexdigest()


def capture():
    return ff.capture_mackey()


def rank_mod(A, p=GOOD) -> int:
    return ff.rank_mod(np.asarray(A, dtype=np.int64), p)


def row_basis(A, p, ncols=None):
    return modular_radicals.rowbasis(np.asarray(A, dtype=np.int64), p, ncols)


def rref_key(A, p):
    A = np.asarray(A, dtype=np.int64) % p
    if A.size == 0:
        return ()
    R, _ = modular_radicals.rref(A, p)
    rows = []
    for row in R:
        if np.any(row):
            rows.append(tuple(int(x) for x in row))
    return tuple(rows)


def factor_kernel_key(factor, p):
    d = factor[0].shape[0]
    equations = []
    for i in range(d):
        for j in range(d):
            equations.append([int(factor[a][i, j]) for a in range(len(factor))])
    K = modular_radicals.nullspace(np.asarray(equations, dtype=np.int64) % p, p)
    return rref_key(K, p)


def product_rows(tensor, X, Y, p):
    if len(X) == 0 or len(Y) == 0:
        return np.zeros((0, tensor.shape[0]), dtype=np.int64)
    return np.einsum("cab,ia,jb->ijc", tensor, X, Y, optimize=True).reshape(-1, tensor.shape[0]) % p


class SparseRank:
    def __init__(self, p: int):
        self.p = p
        self.pivots: dict[int, dict[int, int]] = {}

    def add(self, row: dict[int, int]) -> bool:
        p = self.p
        r = {int(k): int(v) % p for k, v in row.items() if int(v) % p}
        while r:
            c = min(r)
            if c not in self.pivots:
                inv = pow(r[c], -1, p)
                r = {k: v * inv % p for k, v in r.items() if v * inv % p}
                self.pivots[c] = r
                return True
            factor = r[c]
            pivot = self.pivots[c]
            for k, v in pivot.items():
                nv = (r.get(k, 0) - factor * v) % p
                if nv:
                    r[k] = nv
                else:
                    r.pop(k, None)
        return False

    @property
    def rank(self) -> int:
        return len(self.pivots)


def matrix_stats(M):
    M = sp.Matrix(M)
    maxnum = 0
    maxden = 1
    nnz = 0
    payload = []
    for x in M:
        q = sp.Rational(x)
        payload.append([int(q.p), int(q.q)])
        if q:
            nnz += 1
            maxnum = max(maxnum, abs(int(q.p)))
            maxden = max(maxden, int(q.q))
    return {
        "shape": [M.rows, M.cols],
        "nonzero": nnz,
        "max_abs_numerator": maxnum,
        "max_denominator": maxden,
        "sha256": sha(payload),
    }


def add_mod_basis(p, width):
    pivots = {}

    def add(v):
        x = np.asarray(v, dtype=np.int64).copy() % p
        while np.any(x):
            c = int(np.flatnonzero(x)[0])
            if c not in pivots:
                x = x * pow(int(x[c]), -1, p) % p
                pivots[c] = x
                return True
            x = (x - int(x[c]) * pivots[c]) % p
        return False

    def rows():
        return [pivots[k] for k in sorted(pivots)]

    return add, rows


def denominator_lcm(M):
    out = 1
    for x in M:
        out = math.lcm(out, int(sp.Rational(x).q))
    return out
