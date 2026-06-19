#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1298_release_gate_matrix():
    data = json.loads((ROOT / "data" / "bt1298_v1_release_gate_matrix.json").read_text(encoding="utf-8"))
    gates = {g["gate"]: g for g in data["gates"]}
    assert data["release_target"] == "v1.0.0"
    for name in ["strict_recovery_certificate", "external_candidate_batch", "unified_release_packet", "readiness_badge", "paper_build_handshake", "release_pytest_subset"]:
        assert name in gates


def test_bt1299_release_gate_runner_exists():
    text = (ROOT / "tools" / "bt1299_run_v1_release_gates.sh").read_text(encoding="utf-8")
    for name in ["bt1281_verify_recovery_certificate.py", "bt1274_batch_score_candidates.py", "bt1291_verify_release_packet.py", "bt1296_verify_release_readiness_badge.py", "bt1300_verify_paper_build_handshake.py"]:
        assert name in text


def test_bt1300_paper_build_handshake_script_exists():
    text = (ROOT / "tools" / "bt1300_verify_paper_build_handshake.py").read_text(encoding="utf-8")
    assert "paper-build.yml" in text
    assert "paper/w33_preprint.tex" in text
    assert "paper/w33_preprint.pdf" in text
