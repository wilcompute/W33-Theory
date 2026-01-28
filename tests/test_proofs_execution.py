import subprocess
import sys
from pathlib import Path

import pytest


def run_script(path):
    res = subprocess.run([sys.executable, path], capture_output=True, text=True)
    # For debugging on failure, include output
    if res.returncode != 0:
        print("STDOUT:\n", res.stdout)
        print("STDERR:\n", res.stderr)
    return res.returncode, res.stdout, res.stderr


def test_proof_minus_one_exec():
    rc, out, err = run_script("src/PROOF_MINUS_ONE.py")
    assert rc == 0


def test_the_proof_exec():
    path = "extracted/claude_workspace/claude_workspace/THE_PROOF.py"
    if not Path(path).exists():
        pytest.skip(f"{path} not found")
    rc, out, err = run_script(path)
    assert rc == 0
