#!/usr/bin/env python3
"""Tests for the direct-product refactor demonstration."""

from __future__ import annotations

import json

from THEORY_PART_CXCV_REFINE_BUNDLES import report_closure


def test_closure_sizes():
    info = report_closure()
    assert info["closure_size"] == info["expected_product"]
    assert info["Gamma_size"] > 0
    assert info["H_size"] > 0


def test_closure_file_exists():
    # ensure the json file is written and parseable
    info = report_closure()
    # file already written to repo root
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent / "closure_info.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["closure_size"] == info["closure_size"]
