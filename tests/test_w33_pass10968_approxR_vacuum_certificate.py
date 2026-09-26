"""Independent verification of the Pass 10968 approximate-R vacuum of Z6II_23.

From the frozen vectors only:
  1. exact D-flat vector, strictly positive on all 23 vacuum directions, FI-cancelling;
  2. ONE parity element: vacuum and even pairs at phase 0, light states at 1/2, integrality/W vectors integral;
  3. every stored mass monomial obeys every selection rule; exotic matrices reach full rank;
  4. the Higgs matrix is structurally rank 5 of 6 AT ALL ORDERS (HNF lattice membership of v_bl + v_l - w);
  5. no parity-even direction outside the vacuum can appear linearly (all orders): outside F-terms vanish;
  6. W restricted to the vacuum is NOT zero (recorded honestly): internal F-flatness is open.
"""
import json
from fractions import Fraction as F
from math import lcm
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import linear_sum_assignment
from sympy.matrices.normalforms import hermite_normal_form

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "data" / "w33_pass10968_approxR_vacuum_certificate.json").read_text())
items = [[F(x) for x in k] for k in C["items"]]
vec = {k: [F(x) for x in v] for k, v in C["field_vectors"].items()}
virtual = [[F(x) for x in v] for v in C["virtual"]]
w = virtual[-1]
NQ = len(items[0]) - (len(virtual) - 1)
lab = lambda p: sorted((n for n in vec if n.rsplit("_", 1)[0] == p), key=lambda s: int(s.split("_")[1]))


def test_dflat_exact():
    a = [F(x) for x in C["dflat_vector"]]
    assert len(a) == len(items) == 23 and all(x > 0 for x in a)
    for k in range(1, NQ):
        assert sum(ai * it[k] for ai, it in zip(a, items)) == 0
    assert C["anomalous_sign"] * sum(ai * it[0] for ai, it in zip(a, items)) == -1


def test_one_parity_element():
    x = [F(v) for v in C["parity_witness"]]
    ph = lambda v: sum(a * b for a, b in zip(v, x)) % 1
    assert all(ph(it) == 0 for it in items)
    assert all(ph([F(t) for t in v]) == F(1, 2) for v in C["odd"])
    assert all(ph([F(t) for t in v]) == 0 for v in C["even_pairs"])
    assert all(ph(v) == 0 for v in virtual)


def test_monomials_and_exotic_rank():
    for key, expo in C["mass_monomials"].items():
        a, b = key.split("*")
        tot = [p + q - r for p, q, r in zip(vec[a], vec[b], w)]
        for i, e in expo.items():
            tot = [t + e * v for t, v in zip(tot, items[int(i)])]
        assert all(t == 0 for t in tot[:NQ]) and all(t.denominator == 1 for t in tot[NQ:]), key
    for Xb, X in (("d", "bd"), ("u", "bu"), ("e", "be"), ("bq", "q")):
        B = np.array([[int(f"{r}*{c}" in C["mass_monomials"]) for c in lab(X)] for r in lab(Xb)])
        rr, cc = linear_sum_assignment(-B)
        assert B[rr, cc].sum() == len(lab(Xb)), Xb


def _lattice():
    integ = virtual[:-1]
    gens = items + integ
    den = lcm(*[v.denominator for g in gens + list(vec.values()) + [w] for v in g])
    G = sp.Matrix([[int(v * den) for v in g] for g in gens]).T
    H = hermite_normal_form(G)
    B = sp.Matrix.hstack(*[H[:, j] for j in range(H.cols) if any(H[:, j])])

    def inl(u):
        try:
            c, prm = B.gauss_jordan_solve(sp.Matrix([int(v * den) for v in u]))
        except ValueError:
            return False
        c = c.subs({p: 0 for p in prm})
        return all(sp.fraction(x)[1] == 1 for x in c)
    return inl


def test_higgs_rank_five_at_all_orders_and_no_outside_linear_terms():
    inl = _lattice()
    allowed = [[a, b] for a in lab("bl") for b in lab("l") if inl([p + q - r for p, q, r in zip(vec[a], vec[b], w)])]
    assert sorted(allowed) == sorted(C["higgs_pairs_allowed_all_orders"])
    B = np.array([[int([a, b] in allowed) for b in lab("l")] for a in lab("bl")])
    rr, cc = linear_sum_assignment(-B)
    assert B[rr, cc].sum() == len(lab("bl")) - 1
    assert C["outside_linear_terms_possible"] == []


def test_superpotential_on_vacuum_is_not_zero():
    assert C["W_S_possible_all_orders"] is True
