from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(path: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(ROOT / path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return completed.stdout


def test_bt2962_exact_two_graph_certificate() -> None:
    stdout = run_script("analysis/bt2962_oam_holonomy_s6_two_graph.py")
    assert "PASS 10 / 10" in stdout
    result = json.loads(
        (ROOT / "data/PART_BT2962_OAM_HOLONOMY_S6_TWO_GRAPH_results.json").read_text()
    )
    assert result["spreads"] == 36
    assert result["classification"]["automorphism_group_order"] == 720
    assert result["odd_curvature_design"]["parameters"] == "2-(10,3,4)"
    assert all(result["checks"].values())


def test_bt2965_exact_route_code_certificate() -> None:
    stdout = run_script("analysis/bt2965_curvature_route_code.py")
    assert "PASS 10 / 10" in stdout
    result = json.loads(
        (ROOT / "data/PART_BT2965_CURVATURE_ROUTE_CODE_results.json").read_text()
    )
    assert result["code"]["parameters"] == "[45,9,9]_2"
    assert result["raw_registers"]["independent_syndrome_bits"] == 36
    assert result["code"]["correctable_fault_weight_modulo_gauge"] == 4
    assert all(result["checks"].values())


def test_blueprint_index_integrator_is_idempotent(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "holonet_machine_blueprint.tex").write_text(
        "\\documentclass{article}\n\\begin{document}\nX\n\\end{document}\n"
    )
    (tmp_path / "docs/index.html").write_text(
        "<!doctype html><html><body><main>X</main></body></html>\n"
    )
    tool = ROOT / "tools/integrate_bt2962_bt2965_blueprint_index.py"
    first = subprocess.run(
        [sys.executable, str(tool), "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    first_result = json.loads(first.stdout)
    assert first_result["blueprint_changed"]
    assert first_result["index_changed"]

    second = subprocess.run(
        [sys.executable, str(tool), "--root", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    second_result = json.loads(second.stdout)
    assert not second_result["blueprint_changed"]
    assert not second_result["index_changed"]

    subprocess.run(
        [sys.executable, str(tool), "--root", str(tmp_path), "--check"],
        check=True,
        capture_output=True,
        text=True,
    )
