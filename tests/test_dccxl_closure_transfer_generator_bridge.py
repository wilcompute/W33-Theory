from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxl_closure_transfer_generator_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert s["one_step_weight_numerator"] == 1
    assert s["one_step_weight_denominator"] == 2
    assert s["nilpotent_index"] == 6
    assert s["maximal_propagation_denominator"] == 32


def test_generator_matrix_has_half_shift_form() -> None:
    payload = build_bridge()
    G = payload["generator_matrix"]
    assert G[0][1] == {"numerator": 1, "denominator": 2}
    assert G[1][2] == {"numerator": 1, "denominator": 2}
    assert G[4][5] == {"numerator": 1, "denominator": 2}
    assert G[0][0] == {"numerator": 0, "denominator": 1}
    assert G[5][5] == {"numerator": 0, "denominator": 1}


def test_generator_powers_match_expected_weights() -> None:
    payload = build_bridge()
    powers = payload["generator_powers"]
    assert powers["G^0"][0][0] == {"numerator": 1, "denominator": 1}
    assert powers["G^1"][0][1] == {"numerator": 1, "denominator": 2}
    assert powers["G^2"][0][2] == {"numerator": 1, "denominator": 4}
    assert powers["G^5"][0][5] == {"numerator": 1, "denominator": 32}
    assert all(entry == {"numerator": 0, "denominator": 1} for row in powers["G^6"] for entry in row)


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
