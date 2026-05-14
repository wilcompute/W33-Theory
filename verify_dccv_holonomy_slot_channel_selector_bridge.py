#!/usr/bin/env python3
"""Part DCCV: holonomy slot-channel selector bridge.

DCXC reduced the live frontier to one open upper-right slot with nonzero live
values {1,2} over F3. DCCIII-DCCIV identified the remote side as two complete
qutrit couplers over two ordered line types with helicity count 2.

This verifier closes the bookkeeping gap: all remaining live selectors are
exactly 2-valued and therefore can be represented by one common selector bit
(stored as a nonzero F3 trit value).
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

from verify_dcciii_holonomy_remote_qutrit_coupler_bridge import (  # noqa: E402
    build_bridge as build_dcciii_bridge,
)
from verify_dcciv_holonomy_photonic_qutrit_port_packet_bridge import (  # noqa: E402
    build_bridge as build_dcciv_bridge,
)
from verify_dcxc_holonomy_one_slot_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcxc_bridge,
)


OUT_PATH = ROOT / "data" / "dccv_holonomy_slot_channel_selector_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    open_slot_count: int
    live_slot_value_count: int
    remote_coupler_count: int
    ordered_line_type_count: int
    helicity_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    slot = build_dcxc_bridge()
    coupler = build_dcciii_bridge()
    packet = build_dcciv_bridge()

    live_slot_values = [int(value) for value in slot["slot_data"]["allowed_live_slot_values"]]
    open_slot_position = [int(index) for index in slot["slot_data"]["open_slot_position"]]
    remote_components = list(coupler["remote_qutrit_couplers"]["components"])
    component_names = sorted(str(component["name"]) for component in remote_components)
    ordered_line_types = [str(value) for value in packet["host_support"]["ordered_line_types"]]
    helicity_count = int(packet["summary"]["helicity_count"])

    canonical_value_order = sorted(live_slot_values)
    canonical_component_order = component_names
    canonical_line_type_order = sorted(ordered_line_types)

    value_to_component = {
        str(value): component
        for value, component in zip(canonical_value_order, canonical_component_order)
    }
    value_to_line_type = {
        str(value): line_type
        for value, line_type in zip(canonical_value_order, canonical_line_type_order)
    }

    identities = {
        "dcxc_already_reduces_the_frontier_to_one_open_slot_with_two_nonzero_live_values": (
            slot["summary"]["remaining_open_slot_count"] == 1
            and canonical_value_order == [1, 2]
            and slot["summary"]["current_slot_value"] == 0
        ),
        "dcciii_already_reduces_the_remote_side_to_two_complete_qutrit_couplers": (
            coupler["summary"]["component_count"] == 2
            and coupler["summary"]["routes_per_component"] == 9
            and coupler["summary"]["total_route_count"] == 18
        ),
        "dcciv_already_identifies_two_ordered_line_types_and_photonic_helicity_two": (
            sorted(ordered_line_types) == ["negative", "positive"]
            and packet["summary"]["helicity_count"] == 2
            and packet["summary"]["common_packet_size"] == 162
        ),
        "all_remaining_live_selectors_are_exactly_two_valued": (
            len(canonical_value_order) == 2
            and len(canonical_component_order) == 2
            and len(canonical_line_type_order) == 2
            and helicity_count == 2
        ),
        "the_canonical_slot_channel_selector_ledger_is_well_defined_and_invertible": (
            sorted(int(value) for value in value_to_component.keys()) == [1, 2]
            and sorted(int(value) for value in value_to_line_type.keys()) == [1, 2]
            and len(set(value_to_component.values())) == 2
            and len(set(value_to_line_type.values())) == 2
        ),
        "therefore_the_remaining_frontier_is_one_two_channel_selector_choice_encoded_by_one_nonzero_slot_value": (
            slot["summary"]["remaining_open_slot_count"] == 1
            and len(canonical_value_order) == 2
            and len(canonical_component_order) == 2
            and len(canonical_line_type_order) == 2
        ),
    }

    summary = BridgeSummary(
        open_slot_count=int(slot["summary"]["remaining_open_slot_count"]),
        live_slot_value_count=len(canonical_value_order),
        remote_coupler_count=len(canonical_component_order),
        ordered_line_type_count=len(canonical_line_type_order),
        helicity_count=helicity_count,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "selector_ledger": {
            "open_slot_position": open_slot_position,
            "current_slot_value": int(slot["summary"]["current_slot_value"]),
            "allowed_live_slot_values": canonical_value_order,
            "canonical_component_order": canonical_component_order,
            "canonical_ordered_line_type_order": canonical_line_type_order,
            "value_to_component": value_to_component,
            "value_to_ordered_line_type": value_to_line_type,
        },
        "interpretation": {
            "verdict": (
                "After DCCIII-DCCIV, the last live frontier datum is no longer a free geometric family. "
                "It is one open slot with two nonzero values, and those two values match the two remote qutrit couplers and two ordered line types. "
                "So the remaining wall is a one-bit channel selector encoded as one nonzero F3 slot value."
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