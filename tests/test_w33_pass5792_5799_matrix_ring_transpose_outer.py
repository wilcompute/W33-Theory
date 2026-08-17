from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5792_5799_matrix_ring_transpose_outer.py"
RESULT = ROOT / "data" / "PART_W33_PASS5792_5799_MATRIX_RING_TRANSPOSE_OUTER.json"


def test_pass5792_5799_exact_replay() -> None:
    before = RESULT.read_bytes()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PASS5792-5799: PASS" in proc.stdout
    assert RESULT.read_bytes() == before
    d = json.loads(RESULT.read_text())
    assert d["status"] == "PASS"
    assert d["pass_5792_affine_left_right_group"]["group_order"] == 576
    assert d["pass_5792_affine_left_right_group"]["matrix_units"] == 6
    assert d["pass_5792_affine_left_right_group"]["matrix_singular_elements"] == 10
    assert d["pass_5793_point_heavy_hyperplane_model"]["heavy_supports_match_frozen_q5_blocks"]
    assert d["pass_5794_character_replay"]["permutation_character_gram_P_H_L"] == [
        [3, 2, 2],
        [2, 3, 2],
        [2, 2, 3],
    ]
    assert d["pass_5794_character_replay"]["sign_twisted_point_pairings_with_P_H_L"] == [0, 0, 0]
    assert d["pass_5795_transpose_normalizer"]["transpose_normalizes_affine_group"]
    assert not d["pass_5795_transpose_normalizer"]["transpose_is_inside_affine_group"]
    assert d["pass_5796_outer_carrier_intertwiner"]["transpose_exchanges_translation_stabilizer_types"]
