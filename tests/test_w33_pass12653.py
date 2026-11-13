"""Pass 12653: kappa <= 3 on all 448 supports, negative LP / conditioning routes, five-qubit lift points, size-7 search re-check."""
import itertools
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_448_supports_three_orbits_and_kappa():
    d = load("w33_kappa_448_supports.json")
    assert d["n_supports"] == 448 and d["orbit_sizes"] == [16, 192, 240]
    by = {o["size"]: o for o in d["orbits"]}
    assert abs(by[192]["kappa"] - 3) < 1e-8 and by[192]["contains_model"] and by[192]["choi_pt_min_eig"] > -1e-9
    assert abs(by[240]["kappa"] - 3) < 1e-8 and by[240]["choi_pt_min_eig"] < -1
    assert abs(by[16]["kappa"] - 2) < 1e-8
    for f in d["y_t_family"]:
        assert f["identity_holds"] and f["spectrum"] == [1.0, 1.0, 1.0, 3.0]
    assert abs([f for f in d["y_t_family"] if f["t"] == 2.0][0]["XX_on_y"] + 0.6) < 1e-12


def test_support_count_independent():
    # independent recount: 6-subsets of F_2^4 whose 15 pairwise sums are distinct (hence all non-zero vectors)
    n = sum(1 for S in itertools.combinations(range(16), 6) if len({a ^ b for a, b in itertools.combinations(S, 2)}) == 15)
    assert n == 448


def test_selfdual_lp_is_trivial_but_valid():
    d = load("w33_selfdual_pauli_lp.json")
    for c in d["cases"]:
        dd = 1 << c["n"]
        assert c["LP"] >= c["truth_SigmaU_max"] - 1e-6
        assert abs(min(c["LP"], c["LP_with_clique_cuts"]) - (dd - 1)) < 1e-6  # trivial bound d - 1


def test_conditioning_route_only_works_at_three_qubits():
    d = load("w33_five_qubit_conditioning_scan.json")
    assert abs(d["control_n3_best"]["route_bound"] - 6) < 1e-6
    assert len(d["n5_rows"]) >= 40 and d["n5_best_route_bound"] > 44.9
    d4 = load("w33_four_qubit_conditioning_scan.json")
    assert abs(d4["A"]["best"]["route_bound"] - 21) < 1e-6 and abs(d4["B"]["best"]["route_bound"] - 21) < 1e-6


def test_five_qubit_set_has_no_lift_point():
    d = load("w33_five_qubit_lift_points.json")
    assert d["control_typeA_typeB"] == [0, 120]
    assert d["n_uncovered"] == 744 and d["disjoint_image_points"] == 0 and d["lift_points"] == 0


def test_new_search_reproduces_size7_none():
    d = load("w33_five_qubit_size7_dlx.json")
    assert d["control_n3_size5"]["status"] == "exists" and d["control_n3_size7"]["status"] == "none"
    assert d["control_n5_size7"]["status"] == "none" and len(d["control_n5_size7"]["per_rep"]) == 8
