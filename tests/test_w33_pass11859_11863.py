"""Regression tests for Passes 11859-11863 (parity orbifold, sectors, positivity bounds, triality, Lean)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11859_11862_parity_orbifold_sectors_breaking as P  # noqa: E402

DATA = ROOT / "data"


def load():
    return json.load(open(DATA / "w33_pass11859_11862_parity_orbifold_sectors_breaking.json"))


def test_no_chirality_from_e8_automorphisms():
    d = load()
    assert not d["parity_orbifold"]["any_chiral"] and all(r["normalises_so11"] for r in d["parity_orbifold"]["samples"])
    g = d["gut_phase_times_element"]
    assert not g["any_chiral"] and g["X_charges_on_spinor_block"] == {"-5": 4, "-3": 20, "-1": 40, "1": 40, "3": 20, "5": 4}


def test_sectors_and_multiplicity_free():
    s = P.sectors()
    assert s["0"]["orbits"] == [1, 20, 30, 30] and s["1"]["orbits"] == [6, 15, 60] and s["2"]["orbits"] == [6, 15, 60]
    lp = load()["lorentz_parts"]
    assert lp["Di"] == 1.0 and lp["vector5"] == 1.0 and lp["Sym2Di"] == 1.0
    assert all(v == 0.0 for v in lp["overlaps"].values())


def test_central_translation_is_colour_triality_and_b_minus_l():
    b = load()["breaking"]
    assert b["tc_equals_exp_8pi_i_Y"] < 1e-6 and b["q_equals_12Y_mod_3"]
    assert b["contains_SM_algebra"] and b["rank"] == 5 and b["centre_dim"] == 1
    assert b["centre_spectrum_on_spinor_block"] == {"-3/4": 16, "-1/4": 48, "1/4": 48, "3/4": 16}


def test_positivity_bounds():
    c = json.load(open(DATA / "w33_pass11861_bootstrap_positivity_bounds.json"))
    ch = {r["dim"]: r for r in c["channels"]}
    assert (ch[60]["E15"], ch[60]["D"]) == (-96.0, 2.0) and (ch[24]["E15"], ch[24]["E20"]) == (96.0, -16.0)
    assert (ch[1]["D"], ch[1]["C"], ch[1]["E15"], ch[1]["E20"]) == (17.0, 60.0, 576.0, 64.0)
    b = c["bounds"]
    assert abs(b["g3_squared_max_from_60_channel"] - 1 / 48) < 1e-12
    assert abs(b["g_prime_squared_max_at_g3_zero_from_24_channel"] - 1 / 8) < 1e-12
    assert abs(b["g4_window_at_g3_gprime_zero"][1] - 1 / 12) < 1e-12


def test_lean_module():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11863A6NotInSL2" in root
    src = (ROOT / "formal" / "W33" / "Pass11863A6NotInSL2.lean").read_text(encoding="utf-8")
    for name in ("sl2_involution", "no_injective_hom", "s1_ne_s2"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
