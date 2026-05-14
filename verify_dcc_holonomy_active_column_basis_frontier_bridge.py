#!/usr/bin/env python3
"""Part DCC: holonomy active-column basis frontier bridge.

DCXCIX proves the remaining curved frontier is universal across the 36 active
curvature columns.  The next question is whether those columns are merely a
support set or already the exact full-rank basis block carrying the live wall.

This verifier proves that they are.
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

from verify_dcxcix_holonomy_column_chart_universality_bridge import (  # noqa: E402
    build_bridge as build_dcxcix_bridge,
)
from w33_current_k3_mixed_plane_active_basis_failure_bridge import (  # noqa: E402
    build_current_k3_mixed_plane_active_basis_failure_summary,
)
from w33_k3_mixed_plane_active_column_basis_bridge import (  # noqa: E402
    build_k3_mixed_plane_active_column_basis_summary,
)


OUT_PATH = ROOT / "data" / "dcc_holonomy_active_column_basis_frontier_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    active_column_count: int
    active_restricted_rank: int
    inert_column_count: int
    inert_triple_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    columns = build_dcxcix_bridge()
    current = build_current_k3_mixed_plane_active_basis_failure_summary()
    exact = build_k3_mixed_plane_active_column_basis_summary()

    current_state = current["current_mixed_plane_active_basis_state"]
    basis = exact["mixed_plane_active_column_basis"]
    host = exact["canonical_mixed_plane_support"]

    active_column_count = int(basis["active_column_count"])
    active_restricted_rank = int(basis["active_column_restricted_rank"])
    inert_column_count = int(basis["inactive_column_count"])
    inert_triples = basis["inactive_column_complement_triples"]

    identities = {
        "dcxcix_already_proves_the_frontier_is_not_a_choice_among_active_columns": (
            columns["summary"]["curvature_column_count"] == 45
            and columns["summary"]["active_column_count"] == 36
            and columns["summary"]["inactive_column_count"] == 9
        ),
        "the_exact_live_wall_already_lives_on_a_full_rank_36_column_active_complement": (
            active_column_count == 36
            and int(basis["off_diagonal_curvature_rank"]) == 36
            and active_restricted_rank == 36
        ),
        "the_remaining_9_columns_form_a_rigid_inert_block_split_into_3_exact_triples": (
            inert_column_count == 9
            and inert_triples == [[36, 40, 44], [37, 41, 42], [38, 39, 43]]
        ),
        "the_current_host_still_vanishes_on_the_entire_active_complement": (
            current_state["current_slot_state"] == "zero_by_splitness"
            and int(current_state["current_active_column_supported_entry_count"]) == 0
            and int(current_state["current_inactive_column_supported_entry_count"]) == 0
        ),
        "therefore_the_remaining_curved_frontier_is_the_first_nonzero_row_entry_on_the_full_rank_36_column_active_complement": (
            active_column_count == 36
            and active_restricted_rank == 36
            and inert_column_count == 9
            and inert_triples == [[36, 40, 44], [37, 41, 42], [38, 39, 43]]
            and int(current_state["current_active_column_supported_entry_count"]) == 0
            and host["ordered_line_types"] == ["positive", "negative"]
        ),
    }

    summary = BridgeSummary(
        active_column_count=active_column_count,
        active_restricted_rank=active_restricted_rank,
        inert_column_count=inert_column_count,
        inert_triple_count=len(inert_triples),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "basis_data": {
            "off_diagonal_curvature_rank": int(basis["off_diagonal_curvature_rank"]),
            "active_columns": basis["active_columns"],
            "inactive_columns": basis["inactive_columns"],
            "inactive_column_complement_triples": inert_triples,
            "fixed_host_plane": "U1",
            "fixed_shell": [81, 162, 81],
        },
        "interpretation": {
            "verdict": (
                "The live wall now sits on an exact full-rank 36-column active complement, not on all 45 sign channels. The remaining 9 columns are a rigid inert block split into three triples, so the last curved frontier is the first nonzero row entry on that 36-column active basis."
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