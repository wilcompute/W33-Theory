"""Regression gate for the fibre-hypervisor suspension ladder theorem."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

from w33_fibre_suspension_ladder import verify  # noqa: E402


def test_fibre_suspension_certificate_passes() -> None:
    payload = verify()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())


def test_certificate_matches_frozen_artifact() -> None:
    payload = verify()
    frozen_path = os.path.join(ROOT, "data", "w33_fibre_suspension_ladder.json")
    with open(frozen_path, encoding="utf-8") as fh:
        frozen = json.load(fh)
    assert frozen["certificate_sha256"] == payload["certificate_sha256"]


def test_suspension_core_numbers() -> None:
    payload = verify()
    s = payload["suspension"]
    assert s["retention_points"] == 36
    assert s["release_boundary"] == 36
    assert s["suspend_resume_cycle_boundary"] == 72
    assert payload["fibre"]["hypervisor_states"] == 1296
