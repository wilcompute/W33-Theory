"""Pass 12709."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12709_round.json"), encoding="utf-8"))


def test_B_prime():
    rows = D["B_prime"]["rows"]
    assert all(r["window_MeV"][0] >= 5.0 and r["window_MeV"][1] <= 60.0 for r in rows)
    assert all(4e-8 < r["ACP_Br_needed"]["m_Phi=11"][0] < 2e-7 for r in rows)


def test_w33_curvature():
    w = D["w33_curvature"]
    assert w["banchoff"] == -2.0 and w["chi"] == -80 and w["triangle_in_tet"] == 1 and w["edge_in_tet"] == 1


def test_stability():
    s = D["stability"]
    assert 170.8 < s["Mt_crit"]["0.118"] < 171.2
    f = s["forecast"]
    assert f["today exp + scheme"]["P_stable"] > 1e-3 and f["FCC-ee (central PDG)"]["P_stable"] < 1e-20


def test_evidence():
    e = D["evidence"]["rows"]
    r = e["exp only (12698: 0.43) | width 15"]
    assert abs(r["boundary"] - 13.5) < 0.6 and abs(r["A"] - 2.6) < 0.4
    assert all(v["B_prime"] < 0.1 and v["boundary_trials"] < 2 for v in e.values())
