"""Pass 12707."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12707_round.json"), encoding="utf-8"))


def test_card_and_drift():
    assert D["card"]["Mt"]["value"] == 172.57 and D["card"]["dark_dimension"]["R_max_um"] == 0.2
    assert "1650.0" in D["drift"]["M_VL_values_seen"] and any(v.startswith("1740") for v in D["drift"]["M_VL_values_seen"])


def test_threshold():
    for r in D["threshold"]["rows"].values():
        assert 0.005 < r["shift"] < 0.010            # one-loop finite threshold raises y' by ~0.006-0.009
        assert r["with_V"] > r["with_V_and_Z"] > r["no_threshold"]


def test_sensitivity():
    m = D["sensitivity"]["mu0"]
    assert 5.0e10 < m["PDG"] < 5.8e10 and m["PDG+FLAG"] > 7.5e10
    assert m["Mt+0.5 (scheme)"] < 1.5e10 and m["Mt-0.5 (scheme)"] > 3e11
    e = D["sensitivity"]["errors"]
    assert 0.015 < e["today exp"]["sigma_yprime"] < 0.022 and e["FCC era"]["sigma_yprime"] < 0.005


def test_B_revised():
    b = D["B_revised"]
    lo, hi = b["surviving_yB"]
    assert 0.485 < lo < 0.49 and 0.50 < hi < 0.51
    surv = [r for r in b["rows"] if not r.get("excluded_by_2610_01825")]
    assert all(0.015 < r["gap"] < 0.04 for r in surv)
    assert all(r["gap"] > 0.04 for r in b["rows"] if r.get("excluded_by_2610_01825"))


def test_reheating():
    assert all(r["T_RH_max_est"] >= 5.96 - 1e-9 for r in D["reheating"]["rows"])
