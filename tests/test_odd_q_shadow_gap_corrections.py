"""Regression tests for the GAP-owned odd-q shadow corrections."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_odd_q_shadow_correction_capstone.g"
CERTIFICATE = ROOT / "data" / "w33_odd_q_shadow_correction_capstone.json"


@lru_cache(maxsize=1)
def _certificate() -> dict:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for the odd-q correction capstone"
    result = subprocess.run(
        [gap, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert "Odd-q shadow correction capstone: PASS" in result.stdout
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_gap_owns_the_correct_quadratic_and_polar_forms() -> None:
    cert = _certificate()
    assert cert["status"] == "PASS"
    assert cert["uniform_construction"]["quadratic_refinement"] == (
        "q(x)=x^T A x/4 mod 2"
    )
    assert cert["uniform_construction"]["polar_form"] == (
        "B(x,y)=x^T A y/2 mod 2"
    )
    assert cert["surviving_theorems"]["point_code_C_subset_imA"] is True
    assert cert["refutations"]["half_quadratic_refinement"] is False


def test_full_group_mtx_anchor_table() -> None:
    rows = {row["q"]: row for row in _certificate()["anchor_table"]}
    assert rows[3]["Sp4_order"] == 51840
    assert rows[3]["MTX_factors"] == [8]
    assert rows[3]["polar_rank"] == 8
    assert rows[5]["Sp4_order"] == 9360000
    assert rows[5]["MTX_factors"] == [24]
    assert rows[5]["polar_rank"] == 0
    assert rows[7]["Sp4_order"] == 276595200
    assert rows[7]["MTX_factors"] == [24, 24]
    assert rows[7]["polar_rank"] == 48


def test_historical_entry_points_are_thin_gap_launchers() -> None:
    for name in (
        "w33_pass194_odd_q_shadow_ladder.py",
        "w33_pass198_layer_law_q7.py",
        "w33_pass199_q7_shadow_identity.py",
        "w33_pass200_q5_golay_leech_shadow.py",
        "w33_pass205_q7_composition_series.py",
    ):
        source = (ROOT / "analysis" / name).read_text(encoding="utf-8")
        assert "subprocess.run" in source
        assert '"gap", "-q"' in source
        assert "numpy" not in source
        assert "sympy" not in source


def test_odd_q_corrections_are_visible_and_scoped() -> None:
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    normalized_paper = paper.replace("\\_", "_")
    assert "w33_odd_q_shadow_correction_capstone.g" in normalized_paper
    assert "q=5:[24]" in index
    assert "q=7:[24,24]" in index
    assert "higher residue classes remain coefficient-law predictions" in index
    assert "No ``all higher rungs'' theorem is claimed" in paper
