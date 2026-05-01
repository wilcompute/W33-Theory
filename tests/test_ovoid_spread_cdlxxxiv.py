"""Phase CDLXXXIV — q=3 spread survives; point-ovoid claim is corrected."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))
from w33_ovoid_spread_bridge import build_ovoid_spread_summary


def test_phase_cdlxxxiv_ovoid_spread() -> None:
    summary = build_ovoid_spread_summary()
    t = summary["q3_spread_ovoid_theorem"]
    assert summary["status"] == "corrected"
    assert t["spread_size_is_q_squared_plus_one"] is True
    assert t["spread_count_is_36"] is True
    assert t["the_explicit_point_graph_has_alpha_7"] is True
    assert t["there_is_no_point_ovoid_of_size_10_at_q_3"] is True
    assert t["the_honest_4_times_10_law_is_line_size_times_spread_size"] is True
