#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_projective_phase_fibre_dichotomy import build_result  # noqa: E402


def test_projective_phase_fibre_dichotomy() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["observable_group"]["order"] == 288
    assert data["observable_group"]["GAP_id"] == "SmallGroup(288,1025)"

    w = data["W33_completion"]
    c = data["complex_Clifford_completion"]
    assert (w["order"], w["center_order"], w["derived_order"], w["swap_order"]) == (576, 2, 96, 2)
    assert (c["order"], c["center_order"], c["derived_order"], c["special_swap_order"]) == (1152, 4, 96, 8)
    assert w["element_orders"] == {1: 1, 2: 43, 3: 80, 4: 84, 6: 272, 12: 96}
    assert c["element_orders"] == {1: 1, 2: 31, 3: 80, 4: 32, 6: 176, 8: 192, 12: 256, 24: 384}
    assert w["projective_fibre_bits_uniform"] == 1.0
    assert c["projective_fibre_bits_uniform"] == 2.0


if __name__ == "__main__":
    test_projective_phase_fibre_dichotomy()
    print("projective phase-fibre dichotomy focused test passed")
