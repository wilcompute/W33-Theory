"""Pass 12694."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12694_round.json")))


def test_third_gen_pq_safe():
    t = D["third_generation_PQ"]
    assert t["BR_K_pi_a"] < 1e-12 and t["BR_B_K_a"] < 1e-10


def test_tags_deuterium_coincidence():
    assert 0.3 < D["soft_lepton_tags"]["fraction"] < 0.4
    assert abs(D["deuterium_rates"]["PArthENoPE (Pisanti+2021)"]["pull"]) < 0.5
    assert 0.2 < D["km3net_coincidence"]["rows"]["2.4"]["P_at_least_one"] < 0.35


def test_helium_mixture_and_wmass():
    assert all(2.75 < m["Neff"] < 2.95 for m in D["helium_mixture"].values())
    w = D["W_mass"]
    assert abs(w["without CDF"]["pull_vs_SM"]) < 1.5 and w["CDF_pull_vs_rest"] > 5
