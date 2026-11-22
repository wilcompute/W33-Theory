"""Pass 12693."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12693_round.json")))


def test_post_bbn_entropy_excluded_by_deuterium():
    assert D["low_neff"]["post_BBN_entropy"]["2.86"]["pull"] > 5


def test_triplet_limit_and_fn():
    assert 1700 < D["vlq_effective_limit"]["M_VL_limit"] < 1780
    assert D["aligned_FN"]["both_ok"] == []


def test_proton_fraction_and_empress():
    assert D["proton_fraction"]["rows"]["KM3NeT-only 5.8e-8"]["f_p_strong_evolution"] > 1
    e = D["empress"]
    assert -2.4 < e["EMPRESS_vs_others_pull"] < -2.1 and -2.2 < e["combined_with_ACT"]["pull_vs_SM"] < -1.8
