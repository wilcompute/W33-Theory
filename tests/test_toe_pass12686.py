"""Pass 12686: intermediate-scale follow-ups."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12686_intermediate_scale_followups.json")))


def test_T_parameter_calibrated_and_small():
    c = D["T_parameter"]["calibration"]
    assert abs(c["T_sm_top"] - c["expected"]) < 1e-9 and abs(c["degenerate_doublet"]) < 1e-9
    assert all(abs(r["T"]) < 0.01 for r in D["T_parameter"]["rescue"])


def test_joint_pulls():
    j = D["joint_boundary_test"]["results"]
    assert abs(j["sqrt(v M_Pl)"]["direct"]["pull"]) < 0.5 and abs(j["axion f_a (lattice 2025)"]["direct"]["pull"]) < 0.5
    assert j["M_Pl"]["direct"]["pull"] > 2 and j["dark dimension M5 (R 1-30 um)"]["direct"]["pull"] < -2


def test_inflation_ns_low_vs_act():
    ok = [r for r in D["inflation"]["rows"] if r["r_ok"]]
    assert max(r["ns"] for r in ok) < 0.969 and min(r["pull_ns"] for r in ok) < -1.5


def test_neutrinos_and_gw():
    assert all(4e-4 < r["y_for_0p05eV"] < 2e-3 for r in D["dark_dimension_neutrinos"]["rows"])
    assert D["axion_string_GW"]["suppression_vs_fa_1e15"] < 1e-12
