"""Exact Eguchi–Hanson inner coefficients for the cubic flux EFT."""

import json
from pathlib import Path

import sympy as sp


def verify():
    r, a = sp.symbols("r a", positive=True)
    alpha, beta = sp.symbols("alpha beta", real=True)
    radial_factor = 1-a**4/r**4

    def proper_derivative(function):
        return sp.sqrt(radial_factor)*sp.diff(function, r)

    horizontal = r/2
    fiber = r*sp.sqrt(radial_factor)/2
    sectional = [sp.simplify(-proper_derivative(proper_derivative(w))/w) for w in (horizontal, horizontal, fiber)]
    curvature_eigenvalues = [2*value for value in sectional]
    assert curvature_eigenvalues == [-4*a**4/r**6, -4*a**4/r**6, 8*a**4/r**6]
    kretschmann = sp.expand(4*sum(value**2 for value in curvature_eigenvalues))
    assert kretschmann == 384*a**8/r**12
    curvature_cube = sp.expand(sum(value**3 for value in curvature_eigenvalues))

    # After angular integration the volume density is pi^2 r^3; suppress pi^2 here.
    direct = sp.integrate(curvature_cube*r**3, (r, a, sp.oo))
    assert direct == 192/(7*a**2)
    assert sp.integrate(kretschmann*r**3, (r, a, sp.oo)) == 48

    external_warp = alpha*(24/r**2+8*a**4/r**6)/7
    warp_flux = r**3 * radial_factor * sp.diff(external_warp, r)
    laplacian = sp.factor(sp.diff(warp_flux, r)/r**3)
    assert sp.simplify(laplacian+alpha*kretschmann/7) == 0
    assert sp.simplify(warp_flux.subs(r, a)) == 0
    assert sp.limit(external_warp, r, sp.oo) == 0

    backreaction = sp.integrate(sp.Rational(5, 2)*alpha*kretschmann*external_warp*r**3, (r, a, sp.oo))
    assert backreaction == 19968*alpha**2/(49*a**2)
    kinetic = sp.integrate(-sp.Rational(35, 2)*radial_factor*sp.diff(external_warp, r)**2*r**3, (r, a, sp.oo))
    assert sp.simplify(kinetic+backreaction) == 0
    combined = sp.factor(beta*direct+backreaction)
    assert sp.simplify(combined.subs(beta, -104*alpha**2/7)) == 0

    # a=sqrt(ell*R), with L proportional to R and Vol(M) proportional to R^4.
    ell, radius = sp.symbols("ell R", positive=True)
    scale = sp.sqrt(ell*radius)
    assert ell**4/(radius**2*scale**2) == (ell/radius)**3
    return {
        "curvature_cube_core_in_units_pi_squared": str(direct),
        "gauss_bonnet_core_external_log_warp": str(external_warp),
        "gauss_bonnet_exchange_core_in_units_pi_squared": str(backreaction),
        "combined_inner_action_coefficient_in_units_pi_squared": str(combined),
        "example_double_scaling": "a=sqrt(ell*R): local expansion ell/R, dimensionless reduced effect (ell/R)^3",
    }


if __name__ == "__main__":
    result = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_cubic_flux_bubble_eft.json"
    path.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
