"""Pass 12731."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12731_round.json")))


def test_two_loop_orbifold():
    t = D["two_loop_orbifold"]
    assert abs(t["reference"][1] - 0.26) < 0.02
    r = {x["Lambda_R"]: x for x in t["rows"]}
    assert r[10]["delta"] <= 0.101 and r[40]["delta"] < r[10]["delta"] and r[40]["M12"] > r[3]["M12"]


def test_higgsino_not_inelastic():
    assert not any(x["inelastic"] for x in D["higgsino"]["rows"])


def test_notes_exist():
    assert os.path.exists(os.path.join(ROOT, "analysis", "NOTE_DRAFT_quartic_zero_floor_and_Bprime.md"))
    assert D["pq_relaxation"]["amplitude_ratio"] > 1e6
