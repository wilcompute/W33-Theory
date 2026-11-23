"""Pass 12733."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12733_round.json")))


def test_brane_proton():
    rows = [r for r in D["brane_proton"]["rows"] if r["Lambda_R"] == 10]
    weak = next(r for r in rows if r["coupling"] == "weak"); strong = next(r for r in rows if r["coupling"] == "NDA strong")
    assert weak["tau_yr"] > 1e37 and strong["tau_yr"] < 1e35


def test_evidence_order():
    e = D["evidence"]["rows"]["15"]
    assert e["hybrid"] < e["Bprime"] and e["hybrid"] < e["A_escape"] and max(e.values()) < 1


def test_figure_and_belle():
    assert os.path.exists(os.path.join(ROOT, "analysis", "figures", "y_floor.png"))
    assert 0.45 < D["belle_2026"]["mesogenesis_share_max"] < 0.55
