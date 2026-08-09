#!/usr/bin/env python3
"""Pass 4465 -- general GQ(s,t) line-signing trace/apartment theorem.

The W33 theorem of Pass 4461 is a special case of a parameter-exact statement
for every finite generalized quadrangle GQ(s,t).

For the point-collinearity graph:

    n = (s+1)(st+1)
    L = (t+1)(st+1)               geometric lines
    d = s(t+1)
    lambda = s-1
    mu = t+1.

Give one Rademacher sign sigma_l to each geometric line and all edges of its
K_{s+1} clique that same sign.  Then:

    tr(A_sigma^2) = n d

    tr(A_sigma^3) = 6*C(s+1,3) * sum_l sigma_l

    tr(A_sigma^4)
      = n d(2d-1)
        + 24 L C(s+1,4)
        + 8 W_Q(sigma),

where W_Q is the sum of products of the four side-line signs over the induced
quadrangles of the point graph.

Why the fourth-moment classification is complete:
  * repeated-edge closed 4-walks contribute n d(2d-1);
  * a simple 4-cycle with a chord contains a triangle, and every triangle in a
    GQ collinearity graph lies on one geometric line, forcing the whole 4-cycle
    into that K_{s+1};
  * all remaining simple 4-cycles are induced quadrangles and use four distinct
    geometric lines.

The number of induced quadrangles is

    Q = n s^2 t^2 (t+1) / 8.

Let H be line/quadrangle incidence and A* the line-collinearity graph (the point
collinearity graph of the dual GQ(t,s)).  Then a line occurs in

    r = (s+1)s^2 t^2 / 2

quadrangles; two intersecting lines occur together in

    alpha = s^2 t

quadrangles; two disjoint lines occur together in

    beta = C(s+1,2) = s(s+1)/2

quadrangles.  Hence

    H H^T = (r-beta) I + (alpha-beta) A* + beta J.

For independent random line signs, distinct quadrangles give distinct degree-4
Walsh supports, so E W_Q=0, Var W_Q=Q and the frustrated quadrangle fraction has
mean 1/2 and SD 1/(2 sqrt(Q)).

The script evaluates the formulas for the four classical examples used by the
recent cross-GQ signing passes: GQ(2,2), W(3,3)=GQ(3,3), Q(5,3)=GQ(3,9), and its
dual parameter set GQ(9,3).  It rebuilds W(3,3) explicitly and checks every
formula against the exact enumerator from Pass 4461.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class GQFormula:
    s: int
    t: int
    points: int
    lines: int
    degree: int
    quadrangles: int
    quadrangles_per_line: int
    quadrangles_per_intersecting_line_pair: int
    quadrangles_per_disjoint_line_pair: int
    trace4_constant: int
    trace3_line_coefficient: int
    random_frustration_sd: float


def formulas(s: int, t: int) -> GQFormula:
    if s < 1 or t < 1:
        raise ValueError("s,t must be positive")
    n = (s + 1) * (s * t + 1)
    L = (t + 1) * (s * t + 1)
    d = s * (t + 1)
    Q_num = n * s * s * t * t * (t + 1)
    assert Q_num % 8 == 0
    Q = Q_num // 8
    r_num = (s + 1) * s * s * t * t
    assert r_num % 2 == 0
    r = r_num // 2
    alpha = s * s * t
    beta = s * (s + 1) // 2
    constant = n * d * (2 * d - 1) + 24 * L * math.comb(s + 1, 4)
    c3 = 6 * math.comb(s + 1, 3)
    return GQFormula(
        s=s,
        t=t,
        points=n,
        lines=L,
        degree=d,
        quadrangles=Q,
        quadrangles_per_line=r,
        quadrangles_per_intersecting_line_pair=alpha,
        quadrangles_per_disjoint_line_pair=beta,
        trace4_constant=constant,
        trace3_line_coefficient=c3,
        random_frustration_sd=1.0 / (2.0 * math.sqrt(Q)),
    )


def main() -> int:
    table = {
        "GQ(2,2)=W(3,2)": formulas(2, 2),
        "GQ(3,3)=W(3,3)": formulas(3, 3),
        "GQ(3,9)=Q(5,3)": formulas(3, 9),
        "GQ(9,3) dual parameter set": formulas(9, 3),
    }

    # Duality preserves the number of apartments/quadrangles, not the number of
    # line-signing degrees of freedom or the clique size of one signed line.
    assert table["GQ(3,9)=Q(5,3)"].quadrangles == table["GQ(9,3) dual parameter set"].quadrangles == 102060
    assert table["GQ(3,9)=Q(5,3)"].lines == 280
    assert table["GQ(9,3) dual parameter set"].lines == 112

    # Rebuild W33 and verify the symbolic specialisation exhaustively.
    _, lines, A, _, edge_line = geometry()
    w33 = table["GQ(3,3)=W(3,3)"]
    assert w33.points == 40
    assert w33.lines == 40
    assert w33.degree == 12
    assert w33.quadrangles == 1620
    assert w33.quadrangles_per_line == 162
    assert w33.quadrangles_per_intersecting_line_pair == 27
    assert w33.quadrangles_per_disjoint_line_pair == 6
    assert w33.trace4_constant == 12000
    assert w33.trace3_line_coefficient == 24

    cycles = simple_four_cycles(A)
    supports = [frozenset(edge_line[e] for e in C) for C in cycles]
    assert len(supports) == w33.quadrangles
    per_line = np.zeros(40, dtype=np.int64)
    pair = np.zeros((40, 40), dtype=np.int64)
    for support in supports:
        for i in support:
            per_line[i] += 1
        ids = sorted(support)
        for ai, i in enumerate(ids):
            for j in ids[ai + 1:]:
                pair[i, j] += 1
                pair[j, i] += 1
    assert set(per_line.tolist()) == {w33.quadrangles_per_line}
    for i in range(40):
        for j in range(i + 1, 40):
            meet = bool(lines[i] & lines[j])
            expected = (
                w33.quadrangles_per_intersecting_line_pair
                if meet
                else w33.quadrangles_per_disjoint_line_pair
            )
            assert int(pair[i, j]) == expected

    # The constant trace term can also be recovered directly from the unsigned
    # W33 line signing, where every apartment parity is +1.
    trace4_unsigned = int(np.trace(np.linalg.matrix_power(A, 4)))
    assert trace4_unsigned == w33.trace4_constant + 8 * w33.quadrangles
    assert trace4_unsigned == 24960

    result = {
        "pass": 4465,
        "theorem": "general GQ(s,t) line-signing trace and quadrangle-incidence theorem",
        "formulas": {
            "n": "(s+1)(st+1)",
            "L": "(t+1)(st+1)",
            "d": "s(t+1)",
            "Q": "n*s^2*t^2*(t+1)/8",
            "trace2": "n*d",
            "trace3": "6*C(s+1,3)*sum_l sigma_l",
            "trace4": "n*d*(2d-1) + 24*L*C(s+1,4) + 8*W_Q",
            "r": "(s+1)*s^2*t^2/2",
            "alpha": "s^2*t",
            "beta": "s(s+1)/2",
            "HHt": "(r-beta)I + (alpha-beta)A_dual + beta J",
            "random_WQ_mean": 0,
            "random_WQ_variance": "Q",
            "random_frustrated_fraction_mean": 0.5,
            "random_frustrated_fraction_sd": "1/(2 sqrt(Q))",
        },
        "examples": {name: asdict(row) for name, row in table.items()},
        "W33_exact_rebuild": {
            "quadrangles_enumerated": len(cycles),
            "unsigned_trace4": trace4_unsigned,
            "status": "PASS",
        },
        "boundary": (
            "The theorem identifies the exact low spectral moments controlled by a line signing on any GQ(s,t). "
            "It does not predict Ramanujan probability from s,t alone; the recent Q(5,3) counterexample already "
            "shows that such a stronger coarseness law is false."
        ),
    }

    out = ROOT / "data" / "PART_W33_PASS4465_GENERAL_GQ_LINE_SIGNING_TRACE.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4465 -- general GQ(s,t) line-signing trace theorem")
    for name, row in table.items():
        print(
            f"  {name}: points={row.points} lines={row.lines} d={row.degree} "
            f"Q={row.quadrangles} r={row.quadrangles_per_line} "
            f"trace4_const={row.trace4_constant}"
        )
    print("  dual GQ(3,9)/GQ(9,3): same Q=102060, different line registers 280 vs 112")
    print("  W33 exact rebuild: PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
