"""Regression tests for Part CCXVII — String Theory Landscape and Vacuum Selection from W(3,3)."""
import json, math, pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "PART_CCXVII_string_landscape_results.json").read_text(encoding="utf-8"))
STR  = DATA["string_data"]
SRG  = DATA["srg_params"]

def test_verified():
    assert DATA["verified"] is True

def test_free_parameters_zero():
    assert DATA["free_parameters"] == 0

def test_bosonic_string_dim():
    """Bosonic string critical dimension = M_LAM - 1 = 26."""
    assert STR["D_bosonic"] == 26

def test_superstring_dim():
    """Superstring critical dimension = LAP_MID = 10."""
    assert STR["D_superstring"] == 10

def test_mtheory_dim():
    """M-theory dimension = LAP_MID + 1 = 11."""
    assert STR["D_Mtheory"] == 11

def test_landscape_log10():
    """String landscape log10(N_vac) ~ M_LAM = 27."""
    assert STR["landscape_log10"] == 27

def test_compactification_dim():
    """Bosonic-Super compactification dimension = LAP_TOP = 16."""
    assert STR["D_compact"] == 16

def test_E8_dim():
    """dim(E8) = 248."""
    assert STR["E8_dim"] == 248

def test_E8xE8_dim():
    """dim(E8×E8) = 496."""
    assert STR["E8xE8_dim"] == 496

def test_rank_E8xE8():
    """rank(E8×E8) = LAP_TOP = 16."""
    assert STR["rank_E8xE8"] == 16

def test_stability_fraction():
    """Spectral stability fraction M_LAM/V = 0.675."""
    assert abs(STR["stability_fraction"] - 0.675) < 1e-8

def test_string_coupling_weak():
    """String coupling g_s = XI_POS/LAP_TOP = 0.125 < 1."""
    assert STR["g_string"] < 1.0
    assert abs(STR["g_string"] - 0.125) < 1e-10

def test_dilaton_ratio():
    """1/g_s = LAP_TOP/XI_POS = 8."""
    assert abs(STR["dilaton_ratio"] - 8.0) < 1e-10

def test_moduli_flux_product():
    """Moduli flux product LAP_TOP × LAP_MID = 160."""
    assert STR["moduli_flux_product"] == 160

def test_W_flux():
    """Flux superpotential W_flux = MU × M_NEG = 48."""
    assert STR["W_flux"] == 48

def test_Dbrane_charge_types():
    """D-brane charge types = M_NEG = K = 12."""
    assert STR["N_dbrane"] == 12

def test_CY3_Euler():
    """Calabi-Yau Euler characteristic = M_LAM = Q^3 = 27."""
    assert STR["CY3_Euler"] == 27

def test_all_individual_checks():
    for c in DATA["checks"]:
        assert c["pass"], f"Check '{c['check']}' failed: got={c['got']} expected={c['expected']}"
