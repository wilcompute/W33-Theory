#!/usr/bin/env python3
"""Part DCXCVIII: holonomy row-entry curved frontier bridge.

DCXCVII identifies the last unresolved curved theorem with realization of the
 nonzero off-diagonal curvature block. This verifier localizes that block all
the way down to the smallest supported witness already present in the exact
precomplex: one nonzero row entry on the same fixed mixed-plane host.
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

from verify_dcxcvii_holonomy_off_diagonal_curvature_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcxcvii_bridge,
)
from w33_current_k3_mixed_plane_row_entry_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_row_entry_failure_summary,
)
from w33_k3_mixed_plane_row_entry_witness_bridge import (  # noqa: E402
    build_k3_mixed_plane_row_entry_witness_summary,
)


OUT_PATH = ROOT / "data" / "dcxcviii_holonomy_row_entry_curved_frontier_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    current_supported_entry_count: int
    exact_supported_row_count: int
    exact_row_support_size: int
    distinct_live_entry_value_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    curvature = build_dcxcvii_bridge()
    current = build_current_k3_mixed_plane_row_entry_failure_summary()
    exact = build_k3_mixed_plane_row_entry_witness_summary()

    current_state = current["current_mixed_plane_row_entry_state"]
    row_entry = exact["row_entry_witness"]
    host = exact["canonical_mixed_plane_support"]

    identities = {
        "dcxcvii_already_identifies_the_last_curved_theorem_with_the_nonzero_off_diagonal_curvature_witness": (
            curvature["summary"]["current_off_diagonal_curvature_rank"] == 0
            and curvature["summary"]["exact_off_diagonal_curvature_rank"] == 36
            and curvature["summary"]["exact_off_diagonal_support_rows"] == 4046
        ),
        "the_current_host_still_has_zero_supported_row_entries": (
            current_state["current_slot_state"] == "zero_by_splitness"
            and current_state["current_supported_row_count"] == 0
            and current_state["current_supported_entry_count"] == 0
        ),
        "the_exact_curved_witness_localizes_to_one_sparse_supported_rows": (
            row_entry["supported_row_count"] == 4046
            and row_entry["row_support_size_distribution"] == {1: 4046}
            and row_entry["entry_value_distribution"] == {1: 2029, 2: 2017}
        ),
        "both_row_components_already_carry_live_entries_on_the_same_fixed_host": (
            row_entry["row_component_distribution"] == {"invariant_row": 2018, "sign_row": 2028}
            and host["ordered_line_types"] == ["positive", "negative"]
            and list(host["qutrit_lift_split"]) == [81, 81]
        ),
        "therefore_the_one_remaining_curved_theorem_localizes_to_one_nonzero_row_entry_witness_on_the_same_fixed_host": (
            curvature["summary"]["exact_off_diagonal_support_rows"] == 4046
            and current_state["current_supported_entry_count"] == 0
            and row_entry["row_support_size_distribution"] == {1: 4046}
            and row_entry["entry_value_distribution"] == {1: 2029, 2: 2017}
        ),
    }

    summary = BridgeSummary(
        current_supported_entry_count=int(current_state["current_supported_entry_count"]),
        exact_supported_row_count=int(row_entry["supported_row_count"]),
        exact_row_support_size=1,
        distinct_live_entry_value_count=len(row_entry["entry_value_distribution"]),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "local_data": {
            "fixed_host_plane": "U1",
            "fixed_shell": [81, 162, 81],
            "row_support_size_distribution": row_entry["row_support_size_distribution"],
            "entry_value_distribution": row_entry["entry_value_distribution"],
            "row_component_distribution": row_entry["row_component_distribution"],
        },
        "interpretation": {
            "verdict": (
                "The last curved frontier now localizes to the smallest supported object already present in the exact precomplex: one nonzero row entry of the off-diagonal curvature block on the same fixed mixed-plane host."
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