"""Pass 12677: uniform torus levels, E8/2E8 structure of type C, qutrit side, certificate fails above c8."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_torus_levels_uniform():
    for q, poly0 in ((4, ["1", "-30", "145"]), (16, ["1", "-2040", "1768476"])):
        d = load(f"w33_q{q}_torus_level_eigenspace_newton.json")
        assert d["smallest_conjugate"] and d["minimal_polynomial_of_Ntau"][:3] == poly0[:3]
        assert float(d["max_dist_to_int"]) < 1e-25
    assert load("w33_q32_torus_level_identify.json")["tau_is_smallest_conjugate"]


def test_type_C_is_E8_mod_2():
    c = load("w33_f8_typeC_quadric.json")
    hyp = [f for f in c["invariant_forms"] if f["singular"] == 135]
    assert len(hyp) == 1
    sw = hyp[0]["singular_by_weight"]
    assert sw["0"] == {"0": 45, "1": 120} and sw["1"] == {"0": 54} and sw["2"] == {"0": 27} and sw["3"] == {"0": 9}
    for t in ("A", "B"):
        d = load(f"w33_f8_type{t}_quadric.json")
        h = [f for f in d["invariant_forms"] if f["singular"] == 135][0]["singular_by_weight"]
        assert any(len(v) == 2 for k, v in h.items() if k != "0")     # mixed: not clean


def test_qutrit_side():
    d = load("w33_qutrit_E6a1_eigenstates.json")
    assert d["order9_in_PSp43"] == 5760 == d["E6a1_class_size"]
    fids = {round(r["fidelity"], 6): r["count"] for r in d["stabiliser_fidelities"]}
    assert fids == {0.392454: 324, 0.444444: 162, 1.0: 27}


def test_certificate_fails_above_c8():
    d = load("w33_f8_codespace_deg8_certificate_2498509_1000000.json")
    assert not d["certified"] and d["scs_margin"] < 0
