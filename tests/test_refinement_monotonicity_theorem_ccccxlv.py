"""Part CCCCXLV -- refinement monotonicity theorem."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXLV_REFINEMENT_MONOTONICITY_THEOREM")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXLV_refinement_monotonicity_theorem_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXLV_refinement_monotonicity_theorem_results.json"
    assert out.exists()


def test_verified_and_checks() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 6
    assert data["checks_passed"] == 6


def test_exact_feasible_stratum_consequence() -> None:
    data = _load_results()
    tr = data["two_reference"]
    rep = data["representative"]

    assert tr["distinct_signatures"] == 3
    assert tr["feasible_signatures"] == 1
    assert tr["feasible_pairs"] == 15120

    assert rep["pair"] == [0, 13]
    assert rep["inherited_refinement_verified_for_all_c"] is True
    assert rep["c_checked"] == 240
