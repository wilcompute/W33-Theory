"""Pass 12719."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12719_round.json"), encoding="utf-8"))
TF = json.load(open(os.path.join(ROOT, "data", "explore_pass12719_transformer.json")))


def test_mediation():
    m = D["mediation"]["rows"]
    assert abs(m[0]["y"] - 0.472) < 0.002 and m[-1]["y"] < 0.44


def test_decay():
    r = {x["n"]: x for x in D["pgb_decay"]["rows"]}
    assert r[11]["regime"] == "prompt" and r[16]["regime"].startswith("R-hadron") and r[19]["regime"] == "BBN-excluded"


def test_dw_obstruction():
    assert D["dw"]["n"] == 0 and D["dw"]["with_singlet"]["n"] == 0


def test_qudit():
    q = {(x["model"], x["d"]): x for x in D["qudit"]["rows"]}
    assert q[("f = 1", 3)]["fail_per_bit"] < q[("f = 1", 2)]["fail_per_bit"]
    assert q[("f = d - 1", 3)]["fail_per_bit"] > q[("f = d - 1", 2)]["fail_per_bit"]
    assert q[("f = 1", 3)]["info_per_cost"] == max(x["info_per_cost"] for x in D["qudit"]["rows"])


def test_transformer_ran():
    rows = TF["rows"]
    assert set(rows) == {"fp32", "binary", "ternary", "2bit"} and rows["ternary"]["zero_frac"] > 0.3


W = json.load(open(os.path.join(ROOT, "data", "explore_pass12719_web.json")))


def test_web_topmass():
    r = W["top_mass"]["rows"]
    assert r[1]["mu0"] < r[0]["mu0"] and r[1]["y_Bprime"] - r[1]["y_hybrid"] > 0.03


def test_web_desi_radion():
    d = {x["w0"]: x for x in W["desi_radion"]["rows"]}
    assert d[-0.84]["ratio_to_LLR_2sigma"] > 30 and W["desi_radion"]["max_one_plus_w0"] < 0.01
