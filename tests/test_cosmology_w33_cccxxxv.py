"""
Part CCCXXXV -- Cosmological parameters in W(3,3)
Regression tests for exploration/PART_CCCXXXV_COSMOLOGY_W33_BRIDGE.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXV_COSMOLOGY_W33_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6, H_0,
    OMEGA_C_H2_W33, OMEGA_B_H2_W33, N_S_W33, OMEGA_C_OVER_B_W33, H_0_W33,
    OMEGA_C_H2, OMEGA_B_H2, N_S, OMEGA_C_OVER_B,
    H_0_PLANCK, H_0_SHOES,
    H_0_VS_PLANCK_Z, H_0_VS_SHOES_Z,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 21


def test_omega_c_h2_W33():
    assert OMEGA_C_H2_W33 == Fraction(K, PHI4 ** 2)
    assert OMEGA_C_H2_W33 == Fraction(12, 100)
    assert float(OMEGA_C_H2_W33) == 0.12


def test_omega_b_h2_W33():
    assert OMEGA_B_H2_W33 == Fraction(1, Q ** 2 * (MU + 1))
    assert OMEGA_B_H2_W33 == Fraction(1, 45)


def test_n_s_W33():
    assert N_S_W33 == Fraction(Q ** Q + LAM, PHI4 * Q)
    assert N_S_W33 == Fraction(29, 30)


def test_omega_c_over_b_W33():
    assert OMEGA_C_OVER_B_W33 == Fraction(Q ** Q, MU + 1)
    assert OMEGA_C_OVER_B_W33 == Fraction(27, 5)


def test_H_0_W33():
    assert H_0_W33 == 70
    assert H_0_W33 == PHI6 * PHI4


def test_internal_consistency():
    # Omega_c/Omega_b should equal Omega_c h^2 / Omega_b h^2
    assert OMEGA_C_H2_W33 / OMEGA_B_H2_W33 == OMEGA_C_OVER_B_W33


def test_omega_c_h2_within_1_sigma():
    # EXACT match (z = 0.0)
    z = (float(OMEGA_C_H2_W33) - OMEGA_C_H2) / 0.0012
    assert abs(z) < 0.01


def test_omega_b_h2_within_1_sigma():
    z = (float(OMEGA_B_H2_W33) - OMEGA_B_H2) / 0.00015
    assert abs(z) < 1


def test_n_s_within_1_sigma():
    z = (float(N_S_W33) - N_S) / 0.0038
    assert abs(z) < 1


def test_omega_c_over_b_within_1_sigma():
    z = (float(OMEGA_C_OVER_B_W33) - OMEGA_C_OVER_B) / (OMEGA_C_OVER_B * 0.012)
    assert abs(z) < 1


def test_residual_records_four():
    records = residual_records()
    assert len(records) == 4
    for r in records:
        assert "PASS" in r.status


def test_hubble_tension_W33_between_measurements():
    # H_0_W33 = 70 sits between Planck (67.4) and SH0ES (74.0)
    assert H_0_PLANCK < H_0_W33 < H_0_SHOES


def test_hubble_tension_z_signs():
    # H_0 = 70 is above Planck 67.4 (positive z) and below SH0ES 74.0 (negative z)
    assert H_0_VS_PLANCK_Z > 0
    assert H_0_VS_SHOES_Z < 0


# Cross-link with CCCXXXIII
def test_H_0_appears_in_y_d_numerator():
    # CCCXXXIII: y_d = H_0 / 137^3 = 70/137^3
    # H_0 = 70 here is also Omega_c h^2 numerator k * (Phi_4^2 numerator).
    # The shared integer is 70 = Phi_6 * Phi_4.
    assert PHI6 * PHI4 == 70 == H_0


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXV_COSMOLOGY_W33_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXV_cosmology_w33_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXV_cosmology_w33_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXV_COSMOLOGY_W33_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_hubble_tension_present():
    out = ROOT / "PART_CCCXXXV_cosmology_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["hubble_tension"]["H_0_W33"] == 70


def test_json_down_yukawa_link():
    out = ROOT / "PART_CCCXXXV_cosmology_w33_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    link = data["down_yukawa_cosmology_coincidence"]
    assert "70" in link["y_d_numerator_W33"]
