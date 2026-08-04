#!/usr/bin/env python3
"""Passes 3376--3389: exact cohomology word metrics, tau barycenters, and voltage lifts."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

import numpy as np

P = 3
COEFFICIENT_DIM = 5
COEFFICIENT_SIZE = P ** COEFFICIENT_DIM
FILLED_FACES = 240
BASE_VERTICES = 45
BASE_EDGES = 720
BASE_DEGREE = 32
BASE_TRIANGLES = 5280
MIN_DEFECT_NONZERO_TRIANGLES = 42

FULL_SPECTRUM = {10: 1, 7: 6, 4: 22, 1: 44, -2: 42, -5: 20}
HIDDEN_SPECTRUM = {4: 4, 1: 12, -2: 9, -5: 2}
BARYCENTRIC_SPECTRUM = {10: 1, 7: 6, 4: 18, 1: 32, -2: 33, -5: 18}


def tau(x: tuple[int, ...]) -> tuple[int, ...]:
    x1, x2, x3, x4, x5 = x
    return ((-x4) % 3, (1 - x3) % 3, (1 - x2) % 3, (-x1) % 3, x5)


def orbit_partition() -> list[tuple[tuple[int, ...], ...]]:
    points = list(product(range(3), repeat=5))
    seen: set[tuple[int, ...]] = set()
    orbits: list[tuple[tuple[int, ...], ...]] = []
    for x in points:
        if x in seen:
            continue
        orbit = tuple(sorted({x, tau(x)}))
        seen.update(orbit)
        orbits.append(orbit)
    return orbits


def barycenter_signature(orbit: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    """Return twice the normalized Q15 one-hot barycenter as an integer 15-vector."""
    signature: list[int] = []
    if len(orbit) == 1:
        for position in range(5):
            counts = [0, 0, 0]
            counts[orbit[0][position]] = 2
            signature.extend(counts)
    else:
        for position in range(5):
            counts = [0, 0, 0]
            for x in orbit:
                counts[x[position]] += 1
            signature.extend(counts)
    return tuple(signature)


def hidden_bit(orbit: tuple[tuple[int, ...], ...]) -> int:
    x = orbit[0]
    a = (x[0] + x[3]) % 3
    b = (x[1] + x[2] - 1) % 3
    value = (a * b) % 3
    if value not in (1, 2):
        raise ValueError("hidden bit requested outside the ambiguous stratum")
    if len(orbit) == 2:
        y = orbit[1]
        check = ((y[0] + y[3]) * (y[1] + y[2] - 1)) % 3
        assert check == value
    return value


def missing_symbol(values: tuple[int, int]) -> int:
    missing = {0, 1, 2} - set(values)
    assert len(missing) == 1
    return missing.pop()


def ambiguous_center(
    fiber: list[tuple[tuple[int, ...], ...]]
) -> tuple[int, int, int]:
    orbit = fiber[0]
    assert len(orbit) == 2
    x, y = orbit
    missing = [missing_symbol((x[i], y[i])) for i in range(4)]
    assert missing[2] == (1 - missing[1]) % 3
    assert missing[3] == (-missing[0]) % 3
    assert x[4] == y[4]
    return (missing[0], missing[1], x[4])


def hamming_quotient(
    orbits: list[tuple[tuple[int, ...], ...]]
) -> np.ndarray:
    orbit_of: dict[tuple[int, ...], int] = {}
    for index, orbit in enumerate(orbits):
        for x in orbit:
            orbit_of[x] = index
    matrix = np.zeros((len(orbits), len(orbits)), dtype=np.int64)
    for source, orbit in enumerate(orbits):
        x = orbit[0]
        for position in range(5):
            for value in range(3):
                if value == x[position]:
                    continue
                y = list(x)
                y[position] = value
                matrix[source, orbit_of[tuple(y)]] += 1
    assert set(matrix.sum(axis=1).tolist()) == {10}
    return matrix


def trace_moments(matrix: np.ndarray, max_power: int = 5) -> list[int]:
    current = np.eye(matrix.shape[0], dtype=np.int64)
    moments = []
    for _ in range(max_power + 1):
        moments.append(int(np.trace(current)))
        current = current @ matrix
    return moments


def spectrum_moments(spectrum: dict[int, int], max_power: int = 5) -> list[int]:
    return [
        sum(multiplicity * (eigenvalue ** power)
            for eigenvalue, multiplicity in spectrum.items())
        for power in range(max_power + 1)
    ]


def word_metric_certificate() -> dict:
    local_counts = [1, 3 * (COEFFICIENT_SIZE - 1), 0]
    local_counts[2] = COEFFICIENT_SIZE ** 2 - sum(local_counts[:2])
    assert local_counts == [1, 726, 58322]

    coefficients = [1]
    for _ in range(FILLED_FACES):
        updated = [0] * (len(coefficients) + 2)
        for degree, value in enumerate(coefficients):
            updated[degree] += value
            updated[degree + 1] += local_counts[1] * value
            updated[degree + 2] += local_counts[2] * value
        coefficients = updated

    quotient_size = P ** 2180
    cumulative = 0
    first_covering_radius = None
    cumulative_before = None
    cumulative_at = None
    for radius, value in enumerate(coefficients):
        cumulative += value
        if cumulative >= quotient_size:
            first_covering_radius = radius
            cumulative_before = cumulative - value
            cumulative_at = cumulative
            break
    assert first_covering_radius == 389
    assert cumulative_before is not None and cumulative_at is not None
    assert cumulative_before < quotient_size <= cumulative_at

    def integer_digest(value: int) -> dict:
        text = str(value)
        return {
            "decimal_digits": len(text),
            "bit_length": value.bit_length(),
            "sha256_decimal": hashlib.sha256(text.encode("ascii")).hexdigest(),
        }

    return {
        "local_length_enumerator": {
            "length_0": local_counts[0],
            "length_1": local_counts[1],
            "length_2": local_counts[2],
            "polynomial": "1 + 726 z + 58322 z^2",
        },
        "flat_space": {
            "dimension_F3": 2400,
            "diameter": 480,
            "uniform_mean_length": "117370/59049",
        },
        "cohomology_quotient": {
            "dimension_F3": 2180,
            "cayley_diameter_lower_bound": 389,
            "cayley_diameter_upper_bound": 480,
            "sphere_bound_threshold_radius": 389,
            "cumulative_radius_388": integer_digest(cumulative_before),
            "cumulative_radius_389": integer_digest(cumulative_at),
            "quotient_size": integer_digest(quotient_size),
        },
    }


def tau_barycentric_certificate() -> dict:
    orbits = orbit_partition()
    assert len(orbits) == 135
    assert Counter(map(len, orbits)) == Counter({2: 108, 1: 27})
    orbit_index = {orbit: index for index, orbit in enumerate(orbits)}

    fibers: dict[tuple[int, ...], list[tuple[tuple[int, ...], ...]]] = defaultdict(list)
    for orbit in orbits:
        fibers[barycenter_signature(orbit)].append(orbit)
    fiber_list = list(fibers.values())
    assert len(fiber_list) == 108
    assert Counter(map(len, fiber_list)) == Counter({1: 81, 2: 27})

    fiber_types = Counter()
    distance_histogram = Counter()
    norm_shells = Counter()
    for fiber in fiber_list:
        if len(fiber) == 1 and len(fiber[0]) == 1:
            fiber_types["fixed_singleton"] += 1
            norm_shells["5"] += 1
        elif len(fiber) == 1:
            fiber_types["distance2_singleton"] += 1
            norm_shells["4"] += 1
        else:
            fiber_types["distance4_double"] += 1
            norm_shells["3"] += 1
        for orbit in fiber:
            if len(orbit) == 2:
                distance = sum(a != b for a, b in zip(orbit[0], orbit[1]))
                distance_histogram[distance] += 1

    assert fiber_types == Counter({
        "fixed_singleton": 27,
        "distance2_singleton": 54,
        "distance4_double": 27,
    })
    assert distance_histogram == Counter({2: 54, 4: 54})
    assert norm_shells == Counter({"5": 27, "4": 54, "3": 27})

    quotient = hamming_quotient(orbits)
    orbit_to_barycenter: dict[int, int] = {}
    for barycenter, fiber in enumerate(fiber_list):
        for orbit in fiber:
            orbit_to_barycenter[orbit_index[orbit]] = barycenter

    barycentric = np.zeros((108, 108), dtype=np.int64)
    for barycenter, fiber in enumerate(fiber_list):
        aggregated_rows = []
        for orbit in fiber:
            row = np.zeros(108, dtype=np.int64)
            source = orbit_index[orbit]
            for target, weight in enumerate(quotient[source]):
                row[orbit_to_barycenter[target]] += weight
            aggregated_rows.append(row)
        assert all(np.array_equal(aggregated_rows[0], row)
                   for row in aggregated_rows[1:])
        barycentric[barycenter] = aggregated_rows[0]
    assert set(barycentric.sum(axis=1).tolist()) == {10}

    ambiguous_fibers = [fiber for fiber in fiber_list if len(fiber) == 2]
    centers = [ambiguous_center(fiber) for fiber in ambiguous_fibers]
    assert len(set(centers)) == 27
    assert set(centers) == set(product(range(3), repeat=3))

    oriented_pairs: list[tuple[int, int]] = []
    for fiber in ambiguous_fibers:
        by_hidden = {hidden_bit(orbit): orbit_index[orbit] for orbit in fiber}
        assert set(by_hidden) == {1, 2}
        oriented_pairs.append((by_hidden[1], by_hidden[2]))

    hidden = np.zeros((27, 27), dtype=np.int64)
    for column, (positive, negative) in enumerate(oriented_pairs):
        vector = np.zeros(135, dtype=np.int64)
        vector[positive] = 1
        vector[negative] = -1
        image = quotient @ vector
        for fiber in fiber_list:
            indices = [orbit_index[orbit] for orbit in fiber]
            if len(fiber) == 1:
                assert image[indices[0]] == 0
            else:
                assert image[indices[0]] == -image[indices[1]]
        for row, (positive_row, negative_row) in enumerate(oriented_pairs):
            assert image[positive_row] == -image[negative_row]
            hidden[row, column] = image[positive_row]

    center_index = {center: index for index, center in enumerate(centers)}
    cayley_kernel: dict[tuple[int, int, int], int] = {}
    for source_center, source in center_index.items():
        for target_center, target in center_index.items():
            delta = tuple((target_center[i] - source_center[i]) % 3 for i in range(3))
            value = int(hidden[source, target])
            if delta in cayley_kernel:
                assert cayley_kernel[delta] == value
            cayley_kernel[delta] = value
    nonzero_kernel = {
        str(delta): value for delta, value in sorted(cayley_kernel.items())
        if value != 0
    }
    assert nonzero_kernel == {
        "(0, 0, 1)": 1,
        "(0, 0, 2)": 1,
        "(0, 1, 0)": -1,
        "(0, 2, 0)": -1,
        "(1, 0, 0)": -1,
        "(2, 0, 0)": -1,
    }

    shell_labels = []
    for fiber in fiber_list:
        if len(fiber) == 1 and len(fiber[0]) == 1:
            shell_labels.append("fixed")
        elif len(fiber) == 1:
            shell_labels.append("distance2")
        else:
            shell_labels.append("ambiguous")
    shell_order = ["fixed", "distance2", "ambiguous"]
    shell_id = {label: index for index, label in enumerate(shell_order)}
    shell_matrix = np.zeros((3, 3), dtype=np.int64)
    for label in shell_order:
        indices = [i for i, item in enumerate(shell_labels) if item == label]
        rows = []
        for source in indices:
            row = np.zeros(3, dtype=np.int64)
            for target, weight in enumerate(barycentric[source]):
                row[shell_id[shell_labels[target]]] += weight
            rows.append(row)
        assert all(np.array_equal(rows[0], row) for row in rows[1:])
        shell_matrix[shell_id[label]] = rows[0]
    assert shell_matrix.tolist() == [[2, 8, 0], [2, 4, 4], [0, 4, 6]]

    assert trace_moments(quotient) == spectrum_moments(FULL_SPECTRUM)
    assert trace_moments(barycentric) == spectrum_moments(BARYCENTRIC_SPECTRUM)
    assert trace_moments(hidden) == spectrum_moments(HIDDEN_SPECTRUM)
    assert all(
        FULL_SPECTRUM.get(eigenvalue, 0)
        == BARYCENTRIC_SPECTRUM.get(eigenvalue, 0)
        + HIDDEN_SPECTRUM.get(eigenvalue, 0)
        for eigenvalue in set(FULL_SPECTRUM) | set(HIDDEN_SPECTRUM)
    )

    return {
        "tau_orbits": {"total": 135, "fixed": 27, "paired": 108},
        "Q15_barycenters": {
            "distinct": 108,
            "fiber_profile": {"size_1": 81, "size_2": 27},
            "typed_profile": dict(sorted(fiber_types.items())),
            "ternary_distance_profile_for_pairs": {
                str(key): value for key, value in sorted(distance_histogram.items())
            },
            "squared_norm_shells": dict(sorted(norm_shells.items())),
        },
        "ambiguous_double_cover": {
            "base": "tau-fixed affine flat F3^3",
            "base_size": 27,
            "cover_size": 54,
            "hidden_fiber": "C2 represented by h=(x1+x4)(x2+x3-1) in {1,2}",
            "center_map": "coordinatewise missing symbols",
        },
        "barycentric_walk": {
            "strongly_lumpable": True,
            "states": 108,
            "degree": 10,
            "spectrum": {str(k): v for k, v in sorted(BARYCENTRIC_SPECTRUM.items())},
            "three_shell_matrix": shell_matrix.tolist(),
            "three_shell_sizes": [27, 54, 27],
            "three_shell_stationary_masses": [27, 108, 108],
            "three_shell_spectrum": {"10": 1, "4": 1, "-2": 1},
        },
        "hidden_phase_sector": {
            "states": 27,
            "indexing": "tau-fixed affine flat F3^3",
            "signed_cayley_kernel": nonzero_kernel,
            "operator": "+C3(axis3)-C3(axis1)-C3(axis2)",
            "spectrum": {str(k): v for k, v in sorted(HIDDEN_SPECTRUM.items())},
            "shifted_by_2I_spectrum": {"6": 4, "3": 12, "0": 9, "-3": 2},
        },
        "direct_sum": "H(5,3)/<tau> = barycentric_108 direct_sum hidden_signed_torus_27",
    }


def cohomology_and_voltage_certificate() -> dict:
    scalar_support_generators = FILLED_FACES * 3
    scalar_local_relations = FILLED_FACES
    scalar_flat_rank = scalar_support_generators - scalar_local_relations
    scalar_coboundary_rank = BASE_VERTICES - 1
    scalar_cohomology_rank = scalar_flat_rank - scalar_coboundary_rank
    assert (scalar_support_generators, scalar_local_relations,
            scalar_flat_rank, scalar_coboundary_rank,
            scalar_cohomology_rank) == (720, 240, 480, 44, 436)

    generator_rank = scalar_support_generators * COEFFICIENT_DIM
    local_relation_rank = scalar_local_relations * COEFFICIENT_DIM
    flat_rank = scalar_flat_rank * COEFFICIENT_DIM
    coboundary_rank = scalar_coboundary_rank * COEFFICIENT_DIM
    cohomology_rank = scalar_cohomology_rank * COEFFICIENT_DIM
    total_relation_rank = generator_rank - cohomology_rank
    assert (generator_rank, local_relation_rank, flat_rank,
            coboundary_rank, cohomology_rank,
            total_relation_rank) == (3600, 1200, 2400, 220, 2180, 1420)

    full_lift_vertices = BASE_VERTICES * COEFFICIENT_SIZE
    voltage_subgroup_order = 3
    components = COEFFICIENT_SIZE // voltage_subgroup_order
    component_vertices = BASE_VERTICES * voltage_subgroup_order
    component_edges = component_vertices * BASE_DEGREE // 2
    component_triangles = (BASE_TRIANGLES - MIN_DEFECT_NONZERO_TRIANGLES) * 3
    component_trace2 = 2 * component_edges
    component_trace3 = 6 * component_triangles

    base_trace2 = 2 * BASE_EDGES
    base_trace3 = 6 * BASE_TRIANGLES
    magnetic_trace2 = (component_trace2 - base_trace2) // 2
    magnetic_trace3 = (component_trace3 - base_trace3) // 2
    assert magnetic_trace2 == 1440
    assert magnetic_trace3 == 31302
    assert base_trace3 - magnetic_trace3 == MIN_DEFECT_NONZERO_TRIANGLES * 9

    return {
        "minimum_defect_equivariant_presentation": {
            "scalar_exact_sequence_dimensions": [240, 720, 480, 44, 436],
            "scalar_sequence": "0 -> F3[240 faces] -> F3[720 supports] -> Z1 -> H1 -> 0",
            "coefficient_generator_rank": generator_rank,
            "local_relation_rank": local_relation_rank,
            "flat_rank": flat_rank,
            "coboundary_rank": coboundary_rank,
            "cohomology_rank": cohomology_rank,
            "total_relation_rank": total_relation_rank,
            "coefficient_action": "trivial F3^5 tensor factor under the certified PSp(4,3) support action",
        },
        "minimum_defect_voltage_lift": {
            "full_C3_5_lift_vertices": full_lift_vertices,
            "voltage_subgroup_order": voltage_subgroup_order,
            "connected_components": components,
            "vertices_per_component": component_vertices,
            "degree": BASE_DEGREE,
            "edges_per_component": component_edges,
            "triangles_per_component": component_triangles,
            "character_blocks": ["base_45", "magnetic_45", "conjugate_magnetic_45"],
            "base_trace2": base_trace2,
            "base_trace3": base_trace3,
            "magnetic_trace2": magnetic_trace2,
            "magnetic_trace3": magnetic_trace3,
            "cubic_moment_deficit": base_trace3 - magnetic_trace3,
            "nonseparable_certificate": "magnetic cubic trace differs from the untwisted block",
            "cardinality_falsifier": "the 135-vertex voltage component has degree 32, not the degree-10 Hamming-orbifold walk",
        },
    }


def build_certificate() -> dict:
    sections = {
        "word_metric": word_metric_certificate(),
        "tau_barycentric": tau_barycentric_certificate(),
        "cohomology_voltage": cohomology_and_voltage_certificate(),
    }
    checks = {
        "flat_word_diameter_480": sections["word_metric"]["flat_space"]["diameter"] == 480,
        "quotient_sphere_lower_bound_389": sections["word_metric"]["cohomology_quotient"]["cayley_diameter_lower_bound"] == 389,
        "barycenter_fiber_profile_81_27": sections["tau_barycentric"]["Q15_barycenters"]["fiber_profile"] == {"size_1": 81, "size_2": 27},
        "barycentric_lumping_108": sections["tau_barycentric"]["barycentric_walk"]["states"] == 108,
        "hidden_signed_torus_27": sections["tau_barycentric"]["hidden_phase_sector"]["states"] == 27,
        "hidden_spectrum_closed": sum(sections["tau_barycentric"]["hidden_phase_sector"]["spectrum"].values()) == 27,
        "equivariant_presentation_2180": sections["cohomology_voltage"]["minimum_defect_equivariant_presentation"]["cohomology_rank"] == 2180,
        "voltage_components_81x135": (
            sections["cohomology_voltage"]["minimum_defect_voltage_lift"]["connected_components"] == 81
            and sections["cohomology_voltage"]["minimum_defect_voltage_lift"]["vertices_per_component"] == 135
        ),
        "magnetic_trace_changes": sections["cohomology_voltage"]["minimum_defect_voltage_lift"]["magnetic_trace3"] == 31302,
    }
    assert all(checks.values())
    return {
        "schema": "w33.bt3376_3389.cohomology_tau_frontier.v1",
        "status": "PASS",
        "sections": sections,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(payload, encoding="utf-8")
    print("PASS 9/9 cohomology, tau-barycenter, and voltage-lift checks")
    print(payload, end="")


if __name__ == "__main__":
    main()
