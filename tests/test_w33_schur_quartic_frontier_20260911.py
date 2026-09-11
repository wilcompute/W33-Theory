#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur_quartic_d4_triality_bridge import build_result as build_bridge  # noqa: E402
from w33_schur_incidence_vs_projective_symmetry import build_result as build_symmetry  # noqa: E402


def test_schur_d4_triality_bridge() -> None:
    data = build_bridge()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["configuration"] == {
        "line_roots": 24,
        "triple_points": 32,
        "line_degree": 4,
        "triple_degree": 3,
    }
    assert data["group_bridge"]["WD4_order"] == 192
    assert data["group_bridge"]["triality_order"] == 3
    assert data["group_bridge"]["closure_order"] == 576


def test_bare_incidence_has_full_WF4_symmetry() -> None:
    data = build_symmetry()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["bare_incidence"]["automorphism_order"] == 1152
    assert data["Schur_geometric_half"]["projective_stabilizer_order"] == 576


if __name__ == "__main__":
    test_schur_d4_triality_bridge()
    test_bare_incidence_has_full_WF4_symmetry()
    print("Schur quartic frontier tests passed")
