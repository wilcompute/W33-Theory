"""Tests for the stochastic CKM optimizer (optimize_ckm_vevs2.py)."""

import os
import re
import subprocess
import sys


def test_optimize2_improves():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    # ensure baseline data exists
    subprocess.run(
        [sys.executable, "scripts/w33_yukawa_blocks.py"], env=env, cwd=os.getcwd()
    )
    # run optimizer 2
    res = subprocess.run(
        [
            sys.executable,
            "scripts/optimize_ckm_vevs2.py",
            "--trials",
            "2000",
            "--seed",
            "42",
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"optimizer2 failed: {res.stderr}"
    out = res.stdout
    m = re.search(r"base err ([0-9\.]+)", out)
    assert m, "no baseline error printed"
    base = float(m.group(1))
    m2 = re.search(r"best err ([0-9\.]+)", out)
    assert m2, "no best error printed"
    best = float(m2.group(1))
    assert best < base, "optimizer2 did not improve"
    assert best < 0.1, f"improvement too small: {best:.3f}"
