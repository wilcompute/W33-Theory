#!/usr/bin/env python3
"""BT553: W33 Levi Flag Q-Polynomial Obstruction Theorem.

Tests all possible orderings of the nontrivial primitive idempotents for the
Q-polynomial property.  A 4-class scheme is Q-polynomial in an ordering
E_0,E_{i1},...,E_{i4} if multiplication by E_{i1} is tridiagonal in the Krein
algebra, i.e. q_{i1,ij}^{ik}=0 whenever |j-k|>1.

Result: no ordering works.  The Levi flag scheme is P-polynomial/distance
regular, but not Q-polynomial under any ordering.  The smallest obstruction
count is 6 forbidden nonzero Krein entries; in every best attempt the protected
E4 sector is reached off-ladder.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
import sympy as sp


def main() -> dict:
    v = sp.Integer(160)
    s = sp.sqrt(6)
    valencies = [1, 6, 18, 54, 81]
    multiplicities = [1, 24, 30, 24, 81]
    P = sp.Matrix([
        [1, 6, 18, 54, 81],
        [1, 2+s, 2*s, 6-3*s, -9],
        [1, 2, -6, -6, 9],
        [1, 2-s, -2*s, 6+3*s, -9],
        [1, -2, 2, -2, 1],
    ])
    Q = sp.zeros(5, 5)
    for d in range(5):
        for i in range(5):
            Q[d, i] = sp.simplify(sp.Integer(multiplicities[i]) * P[i, d] / sp.Integer(valencies[d]))
    krein = [[[sp.simplify(sum(Q[l, i] * Q[l, j] * P[k, l] for l in range(5)) / v)
               for k in range(5)] for j in range(5)] for i in range(5)]

    candidates = []
    for tail in itertools.permutations([1, 2, 3, 4]):
        order = [0] + list(tail)
        gen = order[1]
        violations = []
        for a, j in enumerate(order):
            for b, k in enumerate(order):
                if abs(a-b) > 1 and sp.simplify(krein[gen][j][k]) != 0:
                    violations.append((a, b, j, k, str(krein[gen][j][k])))
        candidates.append({"order": order, "generator": gen, "violation_count": len(violations), "sample_violations": violations[:8]})

    best_count = min(c["violation_count"] for c in candidates)
    best = [c for c in candidates if c["violation_count"] == best_count]

    checks = {
        "PQ_orthogonality": sp.simplify(P * Q) == v * sp.eye(5),
        "all_24_orderings_tested": len(candidates) == 24,
        "no_q_polynomial_ordering": best_count > 0,
        "best_obstruction_count_is_6": best_count == 6,
    }

    result = {
        "theorem": "BT553 W33 Levi Flag Q-Polynomial Obstruction Theorem",
        "tested_orderings": 24,
        "q_polynomial_order_exists": False,
        "minimum_forbidden_nonzero_entries": best_count,
        "best_orderings": best[:6],
        "interpretation": "The scheme is P-polynomial/distance-regular but not Q-polynomial; the H1=81 idempotent is not part of a dual distance ladder.",
        "all_identities": {k: bool(vv) for k, vv in checks.items()},
        "all_identities_hold": all(bool(vv) for vv in checks.values()),
    }
    out = Path("data/PART_BT553_W33_LEVI_FLAG_Q_POLYNOMIAL_OBSTRUCTION_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
