"""Pass 12728."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12728_round.json")))
Dp = json.load(open(os.path.join(ROOT, "data", "explore_pass12728_deep.json")))


def test_low_scale_inflation_vs_act():
    assert all(r["sigma_from_ACT_plateau"] > 4 and 40 < r["N"] < 50 for r in D["inflation"]["rows"])


def test_sign_check():
    assert D["sign_check"]["consistent"]


def test_timeline():
    c = D["timeline"]["coverage"]
    assert c["2042"]["Bprime"] > 0.7 and c["2045"]["A"] > 0.9 and c["2041"]["hybrid"] < 0.2


def test_deep():
    r = Dp["code"]
    gap_all, gap_l0 = r["all_ternary"] - r["fp32"], r["ternary_fp_layer0"] - r["fp32"]
    assert r["fp32"] < r["ternary_fp_layer0"] < r["all_ternary"] and gap_l0 < gap_all
