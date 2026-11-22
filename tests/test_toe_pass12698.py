"""Pass 12698."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12698_round.json")))


def test_evidence_prior_driven():
    e = D["evidence"]
    assert -0.06 < e["dy_dmt"] < -0.02
    s = e["prior_sensitivity"]
    assert s["SM m_t prior width 15 GeV"]["boundary sqrt(v M_Pl) + generic DM"] > 10
    assert s["SM m_t prior width 2 GeV"]["boundary, trials-corrected (8 candidate scales)"] < 1
    assert all(r["completion B"] < 0.2 for r in s.values())


def test_alp_triplet_deltaRV():
    assert all(r["shortfall"] > 100 for r in D["mev_alp"]["rows"].values())
    assert 1800 < D["long_lived_triplet"]["lightest_T_limit"] < 2000
    d = D["delta_RV"]
    assert 1.0 < d["gap_sigma"] < 1.6 and d["shift_over_unc"] > 5
