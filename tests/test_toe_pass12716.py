"""Pass 12716."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12716_round.json"), encoding="utf-8"))


def test_gift():
    g = D["gift_count"]
    assert sum(g["uneaten"].values()) == 18 and set(g["uneaten"]) == {"(3,1)+0.667", "(3,1)-0.667", "(3,2)+0.167", "(3,2)-0.167"}


def test_protection():
    p = D["protection"]["rows"]
    assert p["S1|H1|nonR"]["best"] <= 5 and p["S1|H5|nonR"]["best"] >= 11 and p["S1|H5|nonR"]["N"] == 10
    assert D["protection"]["reaching_11"] == ["S1|H5|nonR", "S2|H5|nonR"]


def test_unification():
    u = {(round(r["lambda_"], 2), r["M_cut"]): r for r in D["unification"]["rows"]}
    assert u[(1.0, 2.435e18)]["delta"] > 1.0 and abs(u[(4.0, 1e17)]["delta"] - 0.26) < 0.05


def test_odds():
    o = D["odds"]
    assert all((r["BF_hybrid"] > 30) if r["truth"] == "hybrid" else (r["BF_Bprime"] > 30) for r in o)


def test_hamming():
    h = {(r["snr"], r["code"][:3]): r for r in D["hamming"]}
    assert h[(10.0, "bin")]["p_block"] < 1e-8 < h[(10.0, "ter")]["p_block"]
    assert h[(10.0, "ter")]["info_bits_per_cell"] / h[(10.0, "bin")]["info_bits_per_cell"] > 1.6
