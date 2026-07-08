#!/usr/bin/env python3
"""Pass 104: lift W33 local octahedron axes to signed E8 roots.

For a W33 point p, the four lines through p form a local K4 pencil.  Each
of its three perfect matchings is an axis of the local pencil octahedron.
Either endpoint of such an axis is a pair of pencil lines.  Removing p from
their union gives a weight-6 binary word.  The two endpoint words differ by
the neighborhood word of p, hence define the same class in C^perp/C.

This verifier proves that these 120 intrinsic axes are exactly the 120
anisotropic glue classes from Passes 92/101.  It then constructs a
deterministic quadratic-space isometry to E8/2E8 in the exact tetracode E8
coordinates already present in the repository.  The two endpoints of every
axis are assigned the two signed roots in the corresponding root line.

The intrinsic axis-to-coset map is canonical under relabeling.  The final
coordinate lift uses deterministic hyperbolic bases and a chamber, so it is
an explicit gauge choice rather than a canonical coordinate system.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Callable, Iterable

import numpy as np

from analysis.w33_axes_e8_rootline_spectral_bridge import (
    build_w33,
    matchings_of_four,
    w33_axis_incidence,
)
from analysis.w33_tetracode_e8_root_system_bridge import (
    CHAMBER_VECTOR,
    Vector,
    e8_roots_from_w33_tetracode,
    inner,
    simple_roots_from_chamber,
    vector_to_str,
)
from w33_pass92_discriminant_e8 import nullspace_basis, rowspace_basis, to_int

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "w33_pass123_axis_glue_e8_lift.json"


def reduce_mod_basis(vector: int, basis: Iterable[int]) -> int:
    reduced = vector
    for pivot in basis:
        reduced = min(reduced, reduced ^ pivot)
    return reduced


def bit_support(vector: int, length: int = 40) -> list[int]:
    return [index for index in range(length) if (vector >> index) & 1]


def bit_string(vector: int, length: int = 8) -> str:
    return format(vector, f"0{length}b")


def gf2_rank(vectors: Iterable[int]) -> int:
    return len(rowspace_basis(list(vectors)))


def build_code_and_quotient() -> dict[str, Any]:
    points, edges, adjacency, lines, point_lines, edge_to_line = build_w33()
    adjacency_matrix = np.array(adjacency, dtype=np.int64)
    neighborhood_words = [to_int(adjacency_matrix[row]) for row in range(40)]
    code_basis = rowspace_basis(neighborhood_words)
    dual_basis = nullspace_basis(adjacency_matrix)

    combined = list(code_basis)
    glue_basis: list[int] = []
    for vector in dual_basis:
        reduced = reduce_mod_basis(vector, combined)
        if reduced:
            combined.append(reduced)
            combined.sort(reverse=True)
            glue_basis.append(vector)

    quotient_representatives: dict[int, int] = {}
    canonical_to_coordinate: dict[int, int] = {}
    for coordinate in range(256):
        representative = 0
        for index, vector in enumerate(glue_basis):
            if (coordinate >> index) & 1:
                representative ^= vector
        canonical = reduce_mod_basis(representative, code_basis)
        quotient_representatives[coordinate] = representative
        canonical_to_coordinate[canonical] = coordinate

    return {
        "points": points,
        "edges": edges,
        "adjacency": adjacency,
        "lines": lines,
        "point_lines": point_lines,
        "edge_to_line": edge_to_line,
        "neighborhood_words": neighborhood_words,
        "code_basis": code_basis,
        "dual_basis": dual_basis,
        "glue_basis": glue_basis,
        "quotient_representatives": quotient_representatives,
        "canonical_to_coordinate": canonical_to_coordinate,
    }


def axis_glue_records(code_data: dict[str, Any]) -> list[dict[str, Any]]:
    lines = code_data["lines"]
    point_lines = code_data["point_lines"]
    code_basis = code_data["code_basis"]
    canonical_to_coordinate = code_data["canonical_to_coordinate"]

    records: list[dict[str, Any]] = []
    for point in range(40):
        for matching in matchings_of_four(sorted(point_lines[point])):
            endpoint_words: list[int] = []
            endpoint_supports: list[list[int]] = []
            for line_pair in matching:
                support = (set(lines[line_pair[0]]) | set(lines[line_pair[1]])) - {
                    point
                }
                word = sum(1 << vertex for vertex in support)
                endpoint_words.append(word)
                endpoint_supports.append(sorted(support))

            canonical = reduce_mod_basis(endpoint_words[0], code_basis)
            second_canonical = reduce_mod_basis(endpoint_words[1], code_basis)
            if canonical != second_canonical:
                raise AssertionError("axis endpoints must define one quotient class")

            records.append(
                {
                    "point": point,
                    "line_pairs": [list(pair) for pair in matching],
                    "endpoint_words": endpoint_words,
                    "endpoint_supports": endpoint_supports,
                    "canonical_coset": canonical,
                    "quotient_coordinate": canonical_to_coordinate[canonical],
                }
            )
    return records


def quadratic_from_representatives(
    representatives: dict[int, int],
) -> tuple[Callable[[int], int], Callable[[int, int], int]]:
    def quadratic(vector: int) -> int:
        return (representatives[vector].bit_count() // 2) % 2

    def bilinear(left: int, right: int) -> int:
        return (representatives[left] & representatives[right]).bit_count() % 2

    return quadratic, bilinear


def vector_coefficients(vector: Vector, basis: list[Vector]) -> tuple[int, ...]:
    augmented = [
        [basis[column][row] for column in range(8)] + [vector[row]] for row in range(8)
    ]
    for column in range(8):
        pivot = next(row for row in range(column, 8) if augmented[row][column] != 0)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(8):
            if row == column or augmented[row][column] == 0:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][index] - factor * augmented[column][index]
                for index in range(9)
            ]
    coefficients = tuple(augmented[index][8] for index in range(8))
    if any(value.denominator != 1 for value in coefficients):
        raise AssertionError("E8 root is not integral in the simple-root basis")
    return tuple(int(value) for value in coefficients)


def root_mod2_data() -> dict[str, Any]:
    roots = sorted(e8_roots_from_w33_tetracode())
    simple_roots = simple_roots_from_chamber(roots)
    cartan = [
        [int(inner(left, right)) for right in simple_roots] for left in simple_roots
    ]

    root_lines: dict[int, list[Vector]] = defaultdict(list)
    coefficients: dict[Vector, tuple[int, ...]] = {}
    for root in roots:
        coeffs = vector_coefficients(root, simple_roots)
        coefficients[root] = coeffs
        residue = sum((value % 2) << index for index, value in enumerate(coeffs))
        root_lines[residue].append(root)

    def lattice_vector(residue: int) -> Vector:
        return tuple(
            sum(
                (
                    simple_roots[index][coordinate]
                    for index in range(8)
                    if (residue >> index) & 1
                ),
                Fraction(0),
            )
            for coordinate in range(8)
        )

    def quadratic(residue: int) -> int:
        vector = lattice_vector(residue)
        return int(inner(vector, vector) / 2) % 2

    def bilinear(left: int, right: int) -> int:
        return (
            sum(
                ((left >> row) & 1) * ((right >> column) & 1) * cartan[row][column]
                for row in range(8)
                for column in range(8)
            )
            % 2
        )

    positive_by_residue: dict[int, Vector] = {}
    for residue, pair in root_lines.items():
        if len(pair) != 2 or pair[0] != tuple(-entry for entry in pair[1]):
            raise AssertionError("each root residue must be one antipodal pair")
        positive = next(root for root in pair if inner(CHAMBER_VECTOR, root) > 0)
        positive_by_residue[residue] = positive

    return {
        "roots": roots,
        "simple_roots": simple_roots,
        "cartan": cartan,
        "coefficients": coefficients,
        "root_lines": dict(root_lines),
        "positive_by_residue": positive_by_residue,
        "quadratic": quadratic,
        "bilinear": bilinear,
    }


def find_hyperbolic_basis(
    quadratic: Callable[[int], int],
    bilinear: Callable[[int, int], int],
) -> list[int]:
    def search(chosen: list[int]) -> list[int] | None:
        if len(chosen) == 8:
            return chosen

        candidates = [
            vector
            for vector in range(1, 256)
            if gf2_rank(chosen + [vector]) == len(chosen) + 1
            and all(bilinear(vector, previous) == 0 for previous in chosen)
            and quadratic(vector) == 0
        ]
        for first in candidates:
            seconds = [
                vector
                for vector in range(1, 256)
                if gf2_rank(chosen + [first, vector]) == len(chosen) + 2
                and all(bilinear(vector, previous) == 0 for previous in chosen)
                and bilinear(first, vector) == 1
                and quadratic(vector) == 0
            ]
            for second in seconds:
                result = search(chosen + [first, second])
                if result is not None:
                    return result
        return None

    basis = search([])
    if basis is None:
        raise AssertionError("failed to construct a hyperbolic basis")
    return basis


def coordinate_lookup(basis: list[int]) -> dict[int, int]:
    lookup: dict[int, int] = {}
    for mask in range(256):
        vector = 0
        for index, basis_vector in enumerate(basis):
            if (mask >> index) & 1:
                vector ^= basis_vector
        lookup[vector] = mask
    if len(lookup) != 256:
        raise AssertionError("basis coordinate lookup is not bijective")
    return lookup


def build_isometry(
    source_quadratic: Callable[[int], int],
    source_bilinear: Callable[[int, int], int],
    target_quadratic: Callable[[int], int],
    target_bilinear: Callable[[int, int], int],
) -> dict[str, Any]:
    source_basis = find_hyperbolic_basis(source_quadratic, source_bilinear)
    target_basis = find_hyperbolic_basis(target_quadratic, target_bilinear)
    source_coordinates = coordinate_lookup(source_basis)

    def transform(vector: int) -> int:
        mask = source_coordinates[vector]
        image = 0
        for index, basis_vector in enumerate(target_basis):
            if (mask >> index) & 1:
                image ^= basis_vector
        return image

    images = {vector: transform(vector) for vector in range(256)}
    return {
        "source_hyperbolic_basis": source_basis,
        "target_hyperbolic_basis": target_basis,
        "images": images,
        "transform": transform,
    }


def counter_json(counter: Counter[Any]) -> dict[str, int]:
    return {
        str(key): value
        for key, value in sorted(counter.items(), key=lambda item: str(item[0]))
    }


def main() -> int:
    code_data = build_code_and_quotient()
    axis_records = axis_glue_records(code_data)
    source_quadratic, source_bilinear = quadratic_from_representatives(
        code_data["quotient_representatives"]
    )
    root_data = root_mod2_data()
    isometry = build_isometry(
        source_quadratic,
        source_bilinear,
        root_data["quadratic"],
        root_data["bilinear"],
    )
    transform = isometry["transform"]

    axis_coordinates = [record["quotient_coordinate"] for record in axis_records]
    root_residues = [transform(coordinate) for coordinate in axis_coordinates]

    signed_roots: list[Vector] = []
    for record, residue in zip(axis_records, root_residues):
        positive = root_data["positive_by_residue"][residue]
        negative = tuple(-entry for entry in positive)
        record["root_residue"] = residue
        record["positive_root"] = positive
        record["negative_root"] = negative
        signed_roots.extend([positive, negative])

    axis_incidence, *_ = w33_axis_incidence()
    axis_graph = (axis_incidence @ axis_incidence.T > 0).astype(np.int64)
    np.fill_diagonal(axis_graph, 0)

    quotient_graph = np.zeros((120, 120), dtype=np.int64)
    root_graph = np.zeros((120, 120), dtype=np.int64)
    for left, right in combinations(range(120), 2):
        if source_bilinear(axis_coordinates[left], axis_coordinates[right]) == 0:
            quotient_graph[left, right] = quotient_graph[right, left] = 1
        if (
            inner(
                axis_records[left]["positive_root"],
                axis_records[right]["positive_root"],
            )
            == 0
        ):
            root_graph[left, right] = root_graph[right, left] = 1

    endpoint_words = [
        word for record in axis_records for word in record["endpoint_words"]
    ]
    code_basis = code_data["code_basis"]
    dual_basis = code_data["dual_basis"]
    neighborhood_words = code_data["neighborhood_words"]

    signed_inner_profile = Counter(
        inner(left, right) for left in signed_roots for right in signed_roots
    )
    root_line_abs_profile = Counter(
        abs(
            inner(
                axis_records[left]["positive_root"],
                axis_records[right]["positive_root"],
            )
        )
        for left, right in combinations(range(120), 2)
    )

    source_q_profile = Counter(source_quadratic(vector) for vector in range(256))
    target_q_profile = Counter(root_data["quadratic"](vector) for vector in range(256))
    isometry_quadratic_failures = sum(
        source_quadratic(vector) != root_data["quadratic"](isometry["images"][vector])
        for vector in range(256)
    )
    isometry_bilinear_failures = sum(
        source_bilinear(left, right)
        != root_data["bilinear"](isometry["images"][left], isometry["images"][right])
        for left in range(256)
        for right in range(256)
    )

    checks = {
        "w33_code_dimensions_16_24_quotient_8": (
            len(code_basis) == 16
            and len(dual_basis) == 24
            and len(code_data["glue_basis"]) == 8
        ),
        "axis_count_120": len(axis_records) == 120,
        "endpoint_count_240_weight_6": (
            len(endpoint_words) == 240
            and Counter(word.bit_count() for word in endpoint_words) == {6: 240}
        ),
        "endpoint_words_lie_in_Cperp": all(
            all((word & codeword).bit_count() % 2 == 0 for codeword in code_basis)
            for word in endpoint_words
        ),
        "opposite_endpoints_differ_by_neighborhood_codeword": all(
            record["endpoint_words"][0] ^ record["endpoint_words"][1]
            == neighborhood_words[record["point"]]
            for record in axis_records
        ),
        "opposite_endpoints_define_same_coset": all(
            reduce_mod_basis(record["endpoint_words"][0], code_basis)
            == reduce_mod_basis(record["endpoint_words"][1], code_basis)
            for record in axis_records
        ),
        "axis_cosets_are_120_distinct_anisotropic_classes": (
            len(set(axis_coordinates)) == 120
            and all(source_quadratic(vector) == 1 for vector in axis_coordinates)
        ),
        "axis_graph_equals_coset_pairing_graph_entrywise": np.array_equal(
            axis_graph, quotient_graph
        ),
        "source_and_target_forms_have_136_120_split": (
            source_q_profile == {0: 136, 1: 120}
            and target_q_profile == {0: 136, 1: 120}
        ),
        "explicit_map_is_linear_bijection": (
            len(set(isometry["images"].values())) == 256
            and all(
                isometry["images"][left ^ right]
                == isometry["images"][left] ^ isometry["images"][right]
                for left in range(256)
                for right in range(256)
            )
        ),
        "explicit_map_preserves_quadratic_form": isometry_quadratic_failures == 0,
        "explicit_map_preserves_bilinear_form": isometry_bilinear_failures == 0,
        "root_residues_are_120_distinct_root_lines": (
            len(set(root_residues)) == 120
            and set(root_residues) == set(root_data["root_lines"])
        ),
        "axis_graph_equals_E8_rootline_orthogonality_entrywise": np.array_equal(
            axis_graph, root_graph
        ),
        "signed_axis_end_lift_is_full_E8_root_system": (
            len(signed_roots) == 240 and set(signed_roots) == set(root_data["roots"])
        ),
        "signed_inner_product_profile_is_E8": signed_inner_profile
        == {-2: 240, -1: 13440, 0: 30240, 1: 13440, 2: 240},
        "root_line_absolute_profile": root_line_abs_profile == {0: 3780, 1: 3360},
    }

    coordinate_images = [
        bit_string(isometry["images"][1 << column]) for column in range(8)
    ]
    payload = {
        "schema": "w33.pass104.axis_glue_e8_lift.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "The 120 W33 local pencil-octahedron axes are exactly the 120 "
            "anisotropic classes of Cperp/C; their 240 endpoints lift to the "
            "240 signed roots of the repository's exact tetracode E8."
        ),
        "code": {
            "C_dimension": len(code_basis),
            "Cperp_dimension": len(dual_basis),
            "quotient_dimension": len(code_data["glue_basis"]),
            "quotient_order": len(code_data["quotient_representatives"]),
            "quadratic_profile": counter_json(source_q_profile),
        },
        "intrinsic_axis_map": {
            "points": 40,
            "axes_per_point": 3,
            "axes": len(axis_records),
            "axis_endpoints": len(endpoint_words),
            "endpoint_weight_profile": counter_json(
                Counter(word.bit_count() for word in endpoint_words)
            ),
            "distinct_anisotropic_cosets": len(set(axis_coordinates)),
            "axis_graph_parameters": [120, 63, 30, 36],
            "construction": (
                "For an axis endpoint {L_i,L_j} at p, use "
                "(L_i union L_j) minus {p}. The opposite endpoint differs by "
                "the 12-neighbor word of p, which lies in C."
            ),
        },
        "quadratic_isometry": {
            "source_hyperbolic_basis": [
                bit_string(vector) for vector in isometry["source_hyperbolic_basis"]
            ],
            "target_hyperbolic_basis": [
                bit_string(vector) for vector in isometry["target_hyperbolic_basis"]
            ],
            "images_of_source_coordinate_basis": coordinate_images,
            "quadratic_failures": isometry_quadratic_failures,
            "bilinear_failures": isometry_bilinear_failures,
            "gauge_note": (
                "The hyperbolic bases are the lexicographically first bases "
                "found in the current deterministic labelings."
            ),
        },
        "e8_lift": {
            "root_lines": len(set(root_residues)),
            "signed_roots": len(set(signed_roots)),
            "simple_roots": [vector_to_str(root) for root in root_data["simple_roots"]],
            "cartan_matrix": root_data["cartan"],
            "signed_ordered_inner_product_profile": counter_json(signed_inner_profile),
            "root_line_unordered_absolute_inner_product_profile": counter_json(
                root_line_abs_profile
            ),
        },
        "axis_root_table": [
            {
                "axis_id": axis_id,
                "point": record["point"],
                "line_pairs": record["line_pairs"],
                "endpoint_supports": record["endpoint_supports"],
                "quotient_coordinate": bit_string(record["quotient_coordinate"]),
                "root_residue": bit_string(record["root_residue"]),
                "positive_root": vector_to_str(record["positive_root"]),
                "negative_root": vector_to_str(record["negative_root"]),
            }
            for axis_id, record in enumerate(axis_records)
        ],
        "claim_boundary": (
            "This closes the previously open local-axis/root-line bridge. "
            "It does not identify the 240 global W33 edges with roots: the "
            "repository's line-graph degree and W(E6)-orbit no-go results "
            "still apply. The exact 240 carrier here is the two endpoints of "
            "each of the 120 local pencil-octahedron axes. Root signs and "
            "coordinates require the displayed chamber/isometry gauge."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {key: payload[key] for key in ("schema", "status", "theorem")}, indent=2
        )
    )
    print(f"checks: {sum(checks.values())}/{len(checks)}")
    print(f"wrote: {OUT}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
