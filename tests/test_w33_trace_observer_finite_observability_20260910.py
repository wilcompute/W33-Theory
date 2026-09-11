from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_trace_observer_finite_observability import build_result  # noqa: E402


def test_trace_observer_is_exactly_four_step_observable() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())

    obs = data["trace_trajectory_observability"]
    assert obs["minimal_observability_horizon"] == 4
    assert [r["distinct_trajectory_words"] for r in obs["rows"]] == [15, 57, 77, 85]
    assert [r["residual_entropy_bits_exact"] for r in obs["rows"]] == ["228/85", "72/85", "16/85", "0"]
    assert obs["successive_hidden_information_revealed_bits_exact"] == ["156/85", "56/85", "16/85"]

    cube = data["terminal_ambiguity_cube"]
    assert cube["pair_count_after_three_outputs"] == 8
    assert cube["Q3_edge_count"] == 12

    contrast = data["observer_partition_contrast"]
    assert contrast["trace"]["macrostates"] == 15
    assert contrast["support"]["macrostates"] == 15
    assert contrast["trace"]["is_deterministic_factor"] is False
    assert contrast["support"]["is_deterministic_factor"] is True
    assert contrast["support"]["fibre_size_histogram"] == {"1": 4, "3": 6, "9": 4, "27": 1}
