"""Horizon parity floor duality.

MCXLII connects the corrected MCXLI substrate floor to older exact horizon
parity and zeta facts.  The packet is finite arithmetic: it proves that the
same rational floor 1/12 appears as horizon redundancy, normalized chiral
discriminant density, and the absolute value of zeta(-1).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_cross_branch_gap_normalization_spine import (  # noqa: E402
    cross_branch_gap_normalization_packet,
)


def _exact(value: Fraction | int) -> dict[str, object]:
    fraction = Fraction(value)
    return {
        "fraction": str(fraction),
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "float": float(fraction),
    }


def horizon_parity_floor_duality_packet() -> dict[str, object]:
    """Return the exact horizon-parity dual of the MCXLI substrate floor."""
    edge_payload = json.loads((ROOT / "data" / "w33_edge_horizon_parity_code.json").read_text(encoding="utf-8"))
    spine = cross_branch_gap_normalization_packet()

    q = 3
    k = 12
    horizon_total = int(edge_payload["summary"]["horizon_total"])
    payload_edges = int(edge_payload["summary"]["data_payload_edges"])
    parity_symbols = int(edge_payload["summary"]["parity_symbols"])
    rate = Fraction(payload_edges, horizon_total)
    redundancy = Fraction(parity_symbols, horizon_total)

    chiral_discriminant = horizon_total * horizon_total * parity_symbols
    normalized_chiral_density = Fraction(chiral_discriminant, horizon_total**3)
    zeta_minus_one = Fraction(-1, k)
    ym_floor = Fraction(
        int(spine["ym_floor"]["p2_floor"]["numerator"]),
        int(spine["ym_floor"]["p2_floor"]["denominator"]),
    )
    ns_decay = Fraction(
        int(spine["navier_stokes"]["enstrophy_decay_rate_2nu_delta"]["numerator"]),
        int(spine["navier_stokes"]["enstrophy_decay_rate_2nu_delta"]["denominator"]),
    )

    pure_edges = int(edge_payload["grid_split"]["pure_edges"])
    corrected_mixed = int(edge_payload["grid_split"]["corrected_mixed"])
    floor_equals = redundancy == normalized_chiral_density == -zeta_minus_one == ym_floor == Fraction(1, 12)

    return {
        "horizon": {
            "total": horizon_total,
            "payload_edges": payload_edges,
            "parity_symbols": parity_symbols,
            "parity_symbols_are_q_factorial": parity_symbols == factorial(q),
            "rate": _exact(rate),
            "redundancy": _exact(redundancy),
            "rate_plus_redundancy": _exact(rate + redundancy),
            "rate_is_one_minus_floor": rate == 1 - ym_floor,
        },
        "floor_duals": {
            "ym_substrate_floor": _exact(ym_floor),
            "horizon_redundancy": _exact(redundancy),
            "normalized_chiral_discriminant_density": _exact(normalized_chiral_density),
            "absolute_zeta_minus_one": _exact(-zeta_minus_one),
            "valency_reciprocal": _exact(Fraction(1, k)),
            "all_equal": floor_equals,
        },
        "chiral_discriminant": {
            "value": chiral_discriminant,
            "closed_form": f"{horizon_total}^2 * {parity_symbols}",
            "normalized_by_horizon_cubed": _exact(normalized_chiral_density),
            "sqrt_form": f"{horizon_total} * sqrt({parity_symbols})",
        },
        "grid_split": {
            "pure_edges": pure_edges,
            "corrected_mixed": corrected_mixed,
            "floor_times_pure_edges": _exact(redundancy * pure_edges),
            "floor_times_corrected_mixed": _exact(redundancy * corrected_mixed),
            "six_floor_times_pure_edges": _exact(6 * redundancy * pure_edges),
            "six_floor_times_corrected_mixed": _exact(6 * redundancy * corrected_mixed),
            "six_floor_rescales_grid_split_integrally": (
                (6 * redundancy * pure_edges).denominator == 1
                and (6 * redundancy * corrected_mixed).denominator == 1
            ),
        },
        "cross_branch": {
            "ns_decay_over_floor": _exact(ns_decay / ym_floor),
            "ns_decay_is_two_floor": ns_decay == 2 * ym_floor,
            "horizon_redundancy_is_corrected_floor": redundancy == ym_floor,
            "payload_rate_is_chiral_rate": rate == Fraction(11, 12),
        },
        "claim_boundary": (
            "finite arithmetic duality between the corrected substrate floor, horizon parity redundancy, "
            "normalized chiral discriminant density, and zeta(-1); not a new continuum proof"
        ),
        "horizon_parity_floor_duality_detected": (
            floor_equals
            and rate == Fraction(11, 12)
            and rate + redundancy == 1
            and ns_decay == 2 * ym_floor
        ),
    }


def main() -> None:
    packet = horizon_parity_floor_duality_packet()
    payload = {
        "theorem": "Horizon parity floor duality",
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_horizon_parity_floor_duality.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "floor": packet["floor_duals"]["ym_substrate_floor"],
        "horizon_rate": packet["horizon"]["rate"],
        "horizon_redundancy": packet["horizon"]["redundancy"],
        "normalized_chiral_discriminant_density": packet["floor_duals"]["normalized_chiral_discriminant_density"],
        "absolute_zeta_minus_one": packet["floor_duals"]["absolute_zeta_minus_one"],
        "ns_decay_over_floor": packet["cross_branch"]["ns_decay_over_floor"],
        "horizon_parity_floor_duality_detected": packet["horizon_parity_floor_duality_detected"],
        "claim_boundary": packet["claim_boundary"],
    }
    result_path = ROOT / "PART_MCXLII_horizon_parity_floor_duality_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXLII Horizon Parity Floor Duality ===")
    print(
        f"floor={packet['floor_duals']['ym_substrate_floor']['fraction']}, "
        f"rate={packet['horizon']['rate']['fraction']}, "
        f"redundancy={packet['horizon']['redundancy']['fraction']}, "
        f"disc/N^3={packet['floor_duals']['normalized_chiral_discriminant_density']['fraction']}"
    )


if __name__ == "__main__":
    main()
