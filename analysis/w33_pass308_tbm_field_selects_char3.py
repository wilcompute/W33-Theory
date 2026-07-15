#!/usr/bin/env python3
"""Pass 308: the TBM field selects CHARACTERISTIC 3 (odd Frobenius degree) -- not q=3.

Pass 303 found the substrate's two forced fields compose to the tribimaximal
field: the clock's Q(sqrt2) and the machine's Q(sqrt6) generate Q(sqrt2,sqrt3),
which is exactly where TBM's entries live.  The obvious question -- is that
special to q=3, or would any rung do? -- decides whether it is a selection
principle or a coincidence.  This witness settles it, and the answer is weaker
than hoped but real.

THE ARITHMETIC.  The machine at rung q has Levi field Q(sqrt 2q) (Pass 298), so
the compositum with the clock is
        Q(sqrt2, sqrt(2q)) = Q(sqrt2, sqrt q),
since sqrt q = sqrt(2q)/sqrt2.  This equals the TBM field Q(sqrt2, sqrt3)
exactly when the squarefree part of q is 3, i.e. when

        q = 3^t  with t ODD    (q = 3, 27, 243, ...).

RESULT.  Every other rung misses:
    q = 2,8   -> Q(sqrt2)          (machine field rational)
    q = 4,16  -> Q(sqrt2)
    q = 9,81  -> Q(sqrt2)          (even Frobenius degree kills it)
    q = 5,125 -> Q(sqrt2, sqrt5)
    q = 7     -> Q(sqrt2, sqrt7)
    q = 11    -> Q(sqrt2, sqrt11)
So the TBM field selects CHARACTERISTIC 3 with odd Frobenius degree.  It does NOT
select q = 3 uniquely -- q = 27 works too -- but q = 3 is the smallest such rung,
and combined with the two genuine uniqueness results (Pass 225: the half-spinor
is one generation only at q=3; Pass 227: the shadow rank fits an exceptional
group only at q=3) the substrate's q = 3 is picked out.

HONEST WEIGHT.  This is a third selection argument for characteristic 3, weaker
than 225/227 because it is a family (3^odd) rather than a point, and because a
field containment is a coarse instrument.  It is recorded as what it is.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass308_tbm_field_selects_char3.json"


def sf(n):
    o = 1
    for p, e in sp.factorint(int(n)).items():
        if e % 2:
            o *= p
    return int(o)


def main():
    checks = {}

    # the compositum identity: Q(sqrt2, sqrt(2q)) = Q(sqrt2, sqrt q)
    checks["compositum_identity"] = sp.simplify(
        sp.sqrt(6) / sp.sqrt(2) - sp.sqrt(3)) == 0

    table, hits = {}, []
    for p in sp.primerange(2, 13):
        for t in range(1, 5):
            q = p ** t
            if q > 300:
                break
            machine = sf(2 * q)
            comp = sf(q)
            is_tbm = (comp == 3)
            if is_tbm:
                hits.append(q)
            table[str(q)] = {"p": p, "t": t,
                             "machine_field": f"Q(sqrt{machine})" if machine != 1 else "Q",
                             "compositum": f"Q(sqrt2, sqrt{comp})" if comp != 1 else "Q(sqrt2)",
                             "is_TBM_field": bool(is_tbm)}

    checks["q3_gives_TBM"] = 3 in hits
    checks["q27_also_gives_TBM"] = 27 in hits
    checks["hits_are_odd_powers_of_3"] = hits == [3, 27]
    checks["q9_does_NOT"] = not table["9"]["is_TBM_field"]
    checks["q5_does_NOT"] = not table["5"]["is_TBM_field"]
    checks["q7_does_NOT"] = not table["7"]["is_TBM_field"]
    checks["even_q_does_NOT"] = not any(table[str(q)]["is_TBM_field"]
                                        for q in (2, 4, 8, 16))
    # the rule: sf(3^t) = 3 iff t is odd
    checks["sf_3_to_t_is_3_iff_t_odd"] = all(
        (sf(3 ** t) == 3) == (t % 2 == 1) for t in range(1, 8))
    checks["not_unique_to_q3"] = len(hits) > 1

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass308.tbm_field_selects_char3.v1",
        "status": "PASS" if all_pass else "FAIL",
        "the_arithmetic": (
            "The machine at rung q has Levi field Q(sqrt 2q) (Pass 298), so the "
            "compositum with the clock's Q(sqrt2) is Q(sqrt2, sqrt(2q)) = "
            "Q(sqrt2, sqrt q), since sqrt q = sqrt(2q)/sqrt2. That equals the TBM "
            "field Q(sqrt2, sqrt3) exactly when the squarefree part of q is 3, "
            "i.e. when q = 3^t with t ODD."
        ),
        "per_rung": table,
        "rungs_giving_the_TBM_field": hits,
        "VERDICT": (
            "The TBM field selects CHARACTERISTIC 3 with ODD Frobenius degree "
            "(q = 3, 27, 243, ...). It does NOT select q = 3 uniquely -- q = 27 "
            "works too, and q = 9 does not (even degree kills it). Every other "
            "characteristic misses: q=5 gives Q(sqrt2,sqrt5), q=7 gives "
            "Q(sqrt2,sqrt7), and all even q collapse to Q(sqrt2)."
        ),
        "honest_weight": (
            "A third selection argument for characteristic 3, but WEAKER than the "
            "two genuine uniqueness results it joins: Pass 225 (the half-spinor "
            "equals one generation only at q=3 -- an integer equation with a "
            "unique solution) and Pass 227 (the shadow rank fits an exceptional "
            "group only at q=3). This one selects a FAMILY (3^odd) rather than a "
            "point, and a field containment is a coarse instrument. Combined, "
            "q=3 is picked out -- but this pass alone would not do it."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
