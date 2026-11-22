"""Pass 12695."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12695_round.json")))


def test_flavon_and_hllhc():
    assert 1000 < D["light_flavon"]["v_F_min_GeV"] < 3000
    r = D["hl_lhc_reach"]
    assert r["M_VL_discovery"] < r["current_M_VL_limit"] < r["M_VL_exclusion"]


def test_third_family_axion():
    q = D["third_family_axion"]["rows"]["quarks only (t, b)"]
    assert abs(q["E_over_N"] - 5 / 3) < 1e-9 and q["N_DW"] == 2 and q["g_agg_relative_to_KSVZ"] < 0.15


def test_kev_window_and_vud():
    k = D["kev_window"]
    assert 5 < k["T_no_photodisintegration_keV"] < 6 and k["DH_pull_PArthENoPE"] < 2.5 < k["DH_pull_PRIMAT"]
    v = D["Vud_neutron"]
    assert abs(v["bottle 877.8"]["unitarity_K_l3"]["deficit_sigma"]) < 1.5 and v["superallowed_Kl3"]["deficit_sigma"] < -2.5
