"""Part CCCCXLII -- third-reference refinement witness."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXLII_THIRD_REFERENCE_REFINEMENT_WITNESS")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXLII_third_reference_refinement_witness_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXLII_third_reference_refinement_witness_results.json"
    assert out.exists()


def test_verified_and_checks() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 8
    assert data["checks_passed"] == 8


def test_representative_counts() -> None:
    data = _load_results()
    reps = data["representatives"]

    assert reps["feasible_pair"]["pair"] == [0, 13]
    assert reps["feasible_pair"]["two_reference_feasible"] is True
    assert reps["feasible_pair"]["feasible_c_count"] == 240

    assert reps["infeasible_pair_A"]["pair"] == [0, 1]
    assert reps["infeasible_pair_A"]["two_reference_feasible"] is False
    assert reps["infeasible_pair_A"]["feasible_c_count"] == 234

    assert reps["infeasible_pair_B"]["pair"] == [0, 239]
    assert reps["infeasible_pair_B"]["two_reference_feasible"] is False
    assert reps["infeasible_pair_B"]["feasible_c_count"] == 126
