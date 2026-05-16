from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclviii_octahedral_dobrushin_contraction_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert abs(s["dobrushin_alpha"] - 0.5) < 1e-12
    assert abs(s["one_step_sharp_ratio"] - 0.5) < 1e-12


def test_pair_row_distances_have_max_l1_one() -> None:
    payload = build_bridge()
    vals = [x["l1"] for x in payload["pair_row_distances"]]
    assert abs(max(vals) - 1.0) < 1e-12


def test_multistep_profile_matches_half_power() -> None:
    payload = build_bridge()
    for x in payload["multistep_profile"]:
        assert abs(x["worst_ratio"] - x["alpha_power_t"]) < 1e-9


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
