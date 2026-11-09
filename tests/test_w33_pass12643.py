"""Pass 12643 checks (read committed JSON; regenerate with the analysis scripts)."""
import json, os
import sympy as sp
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_mirror_orbits():
    r = load("w33_mirror_orbits.json")
    assert r["two_qutrits"] == dict(orbit_sizes=[216, 216], fibres=216, partners_in_same_orbit=0)
    assert r["three_qubits"] == dict(orbit_sizes=[24192], fibres=12096, partners_in_same_orbit=12096)
def test_threequbit_mirror_witness():
    r = load("w33_threequbit_witness_closed_form.json")
    assert r["meeting_patterns"] == {"(1, 1, 1, 1, 3)": 120960} and r["witness_values"] == {"9/16": 120960}
    m = load("w33_threequbit_mirror_pairs.json")["three_qubit_size5"]
    assert m["fibre_sizes"] == {"2": 12096} and m["pair_overlaps_in_a_fibre"] == {"15": 1} and abs(m["max_witness"] - 9 / 16) < 1e-8
def test_lovasz_bounds():
    r = load("w33_lovasz_theta_unextendible.json")
    c, t = r["p2_n2_size3"], r["p2_n3_size5"]
    assert c["alpha"] == 2 and abs(c["theta"] - 2) < 1e-6
    assert t["alpha"] == 6 and abs(t["theta"] - (4 + 5 ** 0.5)) < 1e-6 and t["anticommutation_degrees"] == [12]
def test_hoffman_constant_exact():
    # lambda_min = -4 cos(pi/9) is a root of x^3 - 12x + 8; the constant is positive
    c = sp.cos(sp.pi / 9)
    assert sp.simplify(sp.expand_trig((-4 * c) ** 3 - 12 * (-4 * c) + 8).rewrite(sp.cos)).evalf() < 1e-12
    H = 28 * c / (3 + c); bound = (7 - H) / 8
    assert abs(float(bound) - 21 * (1 - float(c)) / (8 * (3 + float(c)))) < 1e-14 and float(H) < 7
def test_min_F_rungs():
    r = load("w33_minF_covered_points.json")
    assert abs(r["control_p3_n2_size5"]["min_F"] - 0.14711376) < 1e-6
    assert abs(r["d25_m2_cover0"]["min_F"] - 4 / 25) < 1e-6

def test_theta_exact_dual():
    r = load("w33_theta_coherent_closure.json")
    assert r["theta_upper_exact"] == "4+sqrt(5)" and r["vertex_class_sizes"] and sorted(r["vertex_class_sizes"]) == [1, 12, 15]
    assert sum(int(m) * (2 if "lam**2" in f else 1) for f, m in r["exact_charpoly_factors"]) == 28
