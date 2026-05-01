import json
import os
import subprocess
import sys


def test_z3_symmetry_script_runs():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    res = subprocess.run(
        [sys.executable, "tools/check_z3_symmetry.py"], env=env, timeout=30
    )
    assert res.returncode == 0
    assert os.path.exists("data/z3_symmetry.json")


def test_z3_mapping_is_cycle():
    data = json.load(open("data/z3_symmetry.json", encoding="utf-8"))
    assert data.get("found_order3") is True
    mapping = data.get("mapping")
    assert mapping in ([1, 2, 0], [2, 0, 1]), f"mapping is not a 3-cycle: {mapping}"
