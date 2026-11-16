"""Check the spherical wall obstruction and shoot slightly detuned walls."""

import json
from math import exp, expm1, log, sqrt
from pathlib import Path

from scipy.integrate import solve_ivp
from scipy.optimize import root
import sympy as sp


G = 80/3


def symbolic_checks():
    b, q, a, slope = sp.symbols("b q a slope", real=True)
    kinetic = sp.Rational(80, 3)
    w = 10*sp.exp(-8*b/3)-4*q*sp.exp(-20*b/3)
    v = -20*sp.exp(-16*b/3)+8*q*q*sp.exp(-40*b/3)
    f = -sp.diff(w, b)/kinetic
    assert sp.simplify(v-(kinetic*f*f/2-w*w/3)) == 0
    assert sp.simplify(sp.diff(v, b)/kinetic-f*sp.diff(f, b)-2*w*f/3) == 0
    constraint = a**-2+kinetic*slope*slope/24-v/12
    assert sp.simplify(constraint.subs(slope, f)-a**-2-w*w/36) == 0
    assert sp.simplify(constraint.subs(slope, -f)-a**-2-w*w/36) == 0

    # The planar interior curvature response and its wall gap.
    r, inner, outer = sp.symbols("r qminus qplus", positive=True)
    delta = outer-inner
    interior_response = sp.integrate(r*(inner+delta*r**4), (r, 0, 1))/outer**sp.Rational(1, 3)
    outer_ads_radius = outer**sp.Rational(2, 3)
    wall_jump = 4*delta*outer**sp.Rational(-5, 3)
    assert sp.simplify(6*(outer_ads_radius/2-interior_response)/wall_jump
                       -outer_ads_radius**2/2) == 0
    relative_jump = delta/outer
    inner_w_at_wall = (6+4*relative_jump)/outer_ads_radius
    f_at_wall = relative_jump/outer_ads_radius
    inner_slope_response = (12*(inner_w_at_wall*interior_response/3-1)
                            / (kinetic*f_at_wall))
    scalar_shift_response = -outer_ads_radius*(inner_slope_response
                                               +outer_ads_radius**2*f_at_wall/2)/12
    assert sp.simplify(scalar_shift_response+relative_jump*outer_ads_radius**2/40) == 0

    # Regular small displacement about the inner vacuum in an AdS ball.
    x = sp.Symbol("x", real=True)
    profile = 1+sp.Rational(16, 5)*sp.sinh(x)**2+sp.Rational(16, 7)*sp.sinh(x)**4
    assert sp.simplify(sp.diff(profile, x, 2)+4*sp.coth(x)*sp.diff(profile, x)-32*profile) == 0
    return {"normalized_breathing_kinetic_metric": str(kinetic),
            "leading_near_planar_one_minus_tension_ratio": "Lplus^2/(2*a_wall^2)",
            "leading_wall_breathing_shift": "-(1-qminus/qplus)*Lplus^2/(40*a_wall^2)",
            "wall_radial_constraint_mismatch_for_critical_or_higher_tension": True}


def field_terms(delta_b, q):
    inverse_ads_radius_squared = q**(-4/3)
    potential = inverse_ads_radius_squared*(-20*exp(-16*delta_b/3)+8*exp(-40*delta_b/3))
    force = 4*inverse_ads_radius_squared*exp(-40*delta_b/3)*expm1(8*delta_b)
    return potential, force


def radial_data(log_radius, delta_b, log_slope, q):
    potential, force = field_terms(delta_b, q)
    curvature = exp(-2*log_radius)
    warp_gradient_sq = (curvature-potential/12)/(1-G*log_slope**2/24)
    return warp_gradient_sq, force, curvature


def integrate_to_wall(q, start, wall, initial):
    def rhs(log_radius, fields):
        delta_b, log_slope = fields
        gradient_sq, force, curvature = radial_data(log_radius, delta_b, log_slope, q)
        acceleration = ((force+curvature*log_slope)/gradient_sq
                        + G*log_slope**3/6-4*log_slope)
        return log_slope, acceleration

    solution = solve_ivp(rhs, (start, wall), initial, method="DOP853",
                         atol=2e-18, rtol=4e-11)
    assert solution.success, solution.message
    delta_b, log_slope = solution.y[:, -1]
    gradient_sq, _, _ = radial_data(wall, delta_b, log_slope, q)
    warp_gradient = sqrt(gradient_sq)
    return delta_b+log(q)/4, log_slope*warp_gradient, warp_gradient


def shoot_wall(q_minus, radius, exterior_interval=2.4, center_fraction=0.001):
    # Fix q_plus=1 so L_plus=1. Shoot the two independent, regular
    # asymptotic data and solve the scalar/metric junction ratio exactly.
    wall = log(radius)
    center_start = log(center_fraction*q_minus**(2/3))
    exterior_start = wall+exterior_interval

    def evaluate(trial):
        center_amplitude, exterior_amplitude = trial
        center_value = center_amplitude/radius**4
        initial_correction = field_terms(center_value, q_minus)[1]*exp(2*center_start)/10
        interior = integrate_to_wall(q_minus, center_start, wall,
                                     (center_value+initial_correction, 2*initial_correction))
        outer_value = exterior_amplitude/radius**2*exp(-8*exterior_interval)
        exterior = integrate_to_wall(1, exterior_start, wall, (outer_value, -8*outer_value))
        return interior, exterior

    def residual(trial):
        interior, exterior = evaluate(trial)
        delta_b, delta_scalar, delta_warp = (out-inside for inside, out in zip(interior, exterior))
        return delta_b, delta_scalar-1.5*delta_warp

    guess = (7*(1-q_minus)*q_minus/64, 0)
    solved = root(residual, guess, tol=1e-9)
    assert solved.success or max(abs(value) for value in residual(solved.x)) < 1e-11
    interior, exterior = evaluate(solved.x)
    b_wall, _, warp_gradient = interior
    tension_unit = 4*(1-q_minus)*exp(-20*b_wall/3)
    alpha = -6*(exterior[2]-warp_gradient)/tension_unit
    assert 0 < alpha < 1
    return {"q_minus_over_q_plus": q_minus, "wall_radius_in_exterior_ads_units": radius,
            "tension_over_charge_normalized_value": alpha,
            "radius_squared_times_detuning": radius**2*(1-alpha),
            "wall_scalar_relative_to_outer_minimum": b_wall,
            "radius_squared_times_wall_breathing_shift": radius**2*b_wall,
            "maximum_junction_residual": max(abs(value) for value in residual(solved.x))}


def main():
    rows = []
    for q_minus in (0.50, 0.75, 0.90):
        for radius in (6, 10, 16):
            rows.append(shoot_wall(q_minus, radius))
        assert abs(rows[-1]["radius_squared_times_detuning"]-0.5) < 0.015
        predicted_shift = -(1-q_minus)/40
        assert abs(rows[-1]["radius_squared_times_wall_breathing_shift"]/predicted_shift-1) < 0.005
    control = shoot_wall(0.75, 10, exterior_interval=2.8, center_fraction=0.0005)
    baseline = rows[4]
    assert abs(control["radius_squared_times_detuning"] -
               baseline["radius_squared_times_detuning"]) < 0.001
    result = {"exact_comparison": symbolic_checks(), "detuned_examples": rows,
              "wider_integration_boundary_control": control}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_D3_spherical_discharge.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Verified the critical-wall comparison and subcritical spherical shooting.")


if __name__ == "__main__":
    main()
