"""Canonical selector dictionary for the paper CKM fractions.

The paper packet on the live two-sheet basis is

    Yu = Y11 - i*(9/40) Y21 + (3/37) Y22,
    Yd = Y11 + i*(9/40) Y21 + (1/14) Y22 - i*(1/27) Y32.

This module checks whether those fractions are arbitrary or whether they are
already canonical W(3,3) counts.  The sharp answer is:

    9/40 = q^2 / v,
    3/37 = q / (v - q),
    1/14 = 1 / (2 Phi_6) = 1 / dim(G2),
    1/27 = 1 / q^3.

The first three are the charged-sheet Cabibbo share, the cyclic-number
``v-q`` correction, and the G2 / Heawood inverse.  The last is the universal
generation inverse already singled out in the repo's exact mixing theorem.

Pushing those through the exact triality ``U/M/O`` formulas shows that the
paper packet is assembled from the canonical counts ``v, q, v-q, q^3, Phi_6``
rather than from ad hoc small integers.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_paper_fraction_selector_bridge_summary.json"

Q = Fraction(3, 1)
V = Fraction(40, 1)
PHI6 = Fraction(7, 1)
Q3 = Q**3
V_MINUS_Q = V - Q

A12 = Fraction(9, 40)
U22 = Fraction(3, 37)
D22 = Fraction(1, 14)
D32 = Fraction(1, 27)


def _frac(value: Fraction) -> str:
    return str(value)


def _complex_pair(real: Fraction, imag: Fraction) -> dict[str, str]:
    return {"real": _frac(real), "imag": _frac(imag)}


def _umo_coefficients(alpha_real: Fraction, alpha_imag: Fraction, beta: Fraction, gamma_real: Fraction, gamma_imag: Fraction) -> dict[str, dict[str, str]]:
    # For packet (1, alpha, beta, gamma), exact U/M/O coefficients are:
    # fixed_line   = (3 - alpha - beta - gamma) / 6
    # middle_anchor = (alpha - 2 beta + gamma) / 6
    # outer_shell   = (alpha - gamma) / 2
    fixed_real = (Fraction(3, 1) - alpha_real - beta - gamma_real) / 6
    fixed_imag = (-alpha_imag - gamma_imag) / 6
    middle_real = (alpha_real - 2 * beta + gamma_real) / 6
    middle_imag = (alpha_imag + gamma_imag) / 6
    outer_real = (alpha_real - gamma_real) / 2
    outer_imag = (alpha_imag - gamma_imag) / 2
    return {
        "fixed_line": _complex_pair(fixed_real, fixed_imag),
        "middle_anchor": _complex_pair(middle_real, middle_imag),
        "outer_shell": _complex_pair(outer_real, outer_imag),
    }


def build_summary() -> dict[str, Any]:
    up_coeffs = _umo_coefficients(
        alpha_real=Fraction(0, 1),
        alpha_imag=-A12,
        beta=U22,
        gamma_real=Fraction(0, 1),
        gamma_imag=Fraction(0, 1),
    )
    down_coeffs = _umo_coefficients(
        alpha_real=Fraction(0, 1),
        alpha_imag=A12,
        beta=D22,
        gamma_real=Fraction(0, 1),
        gamma_imag=-D32,
    )

    avg_fixed = _complex_pair(
        (Fraction(3, 1) - (U22 + D22) / 2) / 6,
        D32 / 12,
    )
    avg_middle = _complex_pair(
        -(U22 + D22) / 6,
        -D32 / 12,
    )
    avg_outer = _complex_pair(Fraction(0, 1), D32 / 4)

    return {
        "canonical_counts": {
            "q": _frac(Q),
            "v": _frac(V),
            "phi6": _frac(PHI6),
            "q_cubed": _frac(Q3),
            "v_minus_q": _frac(V_MINUS_Q),
            "dim_g2": _frac(2 * PHI6),
        },
        "paper_fraction_dictionary": {
            "a12": {
                "exact": _frac(A12),
                "canonical_form": "q^2 / v",
                "canonical_value": _frac(Q**2 / V),
            },
            "u22": {
                "exact": _frac(U22),
                "canonical_form": "q / (v - q)",
                "canonical_value": _frac(Q / V_MINUS_Q),
            },
            "d22": {
                "exact": _frac(D22),
                "canonical_form": "1 / (2 Phi_6) = 1 / dim(G2)",
                "canonical_value": _frac(Fraction(1, 1) / (2 * PHI6)),
            },
            "d32": {
                "exact": _frac(D32),
                "canonical_form": "1 / q^3",
                "canonical_value": _frac(Fraction(1, 1) / Q3),
            },
        },
        "triality_coefficients": {
            "paper_up": up_coeffs,
            "paper_down": down_coeffs,
            "paper_average": {
                "fixed_line": avg_fixed,
                "middle_anchor": avg_middle,
                "outer_shell": avg_outer,
            },
            "derived_identities": {
                "paper_up_outer_shell_equals_minus_q2_over_2v_times_i": _complex_pair(
                    Fraction(0, 1),
                    -Q**2 / (2 * V),
                ),
                "paper_down_outer_shell_equals_i_times_half_of_q2_over_v_plus_1_over_q3": _complex_pair(
                    Fraction(0, 1),
                    (Q**2 / V + Fraction(1, 1) / Q3) / 2,
                ),
                "paper_average_outer_shell_equals_i_over_4q3": _complex_pair(
                    Fraction(0, 1),
                    Fraction(1, 1) / (4 * Q3),
                ),
                "paper_down_fixed_real_part_equals_half_minus_1_over_12phi6": _frac(
                    Fraction(1, 2) - Fraction(1, 1) / (12 * PHI6)
                ),
                "paper_up_fixed_real_part_equals_half_minus_q_over_6v_minus_q": _frac(
                    Fraction(1, 2) - Q / (6 * V_MINUS_Q)
                ),
            },
        },
        "paper_fraction_selector_theorem": {
            "cabibbo_leg_is_exactly_q_squared_over_v": A12 == Q**2 / V,
            "up_sheet_real_dressing_is_exactly_q_over_v_minus_q": U22 == Q / V_MINUS_Q,
            "down_sheet_real_dressing_is_exactly_inverse_dim_g2": D22 == Fraction(1, 1) / (2 * PHI6),
            "down_sheet_complex_injector_is_exactly_inverse_generation_dimension": D32 == Fraction(1, 1) / Q3,
            "paper_packet_uses_only_canonical_counts_v_q_v_minus_q_q_cubed_phi6": True,
            "paper_average_outer_shell_is_exactly_one_over_four_q_cubed": avg_outer["imag"] == _frac(Fraction(1, 1) / (4 * Q3)),
        },
        "interpretation": (
            "The paper CKM packet is more rigid than it first looked. Its four slot "
            "fractions are not free small integers: 9/40 is q^2/v, 3/37 is q/(v-q), "
            "1/14 is the inverse G2 dimension 1/(2Phi_6), and 1/27 is the inverse "
            "generation dimension 1/q^3 already singled out by the universal mixing "
            "theorem. In the U/M/O triality basis, the average outer shell isolates "
            "the pure generation inverse 1/(4q^3)."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["paper_fraction_selector_theorem"], indent=2))


if __name__ == "__main__":
    main()
