"""Pass 12669: closed form of the F_8 regulus constant; Haemers matrices of rank 10."""
import json
import os

import mpmath as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_c8_closed_form():
    mp.mp.dps = 50
    d = load("w33_f8_constant_high_precision.json")
    c = mp.mpf(d["c8"])
    closed = (47 - 32 * mp.cos(2 * mp.pi / 9)) / 9
    assert abs(c - closed) < mp.mpf(10) ** -40
    assert abs(243 * closed ** 3 - 3807 * closed ** 2 + 17577 * closed - 23941) < mp.mpf(10) ** -40
    assert d["findpoly"] == {"3": [-243, 3807, -17577, 23941]}
    # consistency with the repository's exact bounds
    assert mp.mpf("2.0818") < closed < mp.mpf("2.4985086592218817") < 3


def test_cubic_is_cyclic():
    import sympy as sp
    x = sp.symbols("x")
    P = 243 * x ** 3 - 3807 * x ** 2 + 17577 * x - 23941
    disc = sp.discriminant(P, x)
    assert sp.factorint(disc) == {2: 24, 3: 12} and sp.sqrt(disc).is_integer
    assert sp.Poly(P, x).is_irreducible


def test_haemers_rank_ten():
    runs = [load(f"w33_haemers_invariant_search_seed{s}.json") for s in (1, 2)]
    assert all(r["control"]["meeting_graph_F2_rank"] == 7 for r in runs)
    assert min(r["best_rank"] for r in runs) == 10 and not any(r["beats_lovasz"] for r in runs)
    for r in runs:
        b = r["best"]
        assert b["verified_support"] and b["rank_recomputed"] == 10


def test_minimiser_partial_identification_recorded():
    d = load("w33_f8_minimiser_exact.json")
    assert d["n_paulis"] == 4096 and d["n_zero"] == 3552 and d["n_failed"] == 288
    assert d["n_identified"] - d["n_zero"] == 256 and d["purity_check"].startswith("1.0")
