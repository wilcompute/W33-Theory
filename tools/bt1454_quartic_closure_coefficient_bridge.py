#!/usr/bin/env python3
"""BT1454: test the golden quartic coefficient against closure arithmetic."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1454_quartic_closure_coefficient_bridge.json"


def main() -> None:
    phi = (math.sqrt(5.0) - 1.0) / 2.0
    coeff = 4.0 - phi * phi
    half_turns = 13
    opposite_pairs = 3
    pair_sides = 2
    orientations = 2
    closure_ticks = opposite_pairs * pair_sides * orientations
    guard_bins = 2 * closure_ticks
    active_bins = closure_ticks * (half_turns + 1)
    bridge = {
        "coefficient": coeff,
        "integer_pair_core": opposite_pairs,
        "golden_tail": coeff - opposite_pairs,
        "square": coeff * coeff,
        "square_integer_core": half_turns,
        "square_golden_tail": coeff * coeff - half_turns,
        "closure_ticks": closure_ticks,
        "guard_bins": guard_bins,
        "active_bins": active_bins,
    }
    checks = {
        "coefficient_is_3_plus_phi": abs(coeff - (3.0 + phi)) < 1e-15,
        "coefficient_square_is_13_plus_phi5": abs(coeff * coeff - (13.0 + phi**5)) < 1e-12,
        "integer_core_is_three_opposite_pairs": opposite_pairs == 3,
        "closure_ticks_are_12": closure_ticks == 12,
        "guard_bins_are_24": guard_bins == 24,
        "active_bins_are_168": active_bins == 168,
        "half_turn_core_is_13": half_turns == 13,
        "bridge_is_numerical_not_physical_derivation": True,
    }
    result = {
        "bt": 1454,
        "title": "Quartic-to-closure coefficient bridge",
        "verified": all(checks.values()),
        "quartic_coefficient": {
            "symbol": "4-phi^2",
            "value": coeff,
            "identity_3_plus_phi": 3.0 + phi,
            "identity_sqrt_13_plus_phi5": math.sqrt(13.0 + phi**5),
        },
        "closure_arithmetic": {
            "opposite_pairs": opposite_pairs,
            "sides": pair_sides,
            "orientations": orientations,
            "closure_ticks": closure_ticks,
            "guard_bins": guard_bins,
            "half_turns": half_turns,
            "active_bins": active_bins,
        },
        "bridge_reading": {
            "linear_reading": "4-phi^2 = 3+phi = three Szilassi opposite pairs plus a golden tail",
            "square_reading": "(4-phi^2)^2 = 13+phi^5 = Otto half-turn core plus fifth-order golden tail",
            "closure_reading": "3 opposite pairs x 2 sides x 2 orientations = 12 closure ticks; doubled gives 24 guard bins; 12*(13+1)=168 active bins",
        },
        "decision": "This is a strong arithmetic bridge but remains a numerical/structural resonance until equations 49/50/64/65/66 are transcribed and audited.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1454, "verified": result["verified"], "coeff": coeff, "closure_ticks": closure_ticks}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
