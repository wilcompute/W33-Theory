"""Pass 12699."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12699_round.json")))


def test_scout_and_potential():
    assert D["anomaly_scout"]["fa_over_Cbs_needed_GeV"] < 1e9 and D["anomaly_scout"]["A_prediction"] < 1e-10
    assert D["dfsz_potential"]["bounded_below"] and D["dfsz_potential"]["m_H2_GeV"] > 1e6


def test_toy_mc_and_haloscope():
    a = D["toy_mc_soft_lepton"]["acceptance"]
    assert 0.7 < a["pT>7.0"] < 0.95 and a["pT>15.0"] < a["pT>10.0"] < a["pT>7.0"]
    assert D["haloscope"]["rows"]["b only (A)"]["time_rel_DFSZ"] < 0.2


def test_susy_tanbeta_bridge():
    rows = {r["log10_MSS"]: r for r in D["high_scale_susy_tanbeta"]["rows"]}
    assert 1.0 < rows[10.0]["tan_beta"] < 1.5 and rows[11.0]["tan_beta"] is None
