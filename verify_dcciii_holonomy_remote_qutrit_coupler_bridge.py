#!/usr/bin/env python3
"""Part DCCIII: holonomy remote-qutrit-coupler bridge.

DCCII proved that the remote curved frontier is the first nonzero row-entry
witness in either of two exact rank-6 K3,3 components. This verifier tightens
that statement: each K3,3 component is exactly one complete 3-input / 3-output
qutrit transport coupler, so the remote side is two disjoint complete qutrit
couplers.
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

from verify_dccii_holonomy_remote_bipartite_frontier_bridge import (  # noqa: E402
    build_bridge as build_dccii_bridge,
)
from w33_k3_mixed_plane_remote_bipartite_split_bridge import (  # noqa: E402
    build_k3_mixed_plane_remote_bipartite_split_summary,
)


OUT_PATH = ROOT / "data" / "dcciii_holonomy_remote_qutrit_coupler_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    component_count: int
    ports_per_side: int
    routes_per_component: int
    total_route_count: int
    all_identities_hold: bool


def _component_route_data(component: dict[str, Any]) -> tuple[list[dict[str, Any]], list[tuple[int, int]]]:
    left = set(component["left_part"])
    right = set(component["right_part"])
    route_profiles: list[dict[str, Any]] = []
    realized_routes: list[tuple[int, int]] = []

    for line_profile in component["line_point_profiles"]:
        left_hits = [int(point) for point in line_profile if point in left]
        right_hits = [int(point) for point in line_profile if point in right]
        route_profiles.append(
            {
                "line_profile": [int(point) for point in line_profile],
                "left_hits": left_hits,
                "right_hits": right_hits,
            }
        )
        if len(left_hits) == 1 and len(right_hits) == 1:
            realized_routes.append((left_hits[0], right_hits[0]))

    return route_profiles, realized_routes


def build_bridge() -> dict[str, Any]:
    dccii = build_dccii_bridge()
    exact = build_k3_mixed_plane_remote_bipartite_split_summary()

    components = exact["mixed_plane_remote_bipartite_split"]["component_profiles"]
    processed_components: list[dict[str, Any]] = []

    for component in components:
        route_profiles, realized_routes = _component_route_data(component)
        left_part = [int(point) for point in component["left_part"]]
        right_part = [int(point) for point in component["right_part"]]
        expected_routes = sorted((left, right) for left in left_part for right in right_part)
        processed_components.append(
            {
                "name": component["name"],
                "left_part": left_part,
                "right_part": right_part,
                "supporting_lines": [int(line_id) for line_id in component["supporting_lines"]],
                "restricted_curvature_rank": int(component["restricted_curvature_rank"]),
                "route_profiles": route_profiles,
                "realized_routes": [[left, right] for left, right in sorted(realized_routes)],
                "expected_routes": [[left, right] for left, right in expected_routes],
                "column_support_counts": {
                    str(point): int(count)
                    for point, count in component["column_support_counts"].items()
                },
            }
        )

    ports_per_side = len(processed_components[0]["left_part"])
    routes_per_component = len(processed_components[0]["realized_routes"])
    total_route_count = sum(len(component["realized_routes"]) for component in processed_components)

    identities = {
        "dccii_already_reduces_the_remote_frontier_to_two_exact_rank_6_components": (
            dccii["summary"]["component_count"] == 2
            and dccii["summary"]["upper_remote_rank"] == 6
            and dccii["summary"]["lower_remote_rank"] == 6
            and dccii["summary"]["component_size"] == 6
        ),
        "each_supporting_line_realizes_exactly_one_ordered_left_right_port_pair": all(
            len(profile["left_hits"]) == 1 and len(profile["right_hits"]) == 1
            for component in processed_components
            for profile in component["route_profiles"]
        ),
        "each_component_realizes_all_three_by_three_qutrit_port_routes_exactly_once": all(
            sorted(component["realized_routes"]) == sorted(component["expected_routes"])
            for component in processed_components
        ),
        "the_full_remote_side_is_two_disjoint_complete_three_by_three_qutrit_couplers": (
            len(processed_components) == 2
            and ports_per_side == 3
            and routes_per_component == 3 * 3 == 9
            and total_route_count == 2 * 9 == 18
        ),
        "each_complete_qutrit_coupler_already_has_full_restricted_rank_six": all(
            component["restricted_curvature_rank"] == 6 for component in processed_components
        ),
        "therefore_the_remaining_remote_frontier_is_the_first_nonzero_port_to_port_route_in_one_of_two_exact_qutrit_couplers": (
            total_route_count == 18
            and all(component["restricted_curvature_rank"] == 6 for component in processed_components)
            and dccii["summary"]["component_count"] == 2
        ),
    }

    summary = BridgeSummary(
        component_count=len(processed_components),
        ports_per_side=ports_per_side,
        routes_per_component=routes_per_component,
        total_route_count=total_route_count,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "remote_qutrit_couplers": {
            "components": processed_components,
        },
        "interpretation": {
            "verdict": (
                "The remote side of the curved frontier is no longer just two abstract K3,3 blocks. "
                "It is exactly two disjoint complete 3-input / 3-output qutrit couplers, so the live wall is the first nonzero port-to-port route in one of those two exact couplers."
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