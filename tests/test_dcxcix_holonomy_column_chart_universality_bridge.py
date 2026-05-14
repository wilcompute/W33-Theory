from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxcix_holonomy_column_chart_universality_bridge import build_bridge


def test_dcxcix_summary_matches_column_chart_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["curvature_column_count"] == 45
    assert summary["active_column_count"] == 36
    assert summary["inactive_column_count"] == 9


def test_dcxcix_column_data_matches_universality_claim() -> None:
    payload = build_bridge()
    column_data = payload["column_data"]

    assert column_data["current_supported_column_count"] == 0
    assert column_data["columns_with_both_row_components"] == 36
    assert column_data["columns_with_both_nonzero_values"] == 36
    assert column_data["fixed_host_plane"] == "U1"


def test_dcxcix_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())