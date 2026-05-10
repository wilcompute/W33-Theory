"""
Part CCCCXXXV -- Per-Closure Derivation Roadmap
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXV_PER_CLOSURE_DERIVATION_ROADMAP import (
    DerivationRecord, DERIVATIONS, class_summary,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_inventory_size():
    assert len(DERIVATIONS) >= 38


def test_class_breakdown():
    cs = class_summary()
    assert cs["A"] >= 4
    assert cs["B"] >= 5
    assert cs["C"] >= 20


def test_total_classes_consistency():
    cs = class_summary()
    total = cs["A"] + cs["B"] + cs["C"]
    assert total == len(DERIVATIONS)


def test_sin2_theta_W_class_A():
    rec = next(d for d in DERIVATIONS if "sin^2 theta_W (M_GUT)" in d.observable)
    assert rec.derivation_class == "A"
    assert "DERIVED" in rec.status


def test_alpha_GUT_class_A():
    rec = next(d for d in DERIVATIONS if "alpha_GUT" in d.observable)
    assert rec.derivation_class == "A"


def test_lambda_H_class_B():
    rec = next(d for d in DERIVATIONS if "lambda_H" in d.observable)
    assert rec.derivation_class == "B"


def test_yukawas_mostly_class_C():
    yukawas = [d for d in DERIVATIONS if d.observable.startswith("y_")]
    class_C = [d for d in yukawas if d.derivation_class == "C"]
    assert len(class_C) >= 5


def test_proton_mass_derived_from_QCD():
    rec = next(d for d in DERIVATIONS if "proton" in d.observable.lower())
    assert "DERIVED_FROM_QCD" in rec.status


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXV_PER_CLOSURE_DERIVATION_ROADMAP")
    mod.main()
    assert (ROOT / "PART_CCCCXXXV_per_closure_derivation_roadmap_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXV_per_closure_derivation_roadmap_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXV_PER_CLOSURE_DERIVATION_ROADMAP").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_has_derivation_classes():
    out = ROOT / "PART_CCCCXXXV_per_closure_derivation_roadmap_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "A_structurally_derived" in data["derivation_classes"]
    assert "B_axiomatic_from_spectral_action" in data["derivation_classes"]
    assert "C_per_closure_open" in data["derivation_classes"]


def test_json_has_roadmap():
    out = ROOT / "PART_CCCCXXXV_per_closure_derivation_roadmap_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "roadmap" in data
    assert "phase_1" in data["roadmap"]
    assert "phase_4" in data["roadmap"]
