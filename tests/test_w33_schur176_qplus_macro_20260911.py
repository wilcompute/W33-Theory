#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur176_qplus_macro_skeleton import build_result  # noqa: E402


def test_schur176_has_qplus_ruling_macro_skeleton() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["qplus"]["generator_lines"] == 6
    assert data["qplus"]["singular_projective_points"] == 9
    assert data["schur176_macro"]["surface_partition"] == [3, 3]
    assert data["schur176_macro"]["common_core_blocks"] == 2
    assert data["schur176_macro"]["cross_blocks"] == 9
    assert data["schur176_macro"]["lines_per_block"] == 16
    assert data["schur176_macro"]["total_lines"] == 176
    assert data["schur176_macro"]["lines_per_surface"] == 64
    assert data["schur176_macro"]["surface_group_order"] == 36


if __name__ == "__main__":
    test_schur176_has_qplus_ruling_macro_skeleton()
    print("Schur-176 Qplus macro-skeleton test passed")
