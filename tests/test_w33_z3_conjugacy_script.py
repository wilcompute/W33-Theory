import glob
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest


def test_run_conjugacy_on_latest_candidates(tmp_path):
    # find latest candidates file
    cand_files = sorted(
        glob.glob("checks/PART_CVII_z3_candidates_*.json"),
        key=lambda p: Path(p).stat().st_mtime,
    )
    if not cand_files:
        pytest.skip("optional z3 candidates file is absent from checks/")
    cand_file = cand_files[-1]

    # run the script with explicit candidates file and a test log
    log_file = tmp_path / "z3_conj_test.log"
    cmd = [
        sys.executable,
        "scripts/w33_z3_conjugacy_classes.py",
        "--candidates-file",
        str(cand_file),
        "--log-file",
        str(log_file),
    ]
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert proc.returncode == 0, f"Conjugacy script failed: {proc.stderr}"

    # check that a new conjugacy JSON was written
    conj_files = sorted(
        glob.glob("checks/PART_CVII_z3_conjugacy_*.json"),
        key=lambda p: Path(p).stat().st_mtime,
    )
    assert conj_files, "No conjugacy file produced"
    conj = json.loads(open(conj_files[-1], encoding="utf-8").read())

    # basic sanity checks
    assert conj.get("Gsize") == 25920
    cand_data = json.loads(open(cand_file, encoding="utf-8").read())
    assert len(conj.get("results", [])) == len(cand_data.get("candidates", []))
    # ensure indices are contiguous starting at 1
    idxs = [int(r["index"]) for r in conj.get("results", [])]
    assert idxs == list(range(1, 1 + len(idxs)))
    time.sleep(0.1)  # give filesystem time to settle
