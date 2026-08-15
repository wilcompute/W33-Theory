#!/usr/bin/env python3
"""Pass5388--5392: all-q Levi flag distance/Hodge theorem.

Let S be any generalized quadrangle of order (q,q), q>1.  Let Gamma be its
point-line incidence (Levi) graph and X=L(Gamma) its line graph.  Vertices of
X are flags of S.

The symmetric 4-class flag fusion is existing literature (Colangelo,
Monzillo, Siciliano, Discrete Math. 347 (2024), 114054).  The contribution
certified here is the explicit Hodge/cycle-space bridge and its all-q
specialization of the W33 BT545--BT551 stack:

  intersection array(X) = {2q,q,q,q ; 1,1,1,2},
  distance shells       = 1,2q,2q^2,2q^3,q^4,
  dim cycle(Gamma)      = q^4,
  E_{-2} = P_cycle
          = 1/N (q^4 A0 - q^3 A1 + q^2 A2 - q A3 + A4),
  N=(q+1)^2(q^2+1).

In particular the terminal first-eigenmatrix row is q-independent,
  (1,-2,2,-2,1),
and the terminal second-eigenmatrix column is
  (q^4,-q^3,q^2,-q,1).
At q=3 this is exactly the W33 protected column (81,-27,9,-3,1).

No code-distance or physical-protection claim follows from this theorem alone.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5388_5392_ALLQ_LEVI_FLAG_HODGE.json"


def ptrim(p: list[int]) -> list[int]:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def padd(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return ptrim(out)


def pscale(a: list[int], c: int) -> list[int]:
    return ptrim([c * x for x in a])


def pmul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return ptrim(out)


def quotient_charpoly(q: int) -> list[int]:
    """Return det(xI-B) low-degree first for the distance quotient matrix."""
    b = [2 * q, q, q, q]
    c = [1, 1, 1, 2]
    a = [0, q - 1, q - 1, q - 1, 2 * q - 2]
    d_prev = [1]
    d_now = [-a[0], 1]
    for i in range(1, 5):
        term1 = pmul([-a[i], 1], d_now)
        term2 = pscale(d_prev, -b[i - 1] * c[i - 1])
        d_prev, d_now = d_now, padd(term1, term2)
    return d_now


def expected_charpoly(q: int) -> list[int]:
    # (x-2q)(x+2)(x-(q-1))*((x-(q-1))^2-2q)
    linear = pmul([-2 * q, 1], [2, 1])
    linear = pmul(linear, [1 - q, 1])
    quadratic = [q * q - 4 * q + 1, 2 - 2 * q, 1]
    return pmul(linear, quadratic)


def theorem_row(q: int) -> dict:
    assert q > 1
    v = (q + 1) * (q * q + 1)  # points, and also lines
    n_levi = 2 * v
    n_flags = (q + 1) * v
    degree = 2 * q

    b = [2 * q, q, q, q]
    c = [1, 1, 1, 2]
    a = [0, q - 1, q - 1, q - 1, 2 * q - 2]
    shells = [1]
    for i in range(4):
        num = shells[-1] * b[i]
        assert num % c[i] == 0
        shells.append(num // c[i])
    assert shells == [1, 2 * q, 2 * q * q, 2 * q**3, q**4]
    assert sum(shells) == n_flags

    m_levi = n_flags
    cycle_rank = m_levi - n_levi + 1
    assert cycle_rank == q**4

    f = q * (q + 1) ** 2 // 2
    g = q * (q * q + 1) // 2
    multiplicities = [1, f, 2 * g, f, q**4]
    assert sum(multiplicities) == n_flags

    # Quotient matrix characteristic polynomial gives the five adjacency
    # eigenvalues: 2q, q-1 +/- sqrt(2q), q-1, -2.
    assert quotient_charpoly(q) == expected_charpoly(q)

    # Exact trace checks without adjoining sqrt(2q).
    trace = 2 * q + 2 * f * (q - 1) + 2 * g * (q - 1) - 2 * q**4
    assert trace == 0
    pair_square_sum = 2 * ((q - 1) ** 2 + 2 * q)
    trace2 = (2 * q) ** 2 + f * pair_square_sum + 2 * g * (q - 1) ** 2 + q**4 * 4
    assert trace2 == n_flags * degree

    # Standard sequence for theta=-2.
    u = [Fraction((-1) ** d, q**d) for d in range(5)]
    bb = b + [0]
    cc = [0] + c
    for i in range(5):
        lhs = Fraction(-2) * u[i]
        rhs = Fraction(a[i]) * u[i]
        if i:
            rhs += Fraction(cc[i]) * u[i - 1]
        if i < 4:
            rhs += Fraction(bb[i]) * u[i + 1]
        assert lhs == rhs

    terminal_P_row = [shells[d] * u[d] for d in range(5)]
    terminal_Q_col = [q**4 * u[d] for d in range(5)]
    assert terminal_P_row == [1, -2, 2, -2, 1]
    assert terminal_Q_col == [q**4, -q**3, q**2, -q, 1]

    return {
        "q": q,
        "points": v,
        "lines": v,
        "levi_vertices": n_levi,
        "flags_linegraph_vertices": n_flags,
        "linegraph_degree": degree,
        "intersection_array": {"b": b, "c": c},
        "a": a,
        "distance_shells": shells,
        "levi_cycle_rank": cycle_rank,
        "spectral_multiplicities": {
            "2q": 1,
            "q-1+sqrt(2q)": f,
            "q-1": 2 * g,
            "q-1-sqrt(2q)": f,
            "-2": q**4,
        },
        "terminal_P_row": [str(x) for x in terminal_P_row],
        "terminal_Q_column": [str(x) for x in terminal_Q_col],
    }


def main() -> dict:
    anchors = {str(q): theorem_row(q) for q in [2, 3, 4, 5, 7, 8, 9, 11, 13]}
    q3 = anchors["3"]
    assert q3["flags_linegraph_vertices"] == 160
    assert q3["distance_shells"] == [1, 6, 18, 54, 81]
    assert q3["levi_cycle_rank"] == 81
    assert q3["terminal_P_row"] == ["1", "-2", "2", "-2", "1"]
    assert q3["terminal_Q_column"] == ["81", "-27", "9", "-3", "1"]

    out = {
        "schema": "w33.allq_levi_flag_hodge.v1",
        "pass_range": [5388, 5392],
        "status": "THEOREM_ALGEBRAIC_AND_GRAPH_THEORETIC",
        "domain": "Any finite generalized quadrangle of order (q,q), q>1; in particular W(3,q) for every prime power q.",
        "literature_boundary": "Colangelo-Monzillo-Siciliano (Discrete Mathematics 347 (2024), 114054; arXiv:2406.03942) already establish the symmetric primitive 4-class flag fusion and its valencies. This certificate does not claim priority for that association scheme.",
        "distance_theorem": {
            "flag_graph": "The first fusion relation is the line graph of the Levi incidence graph.",
            "intersection_array": "{2q,q,q,q ; 1,1,1,2}",
            "distance_shells": "1, 2q, 2q^2, 2q^3, q^4",
            "vertex_count": "(q+1)^2(q^2+1)",
        },
        "spectrum": {
            "eigenvalues": ["2q", "q-1+sqrt(2q)", "q-1", "q-1-sqrt(2q)", "-2"],
            "multiplicities": ["1", "q(q+1)^2/2", "q(q^2+1)", "q(q+1)^2/2", "q^4"],
            "characteristic_polynomial": "(x-2q)(x+2)(x-q+1)((x-q+1)^2-2q)",
        },
        "hodge_bridge": {
            "oriented_incidence_identity": "For the Levi graph oriented point->line, D^T D = 2I + A_X.",
            "cycle_space": "ker(D)=E_{-2}(A_X)",
            "rank_D": "2(q+1)(q^2+1)-1",
            "cycle_dimension": "q^4",
            "projector": "P_cyc=E_{-2}=((q^4)A0-(q^3)A1+(q^2)A2-qA3+A4)/((q+1)^2(q^2+1))",
            "terminal_first_eigenmatrix_row": ["1", "-2", "2", "-2", "1"],
            "terminal_second_eigenmatrix_column": ["q^4", "-q^3", "q^2", "-q", "1"],
        },
        "w33_specialization": {
            "q": 3,
            "flags": 160,
            "shells": [1, 6, 18, 54, 81],
            "cycle_dimension": 81,
            "projector_numerator": [81, -27, 9, -3, 1],
            "reading": "Exactly BT545-BT551: the W33 H1=81 Hodge/Kirchhoff projector is the q=3 terminal primitive idempotent.",
        },
        "anchors": anchors,
        "boundary": "This theorem identifies a graph/Hodge sector. It does not by itself prove a quantum-code distance, a fault-tolerance threshold, or a physical protection mechanism.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
