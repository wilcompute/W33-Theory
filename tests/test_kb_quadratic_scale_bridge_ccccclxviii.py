"""Part CCCCCLXVIII -- K-B quadratic scale bridge."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "PART_CCCCCLXVIII_kb_quadratic_scale_bridge.py"
OUT = ROOT / "data" / "PART_CCCCCLXVIII_kb_quadratic_scale_bridge_results.json"


def _run_script() -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert OUT.exists()
    return json.loads(OUT.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    data = _run_script()
    assert data["part"] == "CCCCCLXVIII"


def test_checks_pass() -> None:
    data = _run_script()
    assert data["all_checks_pass"] is True
    assert all(data["checks"].values())


def test_reduced_functional_coefficients() -> None:
    data = _run_script()
    assert data["reduced_quadratic_functional"]["formula"] == "S2_red(x;y,h) = (2-16x)y + (1-16x)h"
    assert data["coefficients"]["y"] == {"constant_term": "2", "x_coefficient": "-16"}
    assert data["coefficients"]["h"] == {"constant_term": "1", "x_coefficient": "-16"}


def test_critical_roots() -> None:
    data = _run_script()
    assert data["critical_roots"]["y_coefficient_root"] == "1/8"
    assert data["critical_roots"]["h_coefficient_root"] == "1/16"
