"""Verify static D9 shape response with two quartic magnetic invariants."""

import json
from pathlib import Path

import sympy as sp


def verify():
    u, v, delta, alpha, beta = sp.symbols("u v delta alpha beta", real=True)
    curvature_factor = sp.Symbol("k", positive=True)
    origin = {u: 0, v: 0}
    # Units with the unperturbed inverse squared radii summing to one.
    a, b = (1 + delta) / 2, (1 - delta) / 2
    x = (2 * a + sp.Rational(2, 5)) * sp.exp(-4 * (u + v))
    y = (2 * b + sp.Rational(2, 5)) * sp.exp(-4 * (u - v))
    weyl = sp.exp(-8 * u / 3)
    geometric = -2 * weyl * (a * sp.exp(-2 * (u + v)) + b * sp.exp(-2 * (u - v)))
    quadratic = weyl * (x + y) / 2
    quartic = weyl * (alpha * (x + y)**2 + beta * (x*x + y*y))
    potential = geometric + quadratic + quartic
    hessian = sp.hessian(geometric + quadratic, (u, v)).subs(origin)
    assert sp.Matrix([sp.diff(geometric + quadratic, w) for w in (u, v)]).subs(origin) == sp.zeros(2, 1)
    quartic_force = sp.Matrix([sp.diff(quartic, w) for w in (u, v)]).subs(origin)
    vacuum_shift = sp.factor(-(hessian.inv() * quartic_force)[1])
    expected = 4 * delta * (49 * alpha + (147 - 50 * delta**2) * beta) / (15 * (21 - 5 * delta**2))
    assert sp.simplify(vacuum_shift - expected) == 0

    # The equal-degree KK source multiplies curvature by k=1-J*n/2.
    # A common shift of the log radii returns the original curvature and
    # Maxwell terms up to k^(10/3), leaving k^2 times both quartic coefficients.
    sourced = curvature_factor * geometric + quadratic + quartic
    transformed = sourced.subs(u, u - sp.log(curvature_factor) / 2)
    rescaled = potential.subs({alpha: curvature_factor**2 * alpha, beta: curvature_factor**2 * beta})
    assert sp.simplify(transformed - curvature_factor**sp.Rational(10, 3) * rescaled) == 0

    j, n = sp.symbols("J n", real=True)
    source_response = sp.diff((1 - j*n/2)**2 * vacuum_shift, j).subs(j, 0)
    assert sp.simplify(source_response + n * expected) == 0
    assert source_response.subs(delta, 0) == 0
    assert sp.factor(source_response.subs({delta: sp.Rational(3, 5), beta: 0, n: 2})) == -sp.Rational(49, 60) * alpha
    return {
        "units": "unperturbed inverse squared radii sum to one",
        "vacuum_shape_shift_first_order": str(expected),
        "equal_degree_source_shape_derivative_first_order": str(sp.factor(source_response)),
        "exact_source_rescaling": "u=U-log(k)/2; (alpha,beta) -> k^2*(alpha,beta); k=1-J*n/2>0",
        "first_order_unequal_radius_cancellation": "49*alpha + (147-50*delta^2)*beta = 0",
        "control_delta_3_over_5_degree_one_alpha_only": "-49*alpha/60",
    }


if __name__ == "__main__":
    result = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_d9_quartic_flux.json"
    path.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
