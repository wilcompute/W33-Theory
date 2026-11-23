"""Pass 12730."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12730_round.json")))
Q = json.load(open(os.path.join(ROOT, "data", "explore_pass12730_alloc_qat.json")))


def test_orbifold_window():
    m = D["orbifold_mapping"]
    assert 6 < m["cancel_at"] < 7.5 and m["window_0p1"][0] < 9.8 < m["window_0p1"][1]


def test_neff_correction():
    assert D["neff"]["delta_neff_edge"] > -0.1


def test_prior_art():
    p = D["prior_art"]
    assert p["A"] and len(p["hybrid"]) >= 3 and p["B_prime"]


def test_alloc_qat_ran():
    assert Q["uniform_ternary_1p6"] > Q["fp32_ref"] and Q["layer0_2bit_layer1_binary_1p5"] > Q["fp32_ref"]
