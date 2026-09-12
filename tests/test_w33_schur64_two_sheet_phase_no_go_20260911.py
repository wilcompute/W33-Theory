#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur64_two_sheet_phase_no_go import build_result  # noqa: E402


def test_schur64_two_sheet_phase_no_go() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["sheet_torsor"]["order"] == 32
    assert data["sheet_torsor"]["nonabelian"] is True
    assert data["information_reading"]["uniform_sheet_label_bits"] == 1
    assert data["affine_six_bit_test"]["result"] == "NO_GO"


if __name__ == "__main__":
    test_schur64_two_sheet_phase_no_go()
    print("Schur64 two-sheet phase no-go test passed")
