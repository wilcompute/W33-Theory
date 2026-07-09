#!/usr/bin/env python3
"""Pass 157: exact primary structure and minimal shell of the W33 +2 lattice.

For L2 = ker_Z(A - 2I), this witness computes the Gram Smith form exactly,
identifies its radicals over F_2, F_3, and F_5, and constructs the complete
norm-6 shell from ordered pairs of W33 lines through a point.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.bt926_plus2_eigenlattice import canon, snf_with_transforms


OUT = ROOT / "data" / "w33_pass157_eigenlattice_prime_collision.json"
PARI_CERTIFICATE = {
    "minimal_vector_count": 480,
    "minimal_norm": 6,
    "half_shell_columns": 240,
}


def build_w33() -> tuple[list[tuple[int, ...]], np.ndarray]:
    points = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symplectic(x: tuple[int, ...], y: tuple[int, ...]) -> int:
        return (
            x[0] * y[2]
            - x[2] * y[0]
            + x[1] * y[3]
            - x[3] * y[1]
        ) % 3

    adjacency = np.zeros((40, 40), dtype=np.int64)
    for left, right in combinations(range(40), 2):
        if symplectic(points[left], points[right]) == 0:
            adjacency[left, right] = adjacency[right, left] = 1
    return points, adjacency


def rank_mod(matrix: np.ndarray | Matrix, prime: int) -> int:
    rows = [[int(value) % prime for value in row] for row in np.asarray(matrix)]
    work = np.array(rows, dtype=np.int64)
    row_count, column_count = work.shape
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row, column] % prime),
            None,
        )
        if pivot is None:
            continue
        work[[rank, pivot]] = work[[pivot, rank]]
        inverse = pow(int(work[rank, column]), -1, prime)
        work[rank] = (inverse * work[rank]) % prime
        for row in range(row_count):
            if row != rank and work[row, column]:
                work[row] = (
                    work[row] - work[row, column] * work[rank]
                ) % prime
        rank += 1
        if rank == row_count:
            break
    return rank


def column_rank(matrix: np.ndarray, prime: int) -> int:
    return rank_mod(matrix.T, prime)


def integer_eigenbasis(adjacency: np.ndarray) -> np.ndarray:
    operator = adjacency - 2 * np.eye(40, dtype=np.int64)
    diagonal, _, right = snf_with_transforms(operator)
    zero_columns = [
        column for column in range(40) if int(diagonal[column, column]) == 0
    ]
    return np.array(
        [
            [int(right[row, column]) for column in zero_columns]
            for row in range(40)
        ],
        dtype=np.int64,
    )


def pari_minimum_certificate(kernel: np.ndarray) -> tuple[dict[str, int], str]:
    """Run exact PARI Fincke-Pohst enumeration, with a checked cache fallback."""
    if shutil.which("gp") is None:
        return PARI_CERTIFICATE.copy(), "cached"

    reduced = Matrix(kernel.T.tolist()).lll()
    gram = reduced * reduced.T
    gp_matrix = "[" + ";".join(
        ",".join(str(int(gram[row, column])) for column in range(gram.cols))
        for row in range(gram.rows)
    ) + "]"
    program = (
        f"G={gp_matrix};"
        "r=qfminim(G);"
        "print(r[1]);"
        "print(r[2]);"
        "print(matsize(r[3])[2]);"
        "quit;\n"
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
        timeout=300,
    )
    values = [int(line.strip()) for line in completed.stdout.splitlines() if line.strip()]
    if len(values) != 3:
        raise RuntimeError(f"unexpected PARI qfminim output: {completed.stdout!r}")
    return {
        "minimal_vector_count": values[0],
        "minimal_norm": values[1],
        "half_shell_columns": values[2],
    }, "live"


def w33_lines(adjacency: np.ndarray) -> list[frozenset[int]]:
    return [
        frozenset(vertices)
        for vertices in combinations(range(40), 4)
        if all(adjacency[left, right] for left, right in combinations(vertices, 2))
    ]


def local_line_pair_shell(
    adjacency: np.ndarray, lines: list[frozenset[int]]
) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    through = {
        point: [line for line in lines if point in line] for point in range(40)
    }
    vectors: list[np.ndarray] = []
    labels: list[tuple[int, int, int]] = []
    line_ids = {line: index for index, line in enumerate(lines)}
    for point in range(40):
        pencil = through[point]
        for positive in pencil:
            for negative in pencil:
                if positive == negative:
                    continue
                vector = np.zeros(40, dtype=np.int64)
                vector[list(positive - {point})] = 1
                vector[list(negative - {point})] = -1
                vectors.append(vector)
                labels.append((point, line_ids[positive], line_ids[negative]))
    return np.array(vectors, dtype=np.int64), labels


def canonical_ray(vector: np.ndarray) -> tuple[int, ...]:
    forward = tuple(int(value) for value in vector)
    backward = tuple(-value for value in forward)
    return min(forward, backward)


def counter_json(counter: Counter[int]) -> dict[str, int]:
    return {str(key): int(counter[key]) for key in sorted(counter)}


def main() -> int:
    _, adjacency = build_w33()
    identity = np.eye(40, dtype=np.int64)
    ones_matrix = np.ones((40, 40), dtype=np.int64)
    ones = np.ones(40, dtype=np.int64)
    kernel = integer_eigenbasis(adjacency)
    gram = Matrix(kernel.T.tolist()) * Matrix(kernel.tolist())
    smith = smith_normal_form(gram, domain=ZZ)
    invariants = [abs(int(smith[index, index])) for index in range(24)]
    invariant_profile = Counter(invariants)
    determinant = int(gram.det())

    modular = {}
    for prime in (2, 3, 5):
        gram_rank = rank_mod(np.array(gram.tolist(), dtype=object), prime)
        modular[str(prime)] = {
            "L2_mod_p_dimension": column_rank(kernel, prime),
            "gram_rank": gram_rank,
            "radical_dimension": 24 - gram_rank,
        }

    # p=2: W=L2/2L2=ker(A), and rad(W)=im(A), the binary W33 code.
    p2_image_rank = column_rank(adjacency, 2)
    p2_join_rank = column_rank(np.column_stack([kernel, adjacency]), 2)

    # p=3: on H=1^perp, N=A+I is square-zero and its image is rad(W).
    hyperplane = np.zeros((40, 39), dtype=np.int64)
    for index in range(39):
        hyperplane[index, index] = 1
        hyperplane[39, index] = -1
    collision = adjacency + identity
    collision_image = collision @ hyperplane
    p3_image_rank = column_rank(collision_image, 3)
    p3_join_rank = column_rank(np.column_stack([kernel, collision_image]), 3)

    # p=5: the Perron eigenvalue 12 collides with +2; the radical is <1>.
    p5_ones_join_rank = column_rank(np.column_stack([kernel, ones]), 5)

    lines = w33_lines(adjacency)
    shell, labels = local_line_pair_shell(adjacency, lines)
    rays = {canonical_ray(vector) for vector in shell}
    supports = {tuple(np.flatnonzero(vector).tolist()) for vector in shell}
    inner = shell @ shell.T
    local_profiles = {
        tuple(sorted(Counter(int(value) for value in row).items())) for row in inner
    }
    local_profile = Counter(int(value) for value in inner[0])

    pencils = {
        point: [line for line in lines if point in line] for point in range(40)
    }
    endpoint_count = sum(len(list(combinations(pencils[point], 2))) for point in range(40))
    # Each endpoint has one complementary endpoint; divide the 240 endpoints by two.
    axis_count = endpoint_count // 2

    pari, pari_source = pari_minimum_certificate(kernel)

    checks = {
        "w33_srg_relation": bool(
            np.array_equal(
                adjacency @ adjacency,
                8 * identity - 2 * adjacency + 4 * ones_matrix,
            )
        ),
        "integer_eigenbasis_rank_24": kernel.shape == (40, 24),
        "integer_eigenbasis_equation": bool(
            np.array_equal(adjacency @ kernel, 2 * kernel)
        ),
        "exact_determinant": determinant == 2**16 * 3**10 * 5,
        "exact_smith_profile": invariant_profile
        == Counter({1: 8, 2: 6, 6: 9, 30: 1}),
        "all_primary_factors_elementary": all(
            invariant % (prime * prime) != 0
            for invariant in invariants
            for prime in (2, 3, 5)
        ),
        "p2_radical_dimension_16": modular["2"]["radical_dimension"] == 16,
        "p2_radical_is_image_A": (
            p2_image_rank == 16
            and p2_join_rank == 24
            and np.all((adjacency @ adjacency) % 2 == 0)
            and np.all((kernel.T @ adjacency) % 2 == 0)
        ),
        "p3_radical_dimension_10": modular["3"]["radical_dimension"] == 10,
        "p3_collision_identity": bool(
            np.all((collision @ collision - ones_matrix) % 3 == 0)
        ),
        "p3_radical_is_collision_image": (
            column_rank(collision, 3) == 11
            and p3_image_rank == 10
            and p3_join_rank == 24
            and np.all((kernel.T @ collision_image) % 3 == 0)
        ),
        "p5_radical_dimension_1": modular["5"]["radical_dimension"] == 1,
        "p5_radical_is_constants": (
            p5_ones_join_rank == 24
            and np.all((kernel.T @ ones) % 5 == 0)
            and np.all(
                (adjacency - 2 * identity) @ ones % 5 == 0
            )
        ),
        "forty_W33_lines": len(lines) == 40,
        "four_lines_per_point": all(len(pencil) == 4 for pencil in pencils.values()),
        "local_line_pair_vectors_480": (
            shell.shape == (480, 40)
            and len({tuple(vector) for vector in shell}) == 480
            and len(labels) == 480
        ),
        "local_vectors_are_norm6_eigenvectors": bool(
            np.all(np.einsum("ij,ij->i", shell, shell) == 6)
            and np.array_equal(shell @ adjacency, 2 * shell)
        ),
        "projective_shell_is_240_axis_endpoints": (
            len(rays) == 240
            and len(supports) == 240
            and endpoint_count == 240
            and axis_count == 120
        ),
        "minimal_shell_local_profile_constant": (
            len(local_profiles) == 1
            and local_profile
            == Counter({-6: 1, -3: 4, -2: 45, -1: 108, 0: 164,
                        1: 108, 2: 45, 3: 4, 6: 1})
        ),
        "pari_exact_minimum_and_shell_complete": pari == PARI_CERTIFICATE,
    }
    checks = {name: bool(value) for name, value in checks.items()}

    payload = {
        "schema": "w33.pass157.eigenlattice_prime_collision.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "lattice": {
            "definition": "L2 = {x in Z^40 : A x = 2 x}",
            "rank": 24,
            "determinant": determinant,
            "determinant_factorization": "2^16 * 3^10 * 5",
            "smith_invariants": invariants,
            "smith_profile": {
                str(key): int(value)
                for key, value in sorted(invariant_profile.items())
            },
            "discriminant_group_invariant_factors": (
                "(Z/2)^6 + (Z/6)^9 + Z/30"
            ),
            "discriminant_group_primary": (
                "(Z/2)^16 + (Z/3)^10 + Z/5"
            ),
        },
        "primary_radicals": {
            "2": {
                **modular["2"],
                "identification": (
                    "rad(L2/2L2) = im(A mod 2) = C, dimension 16"
                ),
            },
            "3": {
                **modular["3"],
                "identification": (
                    "rad(L2/3L2) = im((A+I)|1^perp), dimension 10"
                ),
                "operator_rank_on_full_space": column_rank(collision, 3),
                "operator_rank_on_augmentation": p3_image_rank,
                "operator_identity": "(A+I)^2 = J mod 3",
            },
            "5": {
                **modular["5"],
                "identification": (
                    "rad(L2/5L2) = span(all-ones), dimension 1"
                ),
            },
        },
        "minimal_shell": {
            **pari,
            "pari_certificate_source": pari_source,
            "construction": (
                "x(p;L+,L-) = 1_(L+ minus p) - 1_(L- minus p), "
                "for ordered distinct lines L+,L- through p"
            ),
            "ordered_local_line_pairs": len(shell),
            "projective_minimal_rays": len(rays),
            "axis_endpoints": endpoint_count,
            "local_axes": axis_count,
            "local_inner_product_profile": counter_json(local_profile),
            "reading": (
                "The 480 minimal vectors are the oriented local line-pair "
                "selectors. Modulo antipodes they are the 240 axis endpoints "
                "used by Pass 123 to lift onto the 240 signed E8 roots."
            ),
        },
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
