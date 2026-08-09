#!/usr/bin/env python3
"""Pass 4530 -- symbolic protected-quotient law for Q(5,q)=GQ(q,q^2).

Pass 4471 proved for a GQ(s,t) that apartment Gram equals incidence Gram over
F2 iff s == 3 (mod 4) and t is odd.  Specializing to Q(5,q), of order
(q,q^2), therefore gives an infinite exact passing family for q == 3 (mod 4).

This pass deliberately leaves the difficult binary-rank function
rho(q)=rank_2(N^T N) explicit.  For every passing q the nondegenerate apartment
quotient has dimension rho(q), while the apartment radical has dimension
h(q)-rho(q), h(q)=rank_2(H).  The q=3 anchor is the independently enumerated
Pass-4506 value h=279, rho=70.

No closed polynomial for h(q) or rho(q) is inferred from q=3.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4530_Q5Q_SYMBOLIC_PROTECTED_LAW.json"


def q5q_row(q: int) -> dict:
    assert q % 4 == 3
    s, t = q, q*q
    points = (s + 1) * (s*t + 1)
    lines = (t + 1) * (s*t + 1)
    r = (s + 1) * s*s * t*t // 2
    alpha = s*s*t
    beta = s*(s + 1)//2
    apartments = lines * r // 4
    # HH^T=(r-beta)I+(alpha-beta)A+beta J.
    # N^T N=(s+1)I+A.  For q=3 mod4: beta even,
    # r-beta even, alpha-beta odd, s+1 even.
    assert beta % 2 == 0
    assert (r-beta) % 2 == 0
    assert (alpha-beta) % 2 == 1
    assert (s+1) % 2 == 0
    return {
        "q": q, "order": [s, t], "points": points, "lines": lines,
        "apartments": apartments, "apartments_through_line_r": r,
        "alpha": alpha, "beta": beta,
        "gram_mod2": "HH^T = N^T N = A_line",
        "protected_dimension": "rho(q)=rank_2(N^T N)",
        "apartment_radical_dimension": "h(q)-rho(q), h(q)=rank_2(H)",
        "rank_bounds": "rho(q) <= h(q) <= lines-1",
    }


def main() -> int:
    c4506 = json.loads((ROOT / "data/PART_W33_PASS4506_Q53_APARTMENT_PROTECTED_BRIDGE.json").read_text())
    q3 = c4506["GQ_3_9"]
    assert q3["points"] == 112 and q3["lines"] == 280 and q3["apartments"] == 102060
    assert q3["rank_H"] == 279 and q3["rank_NtN"] == 70
    assert q3["apartment_radical_dimension"] == 209

    examples = [q5q_row(q) for q in (3, 7, 11, 19)]
    assert examples[0]["points"] == 112
    assert examples[0]["lines"] == 280
    assert examples[0]["apartments"] == 102060

    out = {
        "pass": 4530,
        "family": "Q(5,q)=GQ(q,q^2), q congruent 3 mod 4",
        "symbolic_counts": {
            "points": "(q+1)(q^3+1)",
            "lines": "(q^2+1)(q^3+1)",
            "apartments_through_line": "q^6(q+1)/2",
            "apartments": "(q^2+1)(q^3+1) q^6(q+1)/8",
        },
        "general_GQ_gram": {
            "r": "(s+1)s^2t^2/2",
            "alpha": "s^2t",
            "beta": "s(s+1)/2",
            "identity": "HH^T=(r-beta)I+(alpha-beta)A_*+beta J",
            "incidence": "N^T N=(s+1)I+A_*",
            "passing_criterion": "s congruent 3 mod4 and t odd",
        },
        "Q5q_theorem": {
            "gram_identity": "HH^T=N^T N over F2 for every q congruent 3 mod4",
            "protected_dimension": "rho(q)=rank_2(N^T N)",
            "apartment_radical_dimension": "h(q)-rho(q), where h(q)=rank_2(H)",
            "rank_bounds": "rho(q) <= h(q) <= (q^2+1)(q^3+1)-1",
        },
        "q3_anchor": {"h": 279, "rho": 70, "radical": 209, "protected": 70},
        "examples": examples,
        "theorem": "The W33 apartment/incidence bridge extends symbolically to the infinite Q(5,q) subfamily q=3 mod4; its protected dimension is exactly the binary incidence-Gram rank rho(q), with no q=3 extrapolation needed.",
        "open_rank_problem": "A closed formula for h(q) and rho(q) is not proved here. Classical generalized-quadrangle code literature is relevant, but this certificate does not substitute a remembered or guessed rank formula.",
        "boundary": "This is a symbolic incidence/Gram theorem. It neither enumerates apartments for q>3 nor identifies the protected dimension with a physical state count."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
