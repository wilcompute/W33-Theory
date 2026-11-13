"""Pass 12649 checks (read committed JSON)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_rank_codes_reproduce_counts_and_five_qubit_bound():
    r = load("w33_symmetric_rank_code_spreads.json")
    assert r["n3"]["k3_size5"]["sets_through_pair"] == 56 and r["n4"]["k3_size5"]["sets_through_pair"] == 896
    assert all(not r["n5"]["k%d_size%d" % (k, k + 2)]["exists"] for k in (1, 2, 3))
    s6 = load("w33_five_qubit_size6.json")
    assert s6["control_n3_size5"]["sets_through_pair"] == 56 and not s6["control_n3_size6"]["exists"] and not s6["n5_size6"]["exists"]
def test_genuine_optimum_isolated():
    h = load("w33_optimum_hessian_nullity.json")
    assert h["three_qubit_control"]["nullity"] >= 1 and h["four_qubit_genuine"]["nullity"] == 0 and h["pentad"]["nullity"] == 0
def test_analytic_reduction_hypotheses():
    a = load("w33_threequbit_analytic_one_eighth.json")
    assert a["lemmaA_bijection"] and a["lemmaB_six_pairs"] and abs(a["kappa_numeric"] - 3) < 1e-8
    p = load("w33_threequbit_conditioning_profile.json")["profile"]
    assert all(abs(row["total"] - (6 - 2 * row["t_achieved"] ** 2)) < 1e-6 for row in p)
    k = load("w33_kappa_structure.json")
    assert sorted(sum(r) - 1 for r in k["commutation_matrix"][1:]) == [3, 3, 3, 3, 3]  # I + two commuting neighbours (pentagon)
def test_five_qubit_no_size7():
    r = load("w33_five_qubit_size7.json")
    assert r["n5_size7"]["status"] == "none" and r["control_n3_size5"]["status"] == "exists" and r["control_n3_size7"]["status"] == "none"
def test_kappa_degree_raised_infeasible_with_control():
    r = load("w33_kappa_symmetric_extension.json")
    assert r["const4_plain"]["margin"] > 0.5 and r["const3_plain"]["margin"] < -1 and r["const3_pt"]["margin"] < -1
