"""W(3,3) BREAKTHROUGH 324: selector affine fiber law.

BT323 proved that the eight kappa-pulled Q4 selectors have intersection
geometry

    disjointness graph = K4 disjoint-union K4,
    two-overlap graph  = K4,4.

BT324 explains why.  View the even half of Q4 as the 3-dimensional vector
space F_2^3 in basis [3, 5, 9], and label the four Q4 coordinate directions by
F_2^2:

    1 -> 00, 2 -> 10, 4 -> 01, 8 -> 11.

Every selector matching is then a rank-2 affine map

    f: F_2^3 -> F_2^2

assigning to each even vertex the direction of its matched Q4 edge.  All eight
maps share the same diagonal kernel <111>.  Consequently the raw eight even
vertices collapse to four quotient route cells, and the selector orbit is
exactly

    two linear projections x four translations.

Equal linear projection gives one disjoint K4 fiber.  Distinct linear
projection gives the cross-fiber K4,4 two-overlap graph.  The finite selector
route is therefore an affine quotient law, not just an observed intersection
pattern.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_323_all_selector_kappa_pullback_orbit import (  # noqa: E402
    all_selector_kappa_pullback_orbit_packet,
)


Q = 3
MU = 4
OCTONION = 8
EVEN_BASIS_WORDS = (3, 5, 9)
DOMAIN = tuple(itertools.product((0, 1), repeat=3))
DIRECTION_LABELS = {
    1: (0, 0),
    2: (1, 0),
    4: (0, 1),
    8: (1, 1),
}
LABEL_TO_DIRECTION = {label: direction for direction, label in DIRECTION_LABELS.items()}
DIAGONAL_KERNEL = ((0, 0, 0), (1, 1, 1))


def add_bits(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a ^ b for a, b in zip(left, right))


def span_word(coord: tuple[int, int, int]) -> int:
    value = 0
    for bit, basis_word in zip(coord, EVEN_BASIS_WORDS):
        if bit:
            value ^= basis_word
    return value


WORD_TO_COORD = {span_word(coord): coord for coord in DOMAIN}


def parity(word: int) -> int:
    return word.bit_count() % 2


def edge_set(rows: list[list[int]]) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(row) for row in rows)


def direction_outputs(matching: frozenset[tuple[int, int]]) -> dict[tuple[int, int, int], tuple[int, int]]:
    outputs: dict[tuple[int, int, int], tuple[int, int]] = {}
    for left, right in matching:
        even_vertices = [word for word in (left, right) if parity(word) == 0]
        if len(even_vertices) != 1:
            raise ValueError(f"Q4 matching edge is not parity-crossing: {(left, right)}")
        even_word = even_vertices[0]
        direction = left ^ right
        if direction not in DIRECTION_LABELS:
            raise ValueError(f"Q4 matching edge does not have a coordinate direction: {(left, right)}")
        outputs[WORD_TO_COORD[even_word]] = DIRECTION_LABELS[direction]
    return dict(sorted(outputs.items()))


def linear_apply(
    columns: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    coord: tuple[int, int, int],
) -> tuple[int, int]:
    value = (0, 0)
    for bit, column in zip(coord, columns):
        if bit:
            value = add_bits(value, column)
    return value


def affine_signature(outputs: dict[tuple[int, int, int], tuple[int, int]]) -> dict:
    translation = outputs[(0, 0, 0)]
    basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    columns = tuple(add_bits(outputs[vector], translation) for vector in basis)
    is_affine = all(
        outputs[coord] == add_bits(linear_apply(columns, coord), translation)
        for coord in DOMAIN
    )
    image = {linear_apply(columns, coord) for coord in DOMAIN}
    kernel = tuple(sorted(coord for coord in DOMAIN if linear_apply(columns, coord) == (0, 0)))
    rank = {1: 0, 2: 1, 4: 2}[len(image)]
    return {
        "is_affine": is_affine,
        "linear_columns": columns,
        "translation": translation,
        "rank": rank,
        "kernel": kernel,
    }


def kernel_cosets(kernel: tuple[tuple[int, int, int], ...]) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    seen: set[tuple[int, int, int]] = set()
    cosets = []
    for coord in DOMAIN:
        if coord in seen:
            continue
        coset = tuple(sorted(add_bits(coord, kernel_coord) for kernel_coord in kernel))
        seen.update(coset)
        cosets.append(coset)
    return tuple(cosets)


def quotient_routes(
    outputs: dict[tuple[int, int, int], tuple[int, int]],
    kernel: tuple[tuple[int, int, int], ...],
) -> list[dict]:
    routes = []
    for coset in kernel_cosets(kernel):
        labels = {outputs[coord] for coord in coset}
        label = next(iter(labels))
        routes.append(
            {
                "coset": [list(coord) for coord in coset],
                "constant_on_coset": len(labels) == 1,
                "direction_label": list(label),
                "direction_word": LABEL_TO_DIRECTION[label],
            }
        )
    return routes


def as_json_vector(vector: tuple[int, ...]) -> list[int]:
    return list(vector)


def as_json_matrix(columns: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]) -> list[list[int]]:
    return [as_json_vector(column) for column in columns]


def selector_affine_fiber_law_packet() -> dict:
    bt323 = all_selector_kappa_pullback_orbit_packet()
    matchings = [edge_set(row["q4_pullback_matching"]) for row in bt323["selector_rows"]]
    disjoint_components = [set(component) for component in bt323["disjointness_components"]]

    rows = []
    linear_part_ids: dict[tuple[tuple[int, int], tuple[int, int], tuple[int, int]], str] = {}
    for row, matching in zip(bt323["selector_rows"], matchings):
        outputs = direction_outputs(matching)
        signature = affine_signature(outputs)
        linear_columns = signature["linear_columns"]
        if linear_columns not in linear_part_ids:
            linear_part_ids[linear_columns] = f"linear_{len(linear_part_ids)}"
        selector_index = row["selector_index"]
        fiber_index = next(index for index, component in enumerate(disjoint_components) if selector_index in component)
        routes = quotient_routes(outputs, signature["kernel"])
        rows.append(
            {
                "selector_index": selector_index,
                "bt323_disjointness_fiber": fiber_index,
                "linear_part_id": linear_part_ids[linear_columns],
                "linear_columns": as_json_matrix(linear_columns),
                "translation": as_json_vector(signature["translation"]),
                "rank": signature["rank"],
                "kernel": [as_json_vector(coord) for coord in signature["kernel"]],
                "direction_outputs": {
                    "".join(map(str, coord)): as_json_vector(label)
                    for coord, label in outputs.items()
                },
                "quotient_routes": routes,
            }
        )

    rows_by_selector = {row["selector_index"]: row for row in rows}
    linear_fibers: dict[str, list[int]] = defaultdict(list)
    translations_by_linear: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for row in rows:
        linear_fibers[row["linear_part_id"]].append(row["selector_index"])
        translations_by_linear[row["linear_part_id"]].append(tuple(row["translation"]))

    intersection_by_pair: dict[tuple[int, int], int] = {}
    for left in range(len(matchings)):
        for right in range(left + 1, len(matchings)):
            intersection_by_pair[(left, right)] = len(matchings[left] & matchings[right])

    equal_linear_pairs = [
        pair
        for pair in intersection_by_pair
        if rows_by_selector[pair[0]]["linear_part_id"] == rows_by_selector[pair[1]]["linear_part_id"]
    ]
    different_linear_pairs = [
        pair
        for pair in intersection_by_pair
        if rows_by_selector[pair[0]]["linear_part_id"] != rows_by_selector[pair[1]]["linear_part_id"]
    ]
    disjointness_from_linear = {
        selector: sorted(
            other
            for other in range(len(matchings))
            if other != selector
            and rows_by_selector[other]["linear_part_id"] == rows_by_selector[selector]["linear_part_id"]
        )
        for selector in range(len(matchings))
    }
    two_overlap_from_linear = {
        selector: sorted(
            other
            for other in range(len(matchings))
            if rows_by_selector[other]["linear_part_id"] != rows_by_selector[selector]["linear_part_id"]
        )
        for selector in range(len(matchings))
    }

    quotient_routes_by_selector = {
        row["selector_index"]: row["quotient_routes"]
        for row in rows
    }
    all_routes_constant = all(
        route["constant_on_coset"]
        for routes in quotient_routes_by_selector.values()
        for route in routes
    )
    all_routes_hit_all_directions = all(
        sorted(route["direction_word"] for route in routes) == [1, 2, 4, 8]
        for routes in quotient_routes_by_selector.values()
    )

    checks = {
        "bt323_selector_count_is_8": bt323["q4_selector_count"] == 2**Q == 8,
        "even_basis_spans_the_even_Q4_half": set(WORD_TO_COORD) == {
            word for word in range(16) if parity(word) == 0
        },
        "direction_labeling_is_F2_square": sorted(DIRECTION_LABELS.values()) == [(0, 0), (0, 1), (1, 0), (1, 1)],
        "all_selector_outputs_cover_even_subspace": all(
            set(direction_outputs(matching)) == set(DOMAIN)
            for matching in matchings
        ),
        "all_selector_direction_maps_are_affine": all(
            affine_signature(direction_outputs(matching))["is_affine"]
            for matching in matchings
        ),
        "all_affine_maps_have_rank_2": all(row["rank"] == 2 for row in rows),
        "all_affine_maps_have_common_diagonal_kernel": all(
            tuple(tuple(coord) for coord in row["kernel"]) == DIAGONAL_KERNEL
            for row in rows
        ),
        "diagonal_kernel_has_size_2": len(DIAGONAL_KERNEL) == 2,
        "kernel_quotient_has_four_cosets": len(kernel_cosets(DIAGONAL_KERNEL)) == MU,
        "each_selector_is_constant_on_kernel_cosets": all_routes_constant,
        "each_selector_hits_all_four_coordinate_directions_on_quotient": all_routes_hit_all_directions,
        "there_are_exactly_two_linear_parts": len(linear_fibers) == 2,
        "each_linear_part_has_four_translations": all(
            Counter(translations) == Counter(DIRECTION_LABELS.values())
            for translations in translations_by_linear.values()
        ),
        "linear_part_fibers_match_BT323_disjointness_components": sorted(
            sorted(indices) for indices in linear_fibers.values()
        )
        == bt323["disjointness_components"],
        "equal_linear_part_pairs_are_exactly_12": len(equal_linear_pairs) == 12,
        "different_linear_part_pairs_are_exactly_16": len(different_linear_pairs) == 16,
        "equal_linear_part_pairs_are_disjoint": all(
            intersection_by_pair[pair] == 0 for pair in equal_linear_pairs
        ),
        "different_linear_part_pairs_have_two_edges": all(
            intersection_by_pair[pair] == 2 for pair in different_linear_pairs
        ),
        "bt323_disjointness_graph_is_equal_linear_part_graph": disjointness_from_linear
        == {int(node): neighbors for node, neighbors in bt323["disjointness_graph"].items()},
        "bt323_two_overlap_graph_is_different_linear_part_graph": two_overlap_from_linear
        == {int(node): neighbors for node, neighbors in bt323["two_overlap_graph"].items()},
        "selector_orbit_is_two_linear_parts_times_four_translations": (
            len(linear_fibers) * len(set(DIRECTION_LABELS.values())) == len(rows) == OCTONION
        ),
    }

    return {
        "breakthrough": 324,
        "title": "Selector affine fiber law",
        "source": "Derived from BT323 q4_pullback_matching rows",
        "even_subspace_model": {
            "basis_words": list(EVEN_BASIS_WORDS),
            "word_to_coord": {str(word): as_json_vector(coord) for word, coord in sorted(WORD_TO_COORD.items())},
            "common_kernel": [as_json_vector(coord) for coord in DIAGONAL_KERNEL],
            "kernel_cosets": [
                [as_json_vector(coord) for coord in coset]
                for coset in kernel_cosets(DIAGONAL_KERNEL)
            ],
        },
        "direction_plane": {str(direction): as_json_vector(label) for direction, label in DIRECTION_LABELS.items()},
        "selector_rows": rows,
        "linear_part_fibers": {
            linear_part: sorted(indices)
            for linear_part, indices in sorted(linear_fibers.items())
        },
        "translations_by_linear_part": {
            linear_part: [as_json_vector(translation) for translation in sorted(translations)]
            for linear_part, translations in sorted(translations_by_linear.items())
        },
        "pair_intersection_explanation": {
            "equal_linear_part_pairs": [list(pair) for pair in equal_linear_pairs],
            "different_linear_part_pairs": [list(pair) for pair in different_linear_pairs],
            "equal_linear_part_intersection_size": 0,
            "different_linear_part_intersection_size": 2,
            "disjointness_graph_from_linear_parts": {
                str(selector): neighbors
                for selector, neighbors in disjointness_from_linear.items()
            },
            "two_overlap_graph_from_linear_parts": {
                str(selector): neighbors
                for selector, neighbors in two_overlap_from_linear.items()
            },
        },
        "architectural_reading": (
            "BT323's two four-state selector fibers are the two linear projections "
            "from the even Q4 half F2^3 onto the direction plane F2^2.  The four "
            "members inside each fiber are the four translations.  All eight maps "
            "factor through the same diagonal kernel <111>, so the live route "
            "state is the quotient F2^3/<111>, not the raw eight even vertices."
        ),
        "boundary": (
            "This is a finite Q4/K8,8 selector theorem derived from BT323.  The "
            "external prime-router and AI-router repositories remain heuristic "
            "language sources only; no external result is used as a proof input."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = selector_affine_fiber_law_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 324: SELECTOR AFFINE FIBER LAW")
    print("=" * 78)
    print()
    print(f"linear fibers   = {packet['linear_part_fibers']}")
    print(f"common kernel   = {packet['even_subspace_model']['common_kernel']}")
    print(f"kernel cosets   = {packet['even_subspace_model']['kernel_cosets']}")
    print(f"verified        = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = ROOT / "data" / "w33_BREAKTHROUGH_324_selector_affine_fiber_law.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
