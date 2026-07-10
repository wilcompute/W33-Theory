"""Regression tests for the canonical Levi-chain selector closure."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import bt1880_bt982_to_bt1875_mapper as mapper  # noqa: E402
import bt1874_final_selector_quotient_certificate as certificate  # noqa: E402


def test_mapper_crosswalk_closes_chain_boundary() -> None:
    summary = mapper.theorem_summary()
    assert summary["all_pass"]
    assert summary["checks"]["chain_boundary_closed"]
    assert summary["checks"]["phase_boundary_closed"]


def test_final_selector_has_no_open_boundary() -> None:
    summary = certificate.theorem_summary()
    assert summary["all_pass"]
    assert summary["final_open_boundary"] is None
