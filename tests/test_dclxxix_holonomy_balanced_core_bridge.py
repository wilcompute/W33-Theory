from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxix_holonomy_balanced_core_bridge import build_bridge


def test_dclxxix_summary_matches_expected_balanced_split() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["state_dimension"] == 39
    assert summary["retained_core_rank"] == 15
    assert summary["discarded_rank"] == 24



def test_dclxxix_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxix_balanced_core_description_matches_closed_form() -> None:
    payload = build_bridge()
    assert payload["balanced_core"] == {
        "fast_hankel_singular_value": "1/(2 log(4))",
        "slow_hankel_singular_value": "1/(2 log(5/2))",
        "retained_rank": 15,
        "discarded_rank": 24,
        "retained_transfer": "R_slow(s) = P_-/(s+log(5/2))",
        "discarded_transfer": "R_fast(s) = P_+/(s+log(4))",
    }
