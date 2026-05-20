"""Green moment and condition ladder for W(3,3).

MCXLIV lifts the MCXLIII adjacency Green-kernel packet from entrywise
reciprocity to global moments.  After scaling by the corrected floor, the
total Green mass, trace mass, and inverse Frobenius energy become the exact
integer ladder 40, 100, 1000.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_green_kernel_floor_reciprocity import (  # noqa: E402
    green_kernel_floor_reciprocity_packet,
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


def green_moment_condition_ladder_packet() -> dict[str, object]:
    """Return exact floor-scaled Green moments and condition numbers."""
    green = green_kernel_floor_reciprocity_packet()

    params = green["parameters"]
    spectrum = green["spectrum"]
    floor = _packet_fraction(green["floor_equalities"]["mcxli_mcxlii_floor"])
    total_mass = _packet_fraction(green["trace_data"]["total_entry_sum"])
    trace_mass = _packet_fraction(green["trace_data"]["trace_A_inverse"])
    inverse_frobenius_square = _packet_fraction(
        green["trace_data"]["frobenius_square_trace_A_inverse_squared"]
    )

    q = int(params["q"])
    v = int(params["v"])
    k = int(params["k"])
    eig = spectrum["eigenvalues"]
    mult = spectrum["multiplicities"]

    adjacency_frobenius_square = sum(
        int(mult[name]) * int(eig[name]) * int(eig[name]) for name in ("k", "r", "s")
    )
    singular_values = [abs(int(eig[name])) for name in ("k", "r", "s")]
    cond2 = Fraction(max(singular_values), min(singular_values))
    frobenius_condition_square = Fraction(adjacency_frobenius_square) * inverse_frobenius_square

    total_over_floor = total_mass / floor
    trace_over_floor = trace_mass / floor
    inverse_frobenius_over_floor_square = inverse_frobenius_square / (floor * floor)
    inverse_frobenius_over_floor_trace = inverse_frobenius_square / (floor * trace_mass)
    inverse_frobenius_over_floor_total = inverse_frobenius_square / (floor * total_mass)

    return {
        "parameters": {
            "q": q,
            "v": v,
            "k": k,
            "floor": _exact(floor),
        },
        "green_moments": {
            "total_entry_sum": _exact(total_mass),
            "trace_A_inverse": _exact(trace_mass),
            "inverse_frobenius_square": _exact(inverse_frobenius_square),
            "trace_over_total": _exact(trace_mass / total_mass),
            "total_equals_v_floor": total_mass == v * floor,
            "trace_equals_100_floor": trace_mass == 100 * floor,
            "frobenius_square_equals_1000_floor_squared": (
                inverse_frobenius_square == 1000 * floor * floor
            ),
        },
        "floor_scaled_ladder": {
            "total_over_floor": _exact(total_over_floor),
            "trace_over_floor": _exact(trace_over_floor),
            "inverse_frobenius_over_floor_square": _exact(inverse_frobenius_over_floor_square),
            "positive_integer_ladder": [
                int(total_over_floor),
                int(trace_over_floor),
                int(inverse_frobenius_over_floor_square),
            ],
            "trace_is_five_halves_total": trace_mass == Fraction(5, 2) * total_mass,
            "inverse_frobenius_is_ten_floor_trace": (
                inverse_frobenius_square == (k - 2) * floor * trace_mass
            ),
            "inverse_frobenius_is_twenty_five_floor_total": (
                inverse_frobenius_square == (q * q - 4) ** 2 * floor * total_mass
            ),
            "inverse_frobenius_over_floor_trace": _exact(inverse_frobenius_over_floor_trace),
            "inverse_frobenius_over_floor_total": _exact(inverse_frobenius_over_floor_total),
        },
        "adjacency_dual": {
            "adjacency_frobenius_square": _exact(Fraction(adjacency_frobenius_square)),
            "adjacency_frobenius_square_equals_v_over_floor": (
                adjacency_frobenius_square == v / floor
            ),
            "adjacency_frobenius_square_times_floor": _exact(adjacency_frobenius_square * floor),
        },
        "conditioning": {
            "spectral_condition_number": _exact(cond2),
            "spectral_condition_number_is_one_over_two_floor": cond2 == Fraction(1, 2 * floor),
            "spectral_condition_number_times_floor": _exact(cond2 * floor),
            "frobenius_condition_square": _exact(frobenius_condition_square),
            "q_scaled_frobenius_condition_square": _exact(q * frobenius_condition_square),
            "q_scaled_frobenius_condition_square_equals_trace_ratio_square": (
                q * frobenius_condition_square == trace_over_floor * trace_over_floor
            ),
        },
        "claim_boundary": (
            "finite W33 Green-kernel moment and conditioning identity; "
            "not a continuum analytic estimate by itself"
        ),
        "green_moment_condition_ladder_detected": (
            total_over_floor == 40
            and trace_over_floor == 100
            and inverse_frobenius_over_floor_square == 1000
            and inverse_frobenius_over_floor_trace == k - 2
            and inverse_frobenius_over_floor_total == (q * q - 4) ** 2
            and adjacency_frobenius_square == v / floor
            and cond2 == Fraction(1, 2 * floor)
            and q * frobenius_condition_square == trace_over_floor * trace_over_floor
        ),
    }


def main() -> None:
    packet = green_moment_condition_ladder_packet()
    payload = {
        "theorem": "Green moment condition ladder",
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_green_moment_condition_ladder.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "floor": packet["parameters"]["floor"],
        "positive_integer_ladder": packet["floor_scaled_ladder"]["positive_integer_ladder"],
        "total_entry_sum": packet["green_moments"]["total_entry_sum"],
        "trace_A_inverse": packet["green_moments"]["trace_A_inverse"],
        "inverse_frobenius_square": packet["green_moments"]["inverse_frobenius_square"],
        "spectral_condition_number": packet["conditioning"]["spectral_condition_number"],
        "frobenius_condition_square": packet["conditioning"]["frobenius_condition_square"],
        "green_moment_condition_ladder_detected": packet["green_moment_condition_ladder_detected"],
        "claim_boundary": packet["claim_boundary"],
    }
    result_path = ROOT / "PART_MCXLIV_green_moment_condition_ladder_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXLIV Green Moment Condition Ladder ===")
    print(
        f"floor={packet['parameters']['floor']['fraction']}, "
        f"ladder={packet['floor_scaled_ladder']['positive_integer_ladder']}, "
        f"cond2={packet['conditioning']['spectral_condition_number']['fraction']}"
    )


if __name__ == "__main__":
    main()
