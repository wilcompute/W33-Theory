"""Pass 12645 checks (read committed JSON)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_four_qubit_exact_one_sixteenth():
    r = load("w33_four_qubit_facial_reduction.json")
    assert r["certified"] and r["n_alpha_sets"] == 3 and r["n_equations"] == 318 and r["rank"] == 315
    last = r["attempts"][-1]
    assert last["equations_exact"] and last["exact_psd"] and r["denominator"] == 4
def test_no_mirror_partner_at_four_qubits():
    r = load("w33_four_qubit_mirror_partners.json")
    assert r["n_inside"] == 17 and r["n_partitions"] == 1 and r["partners"] == []
def test_optimisers_have_no_weyl_symmetry():
    r = load("w33_d25_optimiser_structure.json")
    assert r["pentad"]["stabiliser_size"] == 0 and r["d25_single_cover"]["stabiliser_size"] == 0
    assert r["d25_single_cover"]["covered_profile"]["0.166667"] == 48 and r["d25_single_cover"]["uncovered_profile"]["0.166667"] == 96
