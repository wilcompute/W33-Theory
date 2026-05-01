import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "exploration" / "RG_PRECISION_MASSES.py"


def run_script(args):
    cmd = [sys.executable, str(SCRIPT)] + args
    proc = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return proc.stdout, proc.stderr, proc.returncode


def test_required_ratio():
    # run with default ratio and capture the required ratio line
    out, err, code = run_script(["--mtmb", "40"])
    assert code == 0
    # look for "required m_t/m_b ratio" in output
    for line in out.splitlines():
        if "required m_t/m_b ratio" in line:
            parts = line.split()
            # last token is the numeric ratio
            ratio = float(parts[-1])
            assert ratio > 70 and ratio < 75
            return
    assert False, "did not find required ratio line"


def test_prediction_with_72():
    out, err, code = run_script(["--mtmb", "72"])
    assert code == 0
    # ensure predicted m_b is close to 2.85 GeV
    for line in out.splitlines():
        if line.strip().startswith("m_b ="):
            # parse value
            parts = line.split()
            mb = float(parts[2])
            assert abs(mb - 2.85) < 0.1
            return
    assert False, "no m_b prediction found"


def test_two_loop_ratio():
    out, err, code = run_script(["--mtmb", "40", "--two-loop"])
    assert code == 0
    # look for required ratio line and check it's closer to 70
    for line in out.splitlines():
        if "required m_t/m_b ratio" in line:
            ratio = float(line.split()[-1])
            assert 69 < ratio < 72
            return
    assert False, "no required ratio line found"
