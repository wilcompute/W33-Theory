"""Pass 12721."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, "data", "explore_pass12721_misc.json")))
L = json.load(open(os.path.join(ROOT, "data", "explore_pass12721_charlm.json")))


def test_counting():
    a = M["counting"]["(a) Sigma(LR) + H(SU5)"]; b = M["counting"]["(b) Sigma(LR) + coupled (Sigma', H) -> SM"]
    assert sum(a.values()) == 18 and sum(b.values()) == 30 and b.get("(3,2)-0.833") == 6


def test_unification():
    u = M["unification"]
    assert abs(u["Q + U (hybrid)"]["delta"] - 0.26) < 0.03
    assert u["Q + U + X(3,2)_5/6  [case b]"]["delta"] < -1
    assert abs(u["Q + U + D + L  [Pass 12720, eps = 0]"]["delta"] - 0.26) < 0.05


def test_ions_casimir_proton():
    assert not any(v["passes"] for v in M["ions"].values())
    assert M["casimir"]["required_suppression"] < 1e-7
    assert M["light_triplet_proton"]["max_product_yqq_yql"] < 1e-24


def test_charlm():
    assert L["fp32"]["bpc"] < L["2bit"]["bpc"] < L["ternary"]["bpc"] < L["binary"]["bpc"] < L["unigram_bpc"]
    assert L["ternary"]["zero_frac"] > 0.4
