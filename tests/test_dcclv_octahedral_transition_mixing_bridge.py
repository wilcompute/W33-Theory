from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclv_octahedral_transition_mixing_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["vertex_count"] == 6
    assert abs(s["stationary_mass_per_vertex"] - (1.0 / 6.0)) < 1e-12
    assert abs(s["second_abs_eigenvalue"] - 0.5) < 1e-12
    assert abs(s["mixing_ratio"] - 0.5) < 1e-12


def test_power_formula_matches_direct() -> None:
    payload = build_bridge()
    for t in range(1, 9):
        direct = payload["power_checks"][str(t)]["direct"]
        modal = payload["power_checks"][str(t)]["modal"]
        n = len(direct)
        for i in range(n):
            for j in range(n):
                assert abs(direct[i][j] - modal[i][j]) < 1e-9


def test_tv_decay_profile() -> None:
    payload = build_bridge()
    mean_tv = payload["mixing_profile"]["mean_tv"]
    ratio = payload["mixing_profile"]["ratio"]
    for t in range(1, 8):
        assert abs(ratio[str(t)] - 0.5) < 1e-8
        assert abs(mean_tv[str(t + 1)] - 0.5 * mean_tv[str(t)]) < 1e-8


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
