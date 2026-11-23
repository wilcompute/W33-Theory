"""Pass 12725."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12725_round.json")))
C32 = json.load(open(os.path.join(ROOT, "data", "explore_pass12725_codelm32.json")))
C64 = json.load(open(os.path.join(ROOT, "data", "explore_pass12725_codelm64.json")))


def test_so10_orbifold():
    r = {x["MsR"]: x for x in D["so10_orbifold"]["rows"]}
    assert r[10]["shift"] < -1.0 and r[100]["shift"] < r[10]["shift"]


def test_partial_coupling():
    g = D["partial_coupling"]["good"]
    assert g and all(p["chi2"] < 4 and p["sigma8_ratio"] <= 1.0 for p in g)


def test_fcc_floor():
    f = D["fcc_floor"]
    assert 0.39 < f["p2_5"] < 0.41 and f["p97_5"] < 0.44


def test_code_lm():
    for L in (C32, C64):
        assert L["fp32"]["bpc"] < L["ternary"]["bpc"] and L["ternary"]["zero_frac"] > 0.4
    # observed: on code the gap widens from width 32 to 64 (the prose-corpus width^-0.59 law does not carry over here)
    assert (C64["ternary"]["bpc"] - C64["fp32"]["bpc"]) > (C32["ternary"]["bpc"] - C32["fp32"]["bpc"])


AX = json.load(open(os.path.join(ROOT, "data", "explore_pass12725_axion_shift.json")))


def test_axion_shift():
    r = {x["Mt"]: x for x in AX["rows"]}
    assert r[172.8]["m_a_ueV"] > 200 and r[172.8]["DM_fraction"] < 0.25 and 172.3 < AX["Mt_for_full_DM"] < 172.45
