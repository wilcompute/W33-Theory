"""Part CCCCL -- E8 rescue lookup compression law."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCL_E8_RESCUE_LOOKUP_COMPRESSION_LAW")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCL_e8_rescue_lookup_compression_law_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCL_e8_rescue_lookup_compression_law_results.json"
    assert out.exists()


def test_verified_and_checks() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 7
    assert data["checks_passed"] == 7


def test_lookup_and_histogram() -> None:
    data = _load_results()
    assert data["dot_histogram"] == {
        "-8": 120,
        "-4": 6720,
        "0": 15120,
        "4": 6720,
        "8": 240,
    }
    assert data["canonical_direct"] == {
        "-8": 126,
        "-4": 234,
        "0": 240,
        "4": 234,
        "8": 126,
    }
    assert data["canonical_lookup"] == data["canonical_direct"]


def test_deterministic_sample_agreement() -> None:
    data = _load_results()
    assert data["sampled_mismatches"] == []
    summary = data["sampled_summary"]
    assert summary["-8"]["direct_min"] == summary["-8"]["direct_max"] == 126
    assert summary["-4"]["direct_min"] == summary["-4"]["direct_max"] == 234
    assert summary["0"]["direct_min"] == summary["0"]["direct_max"] == 240
    assert summary["4"]["direct_min"] == summary["4"]["direct_max"] == 234
    assert summary["8"]["direct_min"] == summary["8"]["direct_max"] == 126
