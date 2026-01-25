import subprocess
import sys
import pytest


def run_script(path):
    res = subprocess.run([sys.executable, path], capture_output=True, text=True)
    # For debugging on failure, include output
    if res.returncode != 0:
        print('STDOUT:\n', res.stdout)
        print('STDERR:\n', res.stderr)
    return res.returncode, res.stdout, res.stderr


def test_proof_minus_one_exec():
    rc, out, err = run_script('src/PROOF_MINUS_ONE.py')
    assert rc == 0


def test_the_proof_exec():
    rc, out, err = run_script('extracted/claude_workspace/claude_workspace/THE_PROOF.py')
    assert rc == 0
