"""Pass 12666: 4D central charge in antisymmetric three-qubit Paulis; criticality top mass vs ATLAS pole mass."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_4d_central_charge_dictionary():
    d = load("w33_4d_central_charge_pauli.json")
    assert d["n_antisymmetric_paulis"] == 28 and d["span_rank"] == 28
    assert abs(d["normal_form_I4_over_rho4"] - 1) < 1e-12
    for r in d["two_state"]:
        assert r["rank"] == 2 and abs(r["I4_over_r4"] - 1) < 1e-10 and r["pf"] < 1e-9
        assert r["reconstruct_err"] < 1e-12 and r["coeff_formula_err"] < 1e-12
    for r in d["five_to_four"]:
        assert r["rank"] == 2 and abs(r["I4"] - 1) < 1e-10
    assert d["generic_I4_signs"] == [-1, 1]
    for r in d["generic"]:
        assert r["rank"] == 8 and r["I4_im"] < 1e-9 and r["su8_invariance"] < 1e-8 * max(1.0, abs(r["I4"]))


def test_top_pole_comparison():
    d = json.load(open(os.path.join(ROOT, "analysis", "toe_uv", "top_pole_2025.json")))
    assert abs(d["Mt_for_lambda_MPl_zero"] - 171.04) < 0.01
    c = d["comparisons"]
    atlas = c["ATLAS pole mass, ttbar+1 jet, JHEP 12 (2025) 023"]
    assert atlas["value"] == 170.7 and abs(atlas["pull"]) < 0.5
    assert abs(c["direct_run1_combination (MC mass, PDG 2026 still cites it)"]["pull"] - 3.0) < 0.1
