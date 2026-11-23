"""Pass 12717."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12717_round.json"), encoding="utf-8"))


def test_geometric():
    g = D["geometric"]["rows"]
    assert 30 < g[0]["ML_min"] < 31 and g[0]["KK_max"] < 4e15


def test_45_54():
    v = D["v45_54"]
    assert v["zero_modes"] == 30 and sum(v["spectrum"].values()) == 99 - 30 and v["a2"] > 0


def test_proton():
    assert all(r["tau_years"] / 10 > 1e35 for r in D["proton"]["rows"])


def test_flash():
    r = {x["snr"]: x for x in D["flash"]["rows"]}
    assert r[32.0]["q2_per_read"] > r[32.0]["q3_per_read"] > r[32.0]["q4_per_read"]
    assert r[32.0]["q8_bits"] > r[32.0]["q3_bits"] > r[32.0]["q2_bits"]


def test_attention():
    a = D["attention"]["rows"]
    assert a["ternary"]["acc"] > 0.98 and a["ternary"]["zero_frac"] > 0.4 and a["binary"]["acc"] < a["ternary"]["acc"]
