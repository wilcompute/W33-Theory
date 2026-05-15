from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxii_closure_clock_codec_flow_bridge import build_bridge, codec_flow_from_clock


def test_codec_flow_definition() -> None:
    tau = [1, 1, 2, 3, 3]
    flow = codec_flow_from_clock(12, tau)
    assert flow == [24, 24, 48, 96, 96]


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["base_codec_scale"] == 12
    assert s["steps"] == 7
    assert s["final_tau"] == 5
    assert s["final_scale"] == 384
    assert s["reached_96"] is True
    assert s["reached_192"] is True


def test_flow_contains_ladder_levels() -> None:
    payload = build_bridge()
    levels = payload["codec_flow"]["unique_levels"]
    for x in [12, 24, 48, 96, 192]:
        assert x in levels
    assert payload["codec_flow"]["values_with_base"][0] == 12


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
