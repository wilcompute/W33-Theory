#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur_reye_288_action_bridge import build_result  # noqa: E402


def test_schur_reye_action_is_288_not_576() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["orders"]["Schur_half_signed_root_stabilizer"] == 576
    assert data["orders"]["antipodal_kernel"] == 2
    assert data["orders"]["Schur_induced_Reye_group"] == 288
    assert data["orders"]["full_typed_Reye_automorphism_group"] == 576
    assert data["orders"]["index"] == 2
    assert "NOT" in data["correction"]


if __name__ == "__main__":
    test_schur_reye_action_is_288_not_576()
    print("Schur/Reye order-288 action bridge test passed")
