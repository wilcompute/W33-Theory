"""Pass 12729."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12729_round.json")))
O = json.load(open(os.path.join(ROOT, "data", "explore_pass12729_orbifold_fix.json")))
A = json.load(open(os.path.join(ROOT, "data", "explore_pass12729_alloc.json")))


def test_large_fI():
    r = {x["H_I"]: x for x in D["large_fI"]["rows"]}
    assert 0.05 < r[1e12]["f_I_over_MPl"] < 0.1 and r[1e13]["f_I_over_MPl"] > 0.5


def test_evidence_A_below_Bprime():
    e = D["evidence_A"]
    assert e["rows"]["15"]["A"] < e["Bprime"][0]


def test_orbifold_sign_discrepancy_recorded():
    assert O["rows"]["64"]["su5_gauge_only"] < 0 < -O["hall_nomura_dalpha_s_MsR64"]


def test_allocation():
    al = A["allocs"]
    assert al["2.0"]["bits_per_weight"] <= 2.0 + 1e-9 and al["4.0"]["joint_bpc"] <= al["2.0"]["joint_bpc"] + 0.05


def test_layer0_dominates_sensitivity():
    c = A["cost"]
    top4 = sorted(c, key=lambda k: -c[k]["ternary"])[:4]
    assert all(k.endswith("0") for k in top4)
    l0 = sum(v["ternary"] for k, v in c.items() if k.endswith("0")); l1 = sum(v["ternary"] for k, v in c.items() if k.endswith("1"))
    assert l0 > 2 * l1
    assert A["allocs"]["4.0"]["assign"]["o0"] == "fp32"


def test_cprt_orbifold():
    assert abs(O["cprt"]["combination"] - 6 / 7) < 1e-9 and 0.25 < O["cprt"]["rows"]["10"] < 0.4
