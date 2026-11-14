"""Pass 12662: q = 32 stabiliser value 11, c_32 from stabiliser starts, torus-orbit negative."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_annealing_seeds_agree_with_conjecture():
    d = load("w33_regulus_odd_k_structure.json")
    assert [r["best"] for r in d["q8"]["runs"]] == [3, 3]
    assert [r["best"] for r in d["q32"]["runs"]] == [11, 11, 11]
    for q in (8, 32):
        r = d[f"q{q}"]
        assert r["best"] == r["conjectured"] == (q + 1) // 3 == r["check_count"] == r["covered_points"]
        assert r["points_per_hit_line"] == [1] * r["best"] and r["n_hit_lines"] == r["best"]
    assert d["q32"]["pgl_elements_checked"] == 32736 and not d["q32"]["hit_lines_are_cyclic_orbit_of_order_r"]


def test_character_sum_bookkeeping():
    d = load("w33_regulus_odd_k_structure.json")
    for q in (8, 32):
        cs = {int(k): v for k, v in d[f"q{q}"]["char_sums"].items()}
        assert sum(cs.values()) == q
        assert sum(k * v for k, v in cs.items()) // q - 1 == (q + 1) // 3
        assert cs[q * q] == 1


def test_c32_from_stabiliser_starts():
    d = load("w33_regulus_c32_from_stabiliser.json")
    assert abs(d["q8"]["dF_of_stabiliser_state"] - 3) < 1e-8 and abs(d["q8"]["best_c"] - 2.498508646688) < 1e-7
    assert sum(1 for r in d["q8"]["runs"] if abs(r["c"] - 2.498508646688) < 1e-6) >= 15
    q32 = d["q32"]
    assert abs(q32["dF_of_stabiliser_state"] - 11) < 1e-8 and q32["stabiliser_is_local_minimum"]
    assert len(q32["runs"]) == 11 and all(abs(r["c"] - 11) < 1e-6 for r in q32["runs"])
