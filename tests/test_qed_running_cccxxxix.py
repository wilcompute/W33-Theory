"""
Part CCCXXXIX -- QED running alpha_em^{-1}(0) - alpha_em^{-1}(M_Z) = q^2 + 1/k = 109/12
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXXXIX_QED_RUNNING_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    DELTA_W33, DELTA_LEADING,
    ALPHA_INV_0, ALPHA_INV_MZ, SIGMA_MZ, DELTA_DATA,
    Z_LEADING, Z_FULL,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_check_count():
    assert len(checks) == 14


def test_W33_form():
    assert DELTA_W33 == Fraction(Q ** 2 * K + 1, K)
    assert DELTA_W33 == Fraction(109, 12)


def test_leading_subleading_components():
    assert Q ** 2 == 9
    assert K == 12
    assert Q ** 2 * K + 1 == 109


def test_decimal_value():
    assert abs(float(DELTA_W33) - 9.0833) < 1e-3


def test_full_within_1_sigma():
    assert abs(Z_FULL) < 1


def test_full_within_0p1_sigma():
    assert abs(Z_FULL) < 0.1


def test_leading_alone_off():
    # Pure q^2 = 9 is many sigmas off the data
    assert abs(Z_LEADING) > 5


def test_residual_records():
    records = residual_records()
    assert len(records) == 2
    # The full version passes 1 sigma; the leading does not
    full = next(r for r in records if r.id == "QED_RUN_FULL_W33")
    leading = next(r for r in records if r.id == "QED_RUN_LEADING_W33")
    assert "PASS" in full.status
    assert "DISFAVORED" in leading.status


# Cross-link tests
def test_k_in_other_W33_closures():
    # k = 12 in:
    # - Conway prime AP step (CCLXVIII)
    # - Mathieu chain step (CCLXXXVII)
    # - Omega_c h^2 numerator (CCCXXXV: k/Phi_4^2 = 12/100)
    assert K == 12
    OMEGA_C_H2 = Fraction(K, PHI4 ** 2)
    # 12/100 reduces to 3/25; numerator becomes 3 (= q), not 12
    assert OMEGA_C_H2 == Fraction(3, 25)
    # The unreduced form has K in numerator
    assert K * PHI4 ** 2 == 12 * 100


def test_predicted_alpha_inv_MZ():
    pred = ALPHA_INV_0 - float(DELTA_W33)
    assert abs(pred - 127.953) < 0.01


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXXXIX_QED_RUNNING_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXXXIX_qed_running_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXXXIX_qed_running_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXXXIX_QED_RUNNING_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_decomposition():
    out = ROOT / "PART_CCCXXXIX_qed_running_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "9" in data["leading_subleading_decomposition"]["leading_q^2"]
