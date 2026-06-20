#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(path: str):
    proc = subprocess.run([sys.executable, str(ROOT / path)], cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def test_bt1399_pdf_rebuild_manifest():
    data = json.loads((ROOT / "data" / "bt1399_claim_master_pdf_rebuild_manifest.json").read_text(encoding="utf-8"))
    assert data["verified"] is True
    assert data["compiled_locally"] is True
    assert data["pages"] == 6
    assert data["render_verified"] is True


def test_bt1400_erasure_noise_sensitivity_runs_true():
    out = run_tool("tools/bt1400_qutrit_erasure_noise_sensitivity.py")
    assert out["bt"] == 1400
    assert out["verified"] is True
    assert out["baseline_gamma"] > 0.9
    data = json.loads((ROOT / "data" / "bt1400_qutrit_erasure_noise_sensitivity.json").read_text(encoding="utf-8"))
    assert data["checks"]["conservative_passes_visibility_gate"] is True


def test_bt1401_runtime_release_lock_extension_manifest():
    data = json.loads((ROOT / "data" / "bt1401_runtime_release_lock_extension.json").read_text(encoding="utf-8"))
    runner = (ROOT / "tools" / "bt1389_run_runtime_frontier_release_lock.sh").read_text(encoding="utf-8")
    assert data["verified"] is True
    assert "tools/bt1400_qutrit_erasure_noise_sensitivity.py" in data["extended_tools"]
    assert "BT1401 runtime frontier release lock passed" in runner
