"""Pass 12678: clean-quadric census, Galois critical values (q = 4), E7 rung, facial reduction at c8."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_clean_quadric_census():
    d = load("w33_f8_clean_quadric_census.json")
    prof = d["clean_profiles"]
    assert prof["C"] == {"[('hyperbolic', 1)]": prof["C"].get("[('hyperbolic', 1)]", 0)} and d["type_counts"]["C"] > 0
    import ast
    maxw = {"A": 2, "B": 2, "C": 3}
    for t, p in prof.items():
        has3 = (maxw[t] if t in maxw else max(w for w, _ in ast.literal_eval(t))) >= 3
        clean = any("hyperbolic" in k for k in p)
        assert clean == has3, t                     # clean form iff a coset of weight >= 3


def test_galois_critical_values_q4():
    d = load("w33_q4_torus_critical_values_galois.json")
    assert d["all_conjugates_critical"]


def test_E7_rung():
    d = load("w33_f8_E7_rung.json")
    assert d["sigma_orbits_bitangents"] == [1, 9, 9, 9] and d["sigma_orbits_even"] == [9, 9, 9, 9]
    assert d["even_forms_vanishing_on_basis"] == [8] * 9 and d["Sp62_stabiliser_order"] == 18


def test_facial_reduction_at_c8():
    d = load("w33_f8_facial_reduction.json")
    assert d["n_minimisers"] == 128 and d["kernel_total"] == 383 and d["kernel_hist"] == {"2": 191, "1": 1}
    assert d["status"] == "solved" and d["margin_at_c8"] > 0.1 and d["strictly_feasible_on_face"]
