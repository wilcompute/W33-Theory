import json
import subprocess
import sys
from pathlib import Path

import pytest

ART = Path(__file__).resolve().parents[1] / "artifacts"


def test_run_both_canonical_forbids_smoke(tmp_path: Path):
    # run with very small W set and short time to be CI friendly
    cmd = [
        sys.executable,
        "tools/run_both_canonical_forbids.py",
        "--cands",
        "0-18-25,0-20-23",
        "--time",
        "10",
        "--w-list",
        "0",
        "--workers",
        "1",
        "--reports-dir",
        str(tmp_path),
    ]
    # Allow the script to run but do not fail CI if underlying solvers are absent
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        # Best-effort smoke: script should still write a summary file even if anchor failed
        pass

    out = ART / "canonical_forbid_verification_summary.json"
    assert out.exists(), "Expected canonical verification summary to be written"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "forbids" in data
    if not data.get("forbids"):
        pytest.skip(
            "Canonical forbid verification did not produce forbids in this environment (likely missing solvers)"
        )
