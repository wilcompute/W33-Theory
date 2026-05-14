from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxi_holonomy_markov_recurrence_bridge import build_bridge


def test_dclxxi_summary_matches_expected_recurrence_data() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["recurrence_coeff_num"] == 13
    assert summary["recurrence_coeff_den"] == 20
    assert summary["recurrence_const_num"] == 1
    assert summary["recurrence_const_den"] == 10


def test_dclxxi_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxxi_recurrence_roots_and_rank_are_exact() -> None:
    payload = build_bridge()
    assert payload["recurrence"] == {
        "formula": "X_{t+2} = (13/20) X_{t+1} - (1/10) X_t",
        "roots": ["1/4", "2/5"],
        "characteristic_discriminant": "9/400",
        "minimality_rank": 2,
    }


def test_dclxxi_first_two_channel_rows_match_expected_values() -> None:
    payload = build_bridge()
    rows = payload["channel_rows"]
    assert rows[0] == {"t": 1, "diagonal": "3/10", "edge": "-1/40", "nonedge": "0"}
    assert rows[1] == {"t": 2, "diagonal": "39/400", "edge": "-11/800", "nonedge": "1/400"}