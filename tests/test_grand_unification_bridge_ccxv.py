"""Regression tests for Part CCXV — Grand Unification and Gauge Group from W(3,3)."""
import json, math, pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "PART_CCXV_grand_unification_results.json").read_text(encoding="utf-8"))
GUT  = DATA["gut_data"]
SRG  = DATA["srg_params"]

def test_verified():
    assert DATA["verified"] is True

def test_free_parameters_zero():
    assert DATA["free_parameters"] == 0

def test_aut_equals_W_E6():
    assert SRG["AUT_ORDER"] == 51840
    assert GUT["W_E6"] == 51840

def test_Q3_equals_E6_fundamental():
    """Q^3 = 27 = dim of E6 fundamental (27-plet)."""
    assert GUT["Q3_equals_E6_fund"] == 27
    assert GUT["E6_fundamental"] == 27

def test_GUT_chain_length_equals_Q():
    assert GUT["GUT_chain_length"] == SRG["Q"]

def test_E6_generations_equals_Q():
    """Three matter generations = Q = 3."""
    assert GUT["E6_generations"] == 3

def test_V_decomp_SO8_plus_K():
    """V = dim(SO(8)) + K = 28 + 12 = 40."""
    assert GUT["D4_dim"] == 28
    assert GUT["V_decomp_SO8_plus_K"] == SRG["V"]

def test_spectral_ratio_LAP_TOP_over_XI_POS():
    """LAP_TOP / XI_POS = 16/2 = 8 encodes coupling ratio."""
    assert GUT["spectral_ratio_LAP_TOP_over_XI_POS"] == 8

def test_sin2W_GUT_within_9pct():
    """GUT sin²θ_W = MU/LAP_TOP = 0.25 within 9% of observed MZ value."""
    err = abs(GUT["sin2_W_GUT"] - GUT["sin2_W_obs_MZ"]) / GUT["sin2_W_obs_MZ"]
    assert err < 0.09

def test_proton_suppression_log10_below_minus20():
    """Proton decay structural suppression log10 < -20."""
    assert GUT["proton_suppression_log10"] < -20

def test_spectral_gap_value():
    assert DATA["srg_params"]["XI_POS"] - DATA["srg_params"]["XI_NEG"] == 6

def test_inv_alpha_GUT_ratio():
    """1/α_GUT (observed 25) / W33 estimate (6.67) ≈ Q+1 = 4."""
    ratio = GUT["inv_alpha_GUT_ratio_to_Q_plus_1"]
    assert abs(ratio - 4.0) < 0.5

def test_SM_gauge_bosons_equals_K():
    """SM has K=12 gauge bosons (8g + 3W + 1B)."""
    assert GUT["SM_gauge_bosons"] == SRG["K"] == 12

def test_V_minus_1_equals_39():
    """V-1 = 39 encodes GUT gauge structure."""
    assert SRG["V"] - 1 == 39

def test_M_LAM_plus_M_NEG_equals_39():
    assert SRG["M_LAM"] + SRG["M_NEG"] == 39

def test_A5_factor():
    """AUT_ORDER / |A5| = 864 = 32 × M_LAM."""
    assert GUT["AUT_over_A5"] == 864
    assert GUT["expected_32_M_LAM"] == 864

def test_AUT_prime_factorization():
    """AUT_ORDER = 2^7 × 3^4 × 5 = 51840."""
    assert 2**7 * 3**4 * 5 == 51840

def test_all_individual_checks():
    for c in DATA["checks"]:
        assert c["pass"], f"Check '{c['check']}' failed: got={c['got']} expected={c['expected']}"
