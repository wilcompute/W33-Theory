#!/usr/bin/env python3
"""BT552: W33 Levi Flag Krein / Schur Closure Theorem.

Computes the Krein parameters for the 4-class distance association scheme on
160 W33 Levi flags.  BT551 identified the protected primitive idempotent

    E4=(1/160)(81A0-27A1+9A2-3A3+A4)=(1/160)CC^T.

BT552 proves the Schur-product closure law.  The protected idempotent is
spectral/Hodge closed, but not closed alone under Schur square:

    E4 o E4 = (1/160) sum_k q_44^k E_k,

with all five q_44^k nonzero.  Thus the H1=81 sector is a primitive spectral
sector, but its pointwise square repopulates the full Bose--Mesner dual stack.
"""

from __future__ import annotations

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
    q44 = krein[4][4]
    support_q44 = [i for i, x in enumerate(q44) if sp.simplify(x) != 0]

    # Standard Krein identities: q_{0j}^k = delta_{jk}, q_{ij}^0 = delta_{ij} m_i.
    checks = {
        "PQ_orthogonality": sp.simplify(P * Q) == v * sp.eye(5),
        "QP_orthogonality": sp.simplify(Q * P) == v * sp.eye(5),
        "q0_identity": all(krein[0][j][k] == (1 if j == k else 0) for j in range(5) for k in range(5)),
        "qij0_identity": all(krein[i][j][0] == (multiplicities[i] if i == j else 0) for i in range(5) for j in range(5)),
        "q44_all_five_nonzero": support_q44 == [0, 1, 2, 3, 4],
        "q44_total": sp.simplify(sum(q44)) == sp.Rational(1307, 5),
    }

    result = {
        "theorem": "BT552 W33 Levi Flag Krein / Schur Closure Theorem",
        "scheme": {"vertices": 160, "classes": 4, "multiplicities": multiplicities},
        "protected_idempotent": "E4=(1/160)(81A0-27A1+9A2-3A3+A4)",
        "q44_coefficients": [str(sp.simplify(x)) for x in q44],
        "q44_support": support_q44,
        "schur_square_law": "E4 o E4 = (1/160) sum_k q_44^k E_k, with all five primitive sectors present",
        "interpretation": "H1=81 is a primitive spectral/Hodge sector, but its pointwise square repopulates the full dual Bose--Mesner stack.",
        "all_identities": {k: bool(vv) for k, vv in checks.items()},
        "all_identities_hold": all(bool(vv) for vv in checks.values()),
    }
    out = Path("data/PART_BT552_W33_LEVI_FLAG_KREIN_SCHUR_CLOSURE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
