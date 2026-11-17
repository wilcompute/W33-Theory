"""Pass 12687: 3-loop QCD closes the offset; SMASH reheating; VLQ spectrum; dark radiation; combined likelihood."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12687_intermediate_scale_round3.json")))


def test_three_loop_qcd_closes_offset():
    for r in D["three_loop_qcd"]:
        assert abs(r["off2"] + 0.00105) < 0.0001 and abs(r["off3"]) < 0.0002


def test_smash_reheating_ns():
    for r in D["smash_reheating"]:
        assert 55 < r["N_star"] < 57 and r["pull_ns"] < -2.5


def test_vectorlike_spectrum_and_dark_radiation():
    rows = D["vectorlike_spectrum"]["rows"]
    assert not rows[0]["above_singlet_limit_1p49"] and rows[1]["above_doublet_limit_1p6"]
    dr = D["dark_radiation"]["rows"]
    assert abs(dr["SM plasma at decoupling (g_s = 106.75)"]["dNeff"] - 0.22) < 0.005
    assert dr["SM plasma at decoupling (g_s = 106.75)"]["pull"] > 3


def test_combined_ranking():
    m = D["combined_likelihood"]["models"]
    assert m["boundary lambda(sqrt(v M_Pl)) = 0"]["dAIC_vs_SM"] < 0.1
    assert m["dark dimension, no new states"]["dAIC_vs_SM"] > m["full SMASH (f_a boundary + its inflation)"]["dAIC_vs_SM"] > 5
