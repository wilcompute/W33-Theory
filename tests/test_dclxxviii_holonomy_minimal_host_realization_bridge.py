from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxviii_holonomy_minimal_host_realization_bridge import build_bridge


def test_dclxxviii_summary_matches_expected_host_split() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["dynamic_rank"] == 39
    assert summary["fast_rank"] == 24
    assert summary["slow_rank"] == 15



def test_dclxxviii_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxviii_minimal_host_description_matches_closed_form() -> None:
    payload = build_bridge()
    assert payload["minimal_host"] == {
        "state_dimension": 39,
        "fast_state_split": 24,
        "slow_state_split": 15,
        "stationary_boundary_channel": 1,
        "state_matrix": "A = diag(-log(4) I_24, -log(5/2) I_15)",
        "input_map": "B = [U_+^T; U_-^T]",
        "output_map": "C = [U_+ U_-]",
    }
