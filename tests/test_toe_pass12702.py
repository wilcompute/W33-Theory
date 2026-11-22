"""Pass 12702."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12702_round.json")))


def test_hybrid_two_loop():
    h = D["hybrid"]
    r = h["rows"]["1740"]
    assert 0.44 < r["yprime_mu0_1e10"] < 0.48 and abs(r["delta_two_loop"]) < 0.5 and r["M12"] > 1e16
    assert h["no_VL_delta"] < -3
    b = h["yprime_band_174"]
    assert b["mu0=1e9"] > r["yprime_mu0_1e10"] > b["mu0=1e11"] and b["Mt-0.3"] > b["Mt+0.3"]
    assert r["tau_p"] > 1e36                                   # beyond Hyper-K


def test_e6_obstruction():
    e = D["e6_obstruction"]
    assert e["rank_QUE_rows"] == 2 and e["m_ec_when_Q_U_massless"] == "0" and e["n_SM_mass_parameters"] == 17 > e["max_from_1_plus_78"]


def test_radiative_leptogenesis():
    r = D["leptogenesis_radiative"]["rows"]
    assert 2 < r["Lambda = f_a = 1e11"]["dM_over_Gamma"] < 4 and r["Lambda = M_Pl"]["sinphi_needed"][1] < 1e-3
