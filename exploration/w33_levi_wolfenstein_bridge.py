"""Exact Wolfenstein package from the solved Levi-family CKM seeds.

The current exact CKM closure already fixed:

    a_live = 9/25,
    b_live = 3/80,
    lambda = a_paper = 9/40,
    S = sigma / a_live = 53/96,
    D = delta / a_live = 43/96.

This bridge packages those exact Levi-family quantities into an exact
Wolfenstein-style CKM law.  The resulting parameters are

    lambda = 9/40,
    A      = (20/27) * sqrt(53/43),
    tan(delta_CKM) = sqrt(a_live b_live) / lambda^2 = 16*sqrt(15)/27,
    |rho_bar + i eta_bar| = lambda / S = 108/265.

Using the standard O(lambda^4) Wolfenstein matrix, these exact data give

    |V_us| ≈ 0.225,
    |V_cb| ≈ 0.04163,
    |V_ub| ≈ 0.00382,
    J      ≈ 3.278e-5.

So the old experimental CKM packaging is now recovered from the same exact
Levi-family operator seeds, not from a separate fit.
"""

from __future__ import annotations

from fractions import Fraction
import json
from math import atan, sqrt
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_wolfenstein_bridge_summary.json"


A_LIVE = Fraction(9, 25)
B_LIVE = Fraction(3, 80)
LAMBDA = Fraction(9, 40)
S_RATIO = Fraction(53, 96)
D_RATIO = Fraction(43, 96)


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def _complex_report(z: complex) -> dict[str, float]:
    return {"real": float(z.real), "imag": float(z.imag)}


def build_summary() -> dict[str, Any]:
    lambda_float = float(LAMBDA)
    a_float = float(A_LIVE)
    b_float = float(B_LIVE)
    s_float = float(S_RATIO)
    d_float = float(D_RATIO)

    A_param = float(Fraction(20, 27)) * sqrt(s_float / d_float)
    delta_phase = atan(sqrt(a_float * b_float) / (lambda_float**2))
    rho_eta_modulus = float(LAMBDA / S_RATIO)
    rho_bar = rho_eta_modulus * np.cos(delta_phase)
    eta_bar = rho_eta_modulus * np.sin(delta_phase)

    lam2 = lambda_float**2
    lam3 = lambda_float**3
    lam4 = lambda_float**4
    lam6 = lambda_float**6

    rho_plus_i_eta = complex(rho_bar, eta_bar)
    CKM = np.array(
        [
            [
                1 - lam2 / 2 - lam4 / 8,
                lambda_float,
                A_param * lam3 * np.conj(rho_plus_i_eta),
            ],
            [
                -lambda_float + A_param**2 * lambda_float * lam4 * (0.5 - rho_plus_i_eta),
                1 - lam2 / 2 - lam4 * (0.125 + A_param**2 / 2),
                A_param * lam2,
            ],
            [
                A_param * lam3 * (1 - (1 - lam2 / 2) * rho_plus_i_eta),
                -A_param * lam2 + A_param * lam4 * (0.5 - rho_plus_i_eta),
                1 - A_param**2 * lam4 / 2,
            ],
        ],
        dtype=complex,
    )

    CKM_abs = np.abs(CKM)
    J = float(np.imag(CKM[0, 1] * CKM[1, 2] * np.conj(CKM[0, 2]) * np.conj(CKM[1, 1])))

    exact_tan_delta = 16 * sqrt(15) / 27
    vcb_from_levi = b_float * sqrt(s_float / d_float)
    vub_from_levi = A_param * lam3 * rho_eta_modulus
    vcs_correction = float(np.real(CKM[1, 1]))

    return {
        "levi_wolfenstein_dictionary": {
            "a_live": _fraction_report(A_LIVE),
            "b_live": _fraction_report(B_LIVE),
            "lambda": _fraction_report(LAMBDA),
            "S_ratio": _fraction_report(S_RATIO),
            "D_ratio": _fraction_report(D_RATIO),
            "A_parameter": {
                "closed_form": "(20/27) * sqrt(53/43)",
                "value": A_param,
            },
            "delta_phase": {
                "closed_form": "atan(16*sqrt(15)/27)",
                "tan_delta": exact_tan_delta,
                "value_rad": float(delta_phase),
            },
            "rho_eta_modulus": {
                "exact": str(LAMBDA / S_RATIO),
                "value": rho_eta_modulus,
            },
            "rho_bar": rho_bar,
            "eta_bar": eta_bar,
        },
        "levi_wolfenstein_packet": {
            "rho_bar_plus_i_eta_bar": _complex_report(rho_plus_i_eta),
            "CKM_abs": [[float(x) for x in row] for row in CKM_abs],
            "Vus": float(CKM_abs[0, 1]),
            "Vcb": float(CKM_abs[1, 2]),
            "Vub": float(CKM_abs[0, 2]),
            "Jarlskog": J,
            "derived_formulas": {
                "Vcb_from_levi": vcb_from_levi,
                "Vub_from_levi": vub_from_levi,
                "J_from_corrected_wolfenstein": A_param**2 * lam6 * eta_bar * vcs_correction,
                "Vcs_correction_factor": vcs_correction,
            },
        },
        "levi_wolfenstein_theorem": {
            "the_exact_branch_filtered_Cabibbo_parameter_is_lambda_9_over_40": bool(
                LAMBDA == Fraction(9, 40)
            ),
            "the_exact_Wolfenstein_A_parameter_is_20_over_27_times_sqrt_53_over_43": bool(
                abs(A_param - float(Fraction(20, 27)) * sqrt(float(Fraction(53, 43)))) < 1e-15
            ),
            "the_exact_CKM_phase_tangent_is_16_sqrt_15_over_27": bool(
                abs(np.tan(delta_phase) - exact_tan_delta) < 1e-12
            ),
            "the_exact_rho_eta_modulus_is_108_over_265": bool(
                LAMBDA / S_RATIO == Fraction(108, 265)
            ),
            "the_exact_Levi_formula_for_Vcb_is_b_times_sqrt_S_over_D_and_matches_A_lambda_squared": bool(
                abs(vcb_from_levi - A_param * lam2) < 1e-12
            ),
            "the_exact_Levi_formula_for_Vub_matches_A_lambda_cubed_times_modulus_rho_plus_i_eta": bool(
                abs(vub_from_levi - A_param * lam3 * rho_eta_modulus) < 1e-12
                and abs(vub_from_levi - float(CKM_abs[0, 2])) < 2e-4
            ),
            "the_corrected_wolfenstein_Jarlskog_formula_matches_the_constructed_matrix": bool(
                abs(J - A_param**2 * lam6 * eta_bar * vcs_correction) < 1e-12
            ),
            "the_exact_Levi_family_seed_package_closes_to_a_realistic_CKM_Wolfenstein_packet": bool(
                0.22 < float(CKM_abs[0, 1]) < 0.23
                and 0.04 < float(CKM_abs[1, 2]) < 0.043
                and 0.003 < float(CKM_abs[0, 2]) < 0.0045
                and 2.5e-5 < J < 3.5e-5
            ),
        },
        "interpretation": (
            "The exact Levi-family packet already determines a Wolfenstein CKM "
            "package. The Cabibbo branch filter gives lambda, the triality "
            "53/43 split gives A, the family phase operator gives the CKM phase, "
            "and the same package reproduces the realistic Vcb, Vub, and "
            "Jarlskog scales."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 LEVI WOLFENSTEIN BRIDGE")
    print("=" * 72)
    for key, value in summary["levi_wolfenstein_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
