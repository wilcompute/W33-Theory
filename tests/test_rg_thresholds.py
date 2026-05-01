import subprocess
import sys
from pathlib import Path

# use the RG script via subprocess to check threshold functionality

SCRIPT = Path(__file__).resolve().parents[1] / "exploration" / "RG_PRECISION_MASSES.py"


def run_script(args):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout or ""
    err = proc.stderr or ""
    return out + err


def test_threshold_zeroing():
    # run with thresholds and eps=0 to avoid damping; capture output
    out = run_script(["--thresholds", "--eps", "0"])
    # script should produce some output when run successfully
    assert out.strip(), "expected nonempty output when thresholds enabled"
    # JSON file should record the options correctly
    import json

    data = json.load(open("RG_MASSES.json"))
    opts = data.get("options", {})
    assert opts.get("thresholds") is True
    assert opts.get("eps") == 0.0


def test_eps_control():
    # ensure eps flag does not crash the script and is recorded
    out1 = run_script(["--eps", "0.1"])  # nonzero damping
    assert out1.strip(), "script produced no output with --eps flag"
    import json

    data = json.load(open("RG_MASSES.json"))
    opts = data.get("options", {})
    assert abs(opts.get("eps", -1) - 0.1) < 1e-8
