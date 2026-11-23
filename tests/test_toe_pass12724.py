"""Pass 12724."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12724_round.json")))
L32 = json.load(open(os.path.join(ROOT, "data", "explore_pass12724_charlm32_fixed.json")))
L48 = json.load(open(os.path.join(ROOT, "data", "explore_pass12724_charlm48_fixed.json")))
L96 = json.load(open(os.path.join(ROOT, "data", "explore_pass12723_charlm96.json")))


def test_two_component():
    assert 0.75 < D["two_component"]["f_psi_max"] < 0.85


def test_y_floor():
    f = D["y_floor_mc"]
    assert 0.33 < f["p2_5"] < 0.38 and 0.38 < f["median"] < 0.42


def test_orbifold():
    o = {r["MsR"]: r for r in D["orbifold_thresholds"]["rows"]}
    assert abs(o[10]["shift_alpha3_inv"]) < 0.5 and o[100]["shift_alpha3_inv"] < -2


def test_growth_sign():
    g = {(r["lam"], r["beta"]): r for r in D["growth"]["rows"]}
    assert g[(1.0, 0.0)]["sigma8_ratio"] < 1 < g[(1.0, 0.1)]["sigma8_ratio"]


def test_fixed_corpus_scaling():
    gaps = [L32["ternary"]["bpc"] - L32["fp32"]["bpc"], L48["ternary"]["bpc"] - L48["fp32"]["bpc"], L96["ternary"]["bpc"] - L96["fp32"]["bpc"]]
    assert gaps[2] < gaps[0]
