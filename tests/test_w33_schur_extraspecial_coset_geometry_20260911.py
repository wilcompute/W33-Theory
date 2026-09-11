#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur_extraspecial_coset_geometry import build_result  # noqa: E402


def test_schur_configuration_is_extraspecial_coset_geometry() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["point_torsor"]["order"] == 32
    assert data["point_torsor"]["triple_points"] == 32
    assert data["point_torsor"]["action"] == "regular"
    assert data["line_cosets"]["families"] == [8, 8, 8]
    assert data["line_cosets"]["subgroup_types"] == ["V4", "V4", "V4"]
    assert data["line_cosets"]["pairwise_intersection_orders"] == [1, 1, 1]
    assert data["quadratic_quotient"]["singular_nonzero_count"] == 9
    assert data["outer_action"]["family_permutation_group_order"] == 6
    assert data["outer_action"]["family_kernel_mod_E_order"] == 3


if __name__ == "__main__":
    test_schur_configuration_is_extraspecial_coset_geometry()
    print("Schur extraspecial coset-geometry test passed")
