#!/usr/bin/env python3
"""Exact 1296 extended-qutrit Clifford = W33 full point-stabilizer theorem.

This closes the central-lift boundary left open by the affine spinor-parity
certificate.  It works on the *point side* of W(3,3), not the nonconjugate
line-side 1296 carrier.

Starting from the native F3^4 W33 model:
  * PSp(4,3) has order 25920;
  * adjoining the explicit multiplier-2 similitude
        D = diag(2,1,2,1)
    gives PGSp(4,3) of order 51840;
  * the point stabilizers have orders 648 and 1296.

Inside the even 648 stabilizer we reconstruct the certified normal extraspecial
Heisenberg H27 and an SL(2,3) complement.  In the full 1296 stabilizer we find
an explicit GL(2,3) complement.  Every element has a unique H27.GL2 normal
form.  Conjugation on H27/Z(H27) is the complete GL(2,3), and conjugation on
Z(H27)=C3 is multiplication by det(g).

Consequences:
  G_ext ~= 3_+^{1+2} : GL(2,3), order 1296,
  G_even ~= 3_+^{1+2} : SL(2,3), order 648,
  G_ext / C3 ~= AGL(2,3), order 432,
  G_even / C3 ~= ASL(2,3), order 216,
and the determinant/spinor-parity character on the quotient lifts to G_ext
with kernel exactly G_even.

Important semantic correction: the C3 that is central in the 648 Clifford
group is only a normal phase subgroup in the 1296 anti-linear extension;
determinant-minus-one elements invert it and the full 1296 group has trivial
center.
"""
from __future__ import annotations

import itertools
import importlib.util
import json
from pathlib import Path

import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup

from w33_pass1054_1059_core import (
    J, Q, build_w33_bundle, normalize, permutation_images
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_extended_clifford1296_point_stabilizer.json"
SPIN = ROOT / "data/w33_hesse_nullcone_spinor_norm.json"
AFFINE = ROOT / "data/w33_hesse_affine_spinor_parity.json"


def sorted_elements(group: PermutationGroup, degree: int = 40):
    return sorted(
        group.generate_schreier_sims(),
        key=lambda element: tuple(permutation_images(element, degree)),
    )


def commutator(left: Permutation, right: Permutation) -> Permutation:
    return left**-1 * right**-1 * left * right


def det2(matrix: tuple[int, int, int, int]) -> int:
    a, b, c, d = matrix
    return (a * d - b * c) % 3


def explicit_agl9() -> set[tuple[int, ...]]:
    points = list(itertools.product(range(3), repeat=2))
    index = {point: i for i, point in enumerate(points)}
    matrices = []
    for entries in itertools.product(range(3), repeat=4):
        if det2(entries):
            matrices.append(entries)
    out = set()
    for t in points:
        for a, b, c, d in matrices:
            image = []
            for u, v in points:
                w = ((a * u + b * v + t[0]) % 3, (c * u + d * v + t[1]) % 3)
                image.append(index[w])
            out.add(tuple(image))
    assert len(out) == 432
    return out


def main(write=True):
    bundle = build_w33_bundle()
    even_ambient = bundle.group
    even = bundle.point_stabilizer
    assert even_ambient.order() == 25920
    assert even.order() == 648

    # Explicit symplectic similitude with multiplier -1 = 2 mod 3.
    D = np.diag([2, 1, 2, 1]).astype(int) % 3
    assert np.array_equal((D.T @ J @ D) % 3, (2 * J) % 3)
    point_index = {point: index for index, point in enumerate(bundle.points)}
    outer = Permutation([
        point_index[normalize((D @ np.array(point, dtype=int)) % Q)]
        for point in bundle.points
    ])
    assert outer.order() == 2 and outer(0) == 0

    full_ambient = PermutationGroup(list(bundle.point_generators) + [outer])
    full = full_ambient.stabilizer(0)
    assert full_ambient.order() == 51840
    assert full.order() == 1296
    assert even.is_normal(full)
    assert full.center().order() == 1

    even_elements = sorted_elements(even)
    center_even = even.center()
    center_set = set(center_even.generate_schreier_sims())
    assert center_even.order() == 3

    # Reconstruct the unique extraspecial normal H27 used by Pass 1054.
    normal_27 = None
    for element in even_elements:
        if element.is_identity or element in center_set or element.order() != 3:
            continue
        candidate = even.normal_closure(PermutationGroup([element]))
        if candidate.order() == 27:
            normal_27 = candidate
            break
    assert normal_27 is not None
    assert normal_27.order() == 27
    assert not normal_27.is_abelian
    assert normal_27.center().order() == 3
    assert normal_27.derived_subgroup().order() == 3
    assert normal_27.is_normal(full)

    normal_elements = sorted_elements(normal_27)
    normal_set = set(normal_elements)

    # Heisenberg coordinates x^a y^b z^c.
    heisenberg = None
    for x in normal_elements:
        if x.is_identity or x in center_set:
            continue
        for y in normal_elements:
            if y.is_identity or y in center_set:
                continue
            z = commutator(x, y)
            if (not z.is_identity and z in center_set
                    and PermutationGroup([x, y]).order() == 27):
                heisenberg = (x, y, z)
                break
        if heisenberg is not None:
            break
    assert heisenberg is not None
    x, y, z = heisenberg

    coordinate_of = {}
    ordered_normal = [None] * 27
    for a, b, c in itertools.product(range(3), repeat=3):
        element = x**a * y**b * z**c
        assert element not in coordinate_of
        coordinate_of[element] = (a, b, c)
        ordered_normal[9 * a + 3 * b + c] = element
    assert all(element is not None for element in ordered_normal)
    normal_index = {element: i for i, element in enumerate(ordered_normal)}

    # Recover the SL2(3) complement in the even subgroup.
    sylow_two = even.sylow_subgroup(2)
    complement_24 = None
    for element in even_elements:
        if element.order() != 3 or element in normal_set:
            continue
        candidate = PermutationGroup(list(sylow_two.generators) + [element])
        if candidate.order() == 24 and len(set(candidate.generate_schreier_sims()) & normal_set) == 1:
            complement_24 = candidate
            break
    assert complement_24 is not None

    # Correct the outer similitude by one H27 element to obtain a disjoint
    # GL2(3) complement rather than generating the whole parabolic at once.
    complement_48 = None
    outer_lift = None
    for normal in normal_elements:
        candidate_outer = normal * outer
        candidate = PermutationGroup(list(complement_24.generators) + [candidate_outer])
        if candidate.order() != 48:
            continue
        if len(set(candidate.generate_schreier_sims()) & normal_set) == 1:
            complement_48 = candidate
            outer_lift = candidate_outer
            break
    assert complement_48 is not None and outer_lift is not None
    assert complement_48.center().order() == 2
    assert complement_48.derived_subgroup().order() == 24

    complement_elements = sorted_elements(complement_48)

    # Unique H27 . GL2(3) decomposition of the complete point stabilizer.
    decomposition = {}
    for normal in normal_elements:
        for linear in complement_elements:
            element = normal * linear
            assert element not in decomposition
            decomposition[element] = (normal, linear)
    full_elements = sorted_elements(full)
    assert len(decomposition) == 1296
    assert set(decomposition) == set(full_elements)

    # Conjugation matrices on H27/Z and central action.
    matrix_of = {}
    central_action = {}
    central_offsets = set()
    for linear in complement_elements:
        cx = coordinate_of[linear * x * linear**-1]
        cy = coordinate_of[linear * y * linear**-1]
        cz = coordinate_of[linear * z * linear**-1]
        matrix = (cx[0], cy[0], cx[1], cy[1])
        matrix_of[linear] = matrix
        central_offsets.add((cx[2], cy[2]))
        central_action[linear] = cz
        assert det2(matrix) in (1, 2)
        assert cz == (0, 0, det2(matrix))

    all_gl2 = {
        entries for entries in itertools.product(range(3), repeat=4)
        if det2(entries)
    }
    assert set(matrix_of.values()) == all_gl2
    assert len(matrix_of) == 48
    assert sum(det2(matrix) == 1 for matrix in matrix_of.values()) == 24
    assert sum(det2(matrix) == 2 for matrix in matrix_of.values()) == 24

    # The old central C3 is normal, but anti-linear/det=-1 elements invert it.
    assert all(
        linear * z * linear**-1 == (z if det2(matrix_of[linear]) == 1 else z**2)
        for linear in complement_elements
    )

    # Faithful degree-27 extended Clifford action on the Heisenberg carrier.
    def affine27(element):
        normal, linear = decomposition[element]
        return Permutation([
            normal_index[normal * linear * state * linear**-1]
            for state in ordered_normal
        ])

    affine27_images = {element: affine27(element) for element in full_elements}
    affine27_group = PermutationGroup([affine27_images[g] for g in full.generators])
    assert len(set(affine27_images.values())) == 1296
    assert affine27_group.order() == 1296

    # Quotient by the phase C3: exact AGL(2,3) action on 9 phase-space points.
    phase_points = list(itertools.product(range(3), repeat=2))
    phase_index = {point: i for i, point in enumerate(phase_points)}
    representative = {
        (a, b): ordered_normal[9 * a + 3 * b]
        for a, b in phase_points
    }

    def quotient9(element):
        normal, linear = decomposition[element]
        image = []
        for point in phase_points:
            moved = normal * linear * representative[point] * linear**-1
            a, b, _ = coordinate_of[moved]
            image.append(phase_index[(a, b)])
        return Permutation(image)

    quotient_images = {element: quotient9(element) for element in full_elements}
    quotient_group = PermutationGroup([quotient_images[g] for g in full.generators])
    identity9 = Permutation(list(range(9)))
    quotient_kernel = {element for element, image in quotient_images.items() if image == identity9}
    quotient_tuples = {
        tuple(int(image(i)) for i in range(9))
        for image in quotient_images.values()
    }
    assert quotient_group.order() == 432
    assert len(quotient_tuples) == 432
    assert quotient_kernel == center_set
    assert quotient_tuples == explicit_agl9()

    # Lift the determinant/spinor character to all 1296 elements.
    character = {
        element: det2(matrix_of[linear])
        for element, (_, linear) in decomposition.items()
    }
    even_set = set(even.generate_schreier_sims())
    assert sum(value == 1 for value in character.values()) == 648
    assert sum(value == 2 for value in character.values()) == 648
    assert {element for element, value in character.items() if value == 1} == even_set

    spin = json.loads(SPIN.read_text())
    affine = json.loads(AFFINE.read_text())
    assert spin["character_weld"]["identity"].startswith("spinor_norm(rho(g)) = det(g)")
    assert affine["character"]["kernel"] == "ASL(2,3)=F3^2:SL(2,3)"

    checks = {
        "PSp43_order25920": True,
        "PGSp43_order51840": True,
        "outer_is_multiplier2_similitude": True,
        "even_point_stabilizer_order648": True,
        "full_point_stabilizer_order1296": True,
        "full_point_stabilizer_center_trivial": True,
        "normal_extraspecial_H27": True,
        "SL23_complement_order24": True,
        "GL23_complement_order48": True,
        "unique_H27_GL23_normal_form_all1296": True,
        "linear_action_is_all_GL23": True,
        "center_action_equals_determinant": True,
        "old_C3_normal_but_not_central_in_full_extension": True,
        "faithful_degree27_extended_Clifford_action": True,
        "phase_quotient_kernel_exactly_C3": True,
        "phase_quotient_is_exact_AGL23_order432": True,
        "determinant_character_balanced648_648": True,
        "determinant_character_kernel_exactly_even_Clifford648": True,
        "spinor_parity_lifts_through_phase_extension": True,
        "point_side_not_line_side": True,
    }
    assert all(checks.values())

    out = {
        "schema": "w33.extended_clifford1296_point_stabilizer.v1",
        "status": "PASS_FULL_W33_POINT_STABILIZER_IS_EXTENDED_QUTRIT_CLIFFORD_3PLUS12_GL23",
        "headline": (
            "The full PGSp(4,3) stabilizer of a W33 point is explicitly "
            "3_+^{1+2}:GL(2,3), order 1296. Its even PSp subgroup is the certified "
            "qutrit Clifford 3_+^{1+2}:SL(2,3), order 648. Quotienting the normal "
            "phase C3 gives AGL(2,3) and ASL(2,3), while determinant/spinor parity "
            "lifts to the 1296 group with kernel exactly the 648 subgroup."
        ),
        "ambient": {
            "PSp43_order": 25920,
            "PGSp43_order": 51840,
            "outer_similitude_matrix": D.tolist(),
            "similitude_multiplier": 2,
        },
        "point_stabilizers": {
            "even_order": 648,
            "even_structure": "3_+^{1+2}:SL(2,3)",
            "full_order": 1296,
            "full_structure": "3_+^{1+2}:GL(2,3)",
            "full_center_order": 1,
            "heisenberg_order": 27,
            "heisenberg_center_order": 3,
            "SL23_complement_order": 24,
            "GL23_complement_order": 48,
            "GL23_complement_center_order": 2,
            "GL23_complement_derived_order": 24,
        },
        "phase_center_semantics": {
            "C3_central_in_even_648": True,
            "C3_normal_in_full_1296": True,
            "C3_central_in_full_1296": False,
            "det_plus_one_action": "z -> z",
            "det_minus_one_action": "z -> z^2",
            "correction": (
                "The phrase 'extended with C3 center' is only a counting shorthand. "
                "After anti-linear completion the phase C3 is normal but not central."
            ),
        },
        "quotients": {
            "even_mod_C3": "ASL(2,3)",
            "even_mod_C3_order": 216,
            "full_mod_C3": "AGL(2,3)",
            "full_mod_C3_order": 432,
            "full_quotient_degree": 9,
            "quotient_action_equals_explicit_AGL9": True,
        },
        "linear_action": {
            "distinct_GL23_matrices": 48,
            "det_plus_one": 24,
            "det_minus_one": 24,
            "central_offset_pairs": len(central_offsets),
            "center_exponent_equals_determinant": True,
        },
        "spinor_parity_lift": {
            "character": "chi(n,g)=det(g)=spinor_norm(rho(g))",
            "trivial_class_size": 648,
            "nontrivial_class_size": 648,
            "kernel": "even qutrit Clifford 3_+^{1+2}:SL(2,3)",
            "translation_phase_extension_does_not_destroy_character": True,
        },
        "side_selection": {
            "selected": "W(3,3) point stabilizer / extraspecial 3_+^{1+2} side",
            "excluded": "W(3,3) line stabilizer / elementary-abelian 3^3 side",
            "reason": "the physical qutrit Clifford certificate already selects the extraspecial Heisenberg point side",
        },
        "boundary": (
            "This closes the finite 648->1296 extended-Clifford group identification. "
            "The spinor-parity bit remains a finite group character; no physical CPT, "
            "spacetime parity, Lorentz Pin/Spin structure, or continuum dynamics is inferred."
        ),
        "parents": [
            "analysis/w33_pass1054_hessian_affine_isomorphism.py",
            "data/w33_hesse_affine_spinor_parity.json",
            "data/w33_hesse_nullcone_spinor_norm.json",
        ],
        "check_count": len(checks),
        "checks": checks,
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
