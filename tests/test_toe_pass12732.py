"""Pass 12732."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12732_round.json")))


def test_freeze_in():
    assert all(20 < r["x"] < 30 for r in D["freeze_in"]["rows"])


def test_proton_orbifold():
    r = {x["Lambda_R"]: x for x in D["proton_orbifold"]["rows"]}
    assert r[10]["tau_yr"] < 2.4e34 < r[3]["tau_yr"]


def test_floor_referee():
    f = {x["N"]: x["floor"] for x in D["floor_referee"]["families"]}
    assert abs(f[2] - 0.336) < 0.01


def test_saxion():
    s = D["saxion"]["rows"]
    assert any(x["dominates"] for x in s if x["m_s"] == 1e4) and not any(x["dominates"] for x in s if x["m_s"] == 1e8)
