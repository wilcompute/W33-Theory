"""Pass 12651 checks (read committed JSON)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_pentagon_model_matches_data():
    r = load("w33_kappa_pentagon_model.json")
    assert r["model_degrees"] == r["data_degrees"] and abs(r["kappa_model"] - 3) < 1e-9 and abs(r["kappa_data"] - 3) < 1e-9
def test_five_qubit_size9_min_F():
    r = load("w33_five_qubit_size9_minF.json")
    assert r["n_covered"] == 279 and abs(r["min_F_times_32"] - 1) < 1e-7
def test_size8_not_found_and_six_qubit_greedy():
    a = load("w33_five_qubit_size8_anneal2.json")
    assert a["control_size9"]["found"] and not a["size8"]["found"]
    s = load("w33_six_qubit_greedy.json")
    assert s["n6_biased"]["smallest"] == 9
def test_six_qubit_size9_verified():
    v = load("w33_six_qubit_size9_verify.json")
    assert v["maximal"] and v["pairwise"] and v["all_nonsingular"] and v["size"] == 9 and v["nonsingular_T_checked"] == 888832
