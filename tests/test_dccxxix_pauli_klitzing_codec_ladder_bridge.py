from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxix_pauli_klitzing_codec_ladder_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["q_value"] == 3
    assert s["pauli_valency_12"] == 12
    assert s["klitzing_rectified_12"] == 12
    assert s["mod_b_omnitruncated_96"] == 96
    assert s["mod_a_omnitruncated_192"] == 192


def test_ladders_match_expected() -> None:
    payload = build_bridge()
    ladders = payload["ladders"]
    assert ladders["mod_b_direct"] == [12, 24, 48, 96]
    assert ladders["mod_a_sheet_lift"] == [24, 48, 96, 192]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
