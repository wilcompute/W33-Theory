"""Pass 12685: intermediate-scale suite."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12685_intermediate_scale_suite.json")))


def test_control_reproduces_pass12684():
    assert abs(D["control_Mt_sqrt_vMPl"] - 172.57) < 0.05


def test_smash_window_at_measured_top():
    row = next(r for r in D["smash_threshold"] if r["Mt"] == 172.57)
    assert 4e10 < row["mu0"] < 7e10 and -0.012 < row["lambda_SM_min"] < -0.009
    assert 0.05 < row["lambda_sigma_max_for_fa_window"][0] < 0.2


def test_vectorlike_rescue_is_perturbative():
    for r in D["dark_dimension_rescue_vectorlike"]:
        assert r["perturbative"] and 0.45 < r["y_prime_at_MVL"] < 0.56


def test_seesaw_harmless_and_forecast():
    assert all(abs(s["dlambda_MPl"]) < 1e-4 for s in D["seesaw"])
    f = D["forecast"]
    assert f["sigma_log10mu0_future"] < f["variant_spread_decades"] < f["sigma_log10mu0_now_incl_pole_ambiguity"]
    assert f["planck_boundary_sigma_future"] > 8


def test_axion_is_not_ede():
    assert D["axion_ede"]["log10_ratio"] > 30
