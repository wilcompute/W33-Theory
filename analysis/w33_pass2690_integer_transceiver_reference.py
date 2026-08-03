#!/usr/bin/env python3
"""Pass 2690: exact digital contract for the W(3,3) incidence transceiver.

The manuscript proves that T=N-J/10 has rank 24 and T^T T=6E_24.
Hardware should not divide by ten internally.  This witness freezes the
integer-scaled map

    S = 10T = 10N - J,

whose entries are +9 on the four incidences in each row and -1 elsewhere.
It proves the exact projector identities

    S^T S = 600 E_24^P,   S S^T = 600 E_24^L,

and exports the 40 forward and 40 reverse four-tap masks used by the RTL.
The result is an exact digital/fixed-point contract.  It does not infer an
optical 1/sqrt(6) amplitude implementation, loss budget, detector model, or
calibration procedure.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass2690_2695_incidence_transceiver.json"

FROZEN_FORWARD_MASKS = (
    "000000000f",
    "000000e001",
    "0000070001",
    "0000380001",
    "0000000492",
    "0000000922",
    "0000001242",
    "8880000004",
    "3100000004",
    "4600000004",
    "0028400008",
    "0042800008",
    "0015000008",
    "0080402010",
    "0402010010",
    "2010080010",
    "0200802020",
    "1004010020",
    "8020080020",
    "0101002040",
    "0808010040",
    "4040080040",
    "4004004080",
    "0120020080",
    "0800900080",
    "2008004100",
    "00c0020100",
    "0401100100",
    "8002004200",
    "0210020200",
    "1000500200",
    "1040008400",
    "8001040400",
    "0208200400",
    "0810008800",
    "4000440800",
    "0102200800",
    "0420009000",
    "2000841000",
    "0084201000",
)
FROZEN_REVERSE_MASKS = (
    "000000000f",
    "0000000071",
    "0000000381",
    "0000001c01",
    "000000e010",
    "0000070020",
    "0000380040",
    "0001c00010",
    "000e000020",
    "0070000040",
    "0380000010",
    "1c00000020",
    "e000000040",
    "0000092002",
    "0012400002",
    "2480000002",
    "0000124004",
    "0024800004",
    "4900000004",
    "0000248008",
    "0049000008",
    "9200000008",
    "0840002400",
    "4001010800",
    "0108081000",
    "1010004800",
    "8000421000",
    "0202100400",
    "0420009000",
    "2000840400",
    "0084200800",
    "8004002080",
    "1000880100",
    "0220010200",
    "2008004200",
    "0401100080",
    "00c0020100",
    "4002008100",
    "0800600200",
    "0110040080",
)


def canon(vector: tuple[int, ...]) -> tuple[int, ...]:
    """Canonical projective representative over F_3."""
    v = tuple(value % 3 for value in vector)
    for value in v:
        if value:
            scale = 1 if value == 1 else 2
            return tuple((scale * entry) % 3 for entry in v)
    raise ValueError("zero vector has no projective representative")


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*matrix)]


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def rank_q(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    rank = 0
    for column in range(cols):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def build_geometry() -> tuple[
    list[tuple[int, ...]], list[list[int]], list[tuple[int, ...]], list[list[int]]
]:
    points = sorted(
        {canon(vector) for vector in product(range(3), repeat=4) if any(vector)}
    )

    def symplectic(left: tuple[int, ...], right: tuple[int, ...]) -> int:
        return (
            left[0] * right[2] - left[2] * right[0]
            + left[1] * right[3] - left[3] * right[1]
        ) % 3

    adjacency = [[0] * 40 for _ in range(40)]
    for left, right in combinations(range(40), 2):
        if symplectic(points[left], points[right]) == 0:
            adjacency[left][right] = adjacency[right][left] = 1

    lines = [
        vertices
        for vertices in combinations(range(40), 4)
        if all(adjacency[a][b] for a, b in combinations(vertices, 2))
    ]
    incidence = [[0] * 40 for _ in range(40)]
    for line_index, line in enumerate(lines):
        for point in line:
            incidence[line_index][point] = 1
    return points, adjacency, lines, incidence


def mask_hex(row: list[int]) -> str:
    mask = sum((bit & 1) << index for index, bit in enumerate(row))
    return f"{mask:010x}"


def certificate() -> dict[str, object]:
    points, point_adjacency, lines, incidence = build_geometry()
    incidence_t = transpose(incidence)
    identity = [[int(row == column) for column in range(40)] for row in range(40)]
    ones = [[1] * 40 for _ in range(40)]

    line_gram = matmul(incidence, incidence_t)
    point_gram = matmul(incidence_t, incidence)
    line_adjacency = [
        [line_gram[row][column] - 4 * identity[row][column] for column in range(40)]
        for row in range(40)
    ]

    scaled = [
        [10 * incidence[row][column] - 1 for column in range(40)]
        for row in range(40)
    ]
    scaled_t = transpose(scaled)
    point_polar = matmul(scaled_t, scaled)
    line_polar = matmul(scaled, scaled_t)

    expected_point = [
        [
            100 * (4 * identity[row][column] + point_adjacency[row][column])
            - 40 * ones[row][column]
            for column in range(40)
        ]
        for row in range(40)
    ]
    expected_line = [
        [
            100 * (4 * identity[row][column] + line_adjacency[row][column])
            - 40 * ones[row][column]
            for column in range(40)
        ]
        for row in range(40)
    ]

    forward_masks = tuple(mask_hex(row) for row in incidence)
    reverse_masks = tuple(mask_hex(row) for row in incidence_t)

    degrees = [sum(row) for row in point_adjacency]
    adjacent_common = []
    nonadjacent_common = []
    for left, right in combinations(range(40), 2):
        common = sum(
            point_adjacency[left][vertex] * point_adjacency[right][vertex]
            for vertex in range(40)
        )
        (adjacent_common if point_adjacency[left][right] else nonadjacent_common).append(common)

    checks = {
        "w33_srg_40_12_2_4": (
            len(points) == 40
            and set(degrees) == {12}
            and set(adjacent_common) == {2}
            and set(nonadjacent_common) == {4}
        ),
        "forty_isotropic_lines": len(lines) == 40,
        "incidence_40_by_40_degree4": (
            all(sum(row) == 4 for row in incidence)
            and all(sum(row) == 4 for row in incidence_t)
        ),
        "forward_masks_frozen": forward_masks == FROZEN_FORWARD_MASKS,
        "reverse_masks_frozen": reverse_masks == FROZEN_REVERSE_MASKS,
        "forward_masks_all_weight4": all(int(mask, 16).bit_count() == 4 for mask in forward_masks),
        "reverse_masks_all_weight4": all(int(mask, 16).bit_count() == 4 for mask in reverse_masks),
        "S_entries_are_9_or_minus1": {value for row in scaled for value in row} == {-1, 9},
        "S_kills_constants_both_sides": (
            all(sum(row) == 0 for row in scaled)
            and all(sum(row) == 0 for row in scaled_t)
        ),
        "rank_S_24": rank_q(scaled) == 24,
        "StS_exact": point_polar == expected_point,
        "SSt_exact": line_polar == expected_line,
        "StS_projector_polynomial_G2_eq_600G": (
            matmul(point_polar, point_polar)
            == [[600 * value for value in row] for row in point_polar]
        ),
        "SSt_projector_polynomial_G2_eq_600G": (
            matmul(line_polar, line_polar)
            == [[600 * value for value in row] for row in line_polar]
        ),
        "basis_column_contract": all(
            sorted(scaled[row][column] for row in range(40)) == [-1] * 36 + [9] * 4
            for column in range(40)
        ),
        "basis_row_contract": all(
            sorted(row) == [-1] * 36 + [9] * 4 for row in scaled
        ),
    }
    assert all(checks.values()), {name: value for name, value in checks.items() if not value}

    result: dict[str, object] = {
        "theorem": "Passes 2690-2695 exact integer incidence transceiver implementation",
        "status": "PASS_EXACT_MULTIPLIER_FREE_DIGITAL_TRANSCEIVER_WITH_OPTICAL_BOUNDARY",
        "passes": [2690, 2691, 2692, 2693, 2694, 2695],
        "source_theorem": {
            "T": "N-J/10",
            "rank": 24,
            "TtT": "6 E24",
            "integer_scale": "S=10T=10N-J",
        },
        "geometry": {
            "points": 40,
            "lines": 40,
            "incidences": 160,
            "forward_masks_hex": list(forward_masks),
            "reverse_masks_hex": list(reverse_masks),
        },
        "digital_core": {
            "matrix_entries_per_output": {"9": 4, "-1": 36},
            "formula": "y_i=10*local4_i-global40=(local4_i<<3)+(local4_i<<1)-global40",
            "general_multipliers": 0,
            "conservative_output_width": "OW=W+7",
            "point_to_line": True,
            "line_to_point": True,
            "streamed_lanes": 40,
            "polar_square_gain": 600,
            "decode_rule": "on the shared rank-24 image, x=S^T S x / 600",
        },
        "checks": checks,
        "boundary": (
            "This closes an exact digital fixed-point/RTL contract for 10T. "
            "It does not supply the optical 1/sqrt(6) amplitude normalization, "
            "loss budget, detector model, or calibration procedure."
        ),
    }
    digest_source = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["sha256_without_hash_field"] = hashlib.sha256(digest_source).hexdigest()
    return result


def main() -> None:
    result = certificate()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("rank(S)=24; S^T S and S S^T have exact gain 600")
    print("40 forward + 40 reverse masks frozen; all masks have weight 4")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"sha256={result['sha256_without_hash_field']}")


if __name__ == "__main__":
    main()
