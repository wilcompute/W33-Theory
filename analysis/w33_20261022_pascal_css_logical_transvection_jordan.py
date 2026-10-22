#!/usr/bin/env python3
"""Pascal-CSS logical transvection Jordan census on W(3,p), prime p.

This is a finite-field calculation, NOT a general-prime Jordan proof.
All matrix operations, including quotient ranks, are modulo p.
"""
from __future__ import annotations

import itertools
import json
from math import comb

import numpy as np


def rref(matrix: np.ndarray, p: int):
    a = np.asarray(matrix, dtype=np.int64).copy() % p
    pivots = []
    row = 0
    for col in range(a.shape[1]):
        if row == a.shape[0]:
            break
        candidate = next((i for i in range(row, a.shape[0]) if a[i, col]), None)
        if candidate is None:
            continue
        a[[row, candidate]] = a[[candidate, row]]
        a[row] = a[row] * pow(int(a[row, col]), -1, p) % p
        for i in range(a.shape[0]):
            if i != row and a[i, col]:
                a[i] = (a[i] - a[i, col] * a[row]) % p
        pivots.append(col)
        row += 1
    return a[:row], pivots


def rank(matrix: np.ndarray, p: int) -> int:
    return len(rref(matrix, p)[1])


def right_kernel(matrix: np.ndarray, p: int) -> np.ndarray:
    reduced, pivots = rref(matrix, p)
    free = [j for j in range(matrix.shape[1]) if j not in pivots]
    basis = []
    for f in free:
        x = np.zeros(matrix.shape[1], dtype=np.int64)
        x[f] = 1
        for i, j in enumerate(pivots):
            x[j] = (-reduced[i, f]) % p
        basis.append(x)
    return np.asarray(basis, dtype=np.int64)


def normalize(vector, p: int):
    x = np.asarray(vector, dtype=np.int64) % p
    first = next(i for i, z in enumerate(x) if z)
    return tuple(int(z) for z in x * pow(int(x[first]), -1, p) % p)


def projective_points(p: int):
    return sorted({normalize(x, p) for x in itertools.product(range(p), repeat=4)
                   if any(x)})


def predicted_blocks(p: int):
    prediction = {1: 3}
    prediction.update({j: 2 * j for j in range(2, p)})
    prediction[p] = p
    return prediction


def census(p: int) -> dict:
    assert p in (2, 3, 5, 7), "Certified runtime sizes: p=2,3,5,7"
    points = projective_points(p)
    coords = np.asarray(points, dtype=np.int64)
    count = len(points)
    index = {x: i for i, x in enumerate(points)}
    J = np.array([[0,1,0,0],[-1,0,0,0],
                  [0,0,0,1],[0,0,-1,0]], dtype=np.int64)
    B = ((coords @ J @ coords.T) % p != 0).astype(np.int64)
    C, _ = rref(B, p)
    N = right_kernel(B, p)
    assert np.all((B @ B) % p == 0)
    assert count == (p + 1) * (p*p + 1)
    assert len(C) == comb(p + 2, 3)
    assert len(N) == count - len(C)

    # x -> x + <x,w>w is a symplectic transvection.
    w = coords[0]
    images = coords + ((coords @ J @ w) % p)[:, None] * w[None, :]
    permutation = [index[normalize(x, p)] for x in images]
    assert len(set(permutation)) == count
    assert np.array_equal(B[np.ix_(permutation, permutation)], B)
    P = np.zeros((count, count), dtype=np.int64)
    P[np.arange(count), permutation] = 1
    D = (P - np.eye(count, dtype=np.int64)) % p

    # Q = C^perp/C.  Rank(D^k|Q) is rank([C; (ker B)D^k])-rank(C).
    ranks = [count - 2 * len(C)]
    transformed = N.copy()
    for _ in range(p):
        transformed = transformed @ D % p
        ranks.append(rank(np.vstack((C, transformed)), p) - len(C))
    assert ranks[-1] == 0
    blocks = {j: ranks[j-1] - 2*ranks[j] + ranks[j+1]
              for j in range(1, p)}
    blocks[p] = ranks[p-1]
    assert sum(j*m for j, m in blocks.items()) == ranks[0]

    # Verify the polynomial-evaluation model independently for small p.
    polynomial_rank = None
    if p <= 5:
        exponents = [e for e in itertools.product(range(p), repeat=4)
                     if sum(e) == p - 1]
        values = np.asarray(
            [[int(np.prod([pow(int(x), int(e), p)
                            for x, e in zip(v, alpha)]) % p)
              for v in points] for alpha in exponents],
            dtype=np.int64)
        polynomial_rank = rank(values, p)
        assert polynomial_rank == len(C)

    return {
        "p": p, "n": count, "rank_B": len(C),
        "logical_dimension": ranks[0],
        "rank_powers_T_minus_I_on_Q": ranks,
        "Jordan_blocks": blocks,
        "predicted_pattern_matches": blocks == predicted_blocks(p),
        "homogeneous_degree_p_minus_1_rank": polynomial_rank,
        "status": "FINITE_VERIFIED_GENERAL_FORMULA_CONJECTURAL",
    }


def main():
    results = [census(p) for p in (2, 3, 5, 7)]
    assert all(item["predicted_pattern_matches"] for item in results)
    print(json.dumps({"results": results}, indent=2))


if __name__ == "__main__":
    main()
