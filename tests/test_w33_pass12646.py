"""Pass 12646 checks (read committed JSON)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_census_distinct_orbits_and_stabiliser_minima():
    c = load("w33_four_qubit_set_census.json")
    assert len(c) == 5 and len({r["n_inside"] for r in c}) == 5
    m = load("w33_four_qubit_minF_census.json")
    assert all(abs(r["numeric_min_F"] - r["m_star"] / 16) < 1e-7 for r in m)
    # mirror partner <=> theta > alpha (observed)
    assert all((r["n_partitions"] > 1) == (r["theta"] > 15 - r["m_star"] + 1e-3) for r in c)
def test_exact_certificates():
    for k, a, D in [(1, 13, 4096), (2, 14, 16), (4, 14, 8)]:
        r = load("w33_four_qubit_facial_reduction_census%d.json" % k)
        assert r["certified"] and r["alpha"] == a and r["denominator"] == D and r["attempts"][-1]["exact_psd"]
def test_two_copy_no_gain():
    r = load("w33_two_copy_lovasz.json")
    assert r["two_qubits_control"]["closure_dual_bound"] > 5.9
    assert r["three_qubits"]["sqrt_bound"] > 6.2
def test_sixth_level_is_partial_spread():
    r = load("w33_d25_sixth_level.json")
    assert r["n_points"] == 36 and r["whole_points"] and r["full_lines_inside"] == 6 and r["max_dev_from_one_sixth"] < 1e-7
