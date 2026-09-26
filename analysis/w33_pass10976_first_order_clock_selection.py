#!/usr/bin/env python3
"""Pass 10976: exact mean-field first-order clock-selection law.

Passes 10972-10975 supply the S4 clock order parameter and a nonzero native
cubic component. This packet solves the minimal homogeneous Landau free energy

    F = alpha*p2 + beta*p2^2 - gamma*p3,  beta>0, gamma>0

using the exact angular bound max p3 = r^3/sqrt(3). The cubic makes the
S4->S3 transition first order at mean-field level, with exact coexistence,
jump, barrier and spinodal values. No continuum or cosmological claim is made.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass10976_first_order_clock_selection.json"
P72 = ROOT / "data" / "w33_pass10972_tetrahedral_cubic_clock_selector.json"
P73 = ROOT / "data" / "w33_pass10975_e6_cubic_reynolds_clock_weld.json"


def payload() -> dict:
    p72 = json.loads(P72.read_text(encoding="utf-8"))
    p73 = json.loads(P73.read_text(encoding="utf-8"))
    assert p72["invariants"]["cubic_bound_on_p2_1"] == "|p3| <= 1/sqrt(3)"
    assert p73["clock_restriction"]["coefficient"] == "-2/3"

    alpha, beta, gamma, r = sp.symbols(
        "alpha beta gamma r", positive=True, finite=True
    )
    kappa = gamma / sp.sqrt(3)
    f = alpha * r**2 - kappa * r**3 + beta * r**4
    # Nonzero stationary radii solve 4 beta r^2 - 3 kappa r + 2 alpha = 0.
    disc = sp.factor(9 * kappa**2 - 32 * alpha * beta)
    r_minus = sp.simplify((3 * kappa - sp.sqrt(disc)) / (8 * beta))
    r_plus = sp.simplify((3 * kappa + sp.sqrt(disc)) / (8 * beta))

    # Coexistence solves f(r*)=0 and f'(r*)=0 for r*>0.
    r_jump = sp.simplify(kappa / (2 * beta))
    alpha_coex = sp.simplify(kappa**2 / (4 * beta))
    barrier_r = sp.simplify(kappa / (4 * beta))
    barrier = sp.simplify(
        f.subs({alpha: alpha_coex, r: barrier_r})
    )
    ordered_curvature = sp.simplify(
        sp.diff(f, r, 2).subs({alpha: alpha_coex, r: r_jump})
    )
    alpha_ordered_spinodal = sp.simplify(9 * kappa**2 / (32 * beta))

    assert sp.simplify(f.subs({alpha: alpha_coex, r: r_jump})) == 0
    assert sp.simplify(sp.diff(f, r).subs({alpha: alpha_coex, r: r_jump})) == 0
    assert sp.simplify(barrier - kappa**4 / (256 * beta**3)) == 0
    assert sp.simplify(ordered_curvature - kappa**2 / (2 * beta)) == 0
    # Inherit the native E6 normalization if an effective coefficient g_E6
    # multiplies the Reynolds-projected cubic R(D)|A = -(2/3)p3.
    g = sp.symbols("g_E6", positive=True, finite=True)
    gamma_from_e6 = sp.Rational(2, 3) * g
    native = {
        "gamma_eff": "2 g_E6 / 3",
        "r_jump": str(sp.simplify(r_jump.subs(gamma, gamma_from_e6))),
        "alpha_coexistence": str(sp.simplify(alpha_coex.subs(gamma, gamma_from_e6))),
        "alpha_ordered_spinodal": str(
            sp.simplify(alpha_ordered_spinodal.subs(gamma, gamma_from_e6))
        ),
        "barrier_height": str(sp.simplify(barrier.subs(gamma, gamma_from_e6))),
    }

    # Optional linear temperature law alpha=a(T-T0).
    a, Tstar = sp.symbols("a Tstar", positive=True, finite=True)
    latent = sp.simplify(Tstar * a * r_jump**2)

    checks = {
        "parent_four_tetrahedral_vacua":
            p72["landau_selector"]["angular_vacua"]
            == "exactly the four positive tetrahedral clock directions",
        "native_cubic_projection_nonzero":
            p73["clock_restriction"]["nonzero_projection"] is True,
        "native_coefficient_minus_2_over_3":
            p73["clock_restriction"]["coefficient"] == "-2/3",
        "coexistence_positive_alpha":
            alpha_coex == gamma**2 / (12 * beta),
        "finite_jump":
            r_jump == gamma / (2 * sp.sqrt(3) * beta),
        "barrier_positive":
            barrier == gamma**4 / (2304 * beta**3),
        "ordered_spinodal":
            alpha_ordered_spinodal == 3 * gamma**2 / (32 * beta),
        "coexistence_inside_metastability_window":
            sp.simplify(alpha_ordered_spinodal - alpha_coex)
            == gamma**2 / (96 * beta),
        "ordered_curvature_positive":
            ordered_curvature == gamma**2 / (6 * beta),
        "native_rjump":
            native["r_jump"] == "sqrt(3)*g_E6/(9*beta)",
        "native_alpha_coexistence":
            native["alpha_coexistence"] == "g_E6**2/(27*beta)",
        "native_barrier":
            native["barrier_height"] == "g_E6**4/(11664*beta**3)",
    }
    assert all(checks.values())

    return {
        "schema": "w33.pass10976.first-order-clock-selection.v1",
        "status": "PASS",
        "headline": (
            "The nonzero clock cubic forces the minimal homogeneous S4-invariant "
            "Landau model to select one of four S4/S3 clock vacua by a first-order "
            "mean-field transition. Coexistence, jump, barrier and both spinodals "
            "are exact."
        ),
        "free_energy": {
            "order_parameter": "x in A3 augmentation, sum_i x_i=0",
            "invariants": "p2=sum_i x_i^2, p3=sum_i x_i^3",
            "functional": "F=alpha*p2 + beta*p2^2 - gamma*p3",
            "assumptions": "beta>0, gamma>0",
            "angular_minimum": "p3=+r^3/sqrt(3), four S4/S3 tetrahedral rays",
            "radial_function": "f(r)=alpha r^2 - (gamma/sqrt(3)) r^3 + beta r^4",
        },
        "exact_phase_structure": {
            "nonzero_stationary_discriminant":
                "3 gamma^2 - 32 alpha beta",
            "ordered_extrema_exist_for":
                "alpha <= 3 gamma^2/(32 beta)",
            "ordered_spinodal_alpha": "3 gamma^2/(32 beta)",
            "coexistence_alpha": "gamma^2/(12 beta)",
            "order_parameter_jump": "gamma/(2 sqrt(3) beta)",
            "barrier_radius_at_coexistence":
                "gamma/(4 sqrt(3) beta)",
            "barrier_height_at_coexistence":
                "gamma^4/(2304 beta^3)",
            "ordered_radial_curvature_at_coexistence":
                "gamma^2/(6 beta)",
            "disordered_spinodal_alpha": "0",
            "metastability_width_alpha":
                "3 gamma^2/(32 beta)",
            "coexistence_to_ordered_spinodal_gap":
                "gamma^2/(96 beta)",
            "vacuum_multiplicity_below_transition":
                "4 for gamma>0; opposite tetrahedron for gamma<0",
            "goldstone_modes": 0,
            "reason_no_goldstones": "S4->S3 breaks a finite group",
        },
        "native_E6_normalization": native,
        "temperature_parameterization": {
            "if": "alpha=a(T-T0), a>0",
            "transition_temperature_shift":
                "T*-T0 = gamma^2/(12 a beta)",
            "latent_heat_at_coexistence":
                "L=T* a gamma^2/(12 beta^2)",
            "derivation": "L=T* a r_jump^2",
        },
        "interpretation": (
            "Pass 10975 makes gamma structurally nonzero after projection onto "
            "the exact clock symmetry. Therefore the minimal analytic Landau "
            "model does not pass continuously through alpha=0: an ordered "
            "tetrahedral clock vacuum becomes globally degenerate already at "
            "positive alpha and the order parameter jumps discontinuously."
        ),
        "boundary": (
            "This is an exact mean-field statement for the minimal homogeneous "
            "Landau polynomial. It is not a theorem about a microscopic W33 "
            "Hamiltonian, finite-temperature universe, cosmological phase "
            "transition, domain walls, nucleation rate, or fluctuation-corrected "
            "critical behavior. Extra fields, nonlocal terms, fluctuations or a "
            "different dynamical realization can modify the transition."
        ),
        "checks": checks,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    p = payload()
    text = json.dumps(p, indent=2, sort_keys=True) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text(encoding="utf-8") != text:
            raise SystemExit("certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "status": p["status"],
        "coexistence": p["exact_phase_structure"]["coexistence_alpha"],
        "jump": p["exact_phase_structure"]["order_parameter_jump"],
        "native_alpha": p["native_E6_normalization"]["alpha_coexistence"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
