"""Passes 12690-12691."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D0 = json.load(open(os.path.join(ROOT, "data", "toe_pass12690_completion_followups.json")))
D1 = json.load(open(os.path.join(ROOT, "data", "toe_pass12691_three_anomalies.json")))


def test_vlq_splitting_is_yprime():
    for r in D0["vlq_triplet"]["rows"]:
        assert abs(r["dM_TTp"] - r["y_prime"] * 246.22 / 2 ** 0.5) < 1e-6 and r["dM_BT"] < 80.4


def test_leptogenesis_needs_large_xi():
    rows = {(r["M_N"], r["xi"], r["c"]): r["cancellation_factor"] for r in D0["leptogenesis_vs_inflation"]["rows"]}
    assert rows[(1e9, 1.0, 2.0)] > 50 and rows[(1e9, 100.0, 2.0)] < 0.1


def test_alpha_from_ae_matches_fan_et_al():
    a = D1["electron_g2_alpha"]["alpha from a_e | C5 Volkov 2024"]
    assert abs(a["alpha_inv"] - 137.035999166) < 3e-9
    assert D1["electron_g2_alpha"]["Cs 2018 | C5 AKN 2019"]["pull"] < -3.5 and abs(D1["electron_g2_alpha"]["Rb 2020 | C5 AKN 2019"]["pull"]) < 2.5


def test_km3net_and_neutron():
    assert 1.4 < D1["km3net"]["rows"]["r=15"]["sigma_one_sided"] < 1.6
    n = D1["neutron_lifetime"]
    assert n["beam_vs_bottle_sigma"] > 5 and abs(n["tau_SM from g_A (PERKEO III)"]["pull_vs_bottle"]) < 1.5
