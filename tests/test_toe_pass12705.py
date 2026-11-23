"""Pass 12705."""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12705_round.json")))


def test_e6():
    e = D["e6_650_78"]
    assert e["dims"] == {"comm": 17, "78": 5, "650": 11}
    v = e["vacua"]
    assert all(r["n_QU_only"] == 0 for k, r in v.items() if k.startswith("650 alone"))
    assert all(r["n_QU_only"] > 0 and max(r["QU_unbroken_dims"]) <= 16 for k, r in v.items() if k.startswith("650+78"))
    seen = set().union(*[set(r["unbroken_dims"]) for r in v.values()])
    assert {46, 24, 22} <= seen


def test_so10_leftovers():
    rows = D["so10_vacuum_mass_matrix"]["rows"]
    assert all(r["extra"] > 0 for r in rows if r["QU_only"])
    assert any(r["QU_only"] and r["extra"] == 11 and r["color_roots"] == 6 for r in rows)
    u = D["octet_triplet_unification"]
    assert abs(u["reference_no_adjoint"][2] - 0.26) < 0.03
    r15 = next(r for r in u["rows"] if r["M_adj"] == 1e15); assert r15["delta"] > 1.0
    assert all(math.isnan(r["M12"]) for r in u["rows"] if r["M_adj"] <= 1e14)


def test_mfv():
    m = D["mfv_tree_splitting"]["scan"]
    assert m["control y_tau = 0"]["eta_max"] < 1e-12
    assert m["|c2| in [0.3, 3]"]["frac_ge_obs"] > 0.05 and m["|c2| in [0.1, 1]"]["frac_ge_obs"] > 0.03


def test_dark_graviton():
    g = D["dark_graviton_verified"]
    assert 0.52 < g["yprime_natural"][0] < 0.525 and g["yprime_natural"][1] < 0.535
