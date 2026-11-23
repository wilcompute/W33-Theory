"""Pass 12722."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12722_round.json")))
L = json.load(open(os.path.join(ROOT, "data", "explore_pass12722_charlm64.json")))
L48 = json.load(open(os.path.join(ROOT, "data", "explore_pass12721_charlm.json")))


def test_seesaw_triplets_vs_desi():
    assert all(r["sum_NO_eV"] > 0.064 for r in D["seesaw_triplets"]["rows"])


def test_vlb():
    assert D["vlb"]["effective"][1] < 1740


def test_y_with_5():
    y = D["y_with_5"]
    assert y["Mt=172.8|5+5bar=True"] - y["Mt=172.8|5+5bar=False"] > 0.03 and 0.49 < y["Mt=172.8|5+5bar=True"] < 0.51


def test_thawing():
    t = D["thawing"]["best"]
    assert 0 < t["chi2"] < t["chi2_LCDM"]


def test_charlm64():
    assert L["fp32"]["bpc"] < L["ternary"]["bpc"] and L["ternary"]["zero_frac"] > 0.4
    assert L["fp32"]["bpc"] < L48["fp32"]["bpc"]
