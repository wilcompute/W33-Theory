"""Pass 12650 checks (read committed JSON)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_five_qubit_size9_verified():
    v = load("w33_five_qubit_size9_verify.json")
    assert v["maximal"] and v["pairwise_disjoint"] and v["graphs_isotropic"] and v["size"] == 9 and v["nonsingular_T_checked"] == 13888
    ls = load("w33_five_qubit_local_search.json")
    assert ls["control_n4_size5"]["found"] and not ls["n5_size8"]["found"]
def test_greedy_sizes():
    g = load("w33_rank_code_greedy_sizes.json")
    assert g["n4_random"]["smallest"] == 5 and g["n5_biased"]["smallest"] == 9
def test_kappa_hierarchy_and_alternating():
    h = load("w33_kappa_hierarchy.json")
    assert h[0]["const"] == 4 and h[0]["margin"] > 0.5 and all(r["margin"] < -1 for r in h[1:])
    a = load("w33_kappa_alternating.json")
    assert abs(a["max"] - 3) < 1e-9 and a["min_local"] > 2.9999
def test_genuine_optimum_highprec():
    r = load("w33_genuine_optimum_highprec.json")
    assert r["f_star"].startswith("0.05236256075668473370458114670007") and r["identification"] is None and r["higher_degree_search"]["found"] is None
