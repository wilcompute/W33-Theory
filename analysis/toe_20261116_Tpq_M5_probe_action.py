"""Check the wrapped M5 pressure weights and exact round probe action."""

import json
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import Legendre
import sympy as sp

from toe_20261116_Tpq_coupled_warp_branch import metric_response, numerical_branch, scalar_reduction


def exact_checks():
    a, c, d, b, z = sp.symbols("A C D B Z")
    log_radius = c-5*a/3
    external_warp = a+log_radius/3
    base1_scale = d-5*a/3+log_radius/3
    base2_scale = b-5*a/3+log_radius/3
    torus_scale = -2*log_radius/3
    horizontal = -5*a+log_radius+2*d+2*b-20*a/3
    assert sp.expand(external_warp+horizontal-2*base1_scale-2*base2_scale) == -4*a
    sphere1_flux = sp.expand(external_warp-2*base1_scale-2*torus_scale)
    sphere2_flux = sp.expand(external_warp-2*base2_scale-2*torus_scale)
    assert sphere1_flux == 8*a/3-2*d+c and sphere2_flux == 8*a/3-2*b+c
    assert sp.expand(4*external_warp+2*torus_scale) == 4*a

    ratio = sp.Symbol("alpha", positive=True)
    distance = sp.atanh(ratio)
    denominator = 1-ratio**2
    volume = (4*ratio*(1+ratio**2)/denominator**2/32
              -2*ratio/denominator/4+3*distance/8)
    action = sp.simplify(ratio**4/denominator**2-4*volume/ratio)
    expression = 1+1/(2*denominator)-3*distance/(2*ratio)
    assert sp.simplify(action-expression) == 0
    assert sp.limit((1-ratio)*expression, ratio, 1, dir="-") == sp.Rational(1, 4)
    assert sp.series(expression, ratio, 0, 6).removeO() == ratio**4/5

    resonance_volume_times_p = 9*sp.sqrt(6)*sp.pi**3/40
    units = 4*sp.pi**3/(3*resonance_volume_times_p)
    limits = {}
    for norm, factor in ((-7, 256), (17, 512)):
        deficit_times_p_squared = sp.Rational(5*abs(norm), factor)
        action_limit = sp.simplify(units/(4*deficit_times_p_squared))
        limits[str(norm)] = str(action_limit)
    return {"action_prefactor_at_resonance_over_N0_p": str(units),
            "action_over_N0_p_cubed_along_pell_sequences": limits}


def pointwise_examples():
    x, y = scalar_reduction()
    metric = metric_response(x, y)
    mp.mp.dps = 40
    rows = []
    for p, q in ((7, 8), (8, 9), (38, 43)):
        result = numerical_branch(p, q, metric, 8, include_profiles=True)
        coefficients = np.array(result["even_legendre_profiles"])
        polynomial = np.zeros(2*coefficients.shape[1]-1)
        polynomial[::2] = coefficients[0]
        a = Legendre(polynomial)
        roots = a.deriv().roots()
        extrema = [-1., 1., *(r.real for r in roots if abs(r.imag) < 1e-10 and abs(r.real) < 1)]
        location = min(extrema, key=a)
        minimum = a(location)
        alpha = mp.exp(4*mp.mpf(float(minimum)))
        assert 0 < alpha < 1
        bracket = 1+1/(2*(1-alpha**2))-3*mp.atanh(alpha)/(2*alpha)
        assert bracket > 0
        eta = (result["lambda_minus_32"]+8)/24
        k1, k2 = 4*(1+eta), 4*(2-eta)
        fiber = 2*np.sqrt(8*eta)/(p*k1)
        reference_volume = 32*np.pi**3*fiber/(k1*k2)
        page_integral = reference_volume*(1+result["page_integral_relative_shift"])
        exponent_over_N0 = 4*mp.pi**3*alpha*bracket/(3*page_integral)
        polynomial[::2] = coefficients[3]
        fiber_log = Legendre(polynomial)(location)
        momentum_cutoff = 4*(1-alpha**2)*mp.exp(-2*fiber_log+4*minimum/3)/alpha**2
        rows.append({"chern_pair": [p, q], "minimum_warp": float(minimum),
                     "tension_to_charge_ratio": float(alpha),
                     "radius_over_local_ads_length": float(alpha/mp.sqrt(1-alpha**2)),
                     "probe_exponent_over_horizontal_flux": float(exponent_over_N0),
                     "extra_radial_negative_modes_require_bare_torus_eigenvalue_below":
                         float(momentum_cutoff)})
    return rows


def main():
    data = exact_checks()
    data["near_resonant_probe_examples"] = pointwise_examples()
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_M5_probe_action.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the M5 flux weights, hyperbolic action, and fixed-Page nucleation examples.")


if __name__ == "__main__":
    main()
