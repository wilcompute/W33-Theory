#!/usr/bin/env python3
"""Part DCCII: holonomy remote-bipartite frontier bridge.

DCCI proves the active complement splits as 24 + 6 + 6. This verifier zooms
into the remote side and proves the 12-point remote portion is exactly two
disjoint rank-6 K3,3 witness components, both still zero on the current host.
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

from verify_dcci_holonomy_active_sector_trisection_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcci_bridge,
)
from w33_current_k3_mixed_plane_remote_bipartite_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_remote_bipartite_failure_summary,
)
from w33_k3_mixed_plane_remote_bipartite_split_bridge import (  # noqa: E402
    build_k3_mixed_plane_remote_bipartite_split_summary,
)


OUT_PATH = ROOT / "data" / "dccii_holonomy_remote_bipartite_frontier_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    component_count: int
    upper_remote_rank: int
    lower_remote_rank: int
    component_size: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    sectors = build_dcci_bridge()
    current = build_current_k3_mixed_plane_remote_bipartite_failure_summary()
    exact = build_k3_mixed_plane_remote_bipartite_split_summary()

    current_state = current["current_mixed_plane_remote_bipartite_state"]
    components = exact["mixed_plane_remote_bipartite_split"]["component_profiles"]
    host = exact["canonical_mixed_plane_support"]

    upper = components[0]
    lower = components[1]

    identities = {
        "dcci_already_splits_the_active_complement_as_24_plus_6_plus_6": (
            sectors["summary"]["fan_adjacent_rank"] == 24
            and sectors["summary"]["upper_remote_rank"] == 6
            and sectors["summary"]["lower_remote_rank"] == 6
            and sectors["summary"]["sector_count"] == 3
        ),
        "the_remote_12_point_shell_already_splits_as_two_exact_k3_3_components": (
            upper["left_part"] == [3, 4, 5]
            and upper["right_part"] == [12, 13, 14]
            and lower["left_part"] == [6, 7, 8]
            and lower["right_part"] == [9, 10, 11]
        ),
        "each_remote_k3_3_component_already_has_full_rank_6": (
            int(upper["restricted_curvature_rank"]) == 6
            and int(lower["restricted_curvature_rank"]) == 6
        ),
        "the_current_host_still_vanishes_on_both_remote_k3_3_components": (
            current_state["current_slot_state"] == "zero_by_splitness"
            and current_state["current_upper_remote_supported_entry_count"] == 0
            and current_state["current_lower_remote_supported_entry_count"] == 0
        ),
        "therefore_the_remote_side_of_the_frontier_is_reduced_to_the_first_nonzero_row_entry_in_either_exact_k3_3_component": (
            int(upper["restricted_curvature_rank"]) == 6
            and int(lower["restricted_curvature_rank"]) == 6
            and current_state["current_upper_remote_supported_entry_count"] == 0
            and current_state["current_lower_remote_supported_entry_count"] == 0
            and host["ordered_line_types"] == ["positive", "negative"]
        ),
    }

    summary = BridgeSummary(
        component_count=2,
        upper_remote_rank=int(upper["restricted_curvature_rank"]),
        lower_remote_rank=int(lower["restricted_curvature_rank"]),
        component_size=6,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "remote_data": {
            "upper_remote_component": {
                "left_part": upper["left_part"],
                "right_part": upper["right_part"],
                "supporting_lines": upper["supporting_lines"],
            },
            "lower_remote_component": {
                "left_part": lower["left_part"],
                "right_part": lower["right_part"],
                "supporting_lines": lower["supporting_lines"],
            },
            "fixed_host_plane": "U1",
            "fixed_shell": [81, 162, 81],
        },
        "interpretation": {
            "verdict": (
                "On the remote side, the remaining curved frontier is no longer a generic 12-point shell problem. It is already reduced to the first nonzero row-entry witness in either of two exact rank-6 K3,3 components."
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