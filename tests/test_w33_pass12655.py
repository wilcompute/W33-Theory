"""Pass 12655: uniqueness of the E6 sign class, non-split 2^6.W(E6), charge ranks, k-copy hierarchy."""
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def _signs():
    c = json.load(open(os.path.join(ROOT, "artifacts", "canonical_su3_gauge_and_cubic.json"), encoding="utf-8"))
    return {tuple(sorted(map(int, r["triple"]))): (1 if int(r["sign"]) % 3 == 1 else -1) for r in c["solution"]["d_triples"]}


def test_adjoint_identity_holds_numerically_and_fails_for_all_plus():
    # independent of the F2 extraction: check (x#)# = N(x) x at random real x
    for sg, expect in ((_signs(), True), ({t: 1 for t in _signs()}, False)):
        T = np.zeros((27, 27, 27))
        for (i, j, k), s in sg.items():
            for p in set(itertools.permutations((i, j, k))):
                T[p] = s / 6.0
        rng = np.random.default_rng(0); x = rng.standard_normal(27)
        sharp = lambda y: 3 * np.einsum("ijk,j,k->i", T, y, y)
        N = np.einsum("ijk,i,j,k->", T, x, x, x)
        assert np.allclose(sharp(sharp(x)), N * x, atol=1e-9) == expect


def test_sign_class_unique():
    d = load("w33_e6_cubic_sign_uniqueness.json")
    assert d["nonlinear_equations"] == 0 and d["n_equations"] == 2295 and d["consistent"]
    assert d["solution_space_dim"] == d["coboundary_dim"] == 21 and d["sign_classes_total_log2"] == 24
    assert d["repo_signs_satisfy"] and not d["all_plus_satisfies"] and not d["single_sign_flip_satisfies"]
    assert d["random_coboundary_shift_stabiliser_dim"] == 78 and d["single_sign_flip_stabiliser_dim"] < 78


def test_monomial_group_nonsplit():
    d = load("w33_e6_cubic_integral_structure.json")
    assert d["diagonal_sign_kernel_dim"] == 6 and d["n_permutations_with_sign_lift"] == 51840 and d["monomial_group_order"] == 3317760
    assert d["involutions"] == d["involutions_with_order2_lift"] == 891
    s = load("w33_e6_cubic_weyl_splitting.json")
    assert s["involutive_lifts_per_simple_reflection"] == [32] * 6 and s["n_splittings_for_this_simple_system"] == 0 and not s["splits"]


def test_charge_rank_table():
    d = load("w33_e6_cubic_integral_structure.json")["charge_rank_table"]
    for r in d:
        if r["meeting_pairs"] == 0: assert r["rank"] == 1
        if r["is_triad"]: assert r["rank"] == 3 and abs(r["N"]) == 1 and r["count"] == 180
        if 0 < r["meeting_pairs"] and not r["is_triad"]: assert r["rank"] == 2


def test_kcopy_hierarchy_valid_but_slow():
    d = load("w33_kcopy_symmetric_bound.json")
    by = {(c["name"], c["k"]): c["B"] for c in d["cases"]}
    assert abs(by[("three-qubit five-set", 2)] - 12) < 1e-6 and by[("three-qubit five-set", 5)] > 7.4
    assert abs(by[("five-qubit 9-set", 2)] - 40) < 1e-5 and 39 < by[("five-qubit 9-set", 3)] < 39.1
    for c in d["cases"]:
        assert c["B"] >= c["truth"] - 1e-5
