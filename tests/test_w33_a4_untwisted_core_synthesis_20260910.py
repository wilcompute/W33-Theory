from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_a4_untwisted_core_synthesis import build_result  # noqa: E402


def test_local12_is_literal_A4_untwisted_core() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["same_four_label_A4"]["GF4_affine_maps"] == 12
    assert data["same_four_label_A4"]["sets_equal"] is True
    assert data["same_four_label_A4"]["element_order_histogram"] == {"1": 1, "2": 3, "3": 8}
    assert data["stabilizer_ladder"]["A4_section"]["order"] == 12
    assert data["stabilizer_ladder"]["H_prime"]["order"] == 24
    assert data["stabilizer_ladder"]["preimage_A4"]["order"] == 48
    assert data["stabilizer_ladder"]["full_H"]["order"] == 96
    assert "A4" in data["codec_chain"]
    assert "odd S4 parity" in data["twist_boundary"]["twisted_extension"]
