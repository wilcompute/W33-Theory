"""Pass 12718."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12718_round.json"), encoding="utf-8"))
F = json.load(open(os.path.join(ROOT, "data", "explore_pass12718_flash.json")))


def test_transformer():
    t = D["transformer"]["rows"]
    assert t["fp32"]["acc"] > 0.95 and t["ternary"]["acc"] > 0.95 and t["ternary"]["zero_frac"] > 0.35


def test_squark_threshold():
    s = {r["X"]: r for r in D["squark_threshold"]}
    assert abs(s[0.0]["y"] - 0.472) < 0.002 and s[6.0]["y"] < s[2.0]["y"] < s[0.0]["y"]


def test_z10():
    z = D["z10"]
    assert z["n_good"] == 24 and z["n_decay"] == 120 and z["n_quality"] == 640
    assert all(e["harm"] >= 11 and e["decay_ok"] and e["anomaly_free"] for e in z["examples"])


def test_flash():
    best = [r["best_q"] for r in F]
    assert best[0] == 8 and 3 in best and best[-1] == 2
    assert best == sorted(best, reverse=True)
