"""Pass 12679: minimiser stabiliser fidelity closed form, census 600, trivial codes."""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_stabiliser_fidelity_closed_form():
    d = load("w33_f8_minimiser_magic_and_codes.json")
    F = float(d["fidelity_40_digits"])
    assert abs(F - (3 + math.sqrt(3)) * math.cos(math.pi / 18) ** 2 / 9) < 1e-14
    assert abs(float(d["closed_form_diff"])) < 1e-25 and d["logical_stabiliser_fidelity"][0]["count"] == d["n_minimisers"]


def test_codes_trivial():
    c = load("w33_f8_minimiser_magic_and_codes.json")["codes"]
    assert (c["T"]["k"], c["T"]["d"]) == (3, 1) and all(c[t]["d"] == 1 for t in "ABC")


def test_census_600():
    d = load("w33_f8_global_minimiser_stabilisers_600.json")
    assert d["n_at_c8"] == 48 and d["stabiliser_orders"] == {"4": 48} and not d["any_covered"]
    assert d["weight_hist_types"] == {"[(0, 156), (1, 63), (2, 36)]": 24, "[(0, 138), (1, 99), (2, 18)]": 24}
