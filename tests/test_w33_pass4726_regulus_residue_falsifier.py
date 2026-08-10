from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "PART_W33_PASS4726_REGULUS_RESIDUE_FALSIFIER.json"


def test_regulus_residue_falsifier():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    assert d["BT794_skew_charts"] == 540
    assert d["distinct_BT794_transversal_sets"] == 540
    assert d["involution_residues"] == 270
    assert d["family_intersection_size"] == 0
    assert d["maximum_cross_intersection"] == 2
    assert d["per_residue_profile_against_540_transversal_sets"] == {"0": 360, "1": 144, "2": 36}
    assert d["per_transversal_profile_against_270_residues"] == {"0": 180, "1": 72, "2": 18}
