#!/usr/bin/env python3
"""Shared finite Heisenberg bulk utilities for Passes 400--404."""
from __future__ import annotations

from itertools import product
import numpy as np


def vertices(q: int):
    return [(x, y, z) for x in range(q) for y in range(q) for z in range(q)]


def adjacency(q: int) -> np.ndarray:
    verts = vertices(q)
    n = len(verts)
    A = np.zeros((n, n), dtype=np.int64)
    for i, (x, y, z) in enumerate(verts):
        for j in range(i + 1, n):
            xp, yp, zp = verts[j]
            if (x, y) == (xp, yp):
                continue
            if (zp - z - (y * xp - x * yp)) % q == 0:
                A[i, j] = A[j, i] = 1
    return A


def fibre_shift(q: int) -> np.ndarray:
    """Global shift z -> z+1 on every base fibre."""
    n = q**3
    S = np.zeros((n, n), dtype=complex)
    for x, y, z in vertices(q):
        src = (x * q + y) * q + z
        dst = (x * q + y) * q + ((z + 1) % q)
        S[dst, src] = 1
    return S


def fibre_complete(q: int) -> np.ndarray:
    """Disjoint union of K_q on the q^2 central fibres."""
    return np.kron(np.eye(q * q, dtype=np.int64), np.ones((q, q), dtype=np.int64) - np.eye(q, dtype=np.int64))


def reduced_laplacian(q: int) -> np.ndarray:
    A = adjacency(q)
    L = np.diag(A.sum(axis=1)) - A
    return L[:-1, :-1].astype(object)


def matrix_exponential_hermitian(H: np.ndarray, t: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(np.asarray(H, dtype=complex))
    return (vecs * np.exp(-1j * t * vals)) @ vecs.conj().T


def zero_forcing_closure(A: np.ndarray, seeds: set[int]) -> set[int]:
    blue = set(seeds)
    neighbors = [set(np.flatnonzero(A[i]).tolist()) for i in range(A.shape[0])]
    changed = True
    while changed:
        changed = False
        for v in list(blue):
            white = neighbors[v] - blue
            if len(white) == 1:
                blue.add(next(iter(white)))
                changed = True
    return blue
