from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxcvii_holonomy_off_diagonal_curvature_frontier_bridge import build_bridge


def test_dcxcvii_summary_matches_curved_frontier_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["current_off_diagonal_curvature_rank"] == 0
    assert summary["exact_off_diagonal_curvature_rank"] == 36
    assert summary["exact_off_diagonal_support_rows"] == 4046


def test_dcxcvii_frontier_data_matches_fixed_host_package() -> None:
    payload = build_bridge()
    frontier = payload["frontier_data"]

    assert frontier["fixed_host_plane"] == "U1"
    assert frontier["fixed_shell"] == [81, 162, 81]
    assert frontier["exact_off_diagonal_curvature_rank"] == 36
    assert frontier["exact_off_diagonal_curvature_support_rows"] == 4046


def test_dcxcvii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())