"""Find fixed integer Chern backgrounds in the capped M5 fold regime."""

import json
from math import ceil, exp, gcd, pi, sqrt
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import Legendre
from scipy.optimize import brentq

from toe_20261116_Tpq_coupled_warp_branch import metric_response, scalar_reduction, solve_shape
from toe_20261116_Tpq_M5_cap_nonlinear_fold import transitions
from toe_20261116_Tpq_M5_cap_sixth_order import geometric_data, sixth_order
from toe_20261116_Tpq_M5_cap_spectator_branch import reduced_quartic
from toe_20261116_Tpq_M5_finite_stripe import family


def tension_ratio(solution):
    coefficients = solution["even_legendre_profiles"][0]
    polynomial = np.zeros(2*len(coefficients)-1)
    polynomial[::2] = coefficients
    warp = Legendre(polynomial)
    extrema = [-1., 1., *(float(r.real) for r in warp.deriv().roots()
                         if abs(r.imag) < 1e-10 and abs(r.real) < 1)]
    selected = min(extrema, key=warp)
    return exp(4*warp(selected)), selected


def ratio_squared(eta):
    return (1-eta)*(1+eta)**2/(eta*(2-eta)**2)


def quantized_shape(p, q):
    return brentq(lambda value: q*q*value*(2-value)**2
                  -p*p*(1-value)*(1+value)**2, 0, 1)


def continue_polar(metric, target, count=20):
    start = 1/3+0.005
    solved = {start: solve_shape(start, metric, count)}

    def evaluate(eta):
        fit = solve_shape(eta, metric, count)
        solved[eta] = fit
        assert fit["quadrupole_amplitude"] < 0
        return tension_ratio(fit)[0]

    last = start
    for step in range(1, 49):
        eta = start+0.005*step
        if evaluate(eta) < target:
            break
        last = eta
    else:
        raise AssertionError("Warp continuation did not bracket the target tension.")
    at_target = brentq(lambda point: evaluate(point)-target, *sorted((last, eta)), xtol=1e-11)
    scan = [{"eta": float(point), "tension_ratio": tension_ratio(solution)[0],
             "quadrupole_amplitude": solution["quadrupole_amplitude"]}
            for point, solution in sorted(solved.items())]
    return at_target, scan


def choose_pair(target_shape, root, metric):
    target_ratio = np.sqrt(ratio_squared(target_shape))
    # Use the local derivative to rank affordable primitive rational approximants.
    estimate = []
    for p in range(1, 251):
        closest = round(p*target_ratio)
        for q in (closest-1, closest, closest+1):
            if q > 0 and gcd(p, q) == 1:
                eta = quantized_shape(p, q)
                estimate.append((abs(eta-target_shape), p+q, p, q, eta))
    candidates = []
    for _, _, p, q, eta in sorted(estimate)[:20]:
        solution = solve_shape(eta, metric, 20)
        alpha, _ = tension_ratio(solution)
        if 0.00007 < root-alpha < 0.00028:
            candidates.append((p+q, p, q, eta, solution))
    assert candidates
    _, p, q, eta, coarse = min(candidates)
    fine = solve_shape(eta, metric, 23, initial_profiles=coarse["even_legendre_profiles"])
    high = solve_shape(eta, metric, 28, initial_profiles=fine["even_legendre_profiles"])
    alpha, minimum = tension_ratio(high)
    assert abs(alpha-tension_ratio(fine)[0]) < 2e-9
    assert .00007 < root-alpha < .00028
    assert high["maximum_retained_equation_residual"] < 1e-10
    assert high["maximum_traceless_equation_residual"] < 1e-10
    return {"chern_pair": [p, q], "eta": eta, "alpha": alpha,
            "minimum_x": minimum, "distance_below_quartic_zero": root-alpha,
            "field_solution": high}


def torus_example(background, nonlinear, critical):
    p, q = background["chern_pair"]
    eta, alpha = background["eta"], background["alpha"]
    pole = background["minimum_x"]
    assert abs(pole) == 1
    profile = background["field_solution"]["even_legendre_profiles"]
    a_star, c_star = sum(profile[0]), sum(profile[3])
    page_shift = background["field_solution"]["page_integral_relative_shift"]
    # The lift multiplies the reference torus area in AdS units by this
    # local factor. The Page condition supplies the additional scale factor.
    area_per_multiplier = (16*pi*p/(4*(2-eta)*sqrt(8*eta))
                           *(1+page_shift)*exp(4*a_star/3-2*c_star))
    equal_action = nonlinear["equal_action"]
    spectator = 2*pi/sqrt(critical+equal_action["detuning"])
    cap = family(alpha)
    cap_width = cap["round_threshold_period"]*cap["samples"][0]["period_over_round_threshold"]
    multiplier = ceil(1.2*cap_width*spectator/area_per_multiplier)
    longitudinal = area_per_multiplier*multiplier/spectator
    assert longitudinal > cap_width
    return {"horizontal_and_mixed_periods_per_common_scale":
                [1, multiplier*p, multiplier*q],
            "spectator_circumference_at_action_crossing": spectator,
            "longitudinal_circumference_at_action_crossing": longitudinal,
            "unmodulated_cap_width": cap_width}


def main():
    data_dir = Path(__file__).resolve().parents[1]/"data"
    sixth = json.loads((data_dir/"toe_20261116_Tpq_M5_cap_sixth_order.json").read_text(encoding="utf-8"))
    root = sixth["crossing"]["alpha"]
    x, y = scalar_reduction()
    metric = metric_response(x, y)
    shape, trace = continue_polar(metric, root-.00016)
    quantized = choose_pair(shape, root, metric)
    print(f"Located integer Chern pair {quantized['chern_pair']} at alpha={quantized['alpha']:.10f}.",
          flush=True)
    cap_coefficients = sixth_order(quantized["alpha"], 24, 340)
    assert cap_coefficients["quartic"] < 0 < cap_coefficients["reduced_sixth"]
    nonlinear = transitions(quantized["alpha"], 17, 7, cap_coefficients)
    critical, _, _ = reduced_quartic(geometric_data(quantized["alpha"]), 17, 220)
    row = {"shape_trace": trace, "quantized_background": quantized,
           "cap_coefficients": cap_coefficients, "nonlinear_cap": nonlinear,
           "torus_example": torus_example(quantized, nonlinear, critical)}
    output = data_dir/"toe_20261116_Tpq_quantized_cap_fold.json"
    output.write_text(json.dumps(row, indent=2)+"\n", encoding="utf-8")
    print("Verified the M5 fold on quantized Type IIB backgrounds.", flush=True)


if __name__ == "__main__":
    main()
