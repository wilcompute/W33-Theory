#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur176_sixteen_line_fibre_structure import build_result  # noqa: E402


def test_schur176_sixteen_line_fibres() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["core_fibres"]["H"]["torsor"] == "V4 x V4 ~= C2^4"
    assert data["core_fibres"]["K"]["torsor"] == "V4 x V4 ~= C2^4"
    assert data["cross_fibres"]["blocks"] == 9
    assert data["cross_fibres"]["lines_per_block"] == 16
    assert data["cross_fibres"]["kernel_order"] == 16
    assert data["cross_fibres"]["contains_order4_scalar"] is True
    assert data["cross_fibres"]["is_C2^4"] is False


if __name__ == "__main__":
    test_schur176_sixteen_line_fibres()
    print("Schur176 sixteen-line fibre test passed")
