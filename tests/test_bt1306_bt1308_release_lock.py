#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1306_release_lock_verifier_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1306_verify_release_lock.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1306
    assert out["verified"] is True
    assert out["path_count"] > 10


def test_bt1307_release_lock_runner_exists():
    text = (ROOT / "tools" / "bt1307_run_v1_release_lock.sh").read_text(encoding="utf-8")
    assert "bt1299_run_v1_release_gates.sh" in text
    assert "bt1306_verify_release_lock.py" in text
    assert "BT1307 v1 release lock passed" in text


def test_bt1308_workflow_runs_release_lock():
    text = (ROOT / ".github" / "workflows" / "recovery-packet.yml").read_text(encoding="utf-8")
    assert "bash tools/bt1307_run_v1_release_lock.sh" in text
    assert "test_bt1302_bt1304_release_closure.py" in text
