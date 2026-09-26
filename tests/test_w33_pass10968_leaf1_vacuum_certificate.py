"""Independent verification of the Pass 10968 leaf-1 vacuum certificate for Z6II_23.

From the frozen vectors only:
  1. the D-flat vector is strictly positive on every vacuum item, cancels every non-anomalous D-term and
     has the FI-cancelling sign;
  2. ONE parity element (the witness) gives phase 0 to every vacuum item and even pair, 1/2 to every odd
     state, and integral phase to the integrality / W-invariance vectors (a genuine non-R symmetry);
  3. every stored mass monomial Xbar X prod S^a obeys every selection rule exactly;
  4. mass-matrix ranks reached by the stored monomials (reported, and pinned).
"""
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "data" / "w33_pass10968_leaf1_vacuum_certificate.json").read_text())
items = [[F(x) for x in k] for k in C["items"]]
vec = {k: [F(x) for x in v] for k, v in C["field_vectors"].items()}
virtual = [[F(x) for x in v] for v in C["virtual"]]
w = virtual[-1]
NQ = len(items[0]) - (len(virtual) - 1)


def test_dflat_vector_exact():
    a = [F(x) for x in C["dflat_vector"]]
    assert len(a) == len(items) and all(x > 0 for x in a)
    for k in range(1, NQ):
        assert sum(ai * it[k] for ai, it in zip(a, items)) == 0
    assert C["anomalous_sign"] * sum(ai * it[0] for ai, it in zip(a, items)) == -1


def test_one_parity_element_for_the_whole_vacuum():
    x = [F(v) for v in C["parity_witness"]]
    ph = lambda v: sum(a * b for a, b in zip(v, x)) % 1
    assert all(ph(it) == 0 for it in items)
    assert all(ph([F(t) for t in v]) == F(1, 2) for v in C["odd"])
    assert all(ph([F(t) for t in v]) == 0 for v in C["even_pairs"])
    assert all(ph(v) == 0 for v in virtual)


def test_every_monomial_obeys_all_rules():
    for key, expo in C["mass_monomials"].items():
        a, b = key.split("*")
        tot = [p + q - r for p, q, r in zip(vec[a], vec[b], w)]
        for i, e in expo.items():
            tot = [t + e * v for t, v in zip(tot, items[int(i)])]
        assert all(t == 0 for t in tot[:NQ]), key
        assert all(t.denominator == 1 for t in tot[NQ:]), key


def ranks(max_order=99):
    out = {}
    names = {k for key in C["mass_monomials"] for k in key.split("*")} | set(vec)
    lab = lambda p: sorted((n for n in vec if n.rsplit("_", 1)[0] == p), key=lambda s: int(s.split("_")[1]))
    for Xb, X in (("d", "bd"), ("u", "bu"), ("e", "be"), ("bq", "q"), ("bl", "l")):
        R_, C_ = lab(Xb), lab(X)
        B = np.array([[int(f"{r}*{c}" in C["mass_monomials"] and 2 + sum(C["mass_monomials"][f"{r}*{c}"].values()) <= max_order)
                       for c in C_] for r in R_])
        rr, cc = linear_sum_assignment(-B)
        out[Xb] = (int(B[rr, cc].sum()), len(R_))
    return out


def test_mass_ranks_pinned():
    r = ranks()
    print(r)
    assert {k: list(v) for k, v in r.items()} == {k: list(v) for k, v in C["ranks_pinned"].items()}
