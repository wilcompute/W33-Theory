"""Pass 12703."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12703_round.json")))


def test_650_needs_75():
    e = D["e6_650"]
    assert e["f75_on_Q_uc_ec"] == [1, -1, -3] and e["m_ec"] == "10*m0" and e["SM_singlets"] == {"650": 11, "1+78": 6, "total": 17}
    u = e["light_block_unification"]
    assert abs(u["SU(5)-75 direction: Q + U"]["delta"]) < 0.5
    assert all(abs(v["delta"]) > 1.5 for k, v in u.items() if not k.startswith("SU(5)-75"))


def test_two_loop_vl_small():
    t = D["two_loop_vectorlike"]
    h = t["hybrid_1e10_MVL1740"]; assert 0 < h["two_loop_VL"] - h["one_loop_VL"] < 0.005
    assert all(abs(r["two_loop_VL"] - r["one_loop_VL"]) < 0.005 for r in t["B_MVL1650"])


def test_B_hybrid_overlap():
    b = D["B_vs_hybrid"]
    assert 0.49 < b["B_band_two_loop"][0] < 0.50 and b["B_band_two_loop"][1] < 0.54
    assert 1e9 in b["hybrid_MSS_overlapping_B"] and 1e10 not in b["hybrid_MSS_overlapping_B"]


def test_radiative_leptogenesis_short():
    l = D["leptogenesis_O2_model"]
    assert l["control_ytau0"] < 1e-4 * l["invariance_Re_z"][0]
    assert all(v["frac_ge_obs"] == 0 and v["eta_max"] < 6.1e-10 for v in l["scan"].values())
    assert 1.5 < l["ytau_min_factor"] < 2.2 and l["ytau_scaling"]["10"]["frac_ge_obs"] > 0.5


def test_review():
    assert D["review_a790aef"]["rerun_pass"] and D["review_a790aef"]["full_rank"] == 14
