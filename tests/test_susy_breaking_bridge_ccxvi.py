"""Regression tests for Part CCXVI — Supersymmetry Breaking and MSSM Structure from W(3,3)."""
import json, math, pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "PART_CCXVI_susy_breaking_results.json").read_text(encoding="utf-8"))
SUSY = DATA["susy_data"]
SRG  = DATA["srg_params"]

def test_verified():
    assert DATA["verified"] is True

def test_free_parameters_zero():
    assert DATA["free_parameters"] == 0

def test_MSSM_gauge_doubling():
    """2×K = LAM×M_NEG = 24."""
    assert SUSY["MSSM_gauge_doubling"] == 24
    assert SUSY["yukawa_count"] == 24

def test_MSSM_total_equals_E6_adjoint():
    """2V-2 = 78 = E6 adjoint dimension."""
    assert SUSY["MSSM_total_2V_minus_2"] == 78
    assert SUSY["E6_adjoint"] == 78

def test_F_proxy_approx_K():
    """sqrt(E[L²]) ≈ K = 12 (SUSY breaking scale ≈ EW scale)."""
    assert abs(SUSY["F_proxy"] - SRG["K"]) < 0.1

def test_Higgs_doublets_equal_XI_POS():
    """Number of MSSM Higgs doublets = XI_POS = 2."""
    assert SUSY["N_Higgs_doublets"] == 2

def test_mu_ratio():
    """MSSM μ-param ratio MU/K = 1/3."""
    assert abs(SUSY["mu_ratio_MU_over_K"] - 1/3) < 1e-5

def test_tan_beta():
    """tan(β) = |XI_NEG|/XI_POS = 2."""
    assert abs(SUSY["tan_beta_W33"] - 2.0) < 1e-10

def test_cos_2beta():
    """cos(2β) = -3/5 = -0.6."""
    assert abs(SUSY["cos_2beta"] - (-0.6)) < 1e-5

def test_R_parity_Z2_quotient():
    """AUT_ORDER/2 = 25920 = |PSp(4,3)|."""
    assert SUSY["Z2_quotient"] == 25920
    assert SUSY["PSp43_order"] == 25920

def test_susy_suppression_log10():
    """SUSY breaking suppression log10 < -20."""
    assert SUSY["susy_sup_log10"] < -20

def test_goldstino_count():
    """One goldstino from residual spectral mode."""
    assert SUSY["goldstino_count"] == 1

def test_gravitino_ratio():
    """Gravitino/EW mass ratio = spectral_sum/V = 0.15."""
    assert abs(SUSY["gravitino_ratio"] - 0.15) < 1e-10

def test_M2_over_M1():
    """M2/M1 = LAM/MU = 0.5 (GUT-scale gaugino ratio)."""
    assert abs(SUSY["M2_over_M1_W33"] - 0.5) < 1e-10

def test_M3_over_M2():
    """M3/M2 = spectral_gap/LAM = 3."""
    assert abs(SUSY["M3_over_M2_W33"] - 3.0) < 1e-10

def test_all_individual_checks():
    for c in DATA["checks"]:
        assert c["pass"], f"Check '{c['check']}' failed: got={c['got']} expected={c['expected']}"
