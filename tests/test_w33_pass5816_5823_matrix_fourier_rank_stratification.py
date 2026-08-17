from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5816_5823_matrix_fourier_rank_stratification.py"
RESULT = ROOT / "data" / "PART_W33_PASS5816_5823_MATRIX_FOURIER_RANK_STRATIFICATION.json"
MANIFEST = ROOT / "analysis" / "W33_CURRENT_FRONTIER_MANIFEST.tex"


def test_pass5816_5823_byte_exact_replay() -> None:
    before = RESULT.read_bytes()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PASS5816-5823: PASS" in proc.stdout
    assert RESULT.read_bytes() == before


def test_pass5816_5823_frozen_theorems() -> None:
    d = json.loads(RESULT.read_text())
    assert d["status"] == "PASS"
    assert d["pass_5816_line_walsh_decomposition"]["rank_stratum_sizes"] == [1, 9, 6]
    assert d["pass_5817_rank_one_common_W9"]["label_count"] == 9
    assert d["pass_5817_rank_one_common_W9"]["exact_intertwiners"] == [
        "R^T u_(w,phi)=v_Y",
        "H^T u_(w,phi)=-2 h_(w,phi)",
        "D h_(w,phi)=v_Y",
    ]
    assert d["pass_5818_line_only_V6"]["dimension"] == 6
    assert d["pass_5818_line_only_V6"]["kernel_identity"] == "V6 = ker(R) = ker(D^T) inside the 16-line carrier"
    p = d["pass_5819_affine_monomial_action"]
    assert p["verified_pairs"] == 9216
    assert p["rank_one_character_norm"] == 1
    assert p["rank_two_character_norm"] == 1
    assert p["rank_one_rank_two_character_inner_product"] == 0
    assert d["pass_5821_transpose_fourier_action"]["rank_strata_preserved"]
    assert d["pass_5822_projective_rank_quadric"]["det_zero_rank_one_points"] == 9
    assert d["pass_5822_projective_rank_quadric"]["det_one_invertible_points"] == 6


def test_pass5816_5823_promoted_once() -> None:
    needle = r"\input{analysis/PASS5816_5823_matrix_fourier_rank_stratification_insert}%"
    assert MANIFEST.read_text().count(needle) == 1
