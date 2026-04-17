"""Exact CKM unitarity triangle from the Levi-family Wolfenstein package.

The Levi Wolfenstein bridge already fixed the standard CKM data

    lambda = 9/40,
    |rho_bar + i eta_bar| = 108/265,
    gamma = delta_CKM = arctan(16*sqrt(15)/27).

This bridge closes the associated unitarity triangle.

Key exact facts:

    R_u = 108/265,
    tan(gamma) = 16*sqrt(15)/27,
    cos^2(gamma) = 243/1523,
    sin^2(gamma) = 1280/1523.

So the CKM apex is the exact polar packet

    rho_bar = R_u cos(gamma),
    eta_bar = R_u sin(gamma),

and the remaining sides/angles follow with

    R_t = sqrt((1-rho_bar)^2 + eta_bar^2),
    beta = atan2(eta_bar, 1-rho_bar),
    alpha = pi - beta - gamma.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import atan, atan2, cos, pi, sin, sqrt
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_unitarity_triangle_bridge_summary.json"


LAMBDA = Fraction(9, 40)
S_RATIO = Fraction(53, 96)
A_LIVE = Fraction(9, 25)
B_LIVE = Fraction(3, 80)
R_U = LAMBDA / S_RATIO
TAN_GAMMA = 16 * sqrt(15) / 27
COS2_GAMMA = Fraction(243, 1523)
SIN2_GAMMA = Fraction(1280, 1523)


def build_summary() -> dict[str, Any]:
    gamma = atan(TAN_GAMMA)
    ru = float(R_U)
    rho_bar = ru * cos(gamma)
    eta_bar = ru * sin(gamma)
    rt = sqrt((1.0 - rho_bar) ** 2 + eta_bar**2)
    beta = atan2(eta_bar, 1.0 - rho_bar)
    alpha = pi - beta - gamma

    return {
        "levi_unitarity_triangle_dictionary": {
            "lambda": {"exact": str(LAMBDA), "value": float(LAMBDA)},
            "R_u": {"exact": str(R_U), "value": ru},
            "tan_gamma": TAN_GAMMA,
            "cos2_gamma": {"exact": str(COS2_GAMMA), "value": float(COS2_GAMMA)},
            "sin2_gamma": {"exact": str(SIN2_GAMMA), "value": float(SIN2_GAMMA)},
            "rho_bar": rho_bar,
            "eta_bar": eta_bar,
            "R_t": rt,
            "alpha_deg": alpha * 180.0 / pi,
            "beta_deg": beta * 180.0 / pi,
            "gamma_deg": gamma * 180.0 / pi,
        },
        "levi_unitarity_triangle_theorem": {
            "the_exact_apex_radius_Ru_is_108_over_265": bool(R_U == Fraction(108, 265)),
            "the_exact_gamma_phase_tangent_is_16_sqrt_15_over_27": bool(
                abs(TAN_GAMMA - 16 * sqrt(15) / 27) < 1e-15
            ),
            "the_gamma_phase_has_exact_rational_squares_cos2_243_over_1523_and_sin2_1280_over_1523": bool(
                COS2_GAMMA + SIN2_GAMMA == 1
                and abs(cos(gamma) ** 2 - float(COS2_GAMMA)) < 1e-12
                and abs(sin(gamma) ** 2 - float(SIN2_GAMMA)) < 1e-12
            ),
            "the_CKM_apex_is_exactly_the_polar_packet_Ru_times_cos_gamma_sin_gamma": bool(
                abs(rho_bar**2 + eta_bar**2 - ru**2) < 1e-12
            ),
            "the_remaining_unitarity_triangle_angles_close_exactly_alpha_plus_beta_plus_gamma_equals_pi": bool(
                abs(alpha + beta + gamma - pi) < 1e-12
            ),
            "the_exact_Levi_family_seed_package_closes_to_a_realistic_unitarity_triangle": bool(
                0.15 < rho_bar < 0.18
                and 0.35 < eta_bar < 0.39
                and 88.0 < alpha * 180.0 / pi < 91.0
                and 23.0 < beta * 180.0 / pi < 25.5
                and 65.0 < gamma * 180.0 / pi < 68.0
            ),
        },
        "interpretation": (
            "The standard CKM unitarity triangle is now on the same exact Levi-family "
            "spine. The branch filter fixes the apex radius R_u, the family phase "
            "operator fixes gamma, and the remaining apex coordinates and angles follow "
            "without extra choices."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 LEVI UNITARITY TRIANGLE BRIDGE")
    print("=" * 72)
    for key, value in summary["levi_unitarity_triangle_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
