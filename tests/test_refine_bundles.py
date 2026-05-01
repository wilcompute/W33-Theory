#!/usr/bin/env python3
"""Tests for the direct-product refactor demonstration."""

from __future__ import annotations

import json

import pytest
from THEORY_PART_CXCV_REFINE_BUNDLES import report_closure


@pytest.fixture(scope="module")
def closure_info():
    return report_closure()


def test_closure_sizes(closure_info):
    info = closure_info
    assert info["closure_size"] == info["expected_product"]
    assert info["Gamma_size"] > 0
    assert info["H_size"] > 0


def test_closure_file_exists(closure_info):
    # ensure the json file is written and parseable
    info = closure_info
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent / "pillars" / "closure_info.json"
    assert path.exists()
    data = json.loads(path.read_text())
    assert data["closure_size"] == info["closure_size"]
