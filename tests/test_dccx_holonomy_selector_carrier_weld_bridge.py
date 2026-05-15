from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccx_holonomy_selector_carrier_weld_bridge import build_bridge


def test_dccx_summary_matches_welded_carrier_closure() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["selector_chart_count"] == 2
    assert summary["weld_axis_norm_squared"] == 13122
    assert summary["covariance_trace"] == 13122
    assert summary["normalized_projector_rank"] == 1
    assert summary["seam_kernel_dimension"] == 1


def test_dccx_weld_data_matches_expected_kernel_and_charts() -> None:
    payload = build_bridge()
    weld = payload["carrier_weld"]

    assert sorted(weld["selector_chart_vectors"]) == [[-81, 81], [81, -81]]
    assert weld["chart_outer_average"] == [[6561, -6561], [-6561, 6561]]
    assert weld["covariance"] == [[6561, -6561], [-6561, 6561]]
    assert weld["seam_kernel_direction"] == [1, 1]
    assert weld["seam_kernel_image"] == [0, 0]


def test_dccx_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
