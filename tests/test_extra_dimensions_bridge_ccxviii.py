"""Regression tests for Part CCXVIII — Extra Dimensions and KK Theory from W(3,3)."""
import json, math, pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "PART_CCXVIII_extra_dimensions_results.json").read_text(encoding="utf-8"))
KK   = DATA["kk_data"]
SRG  = DATA["srg_params"]

def test_verified():
    assert DATA["verified"] is True

def test_free_parameters_zero():
    assert DATA["free_parameters"] == 0

def test_KK_superstring_extra_dims():
    assert KK["KK_super_extra_dims"] == 6

def test_KK_Mtheory_extra_dims():
    assert KK["KK_M_extra_dims"] == 7

def test_KK_ADD_dims():
    assert KK["KK_ADD_dims"] == 2

def test_KK_mass_ground():
    assert KK["KK_mass_ground"] == 0

def test_KK_mass_L1():
    assert KK["KK_mass_L1"] == 10

def test_KK_mass_L2():
    assert KK["KK_mass_L2"] == 16

def test_KK_mass_ratio():
    assert abs(KK["KK_mass_ratio"] - 1.6) < 1e-3

def test_RS_warp_factor():
    assert KK["RS_warp"] == 18

def test_RS_kr_exponent():
    assert abs(KK["RS_kr_exponent"] - math.log(51840 / 1600)) < 1e-3

def test_N_KK_modes():
    assert KK["N_KK_modes"] == 240

def test_KK_coupling():
    assert abs(KK["KK_coupling"] - 0.3) < 1e-4

def test_UED_level1():
    assert KK["UED_level1"] == 27

def test_UED_level2():
    assert KK["UED_level2"] == 12

def test_KK_total_excitations():
    assert KK["KK_total_excitations"] == 39

def test_SM_4D_fields():
    assert KK["SM_4D_fields"] == 14

def test_SUSY_breaking_scale():
    assert KK["M_SUSY_proxy"] == 10

def test_extra_dim_volume():
    assert abs(KK["extra_dim_volume_proxy"] - round(240/27, 4)) < 1e-3

def test_all_individual_checks():
    for c in DATA["checks"]:
        assert c["pass"], f"Check '{c['check']}' failed: got={c['got']} expected={c['expected']}"
