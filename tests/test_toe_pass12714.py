"""Pass 12714."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12714_round.json"), encoding="utf-8"))
M = json.load(open(os.path.join(ROOT, "data", "explore_pass12714_mss.json")))


def test_pgb():
    p = D["pgb"]
    assert p["unbroken"] == 15 and p["broken"] == 30
    assert sum(p["decomposition"].values()) == 30
    assert not any("(1," in k for k in p["decomposition"])          # no colour singlets: no e^c-type Goldstones


def test_signed_digit():
    assert D["signed_digit"]["correct"] and D["signed_digit"]["locality"] == 2


def test_inclusive():
    f = [r["frac_B_prime"] for r in D["inclusive"]["rows"]]
    assert min(f) > 0.4 and max(f) > 0.99


def test_mixed():
    front = D["mixed"]["front"]
    assert front[-1]["modes"][0] == "2bit"


def test_mss_relation():
    r = {(x["c"], x["M_VL"]): x for x in M}
    assert 8e9 < r[(1.0, 1740.0)]["M_SS"] < 9e9 and r[(1.0, 3000.0)]["y_hybrid"] < r[(1.0, 1740.0)]["y_hybrid"]
