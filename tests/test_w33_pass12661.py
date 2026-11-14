"""Pass 12661: exhaustive stabiliser minimum for the F_8 regulus; q = 32 stabiliser value."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_exhaustive_no_one_or_two_point_lagrangian_at_q8():
    d = load("w33_regulus_stabiliser_exhaustive2.json")
    assert d["q4"]["status"] == "exists" and d["q4"]["lagrangians_found"] == 3  # positive control
    assert d["q8"]["covered_orbit"] == 567 and d["q8"]["level2_orbit_reps"] == 16
    assert d["q8"]["subspaces_by_dim"] == {"2": 16, "3": 2301, "4": 15944, "5": 3672, "6": 0} and d["q8"]["status"] == "none"
    assert d["q8_exactly_two"]["subspaces_by_dim"]["6"] == 0 and d["q8_exactly_two"]["status"] == "none"


def test_q4_example_is_a_one_point_lagrangian():
    # independent check of the control witness: 16 vectors, isotropic, exactly one non-zero point with Q = 0
    d = load("w33_regulus_stabiliser_exhaustive2.json")["q4"]["example"]
    k, q = 2, 4

    def mul(a, b):
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
            if a >> k & 1:
                a ^= 0b111
        return r

    tr = lambda a: (a ^ mul(a, a)) & 1 if (a ^ mul(a, a)) in (0, 1) else None
    parts = lambda v: (v & 3, (v >> 2) & 3, (v >> 4) & 3, (v >> 6) & 3)
    Q = lambda v: mul(parts(v)[0], parts(v)[2]) ^ mul(parts(v)[1], parts(v)[3])

    def om(u, v):
        a, b = parts(u), parts(v)
        return tr(mul(a[0], b[2]) ^ mul(a[1], b[3]) ^ mul(a[2], b[0]) ^ mul(a[3], b[1]))

    assert len(d) == 16 and 0 in d
    assert all(om(u, v) == 0 for u in d for v in d)
    assert all((u ^ v) in d for u in d for v in d)
    assert sum(1 for v in d if v and Q(v) == 0) == 1


def test_stabiliser_values_fit_pattern():
    a = load("w33_regulus_stabiliser_minimum.json")
    b = load("w33_regulus_stabiliser_minimum_k5.json")
    assert a["q8"]["m_star_found"] == 3 == (8 + 1) // 3
    assert b["q32"]["m_star_found"] == 11 == (32 + 1) // 3
    c = load("w33_regulus_constants_q16_q32.json")
    assert c["q32"]["c"] > b["q32"]["m_star_found"]  # the random-start optimiser did not reach the stabiliser value
