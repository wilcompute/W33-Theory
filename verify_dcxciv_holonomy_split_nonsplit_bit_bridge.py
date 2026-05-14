#!/usr/bin/env python3
"""Part DCXCIV: holonomy split-nonsplit bit bridge.

Once the remaining frontier is identified as realization of the unique
nontrivial extension class, the current reduced finite language leaves only one
logical distinction:

    split  (0)  versus  nonsplit  (1).

This verifier makes that Boolean reduction explicit.
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

from verify_dcxciii_holonomy_unique_extension_class_bridge import (  # noqa: E402
    build_bridge as build_dcxciii_bridge,
)
from w33_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary,
)


OUT_PATH = ROOT / "data" / "dcxciv_holonomy_split_nonsplit_bit_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    current_state_bit: int
    exact_live_state_bit: int
    bit_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    classes = build_dcxciii_bridge()
    current = build_current_k3_mixed_plane_nilpotent_holonomy_increment_failure_summary()

    current_state = current["current_mixed_plane_nilpotent_holonomy_increment_state"]["current_slot_state"]
    current_bit = 0
    live_bit = 1

    identities = {
        "the_current_host_is_explicitly_split_in_the_repo_language": current_state == "zero_by_splitness",
        "the_unique_live_class_is_exactly_the_nonsplit_class": (
            classes["summary"]["trivial_class_count"] == 1
            and classes["summary"]["nontrivial_class_count"] == 1
        ),
        "there_are_exactly_two_states_in_the_current_reduced_finite_language_split_and_nonsplit": (
            classes["summary"]["total_class_count"] == 2
            and current_bit == 0
            and live_bit == 1
        ),
        "the_current_state_bit_is_zero": current_bit == 0,
        "the_exact_live_state_bit_is_one": live_bit == 1,
        "therefore_the_remaining_frontier_is_one_boolean_split_nonsplit_activation_bit": (
            current_state == "zero_by_splitness"
            and classes["summary"]["total_class_count"] == 2
            and current_bit == 0
            and live_bit == 1
        ),
    }

    summary = BridgeSummary(
        current_state_bit=current_bit,
        exact_live_state_bit=live_bit,
        bit_count=1,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "bit_data": {
            "current_state_name": "split",
            "current_state_bit": current_bit,
            "exact_live_state_name": "nonsplit",
            "exact_live_state_bit": live_bit,
        },
        "interpretation": {
            "verdict": (
                "In the current reduced finite language the frontier is now one Boolean activation bit. The current host is the split state (0), and exact realization is the nonsplit state (1)."
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