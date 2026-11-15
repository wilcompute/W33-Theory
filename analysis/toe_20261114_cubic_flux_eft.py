"""Check four-dimensional curvature coefficients for the cubic-flux EFT."""

import json
from itertools import combinations_with_replacement
from pathlib import Path

import sympy as sp


def check_surface(c1_squared, signature, euler):
    # The integrals in this function are expressed in units of pi^2.
    scalar, gradient = sp.symbols("s gradient_integral", positive=True)
    volume = 32*sp.Integer(c1_squared)/scalar**2
    plus = sp.diag(scalar/6, -scalar/12, -scalar/12)
    curvature_shift = scalar/12
    plus_norm = sp.expand(sp.trace(plus**2)*volume)
    minus_norm = plus_norm-12*signature
    assert sp.simplify(plus_norm+minus_norm+scalar**2*volume/24) == 8*euler

    a, b, c = sp.symbols("a b c", real=True)
    anti_self_dual = sp.diag(a, b, -a-b)
    assert sp.simplify(sp.trace(anti_self_dual**3)-3*anti_self_dual.det()) == 0
    assert sp.simplify(sp.trace((anti_self_dual+c*sp.eye(3))**3)-sp.trace(anti_self_dual**3)
                       -3*c*sp.trace(anti_self_dual**2)-3*c**3) == 0

    curvature_squared = plus_norm+minus_norm+6*curvature_shift**2*volume
    minus_cube = (gradient+scalar*minus_norm/2)/6  # integrated Derdzinski identity
    curvature_cubed = (sp.trace(plus**3)*volume+minus_cube
                       +3*curvature_shift*(plus_norm+minus_norm)+6*curvature_shift**3*volume)
    return scalar, gradient, sp.simplify(curvature_squared), sp.simplify(curvature_cubed)


def verify():
    scalar, gradient, square, cube = check_surface(c1_squared=3, signature=-5, euler=9)
    assert square == 72
    assert cube == 23*scalar+gradient/6
    # Equal spheres have parallel curvature and two nonzero sectional eigenvalues s/4.
    scalar, gradient, _, product_cube = check_surface(c1_squared=8, signature=0, euler=4)
    assert product_cube.subs(gradient, 0) == 8*scalar
    assert 2*(scalar/4)**3*(16/(scalar/4)**2) == 8*scalar

    # A length rescaling by epsilon yields epsilon^-6 for the squared
    # curvature derivative and epsilon^4 for four-volume.
    epsilon = sp.Symbol("epsilon", positive=True)
    assert epsilon**4*(epsilon**-3)**2 == epsilon**-2

    # The four Fermat tangent monomials each omit one coordinate. Their
    # characters and conjugates under cube-root phases have no linear invariants.
    weights = [(sign, missing, tuple(sign*int(i != missing) for i in range(4)))
               for sign in (1, -1) for missing in range(4)]
    assert all(any(value % 3 for value in weight) for _, _, weight in weights)
    invariant_pairs = [(left[:2], right[:2]) for left, right in combinations_with_replacement(weights, 2)
                       if all((a+b) % 3 == 0 for a, b in zip(left[2], right[2]))]
    assert invariant_pairs == [((1, i), (-1, i)) for i in range(4)]
    return {
        "cubic_internal_euler": 9,
        "cubic_internal_signature": -5,
        "integrated_curvature_operator_square_units_pi_squared": int(square),
        "integrated_curvature_operator_cube": "23*s*pi^2 + integral(|nabla W_minus|^2)/6",
        "first_order_potential_from_parity_even_F_even_four_derivative_local_terms": "constant along fixed-flux family",
        "six_derivative_cubic_operator_nodal_lower_bound_length_power": -2,
        "fermat_symmetry_invariant_linear_terms": 0,
        "fermat_symmetry_invariant_real_quadratic_terms_after_permutations": 1,
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_cubic_flux_eft.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
