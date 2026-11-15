"""Pass 12672: quotient corollary (exact), effective three-qubit / norm-one-torus mechanism, saddle cubic, code-space bounds."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_both_quotients_exact():
    d = load("w33_f8_quotient_exact_corollary.json")
    assert d["parent_equals_closed_form"] and d["both_quotients_exact"]
    types = sorted(q["type"] for q in d["quotients"].values() if q.get("trace") != 0)
    assert types == [17, 27]
    for q in d["quotients"].values():
        if q.get("trace") != 0:
            assert q["quotient_covered"] == 279 and q["anticommuting_nonzero"] == 0 and q["stabilises"]


def test_effective_torus_orbit():
    d = load("w33_f8_effective_three_qubit.json")
    assert d["weights_hist"] == {"0": 27, "1": 18, "2": 9, "3": 9}
    M, cyc = d["intersections"], d["cycle"]
    pos = {b: i for i, b in enumerate(cyc)}
    for i in range(9):
        for j in range(9):
            step = min((pos[i] - pos[j]) % 9, (pos[j] - pos[i]) % 9)
            assert M[i][j] == {0: 7, 1: 3, 2: 1, 3: 0, 4: 0}[step]
    assert d["fixed_sigma"] == 0 and d["fixed_sigma3"] == 0


def test_saddle_cubic():
    import sympy as sp
    d = load("w33_f8_saddle_levels.json")
    r = d["refined"]
    assert r["findpoly"] == "[-13, 265, -1447, 2243]"
    c = sp.symbols("c"); P = 13 * c ** 3 - 265 * c ** 2 + 1447 * c - 2243
    assert sp.factorint(sp.discriminant(P, c)) == {2: 14, 37: 3}
    import mpmath as mp
    mp.mp.dps = 35
    assert abs(sp.N(P.subs(c, sp.Float(r["value"], 35)), 30)) < 1e-25
    for lev, v in d.items():
        if lev != "refined": assert v["full_gradient_norm"] < 1e-7   # symmetric criticality


def test_codespace_lower_bounds_are_below_c8():
    q = load("w33_f8_codespace_quillen_rank3.json")
    cks = [b["c_k"] for b in q["bounds"]]
    assert all(c <= q["c8"] for c in cks) and cks[-1] > 0.35
    s = load("w33_f8_codespace_sos_rank3.json")
    assert s["c_sos"] < s["c8"] and abs(s["c_sos"] - 1) < 1e-4


def test_galois_conjugates_are_exact_pure_critical_states():
    d = load("w33_f8_galois_conjugate_witnesses.json")
    assert d["all_exact"]
    assert [d[f"tau{n}"]["c"] for n in range(3)] == [["47/9", "-16/9", "0"], ["79/9", "0", "-16/9"], ["5/3", "16/9", "16/9"]]
    assert all(d[f"tau{n}"]["critical"] and d[f"tau{n}"]["idempotent"] for n in range(3))


def test_clifford_eigenstates_carry_the_galois_orbit():
    d = load("w33_f8_clifford_eigenstates.json")
    assert d["n_lifts"] == 64 and d["n_eigenvectors"] == 512 and d["lifts_fixing_witness"] == 1
    assert d["max_deviation_from_closed_forms"] < 1e-10
    assert all(v == 64 for v in d["counts_per_j"].values()) and len(d["counts_per_j"]) == 8
