from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxv_holonomy_transfer_function_bridge import build_bridge


def test_dclxxv_summary_matches_expected_shape() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["stationary_rank"] == 1
    assert summary["dynamic_rank"] == 39
    assert summary["denominator_degree"] == 2



def test_dclxxv_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxv_transfer_function_strings_match_closed_forms() -> None:
    payload = build_bridge()
    assert payload["transfer_function"] == {
        "spectral": "R(s) = P_+/(s+log(4)) + P_-/(s+log(5/2))",
        "tripotent": "R(s) = ((s+log(10)/2) M^2 - (log(8/5)/2) M)/((s+log(10)/2)^2 - (log(8/5)/2)^2)",
        "ode": "R(s) = ((s+log(10))X(0)+X'(0))/(s^2 + log(10)s + log(4)log(5/2))",
    }



def test_dclxxv_samples_cover_multiple_positive_frequencies() -> None:
    payload = build_bridge()
    assert payload["sample_points"] == [0.25, 0.5, 1.0, 2.0]
