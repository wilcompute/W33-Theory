"""Poisson-Kemeny Green kernel for W(3,3).

MCXLVI computes the exact random-walk Poisson kernel
Z=(I-P+Pi)^{-1} for P=A/12 and Pi=J/40.  The centered kernel Z-Pi carries
Kemeny's constant on the diagonal and gives exact adjacent/nonedge hitting
times and effective resistances.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_walk_inverse_shell_normalization import (  # noqa: E402
    walk_inverse_shell_normalization_packet,
)


def _exact(value: Fraction | int) -> dict[str, object]:
    fraction = Fraction(value)
    return {
        "fraction": str(fraction),
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "float": float(fraction),
    }


def _packet_fraction(entry: dict[str, object]) -> Fraction:
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def poisson_kemeny_green_kernel_packet() -> dict[str, object]:
    """Return exact shell data for Z=(I-P+Pi)^{-1} and Z-Pi."""
    walk = walk_inverse_shell_normalization_packet()
    floor = _packet_fraction(walk["parameters"]["floor"])

    q = int(walk["parameters"]["q"])
    v = int(walk["parameters"]["v"])
    k = int(walk["parameters"]["k"])
    nonneighbors = int(walk["parameters"]["nonneighbors"])
    edges = v * k // 2
    nonedge_pairs = v * nonneighbors // 2
    stationary = Fraction(1, v)

    ev_positive = Fraction(1, 6)
    ev_negative = Fraction(-1, 3)
    poisson_positive = Fraction(1, 1) / (1 - ev_positive)
    poisson_negative = Fraction(1, 1) / (1 - ev_negative)
    multiplicities = {"stationary": 1, "positive": 24, "negative": 15}

    coeff_i = Fraction(21, 20)
    coeff_a = Fraction(3, 40)
    coeff_j = Fraction(-19, 800)
    centered_coeff_j = coeff_j - stationary

    z_diag = coeff_i + coeff_j
    z_adjacent = coeff_a + coeff_j
    z_nonedge = coeff_j
    z_row_sum = z_diag + k * z_adjacent + nonneighbors * z_nonedge

    centered_diag = z_diag - stationary
    centered_adjacent = z_adjacent - stationary
    centered_nonedge = z_nonedge - stationary
    centered_row_sum = centered_diag + k * centered_adjacent + nonneighbors * centered_nonedge

    kemeny = (
        multiplicities["positive"] * poisson_positive
        + multiplicities["negative"] * poisson_negative
    )
    trace_z = 1 + kemeny
    trace_centered = kemeny

    hitting_adjacent = v * (z_diag - z_adjacent)
    hitting_nonedge = v * (z_diag - z_nonedge)
    commute_adjacent = 2 * hitting_adjacent
    commute_nonedge = 2 * hitting_nonedge
    resistance_adjacent = Fraction(commute_adjacent, 2 * edges)
    resistance_nonedge = Fraction(commute_nonedge, 2 * edges)
    kirchhoff_index = edges * resistance_adjacent + nonedge_pairs * resistance_nonedge

    return {
        "parameters": {
            "q": q,
            "v": v,
            "k": k,
            "floor": _exact(floor),
            "stationary_entry": _exact(stationary),
            "edges": edges,
            "nonedge_pairs": nonedge_pairs,
        },
        "poisson_spectrum": {
            "P_eigenvalues": {
                "stationary": _exact(Fraction(1, 1)),
                "positive": _exact(ev_positive),
                "negative": _exact(ev_negative),
            },
            "Z_eigenvalues": {
                "stationary": _exact(Fraction(1, 1)),
                "positive": _exact(poisson_positive),
                "negative": _exact(poisson_negative),
            },
            "centered_Z_minus_Pi_eigenvalues": {
                "stationary": _exact(Fraction(0, 1)),
                "positive": _exact(poisson_positive),
                "negative": _exact(poisson_negative),
            },
            "multiplicities": multiplicities,
        },
        "poisson_kernel": {
            "formula": "Z = (I - P + Pi)^-1 = 21I/20 + 3A/40 - 19J/800",
            "coefficients": {
                "I": _exact(coeff_i),
                "A": _exact(coeff_a),
                "J": _exact(coeff_j),
            },
            "entry_values": {
                "diagonal": _exact(z_diag),
                "adjacent": _exact(z_adjacent),
                "nonedge": _exact(z_nonedge),
            },
            "shell_row_sum": _exact(z_row_sum),
            "trace": _exact(trace_z),
        },
        "centered_poisson_kernel": {
            "formula": "Z - Pi = 21I/20 + 3A/40 - 39J/800",
            "coefficients": {
                "I": _exact(coeff_i),
                "A": _exact(coeff_a),
                "J": _exact(centered_coeff_j),
            },
            "entry_values": {
                "diagonal": _exact(centered_diag),
                "adjacent": _exact(centered_adjacent),
                "nonedge": _exact(centered_nonedge),
            },
            "shell_row_sum": _exact(centered_row_sum),
            "trace": _exact(trace_centered),
            "diagonal_equals_kemeny_per_vertex": centered_diag == kemeny / v,
            "row_sum_equation": "801/800 + 12*(21/800) + 27*(-39/800) = 0",
        },
        "kemeny": {
            "constant": _exact(kemeny),
            "trace_Z_minus_one": _exact(trace_z - 1),
            "per_vertex": _exact(kemeny / v),
            "formula": "24*(6/5) + 15*(3/4) = 801/20",
        },
        "hitting_times": {
            "adjacent": _exact(hitting_adjacent),
            "nonedge": _exact(hitting_nonedge),
            "nonedge_minus_adjacent": _exact(hitting_nonedge - hitting_adjacent),
            "nonedge_minus_adjacent_equals_q": hitting_nonedge - hitting_adjacent == q,
            "formula": "H_ij = v*(Z_jj - Z_ij)",
        },
        "commute_and_resistance": {
            "commute_adjacent": _exact(commute_adjacent),
            "commute_nonedge": _exact(commute_nonedge),
            "effective_resistance_adjacent": _exact(resistance_adjacent),
            "effective_resistance_nonedge": _exact(resistance_nonedge),
            "kirchhoff_index": _exact(kirchhoff_index),
            "kirchhoff_from_shell_counts": (
                kirchhoff_index
                == edges * resistance_adjacent + nonedge_pairs * resistance_nonedge
                == Fraction(267, 2)
            ),
        },
        "claim_boundary": (
            "finite W33 random-walk Poisson/Kemeny kernel and hitting-resistance identity; "
            "not a continuum stochastic-process limit"
        ),
        "poisson_kemeny_green_kernel_detected": (
            z_row_sum == 1
            and centered_row_sum == 0
            and trace_z == Fraction(821, 20)
            and kemeny == Fraction(801, 20)
            and centered_diag == kemeny / v
            and hitting_adjacent == 39
            and hitting_nonedge == 42
            and resistance_adjacent == Fraction(13, 80)
            and resistance_nonedge == Fraction(7, 40)
            and kirchhoff_index == Fraction(267, 2)
        ),
    }


def main() -> None:
    packet = poisson_kemeny_green_kernel_packet()
    payload = {
        "theorem": "Poisson-Kemeny Green kernel",
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_poisson_kemeny_green_kernel.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "kemeny_constant": packet["kemeny"]["constant"],
        "centered_diagonal": packet["centered_poisson_kernel"]["entry_values"]["diagonal"],
        "hitting_adjacent": packet["hitting_times"]["adjacent"],
        "hitting_nonedge": packet["hitting_times"]["nonedge"],
        "effective_resistance_adjacent": packet["commute_and_resistance"][
            "effective_resistance_adjacent"
        ],
        "effective_resistance_nonedge": packet["commute_and_resistance"][
            "effective_resistance_nonedge"
        ],
        "kirchhoff_index": packet["commute_and_resistance"]["kirchhoff_index"],
        "poisson_kemeny_green_kernel_detected": packet["poisson_kemeny_green_kernel_detected"],
        "claim_boundary": packet["claim_boundary"],
    }
    result_path = ROOT / "PART_MCXLVI_poisson_kemeny_green_kernel_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXLVI Poisson-Kemeny Green Kernel ===")
    print(
        f"K={packet['kemeny']['constant']['fraction']}, "
        f"H_adj={packet['hitting_times']['adjacent']['fraction']}, "
        f"H_non={packet['hitting_times']['nonedge']['fraction']}, "
        f"R={packet['commute_and_resistance']['effective_resistance_adjacent']['fraction']}/"
        f"{packet['commute_and_resistance']['effective_resistance_nonedge']['fraction']}"
    )


if __name__ == "__main__":
    main()
