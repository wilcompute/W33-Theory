from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxiii_spatial_closure_time_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["spatial_dimension"] == 3
    assert s["time_dimension"] == 1
    assert s["total_state_dimension"] == 4
    assert s["base_codec_scale"] == 12
    assert s["final_clock_value"] == 5
    assert s["final_scale"] == 384


def test_spatial_basis_and_time_channel() -> None:
    payload = build_bridge()
    split = payload["spatial_time_split"]
    assert split["spatial_basis"] == ["B23", "B31", "B12"]
    assert split["time_channel"] == "tau = log2(C/12)"
    assert split["state_dimension"] == [3, 1]


def test_logarithmic_time_matches_clock_history() -> None:
    payload = build_bridge()
    history = payload["state_history"]
    assert [step["tau"] for step in history] == [step["log2_scale_over_12"] for step in history]
    assert history[0]["scale"] == 24
    assert history[-1]["scale"] == 384


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
