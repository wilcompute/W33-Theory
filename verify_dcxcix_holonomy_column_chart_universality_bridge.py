#!/usr/bin/env python3
"""Part DCXCIX: holonomy column-chart universality bridge.

DCXCVIII localized the remaining curved frontier to one support-preserving
nonzero row entry on the fixed mixed-plane host.  The next question is whether
that entry still depends on a special curvature column.

This verifier proves that it does not: every active curvature column is already
an exact local chart for the same frontier.
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

from verify_dcxcviii_holonomy_row_entry_curved_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcxcviii_bridge,
)
from w33_current_k3_mixed_plane_column_chart_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_column_chart_failure_summary,
)
from w33_k3_mixed_plane_column_chart_universality_bridge import (  # noqa: E402
    build_k3_mixed_plane_column_chart_universality_summary,
)


OUT_PATH = ROOT / "data" / "dcxcix_holonomy_column_chart_universality_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    curvature_column_count: int
    active_column_count: int
    inactive_column_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    row_entry = build_dcxcviii_bridge()
    current = build_current_k3_mixed_plane_column_chart_failure_summary()
    exact = build_k3_mixed_plane_column_chart_universality_summary()

    current_state = current["current_mixed_plane_column_chart_state"]
    universality = exact["column_chart_universality"]
    host = exact["canonical_mixed_plane_support"]

    curvature_column_count = int(universality["curvature_column_count"])
    active_column_count = int(universality["supported_column_count"])
    inactive_column_count = curvature_column_count - active_column_count

    identities = {
        "dcxcviii_already_localizes_the_last_curved_frontier_to_one_row_entry_witness": (
            row_entry["summary"]["current_supported_entry_count"] == 0
            and row_entry["summary"]["exact_supported_row_count"] == 4046
            and row_entry["summary"]["exact_row_support_size"] == 1
        ),
        "the_current_host_still_has_zero_supported_entries_in_every_curvature_column": (
            current_state["current_slot_state"] == "zero_by_splitness"
            and current_state["current_supported_column_count"] == 0
            and current_state["current_supported_entry_count"] == 0
        ),
        "the_exact_curved_witness_has_45_columns_of_which_exactly_36_are_active": (
            curvature_column_count == 45 and active_column_count == 36 and inactive_column_count == 9
        ),
        "every_active_column_already_carries_both_row_components_and_both_nonzero_f3_values": (
            int(universality["columns_with_both_row_components"]) == 36
            and int(universality["columns_with_both_nonzero_values"]) == 36
        ),
        "therefore_the_remaining_curved_frontier_is_not_a_special_column_choice_but_a_universal_active_column_chart_problem": (
            current_state["current_supported_entry_count"] == 0
            and curvature_column_count == 45
            and active_column_count == 36
            and int(universality["columns_with_both_row_components"]) == 36
            and int(universality["columns_with_both_nonzero_values"]) == 36
            and host["ordered_line_types"] == ["positive", "negative"]
        ),
    }

    summary = BridgeSummary(
        curvature_column_count=curvature_column_count,
        active_column_count=active_column_count,
        inactive_column_count=inactive_column_count,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "column_data": {
            "current_supported_column_count": int(current_state["current_supported_column_count"]),
            "columns_with_both_row_components": int(universality["columns_with_both_row_components"]),
            "columns_with_both_nonzero_values": int(universality["columns_with_both_nonzero_values"]),
            "fixed_host_plane": "U1",
            "fixed_shell": [81, 162, 81],
        },
        "interpretation": {
            "verdict": (
                "The remaining curved frontier is not concentrated in a special curvature column. Every one of the 36 active columns is already a valid local chart for the same nonzero row-entry witness, while the current host remains zero in all of them."
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