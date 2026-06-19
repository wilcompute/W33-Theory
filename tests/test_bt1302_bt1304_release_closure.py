#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1302_workflow_runs_release_gates():
    text = (ROOT / ".github" / "workflows" / "recovery-packet.yml").read_text(encoding="utf-8")
    assert "bt1300_verify_paper_build_handshake.py" in text
    assert "bash tools/bt1299_run_v1_release_gates.sh" in text
    assert "test_bt1298_bt1300_release_gates.py" in text


def test_bt1303_release_source_of_truth_index():
    data = json.loads((ROOT / "data" / "bt1303_v1_release_source_of_truth_index.json").read_text(encoding="utf-8"))
    assert data["release_target"] == "v1.0.0"
    assert data["ready"] is True
    assert data["runner"] == "tools/bt1299_run_v1_release_gates.sh"
    assert data["paper"]["source"] == "paper/w33_preprint.tex"
    assert data["paper"]["artifact"] == "paper/w33_preprint.pdf"
    assert data["recovery_packet"]["strict_target"] == "diam14_polar_path"
    assert "docs/v1_release_command.md" in data["human_entrypoints"]


def test_bt1304_release_command_doc():
    text = (ROOT / "docs" / "v1_release_command.md").read_text(encoding="utf-8")
    assert "bash tools/bt1299_run_v1_release_gates.sh" in text
    assert "BT1299 v1 release gates passed" in text
    assert "data/bt1303_v1_release_source_of_truth_index.json" in text
