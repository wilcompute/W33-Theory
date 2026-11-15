"""Pass 12675: E6(a1) / tritangent structure of the F_8 code space; stabiliser types; local rigidity; q = 32 classes."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_torus_is_E6a1_on_E6_mod_2():
    d = load("w33_f8_torus_is_E6a1.json")
    assert d["phi9"] and d["fixed_points"] == 0 and d["orbit_sizes"] == [9] * 7
    assert len(d["invariant_forms"]) == 1 and d["invariant_forms"][0]["type"] == "elliptic" and d["invariant_forms"][0]["singular"] == 27
    assert d["invariant_forms"][0]["singular_points_per_Lagrangian"] == [3] * 9
    assert all(d["tritangent_per_basis"]) and d["weight_equals_incidence"] and d["zero_sum_singular_triples"] == 45
    assert d["tritangent_orbit_sizes"] == [3, 3, 3, 9, 9, 9, 9] and d["bases_form_one_orbit"]
    assert sorted(d["line_orbit_weights"]) == [[0], [1], [2]]


def test_stabiliser_types():
    d = load("w33_f8_stabiliser_types.json")
    assert d["T_subgroups"] == {"A": 1, "B": 5, "C": 1}
    assert all(abs(v - 2.4985086466880784) < 1e-8 for v in d["typeB_code_space_minima"].values())
    assert d["typeB_rank3_hits"] == 6 and d["typeB_rank3_subgroups"] == {"A": 1, "B": 5, "C": 1}
    c = load("w33_f8_codespace_effective_sos_C_deg6.json")
    assert abs(c["bound"] - 2.4966773) < 1e-6 and abs(c["effective_min"] - 2.4985086467) < 1e-8


def test_local_rigidity_generic_points():
    d = load("w33_f8_local_rigidity.json")
    for t in ("A", "B", "C"):
        for r in d[t]:
            assert r["negative_full"] == 0 and r["null_full"] in (3, 4) and r["null_code"] in (2, 3)
            if r["null_code"] == 3: assert r["null_full"] == 3     # generic points: rigid


def test_q32_four_classes():
    d = load("w33_regulus_torus_clifford_q32.json")
    assert len(d["runs"]) >= 4 and all(abs(r["best"] - 12.48962077) < 1e-6 for r in d["runs"])
