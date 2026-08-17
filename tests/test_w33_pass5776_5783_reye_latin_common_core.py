from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5776_5783_reye_latin_common_core.py"
RESULT = ROOT / "data" / "PART_W33_PASS5776_5783_REYE_LATIN_COMMON_CORE.json"
MANIFEST = ROOT / "analysis" / "W33_CURRENT_FRONTIER_MANIFEST.tex"
INSERT = ROOT / "analysis" / "PASS5776_5783_reye_latin_common_core_insert.tex"


def test_pass5776_5783_replay_is_byte_exact() -> None:
    before = RESULT.read_bytes()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PASS5776-5783: PASS" in proc.stdout
    assert RESULT.read_bytes() == before


def test_pass5776_5783_frozen_theorems() -> None:
    d = json.loads(RESULT.read_text())
    assert d["status"] == "PASS"
    assert d["pass_5776_dual_incidence_gram"]["K9_rank"] == 9
    assert d["pass_5776_dual_incidence_gram"]["K9_quadratic_identity"] == "K_9^2 = 4 K_9"
    assert d["pass_5777_intrinsic_three_by_four"]["component_sizes"] == [4, 4, 4]
    assert d["pass_5778_reye_td34_klein_latin"]["normalized_table"] == [
        [0, 1, 2, 3],
        [1, 0, 3, 2],
        [2, 3, 0, 1],
        [3, 2, 1, 0],
    ]
    assert d["pass_5778_reye_td34_klein_latin"]["intercalate_count"] == 12
    assert d["pass_5779_balanced_six_set_census"]["contained_reye_line_count_spectrum"] == [
        [0, 12],
        [2, 192],
        [4, 12],
    ]
    assert d["pass_5779_balanced_six_set_census"]["heavy_is_exact_zero_line_class"]
    assert d["pass_5779_balanced_six_set_census"]["heavy_complements_are_intercalate_supports"]
    assert d["pass_5780_common_module"]["point_module_dimensions"] == [1, 9, 2]
    assert d["pass_5780_common_module"]["heavy_module_dimensions"] == [1, 9, 2]
    assert d["pass_5780_common_module"]["line_module_dimensions"] == [1, 9, 6]
    assert d["pass_5781_outer_vs_sign"]["sign_twisted_point_self_inner_product"] == 0
    assert d["pass_5781_outer_vs_sign"]["sign_twisted_point_heavy_inner_product"] == 0
    assert d["pass_5781_outer_vs_sign"]["sign_twisted_point_line_inner_product"] == 0


def test_pass5776_5783_is_promoted_once() -> None:
    needle = r"\input{analysis/PASS5776_5783_reye_latin_common_core_insert}%"
    text = MANIFEST.read_text()
    assert text.count(needle) == 1
    assert INSERT.exists()


def test_all_three_canonical_wrappers_receive_the_shared_manifest() -> None:
    for name in ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex"):
        text = (ROOT / name).read_text()
        assert r"\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}%" in text
