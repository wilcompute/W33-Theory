#!/usr/bin/env python3
"""Part DCCVI: holonomy channel-conditioned packet-budget bridge.

DCCV reduced the live wall to a two-valued slot selector. DCCIII-DCCIV already
fix the remote route budget (18 = 9 + 9), local fiber count (9), and common
packet size (162 = 81 + 81).

This verifier makes the conditioned budget explicit:

  - selecting either live slot value chooses one 9-route channel;
  - conditioned packet footprint = 9 * 9 = 81;
  - complementary channel footprint = 81;
  - total remains 81 + 81 = 162.
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

from verify_dcciv_holonomy_photonic_qutrit_port_packet_bridge import (  # noqa: E402
    build_bridge as build_dcciv_bridge,
)
from verify_dccv_holonomy_slot_channel_selector_bridge import (  # noqa: E402
    build_bridge as build_dccv_bridge,
)


OUT_PATH = ROOT / "data" / "dccvi_holonomy_channel_conditioned_packet_budget_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    selector_value_count: int
    routes_per_channel: int
    local_fiber_count: int
    conditioned_packet_size: int
    total_packet_size: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    selector = build_dccv_bridge()
    packet = build_dcciv_bridge()

    selector_values = [int(value) for value in selector["selector_ledger"]["allowed_live_slot_values"]]
    value_to_component = dict(selector["selector_ledger"]["value_to_component"])

    total_route_count = int(packet["summary"]["total_port_route_count"])
    selector_value_count = len(selector_values)
    routes_per_channel = total_route_count // selector_value_count

    local_fiber_count = int(packet["summary"]["local_qutrit_fiber_count"])
    conditioned_packet_size = routes_per_channel * local_fiber_count
    total_packet_size = int(packet["summary"]["common_packet_size"])
    host_split = [int(value) for value in packet["factorizations"]["common_packet"]["host_side"]]

    conditioned_budgets: dict[str, dict[str, Any]] = {}
    for value in selector_values:
        selected_component = value_to_component[str(value)]
        conditioned_budgets[str(value)] = {
            "selected_component": selected_component,
            "selected_route_budget": routes_per_channel,
            "selected_packet_budget": conditioned_packet_size,
            "complement_route_budget": total_route_count - routes_per_channel,
            "complement_packet_budget": total_packet_size - conditioned_packet_size,
        }

    identities = {
        "dccv_already_identifies_exactly_two_live_selector_values": (
            selector_value_count == 2
            and selector_values == [1, 2]
            and selector["summary"]["open_slot_count"] == 1
        ),
        "dcciv_already_identifies_the_remote_route_budget_as_18_and_local_fiber_count_as_9": (
            total_route_count == 18
            and local_fiber_count == 9
            and packet["summary"]["common_packet_size"] == 162
        ),
        "each_selector_value_chooses_one_nine_route_channel": (
            routes_per_channel == 9
            and all(
                budget["selected_route_budget"] == 9 and budget["complement_route_budget"] == 9
                for budget in conditioned_budgets.values()
            )
        ),
        "conditioned_packet_budget_is_exactly_nine_times_nine_equals_81": (
            conditioned_packet_size == 9 * 9 == 81
            and all(
                budget["selected_packet_budget"] == 81 for budget in conditioned_budgets.values()
            )
        ),
        "conditioned_complement_packet_budget_is_also_81": all(
            budget["complement_packet_budget"] == 81 for budget in conditioned_budgets.values()
        ),
        "the_total_packet_budget_remains_81_plus_81_equals_162": (
            total_packet_size == 162
            and conditioned_packet_size + (total_packet_size - conditioned_packet_size) == 162
            and host_split == [81, 81]
        ),
        "therefore_the_two_value_slot_selector_is_equivalent_to_a_channel_conditioned_81_81_packet_budget_split": (
            selector_value_count == 2
            and routes_per_channel == 9
            and conditioned_packet_size == 81
            and total_packet_size == 162
            and host_split == [81, 81]
        ),
    }

    summary = BridgeSummary(
        selector_value_count=selector_value_count,
        routes_per_channel=routes_per_channel,
        local_fiber_count=local_fiber_count,
        conditioned_packet_size=conditioned_packet_size,
        total_packet_size=total_packet_size,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "conditioned_budgets": conditioned_budgets,
        "factorizations": {
            "routes": [total_route_count, routes_per_channel, routes_per_channel],
            "packet": [total_packet_size, conditioned_packet_size, total_packet_size - conditioned_packet_size],
            "host_split": host_split,
        },
        "interpretation": {
            "verdict": (
                "The DCCV two-value selector is not only combinatorial. It induces an exact channel-conditioned packet budget: "
                "each live value selects one 9-route channel and therefore one 81-state conditioned packet footprint, with complementary 81-state budget, preserving total 162."
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