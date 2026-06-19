#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1290_release_addendum_exists():
    path = ROOT / "analysis" / "BT1290_v1_release_recovery_packet_addendum.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "recovery-packet CI passes" in text
    assert "tools/bt1281_verify_recovery_certificate.py" in text
    assert "data/bt1287_recovery_packet_release_manifest.json" in text
    assert "strict target = diam14_polar_path" in text


def test_bt1291_unified_release_verifier_runs_true():
    subprocess.run([sys.executable, str(ROOT / "tools" / "bt1291_verify_release_packet.py")], cwd=ROOT, check=True)
    d = json.loads((ROOT / "data" / "bt1291_release_packet_verification_summary.json").read_text(encoding="utf-8"))
    assert d["verified"] is True
    assert d["release_target"] == "v1.0.0"
    assert d["strict_target"] == "diam14_polar_path"
    assert all(d["checks"].values())


def test_bt1292_release_note_block_exists():
    path = ROOT / "docs" / "release_notes_v1_recovery_packet.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "v1.0.0 Recovery Packet Release Note" in text
    assert "tools/bt1291_verify_release_packet.py" in text
    assert "release packet verified = true" in text
    assert "diam14_polar_path" in text
    assert "strict score 5/5" in text


def test_bt1294_recovery_workflow_runs_unified_verifier():
    path = ROOT / ".github" / "workflows" / "recovery-packet.yml"
    text = path.read_text(encoding="utf-8")
    assert "bt1291_verify_release_packet.py" in text
    assert "test_bt1288_readme_recovery_pointer.py" in text
