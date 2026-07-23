#!/usr/bin/env python3
"""Rigorous phase-current reformulation of Casey's invariant-tangent RH idea.

The useful mathematical core is retained and made branch-independent:

* the completed Riemann xi function regularizes the zeta pole at s=1;
* away from zeros, the horizontal phase current is Im(xi'/xi);
* contour-integrated phase current is the argument principle;
* an off-line reflection pair admits an antisymmetric cocycle current whose
  squared boundary energy is positive and vanishes exactly on Re(s)=1/2.

The final energy identity is an RH-equivalent detector, not a proof that its
classical total vanishes. W(3,3) supplies an exact finite graph model where
that defect energy is identically zero.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]


def completed_xi(s: complex | mp.mpc) -> mp.mpc:
    """Riemann's completed entire xi function, with removable endpoints filled."""
    z = mp.mpc(s)
    if abs(z) < mp.mpf("1e-40") or abs(z - 1) < mp.mpf("1e-40"):
        return mp.mpc(mp.mpf("0.5"))
    return (
        mp.mpf("0.5")
        * z
        * (z - 1)
        * mp.power(mp.pi, -z / 2)
        * mp.gamma(z / 2)
        * mp.zeta(z)
    )


def xi_log_derivative_direct(s: complex | mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    return mp.diff(completed_xi, z) / completed_xi(z)


def xi_log_derivative_decomposed(s: complex | mp.mpc) -> mp.mpc:
    """Exact logarithmic derivative including endpoint, gamma, and zeta terms."""
    z = mp.mpc(s)
    return (
        1 / z
        + 1 / (z - 1)
        - mp.log(mp.pi) / 2
        + mp.digamma(z / 2) / 2
        + mp.diff(mp.zeta, z) / mp.zeta(z)
    )


def horizontal_phase_current(s: complex | mp.mpc) -> mp.mpf:
    """tau(s) = d/dsigma arg xi(s) = Im[xi'(s)/xi(s)]."""
    return mp.im(xi_log_derivative_direct(s))


def zero_product_current(
    sigma: float, t: float, beta: float, gamma: float
) -> float:
    """Natural current from the same-height reflected zero product.

    The pair is beta+i*gamma and 1-beta+i*gamma. The two contributions add.
    """
    y = t - gamma
    return -y / ((sigma - beta) ** 2 + y**2) - y / (
        (sigma - (1 - beta)) ** 2 + y**2
    )


def reflection_cocycle_current(
    sigma: float, t: float, beta: float, gamma: float
) -> float:
    """Antisymmetric current of the ratio of the two reflected zero factors.

    This is Im[d/ds log((s-rho)/(s-rho_star))], where rho_star=1-conj(rho).
    Unlike the product current, it is an actual asymmetry detector.
    """
    y = t - gamma
    return -y / ((sigma - beta) ** 2 + y**2) + y / (
        (sigma - (1 - beta)) ** 2 + y**2
    )


def cocycle_boundary_energy(delta: float, sigma: float = 1.0) -> float:
    """Integral over t of the squared cocycle current for beta=1/2+delta.

    For a = sigma-1/2 and 0 <= |delta| < |a|,

        integral_R A(t)^2 dt = pi*delta^2 / (a*(a^2-delta^2)).

    At Casey's boundary sigma=1 this is 8*pi*delta^2/(1-4*delta^2).
    """
    a = sigma - 0.5
    d = abs(delta)
    if a <= 0 or d >= a:
        raise ValueError("require sigma>1/2 and |delta|<sigma-1/2")
    return math.pi * d * d / (a * (a * a - d * d))


def numerical_cocycle_energy(
    delta: float, gamma: float = 14.0, sigma: float = 1.0
) -> mp.mpf:
    beta = 0.5 + delta
    f: Callable[[mp.mpf], mp.mpf] = lambda t: reflection_cocycle_current(
        sigma, float(t), beta, gamma
    ) ** 2
    return mp.quad(f, [-mp.inf, gamma, mp.inf])


def contour_points(
    left: float,
    right: float,
    bottom: float,
    top: float,
    samples_per_unit: int = 100,
) -> list[mp.mpc]:
    """Counterclockwise rectangle, excluding a duplicate endpoint per edge."""

    def segment(a: mp.mpc, b: mp.mpc, n: int) -> list[mp.mpc]:
        return [a + (b - a) * k / n for k in range(n)]

    nx = max(40, int((right - left) * samples_per_unit))
    ny = max(80, int((top - bottom) * samples_per_unit))
    p0 = mp.mpc(left, bottom)
    p1 = mp.mpc(right, bottom)
    p2 = mp.mpc(right, top)
    p3 = mp.mpc(left, top)
    points = (
        segment(p0, p1, nx)
        + segment(p1, p2, ny)
        + segment(p2, p3, nx)
        + segment(p3, p0, ny)
    )
    points.append(points[0])
    return points


def xi_winding_number(
    left: float, right: float, bottom: float, top: float
) -> int:
    """Numerical argument-principle count for a zero-free contour."""
    points = contour_points(left, right, bottom, top)
    args = [float(mp.arg(completed_xi(z))) for z in points]
    total = 0.0
    for a, b in zip(args, args[1:]):
        step = b - a
        while step <= -math.pi:
            step += 2 * math.pi
        while step > math.pi:
            step -= 2 * math.pi
        total += step
    return int(round(total / (2 * math.pi)))


def build_certificate() -> dict[str, Any]:
    mp.mp.dps = 50

    boundary_samples = {}
    decomposition_errors = {}
    for t in (0.1, 1.0, 5.0, 10.0, 14.0, 20.0, 30.0):
        s = mp.mpc(1, t)
        boundary_samples[str(t)] = mp.nstr(horizontal_phase_current(s), 24)
        decomposition_errors[str(t)] = mp.nstr(
            abs(xi_log_derivative_direct(s) - xi_log_derivative_decomposed(s)),
            8,
        )

    delta = 0.2
    analytic_energy = cocycle_boundary_energy(delta)
    numeric_energy = numerical_cocycle_energy(delta)
    critical_product_current = zero_product_current(1.0, 0.0, 0.5, 14.0)
    critical_cocycle_current = reflection_cocycle_current(1.0, 0.0, 0.5, 14.0)

    winding = xi_winding_number(0.1, 0.9, 10.0, 18.0)

    checks = {
        "completed_xi_reflection": abs(
            completed_xi(mp.mpc("0.31", "3.7"))
            - completed_xi(1 - mp.mpc("0.31", "3.7"))
        )
        < mp.mpf("1e-40"),
        "log_derivative_decomposition": max(
            mp.mpf(value) for value in decomposition_errors.values()
        )
        < mp.mpf("1e-35"),
        "casey_pointwise_boundary_zero_is_false": any(
            abs(mp.mpf(value)) > mp.mpf("1e-6")
            for value in boundary_samples.values()
        ),
        "natural_product_current_nonzero_even_at_delta_zero": abs(
            critical_product_current
        )
        > 1e-12,
        "reflection_cocycle_zero_at_delta_zero": abs(critical_cocycle_current)
        < 1e-12,
        "positive_energy_matches_closed_form": abs(numeric_energy - analytic_energy)
        < mp.mpf("1e-10"),
        "argument_principle_counts_first_zero": winding == 1,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "Casey phase-current reconstruction and W33-compatible defect energy",
        "rigorous_replacements": {
            "pole_regularization": "use completed xi; xi(0)=xi(1)=1/2",
            "phase_torque": "tau(s)=Im[xi'(s)/xi(s)] away from zeros",
            "global_phase_law": "(2*pi)^-1 contour integral xi'/xi counts zeros",
            "asymmetry_detector": (
                "reflection-cocycle current from the ratio of reflected zero factors"
            ),
            "no_cancellation_detector": "integrate the square orbit by orbit",
        },
        "boundary_phase_current_samples_sigma_1": boundary_samples,
        "log_derivative_decomposition_errors": decomposition_errors,
        "local_pair_audit": {
            "delta_zero_product_current": critical_product_current,
            "delta_zero_cocycle_current": critical_cocycle_current,
            "delta": delta,
            "analytic_boundary_energy": analytic_energy,
            "numeric_boundary_energy": mp.nstr(numeric_energy, 24),
            "closed_form_sigma_1": "8*pi*delta^2/(1-4*delta^2)",
            "energy_zero_iff_delta_zero": True,
        },
        "argument_principle": {
            "rectangle": {
                "left": 0.1,
                "right": 0.9,
                "bottom": 10.0,
                "top": 18.0,
            },
            "winding_number": winding,
            "interpretation": "one nontrivial xi zero lies in this rectangle",
        },
        "claim_boundary": {
            "proved": [
                "the completed xi regularizes the zeta pole",
                "the phase current and contour winding are rigorous",
                "the cocycle energy is positive and detects one off-line orbit",
            ],
            "not_proved": [
                "that the total classical cocycle energy vanishes",
                "that compactification imposes pointwise zero current at sigma=1",
                "that the W33 graph determinant equals the classical xi determinant",
            ],
            "combined_frontier": (
                "derive a classical trace or positivity identity forcing the weighted "
                "sum of orbit energies to vanish; W33 supplies the exact finite model"
            ),
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_casey_phase_current_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
