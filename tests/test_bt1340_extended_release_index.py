#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1340_extended_release_lock_index():
    data = json.loads((ROOT / "data" / "bt1340_extended_release_lock_index.json").read_text(encoding="utf-8"))
    assert data["ready"] is True
    assert data["extends"] == "data/bt1303_v1_release_source_of_truth_index.json"
    assert data["runner"] == "tools/bt1340_run_extended_release_lock.sh"
    assert "tools/bt1338_extract_q4_chain_checks.py" in data["new_verifiers"]
    assert "tools/bt1339_optical_loss_crosstalk_budget.py" in data["new_verifiers"]
    assert data["expected_outputs"]["q4_chain_naive_k"] == 0
    assert data["expected_outputs"]["optical_budget_gate_verified"] is True
