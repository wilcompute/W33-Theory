#!/usr/bin/env python3
"""Pass 271: the no-drop phenomenon at the level of ELEMENTARY DIVISORS.

Pass 266 established the mechanism: (q^2+1)(q+2)/2 is the characteristic-0 rank
of the incidence matrix N for every q, and the F2 rank equals it exactly when
2 does not divide q.  This witness descends to the Smith normal form, where the
statement becomes sharp and checkable.

THEOREM 1 (rigorous, all integer matrices).  rank_F2(M) <= rank_Q(M).
    A nonzero k x k minor mod 2 lifts to a nonzero minor over Q, so any k
    independent rows mod 2 are independent over Q.  Hence the "drop"
    delta = rank_Q - rank_F2 is always >= 0 -- which is why delta was never
    negative in Passes 250/256.

THEOREM 2 (the SNF dictionary).  If N has Smith normal form with elementary
divisors d_1 | d_2 | ... | d_r (r = rank_Q), then
    rank_F2(N) = #{ i : d_i is ODD },
    delta      = #{ i : d_i is EVEN }.
So "no 2-modular drop" is exactly "every elementary divisor is odd".

VERIFICATION.  We compute the integer Smith normal form of N for q = 2,3,4,5 and
count odd vs even elementary divisors:
    q = 2 : 10 nonzero, 0 even  -> drop 0
    q = 3 : 25 nonzero, 0 even  -> drop 0   (odd q, cross characteristic)
    q = 4 : 51 nonzero, 1 even  -> drop 1   (even q, defining characteristic)
    q = 5 : 91 nonzero, 0 even  -> drop 0   (odd q)
This is the mechanism of Pass 266 seen directly in the invariant factors.

HONEST SCOPE: Theorem 1 and the SNF dictionary are proved; the general claim
"all elementary divisors are odd for every odd q" is VERIFIED at q = 3,5 here and
at q = 3,5,7,9,11,13,17 at the level of ranks (Passes 238/260/262/266), but is not
proved for all odd q.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import (
    f2_rank,
    incidence_rows,
    isotropic_lines,
    pg3_points,
)
from analysis.w33_pass232_even_q_sister_tower import (
    GF,
    isotropic_lines_gf,
    pg3_points_gf,
)

OUT = ROOT / "data" / "w33_pass271_no_drop_elementary_divisors.json"


def build_rows(q, even):
    if even:
        gf = GF({2: 1, 4: 2, 8: 3}[q])
        pts = pg3_points_gf(gf)
        lines = isotropic_lines_gf(gf, pts)
    else:
        pts = pg3_points(q)
        lines = isotropic_lines(pts, q)
    return len(pts), incidence_rows(lines, len(pts))


def main():
    checks = {}

    # ---- THEOREM 1: rank_F2 <= rank_Q, verified on random integer matrices
    import numpy as np
    rng = np.random.default_rng(4)
    ok = True
    for _ in range(300):
        M = rng.integers(0, 3, (6, 6))
        rq = int(np.linalg.matrix_rank(M.astype(float)))
        rows = [tuple(int(x) % 2 for x in M[i]) for i in range(6)]
        r2 = f2_rank(rows)
        if r2 > rq:
            ok = False
            break
    checks["rank_F2_never_exceeds_rank_Q"] = ok
    checks["so_delta_is_always_nonnegative"] = ok

    # ---- THEOREM 2 + verification via Smith normal form
    table = {}
    for q, even in ((2, True), (3, False), (4, True), (5, False)):
        t0 = time.time()
        n, rows = build_rows(q, even)
        M = sp.Matrix([[int(x) for x in r] for r in rows])
        snf = smith_normal_form(M)
        divs = [int(snf[i, i]) for i in range(min(snf.shape))]
        nonzero = [d for d in divs if d != 0]
        odd = [d for d in nonzero if d % 2 == 1]
        even_d = [d for d in nonzero if d % 2 == 0]
        r2 = f2_rank(rows)
        rq = len(nonzero)
        table[str(q)] = {
            "n": n, "even_q": even,
            "rank_Q_from_snf": rq,
            "num_odd_elementary_divisors": len(odd),
            "num_even_elementary_divisors": len(even_d),
            "rank_F2": r2,
            "drop": rq - r2,
            "snf_dictionary_holds": len(odd) == r2,
            "even_divisor_values": sorted(set(even_d)),
            "seconds": round(time.time() - t0, 1),
        }
        checks[f"q{q}_snf_dictionary"] = len(odd) == r2
        checks[f"q{q}_drop_equals_num_even_divisors"] = (rq - r2) == len(even_d)
        checks[f"q{q}_rankQ_is_char0_law"] = rq == (q * q + 1) * (q + 2) // 2

    # ---- the dichotomy in the invariant factors
    checks["odd_q_all_divisors_odd"] = all(
        table[str(q)]["num_even_elementary_divisors"] == 0 for q in (3, 5))
    checks["q2_all_divisors_odd"] = table["2"]["num_even_elementary_divisors"] == 0
    checks["q4_has_one_even_divisor"] = table["4"]["num_even_elementary_divisors"] == 1
    checks["q4_drop_is_1"] = table["4"]["drop"] == 1

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass271.no_drop_elementary_divisors.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem_1": (
            "rank_F2(M) <= rank_Q(M) for every integer matrix M, because a "
            "nonzero minor mod 2 lifts to a nonzero minor over Q. Hence the drop "
            "delta = rank_Q - rank_F2 is always >= 0 -- proving a priori that "
            "the F2 rank can never exceed the characteristic-0 law of Pass 266."
        ),
        "theorem_2_snf_dictionary": (
            "With elementary divisors d_1 | ... | d_r of N: rank_F2 = #{d_i odd} "
            "and delta = #{d_i even}. So 'no 2-modular drop' is exactly 'all "
            "invariant factors are odd'."
        ),
        "verification": table,
        "reading": (
            "The Pass 266 mechanism is visible directly in the invariant "
            "factors. For odd q (and for q=2) every elementary divisor of the "
            "incidence matrix is ODD, so reduction mod 2 loses nothing and "
            "rank_F2 = rank_Q = (q^2+1)(q+2)/2. At q=4 exactly one invariant "
            "factor is EVEN, and the rank drops by exactly 1 -- matching "
            "delta(4) = 1. The 'delta' of Passes 250/256 is therefore a count of "
            "even invariant factors, and the odd/even dichotomy is the statement "
            "that defining characteristic (2 | q) forces even invariant factors "
            "while cross characteristic (2 does not divide q) does not."
        ),
        "honest_scope": (
            "Theorem 1 and the SNF dictionary are proved. The general statement "
            "'every invariant factor is odd for every odd q' is verified here at "
            "q = 3,5 (and at rank level for q = 3,5,7,9,11,13,17 in Passes "
            "238/260/262/266) but is not proved for all odd q."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
