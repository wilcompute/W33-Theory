from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5798_5799_reye_disjointness_duality.py"
RESULT = ROOT / "data" / "PART_W33_PASS5798_5799_REYE_DISJOINTNESS_DUALITY.json"
MANIFEST = ROOT / "analysis" / "W33_CURRENT_FRONTIER_MANIFEST.tex"


def test_pass5798_5799_byte_exact_replay() -> None:
    before = RESULT.read_bytes()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PASS5798-5799: PASS" in proc.stdout
    assert RESULT.read_bytes() == before


def test_pass5798_5799_frozen_theorems() -> None:
    d = json.loads(RESULT.read_text())
    assert d["status"] == "PASS"
    p = d["pass_5798_heavy_line_reye_copy"]
    assert p["line_heavy_intersection_spectrum"] == [[0, 48], [2, 144]]
    assert p["disjointness_row_degree_on_16_lines"] == 3
    assert p["disjointness_column_degree_on_12_heavies"] == 4
    assert p["heavy_line_point_gram_equals_original_reye_point_gram"]
    q = d["pass_5799_signed_partial_isometry"]
    assert q["B_entries"] == [-3, 1]
    assert q["B_rank"] == 9
    assert q["B_row_and_column_sums_zero"]
    assert q["partial_isometry"] == "U=B/8 has U U^T=E_(W9,line) and U^T U=E_(W9,heavy)"


def test_pass5798_5799_manifest_promotion() -> None:
    needle = r"\input{analysis/PASS5798_5799_reye_disjointness_duality_insert}%"
    assert MANIFEST.read_text().count(needle) == 1
