import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DM_DATA_DIR = ROOT / "data" / "ams_obs" / "ams_pamela_observations"
REQUIRED_DM_DATA = (
    DM_DATA_DIR / "AMS02_H-PRL2021_heliosphere.dat",
    DM_DATA_DIR / "PAMELA_H-ApJ2013_heliosphere.dat",
)


def missing_dm_data():
    return [path for path in REQUIRED_DM_DATA if not path.exists()]


def run_script(name):
    path = ROOT / name
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        cwd=ROOT,
    )
    assert (
        result.returncode == 0
    ), f"Script {name} failed:\n{result.stdout}\n{result.stderr}"
    return result.stdout


@pytest.mark.skipif(
    missing_dm_data(),
    reason="optional AMS/PAMELA observation data is absent from clean checkout",
)
def test_dm_mass_fit_runs():
    out = run_script("THEORY_PART_CLXII_DM_MASS_FIT.py")
    assert "Best-fit DM mass" in out
    assert "AMS-02" in out
