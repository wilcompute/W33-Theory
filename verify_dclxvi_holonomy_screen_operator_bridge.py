#!/usr/bin/env python3
"""Part DCLXVI: holonomy screen operator bridge.

After DCLXV, the next question is whether the universal family of fixed screens is
still extra structure, or whether it is already contained in the finite operator
algebra of W(3,3) itself.

This verifier proves the stronger closure statement. If S is the 40x40 incidence
matrix of the universal fixed-screen family, then

    S = A + I,

where A is the W(3,3) adjacency matrix. Consequently

    S^2 = 9 I + 4 J,

and the screen family is exactly the symmetric 2-(40,13,4) hyperplane design of
PG(3,3), already sitting inside the existing SRG adjacency algebra.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from w33_homology import build_w33

OUT_PATH = ROOT / "data" / "dclxvi_holonomy_screen_operator_bridge.json"
MODULUS = 3


@dataclass(frozen=True)
class OperatorSummary:
    field_order: int
    point_count: int
    screen_count: int
    screen_size: int
    point_pair_screen_count: int
    screen_pair_intersection_count: int
    all_identities_hold: bool


def _canon_point(point: Any) -> tuple[int, int, int, int]:
    values = [int(x) % MODULUS for x in point]
    for value in values:
        if value != 0:
            if value == 2:
                values = [(2 * x) % MODULUS for x in values]
            return tuple(values)
    raise ValueError("zero vector is not a projective point")


def _symplectic_form(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    a, b, c, d = u
    a2, b2, c2, d2 = v
    return (a * b2 - b * a2 + c * d2 - d * c2) % MODULUS


def _adjacency_matrix(adj_lists: list[list[int]]) -> np.ndarray:
    n = len(adj_lists)
    matrix = np.zeros((n, n), dtype=int)
    for i, neighbors in enumerate(adj_lists):
        for j in neighbors:
            matrix[i, j] = 1
    return matrix


def _screen_incidence_matrix(vertices: list[tuple[int, int, int, int]]) -> np.ndarray:
    n = len(vertices)
    matrix = np.zeros((n, n), dtype=int)
    for i, anchor in enumerate(vertices):
        for j, point in enumerate(vertices):
            matrix[i, j] = int(_symplectic_form(anchor, point) == 0)
    return matrix


def _rounded_spectrum(matrix: np.ndarray) -> dict[int, int]:
    eigenvalues = np.linalg.eigvalsh(matrix)
    counts: Counter[int] = Counter()
    for value in eigenvalues:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) > 1e-8:
            raise ValueError(f"non-integral eigenvalue encountered: {value}")
        counts[rounded] += 1
    return dict(sorted(counts.items()))


def build_bridge() -> dict[str, Any]:
    _, raw_vertices, adj_lists, _ = build_w33()
    vertices = list(dict.fromkeys(_canon_point(vertex) for vertex in raw_vertices))
    n = len(vertices)

    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=int)
    J = np.ones((n, n), dtype=int)
    S = _screen_incidence_matrix(vertices)
    closure = S @ S
    point_pair_screen_counts = S.T @ S
    row_sums = sorted(set(int(x) for x in S.sum(axis=1).tolist()))
    col_sums = sorted(set(int(x) for x in S.sum(axis=0).tolist()))
    offdiag_screen_intersections = sorted(
        set(int(closure[i, j]) for i in range(n) for j in range(n) if i != j)
    )
    offdiag_point_pair_counts = sorted(
        set(int(point_pair_screen_counts[i, j]) for i in range(n) for j in range(n) if i != j)
    )
    spectrum = _rounded_spectrum(S)

    identities = {
        "screen_incidence_is_exactly_adjacency_plus_identity": np.array_equal(S, A + I),
        "screen_incidence_is_symmetric": np.array_equal(S, S.T),
        "every_screen_has_size_13": row_sums == [13] and col_sums == [13],
        "any_two_distinct_screens_intersect_in_4_points": offdiag_screen_intersections == [4],
        "any_two_distinct_points_lie_in_4_screens": offdiag_point_pair_counts == [4],
        "screen_operator_closure_is_9I_plus_4J": np.array_equal(closure, 9 * I + 4 * J),
        "screen_family_is_the_symmetric_2_40_13_4_design": (
            row_sums == [13]
            and col_sums == [13]
            and offdiag_screen_intersections == [4]
            and offdiag_point_pair_counts == [4]
        ),
        "screen_operator_spectrum_is_13_1_3_24_minus3_15": spectrum == {-3: 15, 3: 24, 13: 1},
        "therefore_the_universal_holonomy_screen_family_is_already_in_the_w33_adjacency_algebra": (
            np.array_equal(S, A + I)
            and np.array_equal(closure, 9 * I + 4 * J)
            and spectrum == {-3: 15, 3: 24, 13: 1}
        ),
    }

    summary = OperatorSummary(
        field_order=MODULUS,
        point_count=n,
        screen_count=n,
        screen_size=13,
        point_pair_screen_count=4,
        screen_pair_intersection_count=4,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "design_parameters": {
            "v": n,
            "b": n,
            "r": 13,
            "k": 13,
            "lambda": 4,
        },
        "operator_statistics": {
            "screen_row_sums": row_sums,
            "screen_column_sums": col_sums,
            "distinct_offdiagonal_screen_intersections": offdiag_screen_intersections,
            "distinct_offdiagonal_point_pair_counts": offdiag_point_pair_counts,
            "spectrum": spectrum,
        },
        "interpretation": {
            "screen_operator": "S = A + I",
            "closure": "S^2 = 9I + 4J",
            "design": "self-dual symmetric 2-(40,13,4) hyperplane design of PG(3,3)",
            "breakthrough": (
                "The universal holonomy-screen bundle is not extra finite data. Its incidence operator is exactly adjacency plus identity, so the whole screen family already lies inside the existing W(3,3) adjacency algebra."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()