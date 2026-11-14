"""Verify equal-charge fixed-flux E6 scalar radial exponents and transfer."""

import json

import sympy as sp

from toe_20261114_e6_attractor_hessian import OUT as HESSIAN

OUT = HESSIAN.with_name("toe_20261114_e6_scalar_radial.json")


def calculate():
    hessian = json.loads(HESSIAN.read_text(encoding="utf-8"))
    assert (hessian["positive_directions"], hessian["flat_directions"]) == (14, 28)
    r, q = sp.symbols("r q", positive=True)
    power = sp.symbols("s", real=True)
    warp = 1 + q/r**2
    # Maxwell flux held fixed, canonical kinetic coordinates in the STU plane.
    mass = 8*q**2/(warp*r**2*(r**2 + q)**2)

    def operator(field, mass_squared):
        return sp.diff(r**3*sp.diff(field, r), r) - warp*r**3*mass_squared*field

    flat_modes = [sp.Integer(1), 1/r**2]
    fixed_modes = [1/warp, warp**2]
    for modes, mu, indicial in [(flat_modes, 0, power*(power+2)),
                               (fixed_modes, mass, (power-2)*(power+4))]:
        for f in modes:
            assert sp.factor(operator(f, mu)) == 0
        normalized = sp.simplify(operator(r**power, mu) / r**(power+1))
        assert sp.simplify(sp.limit(normalized, r, 0)-indicial) == 0

    # Spherical radius squared tends to q; the AdS2 radius squared is q/4.
    assert sp.limit(mass, r, 0)*q/4 == 2
    t = sp.symbols("t", positive=True)
    # A first variation of H_i=1+epsilon_i+q/r^2, sum epsilon_i=0.
    variation = sp.diff(((warp+t)*(warp-t)*warp)**sp.Rational(1, 3)/(warp+t), t)
    assert sp.simplify(sp.limit(variation, t, 0)+fixed_modes[0]) == 0

    fixed_regular = sp.series(fixed_modes[0], r, 0, 6)
    fixed_far = sp.series(fixed_modes[0], r, sp.oo, 4)
    return dict(status="PASS", background="equal-charge static electric, fixed charge, linear s-wave",
                fixed=dict(multiplicity=14, mass_squared_ads_radius_squared=2,
                           indicial_exponents_r=[2, -4], ads_dimension=2,
                           horizon_series=str(fixed_regular), infinity_series=str(fixed_far)),
                flat=dict(multiplicity=28, mass_squared_ads_radius_squared=0,
                          indicial_exponents_r=[0, -2], ads_dimension_standard=1),
                horizon_transfer_fixed=0, horizon_transfer_flat=1)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
