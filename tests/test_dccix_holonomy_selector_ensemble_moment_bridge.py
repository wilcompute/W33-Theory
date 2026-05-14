from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccix_holonomy_selector_ensemble_moment_bridge import build_bridge


def test_dccix_summary_matches_ensemble_kernel() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["selector_state_count"] == 2
    assert summary["mean_vector"] == [0.0, 0.0]
    assert summary["covariance_trace"] == 13122
    assert summary["covariance_determinant"] == 0
    assert summary["covariance_rank"] == 1


def test_dccix_covariance_matrix_and_spectrum_are_exact() -> None:
    payload = build_bridge()
    ensemble = payload["ensemble"]

    assert ensemble["covariance"] == [[6561, -6561], [-6561, 6561]]
    assert ensemble["eigenvalues"] == [13122, 0]


def test_dccix_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())