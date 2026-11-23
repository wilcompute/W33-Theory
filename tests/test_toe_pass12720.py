"""Pass 12720."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = json.load(open(os.path.join(ROOT, "data", "explore_pass12720_unified.json")))
C = json.load(open(os.path.join(ROOT, "data", "explore_pass12720_curriculum.json")))
M = json.load(open(os.path.join(ROOT, "data", "explore_pass12720_misc.json")))


def test_unified_eps0():
    r = U["0.0"]
    assert r["zero_modes"] == 61 and r["orbit_rank"] == 33 and r["uneaten"] == 28
    c = r["content"]
    assert c["(3,2)+0.167"] == 6 and c["(3,1)-0.667"] == 3 and c["(1,2)+0.500"] == 2 and c["(3,1)+0.333"] == 3


def test_unified_eps_lifts_all():
    r = U["0.2"]
    assert r["grad_norm"] < 1e-7 and r["uneaten"] == 0


def test_curriculum():
    assert all(min(v["accs"]) > 0.98 and v["zero_frac"] > 0.4 for v in C.values())


def test_stability_and_qutrit():
    assert all(r["P_stable"] < 5e-3 for r in M["stability"]["rows"])
    assert all(r["ratio"] > 10 for r in M["qutrit"]["rows"])
