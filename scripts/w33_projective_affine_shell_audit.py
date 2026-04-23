#!/usr/bin/env python3
"""Exact projective/affine shell audit for W(3,3).

This audit packages one structural bridge that was already implicit in the repo
but not yet isolated as a single exact statement:

1. The 40 projective points of PG(3,3), the 40 non-identity projective
   two-qutrit Pauli classes, and the repo's canonical W33 vertex set are the
   same finite object.
2. The 40 totally isotropic projective lines define the symplectic generalized
   quadrangle W(3,3) = GQ(3,3), whose point graph is SRG(40,12,2,4).
3. For every point p, the symplectic perp p^perp is a projective hyperplane
   PG(2,3) of size 13, and its complement in PG(3,3) is an affine cube AG(3,3)
   of size 27.
4. In a canonical chart anchored at p = (1,0,0,0), the 27 affine points are
   exactly F_3^3, and one affine direction class gives the nine size-3 fibers
   already seen in the local H27 qutrit shell.

The point is not to invent new phenomenology. It is to explain the exact local
13 + 27 shell in the strongest finite-geometric language the repo already
supports.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, Iterable, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
for candidate in (ROOT, SCRIPTS):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from scripts.w33_homology import build_w33  # noqa: E402
from scripts.w33_two_qutrit_pauli import (  # noqa: E402
    build_commutation_graph,
    build_pauli_operators,
    find_isomorphism,
    symplectic_form,
)


F = (0, 1, 2)
Point = Tuple[int, int, int, int]


def canonical_projective_point(vector: Iterable[int]) -> Point:
    values = tuple(int(entry) % 3 for entry in vector)
    for value in values:
        if value != 0:
            inverse = 1 if value == 1 else 2
            return tuple((inverse * entry) % 3 for entry in values)
    raise ValueError("zero vector has no projective representative")


def projective_points() -> list[Point]:
    points: list[Point] = []
    seen: set[Point] = set()
    for vector in product(F, repeat=4):
        if vector == (0, 0, 0, 0):
            continue
        point = canonical_projective_point(vector)
        if point not in seen:
            seen.add(point)
            points.append(point)
    return sorted(points)


def canonical_projective_line(left: Point, right: Point) -> tuple[Point, ...]:
    members = {
        canonical_projective_point(
            (
                a * left[0] + b * right[0],
                a * left[1] + b * right[1],
                a * left[2] + b * right[2],
                a * left[3] + b * right[3],
            )
        )
        for a, b in product(F, repeat=2)
        if not (a == 0 and b == 0)
    }
    return tuple(sorted(members))


def projective_lines(points: list[Point]) -> list[tuple[int, ...]]:
    index = {point: idx for idx, point in enumerate(points)}
    lines = {
        tuple(sorted(index[member] for member in canonical_projective_line(points[i], points[j])))
        for i, j in combinations(range(len(points)), 2)
    }
    return sorted(lines)


def isotropic_lines(points: list[Point], all_lines: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    return [
        line
        for line in all_lines
        if all(symplectic_form(points[i], points[j]) == 0 for i, j in combinations(line, 2))
    ]


def adjacency_from_symplectic(points: list[Point]) -> list[list[int]]:
    adjacency = [[] for _ in range(len(points))]
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if symplectic_form(points[i], points[j]) == 0:
                adjacency[i].append(j)
                adjacency[j].append(i)
    return adjacency


def strongly_regular_parameters(adjacency: list[list[int]]) -> dict[str, int]:
    adjacency_sets = [set(neighbors) for neighbors in adjacency]
    degrees = {len(neighbors) for neighbors in adjacency}
    lambda_values = set()
    mu_values = set()
    for i, j in combinations(range(len(adjacency)), 2):
        common = len(adjacency_sets[i] & adjacency_sets[j])
        if j in adjacency_sets[i]:
            lambda_values.add(common)
        else:
            mu_values.add(common)
    return {
        "n": len(adjacency),
        "k": next(iter(degrees)),
        "lambda": next(iter(lambda_values)),
        "mu": next(iter(mu_values)),
    }


def point_perp(index: int, points: list[Point]) -> set[int]:
    base = points[index]
    return {j for j, point in enumerate(points) if symplectic_form(base, point) == 0}


def point_degrees_on_lines(lines: list[tuple[int, ...]], point_indices: set[int]) -> tuple[int, ...]:
    counts = Counter()
    for line in lines:
        line_set = set(line)
        if line_set.issubset(point_indices):
            for point in line:
                counts[point] += 1
    return tuple(sorted(set(counts.values())))


def hyperplane_and_affine_profile(
    anchor_index: int,
    points: list[Point],
    all_projective_lines: list[tuple[int, ...]],
    all_isotropic_lines: list[tuple[int, ...]],
) -> dict[str, Any]:
    hyperplane = point_perp(anchor_index, points)
    affine_points = set(range(len(points))) - hyperplane

    hyperplane_lines = [line for line in all_projective_lines if set(line).issubset(hyperplane)]
    isotropic_through_anchor = [line for line in all_isotropic_lines if anchor_index in line]

    affine_lines = []
    direction_counts = Counter()
    affine_point_line_counts = Counter()
    for line in all_projective_lines:
        line_set = set(line)
        infinity_points = line_set & hyperplane
        affine_part = line_set & affine_points
        if len(infinity_points) == 1 and len(affine_part) == 3:
            direction = next(iter(infinity_points))
            affine_line = tuple(sorted(affine_part))
            affine_lines.append((affine_line, direction))
            direction_counts[direction] += 1
            for point in affine_line:
                affine_point_line_counts[point] += 1

    return {
        "anchor_index": anchor_index,
        "anchor_point": points[anchor_index],
        "hyperplane_size": len(hyperplane),
        "hyperplane_projective_line_count": len(hyperplane_lines),
        "hyperplane_line_size_set": sorted({len(line) for line in hyperplane_lines}),
        "hyperplane_point_projective_line_degrees": point_degrees_on_lines(hyperplane_lines, hyperplane),
        "isotropic_lines_through_anchor": len(isotropic_through_anchor),
        "commuting_neighbors": len(hyperplane) - 1,
        "affine_point_count": len(affine_points),
        "affine_line_count": len(affine_lines),
        "affine_line_size_set": sorted({len(line) for line, _ in affine_lines}),
        "affine_direction_count": len(direction_counts),
        "affine_lines_per_direction": sorted(set(direction_counts.values())),
        "affine_lines_per_point": sorted(set(affine_point_line_counts.values())),
    }


def canonical_anchor_chart(
    points: list[Point],
    all_projective_lines: list[tuple[int, ...]],
) -> dict[str, Any]:
    anchor = (1, 0, 0, 0)
    direction_at_infinity = (0, 0, 0, 1)
    point_index = {point: idx for idx, point in enumerate(points)}
    anchor_index = point_index[anchor]
    hyperplane = point_perp(anchor_index, points)
    affine_points = sorted(set(range(len(points))) - hyperplane)

    coords_to_point: dict[tuple[int, int, int], int] = {}
    for point_index_in_affine in affine_points:
        point = points[point_index_in_affine]
        if point[1] == 0:
            raise AssertionError("affine point unexpectedly lies in the hyperplane")
        inverse = 1 if point[1] == 1 else 2
        scaled = tuple((inverse * entry) % 3 for entry in point)
        coordinate = (scaled[0], scaled[2], scaled[3])
        coords_to_point[coordinate] = point_index_in_affine

    fibers = []
    line_lookup = {tuple(sorted(line)) for line in all_projective_lines}
    direction_index = point_index[direction_at_infinity]
    for x_coord in F:
        for y_coord in F:
            fiber_points = tuple(
                sorted(coords_to_point[(x_coord, y_coord, z_coord)] for z_coord in F)
            )
            line = tuple(sorted(fiber_points + (direction_index,)))
            fibers.append(
                {
                    "coordinate_pair": (x_coord, y_coord),
                    "fiber_points": fiber_points,
                    "line_exists_in_pg33": line in line_lookup,
                }
            )

    return {
        "anchor_point": anchor,
        "anchor_index": anchor_index,
        "direction_at_infinity": direction_at_infinity,
        "coordinate_count": len(coords_to_point),
        "coordinates_cover_f3_cube": set(coords_to_point) == set(product(F, repeat=3)),
        "fiber_count": len(fibers),
        "fiber_size_set": sorted({len(record["fiber_points"]) for record in fibers}),
        "all_fibers_extend_to_projective_lines": all(
            record["line_exists_in_pg33"] for record in fibers
        ),
        "sample_fibers": fibers[:3],
    }


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    points = projective_points()
    all_projective_lines = projective_lines(points)
    all_isotropic_lines = isotropic_lines(points, all_projective_lines)
    adjacency = adjacency_from_symplectic(points)
    pauli_points, _ = build_pauli_operators()
    pauli_adjacency = build_commutation_graph(points)
    repo_n, repo_vertices, repo_adjacency, repo_edges = build_w33()
    identity_iso, mismatches = find_isomorphism(points, pauli_adjacency)

    hyperplane_profiles = [
        hyperplane_and_affine_profile(i, points, all_projective_lines, all_isotropic_lines)
        for i in range(len(points))
    ]
    anchor_chart = canonical_anchor_chart(points, all_projective_lines)
    srg = strongly_regular_parameters(adjacency)

    theorem = {
        "the_40_points_of_pg_3_3_match_the_repo_w33_vertices_and_projective_two_qutrit_pauli_points": (
            len(points) == 40
            and points == pauli_points
            and sorted(points) == sorted(repo_vertices)
            and identity_iso is True
            and mismatches == 0
        ),
        "the_40_totally_isotropic_lines_form_the_symplectic_generalized_quadrangle_gq_3_3": (
            len(all_isotropic_lines) == 40
            and all(len(line) == 4 for line in all_isotropic_lines)
            and all(profile["isotropic_lines_through_anchor"] == 4 for profile in hyperplane_profiles)
        ),
        "the_point_graph_is_exactly_srg_40_12_2_4": (
            srg == {"n": 40, "k": 12, "lambda": 2, "mu": 4}
            and len(repo_edges) == 240
            and all(len(neighbors) == 12 for neighbors in adjacency)
        ),
        "every_point_perp_is_a_pg_2_3_hyperplane_of_size_13": (
            all(
                profile["hyperplane_size"] == 13
                and profile["hyperplane_projective_line_count"] == 13
                and profile["hyperplane_line_size_set"] == [4]
                and profile["hyperplane_point_projective_line_degrees"] == (4,)
                for profile in hyperplane_profiles
            )
        ),
        "every_hyperplane_complement_is_an_ag_3_3_affine_cube_of_size_27": (
            all(
                profile["affine_point_count"] == 27
                and profile["affine_line_count"] == 117
                and profile["affine_line_size_set"] == [3]
                and profile["affine_lines_per_point"] == [13]
                for profile in hyperplane_profiles
            )
        ),
        "every_affine_cube_has_exactly_13_direction_classes_of_9_parallel_lines": (
            all(
                profile["affine_direction_count"] == 13
                and profile["affine_lines_per_direction"] == [9]
                for profile in hyperplane_profiles
            )
        ),
        "the_canonical_anchor_chart_recovers_f3_cubed_and_the_9_times_3_fiber_packet": (
            anchor_chart["coordinate_count"] == 27
            and anchor_chart["coordinates_cover_f3_cube"] is True
            and anchor_chart["fiber_count"] == 9
            and anchor_chart["fiber_size_set"] == [3]
            and anchor_chart["all_fibers_extend_to_projective_lines"] is True
        ),
    }
    theorem["the_projective_affine_shell_bridge_is_fully_closed"] = all(theorem.values())

    return {
        "status": "ok",
        "notation_note": (
            "The classical symplectic generalized quadrangle is often written W(3,3) "
            "or W(3) depending on convention. In repo notation, W(3,3) refers to the "
            "q=3 case inside PG(3,3)."
        ),
        "projective_space": {
            "point_count": len(points),
            "projective_line_count": len(all_projective_lines),
            "projective_line_size_set": sorted({len(line) for line in all_projective_lines}),
        },
        "symplectic_generalized_quadrangle": {
            "isotropic_line_count": len(all_isotropic_lines),
            "isotropic_line_size_set": sorted({len(line) for line in all_isotropic_lines}),
            "point_graph_parameters": srg,
            "repo_w33_edge_count": len(repo_edges),
            "repo_vertex_count": repo_n,
            "repo_adjacency_matches_symplectic_point_graph": adjacency == repo_adjacency,
        },
        "canonical_pauli_bridge": {
            "point_count": len(pauli_points),
            "identity_isomorphism_to_repo_w33": identity_iso,
            "mismatching_vertices": mismatches,
        },
        "hyperplane_profiles": {
            "distinct_hyperplane_sizes": sorted({profile["hyperplane_size"] for profile in hyperplane_profiles}),
            "distinct_hyperplane_line_counts": sorted(
                {profile["hyperplane_projective_line_count"] for profile in hyperplane_profiles}
            ),
            "distinct_isotropic_line_counts_through_anchor": sorted(
                {profile["isotropic_lines_through_anchor"] for profile in hyperplane_profiles}
            ),
            "distinct_affine_point_counts": sorted(
                {profile["affine_point_count"] for profile in hyperplane_profiles}
            ),
            "distinct_affine_line_counts": sorted(
                {profile["affine_line_count"] for profile in hyperplane_profiles}
            ),
            "distinct_affine_direction_counts": sorted(
                {profile["affine_direction_count"] for profile in hyperplane_profiles}
            ),
        },
        "canonical_anchor_chart": anchor_chart,
        "projective_affine_shell_theorem": theorem,
        "bridge_verdict": (
            "The local qutrit shell is exactly a projective/affine decomposition. "
            "Around every point, the commuting screen is the 13-point tangent "
            "hyperplane PG(2,3), while the 27 non-commuting bulk is the affine "
            "cube AG(3,3). In the canonical anchor chart this affine bulk is "
            "literally F_3^3, and the nine size-3 fibers already isolated in the "
            "repo are one affine direction class. So the exact H27 shell is not "
            "just a count; it is the affine ternary bulk of the symplectic "
            "generalized quadrangle."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXIV_projective_affine_shell_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 projective/affine shell audit")
    for key, value in payload["projective_affine_shell_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
