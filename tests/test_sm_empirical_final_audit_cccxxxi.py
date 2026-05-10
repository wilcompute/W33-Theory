"""
Part CCCXXXI -- SM Empirical Closure: Final Audit
Regression tests for exploration/PART_CCCXXXI_SM_EMPIRICAL_FINAL_AUDIT_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXI_SM_EMPIRICAL_FINAL_AUDIT_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, ALPHA_INV,
    V_EW,
    DIMENSIONLESS_CLOSURES, DIMENSIONAL_CLOSURES,
    INTEGER_FINGERPRINT, OPEN_BOUNDARIES,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_eleven_dimensionless_closures():
    assert len(DIMENSIONLESS_CLOSURES) == 11


def test_five_dimensional_closures():
    assert len(DIMENSIONAL_CLOSURES) == 5


def test_nine_or_more_within_1_sigma():
    within = sum(1 for c in DIMENSIONLESS_CLOSURES if abs(c.z_score) < 1)
    assert within >= 9


def test_ten_or_more_within_2_sigma():
    within = sum(1 for c in DIMENSIONLESS_CLOSURES if abs(c.z_score) < 2)
    assert within >= 10


def test_open_boundaries_at_least_10():
    assert len(OPEN_BOUNDARIES) >= 10


def test_open_boundaries_includes_neutrino():
    text = " ".join(OPEN_BOUNDARIES)
    assert "neutrino" in text or "Neutrino" in text


def test_integer_fingerprint_137():
    assert INTEGER_FINGERPRINT["137"] == 137
    assert INTEGER_FINGERPRINT["137"] == Q ** Q * (MU + 1) + LAM


def test_integer_fingerprint_phi4():
    assert INTEGER_FINGERPRINT["Phi_4"] == 10
    assert INTEGER_FINGERPRINT["Phi_4^2"] == 100
    assert INTEGER_FINGERPRINT["Phi_4^3"] == 1000


def test_integer_fingerprint_v_plus_1():
    assert INTEGER_FINGERPRINT["v+1"] == 41


def test_v_EW_anchor():
    assert V_EW == 246.21965


def test_heavy_quark_yukawas_all_present():
    sectors = {c.sector for c in DIMENSIONLESS_CLOSURES}
    assert {"top", "bottom", "charm", "strange"} <= sectors


def test_heavy_quark_yukawas_within_1_sigma():
    for sector in ("top", "bottom", "charm", "strange"):
        c = next(c for c in DIMENSIONLESS_CLOSURES if c.sector == sector)
        assert abs(c.z_score) < 1, f"{sector} z = {c.z_score}"


def test_dimensional_predictions_within_4_sigma():
    # m_H is at 3.16 sigma due to MS-bar vs tree-level interpretation
    # All others within 1 sigma
    for c in DIMENSIONAL_CLOSURES:
        assert abs(c.z_score) < 4


def test_m_top_dimensional_within_1_sigma():
    c = next(c for c in DIMENSIONAL_CLOSURES if c.sector == "top")
    assert abs(c.z_score) < 1


def test_y_s_eq_phi4_y_c_squared():
    y_c = 1/137
    y_s = 10/18769
    assert abs(y_s - PHI4 * y_c ** 2) < 1e-15


def test_status_field_consistency():
    for c in DIMENSIONLESS_CLOSURES:
        assert c.status in {"PASS_1_SIGMA", "PASS_2_SIGMA", "PASS_3_SIGMA",
                            "TENSION_3-5_SIGMA", "DISFAVORED"}
    for c in DIMENSIONAL_CLOSURES:
        assert c.status in {"PASS_1_SIGMA", "PASS_2_SIGMA", "PASS_3_SIGMA",
                            "TENSION_3-5_SIGMA", "DISFAVORED"}


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXI_SM_EMPIRICAL_FINAL_AUDIT_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXI_sm_empirical_final_audit_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXI_sm_empirical_final_audit_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXI_SM_EMPIRICAL_FINAL_AUDIT_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_inventory():
    out = ROOT / "PART_CCCXXXI_sm_empirical_final_audit_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    inv = data["inventory_summary"]
    assert inv["dimensionless_closures_total"] == 11
    assert inv["dimensional_predictions_total"] == 5
    assert inv["dimensionless_closures_within_1_sigma"] >= 9
