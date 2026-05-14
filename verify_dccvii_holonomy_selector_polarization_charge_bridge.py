#!/usr/bin/env python3
"""Part DCCVII: holonomy selector-polarization-charge bridge.

DCCVI gave an exact conditioned packet budget split 81/81 for each of the two
live selector values. This verifier upgrades that budget to a signed
polarization-charge law on the two ordered line types.

For each selector value, assign +81 to the selected ordered type and -81 to the
complementary ordered type. Then:

  - net charge is always 0,
  - total absolute budget is always 162,
  - flipping selector value swaps the channel and negates the charge vector.
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

from verify_dccv_holonomy_slot_channel_selector_bridge import (  # noqa: E402
    build_bridge as build_dccv_bridge,
)
from verify_dccvi_holonomy_channel_conditioned_packet_budget_bridge import (  # noqa: E402
    build_bridge as build_dccvi_bridge,
)


OUT_PATH = ROOT / "data" / "dccvii_holonomy_selector_polarization_charge_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    selector_value_count: int
    conditioned_packet_budget: int
    total_absolute_budget: int
    all_identities_hold: bool


def _selector_flip_map(values: list[int]) -> dict[str, int]:
    if len(values) != 2:
        raise ValueError("selector flip map requires exactly two values")
    a, b = sorted(values)
    return {str(a): b, str(b): a}


def build_bridge() -> dict[str, Any]:
    selector = build_dccv_bridge()
    budget = build_dccvi_bridge()

    selector_values = [int(value) for value in selector["selector_ledger"]["allowed_live_slot_values"]]
    ordered_types = sorted(
        str(value) for value in selector["selector_ledger"]["canonical_ordered_line_type_order"]
    )
    value_to_ordered_type = dict(selector["selector_ledger"]["value_to_ordered_line_type"])

    conditioned_packet_budget = int(budget["summary"]["conditioned_packet_size"])
    total_packet_budget = int(budget["summary"]["total_packet_size"])

    charge_profiles: dict[str, dict[str, Any]] = {}
    for value in selector_values:
        selected_type = value_to_ordered_type[str(value)]
        profile = {ordered_type: (-conditioned_packet_budget) for ordered_type in ordered_types}
        profile[selected_type] = conditioned_packet_budget
        charge_profiles[str(value)] = {
            "selected_ordered_line_type": selected_type,
            "charge_by_ordered_line_type": profile,
            "net_charge": sum(profile.values()),
            "absolute_charge_budget": sum(abs(charge) for charge in profile.values()),
        }

    flip_map = _selector_flip_map(selector_values)
    flip_negation_checks = {}
    for value in sorted(charge_profiles.keys()):
        flipped = str(flip_map[value])
        value_profile = charge_profiles[value]["charge_by_ordered_line_type"]
        flipped_profile = charge_profiles[flipped]["charge_by_ordered_line_type"]
        flip_negation_checks[value] = all(
            value_profile[line_type] == -flipped_profile[line_type] for line_type in ordered_types
        )

    identities = {
        "dccv_already_provides_a_two_value_selector_over_two_ordered_line_types": (
            sorted(selector_values) == [1, 2]
            and ordered_types == ["negative", "positive"]
            and len(selector_values) == len(ordered_types) == 2
        ),
        "dccvi_already_provides_an_exact_conditioned_budget_of_81_with_total_162": (
            conditioned_packet_budget == 81
            and total_packet_budget == 162
            and budget["summary"]["selector_value_count"] == 2
        ),
        "each_selector_value_defines_a_signed_charge_vector_with_plus_81_on_selected_type_and_minus_81_on_complement": all(
            sorted(profile["charge_by_ordered_line_type"].values()) == [-81, 81]
            for profile in charge_profiles.values()
        ),
        "net_charge_is_always_zero": all(profile["net_charge"] == 0 for profile in charge_profiles.values()),
        "absolute_charge_budget_is_always_162": all(
            profile["absolute_charge_budget"] == 162 for profile in charge_profiles.values()
        ),
        "selector_flip_is_an_involution_that_negates_the_charge_vector": (
            flip_map == {"1": 2, "2": 1}
            and all(flip_negation_checks.values())
        ),
        "therefore_the_remaining_two_value_selector_is_equivalent_to_a_signed_polarization_charge_choice": (
            len(selector_values) == 2
            and conditioned_packet_budget == 81
            and all(profile["net_charge"] == 0 for profile in charge_profiles.values())
            and all(profile["absolute_charge_budget"] == 162 for profile in charge_profiles.values())
            and all(flip_negation_checks.values())
        ),
    }

    summary = BridgeSummary(
        selector_value_count=len(selector_values),
        conditioned_packet_budget=conditioned_packet_budget,
        total_absolute_budget=162,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "selector_flip_map": flip_map,
        "charge_profiles": charge_profiles,
        "interpretation": {
            "verdict": (
                "DCCVI's conditioned 81/81 budget can be represented as a signed polarization-charge law on ordered line types. "
                "Each live selector value picks one +81 channel against one -81 complement; the selector flip is an involutive sign reversal."
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