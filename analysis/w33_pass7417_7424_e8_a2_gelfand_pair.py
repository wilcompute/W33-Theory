#!/usr/bin/env python3
"""Passes 7417--7424: E8 A2 Gelfand-pair / eigenmatrix theorem.

Build the exact 1120-point A2 action of the E8 Weyl group (central -I acts
trivially), compute the stabilizer suborbits, and identify them with the five
relations of Passes 7401--7408. Because the orbital algebra has rank five and
coincides with the already-verified commutative Bose-Mesner algebra, the
permutation representation is multiplicity-free.

The first eigenmatrix is recovered exactly from the integer multiplication
operator A*R_j, without floating point diagonalization.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.combinatorics import Permutation, PermutationGroup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PASS7417_7424_E8_A2_GELFAND_PAIR_results.json"


def build_e8_roots_scaled2():
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                v = [0] * 8
                v[i], v[j] = si, sj
                roots.append(tuple(v))
    for signs in itertools.product((1, -1), repeat=8):
        if sum(s == -1 for s in signs) % 2 == 0:
            roots.append(tuple(signs))
    assert len(roots) == len(set(roots)) == 240
    return roots


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def enumerate_a2(roots):
    ridx = {r: i for i, r in enumerate(roots)}
    blocks = set()
    for i, j in itertools.combinations(range(240), 2):
        if dot(roots[i], roots[j]) != -4:
            continue
        s = add(roots[i], roots[j])
        blocks.add(frozenset((
            i, j, ridx[s],
            ridx[neg(roots[i])], ridx[neg(roots[j])], ridx[neg(s)],
        )))
    blocks = sorted(blocks, key=lambda S: tuple(sorted(S)))
    assert len(blocks) == 1120
    return blocks


def choose_basis(S, roots):
    for i, j in itertools.combinations(sorted(S), 2):
        if dot(roots[i], roots[j]) == -4:
            return i, j
    raise AssertionError


def orthogonality_graph(blocks, roots):
    bases = [choose_basis(S, roots) for S in blocks]
    A = np.zeros((1120, 1120), dtype=np.uint8)
    for i in range(1120):
        ai, bi = bases[i]
        for j in range(i + 1, 1120):
            aj, bj = bases[j]
            if all(dot(roots[x], roots[y]) == 0 for x in (ai, bi) for y in (aj, bj)):
                A[i, j] = A[j, i] = 1
    return A


SIMPLE_ROOTS_SCALED2 = [
    (2,-2,0,0,0,0,0,0),
    (0,2,-2,0,0,0,0,0),
    (0,0,2,-2,0,0,0,0),
    (0,0,0,2,-2,0,0,0),
    (0,0,0,0,2,-2,0,0),
    (0,0,0,0,0,2,2,0),
    (-1,-1,-1,-1,-1,-1,-1,-1),
    (0,0,0,0,0,2,-2,0),
]


def reflect(v, a):
    ds = dot(v, a)
    assert ds % 4 == 0
    c = ds // 4
    return tuple(v[i] - c * a[i] for i in range(8))


def induced_weyl_action(roots, blocks):
    ridx = {r: i for i, r in enumerate(roots)}
    bidx = {S: i for i, S in enumerate(blocks)}
    generators = []
    for a in SIMPLE_ROOTS_SCALED2:
        root_perm = [ridx[reflect(r, a)] for r in roots]
        block_perm = []
        for S in blocks:
            image = frozenset(root_perm[i] for i in S)
            block_perm.append(bidx[image])
        generators.append(Permutation(block_perm))
    return PermutationGroup(generators)


def relation_labels(A):
    C = A.astype(np.int16) @ A.astype(np.int16)
    labels = np.zeros((1120, 1120), dtype=np.int8)
    labels[A.astype(bool)] = 1
    non = (A == 0) & (~np.eye(1120, dtype=bool))
    for idx, mu in enumerate((10, 16, 40), start=2):
        labels[non & (C == mu)] = idx
    valencies = [int(np.sum(labels[0] == k)) for k in range(5)]
    assert valencies == [1,120,648,270,81]
    return labels, valencies


A_MULT_COLUMNS = [
    [0,1,0,0,0],
    [120,2,10,16,40],
    [0,54,70,72,80],
    [0,36,30,32,0],
    [0,27,10,0,0],
]


def exact_first_eigenmatrix():
    M = sp.Matrix(A_MULT_COLUMNS).T
    thetas = [120,20,8,-4,-40]
    rows = []
    for theta in thetas:
        ns = (M.T - theta * sp.eye(5)).nullspace()
        assert len(ns) == 1
        v = ns[0]
        row = [sp.simplify(x / v[0]) for x in v]
        assert all(x.q == 1 for x in row)
        rows.append([int(x) for x in row])
    P = sp.Matrix(rows)
    multiplicities = [1,84,300,700,35]
    valencies = [1,120,648,270,81]
    Mdiag = sp.diag(*multiplicities)
    Kdiag = sp.diag(*valencies)
    assert P.T * Mdiag * P == 1120 * Kdiag
    Q = 1120 * P.inv()
    assert P * Q == Q * P == 1120 * sp.eye(5)
    return rows, multiplicities, [[str(x) for x in Q.row(i)] for i in range(5)]


def main():
    roots = build_e8_roots_scaled2()
    blocks = enumerate_a2(roots)
    A = orthogonality_graph(blocks, roots)
    labels, valencies = relation_labels(A)

    G = induced_weyl_action(roots, blocks)
    effective_order = G.order()
    assert effective_order == 348_364_800  # W(E8)/{+-I}

    H = G.stabilizer(0)
    stabilizer_order = H.order()
    assert stabilizer_order == 311_040

    orbits = H.orbits()
    orbit_sizes = sorted(len(O) for O in orbits)
    assert orbit_sizes == [1,81,120,270,648]
    assert len(orbits) == 5

    # Each stabilizer suborbit is exactly one combinatorial relation class.
    orbit_relation = []
    for O in orbits:
        rels = {int(labels[0, j]) for j in O}
        assert len(rels) == 1
        orbit_relation.append({
            "size": len(O),
            "relation": rels.pop(),
        })
    assert sorted((x["relation"], x["size"]) for x in orbit_relation) == [
        (0,1),(1,120),(2,648),(3,270),(4,81)
    ]

    P, multiplicities, Q = exact_first_eigenmatrix()
    assert sum(multiplicities) == 1120

    result = {
        "schema": "w33.pass7417_7424.e8_a2_gelfand_pair.v1",
        "status": "PASS",
        "passes": "7417-7424",
        "effective_group": {
            "name": "W(E8)/{+-I} on A2 subsystems",
            "order": int(effective_order),
            "degree": 1120,
            "point_stabilizer_order": int(stabilizer_order),
            "rank": len(orbits),
            "subdegrees": orbit_sizes,
        },
        "orbital_identification": orbit_relation,
        "gelfand_pair": {
            "multiplicity_free": True,
            "reason": (
                "The group orbital algebra has rank 5 and its five orbitals are "
                "exactly the five relations of the commutative rank-5 Bose-Mesner "
                "algebra from Pass7401-7408."
            ),
            "irreducible_dimensions": multiplicities,
            "decomposition": "1 + 84 + 300 + 700 + 35 = 1120",
        },
        "association_scheme": {
            "valencies": valencies,
            "first_eigenmatrix_P": P,
            "multiplicities": multiplicities,
            "second_eigenmatrix_Q_as_exact_strings": Q,
            "orthogonality": "P^T diag(m) P = 1120 diag(k), and P Q = Q P = 1120 I",
        },
        "boundary": (
            "The irreducibility claim is for the complex permutation representation "
            "of the effective finite Weyl action. The dimensions agree with classical "
            "W(E8) character degrees; no physical particle assignment is implied."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status":"PASS",
        "effective_order":int(effective_order),
        "stabilizer":int(stabilizer_order),
        "subdegrees":orbit_sizes,
        "irreducibles":multiplicities,
        "P":P,
    }, indent=2))
    return result


if __name__ == "__main__":
    main()
