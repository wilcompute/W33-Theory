"""A2 overlap null-plane audit for complete two-qutrit MUB frames.

This is the local executable form of remote Part CXXV.  It records the
coarse three-sector overlap quotient for the 36 complete stabilizer MUB
frames and checks that total overlap kills the A2 sector-difference plane.
"""

from __future__ import annotations

from typing import Dict, Tuple

TYPES = ("E+", "E-", "O")
SECTOR_SIZE = 12
SELF_OVERLAP = 10
FOUR_OVERLAP = 4
ONE_OVERLAP = 1

FOUR_OVERLAP_QUOTIENT = (
    (3, 6, 6),
    (6, 3, 6),
    (6, 6, 3),
)

TOTAL_OVERLAP_QUOTIENT = (
    (30, 30, 30),
    (30, 30, 30),
    (30, 30, 30),
)

A2_BASIS = ((1, -1, 0), (1, 1, -2))


def mat_vec(
    matrix: Tuple[Tuple[int, ...], ...], vector: Tuple[int, ...]
) -> Tuple[int, ...]:
    """Multiply a small integer matrix by an integer vector."""
    return tuple(
        sum(matrix[row][col] * vector[col] for col in range(len(vector)))
        for row in range(len(matrix))
    )


def det3(matrix: Tuple[Tuple[int, int, int], ...]) -> int:
    """Return the determinant of a 3x3 integer matrix."""
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def mub_a2_overlap_null_plane_summary() -> Dict[str, object]:
    """Return exact Part CXXV overlap quotient certificates."""
    same_sector_total = SELF_OVERLAP + 3 * FOUR_OVERLAP + 8 * ONE_OVERLAP
    cross_sector_total = 6 * FOUR_OVERLAP + 6 * ONE_OVERLAP
    within_edges = len(TYPES) * (SECTOR_SIZE * 3 // 2)
    cross_edges = 3 * (SECTOR_SIZE * 6)
    total_four_overlap_edges = SECTOR_SIZE * len(TYPES) * 15 // 2

    return {
        "source_scope": {
            "remote_part": "CXXV",
            "title": "A2 overlap null plane for complete two-qutrit MUB frames",
        },
        "sector_packet": {
            "sector_labels": TYPES,
            "sector_size": SECTOR_SIZE,
            "frame_count": SECTOR_SIZE * len(TYPES),
            "coarse_quotient_shape": "36 = 12 x 3",
            "a2_basis": A2_BASIS,
        },
        "four_overlap_graph": {
            "quotient": FOUR_OVERLAP_QUOTIENT,
            "row_sums": tuple(sum(row) for row in FOUR_OVERLAP_QUOTIENT),
            "regular_degree": 15,
            "within_sector_edges": within_edges,
            "cross_sector_edges": cross_edges,
            "total_edges": total_four_overlap_edges,
            "constant_eigenvalue": mat_vec(FOUR_OVERLAP_QUOTIENT, (1, 1, 1)),
            "a2_eigenvalue": -3,
            "a2_images": tuple(
                mat_vec(FOUR_OVERLAP_QUOTIENT, basis) for basis in A2_BASIS
            ),
        },
        "total_overlap_form": {
            "quotient": TOTAL_OVERLAP_QUOTIENT,
            "same_sector_total": same_sector_total,
            "cross_sector_total": cross_sector_total,
            "row_sums": tuple(sum(row) for row in TOTAL_OVERLAP_QUOTIENT),
            "constant_eigenvalue": mat_vec(TOTAL_OVERLAP_QUOTIENT, (1, 1, 1)),
            "a2_images": tuple(
                mat_vec(TOTAL_OVERLAP_QUOTIENT, basis) for basis in A2_BASIS
            ),
            "determinant": det3(TOTAL_OVERLAP_QUOTIENT),
            "rank": 1,
        },
        "theorem": {
            "four_overlap_graph_is_15_regular": (
                tuple(sum(row) for row in FOUR_OVERLAP_QUOTIENT) == (15, 15, 15)
                and total_four_overlap_edges == 270
            ),
            "same_and_cross_sector_total_overlap_balances_to_30": (
                same_sector_total == cross_sector_total == 30
            ),
            "four_overlap_quotient_has_a2_eigenvalue_minus_3": all(
                mat_vec(FOUR_OVERLAP_QUOTIENT, basis)
                == tuple(-3 * value for value in basis)
                for basis in A2_BASIS
            ),
            "total_overlap_quotient_kills_a2_plane": all(
                mat_vec(TOTAL_OVERLAP_QUOTIENT, basis) == (0, 0, 0)
                for basis in A2_BASIS
            ),
            "total_overlap_quotient_is_rank_one": (
                det3(TOTAL_OVERLAP_QUOTIENT) == 0
                and TOTAL_OVERLAP_QUOTIENT[0]
                == TOTAL_OVERLAP_QUOTIENT[1]
                == TOTAL_OVERLAP_QUOTIENT[2]
            ),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(mub_a2_overlap_null_plane_summary(), indent=2))
