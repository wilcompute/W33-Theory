"""Pass 12700."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12700_round.json")))


def test_threshold_bridge():
    c = D["tanbeta_threshold"]["cases"]
    x0 = c["Xt=0.00,Mt=172.57"]
    assert 10.6 < x0["log10_MSS_max"] < 10.9                       # reproduces Pass 12699's ceiling
    assert abs(x0["rows"][2]["tan_beta"] - 1.26) < 0.02
    assert c["Xt=2.45,Mt=172.57"]["log10_MSS_max"] < 9.0             # maximal mixing lowers the ceiling
    assert c["Xt=0.00,Mt=172.27"]["log10_MSS_max"] > 11.0            # -1 sigma M_t lifts it above 1e11


def test_A_scan():
    a = D["A_scan"]
    assert a["agreement"] == a["n"] and 0 < a["bounded_below"] < a["n"]
    assert a["tuning"]["leff=0.3,mH2=1e+08"] > 1e9 and 3e3 < a["mH2_at_Delta10"] < 1e4


def test_unification_and_ledger():
    u = D["unification"]["rows"]
    assert abs(u["MSSM at 1 TeV"]["delta_a3_inv"]) < 1 < abs(u["high-scale SUSY 1e10"]["delta_a3_inv"])
    L = D["naturalness_ledger"]["rows"]
    assert L["seesaw M_N=5e+08"] > 1e5 and L["B: VL top partner y'=0.51, M=1.74 TeV"] < 10
