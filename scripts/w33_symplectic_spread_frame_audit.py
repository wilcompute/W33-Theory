#!/usr/bin/env python3
"""Exact symplectic-spread / stabilizer-frame audit for W(3,3).

This audit packages the complete spread layer of the exact two-qutrit kernel.

Finite-geometric side:
1. The 40 totally isotropic lines of W(3,3) admit exactly 36 spreads.
2. Each spread is a partition of the 40 points into 10 isotropic lines.
3. Every isotropic line lies in exactly 9 spreads.
4. Fix any anchor point p. Then every spread contains exactly one isotropic
   line through p, so the 36 spreads split uniformly as 4 anchor-line sectors
   of size 9.
5. Relative to the affine shell PG(2,3) + AG(3,3) at p, each spread consists
   of one isotropic line inside p^perp and 9 affine lines, one in each of the
   9 directions not lying on that anchor line.

Quantum-information side:
6. Every spread yields 10 commuting 2-qutrit stabilizer contexts.
7. The 10 joint eigenbases form a complete MUB frame in dimension 9, and this
   is verified numerically for all 36 spreads with machine-precision overlap.

The point is not a full universality claim. It isolates the exact complete
stabilizer-frame layer already present in the kernel.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, Iterable, List, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from scripts.w33_projective_affine_shell_audit import (  # noqa: E402
    isotropic_lines,
    point_perp,
    projective_lines,
    projective_points,
)
from scripts.w33_two_qutrit_pauli import build_pauli_operators  # noqa: E402


Point = Tuple[int, int, int, int]
Spread = Tuple[int, ...]


def isotropic_line_index_by_point(lines: list[tuple[int, ...]], n_points: int = 40) -> list[list[int]]:
    point_to_lines: list[list[int]] = [[] for _ in range(n_points)]
    for index, line in enumerate(lines):
        for point in line:
            point_to_lines[point].append(index)
    return point_to_lines


def line_masks(lines: list[tuple[int, ...]]) -> list[int]:
    masks = []
    for line in lines:
        mask = 0
        for point in line:
            mask |= 1 << point
        masks.append(mask)
    return masks


def symplectic_spreads(lines: list[tuple[int, ...]], n_points: int = 40) -> list[Spread]:
    point_to_lines = isotropic_line_index_by_point(lines, n_points=n_points)
    masks = line_masks(lines)
    full_mask = (1 << n_points) - 1
    found: list[Spread] = []

    def backtrack(chosen: list[int], used_mask: int) -> None:
        if used_mask == full_mask:
            found.append(tuple(sorted(chosen)))
            return

        first_uncovered = ((~used_mask) & full_mask & -((~used_mask) & full_mask)).bit_length() - 1
        for line_index in point_to_lines[first_uncovered]:
            mask = masks[line_index]
            if used_mask & mask:
                continue
            if len(chosen) >= 10:
                continue
            chosen.append(line_index)
            backtrack(chosen, used_mask | mask)
            chosen.pop()

    backtrack([], 0)
    return sorted(set(found))


def qutrit_projector_basis(generator_1: np.ndarray, generator_2: np.ndarray) -> np.ndarray:
    omega = np.exp(2j * np.pi / 3)
    basis = np.zeros((9, 9), dtype=np.complex128)
    column = 0
    for s in range(3):
        for t in range(3):
            projector = np.zeros((9, 9), dtype=np.complex128)
            for i in range(3):
                for j in range(3):
                    projector += (omega ** (-(i * s + j * t))) * (
                        np.linalg.matrix_power(generator_1, i)
                        @ np.linalg.matrix_power(generator_2, j)
                    )
            projector /= 9.0
            norms = np.linalg.norm(projector, axis=0)
            pivot = int(np.argmax(norms))
            vector = projector[:, pivot]
            basis[:, column] = vector / np.linalg.norm(vector)
            column += 1
    qmat, _ = np.linalg.qr(basis)
    return qmat


def mub_max_deviation_for_spread(
    spread: Spread,
    lines: list[tuple[int, ...]],
    point_vectors: list[Point],
    pauli_matrices: dict[Point, np.ndarray],
) -> float:
    bases = []
    for line_index in spread:
        line = lines[line_index]
        generator_1 = pauli_matrices[point_vectors[line[0]]]
        generator_2 = pauli_matrices[point_vectors[line[1]]]
        bases.append(qutrit_projector_basis(generator_1, generator_2))

    target = 1.0 / 9.0
    max_dev = 0.0
    for i in range(len(bases)):
        for j in range(i + 1, len(bases)):
            overlap = bases[i].conj().T @ bases[j]
            dev = float(np.max(np.abs(np.abs(overlap) ** 2 - target)))
            if dev > max_dev:
                max_dev = dev
    return max_dev


def anchor_profile(
    anchor_index: int,
    spreads: list[Spread],
    lines: list[tuple[int, ...]],
    points: list[Point],
) -> dict[str, Any]:
    hyperplane = point_perp(anchor_index, points)
    affine_points = set(range(len(points))) - hyperplane
    anchor_lines = [line_index for line_index, line in enumerate(lines) if anchor_index in line]
    spreads_per_anchor_line = {
        tuple(lines[line_index]): sum(1 for spread in spreads if line_index in spread)
        for line_index in anchor_lines
    }

    spread_profiles = []
    for spread in spreads:
        spread_lines = [lines[index] for index in spread]
        chosen_anchor_lines = [line for line in spread_lines if anchor_index in line]
        if len(chosen_anchor_lines) != 1:
            raise AssertionError("spread does not contain exactly one anchor line")
        anchor_line = chosen_anchor_lines[0]

        affine_direction_points = []
        for line in spread_lines:
            line_set = set(line)
            infinity = line_set & hyperplane
            affine = line_set & affine_points
            if len(infinity) == 1 and len(affine) == 3:
                affine_direction_points.append(next(iter(infinity)))

        spread_profiles.append(
            {
                "anchor_line": anchor_line,
                "lines_inside_hyperplane": sum(1 for line in spread_lines if set(line).issubset(hyperplane)),
                "affine_direction_count": len(set(affine_direction_points)),
                "affine_direction_points": tuple(sorted(affine_direction_points)),
                "expected_affine_direction_points": tuple(sorted(set(hyperplane) - set(anchor_line))),
            }
        )

    return {
        "anchor_index": anchor_index,
        "anchor_point": points[anchor_index],
        "anchor_line_count": len(anchor_lines),
        "anchor_lines": [tuple(lines[line_index]) for line_index in anchor_lines],
        "spreads_per_anchor_line": spreads_per_anchor_line,
        "spread_profiles": spread_profiles,
    }


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    points = projective_points()
    all_isotropic_lines = isotropic_lines(points, projective_lines(points))
    spreads = symplectic_spreads(all_isotropic_lines, n_points=len(points))
    pauli_points, pauli_matrices = build_pauli_operators()

    line_occurrences = Counter()
    for spread in spreads:
        for line_index in spread:
            line_occurrences[line_index] += 1

    anchor_profiles = [anchor_profile(anchor_index, spreads, all_isotropic_lines, points) for anchor_index in range(len(points))]
    mub_deviations = [
        mub_max_deviation_for_spread(spread, all_isotropic_lines, pauli_points, pauli_matrices)
        for spread in spreads
    ]

    theorem = {
        "the_40_isotropic_lines_of_w33_admit_exactly_36_spreads": (
            len(all_isotropic_lines) == 40
            and len(spreads) == 36
            and all(len(spread) == 10 for spread in spreads)
        ),
        "every_spread_is_a_partition_of_the_40_points_into_10_isotropic_lines": (
            all(
                len({point for line_index in spread for point in all_isotropic_lines[line_index]}) == 40
                for spread in spreads
            )
        ),
        "every_isotropic_line_lies_in_exactly_9_spreads": (
            set(line_occurrences.values()) == {9}
            and len(line_occurrences) == 40
        ),
        "for_every_anchor_point_the_36_spreads_split_as_4_anchor_lines_times_9": (
            all(
                profile["anchor_line_count"] == 4
                and set(profile["spreads_per_anchor_line"].values()) == {9}
                for profile in anchor_profiles
            )
        ),
        "for_every_anchor_point_each_spread_is_one_memory_line_plus_9_affine_measurement_lines": (
            all(
                record["lines_inside_hyperplane"] == 1
                and record["affine_direction_count"] == 9
                and record["affine_direction_points"] == record["expected_affine_direction_points"]
                for profile in anchor_profiles
                for record in profile["spread_profiles"]
            )
        ),
        "every_spread_yields_a_complete_2qutrit_stabilizer_mub_frame": (
            len(mub_deviations) == 36
            and max(mub_deviations) < 1e-12
        ),
    }
    theorem["the_symplectic_spread_frame_bridge_is_fully_closed"] = all(theorem.values())

    canonical_anchor_index = points.index((1, 0, 0, 0))
    canonical_anchor = anchor_profiles[canonical_anchor_index]
    canonical_anchor_lines = canonical_anchor["anchor_lines"]
    sector_sizes = Counter()
    for record in canonical_anchor["spread_profiles"]:
        sector_sizes[record["anchor_line"]] += 1

    return {
        "status": "ok",
        "spread_dictionary": {
            "point_count": len(points),
            "isotropic_line_count": len(all_isotropic_lines),
            "spread_count": len(spreads),
            "spread_size": 10,
            "line_occurrence_distribution": dict(Counter(line_occurrences.values())),
            "mub_max_deviation": max(mub_deviations),
            "mub_mean_deviation": float(sum(mub_deviations) / len(mub_deviations)),
        },
        "canonical_anchor_frame": {
            "anchor_index": canonical_anchor["anchor_index"],
            "anchor_point": canonical_anchor["anchor_point"],
            "anchor_lines": canonical_anchor_lines,
            "sector_sizes": {str(key): value for key, value in sector_sizes.items()},
            "sample_spread_profile": canonical_anchor["spread_profiles"][0],
        },
        "symplectic_spread_frame_theorem": theorem,
        "bridge_verdict": (
            "The complete stabilizer-frame layer is now explicit. W(3,3) has exactly "
            "36 symplectic spreads, each spread is a full 10-line partition of the 40-point "
            "kernel, every isotropic line lies in 9 spreads, and relative to any anchor "
            "point each spread is exactly one isotropic memory line at infinity together "
            "with 9 affine measurement lines covering the 9 remaining directions. Every "
            "one of those 36 spreads gives a complete 2-qutrit stabilizer MUB frame in "
            "dimension 9. This closes the exact complete-frame side of the qutrit kernel, "
            "while keeping the non-Clifford/universality boundary honest."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXV_symplectic_spread_frame_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 symplectic-spread frame audit")
    for key, value in payload["symplectic_spread_frame_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
