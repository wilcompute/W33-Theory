#!/usr/bin/env python3
"""Pass 10961: exact Albert Cl(9), doubled Cl(10), and clock grade obstruction."""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction as Fr
from math import lcm
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10961_albert_clifford10_doubled_clock.json"
MATS = ROOT / "data/w33_pass10961_albert_clifford9_gammas.json"

_spec = importlib.util.spec_from_file_location(
    "p50", ROOT / "analysis/w33_pass10950_clock_albert_lorentz_spinor.py")
P50 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P50)


def qfrac(x):
    q = sp.Rational(x)
    return Fr(int(q.p), int(q.q))


def rank_mats(mats):
    return P50.rank([
        [qfrac(x) for x in sp.Matrix(M).reshape(M.rows * M.cols, 1)]
        for M in mats
    ])


def strings(M):
    return [[str(sp.simplify(M[i, j])) for j in range(M.cols)]
            for i in range(M.rows)]


def sha_payload(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True).encode("utf-8")
    ).hexdigest()


def main():
    J = P50.build_clock_albert()
    n, prodF = J["n"], J["prod"]
    den = lcm(*[x.denominator for x in prodF.flat])
    Pi = np.array([
        [[int(x * den) for x in prodF[i, j]] for j in range(n)]
        for i in range(n)
    ], dtype=np.int64)

    Ls = np.stack([Pi[i].T for i in range(n)])

    def Lv(x):
        return np.tensordot(np.asarray(x, dtype=np.int64), Ls, axes=1)

    def mulv(x, y):
        return np.asarray(x, dtype=np.int64) @ np.tensordot(
            Pi, np.asarray(y, dtype=np.int64), axes=([1], [0]))

    I27 = np.eye(n, dtype=np.int64)
    idx, frame = J["idx"], J["G"]
    evec = sum(I27[idx[g]] for g in frame)
    cvec = I27[idx[frame[0]]]
    trL = np.array([np.trace(Ls[i]) for i in range(n)])

    Lc = Lv(cvec)
    A0 = P50.nullspace(Lc.tolist())
    Ahalf = P50.nullspace((2 * Lc - den * I27).tolist())
    assert len(A0) == 10 and len(Ahalf) == 16
    A0i = [np.array([
        int(x * lcm(*[y.denominator for y in v])) for x in v
    ], dtype=np.int64) for v in A0]

    Hi = [np.array([
        int(x * lcm(*[y.denominator for y in v])) for x in v
    ], dtype=np.int64) for v in Ahalf]
    uvec = evec - cvec

    def trform(x, y):
        return Fr(
            int(np.dot(trL, mulv(x, y))),
            9 * den * den,
        )

    uu = trform(uvec, uvec)
    spatial = []
    for v in A0i:
        coef = trform(v, uvec) / uu
        w = [Fr(int(a)) - coef * int(b) for a, b in zip(v, uvec)]
        q = lcm(*[x.denominator for x in w])
        spatial.append(np.array(
            [int(x * q) for x in w], dtype=np.int64))
    sp9 = []
    for s in spatial:
        if P50.rank([x.tolist() for x in sp9 + [s]]) > len(sp9):
            sp9.append(s)
    assert len(sp9) == 9

    gram9 = sp.Matrix(9, 9, lambda i, j: sp.Rational(
        trform(sp9[i], sp9[j]).numerator,
        trform(sp9[i], sp9[j]).denominator,
    ))
    assert gram9 == 2 * sp.eye(9)

    Harr = np.stack(Hi).T
    Hmat = sp.Matrix(Harr.tolist())
    Hpinv = (Hmat.T * Hmat).inv() * Hmat.T

    def rep16(M):
        img = sp.Matrix((M @ Harr).tolist())
        R = Hpinv * img
        assert Hmat * R == img
        return R

    gamma9 = [rep16(Lv(s)) for s in sp9]
    I16 = sp.eye(16)
    Z16 = sp.zeros(16, 16)
    for i in range(9):
        for j in range(9):
            lhs = gamma9[i] * gamma9[j] + gamma9[j] * gamma9[i]
            rhs = (2 if i == j else 0) * I16
            assert lhs == rhs

    assert rank_mats([
        gamma9[i] * gamma9[j]
        for i, j in itertools.combinations(range(9), 2)
    ]) == 36

    gamma10 = [
        sp.Matrix.vstack(
            sp.Matrix.hstack(Z16, g),
            sp.Matrix.hstack(g, Z16),
        )
        for g in gamma9
    ]
    Gamma10 = sp.diag(I16, -I16)
    gamma10.append(Gamma10)
    I32 = sp.eye(32)

    for i in range(10):
        for j in range(10):
            lhs = gamma10[i] * gamma10[j] + gamma10[j] * gamma10[i]
            rhs = (2 if i == j else 0) * I32
            assert lhs == rhs

    bivectors = [
        gamma10[i] * gamma10[j]
        for i, j in itertools.combinations(range(10), 2)
    ]
    assert rank_mats(bivectors) == 45

    mixed = [Gamma10 * gamma10[i] for i in range(9)]
    vector_rank = rank_mats(gamma10)
    mixed_rank = rank_mats(mixed)
    union_rank = rank_mats(gamma10 + mixed)
    assert vector_rank == 10 and mixed_rank == 9 and union_rank == 19

    exact = json.loads(
        (ROOT / "data/w33_pass10956_albert_spin8_exact_matrices.json")
        .read_text(encoding="utf-8"))
    U = sp.Matrix([
        [sp.Rational(x) for x in row]
        for row in exact["halfturn_U_equals_R_over_2"]
    ])
    assert U * U == -I16
    Uinv = -U

    C9 = sp.zeros(9, 9)
    for i in range(9):
        image = U * gamma9[i] * Uinv
        for j in range(9):
            C9[j, i] = sp.simplify(
                (gamma9[j] * image).trace() / 16)
        rebuild = sum(
            (C9[j, i] * gamma9[j] for j in range(9)),
            sp.zeros(16, 16))
        assert rebuild == image

    assert C9.T * C9 == sp.eye(9)
    assert C9.det() == 1
    assert C9 * C9 == sp.eye(9)
    assert C9.trace() == 5
    assert C9.eigenvals() == {1: 7, -1: 2}

    zeta8 = (1 + sp.I) / sp.sqrt(2)
    assert sp.simplify(zeta8 ** 2 - sp.I) == 0
    GA = sp.diag((1 / zeta8) * U, zeta8 * U)
    GAinv = sp.diag(-zeta8 * U, -(1 / zeta8) * U)
    assert sp.simplify(GA * GAinv - I32) == sp.zeros(32, 32)
    assert sp.simplify(GA ** 2 - sp.I * Gamma10) == sp.zeros(32, 32)
    assert sp.simplify(GA ** 4 + I32) == sp.zeros(32, 32)
    assert sp.simplify(GA ** 8 - I32) == sp.zeros(32, 32)

    for i in range(9):
        rotated = sum(
            (C9[j, i] * gamma10[j] for j in range(9)),
            sp.zeros(32, 32))
        lhs = sp.simplify(GA * gamma10[i] * GAinv)
        rhs = -sp.I * Gamma10 * rotated
        assert sp.simplify(lhs - rhs) == sp.zeros(32, 32)

    assert sp.simplify(
        GA * Gamma10 * GAinv - Gamma10
    ) == sp.zeros(32, 32)

    clock_image_vectors = [
        sp.simplify(GA * g * GAinv) for g in gamma10
    ]
    rationalized_images = [
        sp.simplify(sp.I * clock_image_vectors[i]) for i in range(9)
    ] + [clock_image_vectors[9]]
    image_union_rank = rank_mats(gamma10 + rationalized_images)
    assert image_union_rank == 19

    G2 = sp.I * Gamma10
    G2inv = -sp.I * Gamma10
    for i in range(9):
        assert sp.simplify(
            G2 * gamma10[i] * G2inv + gamma10[i]
        ) == sp.zeros(32, 32)
    assert sp.simplify(
        G2 * Gamma10 * G2inv - Gamma10
    ) == sp.zeros(32, 32)

    p59 = json.loads(
        (ROOT / "data/w33_pass10959_albert_clock_extension_obstruction.json")
        .read_text(encoding="utf-8"))
    assert p59["minimal_completion"]["doubled_clock"] == (
        "diag(zeta8^-1 U, zeta8 U)")

    mats_payload = {
        "schema": "w33.pass10961.albert-clifford9-gammas.v1",
        "field": "Q",
        "spatial_gram": strings(gram9),
        "gamma9": [strings(g) for g in gamma9],
        "halfturn_vector_action_C9": strings(C9),
    }
    mats_payload["sha256"] = sha_payload({
        "gamma9": mats_payload["gamma9"],
        "C9": mats_payload["halfturn_vector_action_C9"],
    })
    MATS.write_text(
        json.dumps(mats_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    out = {
        "schema": "w33.pass10961.albert-clifford10-doubled-clock.v1",
        "status": "PASS_ALBERT_CL9_CL10_AND_CLOCK_GRADE_OBSTRUCTION",
        "albert_cl9": {
            "spatial_dimension": 9,
            "peirce_spinor_dimension": 16,
            "spatial_gram": "2 I9",
            "gamma_count": 9,
            "clifford_relation": "{gamma_i,gamma_j}=2 delta_ij I16",

            "bivector_span_dimension": 36,
            "reading":
                "the nine spatial Peirce-0 Jordan multiplications are exact Euclidean Cl(9) gamma matrices on the Albert Peirce 16",
        },
        "doubled_cl10": {
            "carrier_dimension": 32,
            "construction":
                "Gamma_i=[[0,gamma_i],[gamma_i,0]] for i=1..9; Gamma_10=diag(I16,-I16)",
            "clifford_relation":
                "{Gamma_a,Gamma_b}=2 delta_ab I32",
            "vector_span_dimension": vector_rank,
            "bivector_span_dimension": 45,
            "mixed_bivectors":
                "M_i=Gamma_10 Gamma_i, i=1..9",
            "vector_plus_mixed_span_dimension": union_rank,
        },
        "spin9_halfturn": {
            "vector_action_dimension": 9,
            "C9_orthogonal": True,
            "C9_determinant": int(C9.det()),
            "C9_trace": int(C9.trace()),
            "C9_spectrum": {"+1": 7, "-1": 2},
            "reading":
                "U is a pi rotation on one spatial 2-plane",
        },

        "doubled_clock_generator": {
            "formula": "G=diag(zeta8^-1 U,zeta8 U)",
            "G_squared": "i Gamma_10",
            "G_fourth": "-I32",
            "G_eighth": "+I32",
            "Gamma10_fixed": True,
            "spatial_grade_action":
                "G Gamma_i G^-1 = -i Gamma_10 sum_j C9[j,i] Gamma_j",
            "one_tick_target_grade":
                "the nine spatial Clifford vectors map into the nine mixed bivectors Gamma_10 Gamma_j",
            "vector_span_plus_image_rank": image_union_rank,
        },
        "clifford_normalizer_obstruction": {
            "full_C8_normalizes_vector_space": False,
            "witness": "the frozen order-eight generator G itself",
            "vector_space_dimension": 10,
            "intersection_dimension_with_one_tick_image": 1,
            "intersection": "span{Gamma_10}",
            "two_ticks_normalize_vector_space": True,
            "two_tick_operator": "G^2=i Gamma_10",
            "two_tick_vector_action":
                "Gamma_i -> -Gamma_i for i=1..9; Gamma_10 -> Gamma_10",
            "two_tick_O10_determinant": -1,
            "four_ticks": "central -I32, trivial by conjugation",
        },

        "parent_welds": {
            "pass10950":
                "the same nine Peirce-0 multiplications were the boost half of the certified so(1,9) action",
            "pass10956":
                "U=R/2 is the exact Spin(9) halfturn with U^2=-I16",
            "pass10959":
                "G is exactly the minimal doubled Albert clock generator used in the faithful 32D GL(2,3) completion",
        },
        "theorem": (
            "The nine spatial Peirce-0 Jordan multiplication operators act on "
            "the Albert Peirce 16 as exact rational Euclidean Cl(9) generators: "
            "their Gram form is 2I9 and their anticommutators are "
            "2 delta_ij I16. Doubling the carrier gives an explicit Cl(10) "
            "Dirac system with 10 vector generators and a 45-dimensional "
            "bivector algebra. For the minimal doubled clock generator "
            "G=diag(zeta8^-1 U,zeta8 U), one tick fixes Gamma_10 but sends "
            "each of the other nine Clifford vectors to -i times a mixed "
            "bivector Gamma_10 Gamma_j, rotated by the exact Spin(9) halfturn "
            "matrix C9. Hence the full order-eight clock is not contained in "
            "the Clifford vector normalizer for this canonical Albert Cl(10) "
            "extension. Two ticks equal i Gamma_10 and do normalize the vector "
            "space, acting by -1 on the nine spatial vectors and +1 on Gamma_10."
        ),

        "boundary": (
            "This is an exact Clifford/representation theorem for the canonical "
            "Cl(10) extension reconstructed from the executable Albert algebra. "
            "It rules out identifying the full doubled order-eight clock with "
            "a Spin(10) or Pin(10) vector normalizer in this extension. It does "
            "not rule out a different larger Clifford module, a grade-mixing "
            "Clifford-algebra automorphism, a projective/semilinear realization, "
            "or a separate physical Spin(10) embedding."
        ),
    }
    OUT.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": out["status"],
        "gamma9": 9,
        "cl10_bivectors": 45,
        "one_tick_vector_plus_image_rank": image_union_rank,
        "G2": out["doubled_clock_generator"]["G_squared"],
        "C9_spectrum": out["spin9_halfturn"]["C9_spectrum"],
    }, indent=2))


if __name__ == "__main__":
    main()
