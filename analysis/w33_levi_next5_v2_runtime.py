"""Track module extracted from w33_levi_next5_v2."""
from __future__ import annotations
from w33_levi_next5_v2_common import *
from w33_levi_next5_v2_mod8 import projective_transvections

def compose_permutations(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(right)))


def inverse_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for i, image in enumerate(permutation):
        inverse[image] = i
    return tuple(inverse)


def close_permutation_group(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = tuple(range(len(generators[0])))
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators:
            image = compose_permutations(generator, current)
            if image not in seen:
                seen.add(image)
                queue.append(image)
    return seen


def linear_projective_permutation(geometry: base.Geometry, diagonal: tuple[int, int, int, int]) -> tuple[int, ...]:
    field = base.FiniteField(3)
    index = {point: i for i, point in enumerate(geometry.points)}
    out = []
    for point in geometry.points:
        image = tuple(field.mul(diagonal[i], point[i]) for i in range(4))
        out.append(index[field.normalize_projective(image)])
    return tuple(out)


def orbit_sizes(permutations: list[tuple[int, ...]], size: int) -> list[int]:
    seen = bytearray(size)
    out = []
    for start in range(size):
        if seen[start]:
            continue
        seen[start] = 1
        queue = deque([start])
        count = 0
        while queue:
            current = queue.popleft()
            count += 1
            for permutation in permutations:
                image = permutation[current]
                if not seen[image]:
                    seen[image] = 1
                    queue.append(image)
        out.append(count)
    return sorted(out)


def permutation_digest(permutation: tuple[int, ...]) -> str:
    digest = hashlib.sha256()
    for value in permutation:
        digest.update(struct.pack("<H", value))
    return digest.hexdigest()


def native_runtime_track(geometry: base.Geometry) -> dict:
    generators = projective_transvections(geometry)
    psp = close_permutation_group(generators)
    outer = linear_projective_permutation(geometry, (1, 2, 1, 2))
    full = close_permutation_group(generators + [outer])

    point_stabilizer = {element for element in psp if element[0] == 0}
    center = {
        element for element in point_stabilizer
        if all(compose_permutations(element, other) == compose_permutations(other, element) for other in point_stabilizer)
    }
    nonneighbor = next(point for point in range(1, 40) if not ((geometry.point_adjacency[0] >> point) & 1))
    pair = {0, nonneighbor}
    pair_stabilizer = {element for element in psp if {element[0], element[nonneighbor]} == pair}

    full_list = sorted(full)
    full_index = {element: index for index, element in enumerate(full_list)}
    regular_permutations = [
        tuple(full_index[compose_permutations(generator, element)] for element in full_list)
        for generator in generators + [outer]
    ]

    point_transversal = {}
    for element in sorted(psp):
        point_transversal.setdefault(element[0], element)

    center_list = sorted(center)
    unused = set(point_stabilizer)
    quotient_representatives = []
    stabilizer_coordinates = {}
    while unused:
        representative = min(unused)
        quotient_index = len(quotient_representatives)
        quotient_representatives.append(representative)
        coset = {compose_permutations(representative, central) for central in center_list}
        for phase, central in enumerate(center_list):
            stabilizer_coordinates[compose_permutations(representative, central)] = (quotient_index, phase)
        unused -= coset

    coordinates = set()
    psp_set = set(psp)
    for element in full_list:
        if element in psp_set:
            chirality = 0
            even_element = element
        else:
            chirality = 1
            even_element = compose_permutations(outer, element)
            if even_element not in psp_set:
                raise AssertionError("outer coset orientation failed")
        point = even_element[0]
        stabilizer_element = compose_permutations(inverse_permutation(point_transversal[point]), even_element)
        clifford_class, central_phase = stabilizer_coordinates[stabilizer_element]
        coordinates.add((chirality, point, central_phase, clifford_class))

    checks = {
        "PSp_order_25920": len(psp) == 25920,
        "outer_not_inner": outer not in psp,
        "outer_normalizes_PSp": all(compose_permutations(outer, compose_permutations(g, outer)) in psp for g in generators),
        "full_order_51840": len(full) == 51840,
        "point_stabilizer_648": len(point_stabilizer) == 648,
        "point_stabilizer_center_3": len(center) == 3,
        "Clifford_quotient_216": len(quotient_representatives) == 216,
        "noncollinear_pair_stabilizer_48": len(pair_stabilizer) == 48,
        "pair_orbit_540": len(psp) // len(pair_stabilizer) == 540,
        "PSp_two_regular_chirality_orbits": orbit_sizes(regular_permutations[:-1], 51840) == [25920, 25920],
        "full_W_E6_regular_orbit": orbit_sizes(regular_permutations, 51840) == [51840],
        "coordinate_bijection_2x40x3x216": len(coordinates) == 2 * 40 * 3 * 216 == 51840,
    }
    return {
        "status": "PROVED" if all(checks.values()) else "FAIL",
        "all_pass": all(checks.values()),
        "checks": checks,
        "native_group": "PSp(4,3) on each chirality sheet",
        "full_group": "PSp(4,3):2, the standard W(E6) extension",
        "orbit_structure": {"PSp": [25920, 25920], "full_extension": [51840]},
        "stabilizers": {
            "regular_state": 1,
            "projective_point": 648,
            "point_stabilizer_center": 3,
            "point_stabilizer_mod_center_Clifford": 216,
            "noncollinear_pair": 48,
        },
        "factorizations": {
            "PSp": "25920 = 40 * 648 = 120 * 216 = 540 * 48",
            "W_E6": "51840 = 2 * 40 * 3 * 216 = 2 * 540 * 48",
        },
        "coordinate_model": "(chirality, projective point, central phase in C3, projective Clifford class in P/Z(P))",
        "generator_digests": [permutation_digest(permutation) for permutation in regular_permutations],
    }
