"""
Part CCCXLIV -- Neutrino mass scale Sigma m_nu = q*Phi_6 * v_EW^2 / M_GUT
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXLIV_NEUTRINO_MASS_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    Y_NU_SQ_W33, M_GUT_GeV, V_EW_GeV,
    SIGMA_M_NU_W33_meV, SIGMA_M_NU_W33_eV,
    SIGMA_NH_MIN_meV, SIGMA_PLANCK_UPPER_meV,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_y_nu_squared_W33():
    assert Y_NU_SQ_W33 == Q * PHI6
    assert Y_NU_SQ_W33 == 21


def test_components():
    assert Q == 3
    assert PHI6 == 7
    assert Q * PHI6 == 21


def test_sigma_m_nu_in_window():
    assert 55 < SIGMA_M_NU_W33_meV < 65


def test_above_NH_minimum():
    assert SIGMA_M_NU_W33_meV >= SIGMA_NH_MIN_meV


def test_below_Planck_bound():
    assert SIGMA_M_NU_W33_meV < SIGMA_PLANCK_UPPER_meV


def test_residual_records():
    records = residual_records()
    assert len(records) == 1
    assert records[0].in_range
    assert "PASS" in records[0].status


def test_seesaw_formula():
    # Sigma m_nu = y_nu^2 * v^2 / M_GUT
    expected = Y_NU_SQ_W33 * V_EW_GeV ** 2 / M_GUT_GeV * 1e12  # in meV
    assert abs(SIGMA_M_NU_W33_meV - expected) < 1e-6


# Cross-link with CCCXXXV cosmology (H_0)
def test_y_nu_sq_in_terms_of_H_0():
    # y_nu^2 = q*Phi_6 = 21
    # H_0 = Phi_6 * Phi_4 = 70
    # so y_nu^2 = q*H_0/Phi_4 = 3*70/10 = 21
    H_0 = PHI6 * PHI4
    assert Y_NU_SQ_W33 == Q * H_0 // PHI4 == 21


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXLIV_NEUTRINO_MASS_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXLIV_neutrino_mass_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXLIV_neutrino_mass_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXLIV_NEUTRINO_MASS_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True
