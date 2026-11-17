"""Test cyclic R rephasings, geometric rotations, and spin inflow for the E6 vacuum."""

import json
from itertools import product

import sympy as sp

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_monomials, hypercharge_integer_weights,
)
from toe_20261117_E6_fixed_point_R_anomaly import (
    anomaly_matrices, covering_nonabelian_levels, local_invariant_decomposition,
    adjoint_roots,
)
from toe_20261117_E6_two_corner_vacuum import corner_system
from toe_20261117_E6_two_protected_corners import multiply, torus_generator_basis


def charge_solutions():
    # Norm constraints set each barred frame charge to the opposite of
    # its partner. The triplet and weak mass terms then force K,L to
    # carry A's charge and imply 2(B-A)=0, with the analogous dual charges.
    solutions = []
    for a, b, x in product(range(4), repeat=3):
        if ((2*(b-a)) % 4 == 0 and (2*x+a-2) % 4 == 0
                and (2*x-2*a-2) % 4 == 0):
            charges = {"A": a, "Abar": -a % 4, "B": b, "Bbar": -b % 4,
                       "K": a, "Kbar": -a % 4, "L": a, "Lbar": -a % 4,
                       "X": x, "s": 0, "t": 0}
            assert (4*x-a) % 4 != 2  # The known contact contains Abar.
            solutions.append(charges)
    assert {(v["A"], v["B"], v["X"]) for v in solutions} == {
        (0, 0, 1), (0, 0, 3), (0, 2, 1), (0, 2, 3),
    }
    return solutions


def charge_identity():
    a, x, theta = sp.symbols("a x theta")
    mass_yukawa = 2*x+a-2*theta
    effective_down_yukawa = 2*x-2*a-2*theta
    contact_difference = 4*x-a-2*theta
    assert sp.expand(contact_difference-mass_yukawa-effective_down_yukawa) == 2*theta
    return {"contact_charge_minus_superpotential_charge_for_allowed_yukawas": "2*theta"}


def smallest_orthogonal_flux(cubic, corners):
    charges, norm, local, total, _ = anomaly_matrices(cubic, corners)
    inverse_norm = norm.inv()
    coroots = [inverse_norm*sp.Matrix(root) for root in adjoint_roots(cubic, charges, corners)]
    assert all(e.is_Integer for root in coroots for e in root)
    assert all((root.T*norm*root)[0] == 2 for root in coroots)
    for v, w in product(coroots, repeat=2):
        exponent = (v.T*total*w)[0]
        if (v.T*norm*w)[0] == 0 and abs(exponent) == 2:
            return (
                {"first_cocharacter": list(map(int, charges*v)),
                 "second_cocharacter": list(map(int, charges*w)),
                 "both_cocharacters_are_E6_coroots": True,
                 "inherited_E6_instanton_number": 0,
                 "integer_exponent_for_unit_superspace_charge": int(exponent),
                 "local_integer_exponents": [int((v.T*m*w)[0]) for m in local]},
                charges, norm, local,
            )
    raise AssertionError("No orthogonal unit-coroot pair with mixed index two")


def geometric_test(cubic, corners):
    p, px, py, _ = corners
    ux, uy = multiply(p, px), multiply(p, py)
    fixed_dims = [torus_generator_basis(cubic, (q,), 1)[0].rows
                  for q in (ux, uy, multiply(ux, uy))]
    corner_dims = [torus_generator_basis(cubic, (q,), 1)[0].rows for q in corners]
    assert fixed_dims == [46, 38, 46] and corner_dims == [38, 38, 46, 38]
    axes = [(1, 0), (0, 1), (1, 1)]
    dims = dict(zip(axes, fixed_dims, strict=True))
    intrinsic = {(1, -1): 6, (-1, 1): 2}
    gauge_compatible = []
    all_compatible = []
    for image_x, image_y in product(axes, repeat=2):
        if image_x == image_y:
            continue
        image_xy = tuple((a+b) % 2 for a, b in zip(image_x, image_y, strict=True))
        if any(dims[src] != dims[dst]
               for src, dst in zip(axes, (image_x, image_y, image_xy), strict=True)):
            continue
        gauge_compatible.append((image_x, image_y))
        transformed = {}
        for (s, t), count in intrinsic.items():
            x, y = (s**a*t**b for a, b in (image_x, image_y))
            transformed[x, y] = count
        if transformed == intrinsic:
            all_compatible.append((image_x, image_y))
    assert gauge_compatible == [((1, 0), (0, 1)), ((1, 1), (0, 1))]
    assert all_compatible == [((1, 0), (0, 1))]
    return {"nontrivial_translation_fixed_algebra_dimensions_x_y_xy": fixed_dims,
            "corner_fixed_algebra_dimensions": corner_dims,
            "translation_actions_compatible_with_gauge_dims": gauge_compatible,
            "translation_actions_also_compatible_with_charged_hypers": all_compatible,
            "nontrivial_half_translation_allowed": corner_dims.count(46) != 1}


def spin_axion_classes(corners, charges, norm, local):
    rows, classes = local_invariant_decomposition(
        corners, charges, norm, local, covering_nonabelian_levels()
    )
    result = []
    for f, (row, characteristic) in enumerate(zip(rows, classes, strict=True)):
        assert row["inherited_E6_coefficient"] % 2 == 0
        a = row["inherited_E6_coefficient"]//2
        if f == 2:
            b = row["quotient_character_square_coefficient"]//2
            divisor = 1
        else:
            b = row["four_times_SU2_instanton_coefficient"]
            divisor = 2
        assert all((value/divisor).is_Integer for value in characteristic)
        assert local[f]/2 == a*norm + b*characteristic/divisor
        result.append({"J_coefficient": a, "local_spin_class_coefficient": b,
                       "local_characteristic_class_divisor": divisor})
    # A holomorphic unit harmonic has R charge zero, two, or one under
    # the three respective shifts. The contact has charge zero.
    first_harmonics = {step: next(n for n in range(1, 5) if n*step % 4 == 2)
                       for step in (1, 2, 3)}
    assert first_harmonics == {1: 2, 2: 1, 3: 2}
    return {"coefficients_for_axion_shift_pi": result,
            "first_holomorphic_harmonic_by_shift_in_pi_over_2_units": first_harmonics}


def certificate():
    cubic = cubic_monomials()
    corners = corner_system(hypercharge_integer_weights(), cubic)
    witness, charges, norm, local = smallest_orthogonal_flux(cubic, corners)
    return {"allowed_diagonal_Z4R_charges": charge_solutions(),
            "all_cyclic_charge_identity": charge_identity(),
            "orthogonal_flux_for_cyclic_R": witness,
            "geometric_rotation_controls": geometric_test(cubic, corners),
            "integral_spin_inflow": spin_axion_classes(corners, charges, norm, local)}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
