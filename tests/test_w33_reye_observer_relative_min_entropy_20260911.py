#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_reye_observer_relative_min_entropy import build_result  # noqa: E402


def test_reye_observer_relative_min_entropy() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["point_decoder"]["H_min_bits_given_role"] == 2.0
    assert data["point_decoder"]["H_min_bits_after_side_information"] == 0.0
    assert data["block_decoder"]["H_min_bits_no_offsets"] == 4.0
    assert data["block_decoder"]["H_min_bits_one_offset"] == 2.0
    assert data["block_decoder"]["H_min_bits_two_offsets"] == 0.0
    assert data["independent_observer_cross_check"]["p_guess_no_suppression"] == "1"
    assert data["independent_observer_cross_check"]["p_guess_all_four_outputs_suppressed"] == "1/85"
    assert "does not imply" in data["claim_boundary"]


if __name__ == "__main__":
    test_reye_observer_relative_min_entropy()
    print("Reye observer-relative min-entropy test passed")
