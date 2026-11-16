"""Resolve the constrained O(5) Hessian on the detuned D3 profiles."""

import json
from math import exp, log
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import root_scalar

from toe_20261116_D3_spherical_discharge import G, field_terms, integrate_to_wall, shoot_wall


def exact_bulk_checks():
    a, v, curvature = sp.symbols("a v Vbb", positive=True)
    k, kb = sp.symbols("K Kb", real=True)
    c = sp.Rational(10, 9)
    s = sp.sqrt(1-c*v*v)
    kbb = (-a*a*curvature/24-kb*kb)/k
    hbb = -kbb*s
    hbv = kb*c*v/s
    hvv = k*c/s**3
    expected = c*(a*a*curvature/24+s*s*kb*kb)/s**2
    assert sp.simplify(hbb*hvv-hbv*hbv-expected) == 0

    n, va, x = sp.symbols("n va x", positive=True)
    kinetic = sp.Rational(80, 3)
    euclidean_lagrangian = n*(a**4*x-12*a*a)+(kinetic*a**4*va*va/2-12*a*a)/n
    momentum = sp.diff(euclidean_lagrangian, va)
    hamiltonian = momentum*va-euclidean_lagrangian
    x_on_constraint = ((kinetic*a**4*va*va/2-12*a*a)/n**2+12*a*a)/a**4
    assert sp.simplify(hamiltonian.subs(x, x_on_constraint)-24*a*a/n) == 0


def endpoint_gradient(q_inner, x_wall, b_wall, alpha, x_reference,
                      exterior_extent, center_fraction):
    radius = exp(x_wall)
    x_center = log(center_fraction*q_inner**(2/3))
    x_boundary = x_wall+exterior_extent

    def interior(amplitude):
        value = amplitude/radius**4
        curvature_correction = field_terms(value, q_inner)[1]*exp(2*x_center)/10
        return integrate_to_wall(q_inner, x_center, x_wall,
                                 (value+curvature_correction, 2*curvature_correction))

    def exterior(amplitude):
        value = amplitude/radius**2*exp(-8*exterior_extent)
        return integrate_to_wall(1, x_boundary, x_wall, (value, -8*value))

    profiles = []
    guesses = (7*(1-q_inner)*q_inner/64, b_wall*radius**2)
    for profile, guess in zip((interior, exterior), guesses):
        fit = root_scalar(lambda parameter: profile(parameter)[0]-b_wall,
                          x0=guess, x1=guess+1e-4, xtol=5e-14)
        assert fit.converged
        result = profile(fit.root)
        assert abs(result[0]-b_wall) < 3e-10
        profiles.append(result)
    _, scalar_jump, warp_jump = (outer-inner for inner, outer in zip(*profiles))
    tension = alpha*4*(1-q_inner)*exp(-20*b_wall/3)
    return exp(4*(x_wall-x_reference))*np.array(
        [4*(6*warp_jump+tension), -G*scalar_jump-20*tension/3]
    )


def finite_difference_hessian(q_inner, radius, b_wall, alpha, step,
                              exterior_extent=2.4, center_fraction=0.001):
    x_reference = log(radius)
    position = np.array([x_reference, b_wall])

    def gradient(point):
        return endpoint_gradient(q_inner, *point, alpha, x_reference,
                                 exterior_extent, center_fraction)

    assert np.linalg.norm(gradient(position)) < 2e-8
    hessian = np.column_stack([(gradient(position+step*direction) -
                               gradient(position-step*direction))/(2*step)
                              for direction in np.eye(2)])
    assert abs(hessian[0, 1]-hessian[1, 0]) < 0.001
    return (hessian+hessian.T)/2


def index_checks():
    rows = []
    for q_inner in (0.75, 0.90):
        for radius in (6, 10, 16):
            wall = shoot_wall(q_inner, radius)
            b_wall = wall["wall_scalar_relative_to_outer_minimum"]
            alpha = wall["tension_over_charge_normalized_value"]
            # The regular interior profile increases to b_wall; the
            # normalizable exterior profile increases from b_wall to zero.
            assert b_wall < 0
            maximum_interior_excursion = b_wall-log(q_inner)/4
            assert 0 < maximum_interior_excursion < log(2.5)/8
            assert -log(2.5)/8 < b_wall

            coarse = finite_difference_hessian(q_inner, radius, b_wall, alpha, 3e-5)
            fine = finite_difference_hessian(q_inner, radius, b_wall, alpha, 1e-5)
            assert np.max(abs(coarse-fine)) < 0.001
            eigenvalues = np.linalg.eigvalsh(fine)
            schur = fine[0, 0]-fine[0, 1]**2/fine[1, 1]
            assert fine[1, 1] > 0 and schur < 0 and eigenvalues[0] < 0 < eigenvalues[1]
            scaled = -schur*radius**2/(16*(1-q_inner))
            if radius == 16:
                assert abs(scaled-1) < 0.03
            rows.append({"q_minus_over_q_plus": q_inner, "wall_radius_over_outer_ads": radius,
                         "alpha": alpha, "endpoint_hessian_normalized_by_wall_radius_fourth":
                         fine.tolist(), "endpoint_hessian_eigenvalues": eigenvalues.tolist(),
                         "radius_schur_complement": float(schur),
                         "schur_relative_to_leading_near_planar_value": float(scaled),
                         "finite_difference_hessian_change": float(np.max(abs(coarse-fine)))})
    return rows


def main():
    exact_bulk_checks()
    rows = index_checks()
    control = shoot_wall(0.75, 10, exterior_interval=2.8, center_fraction=0.0005)
    wider_hessian = finite_difference_hessian(
        0.75, 10, control["wall_scalar_relative_to_outer_minimum"],
        control["tension_over_charge_normalized_value"], 1e-5,
        exterior_extent=2.8, center_fraction=0.0005,
    )
    baseline_hessian = np.array(rows[1]["endpoint_hessian_normalized_by_wall_radius_fourth"])
    cutoff_change = float(np.max(abs(wider_hessian-baseline_hessian)))
    assert cutoff_change < 0.001
    wider_eigenvalues = np.linalg.eigvalsh(wider_hessian)
    assert wider_eigenvalues[0] < 0 < wider_eigenvalues[1]
    data = {"bulk_dirichlet_block_positive_if_potential_convex_along_profile": True,
            "index_reduces_to_two_endpoint_variables_in_O5": True,
            "tested_detuned_saddles": rows,
            "wider_boundary_control": {"charge_ratio": 0.75, "wall_radius": 10,
                                       "max_hessian_change": cutoff_change,
                                       "eigenvalues": wider_eigenvalues.tolist()}}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_D3_radial_negative_mode.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified the constrained Dirichlet Hessian and the radial index of six detuned walls.")


if __name__ == "__main__":
    main()
