#!/usr/bin/env python3
"""Exact Parseval measurement-frame audit on the W(3,3) line module.

This packages the new Part LXXIII claim as an executable theorem surface.

The carrier is the 40-dimensional true-line module of W(3,3). Two natural
0/1 probes act on that carrier:

1. B : true lines (40) -> spreads (36),
2. R : true lines (40) -> anti-lines (90), where the anti-lines are the 90
   non-isotropic projective lines of PG(3,3) in the same symplectic
   convention as the true-line carrier, and incidence means point-intersection.

The centered probes resolve the line module exactly as

    40 = 1 + 15 + 24,

with the spread probe carrying the 15-sector, the anti-line probe carrying the
24-sector, and the mean channel carrying the trivial line.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for extra in (ROOT, ROOT / "exploration"):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from w33_line_spread_intertwiner_bridge import (  # noqa: E402
    _all_spreads,
    _build_lines,
    _omega,
    _projective_points_f3_4,
)


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_parseval_measurement_frame_audit_summary.json"


def _normalize(vector: tuple[int, int, int, int], q: int = 3) -> tuple[int, int, int, int] | None:
    reduced = tuple(entry % q for entry in vector)
    if not any(reduced):
        return None
    for entry in reduced:
        if entry:
            inv = 1 if entry == 1 else 2
            return tuple((inv * value) % q for value in reduced)
    raise AssertionError("Unreachable normalization state.")


def _projective_line_from_pair(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
    q: int = 3,
) -> frozenset[tuple[int, int, int, int]]:
    line: set[tuple[int, int, int, int]] = set()
    for a, b in product(range(q), repeat=2):
        if a == 0 and b == 0:
            continue
        vector = tuple((a * left[index] + b * right[index]) % q for index in range(4))
        point = _normalize(vector, q=q)
        if point is not None:
            line.add(point)
    return frozenset(line)


def _all_projective_lines(
    points: list[tuple[int, int, int, int]],
) -> list[frozenset[tuple[int, int, int, int]]]:
    lines: set[frozenset[tuple[int, int, int, int]]] = set()
    for left, right in combinations(points, 2):
        line = _projective_line_from_pair(left, right)
        if len(line) == 4:
            lines.add(line)
    return sorted(lines, key=lambda line: tuple(sorted(line)))


def _projective_line_split(
    points: list[tuple[int, int, int, int]],
) -> tuple[
    list[frozenset[tuple[int, int, int, int]]],
    list[frozenset[tuple[int, int, int, int]]],
]:
    isotropic: list[frozenset[tuple[int, int, int, int]]] = []
    anti_lines: list[frozenset[tuple[int, int, int, int]]] = []
    for line in _all_projective_lines(points):
        left, right = sorted(line)[:2]
        if _omega(left, right) == 0:
            isotropic.append(line)
        else:
            anti_lines.append(line)
    return isotropic, anti_lines


def _distribution(values: np.ndarray) -> dict[int, int]:
    return dict(sorted(Counter(int(value) for value in np.asarray(values).ravel()).items()))


def _spectrum(matrix: np.ndarray) -> dict[int, int]:
    eigenvalues = np.rint(np.linalg.eigvalsh(matrix.astype(float))).astype(int)
    return dict(sorted(Counter(int(value) for value in eigenvalues).items()))


@lru_cache(maxsize=1)
def _build_parseval_probe_data() -> dict[str, Any]:
    points = _projective_points_f3_4()
    point_index = {point: index for index, point in enumerate(points)}

    true_lines = _build_lines()
    spreads = _all_spreads(true_lines)
    isotropic_projective_lines, anti_projective_lines = _projective_line_split(points)

    isotropic_index_lines = sorted(
        tuple(sorted(point_index[point] for point in line)) for line in isotropic_projective_lines
    )
    if isotropic_index_lines != true_lines:
        raise AssertionError("Projective 40-line split does not match the canonical true-line carrier.")

    B = np.zeros((40, 36), dtype=int)
    for spread_index, spread in enumerate(spreads):
        for line_index in spread:
            B[line_index, spread_index] = 1

    anti_line_sets = [set(point_index[point] for point in line) for line in anti_projective_lines]
    R = np.zeros((40, 90), dtype=int)
    for line_index, line in enumerate(true_lines):
        line_set = set(line)
        for anti_index, anti_line in enumerate(anti_line_sets):
            if line_set & anti_line:
                R[line_index, anti_index] = 1

    I40 = np.eye(40, dtype=int)
    J40 = np.ones((40, 40), dtype=int)
    B4 = 4 * B - np.ones((40, 36), dtype=int)
    R5 = 5 * R - 2 * np.ones((40, 90), dtype=int)

    line_disjoint = ((B @ B.T - 9 * I40) // 3).astype(int)
    np.fill_diagonal(line_disjoint, 0)

    B4Bt = B4 @ B4.T
    R5Rt = R5 @ R5.T
    integer_parseval_left = 25 * B4Bt + 8 * R5Rt
    integer_parseval_right = 7200 * I40 - 180 * J40

    mean_vector = np.ones((40, 1), dtype=int)

    return {
        "B": B,
        "R": R,
        "B4": B4,
        "R5": R5,
        "B4Bt": B4Bt,
        "R5Rt": R5Rt,
        "I40": I40,
        "J40": J40,
        "true_lines": true_lines,
        "spreads": spreads,
        "anti_projective_lines": anti_projective_lines,
        "line_disjoint": line_disjoint,
        "integer_parseval_left": integer_parseval_left,
        "integer_parseval_right": integer_parseval_right,
        "B_mean_residual": B4.T @ mean_vector,
        "R_mean_residual": R5.T @ mean_vector,
    }


@lru_cache(maxsize=1)
def build_parseval_measurement_frame_summary() -> dict[str, Any]:
    built = _build_parseval_probe_data()
    B = built["B"]
    R = built["R"]
    B4 = built["B4"]
    R5 = built["R5"]
    B4Bt = built["B4Bt"]
    R5Rt = built["R5Rt"]
    I40 = built["I40"]
    J40 = built["J40"]
    line_disjoint = built["line_disjoint"]

    centered_spread_spectrum = {value // 16: count for value, count in _spectrum(B4Bt).items()}
    centered_anti_line_spectrum = {value // 25: count for value, count in _spectrum(R5Rt).items()}

    checks = {
        "projective_line_split_has_40_true_lines_and_90_anti_lines": (
            len(built["true_lines"]) == 40 and len(built["anti_projective_lines"]) == 90
        ),
        "spread_probe_has_uniform_9_by_10_incidence": (
            B.shape == (40, 36)
            and int(B.sum()) == 360
            and _distribution(B.sum(axis=1)) == {9: 40}
            and _distribution(B.sum(axis=0)) == {10: 36}
        ),
        "anti_line_probe_has_uniform_36_by_16_incidence": (
            R.shape == (40, 90)
            and int(R.sum()) == 1440
            and _distribution(R.sum(axis=1)) == {36: 40}
            and _distribution(R.sum(axis=0)) == {16: 90}
        ),
        "signed_spread_probe_annihilates_the_mean_channel": bool(
            np.array_equal(built["B_mean_residual"], np.zeros((36, 1), dtype=int))
        ),
        "signed_anti_line_probe_annihilates_the_mean_channel": bool(
            np.array_equal(built["R_mean_residual"], np.zeros((90, 1), dtype=int))
        ),
        "parseval_identity_holds_exactly_in_integer_form": bool(
            np.array_equal(built["integer_parseval_left"], built["integer_parseval_right"])
        ),
        "full_identity_resolution_holds_exactly_in_integer_form": bool(
            np.array_equal(built["integer_parseval_left"] + 180 * J40, 7200 * I40)
        ),
        "signed_probe_orthogonality_holds_exactly": bool(
            np.array_equal(B4.T @ R5, np.zeros((36, 90), dtype=int))
        ),
        "signed_spread_probe_has_expected_spectrum": _spectrum(B4Bt) == {0: 25, 288: 15},
        "signed_anti_line_probe_has_expected_spectrum": _spectrum(R5Rt) == {0: 16, 900: 24},
        "line_disjoint_graph_has_expected_1_15_24_spectrum": _spectrum(line_disjoint) == {
            -3: 24,
            3: 15,
            27: 1,
        },
    }

    theorem = {
        "the_36_spreads_and_90_anti_lines_form_an_exact_parseval_measurement_frame_on_the_40_line_module": (
            checks["spread_probe_has_uniform_9_by_10_incidence"]
            and checks["anti_line_probe_has_uniform_36_by_16_incidence"]
            and checks["parseval_identity_holds_exactly_in_integer_form"]
        ),
        "the_centered_spread_probe_carries_exactly_the_line_side_15_sector": (
            checks["signed_spread_probe_annihilates_the_mean_channel"]
            and checks["signed_spread_probe_has_expected_spectrum"]
        ),
        "the_centered_anti_line_probe_carries_exactly_the_line_side_24_sector": (
            checks["signed_anti_line_probe_annihilates_the_mean_channel"]
            and checks["signed_anti_line_probe_has_expected_spectrum"]
        ),
        "the_mean_channel_completes_the_exact_split_1_plus_15_plus_24": (
            checks["signed_probe_orthogonality_holds_exactly"]
            and checks["line_disjoint_graph_has_expected_1_15_24_spectrum"]
            and checks["full_identity_resolution_holds_exactly_in_integer_form"]
        ),
    }

    return {
        "status": "ok",
        "carrier_dictionary": {
            "line_side": "40 = 1 + 15 + 24",
            "projective_line_split": {"total": 130, "true_lines": 40, "anti_lines": 90},
            "spread_probe": {
                "shape": [40, 36],
                "incidence_count": int(B.sum()),
                "density": "1/4",
                "row_degree_distribution": _distribution(B.sum(axis=1)),
                "column_degree_distribution": _distribution(B.sum(axis=0)),
            },
            "anti_line_probe": {
                "shape": [40, 90],
                "incidence_count": int(R.sum()),
                "density": "2/5",
                "row_degree_distribution": _distribution(R.sum(axis=1)),
                "column_degree_distribution": _distribution(R.sum(axis=0)),
            },
        },
        "exact_identities": {
            "centered_spread_probe": "B_c = B - J/4",
            "centered_anti_line_probe": "R_c = R - 2J/5",
            "parseval_identity": "B_c B_c^T / 18 + R_c R_c^T / 36 = I - J/40",
            "full_identity_resolution": "J/40 + B_c B_c^T / 18 + R_c R_c^T / 36 = I",
            "signed_spread_probe": "B_4 = 4B - J",
            "signed_anti_line_probe": "R_5 = 5R - 2J",
            "signed_orthogonality": "B_4^T R_5 = 0",
            "integer_parseval_identity": "25 B_4 B_4^T + 8 R_5 R_5^T = 7200 I - 180 J",
        },
        "spectral_data": {
            "line_disjoint_spectrum": _spectrum(line_disjoint),
            "centered_spread_probe_spectrum": centered_spread_spectrum,
            "centered_anti_line_probe_spectrum": centered_anti_line_spectrum,
            "signed_spread_probe_spectrum": _spectrum(B4Bt),
            "signed_anti_line_probe_spectrum": _spectrum(R5Rt),
        },
        "theorem": theorem,
        "checks": checks,
        "interpretation": (
            "The 36 spread probes recover the exact line-side 15-sector and the 90 anti-lines are the "
            "90 non-isotropic projective lines of PG(3,3) seen from the same true-line carrier by point "
            "intersection. After correct centering, the spread and anti-line channels are orthogonal and "
            "resolve the zero-mean line module exactly, so the full 40-dimensional line carrier splits as "
            "mean + spread features + anti-line features = 1 + 15 + 24."
        ),
    }


def write_summary(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    output_path.write_text(
        json.dumps(build_parseval_measurement_frame_summary(), indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    output_path = write_summary()
    summary = build_parseval_measurement_frame_summary()

    print("=" * 72)
    print("W33 PARSEVAL MEASUREMENT FRAME AUDIT")
    print("=" * 72)
    print(f"wrote: {output_path}")
    for key, value in summary["theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()