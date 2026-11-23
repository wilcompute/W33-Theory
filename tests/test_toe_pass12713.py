"""Pass 12713."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12713_round.json"), encoding="utf-8"))


def test_energy_front():
    assert D["energy"]["pareto"][:2] == ["binary", "ternary"]
    assert abs(D["energy"]["rows"]["ternary"]["DRAM_pJ"] - 48.0) < 0.5


def test_missing_partner_no_go():
    s = D["missing_partner"]["splittings"]
    assert D["missing_partner"]["QU_only"] == []
    assert sum(v["dim"] for k, v in s.items() if k.startswith("24 x")) == 240
    assert sum(v["dim"] for k, v in s.items() if k.startswith("75 x")) == 750
    assert sum(v["dim"] for k, v in s.items() if k.startswith("200")) == 2000
    assert all(v["contains"]["Q"] and v["contains"]["U"] for v in s.values() if v["contains"]["E"])


def test_exclusive():
    e = D["exclusive"]["rows"]
    assert e["exclusive reach 1e-07"] < 0.3 and e["exclusive reach 1e-09"] > 0.95


def test_carries():
    c = D["carries"]["64"]
    assert c["bt_mean"] < c["bin_mean"] / 2 and abs(c["p_carry_bt"] - 0.25) < 0.01


def test_inversion():
    assert all(1.8 < r["factor"] < 3.5 for r in D["inversion"]["flat"])
