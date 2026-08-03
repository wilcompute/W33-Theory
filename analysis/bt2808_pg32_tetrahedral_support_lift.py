#!/usr/bin/env python3
"""Pass 2808: exact PG(3,2) tetrahedral support lift into W(3,3).

This verifier closes the open W33-lift boundary recorded in BT805.  It uses
only exact finite arithmetic (SymPy is used for characteristic polynomials).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json"


def canonical_projective(vector: Iterable[int], q: int) -> tuple[int, ...]:
    v = tuple(int(x) % q for x in vector)
    if not any(v):
        raise ValueError("zero vector has no projective class")
    first = next(x for x in v if x)
    inv = pow(first, -1, q)
    return tuple((x * inv) % q for x in v)


def projective_points(q: int, dimension: int = 4) -> list[tuple[int, ...]]:
    return sorted(
        {
            canonical_projective(v, q)
            for v in itertools.product(range(q), repeat=dimension)
            if any(v)
        }
    )


def support_mask(v: Iterable[int]) -> int:
    mask = 0
    for i, value in enumerate(v):
        if int(value) != 0:
            mask |= 1 << i
    return mask


def bitstring(mask: int) -> str:
    return format(mask, "04b")


def role(mask: int) -> str:
    return {1: "vertex", 2: "edge", 3: "face", 4: "body"}[mask.bit_count()]


def pg32_lines() -> list[tuple[int, int, int]]:
    lines = {
        tuple(sorted((a, b, a ^ b)))
        for a, b in itertools.combinations(range(1, 16), 2)
    }
    return sorted(lines)


def pg32_planes() -> list[tuple[int, ...]]:
    planes = []
    for normal in range(1, 16):
        points = tuple(
            x
            for x in range(1, 16)
            if ((normal & x).bit_count() % 2) == 0
        )
        planes.append(points)
    return sorted(planes)


def matchings() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    out = set()
    for p in itertools.permutations(range(4)):
        pairs = tuple(
            sorted(
                (
                    tuple(sorted((p[0], p[1]))),
                    tuple(sorted((p[2], p[3]))),
                )
            )
        )
        out.add(pairs)
    return sorted(out)


def pairing_involution(matching: tuple[tuple[int, int], tuple[int, int]]) -> dict[int, int]:
    tau: dict[int, int] = {}
    for a, b in matching:
        tau[a] = b
        tau[b] = a
    return tau


def symplectic_product(
    u: tuple[int, ...],
    v: tuple[int, ...],
    matching: tuple[tuple[int, int], tuple[int, int]],
    q: int = 3,
) -> int:
    return sum(u[a] * v[b] - u[b] * v[a] for a, b in matching) % q


def w33_adjacency(
    points: list[tuple[int, ...]],
    matching: tuple[tuple[int, int], tuple[int, int]],
) -> sp.Matrix:
    n = len(points)
    return sp.Matrix(
        n,
        n,
        lambda i, j: int(
            i != j and symplectic_product(points[i], points[j], matching) == 0
        ),
    )


def quotient_matrix(
    adjacency: sp.Matrix,
    fibers: dict[int, list[int]],
) -> tuple[sp.Matrix, bool]:
    masks = list(range(1, 16))
    quotient = sp.zeros(15)
    equitable = True
    for i, source_mask in enumerate(masks):
        profiles = []
        for source in fibers[source_mask]:
            profiles.append(
                tuple(
                    sum(int(adjacency[source, target]) for target in fibers[target_mask])
                    for target_mask in masks
                )
            )
        if len(set(profiles)) != 1:
            equitable = False
        for j, value in enumerate(profiles[0]):
            quotient[i, j] = value
    return quotient, equitable


def zero_sum_sign_count(r: int) -> int:
    return sum(
        1
        for signs in itertools.product((1, -1), repeat=r)
        if sum(signs) % 3 == 0
    )


def closed_quotient_entry(
    source_mask: int,
    target_mask: int,
    matching: tuple[tuple[int, int], tuple[int, int]],
) -> int:
    tau = pairing_involution(matching)
    tau_source = 0
    for i in range(4):
        if source_mask & (1 << i):
            tau_source |= 1 << tau[i]
    target_weight = target_mask.bit_count()
    overlap = (target_mask & tau_source).bit_count()
    numerator = (2 ** (target_weight - overlap)) * zero_sum_sign_count(overlap)
    assert numerator % 2 == 0
    return numerator // 2 - int(source_mask == target_mask)


def matrix_sha256(matrix: sp.Matrix) -> str:
    payload = json.dumps(
        [[int(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)],
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def perm_compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(4))


def perm_order(p: tuple[int, ...]) -> int:
    identity = tuple(range(4))
    power = identity
    for order in range(1, 25):
        power = perm_compose(p, power)
        if power == identity:
            return order
    raise AssertionError("permutation order exceeds S4")


def transform_matching(
    matching: tuple[tuple[int, int], tuple[int, int]],
    p: tuple[int, ...],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in matching))


def polynomial_factor_string(eigenvalues: dict[int, int]) -> str:
    factors = []
    for eigenvalue in sorted(eigenvalues, reverse=True):
        multiplicity = eigenvalues[eigenvalue]
        base = f"(x-{eigenvalue})" if eigenvalue >= 0 else f"(x+{-eigenvalue})"
        factors.append(base if multiplicity == 1 else f"{base}^{multiplicity}")
    return "".join(factors)


def build_certificate() -> dict:
    checks: dict[str, bool] = {}

    binary_points = list(range(1, 16))
    binary_lines = pg32_lines()
    binary_planes = pg32_planes()
    checks["pg32_point_count_15"] = len(binary_points) == 15
    checks["pg32_line_count_35"] = len(binary_lines) == 35
    checks["pg32_plane_count_15"] = len(binary_planes) == 15
    checks["pg32_line_size_3"] = all(len(line) == 3 for line in binary_lines)
    checks["pg32_point_degree_7"] = all(
        sum(mask in line for line in binary_lines) == 7 for mask in binary_points
    )
    checks["pg32_plane_is_fano_7_7"] = all(
        len(plane) == 7
        and sum(set(line).issubset(plane) for line in binary_lines) == 7
        for plane in binary_planes
    )

    points = projective_points(3)
    fibers: dict[int, list[int]] = defaultdict(list)
    for index, point in enumerate(points):
        fibers[support_mask(point)].append(index)

    fiber_rows = []
    for mask in range(1, 16):
        fiber_rows.append(
            {
                "mask": bitstring(mask),
                "integer_label": mask,
                "tetrahedral_role": role(mask),
                "support_weight": mask.bit_count(),
                "fiber_size": len(fibers[mask]),
                "expected_fiber_size": 2 ** (mask.bit_count() - 1),
                "ternary_projective_points": [list(points[i]) for i in fibers[mask]],
            }
        )

    fiber_weight_totals = {
        weight: sum(
            len(fibers[mask])
            for mask in range(1, 16)
            if mask.bit_count() == weight
        )
        for weight in range(1, 5)
    }
    tetrahedral_cell_counts = {
        weight: sum(mask.bit_count() == weight for mask in range(1, 16))
        for weight in range(1, 5)
    }
    tomotope_profile = [fiber_weight_totals[w] for w in range(1, 5)]

    checks["pg33_point_count_40"] = len(points) == 40
    checks["all_15_support_fibers_nonempty"] = len(fibers) == 15
    checks["fiber_law_2_pow_weight_minus_1"] = all(
        len(fibers[mask]) == 2 ** (mask.bit_count() - 1)
        for mask in range(1, 16)
    )
    checks["tetrahedral_cells_4_6_4_1"] = [
        tetrahedral_cell_counts[w] for w in range(1, 5)
    ] == [4, 6, 4, 1]
    checks["tomotope_profile_4_12_16_8"] = tomotope_profile == [4, 12, 16, 8]

    all_matchings = matchings()
    checks["three_tetrahedral_pairings"] = len(all_matchings) == 3

    matching_results = []
    full_eigenvalues_reference = {12: 1, 2: 24, -4: 15}
    quotient_eigenvalues_reference = {12: 1, 2: 9, -4: 5}
    residual_eigenvalues_reference = {2: 15, -4: 10}

    for matching in all_matchings:
        adjacency = w33_adjacency(points, matching)
        quotient, equitable = quotient_matrix(adjacency, fibers)
        fiber_sizes = sp.Matrix([len(fibers[mask]) for mask in range(1, 16)])
        diagonal_sizes = sp.diag(*list(fiber_sizes))
        full_eigenvalues = {int(k): int(v) for k, v in adjacency.eigenvals().items()}
        quotient_eigenvalues = {int(k): int(v) for k, v in quotient.eigenvals().items()}
        residual_eigenvalues = {
            eigenvalue: full_eigenvalues[eigenvalue]
            - quotient_eigenvalues.get(eigenvalue, 0)
            for eigenvalue in full_eigenvalues
            if full_eigenvalues[eigenvalue]
            - quotient_eigenvalues.get(eigenvalue, 0)
        }

        a2 = adjacency * adjacency
        degree_set = {
            sum(int(adjacency[i, j]) for j in range(40)) for i in range(40)
        }
        lambda_set = {
            int(a2[i, j])
            for i in range(40)
            for j in range(40)
            if i != j and adjacency[i, j] == 1
        }
        mu_set = {
            int(a2[i, j])
            for i in range(40)
            for j in range(40)
            if i != j and adjacency[i, j] == 0
        }

        formula_ok = all(
            int(quotient[i, j])
            == closed_quotient_entry(source, target, matching)
            for i, source in enumerate(range(1, 16))
            for j, target in enumerate(range(1, 16))
        )
        polynomial_ok = (
            quotient * quotient
            == 8 * sp.eye(15)
            - 2 * quotient
            + 4 * sp.ones(15, 1) * fiber_sizes.T
        )
        detailed_balance_ok = (
            diagonal_sizes * quotient == quotient.T * diagonal_sizes
        )

        matching_results.append(
            {
                "matching": [list(pair) for pair in matching],
                "involution": pairing_involution(matching),
                "w33_srg": {
                    "vertices": 40,
                    "degree_set": sorted(degree_set),
                    "lambda_set": sorted(lambda_set),
                    "mu_set": sorted(mu_set),
                    "eigenvalues": {
                        str(k): v for k, v in sorted(full_eigenvalues.items())
                    },
                    "characteristic_factorization": polynomial_factor_string(
                        full_eigenvalues
                    ),
                },
                "quotient": {
                    "equitable": equitable,
                    "row_sum_set": sorted(
                        {
                            sum(int(quotient[i, j]) for j in range(15))
                            for i in range(15)
                        }
                    ),
                    "entry_histogram": {
                        str(k): v
                        for k, v in sorted(
                            Counter(int(x) for x in quotient).items()
                        )
                    },
                    "eigenvalues": {
                        str(k): v for k, v in sorted(quotient_eigenvalues.items())
                    },
                    "characteristic_factorization": polynomial_factor_string(
                        quotient_eigenvalues
                    ),
                    "residual_phase_eigenvalues": {
                        str(k): v for k, v in sorted(residual_eigenvalues.items())
                    },
                    "residual_characteristic_factorization": polynomial_factor_string(
                        residual_eigenvalues
                    ),
                    "detailed_balance": detailed_balance_ok,
                    "quadratic_identity": polynomial_ok,
                    "closed_formula_verified": formula_ok,
                    "sha256": matrix_sha256(quotient),
                    "matrix": [
                        [int(quotient[i, j]) for j in range(15)]
                        for i in range(15)
                    ],
                },
            }
        )

        checks[f"w33_srg_{matching}"] = (
            degree_set == {12} and lambda_set == {2} and mu_set == {4}
        )
        checks[f"w33_spectrum_{matching}"] = (
            full_eigenvalues == full_eigenvalues_reference
        )
        checks[f"support_partition_equitable_{matching}"] = equitable
        checks[f"quotient_spectrum_{matching}"] = (
            quotient_eigenvalues == quotient_eigenvalues_reference
        )
        checks[f"phase_residual_spectrum_{matching}"] = (
            residual_eigenvalues == residual_eigenvalues_reference
        )
        checks[f"detailed_balance_{matching}"] = detailed_balance_ok
        checks[f"quotient_quadratic_identity_{matching}"] = polynomial_ok
        checks[f"quotient_closed_formula_{matching}"] = formula_ok

    s4 = list(itertools.permutations(range(4)))
    base_matching = all_matchings[0]
    stabilizer = [
        p for p in s4 if transform_matching(base_matching, p) == base_matching
    ]
    orbit = {transform_matching(base_matching, p) for p in s4}
    order_census = Counter(perm_order(p) for p in stabilizer)
    nonabelian = any(
        perm_compose(p, q) != perm_compose(q, p)
        for p in stabilizer
        for q in stabilizer
    )
    checks["s4_order_24"] = len(s4) == 24
    checks["pairing_orbit_size_3"] = len(orbit) == 3
    checks["pairing_stabilizer_order_8"] = len(stabilizer) == 8
    checks["pairing_stabilizer_d8_order_census"] = order_census == Counter(
        {2: 5, 4: 2, 1: 1}
    )
    checks["pairing_stabilizer_nonabelian"] = nonabelian

    face_masks = sorted(mask for mask in range(1, 16) if mask.bit_count() == 3)
    repo_type_a_masks = sorted(
        int(x, 2) for x in ("1110", "1101", "1011", "0111")
    )
    face_pairing_charts = [
        {
            "face_mask": bitstring(face),
            "matching": [list(pair) for pair in matching],
        }
        for face in face_masks
        for matching in all_matchings
    ]
    checks["type_a_masks_are_exactly_tetrahedral_faces"] = (
        face_masks == repo_type_a_masks
    )
    checks["face_pairing_chart_count_12"] = len(face_pairing_charts) == 12

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"failed checks: {failed}")

    return {
        "schema": "w33.pass2808.pg32_tetrahedral_support_lift.v1",
        "status": "COMPLETE_EXACT",
        "canonical_pass": 2808,
        "title": (
            "PG(3,2) Tetrahedral Support-Lift / "
            "Tomotope Equitable-Quotient Theorem"
        ),
        "headline": (
            "The support map PG(3,3)->PG(3,2) partitions the 40 W33 points "
            "over the 15 tetrahedral cells with fiber law 2^(weight-1), giving "
            "the exact tomotope profile (4,12,16,8); for each tetrahedral "
            "symplectic pairing this is an equitable W33 partition."
        ),
        "check_count": len(checks),
        "checks": checks,
        "pg32": {
            "point_count": len(binary_points),
            "line_count": len(binary_lines),
            "plane_count": len(binary_planes),
            "tetrahedral_cell_counts_by_weight": {
                str(k): v for k, v in tetrahedral_cell_counts.items()
            },
            "line_type_census_from_bt805": {
                "vertex_vertex_edge": 6,
                "vertex_face_edge": 12,
                "edge_edge_edge": 4,
                "edge_face_face": 6,
                "body_edge_edge": 3,
                "body_face_vertex": 4,
            },
        },
        "support_lift": {
            "definition": (
                "pi([x1:x2:x3:x4]) = binary support mask of nonzero coordinates"
            ),
            "fiber_law": "|pi^{-1}(S)| = 2^(|S|-1)",
            "fiber_rows": fiber_rows,
            "weight_total_profile": {
                str(k): v for k, v in fiber_weight_totals.items()
            },
            "tomotope_f_vector": tomotope_profile,
            "interpretation": (
                "tetrahedron k-cells lift to 2^k ternary phase classes; "
                "the lifted rank counts are 4,12,16,8"
            ),
        },
        "equitable_quotients": {
            "matching_count": len(all_matchings),
            "closed_formula": (
                "Q_ST = 2^(|T|-r-1) c_r - delta_ST, "
                "r=|T intersect tau(S)|, c_r=# sign vectors in {+1,-1}^r "
                "whose sum is 0 mod 3"
            ),
            "zero_sum_sign_counts": {
                str(r): zero_sum_sign_count(r) for r in range(5)
            },
            "full_w33_spectrum": {"12": 1, "2": 24, "-4": 15},
            "binary_support_quotient_spectrum": {"12": 1, "2": 9, "-4": 5},
            "ternary_phase_residual_spectrum": {"2": 15, "-4": 10},
            "quadratic_identity": "Q^2 = 8 I - 2 Q + 4 1 s^T",
            "detailed_balance": "diag(s) Q = Q^T diag(s)",
            "matching_results": matching_results,
        },
        "selector_bridge": {
            "tetrahedral_symmetry": "S4",
            "pairings": [
                [list(pair) for pair in matching] for matching in all_matchings
            ],
            "pairing_orbit_size": len(orbit),
            "pairing_stabilizer_order": len(stabilizer),
            "pairing_stabilizer_type": "D8",
            "pairing_stabilizer_element_order_census": {
                str(k): v for k, v in sorted(order_census.items())
            },
            "factorization": "24 = 8 * 3 = |S4| = |D8| * #(perfect matchings)",
            "type_a_face_masks": [bitstring(mask) for mask in face_masks],
            "face_pairing_chart_count": len(face_pairing_charts),
            "face_pairing_charts": face_pairing_charts,
        },
        "boundaries": {
            "not_linear_reduction": (
                "The support map is a combinatorial projective partition, not a "
                "field homomorphism or a linear map F3^4 -> F2^4."
            ),
            "selector_intertwiner": (
                "The 12 face-pairing charts match the existing Type-A mask count "
                "and 4*3 architecture. This certificate does not yet identify the "
                "existing 2160x160 selector matrices with these charts objectwise."
            ),
            "tomotope": (
                "The equality (4,12,16,8) is an exact fiber-capacity theorem. "
                "An incidence-preserving isomorphism from the support quotient to "
                "the abstract tomotope remains a separate claim."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    certificate = build_certificate()
    payload = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")
    if args.stdout:
        print(payload, end="")
    else:
        print(f"PASS {certificate['check_count']}/{certificate['check_count']}")
        print(args.output)


if __name__ == "__main__":
    main()
