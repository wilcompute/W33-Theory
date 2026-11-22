"""Pass 12701."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12701_round.json")))


def test_leptogenesis():
    r = D["leptogenesis_A"]["rows"]
    lo = r["m~ = m_atm, M=1.24e+07"]
    assert 9 < lo["Delta"] < 11 and 1e-5 < lo["degeneracy_dM_over_M"] < 1e-3
    assert r["m~ = m_sol, M=1e+09"]["enhancement"] > 1   # even at 1e9 hierarchical needs mild help for these kappas


def test_split_bridge():
    s = D["split_bridge"]
    assert 7.3 < s["log10_ceiling"] < 8.0
    rows = {r["log10_MSS"]: r for r in s["rows"]}
    assert rows[8.0]["tan_beta"] is None and 1.3 < rows[7.0]["tan_beta"] < 1.6


def test_repair_and_two_loop():
    e = D["e6_repair"]
    assert abs(e["hits"][0]["delta"]) < 0.8 and e["hits"][0]["M12"] > 1e16
    assert 0.44 < e["vl_quartic_zero"]["yprime_for_mu0_1e10"] < 0.51
    t = D["two_loop_unification"]["rows"]
    assert abs(t["MSSM at 1 TeV"]["delta_a3_inv"]) < 0.3 and t["high-scale SUSY 1e10"]["tau_p_years"] < 1e30
    assert t["MSSM at 1 TeV"]["delta_a3_inv"] - (-0.62) > 0.5   # two-loop shift is positive (+0.8)
