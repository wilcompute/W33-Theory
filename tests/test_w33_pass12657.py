"""Pass 12657: regulus MUB sets over F_q, type B = F_4 regulus, AG(2,4) identity, size-8 cross-check."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_regulus_sets_maximal_and_quadric():
    d = load("w33_regulus_mub_sets.json")
    for q, n_T, cov in ((2, 4, 9), (4, 448, 75), (8, 888832, 567)):
        r = d[f"q{q}"]
        assert r["size"] == q + 1 and r["maximal"] and r["extendible_T"] == 0
        assert r["n_nonsingular_T"] == n_T and r["covered"] == cov and r["covered_equals_quadric"]
    assert (d["q4"]["lagrangians_inside_C"], d["q4"]["partitions_of_C"]) == (10, 2)
    assert [10, 2] in [list(t) for t in d["q4"]["census_types_(n_inside,n_partitions)"]]
    assert all(v < 1e-10 for v in d["IC_formula_max_residual"].values())
    assert abs(d["q4_min_F_CZ_model"] - 1 / 16) < 1e-6


def test_affine_plane_identity_and_minimum():
    d = load("w33_typeB_affine_plane_inequality.json")
    assert d["n_lines"] == 20 and d["identity_residual"] < 1e-12
    assert abs(d["min_LHS"] - 0.375) < 1e-6 and d["min_LHS"] > 0.375 - 1e-7
    assert abs(d["basis_state_LHS"] - 1.25) < 1e-12 and abs(d["uniform_real_LHS"] - 1.25) < 1e-12


def test_decomposable_level_is_trivial():
    d = load("w33_typeB_decomposable_certificate.json")
    assert abs(d["control_norm_squared"]["delta"] - 1) < 1e-4
    assert abs(d["typeB"]["delta"] - 5 / 16) < 1e-4 and not d["proves_three_eighths_numerically"]


def test_size8_reverse_crosscheck():
    d = load("w33_five_qubit_size8_dlx_reverse.json")["n5_size8"]
    assert d["status"] == "none" and [r["s2"] for r in d["per_rep"]] == [692, 694]
    assert not any(r["timeout"] for r in d["per_rep"]) and d["nodes"] == 107943913
    full = load("w33_five_qubit_size8_dlx_full.json")["n5_size8"]
    assert {r["s2"]: r["nodes"] for r in full["per_rep"]}[692] != d["per_rep"][0]["nodes"]
