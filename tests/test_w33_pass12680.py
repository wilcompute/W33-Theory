"""Pass 12680: order-4 orbit classification; magic vs certainty across torus eigenstates."""
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_orbit_classification():
    d = load("w33_f8_order4_orbit_classification.json")
    assert d["n_groups"] == 893088 and d["n_orbits"] == 17
    t = collections.Counter(r["type"] for r in d["orbits"])
    assert t["A"] == 1 and t["B"] == 5 and t["C"] == 2
    hit = [r for r in d["orbits"] if r["minimiser_stabilisers_in_orbit"] > 0]
    assert sorted((r["type"], r["size"]) for r in hit) == [("A", 1512), ("B", 42336)]


def test_magic_constant_on_primitive_orbit():
    d = load("w33_f8_torus_eigenstate_magic.json")
    prim = {round(e["fidelity"], 8) for r in ("1", "2", "4", "5", "7", "8") for e in d[r]}
    assert prim == {0.50992911}
    assert {round(e["fidelity"], 8) for r in ("3", "6") for e in d[r]} == {0.49056261}
