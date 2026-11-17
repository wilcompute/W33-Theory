"""Pass 12688: running-quartic inflation, dark-dimension cosmology, FCC separation, ACT without DESI, ranking."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12688_intermediate_scale_round4.json")))


def test_running_quartic_reaches_act():
    n = D["running_quartic_inflation"]["needed"]
    assert 0.03 < n["xi=1 P-ACT-LB 0.9743"]["b"] < 0.05 and n["xi=1 P-ACT-LB 0.9743"]["r"] < 0.036
    assert 0.015 < n["xi=10 P-ACT 0.9709"]["b"] < 0.025
    # the Higgs portal would have to be >~ sqrt(lambda_sigma): delta = portal^2/lambda_sigma >~ 1 -> non-perturbative
    assert all(c["portal_over_sqrt_lambda_sigma"] > 1 for c in D["running_quartic_inflation"]["couplings"].values())


def test_dark_dimension_excludes_intermediate_scale_cosmology():
    o = D["dark_dimension_cosmology"]["overproduction_T3"]
    assert o["T = f_a ~ 1e11 GeV (post-inflation PQ)"] > 1e30 and o["T = 1 GeV (graviton DM)"] == 1.0


def test_fcc_and_act():
    s = D["fcc_separation"]
    assert s["FCC-ee, current NNLO matching"]["sqrtvMPl_vs_sqrtvMbar_sigma"] < 2 < s["FCC-ee, matching N3LO (errors /4)"]["sqrtvMPl_vs_sqrtvMbar_sigma"]
    assert -1.6 < D["act_without_desi"]["SMASH_pull_PACT"] < -1.3


def test_ranking():
    r = D["ranking"]
    assert abs(r["dark dimension + VL quark, T_i ~ 1 GeV (non-thermal gravitons)"]["dAIC"] - 2.0) < 0.01
    assert r["full SMASH with running quartic (b fitted)"]["dAIC"] < 2.1 < r["lambda(M_Pl) = 0 (AS / MPP)"]["dAIC"]
