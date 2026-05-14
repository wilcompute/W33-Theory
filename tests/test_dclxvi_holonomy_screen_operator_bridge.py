from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxvi_holonomy_screen_operator_bridge import build_bridge


def test_dclxvi_summary_matches_design_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["field_order"] == 3
    assert summary["point_count"] == 40
    assert summary["screen_count"] == 40
    assert summary["screen_size"] == 13
    assert summary["point_pair_screen_count"] == 4
    assert summary["screen_pair_intersection_count"] == 4


def test_dclxvi_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxvi_operator_statistics_match_adjacency_closure() -> None:
    payload = build_bridge()
    stats = payload["operator_statistics"]

    assert stats["screen_row_sums"] == [13]
    assert stats["screen_column_sums"] == [13]
    assert stats["distinct_offdiagonal_screen_intersections"] == [4]
    assert stats["distinct_offdiagonal_point_pair_counts"] == [4]


def test_dclxvi_spectrum_matches_shifted_w33_spectrum() -> None:
    payload = build_bridge()
    assert payload["operator_statistics"]["spectrum"] == {-3: 15, 3: 24, 13: 1}