#!/usr/bin/env python3
"""Pass 1054: explicit Hessian normal form for the selected order-648 stabilizer.

The Pass-1047 point stabilizer is converted, generator by generator, into a
faithful degree-27 affine action on its normal Heisenberg group. This gives an
explicit permutation-level isomorphism H_point ~= 3^(1+2)_+ : SL(2,3).
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

from w33_pass1054_1059_core import build_w33_bundle, cycle_partition, permutation_images


def sorted_elements(group: PermutationGroup, degree: int = 40) -> list[Permutation]:
    return sorted(group.generate_schreier_sims(), key=lambda element: tuple(permutation_images(element, degree)))


def commutator(left: Permutation, right: Permutation) -> Permutation:
    return left**-1 * right**-1 * left * right


def main() -> dict[str, object]:
    bundle = build_w33_bundle()
    stabilizer = bundle.point_stabilizer
    elements = sorted_elements(stabilizer)
    center = stabilizer.center()
    center_elements = set(center.generate_schreier_sims())

    normal_27 = None
    for element in elements:
        if element.is_identity or element in center_elements or element.order() != 3:
            continue
        candidate = stabilizer.normal_closure(PermutationGroup([element]))
        if candidate.order() == 27:
            normal_27 = candidate
            break
    if normal_27 is None:
        raise AssertionError("normal extraspecial subgroup of order 27 not found")

    normal_elements = sorted_elements(normal_27)
    normal_set = set(normal_elements)
    heisenberg_generators = None
    for x in normal_elements:
        if x.is_identity or x in center_elements:
            continue
        for y in normal_elements:
            if y.is_identity or y in center_elements:
                continue
            z = commutator(x, y)
            if not z.is_identity and z in center_elements and PermutationGroup([x, y]).order() == 27:
                heisenberg_generators = (x, y, z)
                break
        if heisenberg_generators is not None:
            break
    if heisenberg_generators is None:
        raise AssertionError("Heisenberg generators were not found")
    x, y, z = heisenberg_generators

    coordinate_of: dict[Permutation, tuple[int, int, int]] = {}
    element_at: list[Permutation | None] = [None] * 27
    for a, b, c in itertools.product(range(3), repeat=3):
        element = x**a * y**b * z**c
        coordinate = (a, b, c)
        if element in coordinate_of:
            raise AssertionError("Heisenberg normal form is not unique")
        coordinate_of[element] = coordinate
        element_at[9 * a + 3 * b + c] = element
    if any(element is None for element in element_at):
        raise AssertionError("Heisenberg coordinate table is incomplete")
    ordered_normal = [element for element in element_at if element is not None]
    normal_index = {element: index for index, element in enumerate(ordered_normal)}

    sylow_two = stabilizer.sylow_subgroup(2)
    complement = None
    for element in elements:
        if element.order() != 3 or element in normal_set:
            continue
        candidate = PermutationGroup(list(sylow_two.generators) + [element])
        if candidate.order() != 24:
            continue
        if len(set(candidate.generate_schreier_sims()) & normal_set) == 1:
            complement = candidate
            break
    if complement is None:
        raise AssertionError("split SL(2,3) complement was not found")
    complement_elements = sorted_elements(complement)

    decomposition: dict[Permutation, tuple[Permutation, Permutation]] = {}
    for normal in normal_elements:
        for linear in complement_elements:
            element = normal * linear
            if element in decomposition:
                raise AssertionError("N.L decomposition is not unique")
            decomposition[element] = (normal, linear)
    if len(decomposition) != 648:
        raise AssertionError("N.L decomposition misses stabilizer elements")

    def affine_image(element: Permutation) -> Permutation:
        normal, linear = decomposition[element]
        return Permutation([normal_index[normal * linear * state * linear**-1] for state in ordered_normal])

    affine_images = {element: affine_image(element) for element in elements}
    affine_group = PermutationGroup([affine_images[generator] for generator in stabilizer.generators])

    matrix_image: dict[tuple[int, int, int, int], int] = {}
    central_offsets: set[tuple[int, int]] = set()
    for linear in complement_elements:
        conjugated_x = coordinate_of[linear * x * linear**-1]
        conjugated_y = coordinate_of[linear * y * linear**-1]
        matrix = (conjugated_x[0], conjugated_y[0], conjugated_x[1], conjugated_y[1])
        determinant = (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % 3
        if determinant != 1:
            raise AssertionError("complement action does not lie in SL(2,3)")
        matrix_image[matrix] = matrix_image.get(matrix, 0) + 1
        central_offsets.add((conjugated_x[2], conjugated_y[2]))

    checks = {
        "ambient_PSp43_order_25920": bundle.group.order() == 25920,
        "selected_stabilizer_order_648": stabilizer.order() == 648,
        "normal_subgroup_order_27": normal_27.order() == 27,
        "normal_subgroup_is_extraspecial": not normal_27.is_abelian and normal_27.center().order() == 3 and normal_27.derived_subgroup().order() == 3,
        "heisenberg_coordinates_are_bijective": len(coordinate_of) == 27,
        "commutator_is_central_C3": z.order() == 3 and z in center_elements and center.order() == 3,
        "complement_is_SL23_order_24": complement.order() == 24,
        "complement_meets_Heisenberg_trivially": len(set(complement_elements) & normal_set) == 1,
        "split_product_has_order_648": PermutationGroup(list(normal_27.generators) + list(complement.generators)).order() == 648,
        "linear_image_is_all_SL23": len(matrix_image) == 24,
        "all_linear_determinants_are_one": all((a * d - b * c) % 3 == 1 for a, b, c, d in matrix_image),
        "affine_image_is_faithful": len(set(affine_images.values())) == 648,
        "affine_image_group_order_648": affine_group.order() == 648,
        "affine_center_and_derived_match_G25": affine_group.center().order() == 3 and affine_group.derived_subgroup().order() == 216,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])

    generating_images = []
    for generator in list(normal_27.generators) + list(complement.generators):
        generating_images.append({
            "source_cycle_partition_on_40": list(cycle_partition(generator, 40)),
            "affine_images_on_27": permutation_images(affine_images[generator], 27),
            "order": int(generator.order()),
            "role": "Heisenberg" if generator in normal_set else "SL(2,3) complement",
        })

    return {
        "schema": "w33.pass1054.hessian_affine_isomorphism.v1",
        "status": "PASS",
        "headline": "The selected W(3,3) point stabilizer is explicitly represented as the faithful degree-27 affine Hessian group 3^(1+2)_+:SL(2,3). A normal extraspecial Heisenberg 27 and a disjoint SL(2,3) complement of order 24 are constructed, every one of the 648 stabilizer elements has a unique N.L normal form, and the resulting affine image has order 648, center 3, and derived subgroup 216.",
        "orders": {"stabilizer": int(stabilizer.order()), "heisenberg": int(normal_27.order()), "complement": int(complement.order()), "affine_image": int(affine_group.order())},
        "heisenberg": {"coordinate_order": "x^a y^b z^c, a,b,c in F3", "commutator_convention": "z = x^-1 y^-1 x y", "center_order": int(normal_27.center().order()), "derived_order": int(normal_27.derived_subgroup().order())},
        "linear_quotient": {"distinct_SL2_3_matrices": len(matrix_image), "matrices_row_major": [list(matrix) for matrix in sorted(matrix_image)], "central_offset_pairs": [list(pair) for pair in sorted(central_offsets)]},
        "generator_correspondence": generating_images,
        "check_count": len(checks),
        "checks": checks,
        "scope": "This is an explicit permutation-level isomorphism to the Hessian normal form 3^(1+2)_+:SL(2,3), the abstract group underlying ST G25. It does not construct a complex 3x3 CHEVIE matrix conjugator.",
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1054_hessian_affine_isomorphism.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "headline", "orders", "check_count")}, indent=2))
