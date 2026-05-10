"""
Part CCCXXXII -- GUT-Planck Hierarchy in W(3,3)
Regression tests for exploration/PART_CCCXXXII_GUT_PLANCK_HIERARCHY_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXII_GUT_PLANCK_HIERARCHY_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    ALPHA_GUT_INV_W33, M_PL_OVER_M_GUT_W33,
    M_GUT_MSSM, ALPHA_GUT_INV, M_PL_REDUCED, M_PL_GR,
    M_PL_OVER_M_GUT, RESIDUAL_RATIO, Z_RATIO,
    RESIDUAL_ALPHA_GUT, Z_ALPHA_GUT,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 17


def test_alpha_GUT_W33_equals_F():
    assert ALPHA_GUT_INV_W33 == F == 24


def test_M_Pl_ratio_W33_form():
    assert M_PL_OVER_M_GUT_W33 == LAM * Q * (F - MU - 1)
    assert M_PL_OVER_M_GUT_W33 == 6 * 19 == 114


def test_alpha_GUT_within_2_sigma():
    assert abs(Z_ALPHA_GUT) < 2


def test_M_Pl_ratio_within_1_sigma():
    assert abs(Z_RATIO) < 1


def test_F_minus_MU_minus_1_equals_19():
    # 19 is the Bernoulli small-prime tower member from CCLVIII
    assert F - MU - 1 == 19


def test_steiner_S_5_8_24_parameters():
    # Parameters of the Steiner system S(5,8,24)
    assert (MU + 1, LAM ** Q, F) == (5, 8, 24)


def test_M_Pl_predicted_close_to_measured():
    M_Pl_pred = M_PL_OVER_M_GUT_W33 * M_GUT_MSSM
    rel_diff = abs(M_Pl_pred - M_PL_REDUCED) / M_PL_REDUCED
    assert rel_diff < 0.05  # Within 5%


def test_M_GUT_in_canonical_window():
    assert 1e16 < M_GUT_MSSM < 5e16


def test_alpha_GUT_inv_in_window():
    assert 23 < ALPHA_GUT_INV < 26


def test_three_scale_chain_v_EW_M_GUT_M_Pl():
    V_EW = 246.21965
    assert M_GUT_MSSM > V_EW * 1e13
    assert M_PL_REDUCED > M_GUT_MSSM * 50


def test_residual_records_two():
    records = residual_records()
    assert len(records) == 2
    statuses = {r.status for r in records}
    assert all("PASS" in s for s in statuses)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXII_GUT_PLANCK_HIERARCHY_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXII_gut_planck_hierarchy_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXII_gut_planck_hierarchy_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXII_GUT_PLANCK_HIERARCHY_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_json_predictions_present():
    out = ROOT / "PART_CCCXXXII_gut_planck_hierarchy_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["predictions"]["alpha_GUT_inv_W33"] == 24
    assert data["predictions"]["M_Pl_over_M_GUT_W33"] == 114
