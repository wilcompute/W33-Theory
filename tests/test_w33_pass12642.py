"""Pass 12642 certificate checks (reads committed JSON; regenerate with the analysis scripts)."""
import json, os
from fractions import Fraction
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_chirality_witness_closed_form():
    r = load("w33_chirality_third_moment.json")
    assert r["order2_difference_norm"] < 1e-12
    assert Fraction(r["closed_form"]) == Fraction(16, 27)
    assert abs(r["max_Delta_pure"] - 16 / 27) < 1e-8 and abs(r["min_Delta_pure"] + 16 / 27) < 1e-8
    assert r["same_covered_points"] and r["shared_collinear_pairs"] == 0 and r["collinear_pairs_L"] == 30
    assert all(m == [0, 1, 1, 1, 1] for m in r["left_line_meets_right_lines"])
def test_threequbit_degree6_tight():
    r = load("w33_threequbit_degree6.json")
    c, t = r["control_d4_size3"], r["d8_size5"]
    assert abs(c["delta"] - 0.25) < 1e-6 and abs(t["delta"] - 0.125) < 1e-6
    assert abs(t["numeric_min_F"] - 0.125) < 1e-6 and t["identity_max_rel_residual"] < 1e-8
    assert min(t["eig_min_G"], t["eig_min_H"]) > -1e-5
def test_size5_single_type():
    r = load("w33_threequbit_size5_orbits.json")
    assert r["n_size5"] == 24192 and r["n_types"] == 1 and 1451520 // r["n_size5"] == 60
