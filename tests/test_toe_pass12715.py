"""Pass 12715."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12715_round.json"), encoding="utf-8"))


def test_superpotential():
    s = D["superpotential"]
    assert s["zero_modes"] == 30 and s["quality_min_dim"] == 11
    y = {round(float(k), 3): v for k, v in s["Y_content"].items()}
    assert y == {0.167: 12, 0.667: 6, 0.833: 12}
    l = s["lifting"]
    assert 8 < l[1]["median_lifted"] / l[0]["median_lifted"] < 12          # linear in eps


def test_plane():
    p = D["plane"]
    assert all(r["gap"] > 0 for r in p) and p[-1]["gap"] > p[0]["gap"]


def test_multiplier():
    m = D["multiplier"]
    assert m["verified"] and m["levels_max"] <= 6 and m["binary_wallace_levels"] == 8


def test_energy():
    e = D["energy"]
    assert 0.07 < e["crossover_pJ_per_bit"] < 0.08
    assert e["fronts"]["0.02"]["ternary_share"] > e["fronts"]["30.0"]["ternary_share"]
