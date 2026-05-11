"""
Part CCCCCXX -- The Complete Derivation Chain: From q! = 2q to All Observables
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCCXX_COMPLETE_DERIVATION_CHAIN import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    DERIVATION_CHAIN, THREE_FOLD_FEATURES,
    axiom_bits, predictions_count,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_14_derivation_steps():
    assert len(DERIVATION_CHAIN) == 14


def test_5_three_fold_features():
    assert len(THREE_FOLD_FEATURES) == 5


def test_master_equation_at_q_3():
    assert math.factorial(3) == 2 * 3


def test_chain_steps_have_required_fields():
    for step in DERIVATION_CHAIN:
        assert "step" in step
        assert "name" in step
        assert "statement" in step
        assert "source" in step


def test_chain_first_step_is_master_equation():
    assert "q! = 2q" in DERIVATION_CHAIN[0]["statement"]


def test_chain_last_step_is_monster():
    assert "Monster" in DERIVATION_CHAIN[-1]["name"]


def test_axiom_bits():
    assert axiom_bits() == 40  # 5 ASCII * 8 bits


def test_predictions_count():
    assert predictions_count() >= 80


def test_three_fold_features_all_present():
    expected = {"3 spatial dimensions", "3 fermion generations",
                "SU(3)_C color", "SO(8) triality", "Tits magic square q=3 entry"}
    assert set(THREE_FOLD_FEATURES.keys()) == expected


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCCXX_COMPLETE_DERIVATION_CHAIN")
    mod.main()
    assert (ROOT / "PART_CCCCCXX_complete_derivation_chain_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCCXX_complete_derivation_chain_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCCXX_COMPLETE_DERIVATION_CHAIN").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_chain_complete():
    out = ROOT / "PART_CCCCCXX_complete_derivation_chain_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data["derivation_chain"]) == 14
