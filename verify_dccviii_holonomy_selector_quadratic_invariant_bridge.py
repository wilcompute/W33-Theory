#!/usr/bin/env python3
"""Part DCCVIII: holonomy selector-quadratic-invariant bridge.

DCCVII encoded the two-value selector as signed polarization charge vectors
{(+81,-81),(-81,+81)} on ordered line types (negative, positive).

This verifier extracts the invariant quadratic data:

  - L2 norm squared is constant: 81^2 + 81^2,
  - signed two-channel product is constant: (-81)*(+81),
  - orientation scalar flips sign under selector flip.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from verify_dccvii_holonomy_selector_polarization_charge_bridge import (  # noqa: E402
    build_bridge as build_dccvii_bridge,
)


OUT_PATH = ROOT / "data" / "dccviii_holonomy_selector_quadratic_invariant_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    selector_value_count: int
    invariant_norm_squared: int
    invariant_signed_product: int
    orientation_magnitude: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    charge_payload = build_dccvii_bridge()

    selector_flip_map = dict(charge_payload["selector_flip_map"])
    charge_profiles = dict(charge_payload["charge_profiles"])
    selector_values = sorted(charge_profiles.keys())

    ordered_types = ["negative", "positive"]
    quadratic_profiles: dict[str, dict[str, Any]] = {}
    for value in selector_values:
        charges = charge_profiles[value]["charge_by_ordered_line_type"]
        q_negative = int(charges["negative"])
        q_positive = int(charges["positive"])
        norm_squared = q_negative * q_negative + q_positive * q_positive
        signed_product = q_negative * q_positive
        orientation_scalar = q_positive - q_negative

        quadratic_profiles[value] = {
            "charge_vector": [q_negative, q_positive],
            "norm_squared": norm_squared,
            "signed_product": signed_product,
            "orientation_scalar": orientation_scalar,
        }

    invariant_norm_squared = int(quadratic_profiles[selector_values[0]]["norm_squared"])
    invariant_signed_product = int(quadratic_profiles[selector_values[0]]["signed_product"])
    orientation_magnitude = abs(int(quadratic_profiles[selector_values[0]]["orientation_scalar"]))

    flip_checks: dict[str, dict[str, bool]] = {}
    for value in selector_values:
        flipped = str(selector_flip_map[value])
        this_profile = quadratic_profiles[value]
        that_profile = quadratic_profiles[flipped]
        flip_checks[value] = {
            "norm_preserved": this_profile["norm_squared"] == that_profile["norm_squared"],
            "signed_product_preserved": this_profile["signed_product"] == that_profile["signed_product"],
            "orientation_negated": this_profile["orientation_scalar"] == -that_profile["orientation_scalar"],
        }

    identities = {
        "dccvii_already_provides_exactly_two_selector_charge_vectors_plusminus_81": (
            selector_values == ["1", "2"]
            and all(
                sorted(profile["charge_vector"]) == [-81, 81]
                for profile in quadratic_profiles.values()
            )
        ),
        "selector_flip_is_the_two_cycle_1_2": selector_flip_map == {"1": 2, "2": 1},
        "l2_norm_squared_is_selector_invariant": (
            invariant_norm_squared == 81 * 81 + 81 * 81
            and all(profile["norm_squared"] == invariant_norm_squared for profile in quadratic_profiles.values())
            and all(checks["norm_preserved"] for checks in flip_checks.values())
        ),
        "signed_two_channel_product_is_selector_invariant": (
            invariant_signed_product == -81 * 81
            and all(profile["signed_product"] == invariant_signed_product for profile in quadratic_profiles.values())
            and all(checks["signed_product_preserved"] for checks in flip_checks.values())
        ),
        "orientation_scalar_flips_sign_under_selector_flip": (
            orientation_magnitude == 162
            and sorted(profile["orientation_scalar"] for profile in quadratic_profiles.values()) == [-162, 162]
            and all(checks["orientation_negated"] for checks in flip_checks.values())
        ),
        "therefore_the_remaining_selector_is_one_z2_orientation_over_a_fixed_quadratic_invariant_shell": (
            len(selector_values) == 2
            and invariant_norm_squared == 13122
            and invariant_signed_product == -6561
            and orientation_magnitude == 162
            and all(checks["orientation_negated"] for checks in flip_checks.values())
        ),
    }

    summary = BridgeSummary(
        selector_value_count=len(selector_values),
        invariant_norm_squared=invariant_norm_squared,
        invariant_signed_product=invariant_signed_product,
        orientation_magnitude=orientation_magnitude,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "quadratic_profiles": quadratic_profiles,
        "flip_checks": flip_checks,
        "interpretation": {
            "verdict": (
                "The DCCVII signed selector has fixed quadratic shell data (norm and signed product) and only a Z2 orientation degree of freedom. "
                "Selector flip preserves invariants and reverses orientation scalar."
            )
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()