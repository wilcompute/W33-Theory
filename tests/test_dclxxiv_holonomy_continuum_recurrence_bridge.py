from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxiv_holonomy_continuum_recurrence_bridge import build_bridge


def test_dclxxiv_summary_matches_expected_shape() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["stationary_rank"] == 1
    assert summary["recurrence_order"] == 2



def test_dclxxiv_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxiv_ode_and_sampled_discrete_coefficients_match_closed_forms() -> None:
    payload = build_bridge()
    assert payload["continuum_recurrence"] == {
        "ode": "X'' + log(10) X' + log(4)log(5/2) X = 0",
        "fast_rate": payload["continuum_recurrence"]["fast_rate"],
        "slow_rate": payload["continuum_recurrence"]["slow_rate"],
        "sampled_discrete_sum": "13/20",
        "sampled_discrete_product": "1/10",
    }



def test_dclxxiv_channel_samples_have_all_three_channel_types() -> None:
    payload = build_bridge()
    samples = payload["channel_samples"]
    assert set(samples) == {"diag", "edge", "nonedge"}
    for channel in samples.values():
        assert len(channel["x"]) == 5
        assert len(channel["x_prime"]) == 5
        assert len(channel["x_second"]) == 5
