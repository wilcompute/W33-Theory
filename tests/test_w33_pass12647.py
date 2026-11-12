"""Pass 12647 checks (read committed JSON)."""
import json, os
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_pauli_reduced_sos_reaches_one_eighth():
    r = load("w33_threequbit_pauli_reduced_sos.json")
    assert r["sector0_K"] == 15 and r["sector0_G"] == 36 and abs(r["delta"] - 0.125) < 1e-7
def test_three_qubit_exact_to_1e6():
    r = load("w33_threequbit_epsilon_exact.json")
    certified = [x["eps"] for x in r["runs"] if x.get("certified")]
    assert "1/1000000" in certified
def test_census_refutes_mirror_theta_conjecture():
    g = load("w33_four_qubit_greedy_census.json")
    c = Counter((x["n_partitions"] > 1, x["theta_gt_alpha"]) for x in g["classes"])
    assert c[(False, True)] >= 1 and c[(True, False)] >= 1
    assert any(x["size"] == 8 for x in g["classes"])
def test_minimiser_variety_adds_no_kernel():
    v = load("w33_threequbit_minimiser_variety.json")
    assert v["q_span_rank_stabiliser"] == 20 and len(v["fixed_paulis"]) == 15
    p = load("w33_threequbit_kernel_projector.json")
    assert p["numerical_rank"] == 20
def test_size5_four_qubit_exact():
    r = load("w33_four_qubit_size5_exact.json")
    assert r["n_uncovered"] == 180 and any(a["exact_psd"] and a["target"] == "74/5" for a in r["attempts"])
