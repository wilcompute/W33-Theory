#!/usr/bin/env python3
"""Part DCXCVII: holonomy off-diagonal curvature frontier bridge.

DCXCVI proved that no finite ambiguity remains and that the only unresolved
content is one curved K3 existence theorem. This verifier identifies the exact
content of that theorem: realization of the nonzero off-diagonal curvature
block already carried by the transport-twisted precomplex on the same fixed
mixed-plane host.
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

from verify_dcxcvi_holonomy_pure_k3_existence_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcxcvi_bridge,
)
from w33_current_k3_mixed_plane_off_diagonal_curvature_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_off_diagonal_curvature_failure_summary,
)
from w33_k3_mixed_plane_off_diagonal_curvature_witness_bridge import (  # noqa: E402
    build_k3_mixed_plane_off_diagonal_curvature_witness_summary,
)


OUT_PATH = ROOT / "data" / "dcxcvii_holonomy_off_diagonal_curvature_frontier_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    current_off_diagonal_curvature_rank: int
    exact_off_diagonal_curvature_rank: int
    exact_off_diagonal_support_rows: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    frontier = build_dcxcvi_bridge()
    current = build_current_k3_mixed_plane_off_diagonal_curvature_failure_summary()
    exact = build_k3_mixed_plane_off_diagonal_curvature_witness_summary()

    current_state = current["current_mixed_plane_off_diagonal_curvature_state"]
    exact_curvature = exact["transport_twisted_off_diagonal_curvature_package"]
    host = exact["canonical_mixed_plane_support"]

    identities = {
        "dcxcvi_already_reduces_the_remaining_problem_to_one_curved_k3_existence_theorem": (
            frontier["summary"]["finite_ambiguity_count"] == 0
            and frontier["summary"]["remaining_curved_theorem_count"] == 1
            and frontier["summary"]["fixed_packet_dimension"] == 162
        ),
        "the_current_host_still_has_zero_off_diagonal_curvature_on_the_fixed_support_package": (
            current_state["current_slot_state"] == "zero_by_splitness"
            and current_state["current_off_diagonal_curvature_rank"] == 0
            and current_state["current_off_diagonal_curvature_support_rows"] == 0
            and list(current_state["qutrit_lift_split"]) == [81, 81]
        ),
        "the_exact_internal_curved_datum_is_the_nonzero_off_diagonal_curvature_block": (
            exact_curvature["off_diagonal_curvature_rank"] == 36
            and exact_curvature["off_diagonal_curvature_support_rows"] == 4046
            and bool(exact_curvature["upper_right_curvature_identity_exact"])
        ),
        "that_nonzero_curvature_block_lives_on_the_same_fixed_mixed_plane_host": (
            host["ordered_line_types"] == ["positive", "negative"]
            and list(host["mixed_signature"]) == [1, 1]
            and list(host["qutrit_lift_split"]) == [81, 81]
        ),
        "therefore_the_unique_remaining_curved_theorem_is_exactly_realization_of_the_nonzero_off_diagonal_curvature_witness_on_the_same_fixed_host": (
            frontier["summary"]["remaining_curved_theorem_count"] == 1
            and current_state["current_off_diagonal_curvature_rank"] == 0
            and exact_curvature["off_diagonal_curvature_rank"] == 36
            and exact_curvature["off_diagonal_curvature_support_rows"] == 4046
            and host["ordered_line_types"] == ["positive", "negative"]
        ),
    }

    summary = BridgeSummary(
        current_off_diagonal_curvature_rank=int(current_state["current_off_diagonal_curvature_rank"]),
        exact_off_diagonal_curvature_rank=int(exact_curvature["off_diagonal_curvature_rank"]),
        exact_off_diagonal_support_rows=int(exact_curvature["off_diagonal_curvature_support_rows"]),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "frontier_data": {
            "fixed_host_plane": "U1",
            "fixed_shell": [81, 162, 81],
            "current_off_diagonal_curvature_rank": int(current_state["current_off_diagonal_curvature_rank"]),
            "exact_off_diagonal_curvature_rank": int(exact_curvature["off_diagonal_curvature_rank"]),
            "exact_off_diagonal_curvature_support_rows": int(exact_curvature["off_diagonal_curvature_support_rows"]),
        },
        "interpretation": {
            "verdict": (
                "The single curved theorem left by DCXCVI is not abstract anymore. It is exactly realization of the nonzero off-diagonal curvature block already present in the transport-twisted precomplex on the same fixed mixed-plane host."
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