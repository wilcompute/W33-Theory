"""Exact finite checks of the many-sphere magnetic force and KK gap formulas."""

import json
from pathlib import Path

import sympy as sp


def check_case(d, count):
    fluxes = sp.symbols(f"X:{count}", positive=True)
    betas = sp.symbols(f"b:{count}", real=True)
    curvatures = sp.symbols(f"A:{count}", positive=True)
    sphere_sum = sum(curvatures)
    volume_power = sp.Rational(4, d-2)
    common_power = count * volume_power
    spacing = d-2+count
    total = sum(fluxes)
    invariant = total**(d-2) * sp.prod(fluxes)
    for order in (0, 1, 2):
        degree = 1 + spacing*order
        energy = total * invariant**order
        ratio = (4*degree+common_power)/(4+common_power)
        for other in fluxes[1:]:
            pair_force = fluxes[0]*sp.diff(energy, fluxes[0]) - other*sp.diff(energy, other)
            assert sp.factor(total*pair_force-ratio*(fluxes[0]-other)*energy) == 0

    maxwell_fields = [2*a + 2*sphere_sum/spacing for a in curvatures]
    potential = sp.exp(-volume_power*sum(betas)) * sum(
        -2*a*sp.exp(-2*b) + x*sp.exp(-4*b)/2
        for a, b, x in zip(curvatures, betas, maxwell_fields)
    )
    vacuum = dict.fromkeys(betas, 0)
    assert sp.factor(potential.subs(vacuum) + sp.Rational(d-2, spacing)*sphere_sum) == 0
    for b in betas:
        assert sp.factor(sp.diff(potential, b).subs(vacuum)) == 0
    expected_hessian = sp.diag(*(8*(x-a) for a, x in zip(curvatures, maxwell_fields)))
    expected_hessian += volume_power**2 * sp.Rational(d-2, spacing)*sphere_sum*sp.ones(count)
    assert (sp.hessian(potential, betas).subs(vacuum)-expected_hessian).applyfunc(sp.factor) == sp.zeros(count)

    # Constant external curvature and the upper bound on the first positive TT mass.
    radius_sq = (d-1)*spacing/sphere_sum
    assert sp.factor(radius_sq * sum(maxwell_fields) - 2*(d-1)*(d+2*count-2)) == 0
    gap_bound = sp.Rational(2*(d-1)*spacing, count)
    assert gap_bound <= d*(d-1)
    return {
        "external_dimension": d,
        "sphere_count": count,
        "first_nonlinear_field_strength_power": 2*(spacing+1),
        "maxwell_mass_squared_gap_times_AdS_radius_squared_upper_bound": str(gap_bound),
    }


if __name__ == "__main__":
    report = [check_case(d, count) for d, count in ((3, 2), (4, 2), (4, 3), (5, 2), (5, 3), (7, 5))]
    result = json.dumps(report, indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_many_sphere_magnetic.json"
    path.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
