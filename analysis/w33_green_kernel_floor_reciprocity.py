"""Green-kernel floor reciprocity for W(3,3).

MCXLIII turns the corrected MCXLI/MCXLII floor into an adjacency Green-kernel
statement.  The theorem is finite: for the SRG(40,12,2,4) adjacency matrix,
the exact inverse has adjacent entry and row sum both equal to 1/12.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_horizon_parity_floor_duality import (  # noqa: E402
    horizon_parity_floor_duality_packet,
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


def green_kernel_floor_reciprocity_packet() -> dict[str, object]:
    """Return the exact W33 adjacency-inverse reciprocity packet."""
    horizon = horizon_parity_floor_duality_packet()
    floor = _packet_fraction(horizon["floor_duals"]["ym_substrate_floor"])

    q = 3
    v = 40
    k = 12
    lam = 2
    mu = 4
    nonneighbors = v - k - 1

    coeff_i = Fraction(1, 4)
    coeff_a = Fraction(1, 8)
    coeff_j = Fraction(-1, 24)
    diag = coeff_i + coeff_j
    adjacent = coeff_a + coeff_j
    nonedge = coeff_j

    adjacent_shell = k * adjacent
    nonedge_shell = nonneighbors * nonedge
    row_sum = diag + adjacent_shell + nonedge_shell
    trace = v * diag
    total_sum = v * row_sum
    adjacent_minus_nonedge = adjacent - nonedge
    frobenius_square = Fraction(1, k * k) + Fraction(24, 2 * 2) + Fraction(15, (-4) * (-4))

    # SRG identity: A^2 = (k-mu)I + (lambda-mu)A + mu J = 8I - 2A + 4J.
    # Therefore A(6I + 3A - J) = 6A + 3A^2 - kJ = 24I.
    scaled_i = 6
    scaled_a = 3
    scaled_j = -1
    lhs_i = scaled_a * (k - mu)
    lhs_a = scaled_i + scaled_a * (lam - mu)
    lhs_j = scaled_a * mu + scaled_j * k
    inverse_identity_verified = (lhs_i, lhs_a, lhs_j) == (24, 0, 0)

    floor_equalities = {
        "mcxli_mcxlii_floor": _exact(floor),
        "valency_reciprocal": _exact(Fraction(1, k)),
        "green_adjacent_entry": _exact(adjacent),
        "green_row_sum": _exact(row_sum),
        "all_equal": floor == Fraction(1, k) == adjacent == row_sum,
    }

    reciprocity = {
        "diagonal_over_floor": _exact(diag / floor),
        "nonedge_over_floor": _exact(nonedge / floor),
        "diagonal_is_five_halves_floor": diag == Fraction(5, 2) * floor,
        "nonedge_is_minus_half_floor": nonedge == -Fraction(1, 2) * floor,
        "adjacent_minus_nonedge": _exact(adjacent_minus_nonedge),
        "adjacent_minus_nonedge_is_1_over_2mu": adjacent_minus_nonedge == Fraction(1, 2 * mu),
        "neighbor_shell_is_unit": adjacent_shell == 1,
        "row_sum_equation": "5/24 + 12*(1/12) + 27*(-1/24) = 1/12",
    }

    return {
        "parameters": {
            "q": q,
            "v": v,
            "k": k,
            "lambda": lam,
            "mu": mu,
            "nonneighbors": nonneighbors,
        },
        "spectrum": {
            "eigenvalues": {"k": 12, "r": 2, "s": -4},
            "multiplicities": {"k": 1, "r": 24, "s": 15},
        },
        "inverse_coefficients": {
            "I": _exact(coeff_i),
            "A": _exact(coeff_a),
            "J": _exact(coeff_j),
            "formula": "A^-1 = I/4 + A/8 - J/24 = (6I + 3A - J)/24",
        },
        "integer_scaled_inverse": {
            "denominator": 24,
            "I": scaled_i,
            "A": scaled_a,
            "J": scaled_j,
            "formula": "24 A^-1 = 6I + 3A - J",
            "identity": "A(6I + 3A - J) = 24I",
            "lhs_coefficients_after_srg_reduction": {"I": lhs_i, "A": lhs_a, "J": lhs_j},
            "verified": inverse_identity_verified,
        },
        "entry_values": {
            "diagonal": _exact(diag),
            "adjacent": _exact(adjacent),
            "nonedge": _exact(nonedge),
        },
        "shell_contributions": {
            "diagonal": _exact(diag),
            "adjacent_shell": _exact(adjacent_shell),
            "nonedge_shell": _exact(nonedge_shell),
            "row_sum": _exact(row_sum),
        },
        "floor_equalities": floor_equalities,
        "reciprocity": reciprocity,
        "trace_data": {
            "trace_A_inverse": _exact(trace),
            "total_entry_sum": _exact(total_sum),
            "frobenius_square_trace_A_inverse_squared": _exact(frobenius_square),
        },
        "claim_boundary": (
            "finite W33 adjacency Green-kernel identity extending the corrected substrate floor; "
            "not a new continuum proof by itself"
        ),
        "green_kernel_floor_reciprocity_detected": (
            floor_equalities["all_equal"]
            and inverse_identity_verified
            and reciprocity["diagonal_is_five_halves_floor"]
            and reciprocity["nonedge_is_minus_half_floor"]
            and reciprocity["neighbor_shell_is_unit"]
            and trace == Fraction(25, 3)
            and total_sum == Fraction(10, 3)
        ),
    }


def main() -> None:
    packet = green_kernel_floor_reciprocity_packet()
    payload = {
        "theorem": "Green-kernel floor reciprocity",
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_green_kernel_floor_reciprocity.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "floor": packet["floor_equalities"]["mcxli_mcxlii_floor"],
        "green_adjacent_entry": packet["entry_values"]["adjacent"],
        "green_row_sum": packet["shell_contributions"]["row_sum"],
        "green_nonedge_entry": packet["entry_values"]["nonedge"],
        "integer_scaled_inverse": packet["integer_scaled_inverse"],
        "trace_A_inverse": packet["trace_data"]["trace_A_inverse"],
        "green_kernel_floor_reciprocity_detected": packet["green_kernel_floor_reciprocity_detected"],
        "claim_boundary": packet["claim_boundary"],
    }
    result_path = ROOT / "PART_MCXLIII_green_kernel_floor_reciprocity_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXLIII Green-Kernel Floor Reciprocity ===")
    print(
        f"floor={packet['floor_equalities']['mcxli_mcxlii_floor']['fraction']}, "
        f"adj={packet['entry_values']['adjacent']['fraction']}, "
        f"nonedge={packet['entry_values']['nonedge']['fraction']}, "
        f"row_sum={packet['shell_contributions']['row_sum']['fraction']}"
    )


if __name__ == "__main__":
    main()
