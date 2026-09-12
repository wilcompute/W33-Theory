#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_e7_d4_presymplectic_reye_normal_form import build_result  # noqa: E402


def test_e7_selected_d4_has_presymplectic_pauli_reye_normal_form() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    nf = data["normal_form"]
    assert nf["span_order"] == 16
    assert nf["span_dimension"] == 4
    assert nf["restricted_symplectic_rank"] == 2
    assert nf["radical_order"] == 4
    assert nf["radical_words"] == ["III", "IIX", "IZI", "IZX"]
    assert data["coset_geometry"]["anticommutation_graph"] == "K4,4,4"
    assert data["Reye"]["points"] == 12
    assert data["Reye"]["blocks"] == 16
    assert data["Reye"]["incidences"] == 48
    assert data["Reye"]["typed_Q4_tomotope_isomorphism"] is True
    assert data["Reye"]["typed_24cell_isomorphism"] is True


if __name__ == "__main__":
    test_e7_selected_d4_has_presymplectic_pauli_reye_normal_form()
    print("E7 D4 presymplectic Reye normal-form test passed")
