"""Walk-inverse shell normalization for W(3,3).

MCXLV normalizes the MCXLIII/MCXLIV Green kernel by the random-walk matrix
P=A/12.  Since P^{-1}=12A^{-1}, the floor-scaled Green moments become raw
walk-inverse moments and the shell entries collapse to 5/2, 1, -1/2.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_green_moment_condition_ladder import (  # noqa: E402
    green_moment_condition_ladder_packet,
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


def walk_inverse_shell_normalization_packet() -> dict[str, object]:
    """Return exact shell data for P^{-1}, where P=A/12."""
    ladder = green_moment_condition_ladder_packet()
    floor = _packet_fraction(ladder["parameters"]["floor"])

    q = int(ladder["parameters"]["q"])
    v = int(ladder["parameters"]["v"])
    k = int(ladder["parameters"]["k"])
    nonneighbors = v - k - 1

    # P^{-1}=k A^{-1}; equivalently 2P^{-1}=6I+3A-J.
    diag = Fraction(5, 2)
    adjacent = Fraction(1, 1)
    nonedge = Fraction(-1, 2)
    adjacent_shell = k * adjacent
    nonedge_shell = nonneighbors * nonedge
    row_sum = diag + adjacent_shell + nonedge_shell

    trace = v * diag
    total_sum = v * row_sum
    inverse_frobenius_square = (
        diag * diag + k * adjacent * adjacent + nonneighbors * nonedge * nonedge
    ) * v

    spectrum_inverse = {"trivial": 1, "positive": 6, "negative": -3}
    multiplicities = {"trivial": 1, "positive": 24, "negative": 15}
    spectral_trace = sum(
        multiplicities[name] * spectrum_inverse[name] for name in spectrum_inverse
    )
    spectral_frobenius_square = sum(
        multiplicities[name] * spectrum_inverse[name] * spectrum_inverse[name]
        for name in spectrum_inverse
    )

    raw_ladder = [
        int(_packet_fraction(ladder["floor_scaled_ladder"]["total_over_floor"])),
        int(_packet_fraction(ladder["floor_scaled_ladder"]["trace_over_floor"])),
        int(_packet_fraction(ladder["floor_scaled_ladder"]["inverse_frobenius_over_floor_square"])),
    ]
    walk_ladder = [int(total_sum), int(trace), int(inverse_frobenius_square)]

    return {
        "parameters": {
            "q": q,
            "v": v,
            "k": k,
            "floor": _exact(floor),
            "nonneighbors": nonneighbors,
        },
        "normalization": {
            "transition_matrix": "P = A/12",
            "inverse_relation": "P^-1 = 12 A^-1",
            "integer_scaled_relation": "2 P^-1 = 6I + 3A - J",
            "inverse_identity": "P(6I + 3A - J) = 2I",
            "floor_recovered_as_adjacent_entry_over_k": floor == adjacent / k,
        },
        "entry_values": {
            "diagonal": _exact(diag),
            "adjacent": _exact(adjacent),
            "nonedge": _exact(nonedge),
            "twice_diagonal": _exact(2 * diag),
            "twice_adjacent": _exact(2 * adjacent),
            "twice_nonedge": _exact(2 * nonedge),
        },
        "shell_contributions": {
            "diagonal": _exact(diag),
            "adjacent_shell": _exact(adjacent_shell),
            "nonedge_shell": _exact(nonedge_shell),
            "row_sum": _exact(row_sum),
            "row_sum_equation": "5/2 + 12*1 + 27*(-1/2) = 1",
        },
        "raw_walk_inverse_moments": {
            "total_entry_sum": _exact(total_sum),
            "trace_P_inverse": _exact(trace),
            "frobenius_square_P_inverse": _exact(inverse_frobenius_square),
            "positive_integer_ladder": walk_ladder,
            "equals_mcxliv_floor_scaled_ladder": walk_ladder == raw_ladder,
        },
        "spectrum": {
            "P_eigenvalues": {
                "trivial": _exact(Fraction(1, 1)),
                "positive": _exact(Fraction(1, 6)),
                "negative": _exact(Fraction(-1, 3)),
            },
            "P_inverse_eigenvalues": {
                "trivial": _exact(Fraction(spectrum_inverse["trivial"])),
                "positive": _exact(Fraction(spectrum_inverse["positive"])),
                "negative": _exact(Fraction(spectrum_inverse["negative"])),
            },
            "multiplicities": multiplicities,
            "spectral_trace": _exact(Fraction(spectral_trace)),
            "spectral_frobenius_square": _exact(Fraction(spectral_frobenius_square)),
            "spectral_moments_match_shell_moments": (
                spectral_trace == trace and spectral_frobenius_square == inverse_frobenius_square
            ),
        },
        "integer_shell_kernel": {
            "kernel": "2P^-1",
            "diagonal": 5,
            "adjacent": 2,
            "nonedge": -1,
            "row_sum": 2,
            "trace": 200,
            "frobenius_square": 4000,
        },
        "claim_boundary": (
            "finite W33 random-walk inverse normalization; P^-1 is a signed inverse kernel, "
            "not a stochastic transition matrix"
        ),
        "walk_inverse_shell_normalization_detected": (
            row_sum == 1
            and total_sum == raw_ladder[0] == v
            and trace == raw_ladder[1] == 100
            and inverse_frobenius_square == raw_ladder[2] == 1000
            and walk_ladder == raw_ladder
            and floor == adjacent / k
            and spectral_trace == trace
            and spectral_frobenius_square == inverse_frobenius_square
        ),
    }


def main() -> None:
    packet = walk_inverse_shell_normalization_packet()
    payload = {
        "theorem": "Walk inverse shell normalization",
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_walk_inverse_shell_normalization.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "floor": packet["parameters"]["floor"],
        "entry_values": packet["entry_values"],
        "row_sum": packet["shell_contributions"]["row_sum"],
        "positive_integer_ladder": packet["raw_walk_inverse_moments"]["positive_integer_ladder"],
        "integer_scaled_relation": packet["normalization"]["integer_scaled_relation"],
        "spectral_trace": packet["spectrum"]["spectral_trace"],
        "spectral_frobenius_square": packet["spectrum"]["spectral_frobenius_square"],
        "walk_inverse_shell_normalization_detected": packet[
            "walk_inverse_shell_normalization_detected"
        ],
        "claim_boundary": packet["claim_boundary"],
    }
    result_path = ROOT / "PART_MCXLV_walk_inverse_shell_normalization_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXLV Walk Inverse Shell Normalization ===")
    print(
        f"entries={packet['entry_values']['diagonal']['fraction']},"
        f"{packet['entry_values']['adjacent']['fraction']},"
        f"{packet['entry_values']['nonedge']['fraction']}; "
        f"ladder={packet['raw_walk_inverse_moments']['positive_integer_ladder']}"
    )


if __name__ == "__main__":
    main()
