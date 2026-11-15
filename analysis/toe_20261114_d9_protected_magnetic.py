"""Exact checks of the analytic magnetic potentials preserving D9 static shape."""

import json
from pathlib import Path

import sympy as sp


def verify():
    x, y, scale, k = sp.symbols("X Y scale k", positive=True)
    delta, gamma, born = sp.symbols("delta gamma s", real=True)
    total = x + y
    asymmetry = (x - y) / total
    invariant = total**3 * x * y

    def force_residual(polynomial, degree):
        shape = x * sp.diff(polynomial, x) - y * sp.diff(polynomial, y)
        return sp.expand(total * shape - sp.Rational(1, 5) * (3 * degree + 2) * (x - y) * polynomial)

    dimensions = {}
    for degree in range(1, 19):
        basis = [x**i * y**(degree-i) for i in range(degree+1)]
        columns = [sp.Poly(force_residual(monomial, degree), x, y) for monomial in basis]
        matrix = sp.Matrix([
            [column.coeff_monomial(x**i * y**(degree+1-i)) for column in columns]
            for i in range(degree+2)
        ])
        kernel = matrix.nullspace()
        assert len(kernel) == int((degree-1) % 5 == 0)
        dimensions[degree] = len(kernel)
        if kernel:
            generator = total * invariant**((degree-1)//5)
            assert force_residual(generator, degree) == 0

    # The first allowed term is gamma*(X+Y)^4*X*Y. At v=0 the
    # curvature, Maxwell and correction forces all have v/u ratio 3*delta/7.
    flux_at_v_zero = {x: (sp.Rational(7, 5)+delta)*scale**2,
                      y: (sp.Rational(7, 5)-delta)*scale**2}
    correction = gamma * total * invariant
    corrected_volume_force = (
        sp.Rational(28, 3)*k*scale**sp.Rational(7, 3)
        - sp.Rational(20, 3)*scale**sp.Rational(4, 3)*(total/2).subs(flux_at_v_zero)
        - sp.Rational(80, 3)*scale**sp.Rational(4, 3)*correction.subs(flux_at_v_zero)
    )
    base_correction = correction.subs({x: sp.Rational(7, 5)+delta, y: sp.Rational(7, 5)-delta})
    expected = k - scale - sp.Rational(20, 7)*base_correction*scale**11
    assert sp.simplify(corrected_volume_force/(sp.Rational(28, 3)*scale**sp.Rational(7, 3))-expected) == 0

    born_inf = (sp.sqrt((1 + born*x)*(1 + born*y)) - 1)/born
    first_born_term = sp.expand(sp.series(born_inf, born, 0, 2).removeO().coeff(born))
    assert sp.expand(first_born_term + (x-y)**2/8) == 0
    born_shape_slope_per_n = 4*delta*(245-100*delta**2)/(120*(21-5*delta**2))
    assert sp.factor(born_shape_slope_per_n.subs(delta, sp.Rational(3, 5))) == sp.Rational(209, 960)
    assert sp.simplify(asymmetry**2 + 4*x*y/total**2 - 1) == 0

    return {
        "protected_magnetic_energy": "(X+Y) * f((X+Y)^3 * X * Y), f(0)=1/2",
        "polynomial_kernel_dimensions": dimensions,
        "first_nonlinear_generator": str(total*invariant),
        "first_nonlinear_power_of_field_strength": 12,
        "first_nonlinear_sourced_scale_equation": str(expected),
        "born_infeld_linear_source_slope_per_angular_eigenvalue_and_coupling": str(born_shape_slope_per_n),
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_d9_protected_magnetic.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
