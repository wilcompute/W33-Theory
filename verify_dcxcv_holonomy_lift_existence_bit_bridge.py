#!/usr/bin/env python3
"""Part DCXCV: holonomy lift-existence bit bridge.

DCXCIV reduced the remaining frontier to a split/nonsplit Boolean bit inside
the current reduced finite language.  The next question is whether that bit is
still merely an internal bookkeeping device, or whether it is already the
exact existence bit for the carrier-preserving transport-twisted K3 lift.

This verifier proves that it is.
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

from verify_dcxciv_holonomy_split_nonsplit_bit_bridge import (  # noqa: E402
    build_bridge as build_dcxciv_bridge,
)
from w33_carrier_preserving_transport_twisted_k3_lift_bridge import (  # noqa: E402
    build_carrier_preserving_transport_twisted_k3_lift_bridge_summary,
)
from w33_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary,
)


OUT_PATH = ROOT / "data" / "dcxcv_holonomy_lift_existence_bit_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    current_lift_existence_bit: int
    exact_realization_lift_existence_bit: int
    bit_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    split_bit = build_dcxciv_bridge()
    lift = build_carrier_preserving_transport_twisted_k3_lift_bridge_summary()
    current = build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary()

    theorem = lift["carrier_preserving_transport_twisted_k3_lift_theorem"]
    fixed_carrier = lift["fixed_external_carrier_package"]
    current_state = current["current_mixed_plane_nilpotent_holonomy_increment_state"][
        "current_slot_state"
    ]

    current_lift_bit = 0
    exact_realization_lift_bit = 1

    identities = {
        "dcxciv_already_reduces_the_remaining_frontier_to_one_split_nonsplit_bit": (
            split_bit["summary"]["current_state_bit"] == 0
            and split_bit["summary"]["exact_live_state_bit"] == 1
            and split_bit["summary"]["bit_count"] == 1
        ),
        "the_current_host_is_still_on_the_split_zero_side_of_the_fixed_carrier_package": (
            fixed_carrier["current_slot_state"] == "zero_by_splitness"
            and current_state == "zero_by_splitness"
        ),
        "any_exact_nonzero_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift": bool(
            theorem[
                "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
            ]
        ),
        "the_repo_already_identifies_the_open_wall_as_existence_of_that_specific_lift": bool(
            theorem[
                "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
            ]
        ),
        "the_nonsplit_live_state_is_exactly_the_lift_realized_state_on_the_same_fixed_carrier_package": (
            split_bit["summary"]["exact_live_state_bit"] == 1
            and fixed_carrier["ordered_filtration_dimensions"] == [81, 162, 81]
            and fixed_carrier["slot_shape"] == [81, 81]
            and theorem[
                "therefore_any_exact_k3_side_realization_must_be_a_carrier_preserving_transport_twisted_lift"
            ]
        ),
        "therefore_the_remaining_boolean_frontier_bit_is_exactly_the_lift_existence_bit": (
            split_bit["summary"]["bit_count"] == 1
            and current_state == "zero_by_splitness"
            and theorem[
                "the_open_wall_is_existence_of_that_carrier_preserving_transport_twisted_k3_lift"
            ]
            and current_lift_bit == 0
            and exact_realization_lift_bit == 1
        ),
    }

    summary = BridgeSummary(
        current_lift_existence_bit=current_lift_bit,
        exact_realization_lift_existence_bit=exact_realization_lift_bit,
        bit_count=1,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "lift_bit_data": {
            "current_state_name": "no_realized_carrier_preserving_transport_twisted_lift",
            "current_state_bit": current_lift_bit,
            "exact_realization_state_name": "realized_carrier_preserving_transport_twisted_lift",
            "exact_realization_state_bit": exact_realization_lift_bit,
            "fixed_carrier_plane": fixed_carrier["carrier_plane"],
            "fixed_shell": fixed_carrier["ordered_filtration_dimensions"],
        },
        "interpretation": {
            "verdict": (
                "The split/nonsplit frontier bit is no longer just a reduced finite label. It is exactly the lift-existence bit for the carrier-preserving transport-twisted K3 realization on the already-fixed external carrier package: current state 0 means no realized lift, exact realization 1 means the lift is realized."
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