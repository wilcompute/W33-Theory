#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from analysis.bt3471_face_tower_release_certificate import build_certificate

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/PART_BT3458_BT3471_FACE_TOWER_RELEASE_results.json"


def test_live_release_matches_frozen():
    rebuilt = build_certificate()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert rebuilt == frozen
    assert rebuilt["live_boundaries"]["covering_radius"] == [389, 435]
    assert rebuilt["theorems"]["face_tower"] == [240, 120, 40]
    assert rebuilt["theorems"]["crossed_amplitude_algebra_dimension"] == 16
    assert rebuilt["theorems"]["product_code_max_projective_triples_per_dual_coset"] == 4
