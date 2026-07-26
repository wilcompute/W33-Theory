#!/usr/bin/env python3
"""Pass 1055: unsigned equivariance and the signed-lift obstruction.

The intrinsic W33 axis -> E8 root-line map is exactly PSp(4,3)-equivariant.
Attempting to lift the 120 root lines to the 240 signed roots introduces one
binary gauge variable per axis. Exact GF(2) elimination gives an inconsistency;
a four-equation certificate XORs to 0 = 1.
"""
from __future__ import annotations

import json
from pathlib import Path

from sympy.combinatorics import PermutationGroup

from w33_pass1054_1059_core import build_axes, build_e8_residues, build_quadratic_isometry, build_quotient, build_w33_bundle, dot_scaled

SELECTED_GENERATORS = [6, 19, 22, 39]


def equation_for_pair(generator_index, axis_left, axis_right, axis_generators, endpoint_swap_bits, representatives):
    action = axis_generators[generator_index]
    left_image = action(axis_left)
    right_image = action(axis_right)
    before = dot_scaled(representatives[axis_left], representatives[axis_right])
    after = dot_scaled(representatives[left_image], representatives[right_image])
    if before == 0 or after == 0 or abs(before) != abs(after):
        raise AssertionError("equation requested for an incompatible root-line pair")
    swaps = endpoint_swap_bits[generator_index]
    rhs = (0 if before == after else 1) ^ swaps[axis_left] ^ swaps[axis_right]
    mask = (1 << axis_left) ^ (1 << left_image) ^ (1 << axis_right) ^ (1 << right_image)
    return mask, rhs, {
        "generator": generator_index,
        "axis_pair": [axis_left, axis_right],
        "image_pair": [left_image, right_image],
        "scaled_inner_product_before": before,
        "scaled_inner_product_after": after,
        "endpoint_swap_bits": [swaps[axis_left], swaps[axis_right]],
        "equation_variables": [index for index in range(120) if (mask >> index) & 1],
        "rhs": rhs,
    }


def main() -> dict[str, object]:
    bundle = build_w33_bundle()
    quotient = build_quotient(bundle)
    axes = build_axes(bundle, quotient)
    e8 = build_e8_residues()
    isometry, source_basis, target_basis = build_quadratic_isometry(quotient, e8)

    anisotropic_index = {coordinate: index for index, coordinate in enumerate(quotient.anisotropic)}
    quotient_anisotropic_generators = [[anisotropic_index[generator(coordinate)] for coordinate in quotient.anisotropic] for generator in quotient.quotient_generators]

    unsigned_equivariance_failures = 0
    for axis_generator, quotient_images in zip(axes.axis_generators, quotient_anisotropic_generators):
        for axis_index, coordinate in enumerate(axes.axis_coordinates):
            moved_coordinate = axes.axis_coordinates[axis_generator(axis_index)]
            expected = quotient.anisotropic[quotient_images[anisotropic_index[coordinate]]]
            if moved_coordinate != expected:
                unsigned_equivariance_failures += 1

    representatives = [e8.positive_by_residue[isometry[coordinate]] for coordinate in axes.axis_coordinates]
    endpoint_index = {endpoint: index for index, endpoint in enumerate(axes.endpoints)}
    endpoints_by_axis = [[] for _ in range(120)]
    for endpoint in axes.endpoints:
        axis_index, sign = axes.endpoint_axis_sign[endpoint]
        if sign == 1:
            endpoints_by_axis[axis_index].insert(0, endpoint)
        else:
            endpoints_by_axis[axis_index].append(endpoint)
    if any(len(pair) != 2 for pair in endpoints_by_axis):
        raise AssertionError("endpoint pairing failed")

    endpoint_swap_bits = []
    for endpoint_generator, axis_generator in zip(axes.endpoint_generators, axes.axis_generators):
        bits = []
        for axis_index, pair in enumerate(endpoints_by_axis):
            moved_endpoint = axes.endpoints[endpoint_generator(endpoint_index[pair[0]])]
            image_axis = axis_generator(axis_index)
            bits.append(0 if moved_endpoint == endpoints_by_axis[image_axis][0] else 1)
        endpoint_swap_bits.append(bits)

    selected_group = PermutationGroup([bundle.point_generators[index] for index in SELECTED_GENERATORS])
    unique_equations = []
    metadata = []
    seen = set()
    for generator_index in SELECTED_GENERATORS:
        for left in range(120):
            for right in range(left + 1, 120):
                if dot_scaled(representatives[left], representatives[right]) == 0:
                    continue
                equation = equation_for_pair(generator_index, left, right, axes.axis_generators, endpoint_swap_bits, representatives)
                key = equation[:2]
                if key not in seen:
                    seen.add(key)
                    unique_equations.append(key)
                    metadata.append(equation[2])

    pivots = {}
    contradiction_provenance = None
    contradiction_row = None
    for row_index, (mask_start, rhs_start) in enumerate(unique_equations):
        mask, rhs = mask_start, rhs_start
        provenance = 1 << row_index
        while mask:
            pivot = mask.bit_length() - 1
            if pivot in pivots:
                old_mask, old_rhs, old_provenance = pivots[pivot]
                mask ^= old_mask
                rhs ^= old_rhs
                provenance ^= old_provenance
            else:
                pivots[pivot] = (mask, rhs, provenance)
                break
        if mask == 0 and rhs == 1:
            contradiction_provenance = provenance
            contradiction_row = row_index
            break
    if contradiction_provenance is None:
        raise AssertionError("signed-lift system unexpectedly has a solution")

    certificate_indices = [index for index in range(len(unique_equations)) if (contradiction_provenance >> index) & 1]
    certificate = [metadata[index] for index in certificate_indices]
    certificate_mask = 0
    certificate_rhs = 0
    for index in certificate_indices:
        certificate_mask ^= unique_equations[index][0]
        certificate_rhs ^= unique_equations[index][1]

    rootline_orthogonality_failures = 0
    for left in range(120):
        for right in range(120):
            coordinate_left = axes.axis_coordinates[left]
            coordinate_right = axes.axis_coordinates[right]
            source_bilinear = (quotient.coordinate_representative[coordinate_left] & quotient.coordinate_representative[coordinate_right]).bit_count() % 2
            root_orthogonal = dot_scaled(representatives[left], representatives[right]) == 0
            if left != right and root_orthogonal != (source_bilinear == 0):
                rootline_orthogonality_failures += 1

    code_orbits = sorted(len(orbit) for orbit in quotient.quotient_group.orbits())
    axis_group = PermutationGroup(axes.axis_generators)
    axis_subdegrees = sorted(len(orbit) for orbit in axis_group.stabilizer(0).orbits())

    checks = {
        "PSp43_selected_generators_generate_full_group": selected_group.order() == 25920,
        "code_quotient_orbits_are_1_120_135": code_orbits == [1, 120, 135],
        "axes_are_all_120_anisotropic_coordinates": len(set(axes.axis_coordinates)) == 120 and set(axes.axis_coordinates) == set(quotient.anisotropic),
        "unsigned_axis_map_is_equivariant": unsigned_equivariance_failures == 0,
        "axis_action_is_transitive_order_25920": axis_group.order() == 25920 and axis_group.is_transitive(),
        "axis_action_rank7_subdegrees": axis_subdegrees == [1, 1, 1, 27, 27, 27, 36],
        "axis_pairing_equals_E8_rootline_orthogonality": rootline_orthogonality_failures == 0,
        "signed_gauge_system_is_inconsistent": contradiction_provenance is not None,
        "certificate_xors_to_zero_equals_one": certificate_mask == 0 and certificate_rhs == 1,
        "minimal_found_certificate_has_four_rows": len(certificate_indices) == 4,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])

    return {
        "schema": "w33.pass1055.unsigned_equivariant_signed_obstruction.v1",
        "status": "PASS",
        "headline": "The 120 W33 local axes are equivariantly identical to the 120 E8 root lines under the code-quotient PSp(4,3) action, but the 240 endpoints cannot be made equivariant with the 240 signed roots. The sign-gauge equations over F2 are inconsistent; four explicit equations XOR to 0=1.",
        "unsigned_layer": {"axes": 120, "anisotropic_coordinates": 120, "group_order": int(axis_group.order()), "subdegrees": axis_subdegrees, "equivariance_failures": unsigned_equivariance_failures, "quadratic_isometry_source_basis": source_basis, "quadratic_isometry_target_basis": target_basis},
        "signed_layer": {"endpoints": 240, "gauge_variables": 120, "selected_generators": SELECTED_GENERATORS, "unique_equations_before_contradiction": contradiction_row + 1, "elimination_rank_at_contradiction": len(pivots), "certificate_size": len(certificate), "certificate": certificate, "certificate_xor": {"mask": certificate_mask, "rhs": certificate_rhs}},
        "interpretation": "The Z3 axis choice descends equivariantly, while the Z2 endpoint/sign choice does not. The finite obstruction is not merely the absence of a preferred chamber: no reassignment of the 120 endpoint signs can repair it.",
        "check_count": len(checks),
        "checks": checks,
        "scope": "Exact finite computation. It proves equivariance for the unsigned code embedding and proves a no-go for an internal signed lift. It does not rule out an external extension, semilinear conjugation, or an S3 controller.",
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1055_unsigned_equivariant_signed_obstruction.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "certificate": result["signed_layer"]["certificate"], "check_count": result["check_count"]}, indent=2))
