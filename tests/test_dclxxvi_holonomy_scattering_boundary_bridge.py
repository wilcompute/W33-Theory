from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxvi_holonomy_scattering_boundary_bridge import build_bridge


def test_dclxxvi_summary_matches_expected_sector_ranks() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["stationary_rank"] == 1
    assert summary["fast_rank"] == 24
    assert summary["slow_rank"] == 15



def test_dclxxvi_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxvi_scattering_formulas_match_expected_closed_forms() -> None:
    payload = build_bridge()
    assert payload["scattering_law"] == {
        "cayley": "S(iω) = (iω I - G)(iω I + G)^(-1)",
        "spectral": "S(iω) = P_0 + ((iω-log(4))/(iω+log(4))) P_+ + ((iω-log(5/2))/(iω+log(5/2))) P_-",
        "low_frequency_limit": "lim_{ω->0+} S(iω) = P_0 - P_+ - P_- = J/20 - I",
        "high_frequency_limit": "lim_{ω->∞} S(iω) = I",
    }



def test_dclxxvi_sample_phases_are_unit_magnitude() -> None:
    payload = build_bridge()
    for row in payload["sample_phase_data"].values():
        assert abs(row["fast_magnitude"] - 1.0) < 1e-12
        assert abs(row["slow_magnitude"] - 1.0) < 1e-12
