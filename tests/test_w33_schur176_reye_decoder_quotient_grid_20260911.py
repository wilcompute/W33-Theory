#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur176_reye_decoder_quotient_grid_bridge import build_result  # noqa: E402


def test_schur176_macro_is_decoder_quotient_grid() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["decoder_group"]["kernel_order"] == 16
    assert data["decoder_group"]["quotient_order"] == 36
    assert data["decoder_group"]["order"] == 576
    assert data["quotient_grid"]["cells"] == 9
    assert data["fibre_frontier"]["geometric_lines_per_macro_block"] == 16
    assert data["fibre_frontier"]["status"] == "UNPROVED_OBJECTWISE_LIFT"


if __name__ == "__main__":
    test_schur176_macro_is_decoder_quotient_grid()
    print("Schur176 / Reye decoder quotient-grid test passed")
