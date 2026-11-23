"""Pass 12708 and the ternary/simplex note."""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12708_round.json"), encoding="utf-8"))
N = json.load(open(os.path.join(ROOT, "data", "ternary_radix_simplex_note.json"), encoding="utf-8"))


def test_dwave():
    s = D["dwave"]["slopes"]
    assert abs(s["grav"] - 2) < 0.02 and abs(s["YM"] - 1) < 0.02 and abs(s["s_wave"]) < 0.02
    assert abs(D["dwave"]["width_power"] - 5) < 0.05


def test_msbar_route():
    r = D["msbar_route"]["rows"]
    assert abs(r["central"]["pole"] - 172.3) < 0.1 and 0.15 < D["msbar_route"]["four_loop_term"] < 0.25
    assert r["-1.5"]["mu0"] == float("inf") and r["+2.1"]["mu0"] < 1e9


def test_threshold_checks():
    t = D["threshold_checks"]
    assert abs(t["cw_ratio"] - 1) < 1e-3 and abs(t["Z_const"] - 1 / 3) < 1e-9
    assert max(t["gauge_shift_alpha_inv"].values()) < 1e-3


def test_kappa():
    k = D["kappa_map"]["rows"]
    assert k["kappa = sqrt2 sin"]["consistent"] and not k["kappa = sin"]["consistent"]


def test_ternary_note():
    assert abs(N["radix_economy"]["gain_3_over_2"] - 0.0536) < 0.001
    assert all(abs(g["total_deficit_over_pi"] - 4) < 1e-9 and g["chi"] == 2 for g in N["gauss_bonnet"])
    w = N["w33_clique_complex"]
    assert w["f_vector"] == [40, 240, 160, 40] and all(b == [1, 81, 0, 0] for b in w["betti"].values())
