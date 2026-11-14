"""Pass 12671: exact witness for the F_8 regulus constant; Pauli-stabiliser ladder; order-9 reduction fails."""
import json
import os
from fractions import Fraction as Fr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def kmul(x, y):
    """Multiply a + b s with a, b in Q(g) (g^3 = 3g - 1, s^2 = 3); coordinates [1, g, g^2, s, s g, s g^2]."""
    def qg(p, r):
        c = [Fr(0)] * 5
        for i in range(3):
            for j in range(3): c[i + j] += p[i] * r[j]
        c[2] += 3 * c[4]; c[1] -= c[4]; c[1] += 3 * c[3]; c[0] -= c[3]
        return c[:3]
    a, b, c, d = x[:3], x[3:], y[:3], y[3:]
    ac, bd, ad, bc = qg(a, c), qg(b, d), qg(a, d), qg(b, c)
    return [ac[i] + 3 * bd[i] for i in range(3)] + [ad[i] + bc[i] for i in range(3)]


def test_exact_witness_verified():
    d = load("w33_f8_exact_witness.json")
    assert d["hermitian"] and d["trace_one"] and d["idempotent"] and d["equals_closed_form"]
    assert d["c_exact"][:3] == ["47/9", "-16/9", "0"] and all(v == "0" for v in d["c_exact"][3:])
    assert d["n_nonzero"] == 512


def test_expectation_squares_sum_to_dimension_exactly():
    d = load("w33_f8_exact_witness.json")
    tot = [Fr(0)] * 6
    for co in d["expectations"].values():
        x = [Fr(c) for c in co]
        sq = kmul(x, x)
        tot = [a + b for a, b in zip(tot, sq)]
    assert tot == [Fr(64)] + [Fr(0)] * 5  # tr rho^2 = 1 for rho = (1/64) sum r_P P


def test_rank3_minimiser_rigid_and_identified():
    d = load("w33_f8_rank3_stabiliser_exact.json")
    assert d["all_identified"] and d["hessian_null_dim"] == 2 and d["double_hits"] == 20
    counts = sorted(L["count"] for L in d["levels"])
    assert counts == [8] + [72] * 7 and d["n_nonzero"] == 512


def test_stabiliser_ladder():
    d = load("w33_f8_pauli_stabiliser_ladder.json")
    assert d["rank2"]["dim"] == 16 and d["rank2"]["hits"] == d["rank2"]["starts"]
    assert d["rank3"]["attaining_c8"] == 56 and d["rank3"]["hit_cosets_all_uncovered"]
    assert d["rank4"]["attaining_c8"] == 0 and d["rank4"]["groups_tested"] > 0


def test_order9_reduction_does_not_reach_c8():
    d = load("w33_f8_order9_reduction.json")
    assert d["n_symmetries"] == 3528 and d["attains_c8"] == []
    best = [d["minima"][str(j)]["best_c"] for j in range(9)]
    assert abs(best[0] - 37 / 3) < 1e-8 and all(abs(b - 47 / 9) < 1e-8 for b in best[1:])
