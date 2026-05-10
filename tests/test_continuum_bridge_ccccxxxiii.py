"""
Part CCCCXXXIII -- Continuum Bridge: Spectral-Action Axioms
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXIII_CONTINUUM_BRIDGE_AXIOMATIC import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    A_0, A_2, A_4, C_EH,
    D_F_SQ_SPECTRUM,
    Tr_1, Tr_D_F_sq, Tr_D_F_4,
    AXIOMS,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_seeley_dewitt_coefficients():
    assert A_0 == 480
    assert A_2 == 2240
    assert A_4 == 17600
    assert C_EH == 320


def test_W33_form_of_C_EH():
    assert C_EH == LAM ** 3 * V == 320


def test_W33_form_of_a_2():
    assert A_2 == C_EH * PHI6 == 2240
    assert A_2 == LAM ** 3 * V * PHI6


def test_W33_form_of_a_4():
    assert A_4 == LAM ** 6 * (MU + 1) ** 2 * (K - 1) == 17600


def test_W33_form_of_a_0():
    # 480 = lam^5 * g = 32 * 15 = 480, OR lam * v * k / 2 = 480
    assert A_0 == LAM ** 5 * G
    assert A_0 == LAM * V * K // 2


def test_internal_Dirac_self_consistency():
    """Tr(1) = a_0; Tr(D^2) = a_2; Tr(D^4) = a_4."""
    assert Tr_1() == A_0
    assert Tr_D_F_sq() == A_2
    assert Tr_D_F_4() == A_4


def test_D_F_squared_spectrum():
    """D_F^2 eigenvalues are W(3,3) integers."""
    assert D_F_SQ_SPECTRUM[0] == 82
    assert D_F_SQ_SPECTRUM[4] == 320
    assert D_F_SQ_SPECTRUM[10] == 48
    assert D_F_SQ_SPECTRUM[16] == 30


def test_eigenvalue_W33_forms():
    assert 4 == LAM ** 2
    assert 10 == PHI4
    assert 16 == LAM ** 4


def test_multiplicity_W33_forms():
    assert 82 == Q ** 4 + 1
    assert 320 == LAM ** 3 * V == C_EH
    assert 48 == LAM * F
    assert 30 == Q * PHI4


def test_six_axioms():
    assert len(AXIOMS) == 6
    for key in ["C1_spectral_triple", "C2_almost_commutative", "C3_spectral_action_principle",
                "C4_EH_from_a2", "C5_YM_from_fluctuations", "C6_Higgs_Yukawa_from_DF"]:
        assert key in AXIOMS


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXIII_CONTINUUM_BRIDGE_AXIOMATIC")
    mod.main()
    assert (ROOT / "PART_CCCCXXXIII_continuum_bridge_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXIII_continuum_bridge_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXIII_CONTINUUM_BRIDGE_AXIOMATIC").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_has_axioms():
    out = ROOT / "PART_CCCCXXXIII_continuum_bridge_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "C1_spectral_triple" in data["continuum_axioms"]
    assert "C4_EH_from_a2" in data["continuum_axioms"]
