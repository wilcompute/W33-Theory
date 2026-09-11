#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_swap_extension_class_localization import build_result  # noqa: E402


def test_swap_pullback_distinguishes_extension_classes() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["W33_restriction"]["structure"] == "C2 x C2"
    assert data["Clifford_residual_restriction"]["structure"] == "C4"
    assert data["W33_restriction"]["element_orders"] == {1: 1, 2: 3}
    assert data["Clifford_residual_restriction"]["element_orders"] == {1: 1, 2: 1, 4: 2}


if __name__ == "__main__":
    test_swap_pullback_distinguishes_extension_classes()
    print("swap extension-class localization focused test passed")
