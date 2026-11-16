"""Pass 12682: orbit minima identification, orbit-A symmetry, symmetric degree-8 SOS validation on T."""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))
C8 = 2.4985086466880784


def test_orbit_levels():
    d = {r["orbit"]: r for r in load("w33_f8_orbit_levels_identify.json")}
    g = 2 * math.cos(2 * math.pi / 9)
    assert abs(float(d[15]["value"]) - (87 - 16 * g - 16 * g * g) / 9) < 1e-14
    assert d[2]["findpoly"] == d[12]["findpoly"] == "[-13, 265, -1447, 2243]"
    assert all(abs(float(d[k]["value"]) - v) < 1e-12 for k, v in ((8, 3), (13, 3), (16, 7)))


def test_orbitA_symmetry():
    d = load("w33_f8_orbitA_symmetry.json")
    assert d["order"] == 504 and d["matches_SL28_profile"] and d["distinct_left"] == d["distinct_right"] == 504
    sizes = sorted(s for s, w in d["effective_orbits"])
    assert sizes == [1, 28, 28, 36, 36, 63, 63]


def test_symmetric_sos8_validates_on_T():
    d = load("w33_f8_symmetric_sos8_T.json")
    assert d["block_invariance_residual"] < 1e-10 and d["identity_error"] < 1e-6
    assert abs(d["bound"] - C8) < 1e-6


def test_certainty_purity_rank2():
    d = load("w33_f8_certainty_purity_boundary.json")
    assert abs(d["threshold_purity"] - 0.5) < 1e-4
    near = [r for r in d["grid"] if 0.5 < r["purity"] < 0.56]
    assert all(abs(r["min_C"] - (6 * r["purity"] - 3)) < 1e-3 for r in near)
    assert any(r["min_C"] < 6 * r["purity"] - 3 - 0.01 for r in d["grid"] if r["purity"] > 0.6)


def test_orbitA_degree8_estimate_recorded():
    d = load("w33_f8_symmetric_sos8_A.json")
    assert d["group_order"] == 504 and d["block_invariance_residual"] < 1e-10
    assert 2.40 < d["bound"] < 2.4986 and d["identity_error"] < 1e-4
