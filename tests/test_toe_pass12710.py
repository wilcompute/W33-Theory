"""Pass 12710."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12710_round.json"), encoding="utf-8"))


def test_short_range_gap():
    rows = {round(r["lambda_nm"], 1): r for r in D["short_range"]["rows"]}
    assert rows[200.0]["gap_vs_8_3"] > 1e7 and rows[8.8]["gap_vs_8_3"] > 1e15


def test_mediator():
    m = D["mediator"]
    assert 0.02 < m["lambda_HY_max_for_FCC_sigma"] < 0.06
    r = [x for x in m["rows"] if x["M_Y"] == 2000.0 and x["lambda_HY"] == 0.1][0]
    assert r["shift_vs_noY"] > 0.02


def test_hybrid_evidence():
    h = D["hybrid_evidence"]["rows"]["width 15"]
    assert 0.5 < h["hybrid_symmetric"] < 1.0 and h["hybrid_tuned"] < 1e-20


def test_warped():
    w = {r["kL"]: r for r in D["warped"]["rows"]}
    assert abs(w[0.0]["y_UV"] - 0.505) < 0.002
    assert w[10.0]["y_UV"] < 0.47 < w[3.0]["y_UV"] and w[3.0]["y_IR"] > 0.53


def test_face_pairing():
    b = D["face_pairing"]["best"]
    assert b["F"] == 80 and not b["manifold"] and D["face_pairing"]["chi_range"][0] > 0
