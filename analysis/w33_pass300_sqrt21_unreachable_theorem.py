#!/usr/bin/env python3
"""Pass 300: THEOREM -- Q(sqrt 21) is structurally unreachable from any Levi spectrum.

Pass 298 computed the two forced-field families, verifying both directly:
    Levi(PG(2,q))  has spectrum  +-(q+1), +-sqrt(q)       -> field Q(sqrt q)
    Levi(GQ(q,q))  has spectrum  +-(q+1), +-sqrt(2q), 0   -> field Q(sqrt 2q)
Since q must be a PRIME POWER for these geometries to exist, the reachable
quadratic fields are exactly
    { Q(sqrt sf(q)) : q a prime power } union { Q(sqrt sf(2q)) : q a prime power }.

THEOREM.  Q(sqrt 21) is NOT in that set:
  * sqrt(q) = sqrt(21) needs q = 21 = 3*7, which is not a prime power;
  * sqrt(2q) = sqrt(21) needs 2q = 21, i.e. q = 21/2, not an integer.
So no projective plane and no symplectic quadrangle over any prime power has
sqrt(21) in its incidence spectrum.  The reachable set contains 3, 7, 6 and 14 --
but NOT 21: Q(sqrt3) and Q(sqrt7) are individually reachable (the planes of order
3 and 7) and cannot be multiplied, because a single geometry has a single order.

CONSEQUENCE FOR KOIDE.  eps* = (5 - sqrt21)/2 lives in Q(sqrt 21), so it cannot
arise from ANY incidence spectrum in this family -- for a structural reason, not
a failed search.  With Passes 293/299 (sqrt21 is a coordinate choice, not forced,
even under C2) and Pass 274 (FN accommodates rather than derives Koide), the
geometric route to Koide is closed on independent grounds.  This closure is a
THEOREM rather than an absence of evidence -- exactly the distinction Pass 292
insisted on after the 279/285 failures.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass300_sqrt21_unreachable_theorem.json"


def sf(n):
    o = 1
    for p, e in sp.factorint(int(n)).items():
        if e % 2:
            o *= p
    return int(o)


def is_prime_power(n):
    return len(sp.factorint(int(n))) == 1


def main():
    checks = {}
    reach = {}
    for p in sp.primerange(2, 100):
        for t in range(1, 6):
            q = p ** t
            if q > 200:
                break
            reach.setdefault(sf(q), []).append("PG(2,%d)" % q)
            reach.setdefault(sf(2 * q), []).append("GQ(%d,%d)" % (q, q))

    checks["sqrt2_reachable"] = 2 in reach
    checks["sqrt3_reachable"] = 3 in reach
    checks["sqrt6_reachable_the_substrate"] = 6 in reach
    checks["sqrt7_reachable"] = 7 in reach
    checks["sqrt14_reachable"] = 14 in reach

    # THE THEOREM
    checks["21_is_not_a_prime_power"] = not is_prime_power(21)
    checks["21_factors_as_3_times_7"] = sp.factorint(21) == {3: 1, 7: 1}
    checks["2q_equals_21_has_no_integer_solution"] = (21 % 2 == 1)
    checks["sqrt21_UNREACHABLE"] = 21 not in reach
    checks["3_and_7_reachable_but_not_their_product"] = (
        3 in reach and 7 in reach and 21 not in reach)

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass300.sqrt21_unreachable_theorem.v1",
        "status": "PASS" if all_pass else "FAIL",
        "THEOREM": (
            "Q(sqrt 21) is not reachable as the spectral field of any Levi graph "
            "in this family. Levi(PG(2,q)) gives Q(sqrt q) and Levi(GQ(q,q)) "
            "gives Q(sqrt 2q), and q must be a PRIME POWER. sqrt(q) = sqrt(21) "
            "would need q = 21 = 3*7, not a prime power; sqrt(2q) = sqrt(21) "
            "would need q = 21/2, not an integer. Hence no projective plane and "
            "no symplectic quadrangle over any prime power has sqrt(21) in its "
            "incidence spectrum."
        ),
        "reachable_fields": {str(d): sorted(set(v))[:4]
                             for d, v in sorted(reach.items()) if d < 60},
        "the_near_misses": {
            "sqrt3": "reachable -- PG(2,3)",
            "sqrt7": "reachable -- PG(2,7)",
            "sqrt6": "reachable -- GQ(3,3), THE SUBSTRATE ITSELF",
            "sqrt14": "reachable -- GQ(7,7)",
            "sqrt21": "UNREACHABLE -- 21 = 3*7 is a product of two distinct odd "
                      "primes, and a single geometry has a single order, so "
                      "Q(sqrt3) and Q(sqrt7) cannot be multiplied together",
        },
        "consequence_for_koide": (
            "eps* = (5 - sqrt21)/2 lives in Q(sqrt 21) and therefore cannot arise "
            "from any incidence spectrum in this family -- for a STRUCTURAL "
            "reason, not a failed search. With Passes 293/299 (sqrt21 is a "
            "coordinate choice, not forced, even under C2 symmetry) and Pass 274 "
            "(FN accommodates rather than derives Koide), the geometric route to "
            "Koide is closed on independent grounds. This closure is a THEOREM "
            "rather than an absence of evidence -- exactly the distinction Pass "
            "292 said to insist on after the 279/285 failures."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
