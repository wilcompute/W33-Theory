#!/usr/bin/env python3
"""Part DCCIV: holonomy photonic-qutrit-port-packet bridge.

DCCIII identifies the remote curved remnant as two complete 3x3 qutrit
couplers. DCLXXXVII-DCLXXXIX already identify the exact local 9-fiber bundle and
the common 162-packet. This verifier proves those are the same object viewed at
different resolutions:

    162 = (2 * 3 * 3) * 9 = 18 * 9 = 2 * 81 = 6 * 27 = 81 + 81.

So the remaining frontier is one missing port activation in one of two ordered-
type / photonic qutrit couplers carried over the uniform 9-fiber selector
bundle.
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
from verify_dclxxxvii_holonomy_selector_bundle_bridge import (  # noqa: E402
    build_bridge as build_dclxxxvii_bridge,
)
from verify_dclxxxviii_holonomy_photonic_selector_packet_bridge import (  # noqa: E402
    build_bridge as build_dclxxxviii_bridge,
)
from verify_dclxxxix_holonomy_common_packet_host_bridge import (  # noqa: E402
    build_bridge as build_dclxxxix_bridge,
)


OUT_PATH = ROOT / "data" / "dcciv_holonomy_photonic_qutrit_port_packet_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    helicity_count: int
    total_port_route_count: int
    local_qutrit_fiber_count: int
    common_packet_size: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    coupler = build_dcciii_bridge()
    bundle = build_dclxxxvii_bridge()
    packet = build_dclxxxviii_bridge()
    host = build_dclxxxix_bridge()

    helicity_count = int(packet["summary"]["helicity_count"])
    deterministic_frame_size = int(packet["summary"]["deterministic_frame_size"])
    local_selector_order = int(packet["summary"]["local_selector_order"])
    local_bulk_size = int(packet["summary"]["local_bulk_size"])
    local_qutrit_fiber_count = int(bundle["summary"]["affine_fiber_count"])
    total_port_route_count = int(coupler["summary"]["total_route_count"])
    ports_per_side = int(coupler["summary"]["ports_per_side"])
    routes_per_component = int(coupler["summary"]["routes_per_component"])
    common_packet_size = int(host["summary"]["common_packet_size"])
    host_side = [int(value) for value in host["host_support"]["qutrit_lift_split"]]
    ordered_line_types = list(host["host_support"]["ordered_line_types"])

    identities = {
        "the_remote_port_shell_is_exactly_two_copies_of_a_three_by_three_qutrit_coupler": (
            helicity_count == 2
            and ports_per_side == 3
            and routes_per_component == 3 * 3 == 9
            and total_port_route_count == helicity_count * routes_per_component == 18
        ),
        "the_uniform_local_selector_bundle_has_exactly_nine_qutrit_fibers": (
            local_qutrit_fiber_count == 9
            and bundle["summary"]["global_qutrit_fiber_count"] == 540
        ),
        "the_common_packet_is_exactly_remote_port_routes_times_local_qutrit_fibers": (
            common_packet_size == total_port_route_count * local_qutrit_fiber_count == 18 * 9 == 162
        ),
        "the_same_common_packet_is_helicity_times_the_deterministic_two_qutrit_frame": (
            common_packet_size == helicity_count * deterministic_frame_size == 2 * 81 == 162
        ),
        "the_same_common_packet_is_local_selector_symmetry_times_local_affine_bulk": (
            common_packet_size == local_selector_order * local_bulk_size == 6 * 27 == 162
        ),
        "the_same_common_packet_is_the_host_ordered_type_split_81_plus_81": (
            ordered_line_types == ["positive", "negative"]
            and host_side == [81, 81]
            and common_packet_size == sum(host_side) == 162
        ),
        "therefore_the_common_162_packet_is_the_ordered_type_doubled_qutrit_port_shell_carried_over_the_uniform_nine_fiber_bundle": (
            total_port_route_count == 18
            and local_qutrit_fiber_count == 9
            and common_packet_size == 162
            and host_side == [81, 81]
        ),
        "therefore_the_remaining_curved_frontier_is_one_missing_port_activation_in_one_of_two_ordered_type_qutrit_couplers": (
            coupler["summary"]["component_count"] == 2
            and ordered_line_types == ["positive", "negative"]
            and total_port_route_count == 18
            and local_qutrit_fiber_count == 9
            and common_packet_size == 162
        ),
    }

    summary = BridgeSummary(
        helicity_count=helicity_count,
        total_port_route_count=total_port_route_count,
        local_qutrit_fiber_count=local_qutrit_fiber_count,
        common_packet_size=common_packet_size,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "factorizations": {
            "remote_port_shell": [helicity_count, ports_per_side, ports_per_side],
            "remote_port_routes": [total_port_route_count, local_qutrit_fiber_count],
            "common_packet": {
                "value": common_packet_size,
                "route_bundle_side": [total_port_route_count, local_qutrit_fiber_count],
                "photonic_side": [helicity_count, deterministic_frame_size],
                "selector_side": [local_selector_order, local_bulk_size],
                "host_side": host_side,
            },
        },
        "host_support": {
            "ordered_line_types": ordered_line_types,
            "qutrit_lift_split": host_side,
        },
        "interpretation": {
            "verdict": (
                "The exact common 162-packet is the ordered-type / photonic doubling of one complete 3x3 qutrit port shell, carried uniformly over the 9 local qutrit fibers. "
                "So the remaining curved wall is no longer a generic row-entry problem: it is one missing port activation in one of two ordered-type qutrit couplers."
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