"""
Part CCCXLV -- Final Master Empirical Audit v3 (CCCXXII-CCCXLIV)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXLV_FINAL_AUDIT_V3_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, H_0, ALPHA_INV,
    V_EW, M_GUT,
    DIMENSIONLESS_CLOSURES, DIMENSIONAL_CLOSURES, HIERARCHY_CLOSURES,
    INTEGER_FINGERPRINT, COINCIDENCES, OPEN_BOUNDARIES,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_inventory_sizes():
    assert len(DIMENSIONLESS_CLOSURES) == 27
    assert len(DIMENSIONAL_CLOSURES) == 10
    assert len(HIERARCHY_CLOSURES) == 2


def test_total_closures():
    total = len(DIMENSIONLESS_CLOSURES) + len(DIMENSIONAL_CLOSURES) + len(HIERARCHY_CLOSURES)
    assert total == 39


def test_within_1_sigma_count():
    within = sum(1 for c in DIMENSIONLESS_CLOSURES if abs(c.z_score) < 1)
    assert within >= 24


def test_open_boundaries():
    assert len(OPEN_BOUNDARIES) >= 3


def test_coincidences():
    assert len(COINCIDENCES) >= 7


def test_integer_fingerprint_size():
    assert len(INTEGER_FINGERPRINT) >= 25


def test_recurring_integers():
    assert INTEGER_FINGERPRINT["Phi_4"] == 10
    assert INTEGER_FINGERPRINT["137"] == 137
    assert INTEGER_FINGERPRINT["v+1"] == 41
    assert INTEGER_FINGERPRINT["f"] == 24
    assert INTEGER_FINGERPRINT["Phi_6*Phi_4 (H_0)"] == 70


def test_pmns_complete():
    pmns = [c for c in DIMENSIONLESS_CLOSURES if c.sector == "PMNS"]
    assert len(pmns) == 4


def test_ckm_complete():
    ckm = [c for c in DIMENSIONLESS_CLOSURES if c.sector == "CKM"]
    assert len(ckm) == 4


def test_six_quark_yukawas():
    quarks = {c.sector for c in DIMENSIONLESS_CLOSURES if c.sector in {"top", "bottom", "charm", "strange", "down", "up"}}
    assert quarks == {"top", "bottom", "charm", "strange", "down", "up"}


def test_v_EW_anchor():
    assert V_EW == 246.21965


def test_M_GUT_value():
    assert 1e16 < M_GUT < 5e16


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXLV_FINAL_AUDIT_V3_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXLV_final_audit_v3_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXLV_final_audit_v3_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXLV_FINAL_AUDIT_V3_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_inventory():
    out = ROOT / "PART_CCCXLV_final_audit_v3_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    inv = data["inventory_summary"]
    assert inv["TOTAL_CLOSURES"] == 39
    assert inv["dimensionless_closures_total"] == 27
    assert inv["dimensional_predictions_total"] == 10
