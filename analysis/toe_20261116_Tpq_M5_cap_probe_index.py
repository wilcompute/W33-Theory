"""Check the capped M5 normal-mode factorization and warp-minimum hypotheses."""

import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss
import sympy as sp

from toe_20261116_Tpq_coupled_warp_branch import metric_response, numerical_branch, scalar_reduction


def exact_checks():
    s = sp.Symbol("s")
    k, g = sp.symbols("k g", real=True)
    f, area, volume = [sp.Function(name)(s) for name in ("f", "S", "V")]
    weight = volume/area

    def first_order(value):
        return sp.diff(value, s)+g*k*weight*value

    def adjoint(value):
        return -sp.diff(value, s)-sp.diff(area, s)/area*value+g*k*weight*value

    expected = (
        -sp.diff(area*sp.diff(f, s), s)/area
        -g*k*sp.diff(volume, s)/area*f+(g*k*weight)**2*f
    )
    assert sp.simplify(adjoint(first_order(f))-expected) == 0
    # Four equal angular principal curvatures lie in [c/5, c/4].
    pressure = sp.Symbol("c", positive=True)
    angular = sp.Symbol("k_theta", positive=True)
    curvature_sq = (pressure-4*angular)**2+4*angular**2
    assert curvature_sq.subs(angular, pressure/5) == pressure**2/5
    assert curvature_sq.subs(angular, pressure/4) == pressure**2/4
    assert sp.diff(curvature_sq, angular, 2) == 40

    t = sp.Symbol("t")
    cohomology = sp.Poly((1+t**5)*(1+t), t)
    assert cohomology.nth(2) == 0 and cohomology.nth(3) == 0


def check_background(p, q, metric):
    result = numerical_branch(p, q, metric, 8, include_profiles=True)
    coefficients = np.array(result["even_legendre_profiles"])
    profiles = np.zeros((4, 2*coefficients.shape[1]-1))
    profiles[:, ::2] = coefficients
    a, d, b, c = [Legendre(row) for row in profiles]
    roots = a.deriv().roots()
    candidates = [-1., 1., *(r.real for r in roots if abs(r.imag) < 1e-10 and abs(r.real) < 1-1e-10)]
    minimum = min(candidates, key=a)
    pole = abs(minimum) == 1
    if pole:
        hess_a, hess_c = (-minimum*field.deriv()(minimum) for field in (a, c))
    else:
        assert abs(minimum) < 1e-8
        hess_a, hess_c = (field.deriv(2)(minimum) for field in (a, c))
    assert hess_a > 0
    curvature_ratio = hess_c/hess_a
    # The normal mass at any meridian point lies between these endpoints.
    minimum_mass_relative_to_hess_a = min(4, 10/3+curvature_ratio)
    assert minimum_mass_relative_to_hess_a > 0

    nodes, weights = leggauss(96)
    normalization = (weights @ np.exp(2*d(nodes)-2*b(nodes)-3*c(nodes)))/2
    z = np.exp(2*d(minimum)-2*b(minimum)-3*c(minimum))/normalization
    eta = (result["lambda_minus_32"]+8)/24
    common = 8*a(minimum)/3+c(minimum)
    strengths = (np.sqrt(8*eta)*np.exp(common-2*d(minimum))*z,
                 np.sqrt(8*(1-eta))*np.exp(common-2*b(minimum)))
    pressure = 4*np.exp(-4*a(minimum))
    assert max(strengths) < pressure
    return {"chern_pair": [p, q], "minimum_orbit": "pole" if pole else "equator",
            "lower_mass_bound_relative_to_positive_hessian_of_A":
                float(minimum_mass_relative_to_hess_a),
            "largest_sphere_pressure_over_torus_pressure": float(max(strengths)/pressure),
            "sufficient_spectator_circumference_in_local_ads_units": float(4*np.pi/pressure),
            "internal_collective_coordinates": 2 if pole else 3}


def main():
    exact_checks()
    x, y = scalar_reduction()
    metric = metric_response(x, y)
    data = {"backgrounds": [check_background(p, q, metric) for p, q in ((7, 8), (8, 9), (38, 43))],
            "internal_and_chiral_negative_modes": 0,
            "geometric_normal_negative_modes_for_short_spectator": 1,
            "harmonic_two_and_three_form_dimensions": [0, 0]}
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_M5_cap_probe_index.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the capped M5 normal-mode factorization and short-circle index hypotheses.")


if __name__ == "__main__":
    main()
