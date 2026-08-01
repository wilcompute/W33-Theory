#!/usr/bin/env python3
"""Passes 1861-1865: exceptional-S6 outer doily transfer clock.

Build the 15x15 syntheme/duad incidence matrix D and the exact Pass-1859
exceptional-S6 permutation matrix P.  The outer transfer operator

    T = P^T D

acts on the 15-dimensional duad lattice.  This file verifies its exact
integral, spectral, twisted-equivariant, and eight-step clock structure.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

PASS1859_DUAD_TO_SYNTHEME = (8, 12, 4, 0, 10, 3, 2, 9, 14, 11, 7, 1, 13, 6, 5)
PASS1859_OUTER_IMAGES = (
    (3, 5, 4, 0, 2, 1),
    (2, 3, 0, 1, 5, 4),
    (4, 5, 3, 2, 0, 1),
    (5, 3, 4, 1, 2, 0),
    (2, 5, 0, 4, 3, 1),
)


def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    a = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        b = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for matching in perfect_matchings(rest):
            out.append(tuple(sorted(((min(a, b), max(a, b)),) + matching)))
    return tuple(sorted(set(out)))


def permutation_matrix(image: tuple[int, ...]) -> sp.Matrix:
    # Column j is sent to row image[j].
    n = len(image)
    matrix = sp.zeros(n)
    for j, i in enumerate(image):
        matrix[i, j] = 1
    return matrix


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Composition p o q (apply q first)."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    q = [0] * len(p)
    for i, j in enumerate(p):
        q[j] = i
    return tuple(q)


def cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    sizes = []
    for i in range(len(p)):
        if i in seen:
            continue
        j = i
        size = 0
        while j not in seen:
            seen.add(j)
            size += 1
            j = p[j]
        if size > 1:
            sizes.append(size)
    return tuple(sorted(sizes, reverse=True))


def induced_action_on_duads(p: tuple[int, ...], duads: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    index = {duad: i for i, duad in enumerate(duads)}
    return tuple(index[tuple(sorted((p[a], p[b])))] for a, b in duads)


def generate_outer_automorphism() -> tuple[
    dict[tuple[int, ...], tuple[int, ...]], tuple[tuple[int, ...], ...]
]:
    ident = tuple(range(6))
    adjacent = []
    for i in range(5):
        s = list(range(6))
        s[i], s[i + 1] = s[i + 1], s[i]
        adjacent.append(tuple(s))
    mapping = {ident: ident}
    queue = deque([ident])
    while queue:
        g = queue.popleft()
        alpha_g = mapping[g]
        for s, outer_s in zip(adjacent, PASS1859_OUTER_IMAGES):
            h = compose(s, g)
            alpha_h = compose(outer_s, alpha_g)
            if h in mapping:
                assert mapping[h] == alpha_h
            else:
                mapping[h] = alpha_h
                queue.append(h)
    assert len(mapping) == 720
    return mapping, tuple(adjacent)


def matrix_rank_mod2(matrix: sp.Matrix) -> int:
    rows = [[int(matrix[i, j]) & 1 for j in range(matrix.cols)] for i in range(matrix.rows)]
    rank = 0
    for col in range(matrix.cols):
        pivot = next((r for r in range(rank, matrix.rows) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(matrix.rows):
            if row != rank and rows[row][col]:
                rows[row] = [a ^ b for a, b in zip(rows[row], rows[rank])]
        rank += 1
        if rank == matrix.rows:
            break
    return rank


def matrix_to_rows(matrix: sp.Matrix) -> list[list[int]]:
    return [[int(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def main(output: Path | None = None) -> dict:
    vertices = tuple(range(6))
    duads = tuple(itertools.combinations(vertices, 2))
    synthemes = perfect_matchings(vertices)
    assert len(duads) == len(synthemes) == 15

    duad_index = {duad: i for i, duad in enumerate(duads)}
    incidence = sp.zeros(15)
    for row, syntheme in enumerate(synthemes):
        for duad in syntheme:
            incidence[row, duad_index[duad]] = 1

    outer_identification = permutation_matrix(PASS1859_DUAD_TO_SYNTHEME)
    transfer = outer_identification.T * incidence
    identity = sp.eye(15)
    all_ones = sp.ones(15)

    # Pass 1861: exact integral outer-transfer operator.
    x = sp.symbols("x")
    charpoly = sp.factor(transfer.charpoly(x).as_expr())
    expected_charpoly = x**5 * (x - 3) * (x - 2) * (x + 2) ** 2 * (x**2 + 4) * (x**4 + 16)
    minpoly_identity = transfer * (transfer - 3 * identity) * (transfer**8 - 256 * identity)
    snf = smith_normal_form(transfer, domain=ZZ)
    snf_nonzero = [abs(int(snf[i, i])) for i in range(15) if snf[i, i] != 0]

    # Pass 1862: exact 8-step clock on the balanced image.
    clock_integer_identity = (
        (transfer**8 - 256 * identity) * transfer
        - (3**8 - 256) * (all_ones * transfer) / 15
    )
    clock_integer_rhs = sp.Rational(3**8 - 256, 5) * all_ones
    clock_integer_lhs = (transfer**8 - 256 * identity) * transfer

    traces = {n: int(sp.trace(transfer**n)) for n in range(1, 17)}
    trace_formula = {
        n: 3**n + (-2) ** n + (8 * 2**n if n % 8 == 0 else 0)
        for n in range(1, 17)
    }

    # Pass 1863: twisted equivariance and square of the exceptional automorphism.
    alpha, adjacent = generate_outer_automorphism()
    alpha_inverse = {alpha_g: g for g, alpha_g in alpha.items()}
    twisted_checks = []
    for g in adjacent:
        rho_duad = permutation_matrix(induced_action_on_duads(g, duads))
        alpha_inverse_g = alpha_inverse[g]
        rho_outer_inverse = permutation_matrix(induced_action_on_duads(alpha_inverse_g, duads))
        twisted_checks.append(transfer * rho_duad == rho_outer_inverse * transfer)

    alpha_squared = {g: alpha[alpha[g]] for g in alpha}
    inner_candidates = []
    for h in alpha:
        h_inverse = inverse(h)
        if all(alpha_squared[s] == compose(compose(h, s), h_inverse) for s in adjacent):
            inner_candidates.append(h)
    assert len(inner_candidates) == 1
    inner_h = inner_candidates[0]

    # Pass 1864: doily Gram/singular spectrum and closed-walk law.
    gram = transfer.T * transfer
    point_adjacency = gram - 3 * identity
    point_adjacency_poly = (
        (point_adjacency - 6 * identity)
        * (point_adjacency - identity)
        * (point_adjacency + 3 * identity)
    )
    # SRG(15,6,1,3): A^2=3I-2A+3J.
    srg_identity = point_adjacency**2 - (
        3 * identity - 2 * point_adjacency + 3 * all_ones
    )
    gram_charpoly = sp.factor(gram.charpoly(x).as_expr())

    checks = {
        "duads_15": len(duads) == 15,
        "synthemes_15": len(synthemes) == 15,
        "incidence_row_col_sum_3": all(sum(incidence.row(i)) == 3 for i in range(15))
        and all(sum(incidence.col(j)) == 3 for j in range(15)),
        "pass1859_permutation_matrix": outer_identification.det() == -1
        and outer_identification.T * outer_identification == identity,
        "outer_transfer_integral_01": all(value in (0, 1) for value in transfer),
        "outer_transfer_row_col_sum_3": all(sum(transfer.row(i)) == 3 for i in range(15))
        and all(sum(transfer.col(j)) == 3 for j in range(15)),
        "rank_10": transfer.rank() == 10,
        "kernel_5": len(transfer.nullspace()) == 5,
        "charpoly_exact": sp.expand(charpoly - expected_charpoly) == 0,
        "minimal_polynomial_identity": minpoly_identity == sp.zeros(15),
        "diagonalizable_at_minus2": 15 - (transfer + 2 * identity).rank() == 2,
        "snf_saturated_rank10": snf_nonzero == [1] * 10,
        "clock_integer_identity": clock_integer_lhs == clock_integer_rhs,
        "clock_projected_identity": clock_integer_identity == sp.zeros(15),
        "trace_formula_n1_to16": traces == trace_formula,
        "twisted_equivariance_generators": all(twisted_checks),
        "outer_map_order720": len(alpha) == 720,
        "alpha_square_unique_inner": len(inner_candidates) == 1,
        "alpha_square_inner_cycle_type_4_2": cycle_type(inner_h) == (4, 2),
        "gram_exact": gram == incidence.T * incidence,
        "gram_charpoly_9_4_0": gram_charpoly == x**5 * (x - 4) ** 9 * (x - 9),
        "doily_srg_identity": srg_identity == sp.zeros(15),
        "doily_adjacency_annihilator": point_adjacency_poly == sp.zeros(15),
        "binary_rank_10": matrix_rank_mod2(transfer) == 10,
    }
    assert all(checks.values()), {key: value for key, value in checks.items() if not value}

    result = {
        "schema": "w33.pass1861_1865.outer_doily_transfer_clock.v1",
        "status": "PASS",
        "theorem": (
            "For the Pass-1859 exceptional S6 identification P and the 15x15 "
            "syntheme-duad incidence matrix D, T=P^T D has rank 10, saturated "
            "integral image, characteristic polynomial x^5(x-3)(x-2)(x+2)^2"
            "(x^2+4)(x^4+16), and minimal polynomial x(x-3)(x^8-256). "
            "On the 9-dimensional balanced nonzero image, (T/2)^8=I."
        ),
        "boundary": (
            "T is a finite outer-twisted incidence operator on the S6 doily. "
            "The eight-step phase clock is an exact representation-theoretic "
            "statement; no physical time evolution or continuum dynamics is inferred."
        ),
        "duads": [list(duad) for duad in duads],
        "synthemes": [[list(duad) for duad in syntheme] for syntheme in synthemes],
        "pass1859_duad_to_syntheme": list(PASS1859_DUAD_TO_SYNTHEME),
        "outer_transfer_matrix": matrix_to_rows(transfer),
        "rank": transfer.rank(),
        "nullity": 15 - transfer.rank(),
        "rank_mod2": matrix_rank_mod2(transfer),
        "smith_nonzero": snf_nonzero,
        "characteristic_polynomial": "x^5 (x-3) (x-2) (x+2)^2 (x^2+4) (x^4+16)",
        "minimal_polynomial": "x (x-3) (x^8-256)",
        "balanced_clock": "(T/2)^8 = I on im(T) intersect 1^perp (dimension 9)",
        "trace_formula": "tr(T^n)=3^n+(-2)^n+8*2^n*[8 divides n]",
        "traces_1_to_16": traces,
        "alpha_square_inner_conjugator": list(inner_h),
        "alpha_square_inner_cycle_type": list(cycle_type(inner_h)),
        "gram_spectrum": "9^1 + 4^9 + 0^5",
        "doily_point_graph": "SRG(15,6,1,3)",
        "checks": checks,
        "n_checks": len(checks),
        "n_verified": sum(bool(value) for value in checks.values()),
    }
    canonical = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["sha256_without_hash_field"] = hashlib.sha256(canonical.encode()).hexdigest()
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    output_path = Path("data/w33_pass1861_1865_outer_doily_transfer_clock.json")
    result = main(output_path)
    print(
        json.dumps(
            {
                "status": result["status"],
                "n_verified": result["n_verified"],
                "n_checks": result["n_checks"],
                "rank": result["rank"],
                "rank_mod2": result["rank_mod2"],
                "characteristic_polynomial": result["characteristic_polynomial"],
                "balanced_clock": result["balanced_clock"],
            },
            indent=2,
        )
    )
