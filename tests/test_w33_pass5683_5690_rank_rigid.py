"""Regression lock for Passes 5683-5690."""
from __future__ import annotations

import itertools
import json
from math import comb
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5683_5690_W33_IS_NOT_RANK_RIGID.json"


def rank_p(A, p):
    A = np.array(A, dtype=int) % p
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] % p), None)
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r][c]), p - 2, p)) % p
        for i in range(m):
            if i != r and A[i][c] % p:
                A[i] = (A[i] - A[i][c] * A[r]) % p
        r += 1
    return r


def w3q(q):
    def norm(v):
        for c in v:
            if c:
                inv = pow(c, -1, q)
                return tuple((x * inv) % q for x in v)
    P = sorted({norm(v) for v in itertools.product(range(q), repeat=4) if any(v)})

    def sf(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q
    S = np.array([[pow(sf(P[i], P[j]), 2, q) for j in range(len(P))] for i in range(len(P))])
    C = np.array([[1 if i != j and sf(P[i], P[j]) else 0 for j in range(len(P))]
                  for i in range(len(P))])
    return P, S, C


@pytest.mark.parametrize("q,npts", [(3, 40), (5, 156)])
def test_noncollinearity_rank_is_dim_sym2(q, npts):
    """The one theorem in this thread with a proof behind it."""
    P, S, C = w3q(q)
    assert len(P) == npts
    assert np.array_equal((S != 0).astype(int), C), "C is the elementwise square of sf"
    assert rank_p(S, q) == comb(5, 2) == 10, "rank is dim Sym^2(F_q^4), independent of q"


def test_w33_incidence_is_rigid_but_adjacency_is_not():
    """The correction to Pass 5673."""
    P, S, C = w3q(3)
    A = 1 - C - np.eye(40, dtype=int)
    assert int(np.linalg.matrix_rank(A.astype(float))) == 40
    assert rank_p(A, 2) < 40, "the collinearity adjacency DOES collapse at p=2"
    assert rank_p(C, 3) == 10 < 40, "and the complement collapses hard at p=3"


def test_kernel_is_not_a_block_system_detector():
    """Petersen is primitive yet has a nonzero GF(2) kernel."""
    pv = list(itertools.combinations(range(5), 2))
    PET = np.array([[1 if i != j and not (set(a) & set(b)) else 0
                     for j, b in enumerate(pv)] for i, a in enumerate(pv)])
    assert 10 - rank_p(PET, 2) > 0, "primitive graph, nonzero kernel"
    C5 = np.array([[1 if (i - j) % 5 in (1, 4) else 0 for j in range(5)] for i in range(5)])
    assert 5 - rank_p(C5, 2) > 0


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_grid_line_hypothesis_recorded_as_refuted():
    d = json.loads(CERT.read_text(encoding="utf-8"))["pass_5685"]
    assert d["on_a_grid_row"] == 0 and d["on_a_grid_column"] == 0
    assert d["result"].startswith("REFUTED")
    assert "still_open" in d


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_aut_is_an_order_match_not_an_identification():
    d = json.loads(CERT.read_text(encoding="utf-8"))["pass_5687"]
    assert d["order"] == d["wf4z_order"] == 576
    assert d["typed"] is False, "must not claim identification from an order"
    assert d["groups_of_order_576"] == 8681
    assert "ORDER MATCH ONLY" in d["claim"]


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_correction_to_5673_is_recorded():
    d = json.loads(CERT.read_text(encoding="utf-8"))["pass_5683"]
    assert "Pass 5673" in d["corrects"]
