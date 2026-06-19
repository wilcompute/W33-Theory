#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1280_recovery_packet_guide_exists():
    guide = ROOT / "docs" / "recovery_packet_guide.md"
    assert guide.exists()
    text = guide.read_text(encoding="utf-8")
    assert "Finite Clifford Recovery Packet Guide" in text
    assert "schema/bt1269_tomography_candidate.schema.json" in text
    assert "tools/bt1272_score_candidate.py" in text
    assert "data/bt1275_strict_polar_path_recovery_certificate.json" in text
    assert "data/bt1279_recovery_packet_index.json" in text


def test_bt1281_certificate_verifier_runs_true():
    subprocess.run([sys.executable, str(ROOT / "tools" / "bt1281_verify_recovery_certificate.py")], cwd=ROOT, check=True)
    d = json.loads((ROOT / "data" / "bt1281_recovery_certificate_verification_summary.json").read_text(encoding="utf-8"))
    assert d["verified"] is True
    assert all(d["checks"].values())


def test_bt1282_recovery_packet_section_and_integrator():
    sec = ROOT / "paper" / "sections" / "sec_bt1282_recovery_packet_reproducibility.tex"
    helper = ROOT / "tools" / "integrate_bt1282_recovery_packet_insert.py"
    assert sec.exists()
    assert helper.exists()
    text = sec.read_text(encoding="utf-8")
    assert "Recovery packet and reproducibility artifacts" in text
    assert "bt1279" in text
    assert "bt1275" in text
    assert "bt1281" in text


def test_bt1283_recovery_packet_workflow_exists():
    wf = ROOT / ".github" / "workflows" / "recovery-packet.yml"
    assert wf.exists()
    text = wf.read_text(encoding="utf-8")
    assert "integrate_bt1282_recovery_packet_insert.py" in text
    assert "bt1281_verify_recovery_certificate.py" in text


def test_bt1285_recovery_packet_landing_exists():
    landing = ROOT / "docs" / "recovery_packet_landing.md"
    assert landing.exists()
    text = landing.read_text(encoding="utf-8")
    assert "Recovery Packet" in text
    assert "docs/recovery_packet_guide.md" in text
    assert "data/bt1279_recovery_packet_index.json" in text
    assert "verified = true" in text
    assert "pass = 1" in text


def test_bt1287_release_manifest_exists():
    manifest = ROOT / "data" / "bt1287_recovery_packet_release_manifest.json"
    assert manifest.exists()
    d = json.loads(manifest.read_text(encoding="utf-8"))
    assert d["bt"] == 1287
    assert d["release_target"] == "v1.0.0"
    assert d["strict_certificate"] == "data/bt1275_strict_polar_path_recovery_certificate.json"
    assert "docs/recovery_packet_landing.md" in d["docs"]
