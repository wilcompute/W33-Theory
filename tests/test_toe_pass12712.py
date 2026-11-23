"""Pass 12712."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12712_round.json"), encoding="utf-8"))


def test_energy():
    e = D["energy"]
    assert abs(e["onchip"]["3"]["energy_per_bit_rel"] - 2.52) < 0.01
    w = e["link_windows_alpha1"]
    assert 35 < w["NRZ_to_PAM3"] < 37 and 42 < w["PAM3_to_PAM4"] < 43


def test_rs_exact():
    r = D["rs_exact"]
    assert 6.0 < r["kL_cross_hybrid"] < 7.0
    big = [x for x in r["rows"] if x["kL"] >= 7][0]
    assert abs(big["x1"] - 3.8317) < 1e-3


def test_forecast():
    f = D["forecast"]
    assert f["testable"]["reach 1e-07"] > 0.95 and f["fcc_3sigma"] > 0.95


def test_qat():
    q = D["qat"]["rows"]
    assert q["binary"]["acc"] < q["ternary"]["acc"] < q["2bit"]["acc"] <= q["fp32"]["acc"] + 0.01
    assert 0.35 < q["ternary"]["zero_frac"] < 0.55
