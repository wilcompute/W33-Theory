#!/usr/bin/env python3
"""Pass 174: dual discriminant actions and the fixed order-eight rail.

Pass 173 separated the address and route dark lattices.  This witness
computes the outer involution on both 2-primary discriminant modules and
corrects the interpretation of the v4 cohomology certificate.

For an order-eight generator h, write tau(h)=c*h+u_c with c odd.
The existing address calculation used c=5 and found [u_5]=[4h] != 0.
That obstructs a *pure scalar-5* normal form, but it does not obstruct a
fixed generator.  Relative to c=1, u_1=u_5+4h is a coboundary, so an
order-two shift h'=h+v satisfies tau(h')=h'.  The same phenomenon occurs
on the new route module.

The two modules nevertheless remain sharply asymmetric:

  address: (Z/2)^14 + Z/8, dim H^1 = 3, 512 fixed shifts;
  route:   (Z/2)^8  + Z/8, dim H^1 = 1,  32 fixed shifts.

Exactly half of the fixed shifts on each side preserve q(h)=11/8; the
other half give 3/8.  Thus 11/8 is a choice of quadratic orbit, not a
canonical value of every order-eight generator.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_levi_next5_v4_common import (
    build_w33,
    coordinates,
    dot2,
    gf2_nullspace,
    gf2_rank,
    gf2_row_basis,
    group_closure_cols,
    line_perm_from_point_perm,
    point_outer_perm,
    point_transvection_perm,
    permute_mask,
    quotient_basis,
    SEEDS,
    sha256_json,
    tagged_basis,
)
from w33_levi_next5_v4_cohomology import (
    action_in_p2,
    add_coord,
    apply_auto,
    apply_cols,
    gf2_nullspace_map,
    in_span,
    p2_structure,
    perm_matrix_action,
    q_num128,
    saturated_kernel,
    scale_coord,
    smith,
    torsion_basis,
    torsion_cols,
    torsion_mask,
)


OUT = ROOT / "data" / "w33_pass174_dual_discriminant_fixed_rail.json"


EXPECTED = {
    "address": {
        "mods": [2] * 14 + [8],
        "kernel_basis": [0x3F, 0x5E, 0x8E, 0x118, 0x207, 0xC07, 0x100A, 0x240A, 0x4000],
        "image_basis": [0x5DC5, 0x3518, 0x12E2, 0xFF7, 0x2D7, 0xEF],
        "h1_reps": [0x3F, 0x5E, 0x118],
        "u1_mask": 0x7527,
        "u5_mask": 0x3527,
        "fixed_line_mask": 0x4000,
        "actual_coefficient": 5,
        "fixed_shifts": 512,
        "q_preserving_shifts": 256,
        "smallest_q_preserving_shift": 0x44F,
        "all_shift_digest": "ecb459a1e5039b23d741f86857c45b14878cda71e268443394bb3cc70cd2840b",
        "q_shift_digest": "6199dcd8be51c8351933b5aad4fd7ec3901107796a42249a636520a39a9d349e",
    },
    "route": {
        "mods": [2] * 8 + [8],
        "kernel_basis": [0x2, 0x4, 0x60, 0x80, 0x100],
        "image_basis": [0x180, 0xE4, 0x62, 0x2],
        "h1_reps": [0x4],
        "u1_mask": 0x62,
        "u5_mask": 0x162,
        "fixed_line_mask": 0x100,
        "actual_coefficient": 1,
        "fixed_shifts": 32,
        "q_preserving_shifts": 16,
        "smallest_q_preserving_shift": 0x1,
        "all_shift_digest": "366f8b0cc296c5d26dede2ab0104994346e266113acdc4d71f4bd9278c8d9f39",
        "q_shift_digest": "93bc1816f0648ebe5569041a689c78c2e629a3554bf4ad6fe02c34ae0cbe53c1",
        "basis_digest": "98e8c8243c625299a94a3b47ab91258b939f9ea51840c8b948431aec2831ce3b",
        "gram_digest": "996bfbaa799d92316109cabcd8f8daffa764c71779e9ed340c5af2d24702d97f",
        "smith_left_digest": "3d9aa8e35663b745971ae158b0c4bfebed9d931f5bbc456e211e806cfeaa8274",
        "smith_right_digest": "421cb89118c871e83f10031d45c414af759b0daa0110a67399a03d8cf3141b0a",
        "integral_outer_digest": "374bf650d507e5d13bf26fcdf8381acfebdca1062c8f87fb55c9ad827cb5ac15",
        "p2_outer_digest": "de31edaeef95c36b57c989ca5a6fec1fb6772fcd55cd13d0a52548f7f8b99d4e",
    },
}


def matrix_json(matrix: Matrix) -> list[list[int]]:
    return [
        [int(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def mask_coord(mask: int, mods: list[int]) -> tuple[int, ...]:
    out = (0,) * len(mods)
    for index, basis_vector in enumerate(torsion_basis(mods)):
        if (mask >> index) & 1:
            out = add_coord(out, basis_vector, mods)
    return out


def quotient_coordinates(
    value: int, image_basis: list[int], h1_reps: list[int]
) -> int:
    tagged = tagged_basis(image_basis + h1_reps)
    remainder, tag = coordinates(value, tagged)
    assert remainder == 0
    return tag >> len(image_basis)


def side_certificate(
    label: str,
    operator: Matrix,
    permutation: tuple[int, ...],
) -> dict:
    expected = EXPECTED[label]
    basis = saturated_kernel(operator)
    gram = basis.T * basis
    diagonal, smith_left, smith_right = smith(gram)
    diagonal_values = [abs(int(diagonal[i, i])) for i in range(diagonal.rows)]
    parts = p2_structure(diagonal)
    mods = [part["p_order"] for part in parts]

    integral_outer = perm_matrix_action(basis, permutation)
    outer = action_in_p2(integral_outer, smith_left, diagonal, parts)
    h_index = mods.index(8)
    h = tuple(1 if index == h_index else 0 for index in range(len(mods)))
    outer_h = apply_auto(outer, h, mods)
    actual_coefficient = outer_h[h_index]

    scalar1 = h
    scalar5 = scale_coord(5, h, mods)
    u1_coord = add_coord(outer_h, scale_coord(-1, scalar1, mods), mods)
    u5_coord = add_coord(outer_h, scale_coord(-1, scalar5, mods), mods)
    u1_mask = torsion_mask(u1_coord, mods)
    u5_mask = torsion_mask(u5_coord, mods)

    tau_columns = torsion_cols(outer, mods)
    identity_columns = tuple(1 << index for index in range(len(mods)))
    norm_columns = tuple(
        tau_columns[index] ^ identity_columns[index]
        for index in range(len(mods))
    )
    kernel_basis = gf2_nullspace_map(norm_columns, len(mods))
    image_basis = gf2_row_basis(norm_columns)
    h1_reps: list[int] = []
    quotient_span = list(image_basis)
    for vector in kernel_basis:
        if not in_span(vector, quotient_span):
            h1_reps.append(vector)
            quotient_span = gf2_row_basis(quotient_span + [vector])

    fixed_line_mask = 1 << h_index
    u1_h1 = quotient_coordinates(u1_mask, image_basis, h1_reps)
    u5_h1 = quotient_coordinates(u5_mask, image_basis, h1_reps)
    fixed_line_h1 = quotient_coordinates(fixed_line_mask, image_basis, h1_reps)

    fixed_shifts = [
        mask
        for mask in range(1 << len(mods))
        if apply_cols(norm_columns, mask) == u1_mask
    ]
    q_h_num = q_num128(h, parts, smith_left, diagonal, gram)
    fixed_generators = []
    q_preserving_shifts = []
    q_distribution: dict[int, int] = {}
    for shift_mask in fixed_shifts:
        shift_coord = mask_coord(shift_mask, mods)
        h_prime = add_coord(h, shift_coord, mods)
        assert apply_auto(outer, h_prime, mods) == h_prime
        q_num = q_num128(h_prime, parts, smith_left, diagonal, gram)
        q_distribution[q_num] = q_distribution.get(q_num, 0) + 1
        fixed_generators.append(h_prime)
        if q_num == q_h_num:
            q_preserving_shifts.append(shift_mask)

    q_u1_num = q_num128(u1_coord, parts, smith_left, diagonal, gram)
    q_u5_num = q_num128(u5_coord, parts, smith_left, diagonal, gram)
    smallest_shift = min(q_preserving_shifts)
    smallest_h_prime = add_coord(h, mask_coord(smallest_shift, mods), mods)

    checks = {
        "module_type": mods == expected["mods"],
        "outer_is_involution": all(
            apply_cols(tau_columns, apply_cols(tau_columns, 1 << index))
            == (1 << index)
            for index in range(len(mods))
        ),
        "actual_scalar_coefficient": actual_coefficient
        == expected["actual_coefficient"],
        "cohomology_kernel_basis": kernel_basis == expected["kernel_basis"],
        "cohomology_image_basis": image_basis == expected["image_basis"],
        "cohomology_h1_basis": h1_reps == expected["h1_reps"],
        "scalar1_displacement": u1_mask == expected["u1_mask"],
        "scalar5_displacement": u5_mask == expected["u5_mask"],
        "fixed_line": fixed_line_mask == expected["fixed_line_mask"],
        "scalar1_is_coboundary": in_span(u1_mask, image_basis) and u1_h1 == 0,
        "scalar5_is_fixed_line_class": (
            not in_span(u5_mask, image_basis)
            and u5_h1 == fixed_line_h1 != 0
        ),
        "fixed_shift_count": len(fixed_shifts) == expected["fixed_shifts"],
        "q_preserving_count": len(q_preserving_shifts)
        == expected["q_preserving_shifts"],
        "smallest_q_preserving_shift": smallest_shift
        == expected["smallest_q_preserving_shift"],
        "fixed_shift_digest": sha256_json(fixed_shifts)
        == expected["all_shift_digest"],
        "q_preserving_shift_digest": sha256_json(q_preserving_shifts)
        == expected["q_shift_digest"],
        "q_generator_two_orbits": q_distribution
        == {88: expected["q_preserving_shifts"], 24: expected["q_preserving_shifts"]},
        "fixed_generator_preserves_q": (
            apply_auto(outer, smallest_h_prime, mods) == smallest_h_prime
            and q_num128(smallest_h_prime, parts, smith_left, diagonal, gram)
            == q_h_num
        ),
    }

    if label == "route":
        checks.update(
            {
                "route_basis_digest": sha256_json(matrix_json(basis))
                == expected["basis_digest"],
                "route_gram_digest": sha256_json(matrix_json(gram))
                == expected["gram_digest"],
                "route_smith_left_digest": sha256_json(matrix_json(smith_left))
                == expected["smith_left_digest"],
                "route_smith_right_digest": sha256_json(matrix_json(smith_right))
                == expected["smith_right_digest"],
                "route_integral_outer_digest": sha256_json(matrix_json(integral_outer))
                == expected["integral_outer_digest"],
                "route_p2_outer_digest": sha256_json(outer)
                == expected["p2_outer_digest"],
            }
        )

    q_h = Fraction(q_h_num, 64)
    while q_h >= 2:
        q_h -= 2
    q_u1 = Fraction(q_u1_num, 64)
    while q_u1 >= 2:
        q_u1 -= 2
    q_u5 = Fraction(q_u5_num, 64)
    while q_u5 >= 2:
        q_u5 -= 2

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "lattice": {
            "rank": basis.cols,
            "gram_determinant": int(gram.det()),
            "gram_snf": diagonal_values,
            "p2_module": f"(Z/2)^{len(mods)-1} + Z/8",
            "p2_order_exponent": len(mods) + 2,
        },
        "outer": {
            "actual_h_image": list(outer_h),
            "actual_scalar_coefficient": actual_coefficient,
            "torsion_action_columns_hex": [hex(value) for value in tau_columns],
            "one_plus_tau_columns_hex": [hex(value) for value in norm_columns],
        },
        "cohomology": {
            "kernel_dimension": len(kernel_basis),
            "image_dimension": len(image_basis),
            "H1_dimension": len(h1_reps),
            "kernel_basis_hex": [hex(value) for value in kernel_basis],
            "image_basis_hex": [hex(value) for value in image_basis],
            "H1_basis_hex": [hex(value) for value in h1_reps],
            "scalar1_displacement_mask": hex(u1_mask),
            "scalar1_H1_coordinates": hex(u1_h1),
            "scalar1_is_coboundary": in_span(u1_mask, image_basis),
            "scalar5_displacement_mask": hex(u5_mask),
            "scalar5_H1_coordinates": hex(u5_h1),
            "scalar5_is_coboundary": in_span(u5_mask, image_basis),
            "fixed_line_mask": hex(fixed_line_mask),
            "fixed_line_H1_coordinates": hex(fixed_line_h1),
            "interpretation": (
                "[u_5]=[4h] obstructs a pure scalar-5 normal form; "
                "u_1=u_5+4h is a coboundary, so a fixed generator exists"
            ),
        },
        "fixed_order8_rail": {
            "shift_count": len(fixed_shifts),
            "q_preserving_shift_count": len(q_preserving_shifts),
            "q_h": str(q_h),
            "q_distribution_numerator_over_64": {
                str(key): value for key, value in sorted(q_distribution.items())
            },
            "smallest_q_preserving_shift_mask": hex(smallest_shift),
            "fixed_generator": list(smallest_h_prime),
            "fixed_generator_q": str(q_h),
            "all_shift_digest": sha256_json(fixed_shifts),
            "q_preserving_shift_digest": sha256_json(q_preserving_shifts),
        },
        "quadratic_displacements": {
            "q_u1": str(q_u1),
            "q_u5": str(q_u5),
            "warning": (
                "q(h)=11/8 is preserved by only half the fixed shifts; "
                "the other half have q(h')=3/8"
            ),
        },
    }


def route_hull_certificate(geometry) -> dict:
    """The [40,9,16] route hull and its plus-type 8-space quotient."""
    incidence = Matrix(geometry.incidence.tolist())
    route_basis = saturated_kernel(incidence.T)
    code_rows = gf2_row_basis(
        sum((int(route_basis[row, column]) & 1) << row for row in range(40))
        for column in range(route_basis.cols)
    )
    assert len(code_rows) == 15

    gram_rows = []
    for left in code_rows:
        row_mask = 0
        for column, right in enumerate(code_rows):
            if dot2(left, right):
                row_mask |= 1 << column
        gram_rows.append(row_mask)
    hull_coefficients = gf2_nullspace(gram_rows, 15)
    hull_basis = gf2_row_basis(
        apply_cols(tuple(code_rows), coefficient)
        for coefficient in hull_coefficients
    )
    assert len(hull_basis) == 9

    hull_words = [
        apply_cols(tuple(hull_basis), coefficient)
        for coefficient in range(1 << 9)
    ]
    hull_weights = Counter(word.bit_count() for word in hull_words)
    all_ones = (1 << 40) - 1
    assert in_span(all_ones, hull_basis)

    # Identify the code hull quotient with the 2-torsion discriminant
    # quotient objectwise.  If c is a coefficient vector in the integral
    # route basis, c/2 is dual precisely when Gc is even, and its
    # discriminant quadratic value is c^T G c / 4 mod 2.
    route_gram = route_basis.T * route_basis
    route_D, route_S, _route_T = smith(route_gram)
    route_parts = p2_structure(route_D)
    tagged_code = tagged_basis(code_rows)
    hull_matches_discriminant = True
    all_ones_coefficients = None
    for word in hull_words:
        remainder, coefficient_mask = coordinates(word, tagged_code)
        assert remainder == 0
        coefficient = Matrix(
            [(coefficient_mask >> index) & 1 for index in range(15)]
        )
        gram_times = route_gram * coefficient
        hull_matches_discriminant &= all(int(value) % 2 == 0 for value in gram_times)
        numerator = int((coefficient.T * route_gram * coefficient)[0])
        hull_matches_discriminant &= numerator % 4 == 0
        hull_matches_discriminant &= ((numerator // 4) & 1) == (
            (word.bit_count() // 4) & 1
        )
        if word == all_ones:
            all_ones_coefficients = coefficient_mask

    assert all_ones_coefficients is not None
    all_ones_coefficient = Matrix(
        [(all_ones_coefficients >> index) & 1 for index in range(15)]
    )
    smith_y = route_S * route_gram * all_ones_coefficient / 2
    all_ones_p2 = []
    for part in route_parts:
        value = int(smith_y[part["snf_index"], 0])
        all_ones_p2.append(
            (value * pow(part["odd_part"], -1, part["p_order"]))
            % part["p_order"]
        )

    quotient = quotient_basis(hull_basis, [all_ones])
    assert len(quotient) == 8
    tagged = tagged_basis([all_ones] + quotient)

    def quotient_word(coordinate: int) -> int:
        return apply_cols(tuple(quotient), coordinate)

    def q_value(coordinate: int) -> int:
        return (quotient_word(coordinate).bit_count() // 4) & 1

    q_values = [q_value(coordinate) for coordinate in range(256)]
    q_counts = Counter(q_values)

    polar_rows = []
    for left in range(8):
        row_mask = 0
        x = 1 << left
        for right in range(8):
            y = 1 << right
            if q_value(x ^ y) ^ q_value(x) ^ q_value(y):
                row_mask |= 1 << right
        polar_rows.append(row_mask)

    point_generators = [
        point_transvection_perm(geometry.points, seed) for seed in SEEDS[:5]
    ]
    point_outer = point_outer_perm(geometry.points)
    line_generators = [
        line_perm_from_point_perm(geometry.lines, permutation)
        for permutation in point_generators
    ]
    line_outer = line_perm_from_point_perm(geometry.lines, point_outer)

    def quotient_action(line_permutation: tuple[int, ...]) -> tuple[int, ...]:
        columns = []
        for representative in quotient:
            moved = permute_mask(representative, line_permutation)
            remainder, tag = coordinates(moved, tagged)
            assert remainder == 0
            columns.append(tag >> 1)
        return tuple(columns)

    psp_actions = [quotient_action(permutation) for permutation in line_generators]
    outer_action = quotient_action(line_outer)
    psp_group = group_closure_cols(psp_actions, 8, 25920)
    extended_group = group_closure_cols(psp_actions + [outer_action], 8, 51840)

    def orbit_partition(actions: list[tuple[int, ...]]) -> list[set[int]]:
        unseen = set(range(256))
        orbits = []
        while unseen:
            seed = min(unseen)
            orbit = {seed}
            frontier = [seed]
            while frontier:
                current = frontier.pop()
                for action in actions:
                    image = apply_cols(action, current)
                    if image not in orbit:
                        orbit.add(image)
                        frontier.append(image)
            unseen -= orbit
            orbits.append(orbit)
        return orbits

    psp_orbits = orbit_partition(psp_actions)
    extended_orbits = orbit_partition(psp_actions + [outer_action])
    psp_orbit_report = sorted(
        (len(orbit), q_values[next(iter(orbit))]) for orbit in psp_orbits
    )

    # The symplectic graph uses polar-orthogonality adjacency on all 255
    # nonzero vectors.  Its q=0 and q=1 induced subgraphs are the two
    # orthogonal subconstituents from Pass 124.
    nonzero = list(range(1, 256))

    def polar(left: int, right: int) -> int:
        return q_value(left ^ right) ^ q_value(left) ^ q_value(right)

    def graph_parameters(vertices: list[int]) -> tuple[int, int, int, int]:
        vertex_set = set(vertices)
        neighbors = {
            vertex: {
                other
                for other in vertex_set
                if other != vertex and polar(vertex, other) == 0
            }
            for vertex in vertices
        }
        degrees = {len(value) for value in neighbors.values()}
        assert len(degrees) == 1
        degree = degrees.pop()
        adjacent_common = set()
        nonadjacent_common = set()
        for index, left in enumerate(vertices):
            for right in vertices[index + 1 :]:
                common = len(neighbors[left] & neighbors[right])
                if right in neighbors[left]:
                    adjacent_common.add(common)
                else:
                    nonadjacent_common.add(common)
        assert len(adjacent_common) == len(nonadjacent_common) == 1
        return (
            len(vertices),
            degree,
            adjacent_common.pop(),
            nonadjacent_common.pop(),
        )

    all_parameters = graph_parameters(nonzero)
    isotropic = [value for value in nonzero if q_values[value] == 0]
    anisotropic = [value for value in nonzero if q_values[value] == 1]
    isotropic_parameters = graph_parameters(isotropic)
    anisotropic_parameters = graph_parameters(anisotropic)

    checks = {
        "route_code_rank_15": len(code_rows) == 15,
        "route_code_gram_rank_6": gf2_rank(gram_rows) == 6,
        "route_hull_rank_9": len(hull_basis) == 9,
        "route_hull_40_9_16": hull_weights
        == Counter({0: 1, 16: 135, 20: 240, 24: 135, 40: 1}),
        "all_ones_is_fixed_radical": (
            all(permute_mask(all_ones, permutation) == all_ones for permutation in line_generators + [line_outer])
        ),
        "hull_quotient_dimension_8": len(quotient) == 8,
        "hull_quotient_plus_type": q_counts == Counter({0: 136, 1: 120}),
        "hull_quotient_polar_nondegenerate": gf2_rank(polar_rows) == 8,
        "hull_quadratic_equals_discriminant_quadratic": hull_matches_discriminant,
        "all_ones_is_discriminant_4h": (
            all_ones_coefficients == 0x7FFF
            and all_ones_p2 == [0] * 8 + [4]
        ),
        "psp_action_faithful_25920": len(psp_group) == 25920,
        "outer_extension_order_51840": len(extended_group) == 51840,
        "psp_orbits_1_135_120": psp_orbit_report == [(1, 0), (120, 1), (135, 0)],
        "outer_preserves_orbits": sorted(map(len, extended_orbits)) == [1, 120, 135],
        "sp8_graph_reconstructed": all_parameters == (255, 126, 61, 63),
        "isotropic_graph_reconstructed": isotropic_parameters == (135, 70, 37, 35),
        "anisotropic_graph_reconstructed": anisotropic_parameters == (120, 63, 30, 36),
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "route_code": {
            "parameters": "[40,15,10]",
            "binary_gram_rank": 6,
        },
        "hull": {
            "definition": "H = R intersect R^perp",
            "parameters": "[40,9,16]",
            "weight_enumerator": {
                str(weight): multiplicity
                for weight, multiplicity in sorted(hull_weights.items())
            },
            "fixed_radical": "<all-ones>",
            "fixed_radical_lattice_coefficients": hex(all_ones_coefficients),
            "fixed_radical_discriminant_coordinate": all_ones_p2,
        },
        "quotient": {
            "definition": "H/<all-ones>",
            "dimension": 8,
            "quadratic_form": "q([x]) = wt(x)/4 mod 2",
            "isotropic_vectors": q_counts[0],
            "anisotropic_vectors": q_counts[1],
            "type": "plus",
            "PSp_orbits": [1, 135, 120],
            "PSp_stabilizers": {"isotropic_nonzero": 192, "anisotropic": 216},
            "PSp_action_order": len(psp_group),
            "outer_extension_order": len(extended_group),
        },
        "capstone_graphs": {
            "all_nonzero": {
                "parameters": list(all_parameters),
                "name": "Sp(8,2) orthogonality graph",
            },
            "isotropic": {"parameters": list(isotropic_parameters)},
            "anisotropic": {"parameters": list(anisotropic_parameters)},
            "reading": (
                "the route-code hull reconstructs the full Pass-124 "
                "255=135+120 quadratic split"
            ),
        },
        "digests": {
            "code_basis": sha256_json(code_rows),
            "hull_basis": sha256_json(hull_basis),
            "quotient_basis": sha256_json(quotient),
            "psp_actions": sha256_json(psp_actions),
            "outer_action": sha256_json(outer_action),
        },
    }


def main() -> int:
    geometry = build_w33()
    incidence = Matrix(geometry.incidence.tolist())
    point_outer = point_outer_perm(geometry.points)
    line_outer = line_perm_from_point_perm(geometry.lines, point_outer)

    address = side_certificate("address", incidence, point_outer)
    route = side_certificate("route", incidence.T, line_outer)
    route_hull = route_hull_certificate(geometry)

    # The 2-torsion of the route discriminant has the same 136/120
    # plus-type quotient after dividing by its fixed radical <4h>.
    route_mods = [2] * 8 + [8]
    route_torsion_q = Counter()
    route_fixed_line = 1 << 8
    route_fixed_pair_ok = True
    # Rebuild the route Smith data once to evaluate its 512 torsion points.
    route_basis = saturated_kernel(incidence.T)
    route_gram = route_basis.T * route_basis
    route_D, route_S, _route_T = smith(route_gram)
    route_parts = p2_structure(route_D)
    for mask in range(512):
        coordinate = mask_coord(mask, route_mods)
        q_numerator = q_num128(coordinate, route_parts, route_S, route_D, route_gram)
        route_torsion_q[q_numerator] += 1
        paired = mask_coord(mask ^ route_fixed_line, route_mods)
        route_fixed_pair_ok &= (
            q_num128(paired, route_parts, route_S, route_D, route_gram)
            == q_numerator
        )
    cross_checks = {
        "both_sides_pass": address["status"] == route["status"] == "PASS",
        "route_hull_pass": route_hull["status"] == "PASS",
        "address_route_p2_exponents_17_11": (
            address["lattice"]["p2_order_exponent"] == 17
            and route["lattice"]["p2_order_exponent"] == 11
        ),
        "address_route_H1_dimensions_3_1": (
            address["cohomology"]["H1_dimension"] == 3
            and route["cohomology"]["H1_dimension"] == 1
        ),
        "both_have_q_preserving_fixed_rail": (
            address["fixed_order8_rail"]["q_preserving_shift_count"] == 256
            and route["fixed_order8_rail"]["q_preserving_shift_count"] == 16
        ),
        "scalar5_class_is_not_absolute_obstruction": (
            address["cohomology"]["scalar1_is_coboundary"]
            and route["cohomology"]["scalar1_is_coboundary"]
            and not address["cohomology"]["scalar5_is_coboundary"]
            and not route["cohomology"]["scalar5_is_coboundary"]
        ),
        "route_discriminant_torsion_plus_quotient": (
            route_torsion_q == Counter({0: 272, 64: 240})
            and route_fixed_pair_ok
        ),
    }
    all_pass = all(cross_checks.values())
    payload = {
        "schema": "w33.pass174.dual_discriminant_fixed_rail.v1",
        "status": "PASS" if all_pass else "FAIL",
        "address": address,
        "route": route,
        "route_hull_e8_shadow": route_hull,
        "route_discriminant_torsion": {
            "q_numerator_over_64_counts": {
                str(key): value for key, value in sorted(route_torsion_q.items())
            },
            "fixed_radical": "<4h>",
            "quotient_counts": {"isotropic": 136, "anisotropic": 120},
        },
        "cross_checks": cross_checks,
        "corrected_theorem": (
            "Both 2-primary dark discriminant modules admit an outer-fixed "
            "order-eight generator preserving q=11/8. The nonzero class "
            "[tau(h)-5h]=[4h] obstructs only the pure scalar-5 normal "
            "form, not a fixed rail. Address and route remain distinct by "
            "module types (Z2^14+Z8 versus Z2^8+Z8), H1 dimensions 3 "
            "versus 1, and fixed-shift counts 512 versus 32. The route "
            "code hull H=[40,9,16] has a canonical plus-type quotient "
            "H/<1> of dimension 8 whose 255 nonzero vectors reproduce "
            "the full 135+120 E8/2E8 quadratic split and Pass-124 graphs."
        ),
        "honesty_boundary": (
            "This is a finite discriminant-module and cohomology theorem. "
            "It does not by itself construct a continuum gauge field or "
            "physical transport channel."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    count = (
        sum(address["checks"].values())
        + sum(route["checks"].values())
        + sum(route_hull["checks"].values())
        + sum(cross_checks.values())
    )
    total = (
        len(address["checks"])
        + len(route["checks"])
        + len(route_hull["checks"])
        + len(cross_checks)
    )
    print(f"Pass 174: {'PASS' if all_pass else 'FAIL'} ({count}/{total})")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
