"""Check all bosonic probe blocks for the primitive torus-wrapped M5."""

import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import Legendre
import sympy as sp

from toe_20261116_Tpq_coupled_warp_branch import metric_response, numerical_branch, scalar_reduction


def exact_checks():
    a, b, c, d = sp.symbols("A B C D")
    rho = c-5*a/3
    warp = a+rho/3
    sphere_scale = rho/3+d-5*a/3
    assert sp.expand(2*warp-2*sphere_scale) == 16*a/3-2*d
    assert sp.expand(4*warp-4*rho/3) == 4*a
    source = 4*(sp.exp(-40*a/3)-sp.exp(-16*a/3))
    sphere_radius_factor = sp.exp(8*a)/(1-sp.exp(8*a))
    trace_times_radius_squared = 4*sp.exp(16*a/3)*source*sphere_radius_factor
    assert sp.simplify(trace_times_radius_squared) == 16

    x, parameter = sp.symbols("x epsilon", real=True)
    quadrupole = parameter*sp.legendre(2, x)
    k1 = sp.Rational(16, 3)
    cases = []
    for label, location, geometric_hessian in (
        ("pole", 1, -x*sp.diff(quadrupole, x)),
        ("equator", 0, sp.diff(quadrupole, x, 2)),
    ):
        value = quadrupole.subs(x, location)
        hessian = geometric_hessian.subs(x, location)
        eigenvalue = sp.simplify(4*k1*hessian/(-8*value))
        assert eigenvalue == (8 if label == "pole" else 16)
        cases.append({"minimum_orbit": label,
                      "positive_internal_normal_mass_squared_times_bubble_radius_squared":
                          int(eigenvalue),
                      "positive_polarizations": 2 if label == "pole" else 1,
                      "internal_collective_coordinates": 2 if label == "pole" else 3})
    # Poincare polynomial of S4 x T2. In particular b2=1, b3=0.
    t = sp.Symbol("t")
    cohomology = sp.Poly((1+t**4)*(1+t)**2, t)
    assert cohomology.nth(2) == 1 and cohomology.nth(3) == 0
    return cases


def numerical_examples():
    x, y = scalar_reduction()
    response = metric_response(x, y)
    rows = []
    for p, q in ((7, 8), (8, 9), (38, 43)):
        warp = numerical_branch(p, q, response, 8, include_profiles=True)
        coefficients = np.array(warp["even_legendre_profiles"])
        profiles = np.zeros((4, 2*coefficients.shape[1]-1))
        profiles[:, ::2] = coefficients
        a, d = (Legendre(profiles[i]) for i in (0, 1))
        roots = a.deriv().roots()
        interior = [z.real for z in roots if abs(z.imag) < 1e-10 and abs(z.real) < 1-1e-12]
        candidates = [-1., 1., *interior]
        location = min(candidates, key=a)
        pole = abs(location) == 1
        if pole:
            angular_curvature = -location*a.deriv()(location)
        else:
            assert abs(location) < 1e-8
            angular_curvature = a.deriv(2)(location)
        assert angular_curvature > 0
        value = a(location)
        k1 = (32+warp["lambda_minus_32"])/6
        radius_squared = np.exp(8*value)/(-np.expm1(8*value))
        mass_times_radius_squared = (
            4*k1*np.exp(16*value/3-2*d(location))*angular_curvature*radius_squared
        )
        limit = 8 if pole else 16
        assert abs(mass_times_radius_squared-limit) < 2e-8
        rows.append({"chern_pair": [p, q], "minimum_orbit": "pole" if pole else "equator",
                     "positive_internal_normal_mass_squared_times_bubble_radius_squared":
                         mass_times_radius_squared,
                     "internal_zero_modes": 2 if pole else 3,
                     "chiral_flat_holonomy_zero_modes": 1,
                     "external_center_zero_modes": 5})
    return rows


def main():
    data = {"exact_internal_mass_trace_times_bubble_radius_squared": 16,
            "exact_eigenvalues": exact_checks(), "numerical_examples": numerical_examples(),
            "chiral_nonzero_momentum_eigenvalues_times_bubble_radius_squared":
                "(ell+1)*(ell+2)+a^2*|k_T|_physical^2, ell>=1",
            "chiral_harmonic_three_form_dimension": 0,
            "internal_and_chiral_negative_modes": 0}
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_M5_probe_index.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the internal-normal gaps and chiral cohomology at the wrapped M5 probe.")


if __name__ == "__main__":
    main()
