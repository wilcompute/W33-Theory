"""
Part CCCXL -- Proton mass m_p = q*v_EW/(lam*17*23) = 3v/782 in W(3,3)
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXL_PROTON_MASS_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    M_P_W33_FRAC, M_P_RATIO_W33,
    M_P_MEV, V_EW_GEV, M_P_W33_MEV, RESIDUAL, Z_M_P, LATTICE_SIGMA,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_W33_form():
    assert M_P_W33_FRAC == Fraction(Q, LAM * (PHI3 + MU) * (PHI3 + PHI4))
    assert M_P_W33_FRAC == Fraction(3, 782)


def test_ratio_to_Lambda_QCD():
    assert M_P_RATIO_W33 == Fraction(Q ** 2, LAM)
    assert M_P_RATIO_W33 == Fraction(9, 2)


def test_components():
    assert PHI3 + MU == 17
    assert PHI3 + PHI4 == 23
    assert LAM * (PHI3 + MU) * (PHI3 + PHI4) == 782
    assert Q ** 2 == 9


def test_predicted_value():
    assert 944 < M_P_W33_MEV < 946


def test_within_lattice_sigma():
    assert abs(Z_M_P) < 1


def test_residual_under_10MeV():
    assert abs(RESIDUAL) < 10


def test_residual_records():
    records = residual_records()
    assert len(records) == 2
    assert all("PASS" in r.status for r in records)


# Cross-link with CCCXXXVIII Lambda_QCD
def test_cross_link_with_Lambda_QCD():
    # Lambda_QCD = v_EW/(q*17*23) = v/1173
    Lambda_QCD = V_EW_GEV / (Q * (PHI3 + MU) * (PHI3 + PHI4))
    # m_p = q^2/lam * Lambda_QCD
    m_p_check = (Q ** 2 / LAM) * Lambda_QCD
    assert abs(m_p_check - M_P_W33_MEV / 1000) < 1e-6


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXL_PROTON_MASS_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXL_proton_mass_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXL_proton_mass_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXL_PROTON_MASS_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_scale_chain_extension():
    out = ROOT / "PART_CCCXL_proton_mass_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    chain = data["scale_chain_extension"]
    assert "v_EW" in chain["v_EW_to_m_p"]
