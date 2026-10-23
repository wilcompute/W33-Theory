#!/usr/bin/env python3
"""Five transvections give explicit logical matrices for W(3,3) CSS [[40,20,4]]_3.

Proof boundary: this certifies an *abstract* encoded Clifford symmetry, not
a local photonic implementation or a quantum universal gate.
"""
from __future__ import annotations
import json
import random
import sys
from pathlib import Path
import numpy as np
try:
    from analysis.w33_20261022_pascal_css_logical_transvection_jordan import (
        normalize, projective_points, rank, rref, right_kernel
    )
except ModuleNotFoundError:  # direct script invocation from analysis/
    from w33_20261022_pascal_css_logical_transvection_jordan import (
        normalize, projective_points, rank, rref, right_kernel
    )

P = 3
DIM = 40
LOGICAL = 20
J = np.array([[0,1,0,0],[-1,0,0,0],
              [0,0,0,1],[0,0,-1,0]], dtype=np.int64)
I4 = np.eye(4, dtype=np.int64)
DIRECTIONS = [I4[i] for i in range(4)] + [I4[0] + I4[2]]


def perm_of_direction(points, direction):
    coords = np.asarray(points, dtype=np.int64)
    lookup = {tuple(v): i for i, v in enumerate(points)}
    images = coords + ((coords @ J @ direction) % P)[:, None] * direction
    return tuple(lookup[normalize(v, P)] for v in images)


def cycle_lengths(perm):
    unseen = set(range(len(perm)))
    lengths = []
    while unseen:
        i = min(unseen)
        j = i
        length = 0
        while j in unseen:
            unseen.remove(j)
            j = perm[j]
            length += 1
        assert j == i
        lengths.append(length)
    return {k: lengths.count(k) for k in sorted(set(lengths))}


def group_order(perms):
    """Exhaustive degree-40 permutation closure, no algebra system needed."""
    identity = tuple(range(DIM))
    seen = {identity}
    queue = [identity]
    for g in queue:
        for h in perms:
            product = tuple(g[h[i]] for i in range(DIM))
            if product not in seen:
                seen.add(product)
                queue.append(product)
    return len(seen)


def invert_mod(matrix, p):
    size = matrix.shape[0]
    assert matrix.shape == (size, size)
    augmented = np.column_stack((matrix, np.eye(size, dtype=np.int64)))
    reduced, pivots = rref(augmented, p)
    assert pivots == list(range(size))
    assert np.array_equal(reduced[:, :size], np.eye(size, dtype=np.int64))
    return reduced[:, size:]


def logical_basis(B):
    C, _ = rref(B, P)
    K = right_kernel(B, P)
    representatives = []
    combined = C.copy()
    for vector in K:
        if rank(np.vstack((combined, vector)), P) > len(combined):
            representatives.append(vector)
            combined = np.vstack((combined, vector))
    Q = np.asarray(representatives, dtype=np.int64)
    assert C.shape == (10, 40) and K.shape == (30, 40)
    assert Q.shape == (20, 40) and combined.shape == (30, 40)
    _, pivots = rref(combined, P)
    inverse = invert_mod(combined[:, pivots], P)
    return C, Q, combined, pivots, inverse


def logical_action(Q, C, combined, pivots, inverse, perm):
    transformed = np.zeros_like(Q)
    transformed[:, list(perm)] = Q
    coeff = transformed[:, pivots] @ inverse % P
    assert np.all((coeff @ combined - transformed) % P == 0)
    return coeff[:, len(C):]


def certify():
    points = projective_points(P)
    X = np.asarray(points, dtype=np.int64)
    B = ((X @ J @ X.T) % P != 0).astype(np.int64)
    assert len(points) == 40 and np.all(B @ B % P == 0)
    C, Q, combined, pivots, inverse = logical_basis(B)
    permutations = [perm_of_direction(points, v) for v in DIRECTIONS]
    for perm in permutations:
        assert np.array_equal(B[np.ix_(perm, perm)], B)
        assert cycle_lengths(perm) == {1: 13, 3: 9}
    orders = [group_order(permutations[:i]) for i in range(1, 6)]
    assert orders == [3, 24, 72, 288, 25920], orders

    generators = [logical_action(Q, C, combined, pivots, inverse, perm)
                  for perm in permutations]
    eye = np.eye(LOGICAL, dtype=np.int64)
    for matrix in generators:
        assert rank(matrix, P) == LOGICAL
        assert np.array_equal(matrix @ matrix @ matrix % P, eye)
        assert rank((matrix-eye) % P, P) == 10

    rng = random.Random(20261022)
    for _ in range(100):
        word = [rng.randrange(5) for _ in range(rng.randrange(1, 31))]
        acted = tuple(range(DIM))
        logical = eye.copy()
        for i in word:
            acted = tuple(permutations[i][acted[j]] for j in range(DIM))
            logical = logical @ generators[i] % P
        expected = logical_action(Q, C, combined, pivots, inverse, acted)
        assert np.array_equal(expected, logical), word

    return {
        "schema": "w33.css.logical_sp43_generators.v1",
        "status": "EXACT_FINITE_VERIFIED_PHYSICAL_IMPLEMENTATION_UNPROVED",
        "code": "[[40,20,4]]_3",
        "C_rank": len(C),
        "Q_dimension": Q.shape[0],
        "generator_vectors": [v.tolist() for v in DIRECTIONS],
        "partial_generator_group_orders": orders,
        "group": "PSp(4,3)",
        "full_group_order": orders[-1],
        "projective_transvection_cycle_profile": {"fixed": 13, "3_cycles": 9},
        "logical_transvection_jordan": {"J1":3,"J2":4,"J3":3},
        "logical_generator_matrices": [m.tolist() for m in generators],
        "random_word_consistency_checks": 100,
        "logical_action_faithful_reason": "PSp(4,3) simple and nontrivial homomorphism",
        "physical_locality_assumed": False,
    }


if __name__ == "__main__":
    result = certify()
    payload = json.dumps(result, indent=2) + "\n"
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
