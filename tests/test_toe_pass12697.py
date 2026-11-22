"""Pass 12697."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12697_round.json")))


def test_doublet_and_mixing():
    assert all(r["m_H2_GeV"] > 1e4 for r in D["pq_doublet"]["rows"])
    b = D["b_mixing"]
    assert b["theta_t_max"] > 100 * b["cascade_boundary"] and b["theta_b_max"] > 100 * b["cascade_boundary"]


def test_candidates_superallowed_ranking():
    assert 1e-10 < D["kev_candidates"]["ALP m=2 MeV"]["g_agg_GeV_inv"] < 1e-8
    s = D["superallowed"]
    assert -7 < s["Ft_shift_s"] < -5 and s["shift_over_dNS_unc"] > 10
    r = D["ranking_bic"]
    assert r["Completion B (dark dim + VL, GeV reheating)"]["bayes_factor_vs_SM"] > r["Completion A (b-only PQ, extra scalar, xi>=10)"]["bayes_factor_vs_SM"] > r["lambda(M_Pl) = 0"]["bayes_factor_vs_SM"]
