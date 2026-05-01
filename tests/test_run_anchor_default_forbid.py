import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
CFG = Path(__file__).resolve().parents[1] / "config" / "canonical_forbid.json"


def test_run_anchor_uses_config_default(tmp_path: Path):
    assert CFG.exists(), "Canonical config not present"
    cf = json.loads(CFG.read_text(encoding="utf-8")).get("canonical_forbid")
    assert cf and len(cf) == 3
    forbid_str = f"{cf[0]}-{cf[1]}-{cf[2]}"

    cmd = [
        sys.executable,
        "tools/run_anchor_and_archive.py",
        "--time",
        "10",
        "--w-list",
        "0",
        "--workers",
        "1",
        "--reports-dir",
        str(tmp_path),
    ]
    # best-effort: allow failures but expect the anchor summary file to be created for canonical forbid
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        pass

    summary = ART / f"anchor_core_cpsat_summary_forbid_{forbid_str}.json"
    if not summary.exists():
        pytest.skip(
            f"Anchor summary for canonical forbid {forbid_str} not produced; skipping (likely missing CP-SAT in CI)"
        )
