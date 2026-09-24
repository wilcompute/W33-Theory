#!/usr/bin/env python3
"""Pass 409: exact ramification audit for the cubic Jacobi centroid field."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass409_cubic_ramification_audit.json"
x = sp.symbols("x")
F = x**3 - x**2 - 53*x - 120


def rank_mod(matrix, p):
    a = [[int(v) % p for v in row] for row in matrix]
    rank = 0
    for column in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][column], -1, p)
        a[rank] = [(v*inv) % p for v in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][column]:
                scale = a[i][column]
                a[i] = [(u-scale*v) % p for u, v in zip(a[i], a[rank])]
        rank += 1
    return rank


def multiply(a, b, p):
    values = [0]*5
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            values[i+j] = (values[i+j] + u*v) % p
    for degree in (4, 3):
        coefficient = values[degree] % p
        values[degree] = 0
        values[degree-1] = (values[degree-1] + coefficient) % p
        values[degree-2] = (values[degree-2] + 53*coefficient) % p
        values[degree-3] = (values[degree-3] + 120*coefficient) % p
    return values[:3]


def multiplication_matrix(a, p):
    columns = [multiply(a, basis, p) for basis in ([1,0,0], [0,1,0], [0,0,1])]
    return [[columns[j][i] for j in range(3)] for i in range(3)]


def solve3(matrix, rhs, p):
    augmented = [[int(v) % p for v in row] + [int(r) % p] for row, r in zip(matrix, rhs)]
    for column in range(3):
        pivot = next(i for i in range(column, 3) if augmented[i][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inv = pow(augmented[column][column], -1, p)
        augmented[column] = [(v*inv) % p for v in augmented[column]]
        for i in range(3):
            if i != column and augmented[i][column]:
                scale = augmented[i][column]
                augmented[i] = [(u-scale*v) % p for u, v in zip(augmented[i], augmented[column])]
    return [augmented[i][3] for i in range(3)]


def local_audit(p, trace_gram):
    roots = [r for r in range(p) if int(F.subs(x, r)) % p == 0]
    repeated = [r for r in roots if int(sp.diff(F, x).subs(x, r)) % p == 0]
    assert len(repeated) == 1 and len(set(roots)) == 2
    r = repeated[0]
    s = next(value for value in roots if value != r)
    # CRT idempotent e for the double factor: e(r)=1, e'(r)=0, e(s)=0.
    idempotent = solve3(
        [[1, r, r*r], [0, 1, 2*r], [1, s, s*s]],
        [1, 0, 0], p,
    )
    epsilon = multiply(idempotent, [(-r) % p, 1, 0], p)
    epsilon_matrix = multiplication_matrix(epsilon, p)
    assert epsilon != [0,0,0]
    assert multiply(epsilon, epsilon, p) == [0,0,0]
    assert rank_mod(epsilon_matrix, p) == 1
    trace_rank = rank_mod(trace_gram, p)
    assert trace_rank == 2
    return {
        "prime": p,
        "factorization": f"(x-{r})^2 (x-{s}) over F_{p}",
        "double_root": r,
        "simple_root": s,
        "centroid_algebra": f"F_{p}[epsilon]/(epsilon^2) x F_{p}",
        "double_factor_idempotent_coefficients": idempotent,
        "square_zero_epsilon_coefficients": epsilon,
        "epsilon_multiplication_rank": 1,
        "trace_form_rank": trace_rank,
        "levi_reduction_dimension": 9,
        "levi_killing_rank": 3*trace_rank,
        "levi_nilpotent_ideal": "epsilon*sl2, dimension 3, abelian and square-zero",
        "reduced_semisimple_quotient": "sl2(F_p) + sl2(F_p), dimension 6",
    }


def main(write=True):
    polynomial = sp.Poly(F, x)
    discriminant = int(sp.discriminant(F, x))
    assert polynomial.is_irreducible
    assert discriminant == 94557
    assert sp.factorint(discriminant) == {3: 1, 43: 1, 733: 1}

    companion = sp.zeros(3)
    # Columns are multiplication by alpha on 1,alpha,alpha^2.
    companion[:, 0] = sp.Matrix([0,1,0])
    companion[:, 1] = sp.Matrix([0,0,1])
    companion[:, 2] = sp.Matrix([120,53,1])
    trace_gram = sp.Matrix([
        [sp.trace(companion**(i+j)) for j in range(3)]
        for i in range(3)
    ])
    assert int(trace_gram.det()) == discriminant
    assert all((discriminant // p) % p for p in (3,43,733))

    ramified = [local_audit(p, trace_gram.tolist()) for p in (3,43,733)]
    controls = {}
    for p in (103, 107, 109, 151):
        factorization = sp.factor(F, modulus=p)
        controls[str(p)] = {
            "factorization": str(factorization),
            "trace_form_rank": rank_mod(trace_gram.tolist(), p),
            "etale": rank_mod(trace_gram.tolist(), p) == 3,
        }
        assert controls[str(p)]["etale"]
    assert len(sp.nroots(F)) == 3 and all(abs(complex(root).imag) < 1e-12 for root in sp.nroots(F))

    out = {
        "schema": "w33.pass409.cubic_ramification_audit.v1",
        "status": "PASS_RAMIFIED_PRIMES_ARE_EXACT_TRIALITY_BRANCH_LOCUS",
        "field": {
            "polynomial": "x^3 - x^2 - 53*x - 120",
            "irreducible": True,
            "signature": [3, 0],
            "discriminant": discriminant,
            "discriminant_factorization": {"3": 1, "43": 1, "733": 1},
            "maximal_order": "Z[alpha]; squarefree polynomial discriminant forces index one",
            "galois_closure_group": "S3, since the irreducible cubic discriminant is not a square",
            "triality_action": "The S3 Galois group permutes the three A1 factors after splitting, matching the abstract D4 outer-triality permutation.",
            "integral_trace_gram": [[int(v) for v in row] for row in trace_gram.tolist()],
        },
        "ramified_reductions": ramified,
        "good_prime_controls": controls,
        "computational_interpretation": {
            "generic": "At an unramified prime the centroid is etale and the three A1 channels remain separable after a splitting extension.",
            "branch_locus": "At 3,43,733 two embeddings collide. The collided component is the dual-number algebra F_p[epsilon]/epsilon^2, creating one exact square-zero tangent or derivative lane.",
            "virtual_machine": "The induced operator N=multiplication by epsilon on sl2(A_p) has rank 3 and N^2=0. It supplies a mathematically canonical infinitesimal-update register at precisely the ramified primes.",
            "qutrit_prime_3": "Characteristic 3 is simultaneously the native H27 coefficient field, an E8 bad prime, and a centroid ramification prime. Mod-3 execution therefore conflates triality channels and must not be used to certify characteristic-zero semisimplicity.",
        },
        "repo_collision_audit": {
            "43": "The corpus contains unrelated uses of 43, including Heegner and schedule indices, but no objectwise map to this centroid ramification was found.",
            "733": "The corpus contains BT/pass labels and hashes involving 733, but no prior arithmetic carrier for the centroid prime was found.",
            "policy": "No phenomenological or anomaly identification is promoted from a shared integer alone.",
        },
        "theorem": "The exact primes 3,43,733 are not numerology: they are the complete branch locus of the cubic descent that glues the three A1 triality factors. At each one the 9D Levi reduction acquires a canonical 3D square-zero ideal and Killing rank drops from 9 to 6.",
        "boundary": "Ramification and square-zero tangent channels are exact arithmetic facts. They do not by themselves represent particle generations, gauge anomalies, measured resonances, energy scales, or error thresholds.",
        "parents": [
            "data/w33_pass409_jacobi_d4_identification.json",
            "data/w33_20260923_cubic_jacobi_residual.json",
        ],
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
