#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur_central_phase_reye_quotient import build_result  # noqa: E402


def test_schur_central_phase_quotient_is_dual_reye() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["upstairs"]["triple_points"] == 32
    assert data["upstairs"]["lines"] == 24
    assert data["central_phase"]["center_order"] == 2
    assert data["central_phase"]["hidden_bits_per_point_fibre"] == 1
    assert data["downstairs"]["points"] == 16
    assert data["downstairs"]["blocks"] == 12
    assert data["downstairs"]["incidences"] == 48
    assert data["downstairs"]["degree_profile"] == {3: 16, 4: 12}
    assert data["downstairs"]["same_typed_Q4_Reye"] is False
    assert data["downstairs"]["same_typed_24cell_Reye"] is False
    assert data["downstairs"]["typed_dual_Q4_tomotope_Reye"] is True
    assert data["downstairs"]["typed_dual_24cell_Reye"] is True
    assert data["downstairs"]["typed_orientation"] == (
        "incidence dual of project-native Reye 12_4,16_3"
    )


if __name__ == "__main__":
    test_schur_central_phase_quotient_is_dual_reye()
    print("Schur central-phase dual-Reye quotient test passed")
