#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_schur64_e7_threequbit_pauli_objectwise_bridge import build_result  # noqa: E402


def test_objectwise_schur64_e7_pauli_bridge() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["standard_coordinate_order"] == ["x1", "z1", "x2", "z2", "x3", "z3"]
    assert data["census"] == {
        "projective_threequbit_Pauli_directions": 63,
        "pair_relations_checked": 1953,
        "commuting_pairs": 945,
        "anticommuting_pairs": 1008,
        "closed_anticommuting_XOR_triangles": 336,
    }
    assert len(data["dictionary"]) == 63
    assert len({tuple(row["e7_antipodal_root_pair_representative"]) for row in data["dictionary"]}) == 63
    assert len({row["pauli_word_projective"] for row in data["dictionary"]}) == 63


if __name__ == "__main__":
    test_objectwise_schur64_e7_pauli_bridge()
    print("Schur64/E7 objectwise Pauli bridge test passed")
