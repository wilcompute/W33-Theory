"""Verify the Eguchi–Hanson bolt kinetic norm and canonical core potential."""

import json
from pathlib import Path

import sympy as sp


def verify():
    a, r, matching_radius, radius, ell, phi = sp.symbols("a r b R ell phi", positive=True)
    effective_coefficient = sp.Symbol("Omega", real=True)
    factor = 1-a**4/r**4
    radial_shift = a**3/r**3  # r^4-a^4 fixed, so the chart follows the bolt.
    diagonal_metric = [1/factor, r**2/4, r**2/4, r**2*factor/4]
    variation = []
    for index, metric_component in enumerate(diagonal_metric):
        h = sp.diff(metric_component, a)+radial_shift*sp.diff(metric_component, r)
        if index == 0:
            h += 2*sp.diff(radial_shift, r)*metric_component
        variation.append(sp.factor(h/metric_component))
    scale = 2*a**3/r**4
    assert variation == [-scale, scale, scale, -scale]
    assert sum(variation) == 0

    # For diagonal cohomogeneity-one perturbations the radial divergence
    # is h_rr' + sum_i (w_i'/w_i)(h_rr-h_ii) in the proper radial frame.
    divergence = sp.diff(variation[0], r)+sum(
        (sp.diff(metric, r)/(2*metric))*(variation[0]-value)
        for metric, value in zip(diagonal_metric[1:], variation[1:])
    )
    assert sp.simplify(divergence*sp.sqrt(factor)) == 0
    norm_integrand = sp.pi**2*r**3*sum(value**2 for value in variation)
    total = sp.integrate(norm_integrand, (r, a, sp.oo))
    assert total == 4*sp.pi**2*a**2
    enclosed = sp.integrate(norm_integrand, (r, a, matching_radius))
    assert sp.simplify(enclosed/total-(1-a**4/matching_radius**4)) == 0

    volume = 6*sp.pi**2*radius**4
    kinetic = total/(2*volume)
    canonical = a**2/(2*sp.sqrt(3)*radius**2)
    assert sp.simplify(sp.diff(canonical, a)**2-kinetic) == 0
    potential = -sp.Rational(320, 7)*effective_coefficient/(radius**2*a**2)
    canonical_potential = sp.factor(potential.subs(a**2, 2*sp.sqrt(3)*radius**2*phi))
    potential_curvature = sp.diff(canonical_potential, phi, 2).subs(phi, canonical)
    assert sp.simplify(potential_curvature+sp.Rational(7680, 7)*effective_coefficient*radius**2/a**6) == 0

    # A radius window where the canonical curvature is order one in AdS
    # units while the action correction and the local EFT parameter are small.
    amplitude_scale = ell**sp.Rational(2, 3)*radius**sp.Rational(1, 3)
    assert sp.simplify((ell**4*radius**2/a**6).subs(a, amplitude_scale)) == 1
    assert sp.simplify((ell**4/(radius**2*a**2)).subs(a, amplitude_scale)-(ell/radius)**sp.Rational(8, 3)) == 0
    return {
        "orthonormal_TT_variation": [str(entry) for entry in variation],
        "integrated_squared_norm": str(total),
        "norm_fraction_inside_radius_b": "1-(a/b)^4",
        "canonical_radial_coordinate_core": str(canonical),
        "core_potential_times_AdS_radius_squared": str(canonical_potential),
        "second_derivative_of_dimensionless_core_potential": str(sp.simplify(potential_curvature)),
        "order_one_curvature_double_scaling": "a=ell^(2/3)*R^(1/3)",
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_cubic_flux_bolt_distance.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
