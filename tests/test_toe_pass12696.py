"""Pass 12696."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12696_round.json")))


def test_pq_scan_has_visible_ndw1_third_family():
    s = D["pq_scan"]
    assert s["n_third_family_visible"] > 0
    b_only = [r for r in s["simplest"] if r["x_u"] == 0 and abs(r["x_d"]) == 1 and r["x_e"] == 0 and r["x_Q"] == 0]
    assert b_only and abs(b_only[0]["E_over_N"] - 2 / 3) < 1e-9 and b_only[0]["g_rel"] > 0.6


def test_fcc_kev_ft():
    assert all(r["delta_yprime"] < 0.005 for r in D["fcc_yprime"])
    assert all(1e3 < r["lifetime_s"] < 1e5 for r in D["kev_particle"]["rows"])
    assert -6 < D["ft_shift"]["shift_needed_s"] < -4.5
