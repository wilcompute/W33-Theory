"""Pass 12704."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12704_round.json")))


def test_so10():
    s = D["so10_light_QU"]
    assert s["singlets"] == {"210": 3, "45": 2}
    assert not any(v["degenerate_with_Q"] == ["Q", "u^c"] for v in s["vacua_210_only"])
    assert s["n_QU_only"] > 0 and all(abs(x) > 0.1 for x in next(r for r in s["vacua_45_210"] if r["QU_only"])["others"].values())


def test_tan_beta():
    c = D["tau_on_PQ_doublet"]["cases"]
    t = sorted(v["tan_beta_min"] for v in c.values())
    assert 1.3 < t[0] < 1.8 and 2.7 < t[1] < 3.3


def test_tree_window():
    w = D["tree_splitting_window"]
    assert w["window_log10_delta_frac_gt_5pct"] == [-12.0, -5.0]
    f = {r["log10_delta"]: r["frac_ge_obs"] for r in w["scan"]}
    assert f[-15.0] == 0 and f[-2.0] == 0 and f[-9.0] > 0.95


def test_B_band_and_forecast():
    b = {r["R_um"]: r["yprime"] for r in D["B_dark_graviton_band"]["rows"]}
    assert 0.50 < b[1.0] < 0.515 and 0.525 < b[30.0] < 0.535
    f = D["forecast"]["scenarios"]
    assert f["fcc"]["sigma_log10_mu0"] < 0.25 < f["today"]["sigma_log10_mu0"]
    sep = {(r["MSS"], r["B"]): r["sigma"] for r in f["fcc"]["separation"]}
    assert sep[(1e10, "R>=1um")] > 5 and sep[(3e9, "R>=0.1um")] < 3
