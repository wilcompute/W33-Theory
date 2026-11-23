"""Pass 12726."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12726_round.json")))
L = json.load(open(os.path.join(ROOT, "data", "explore_pass12726_layers.json")))
S = json.load(open(os.path.join(ROOT, "analysis", "toe_status.json"), encoding="utf-8"))


def test_misalignment():
    r = {round(x["f_a"] / 1e9): x for x in D["misalignment"]["rows"]}
    assert 0.99 < r[25]["theta_i"] / 3.14159265 < 0.995 and r[170]["theta_i"] < 2.2


def test_mesogenesis_share():
    assert 0.85 < D["mesogenesis_share"]["max_share"] < 0.87


def test_brane_terms():
    b = D["brane_terms"]
    assert 1.0 < b["a4_only"] / b["natural"]["10"] < 2.0


def test_layers():
    for c in ("prose", "code"):
        r = L[c]
        assert r["none"] < r["attention"] and r["none"] < r["mlp"] and r["all"] >= max(r["attention"], r["mlp"]) - 0.05


def test_status():
    assert S["through_pass"] >= 12726 and S["falsifier"].startswith("y")
