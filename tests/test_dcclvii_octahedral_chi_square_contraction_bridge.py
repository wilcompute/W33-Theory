from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclvii_octahedral_chi_square_contraction_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert abs(s["initial_chi2"] - 5.0) < 1e-12
    assert abs(s["first_step_chi2"] - 0.5) < 1e-12
    assert abs(s["contraction_ratio"] - 0.25) < 1e-12


def test_quarter_ratio_decay() -> None:
    payload = build_bridge()
    ratios = payload["ratios"]
    for t in range(1, 9):
        assert abs(ratios["l2sq_ratio"][str(t)] - 0.25) < 1e-9
        assert abs(ratios["chi2_ratio"][str(t)] - 0.25) < 1e-9


def test_closed_form_match() -> None:
    payload = build_bridge()
    tl = payload["timeline"]
    cf = payload["closed_form"]
    for t in range(1, 10):
        assert abs(tl[t]["l2sq_to_uniform"] - cf["l2sq"][str(t)]) < 1e-8
        assert abs(tl[t]["chi2_to_uniform"] - cf["chi2"][str(t)]) < 1e-8


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
