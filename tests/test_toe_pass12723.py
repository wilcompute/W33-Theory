"""Pass 12723."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12723_round.json")))
L = json.load(open(os.path.join(ROOT, "data", "explore_pass12723_charlm96.json")))
L64 = json.load(open(os.path.join(ROOT, "data", "explore_pass12722_charlm64.json")))


def test_flavour_escape():
    assert all(0.1 < r["r_required"] < 0.6 for r in D["flavour_escape"]["rows"])


def test_coupled_quintessence():
    b = D["coupled_quintessence"]["best"]
    assert b["chi2"] < 3 < D["coupled_quintessence"]["chi2_LCDM"] and b["phantom"] and abs(b["beta"]) <= 0.2


def test_belle2():
    c = {r["lumi_ab"]: r for r in D["belle2"]["curve"]}
    assert c[1.0]["m1"]["frac"] < 0.15 and c[50.0]["m1"]["frac"] > 0.8


def test_charlm96():
    assert L["fp32"]["bpc"] < L64["fp32"]["bpc"] and L["ternary"]["zero_frac"] > 0.4


A = json.load(open(os.path.join(ROOT, "data", "explore_pass12723_attractor.json")))
Mz = json.load(open(os.path.join(ROOT, "data", "explore_pass12723_mesogenesis_drift.json")))


def test_attractor_floor():
    for r in A["rows"]:
        ys = [b for _, b in r["scan"] if b == b]
        assert min(ys) > 0.40 and max(ys) < 0.63


def test_mesogenesis_drift_sign():
    assert not Mz["both"] and all(r["mass_ratio"] < 1 for r in Mz["rows"])
