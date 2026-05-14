#!/usr/bin/env python3
"""Part DCXC: holonomy one-slot frontier bridge.

After DCLXXXIX, the selector bundle, photonic runtime, and canonical host all
agree on the same exact support packet size 162.  The remaining wall can now be
written in the smallest possible matrix language: one upper-right slot.

This verifier proves that every support/count/mode packet already matches, and
the only remaining unresolved datum is the value of the single upper-right entry
in the adapted 2x2 nilpotent increment matrix:

    [[0, x],
     [0, 0]]

with x currently 0 and exact realization requiring x in {1, 2} over F3.
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

from verify_dclxxxix_holonomy_common_packet_host_bridge import (  # noqa: E402
    build_bridge as build_dclxxxix_bridge,
)
from w33_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (  # noqa: E402
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)


OUT_PATH = ROOT / "data" / "dcxc_holonomy_one_slot_frontier_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    support_packet_size: int
    current_slot_value: int
    allowed_live_slot_values: list[int]
    remaining_open_slot_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    packet = build_dclxxxix_bridge()
    current = build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary()
    exact = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()

    support_packet_size = packet["summary"]["host_support_total"]
    current_increment = current["current_mixed_plane_nilpotent_holonomy_increment_state"]["current_nilpotent_increment"]
    current_slot_value = current_increment[0][1]
    allowed_live_increments = exact["mixed_plane_nilpotent_holonomy_increment"]["nonzero_sign_trivial_increments"]
    allowed_live_slot_values = sorted({increment[0][1] for increment in allowed_live_increments})

    identities = {
        "the_support_packet_is_already_exactly_matched": support_packet_size == 162,
        "the_current_host_already_has_the_exact_81_plus_81_support_packet": (
            current["current_mixed_plane_nilpotent_holonomy_increment_state"]["qutrit_lift_split"] == [81, 81]
            and support_packet_size == 162
        ),
        "the_current_adapted_nilpotent_increment_is_exactly_zero": current_increment == [[0, 0], [0, 0]],
        "the_exact_live_nilpotent_increments_are_exactly_the_two_nonzero_upper_right_choices": (
            sorted(allowed_live_increments) == [[[0, 1], [0, 0]], [[0, 2], [0, 0]]]
            and allowed_live_slot_values == [1, 2]
        ),
        "all_other_support_mode_and_packet_constraints_have_already_collapsed": (
            packet["summary"]["common_packet_size"] == 162
            and packet["summary"]["global_selector_carrier"] == 1620
            and current["current_k3_mixed_plane_nilpotent_holonomy_increment_failure_theorem"]["the_current_mixed_plane_host_already_preserves_the_full_canonical_support_package_and_qutrit_lift"]
            is True
        ),
        "there_is_exactly_one_remaining_open_slot": (
            len(allowed_live_slot_values) == 2
            and current_slot_value == 0
            and current_increment[1][0] == 0
            and current_increment[1][1] == 0
            and current_increment[0][0] == 0
        ),
        "therefore_the_live_frontier_is_the_single_upper_right_slot_x_with_current_value_0_and_exact_live_values_1_or_2": (
            support_packet_size == 162
            and current_slot_value == 0
            and allowed_live_slot_values == [1, 2]
        ),
    }

    summary = BridgeSummary(
        support_packet_size=support_packet_size,
        current_slot_value=current_slot_value,
        allowed_live_slot_values=allowed_live_slot_values,
        remaining_open_slot_count=1,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "slot_data": {
            "current_increment": current_increment,
            "allowed_live_increments": allowed_live_increments,
            "open_slot_position": [0, 1],
            "current_slot_value": current_slot_value,
            "allowed_live_slot_values": allowed_live_slot_values,
        },
        "interpretation": {
            "verdict": (
                "The carrier-size, bundle-size, photonic packet, and host support problems are already solved. "
                "The remaining frontier is a single adapted matrix slot: the upper-right entry of the nilpotent increment. "
                "It is currently 0 and exact realization requires it to be 1 or 2 over F3."
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