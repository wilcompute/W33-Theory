import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

OUTPUT = Path("RG_MASSES.json")
SCRIPT = Path("exploration") / "RG_PRECISION_MASSES.py"


@pytest.fixture(scope="module")
def rg_masses_data():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    OUTPUT.unlink(missing_ok=True)
    res = subprocess.run(
        [sys.executable, str(SCRIPT)], env=env, capture_output=True, text=True
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert OUTPUT.exists()
    return json.loads(OUTPUT.read_text(encoding="utf-8"))


def test_rg_script_runs(rg_masses_data):
    assert "masses_predicted" in rg_masses_data


def test_rg_output_structure(rg_masses_data):
    data = rg_masses_data
    assert "masses_predicted" in data
    preds = data["masses_predicted"]
    # ensure top mass prediction is nonzero numeric
    assert "m_t" in preds and isinstance(preds["m_t"], float)
    assert preds["m_t"] != 0.0
    # ratios dictionary should exist
    assert "W33_ratios" in data and isinstance(data["W33_ratios"], dict)
