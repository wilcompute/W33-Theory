#!/usr/bin/env python3
"""Exact cyclotomic certificate for W(3,3) unextendible two-qutrit MUBs.

All arithmetic is in Z[omega], omega^2+omega+1=0, represented by pairs
(a,b) for a+b*omega. No floating-point eigenvalues or external packages.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

P = 3
ZERO = (0, 0)
ONE = (1, 0)
OMEGA = (0, 1)
OMEGA2 = (-1, -1)
POWERS = (ONE, OMEGA, OMEGA2)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[0], -a[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, b):
    x, y = a
    u, v = b
    return (x * u - y * v, x * v + y * u - y * v)


def trace(A):
    out = ZERO
    for i in range(len(A)):
        out = add(out, A[i][i])
    return out


def matrix_product(A, B):
    n = len(A)
    return [[sum_cyclotomic(mul(A[i][k], B[k][j]) for k in range(n))
             for j in range(n)] for i in range(n)]


def sum_cyclotomic(values):
    x = y = 0
    for a, b in values:
        x += a
        y += b
    return (x, y)


def matrix_sum(matrices):
    n = len(matrices[0])
    return [[sum_cyclotomic(M[i][j] for M in matrices) for j in range(n)]
            for i in range(n)]


def matrix_poly_zero(R, coefficient, constant):
    R2 = matrix_product(R, R)
    n = len(R)
    return all(sub(sub(R2[i][j], (coefficient * R[i][j][0],
                                 coefficient * R[i][j][1])),
                       (-constant if i == j else 0, 0)) == ZERO
               for i in range(n) for j in range(n))


def norm(v):
    v = tuple(x % P for x in v)
    a = next((x for x in v if x), None)
    if a is None:
        raise ValueError("zero vector has no projective representative")
    return tuple(x * pow(a, -1, P) % P for x in v)


def symplectic(u, v):
    return (u[0] * v[1] - u[1] * v[0]
            + u[2] * v[3] - u[3] * v[2]) % P


def construct_geometry():
    vectors = list(itertools.product(range(P), repeat=4))
    points = sorted({norm(v) for v in vectors if any(v)})
    lines = set()
    for u, v in itertools.combinations(points, 2):
        if symplectic(u, v):
            continue
        line = tuple(sorted({norm(tuple(a * u[i] + b * v[i] for i in range(4)))
                             for a in range(P) for b in range(P) if a or b}))
        if len(line) == 4:
            lines.add(line)
    lines = sorted(lines)
    assert len(points) == len(lines) == 40
    edges = [(i, j) for i in range(40) for j in range(i + 1, 40)
             if not (set(lines[i]) & set(lines[j]))]
    assert len(edges) == 540
    neighbors = [set() for _ in range(40)]
    for i, j in edges:
        neighbors[i].add(j)
        neighbors[j].add(i)
    return points, lines, edges, neighbors


def maximal_cliques(neighbors):
    result = []

    def rec(R, Pset, X):
        if not Pset and not X:
            result.append(tuple(sorted(R)))
            return
        pivot = max(Pset | X, key=lambda v: len(Pset & neighbors[v])) if Pset | X else None
        todo = sorted(Pset - (neighbors[pivot] if pivot is not None else set()))
        for v in todo:
            rec(R | {v}, Pset & neighbors[v], X & neighbors[v])
            Pset.remove(v)
            X.add(v)
    rec(set(), set(range(40)), set())
    return sorted(result)


V = list(itertools.product(range(3), repeat=2))
PAIR_REPS = [(0, 0)] + [z for z in V if z != (0, 0)
                         and z < tuple(-x % 3 for x in z)]
assert len(PAIR_REPS) == 5
SOURCES = [[PAIR_REPS[0]]] + [[z, tuple(-x % 3 for x in z)]
                               for z in PAIR_REPS[1:]]


def integer_projector_numerator(line):
    """R_L=9 D_L on the 5D swap-even, total-address-zero sector."""
    u, v = line[:2]
    assert symplectic(u, v) == 0
    elements = [tuple((a * u[k] + b * v[k]) % 3 for k in range(4))
                for a in range(3) for b in range(3)]
    assert len(set(elements)) == 9
    M = [[ZERO for _ in range(5)] for _ in range(5)]
    for column, source in enumerate(SOURCES):
        output = {z: ZERO for z in V}
        for aa, bb, cc, dd in elements:
            for z0, z1 in source:
                target = ((z0 + bb) % 3, (z1 + dd) % 3)
                exponent = (2 * aa * z0 + 2 * cc * z1 + aa * bb + cc * dd) % 3
                output[target] = add(output[target], POWERS[exponent])
        assert all(output[z] == output[tuple(-x % 3 for x in z)] for z in V)
        for row, representative in enumerate(PAIR_REPS):
            M[row][column] = output[representative]
    assert trace(M) == (9, 0)
    assert matrix_poly_zero(M, 9, 0)
    return M


def compute():
    pts, lines, disjoint_pairs, neighbors = construct_geometry()
    maxsets = maximal_cliques(neighbors)
    census = Counter(map(len, maxsets))
    assert census == Counter({5: 432, 8: 135, 10: 36}), census
    R = [integer_projector_numerator(line) for line in lines]
    for i, j in disjoint_pairs:
        assert trace(matrix_product(R[i], R[j])) == (9, 0)
    expected = {5: (27, 126, (6, 21), (4, 1)),
                8: (36, 288, (12, 24), (4, 1)),
                10: (0, 0, (18,), (5,))}
    counts = Counter()
    witnesses = {}
    triple_checks = 0
    for subset in maxsets:
        n = len(subset)
        total = matrix_sum([R[i] for i in subset])
        assert trace(total) == (9 * n, 0)
        if n == 10:
            assert all(total[i][j] == ((18, 0) if i == j else ZERO)
                       for i in range(5) for j in range(5))
        else:
            lin, cons = expected[n][:2]
            assert matrix_poly_zero(total, lin, cons)
        if n == 5:
            for i, j, k in itertools.combinations(subset, 3):
                assert trace(matrix_product(matrix_product(R[i], R[j]), R[k])) == (27, 0)
                triple_checks += 1
        counts[n] += 1
        if n not in witnesses:
            witnesses[n] = {"line_indices": list(subset),
                            "sum_numerator_5x5": [[list(z) for z in row] for row in total]}
    assert triple_checks == 4320
    assert counts == census
    exact_spectra = {
        "5": {"eigenvalue_ninths": {"1": 36, "16": 9}, "lower_bound": "1/9"},
        "8": {"eigenvalue_ninths": {"4": 36, "16": 9}, "lower_bound": "4/9"},
        "10": {"eigenvalue_ninths": {"8": 45}, "lower_bound": "8/9"},
    }
    out = {
        "schema": "w33.exact_mub_sym2_block_certificate.v1",
        "status": "PASS_EXACT_Z_OMEGA_EXHAUSTIVE",
        "arithmetic": "Z[omega], omega^2+omega+1=0; signed integer-pair ring only",
        "geometry": {"points": len(pts), "lines": len(lines),
                     "disjoint_context_pairs": len(disjoint_pairs),
                     "maximal_partial_spreads": {str(k): counts[k] for k in sorted(counts)}},
        "decomposition": {"original_symmetric_square_dimension": 45,
                          "center_of_mass_blocks": 9, "block_dimension": 5,
                          "reason": "W(u) tensor W(-u) preserves z+w; diagonal shifts transitively identify all nine s sectors"},
        "integer_polynomials": {
            "5": "R^2 - 27R + 126I = 0; tr(R)=45",
            "8": "R^2 - 36R + 288I = 0; tr(R)=72",
            "10": "R=18I; tr(R)=90",
        },
        "spectra_of_H_on_Sym2": exact_spectra,
        "exact_checks": {"individual_projector_identities": 40,
                         "pairwise_disjoint_overlap_traces": len(disjoint_pairs),
                         "pentad_positive_triple_traces": triple_checks,
                         "all_spread_polynomials": len(maxsets)},
        "representatives": {str(k): v for k, v in witnesses.items()},
        "qualification": "Mathematically exact positivity and strong unextendibility for all Pauli-class maximal partial spreads of sizes 5 and 8. Does not prove a unique physical realization, a noise threshold, or an exact minimum of the pure-state quartic for size 5."
    }
    return out


def main():
    out = compute()
    serialized = json.dumps(out, indent=2, sort_keys=True) + "\n"
    target = Path(__file__).resolve().parents[1] / "data" / "w33_exact_mub_sym2_blocks_20261109.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(serialized, encoding="utf-8")
    print("STATUS", out["status"])
    print("CENSUS", out["geometry"]["maximal_partial_spreads"])
    print("BLOCKS", out["decomposition"])
    print("SPECTRA", out["spectra_of_H_on_Sym2"])
    print("EXACT_CHECKS", out["exact_checks"])
    print("CERT_SHA256", hashlib.sha256(serialized.encode()).hexdigest())
    print("DATA", target)


if __name__ == "__main__":
    main()
