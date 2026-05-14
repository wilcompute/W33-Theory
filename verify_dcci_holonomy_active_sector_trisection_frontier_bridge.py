#!/usr/bin/env python3
"""Part DCCI: holonomy active-sector trisection frontier bridge.

DCC proved that the remaining curved frontier lives on the exact full-rank
36-column active complement. The next question is whether that active block is
still undifferentiated.

This verifier proves that it already splits into three exact full-rank sectors
of sizes 24, 6, and 6, and that the current host still vanishes on all three.
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

from verify_dcc_holonomy_active_column_basis_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcc_bridge,
)
from w33_current_k3_mixed_plane_active_sector_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_active_sector_failure_summary,
)
from w33_k3_mixed_plane_active_sector_trisection_bridge import (  # noqa: E402
    build_k3_mixed_plane_active_sector_trisection_summary,
)


OUT_PATH = ROOT / "data" / "dcci_holonomy_active_sector_trisection_frontier_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    fan_adjacent_rank: int
    upper_remote_rank: int
    lower_remote_rank: int
    sector_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    active_basis = build_dcc_bridge()
    current = build_current_k3_mixed_plane_active_sector_failure_summary()
    exact = build_k3_mixed_plane_active_sector_trisection_summary()

    current_state = current["current_mixed_plane_active_sector_state"]
    sectors = exact["mixed_plane_active_sector_trisection"]
    host = exact["canonical_mixed_plane_support"]

    identities = {
        "dcc_already_identifies_the_live_wall_with_the_full_rank_36_column_active_complement": (
            active_basis["summary"]["active_column_count"] == 36
            and active_basis["summary"]["active_restricted_rank"] == 36
            and active_basis["summary"]["inert_column_count"] == 9
        ),
        "the_exact_active_complement_already_splits_as_24_plus_6_plus_6": (
            len(sectors["fan_adjacent_columns"]) == 24
            and len(sectors["upper_remote_columns"]) == 6
            and len(sectors["lower_remote_columns"]) == 6
            and sectors["fan_adjacent_rank"] == 24
            and sectors["upper_remote_rank"] == 6
            and sectors["lower_remote_rank"] == 6
        ),
        "the_current_host_still_vanishes_on_all_three_exact_active_sectors": (
            current_state["current_slot_state"] == "zero_by_splitness"
            and current_state["current_fan_adjacent_supported_entry_count"] == 0
            and current_state["current_upper_remote_supported_entry_count"] == 0
            and current_state["current_lower_remote_supported_entry_count"] == 0
        ),
        "the_three_sector_frontier_lives_on_the_same_fixed_mixed_plane_host": (
            host["ordered_line_types"] == ["positive", "negative"]
            and list(host["mixed_signature"]) == [1, 1]
            and list(host["qutrit_lift_split"]) == [81, 81]
        ),
        "therefore_the_remaining_curved_frontier_may_first_appear_in_any_of_three_exact_full_rank_sectors": (
            current_state["current_slot_state"] == "zero_by_splitness"
            and sectors["fan_adjacent_rank"] == 24
            and sectors["upper_remote_rank"] == 6
            and sectors["lower_remote_rank"] == 6
            and host["ordered_line_types"] == ["positive", "negative"]
        ),
    }

    summary = BridgeSummary(
        fan_adjacent_rank=int(sectors["fan_adjacent_rank"]),
        upper_remote_rank=int(sectors["upper_remote_rank"]),
        lower_remote_rank=int(sectors["lower_remote_rank"]),
        sector_count=3,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "sector_data": {
            "fan_adjacent_columns": sectors["fan_adjacent_columns"],
            "upper_remote_columns": sectors["upper_remote_columns"],
            "lower_remote_columns": sectors["lower_remote_columns"],
            "fixed_host_plane": "U1",
            "fixed_shell": [81, 162, 81],
        },
        "interpretation": {
            "verdict": (
                "The remaining curved frontier is no longer just a 36-column active block. It already splits into three exact full-rank sectors of sizes 24, 6, and 6, and the current host still vanishes on all three."
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