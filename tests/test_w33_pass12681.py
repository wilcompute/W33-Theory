"""Pass 12681: c8 orbits = torus orbits; exact magic values; three-tangle not canonical."""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_c8_orbits_are_torus_orbits():
    per = load("w33_f8_order4_orbit_classification.json")["per_orbit"]
    assert len(per) == 17
    assert all(r["attains_c8"] == (r["torus_subgroups_in_orbit"] > 0) for r in per)
    assert sum(r["torus_subgroups_in_orbit"] for r in per) == 7 and sum(r["attains_c8"] for r in per) == 4
    assert all(r["minimiser_stabilisers"] == 0 or r["attains_c8"] for r in per)
    A = [r for r in per if r["type"] == "A"][0]
    assert A["stabiliser_order_in_H"] == 504


def test_magic_values_exact():
    d = load("w33_f8_torus_eigenstate_magic.json")["identification"]
    assert abs(float(d["3"]["value"]) - (9 + 5 * math.sqrt(3)) / 36) < 1e-13
    assert abs(float(d["4"]["value"]) - (3 + math.sqrt(3)) * math.cos(math.pi / 18) ** 2 / 9) < 1e-13


def test_tangle_not_canonical():
    d = load("w33_f8_hyperdet_control.json")
    assert d["local_invariant"] and d["n_distinct_under_clifford"] > 10
