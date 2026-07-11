#!/usr/bin/env python3
"""Pass 176: incidence-fixed-line bridge from the SO(10) shadow to E8/2E8.

Let M be the 40-line by 40-point incidence matrix of W(3,3), let

    C = ker_F2(M) = [40,15,8],          H10 = C^perp / C,
    R = ker_F2(M^T) = [40,15,10],       K = R cap R^perp.

The native PSp(4,3) action on H10 has one nonzero fixed vector f.  This
witness proves objectwise that incidence induces

    f^perp / <f>  --M-->  K / <1>,

an equivariant quadratic isometry between plus-type 8-spaces.  It also
identifies the 240 weight-six context words as the two-sheeted lift of the
120 anisotropic vectors and reconstructs SRG(120,63,30,36).

All arithmetic is exact over F2.  No claim about the full automorphism group
of the resulting graph, or about a signed integral E8 Gram realization, is
made here.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
from pathlib import Path
import hashlib
import json

from w33_levi_next5_v5_common import (
    SEEDS,
    build_w33,
    gf2_nullspace,
    line_perm_from_point_perm,
    point_transvection_perm,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass176_incidence_fixed_line_e8_bridge.json"


def rref(rows: list[int], width: int) -> tuple[list[int], list[int]]:
    work = [int(row) for row in rows]
    pivots: list[int] = []
    rank = 0
    for column in range(width):
        pivot = next(
            (i for i in range(rank, len(work)) if (work[i] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(len(work)):
            if i != rank and ((work[i] >> column) & 1):
                work[i] ^= work[rank]
        pivots.append(column)
        rank += 1
    return work[:rank], pivots


def reduce_word(word: int, basis: list[int], pivots: list[int]) -> int:
    value = int(word)
    for row, pivot in zip(basis, pivots):
        if (value >> pivot) & 1:
            value ^= row
    return value


def span(basis: list[int]) -> set[int]:
    values = {0}
    for row in basis:
        values |= {value ^ row for value in tuple(values)}
    return values


def matrix_vector(rows: list[int], vector: int) -> int:
    return sum((((row & vector).bit_count() & 1) << i) for i, row in enumerate(rows))


def permute_word(word: int, permutation: tuple[int, ...]) -> int:
    out = 0
    value = int(word)
    while value:
        bit = value & -value
        out |= 1 << permutation[bit.bit_length() - 1]
        value ^= bit
    return out


def apply_columns(columns: tuple[int, ...], vector: int) -> int:
    out = 0
    value = int(vector)
    while value:
        bit = value & -value
        out ^= columns[bit.bit_length() - 1]
        value ^= bit
    return out


def compose_columns(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Columns for left after right."""
    return tuple(apply_columns(left, column) for column in right)


def digest(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def srg_parameters(adjacency: list[int], n: int) -> tuple[int, int, int, int] | None:
    degrees = {row.bit_count() for row in adjacency}
    if len(degrees) != 1:
        return None
    degree = next(iter(degrees))
    adjacent_common: set[int] = set()
    nonadjacent_common: set[int] = set()
    for i, j in combinations(range(n), 2):
        common = (adjacency[i] & adjacency[j]).bit_count()
        if (adjacency[i] >> j) & 1:
            adjacent_common.add(common)
        else:
            nonadjacent_common.add(common)
    if len(adjacent_common) != 1 or len(nonadjacent_common) != 1:
        return None
    return n, degree, next(iter(adjacent_common)), next(iter(nonadjacent_common))


def analyze() -> dict:
    geometry = build_w33()
    incidence_rows = [
        sum((int(entry) & 1) << i for i, entry in enumerate(row))
        for row in geometry.incidence
    ]
    transpose_rows = [
        sum((int(geometry.incidence[line, point]) & 1) << line for line in range(40))
        for point in range(40)
    ]
    checks: dict[str, bool] = {}

    # Address code C and context code C^perp = row(M).
    address_basis, address_pivots = rref(gf2_nullspace(incidence_rows, 40), 40)
    context_basis, context_pivots = rref(incidence_rows, 40)
    checks["address_context_dimensions_15_25"] = (
        len(address_basis) == 15 and len(context_basis) == 25
    )
    checks["address_inside_context"] = all(
        reduce_word(row, context_basis, context_pivots) == 0
        for row in address_basis
    )
    checks["address_doubly_even_self_orthogonal"] = (
        all(row.bit_count() % 4 == 0 for row in address_basis)
        and all(
            (address_basis[i] & address_basis[j]).bit_count() % 2 == 0
            for i in range(15)
            for j in range(15)
        )
    )

    # Quotient coordinates on H10=C^perp/C.  Context RREF pivot entries are
    # its 25 coordinates; reducing the embedded C leaves ten free entries.
    address_in_context = [
        sum(((row >> pivot) & 1) << i for i, pivot in enumerate(context_pivots))
        for row in address_basis
    ]
    address_coordinate_basis, address_coordinate_pivots = rref(address_in_context, 25)
    free_positions = [i for i in range(25) if i not in address_coordinate_pivots]
    checks["address_shadow_dimension_10"] = len(free_positions) == 10

    def quotient_coordinates(word: int) -> int:
        coordinates = sum(
            ((word >> pivot) & 1) << i for i, pivot in enumerate(context_pivots)
        )
        reduced = reduce_word(
            coordinates, address_coordinate_basis, address_coordinate_pivots
        )
        return sum(((reduced >> position) & 1) << i for i, position in enumerate(free_positions))

    shadow_basis = [context_basis[position] for position in free_positions]

    def shadow_word(vector: int) -> int:
        out = 0
        for i, word in enumerate(shadow_basis):
            if (vector >> i) & 1:
                out ^= word
        return out

    polar_rows = [
        sum(((left & right).bit_count() & 1) << j for j, right in enumerate(shadow_basis))
        for left in shadow_basis
    ]

    def polar(left: int, right: int) -> int:
        gram_left = 0
        for i, row in enumerate(polar_rows):
            if (left >> i) & 1:
                gram_left ^= row
        return (gram_left & right).bit_count() & 1

    def address_quadratic(vector: int) -> int:
        word = shadow_word(vector)
        assert word.bit_count() % 2 == 0
        return (word.bit_count() // 2) & 1

    checks["address_polar_nondegenerate"] = len(rref(polar_rows, 10)[0]) == 10

    # Native PSp(4,3) transvections on H10.
    point_generators = [
        point_transvection_perm(geometry.points, seed) for seed in SEEDS
    ]
    line_generators = [
        line_perm_from_point_perm(geometry.lines, permutation)
        for permutation in point_generators
    ]
    shadow_generators = [
        tuple(
            quotient_coordinates(permute_word(word, permutation))
            for word in shadow_basis
        )
        for permutation in point_generators
    ]
    checks["shadow_generators_invertible"] = all(
        len(rref(list(columns), 10)[0]) == 10 for columns in shadow_generators
    )
    fixed_vectors = [
        vector
        for vector in range(1 << 10)
        if all(apply_columns(generator, vector) == vector for generator in shadow_generators)
    ]
    checks["unique_nonzero_fixed_line"] = len(fixed_vectors) == 2
    fixed = next(vector for vector in fixed_vectors if vector)
    checks["fixed_line_is_isotropic"] = address_quadratic(fixed) == 0

    identity = tuple(1 << i for i in range(10))
    generated_actions = {identity}
    queue = deque([identity])
    while queue:
        action = queue.popleft()
        for generator in shadow_generators:
            product = compose_columns(action, generator)
            if product not in generated_actions:
                generated_actions.add(product)
                queue.append(product)
    checks["native_action_order_25920"] = len(generated_actions) == 25920

    # M descends from H10 because it kills C.  Its image is im(MM^T).
    incidence_images = {
        vector: matrix_vector(incidence_rows, shadow_word(vector))
        for vector in range(1 << 10)
    }
    image_basis, image_pivots = rref(list(incidence_images.values()), 40)
    gram_line_rows = [matrix_vector(incidence_rows, row) for row in incidence_rows]
    gram_line_basis, gram_line_pivots = rref(gram_line_rows, 40)
    checks["incidence_descends_injectively"] = (
        len(set(incidence_images.values())) == 1024 and len(image_basis) == 10
    )
    checks["incidence_image_is_im_MMt"] = (
        len(gram_line_basis) == 10
        and all(reduce_word(row, gram_line_basis, gram_line_pivots) == 0 for row in image_basis)
        and all(reduce_word(row, image_basis, image_pivots) == 0 for row in gram_line_basis)
    )
    all_ones = (1 << 40) - 1
    checks["fixed_line_maps_to_all_ones"] = incidence_images[fixed] == all_ones

    fixed_perp = [vector for vector in range(1 << 10) if polar(fixed, vector) == 0]
    checks["fixed_perp_dimension_9"] = len(fixed_perp) == 512

    # Route hull K=R cap R^perp, enumerated independently inside R.
    route_basis, route_pivots = rref(gf2_nullspace(transpose_rows, 40), 40)
    route_perp_basis, route_perp_pivots = rref(transpose_rows, 40)
    route_words = span(route_basis)
    route_hull = {
        word
        for word in route_words
        if reduce_word(word, route_perp_basis, route_perp_pivots) == 0
    }
    mapped_fixed_perp = {incidence_images[vector] for vector in fixed_perp}
    checks["route_dimensions_15_25_hull9"] = (
        len(route_basis) == 15
        and len(route_perp_basis) == 25
        and len(route_hull) == 512
    )
    checks["fixed_perp_maps_onto_route_hull"] = mapped_fixed_perp == route_hull
    checks["route_hull_contains_all_ones"] = all_ones in route_hull

    quadratic_failures = []
    for vector in fixed_perp:
        image = incidence_images[vector]
        if image.bit_count() % 4:
            quadratic_failures.append((vector, "not_doubly_even"))
            continue
        if address_quadratic(vector) != ((image.bit_count() // 4) & 1):
            quadratic_failures.append((vector, "quadratic_mismatch"))
    checks["all_512_quadratic_identities"] = not quadratic_failures
    route_weight_enumerator = Counter(word.bit_count() for word in route_hull)
    checks["route_hull_enumerator"] = route_weight_enumerator == Counter(
        {0: 1, 16: 135, 20: 240, 24: 135, 40: 1}
    )

    # Generator-by-generator, objectwise equivariance on all 1024 classes.
    equivariance_failures = 0
    for point_generator, line_generator, shadow_generator in zip(
        point_generators, line_generators, shadow_generators
    ):
        for vector in range(1 << 10):
            target = apply_columns(shadow_generator, vector)
            if permute_word(incidence_images[vector], line_generator) != incidence_images[target]:
                equivariance_failures += 1
    checks["all_8192_incidence_equivariance_identities"] = equivariance_failures == 0

    # The quotient f^perp/<f> has the E8/2E8 plus-type census.
    quotient_pairs = []
    seen = set()
    for vector in fixed_perp:
        if vector in seen:
            continue
        pair = tuple(sorted((vector, vector ^ fixed)))
        quotient_pairs.append(pair)
        seen.update(pair)
    isotropic_pairs = [pair for pair in quotient_pairs if address_quadratic(pair[0]) == 0]
    anisotropic_pairs = [pair for pair in quotient_pairs if address_quadratic(pair[0]) == 1]
    checks["plus8_census_136_120"] = (
        len(quotient_pairs) == 256
        and len(isotropic_pairs) == 136
        and len(anisotropic_pairs) == 120
    )

    # Exhaustive weight-six census in the context code.  Its 240 words are
    # distinct anisotropic classes and exhaust both sheets over the 120.
    weight_six_words = []
    for support in combinations(range(40), 6):
        word = sum(1 << point for point in support)
        if all((word & row).bit_count() % 2 == 0 for row in address_basis):
            weight_six_words.append(word)
    weight_six_classes = [quotient_coordinates(word) for word in weight_six_words]
    anisotropic_lifts = {
        vector for vector in fixed_perp if address_quadratic(vector) == 1
    }
    checks["weight6_240_distinct_anisotropic_lifts"] = (
        len(weight_six_words) == 240
        and len(set(weight_six_classes)) == 240
        and set(weight_six_classes) == anisotropic_lifts
    )
    word_for_class = dict(zip(weight_six_classes, weight_six_words))
    checks["fixed_translation_pairs_weight6_sheets"] = all(
        (vector ^ fixed) in word_for_class for vector in weight_six_classes
    )
    checks["paired_weight6_supports_disjoint"] = all(
        (word_for_class[vector] & word_for_class[vector ^ fixed]) == 0
        for vector in weight_six_classes
    )
    mapped_weight_six = {incidence_images[vector] for vector in weight_six_classes}
    route_weight_twenty = {word for word in route_hull if word.bit_count() == 20}
    checks["weight6_bijection_to_route_weight20"] = mapped_weight_six == route_weight_twenty

    # Polar orthogonality on the 120 anisotropic quotient points.
    adjacency = [0] * 120
    for i, j in combinations(range(120), 2):
        if polar(anisotropic_pairs[i][0], anisotropic_pairs[j][0]) == 0:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    parameters = srg_parameters(adjacency, 120)
    checks["anisotropic_graph_srg_120_63_30_36"] = parameters == (120, 63, 30, 36)

    # All generators preserve the sheet involution, quotient form, and graph.
    pair_index = {
        frozenset(pair): i for i, pair in enumerate(anisotropic_pairs)
    }
    quotient_equivariance = True
    for generator in shadow_generators:
        induced = []
        for pair in anisotropic_pairs:
            image_pair = frozenset(apply_columns(generator, value) for value in pair)
            if image_pair not in pair_index:
                quotient_equivariance = False
                break
            induced.append(pair_index[image_pair])
        if not quotient_equivariance:
            break
        for i in range(120):
            mapped_neighbors = {induced[j] for j in range(120) if (adjacency[i] >> j) & 1}
            target_neighbors = {j for j in range(120) if (adjacency[induced[i]] >> j) & 1}
            if mapped_neighbors != target_neighbors:
                quotient_equivariance = False
                break
    checks["native_PSp_quotient_graph_equivariance"] = quotient_equivariance

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass176.incidence_fixed_line_e8_bridge.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": (
            "Incidence induces a native PSp(4,3)-equivariant quadratic isometry "
            "f^perp/<f> -> (R cap R^perp)/<1> between plus-type 8-spaces. "
            "The 240 weight-six context words are exactly the two sheets over its "
            "120 anisotropic vectors, whose polar graph is SRG(120,63,30,36)."
        ),
        "spaces": {
            "address_code": "[40,15,8]",
            "address_shadow": "C^perp/C = F2^10",
            "fixed_vector": hex(fixed),
            "fixed_representative_weight": shadow_word(fixed).bit_count(),
            "route_code": "[40,15,10]",
            "route_hull": "[40,9,16]",
            "route_hull_weight_enumerator": {
                str(weight): count for weight, count in sorted(route_weight_enumerator.items())
            },
        },
        "incidence_bridge": {
            "domain": "f^perp/<f>",
            "codomain": "(R cap R^perp)/<all-ones>",
            "domain_size_before_quotient": len(fixed_perp),
            "codomain_size_before_quotient": len(route_hull),
            "quadratic_identities_checked": len(fixed_perp),
            "equivariance_identities_checked": len(point_generators) * (1 << 10),
            "fixed_image": "all-ones",
            "native_action_order": len(generated_actions),
            "isotropic_anisotropic_quotient_census": [len(isotropic_pairs), len(anisotropic_pairs)],
        },
        "weight6_sheet_cover": {
            "context_words": len(weight_six_words),
            "distinct_shadow_classes": len(set(weight_six_classes)),
            "fixed_translation_pairs": len(anisotropic_pairs),
            "paired_support_intersection": 0,
            "route_weight20_images": len(mapped_weight_six),
        },
        "anisotropic_graph": {
            "parameters": list(parameters) if parameters else None,
            "edges": sum(row.bit_count() for row in adjacency) // 2,
            "adjacency_digest": digest(adjacency),
        },
        "digests": {
            "incidence_images": digest(sorted(incidence_images.items())),
            "weight6_classes": digest(sorted(weight_six_classes)),
            "sheet_pairs": digest(sorted(tuple(pair) for pair in anisotropic_pairs)),
            "native_generators": digest(shadow_generators),
        },
        "checks": checks,
        "scope_boundary": (
            "The proved symmetry is the native PSp(4,3) coordinate action. "
            "No equality with the full automorphism group of the 120-graph is asserted, "
            "and the two-sheet cover is not yet an integral signed E8 Gram realization."
        ),
    }
    return payload


def main() -> int:
    payload = analyze()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
