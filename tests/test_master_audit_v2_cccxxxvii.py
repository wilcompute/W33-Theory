"""
Part CCCXXXVII -- Master Empirical Closure Audit v2 (CCCXXII-CCCXXXVI)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXVII_MASTER_AUDIT_V2_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, H_0, ALPHA_INV,
    V_EW,
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
    assert len(DIMENSIONLESS_CLOSURES) == 21
    assert len(DIMENSIONAL_CLOSURES) == 7
    assert len(HIERARCHY_CLOSURES) == 2


def test_19_or_more_within_1_sigma():
    within = sum(1 for c in DIMENSIONLESS_CLOSURES if abs(c.z_score) < 1)
    assert within >= 19


def test_open_boundaries():
    assert len(OPEN_BOUNDARIES) >= 7


def test_coincidences():
    assert len(COINCIDENCES) >= 5


def test_integer_fingerprint_size():
    assert len(INTEGER_FINGERPRINT) >= 20


def test_recurring_integers():
    assert INTEGER_FINGERPRINT["Phi_4"] == 10
    assert INTEGER_FINGERPRINT["H_0"] == 70
    assert INTEGER_FINGERPRINT["137"] == 137
    assert INTEGER_FINGERPRINT["v+1"] == 41
    assert INTEGER_FINGERPRINT["f"] == 24


def test_v_EW_anchor():
    assert V_EW == 246.21965


def test_six_quark_yukawas_present():
    sectors = {c.sector for c in DIMENSIONLESS_CLOSURES}
    assert {"top", "bottom", "charm", "strange", "down", "up"} <= sectors


def test_three_pmns_angles():
    pmns = [c for c in DIMENSIONLESS_CLOSURES if c.sector == "PMNS"]
    assert len(pmns) == 3


def test_four_cosmology_closures():
    cosmology = [c for c in DIMENSIONLESS_CLOSURES if c.sector == "cosmology"]
    assert len(cosmology) == 4


def test_four_CKM_closures():
    ckm = [c for c in DIMENSIONLESS_CLOSURES if c.sector == "CKM"]
    assert len(ckm) == 4


def test_two_hierarchy_closures():
    assert len(HIERARCHY_CLOSURES) == 2


def test_seven_dimensional_masses():
    sectors = {c.sector for c in DIMENSIONAL_CLOSURES}
    expected = {"Higgs", "top", "bottom", "charm", "strange", "down", "up"}
    assert expected <= sectors


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXVII_MASTER_AUDIT_V2_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXVII_master_audit_v2_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXVII_master_audit_v2_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXVII_MASTER_AUDIT_V2_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_inventory():
    out = ROOT / "PART_CCCXXXVII_master_audit_v2_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    inv = data["inventory_summary"]
    assert inv["dimensionless_closures_total"] == 21
    assert inv["dimensional_predictions_total"] == 7
    assert inv["hierarchy_closures_total"] == 2
    assert inv["dimensionless_closures_within_1_sigma"] >= 19
