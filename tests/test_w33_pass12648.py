"""Pass 12648 checks (read committed JSON)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_smallest_four_qubit_size_is_five():
    r = load("w33_exhaustive_small_maximal_spreads.json")
    assert r["two_qubits"]["k3"]["exists"]
    assert not r["three_qubits"]["k3"]["exists"] and not r["three_qubits"]["k4"]["exists"]
    assert r["three_qubits"]["k5"]["count_containing_fixed_pair"] == 24192 * 20 // (135 * 64)
    assert not r["four_qubits"]["k3"]["exists"] and not r["four_qubits"]["k4"]["exists"]
def test_size5_census_two_types_and_lift():
    c = load("w33_four_qubit_size5_census.json")
    assert c["sets_through_pair"] == 896 and c["N5"] == 105283584 and c["n_types"] == 2
    lift = {r["n_partitions"]: r["lift_points"] for r in load("w33_four_qubit_type_lift.json")}
    assert lift[1] == 0 and lift[2] == 120
def test_type_a_optimum_unidentified():
    r = load("w33_four_qubit_size5_optimum.json")
    assert abs(r["min_F"] - 0.0523625607566847) < 1e-12 and "identification_rejected" in r
def test_pentad_degree6_not_tight():
    r = load("w33_pentad_degree6_sos.json")["pentad_degree6"]
    assert 1 / 9 + 0.02 < r["delta"] < 0.1471 - 0.005
