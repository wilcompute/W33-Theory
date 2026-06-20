#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1390_certificate_importer_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1390_import_s3_maxsat_certificate.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1390
    assert out["verified"] is True
    assert out["score"] == 210
    assert out["optimality_status"] == "witness_verified_only"


def test_bt1391_queue_model_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1391_hesse_sic_t_queue_model.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1391
    assert out["verified"] is True
    assert out["microframes"] == 720
    data = json.loads((ROOT / "data" / "bt1391_hesse_sic_t_queue_model.json").read_text(encoding="utf-8"))
    assert data["checks"]["all_slack_positive"] is True


def test_bt1392_runtime_workflow_manifest():
    manifest = json.loads((ROOT / "data" / "bt1392_runtime_workflow_manifest.json").read_text(encoding="utf-8"))
    workflow = (ROOT / ".github" / "workflows" / "runtime-frontier-release-lock.yml").read_text(encoding="utf-8")
    runner = (ROOT / "tools" / "bt1389_run_runtime_frontier_release_lock.sh").read_text(encoding="utf-8")
    assert manifest["ready"] is True
    assert "bt1389_run_runtime_frontier_release_lock.sh" in workflow
    assert "bt1390_import_s3_maxsat_certificate.py" in runner
    assert "bt1391_hesse_sic_t_queue_model.py" in runner
