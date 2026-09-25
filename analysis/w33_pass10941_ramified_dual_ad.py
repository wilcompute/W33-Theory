#!/usr/bin/env python3
"""Pass 10941 front 4: exact dual-number automatic-differentiation opcodes."""
from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10941_ramified_dual_ad.json"
PARENT = json.loads(
    (ROOT / "data/w33_pass409_cubic_ramification_audit.json").read_text()
)


def invmod(a: int, p: int) -> int:
    return pow(a % p, -1, p)


def mat_inv3(A, p):
    M = [[A[i][j] % p for j in range(3)] + [int(i == j) for j in range(3)] for i in range(3)]
    for c in range(3):
        k = next(i for i in range(c, 3) if M[i][c] % p)
        M[c], M[k] = M[k], M[c]
        z = invmod(M[c][c], p)
        M[c] = [(z * x) % p for x in M[c]]
        for i in range(3):
            if i == c:
                continue
            z = M[i][c] % p
            M[i] = [(a - z * b) % p for a, b in zip(M[i], M[c])]
    return [row[3:] for row in M]


def mv(A, v, p):
    return [sum(a * b for a, b in zip(row, v)) % p for row in A]


def coeff_mul(u, v, p):
    # theta^3 = theta^2 + 53 theta + 120.
    raw = [0] * 5
    for i, a in enumerate(u):
        for j, b in enumerate(v):
            raw[i + j] = (raw[i + j] + a * b) % p
    for d in (4, 3):
        a = raw[d] % p
        raw[d] = 0
        raw[d - 1] = (raw[d - 1] + a) % p
        raw[d - 2] = (raw[d - 2] + 53 * a) % p
        raw[d - 3] = (raw[d - 3] + 120 * a) % p
    return raw[:3]


def dadd(x, y, p):
    return tuple((a + b) % p for a, b in zip(x, y))


def dmul(x, y, p):
    a, da, c = x
    b, db, d = y
    return (a * b % p, (a * db + da * b) % p, c * d % p)


def dinv(x, p):
    a, da, c = x
    ai, ci = invmod(a, p), invmod(c, p)
    return (ai, (-da * ai * ai) % p, ci)


def poly_eval(coeffs, x, p):
    y = (0, 0, 0)
    for a in reversed(coeffs):
        y = dadd(dmul(y, x, p), (a % p, 0, a % p), p)
    return y


def scalar_poly(coeffs, x, p):
    y = 0
    for a in reversed(coeffs):
        y = (y * x + a) % p
    return y


def derivative_coeffs(coeffs):
    return [i * coeffs[i] for i in range(1, len(coeffs))]


rows = []
rng = random.Random(10941)
for parent in PARENT["ramified_reductions"]:
    p = parent["prime"]
    r = parent["double_root"]
    s = parent["simple_root"]
    transform = [
        [1, r, r * r],
        [0, 1, 2 * r],
        [1, s, s * s],
    ]
    transform = [[x % p for x in row] for row in transform]
    inverse = mat_inv3(transform, p)
    assert all(mv(transform, mv(inverse, [int(i == j) for i in range(3)], p), p)[k] == int(k == j)
               for j in range(3) for k in range(3))

    # Bilinearity reduces multiplicativity of the CRT/dual chart to nine basis products.
    product_checks = 0
    basis = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for u in basis:
        for v in basis:
            lhs = tuple(mv(transform, coeff_mul(u, v, p), p))
            rhs = dmul(tuple(mv(transform, u, p)), tuple(mv(transform, v, p)), p)
            assert lhs == rhs
            product_checks += 1

    polynomial_checks = 0
    chain_checks = 0
    inverse_checks = 0
    for _ in range(64):
        a, da, c = (rng.randrange(p) for _ in range(3))
        x = (a, da, c)
        coeffs = [rng.randrange(p) for _ in range(7)]
        got = poly_eval(coeffs, x, p)
        expected = (
            scalar_poly(coeffs, a, p),
            da * scalar_poly(derivative_coeffs(coeffs), a, p) % p,
            scalar_poly(coeffs, c, p),
        )
        assert got == expected
        polynomial_checks += 1

        qcoeffs = [rng.randrange(p) for _ in range(5)]
        qx = poly_eval(qcoeffs, x, p)
        composed = poly_eval(coeffs, qx, p)
        qa = scalar_poly(qcoeffs, a, p)
        qc = scalar_poly(qcoeffs, c, p)
        chain = (
            scalar_poly(coeffs, qa, p),
            da
            * scalar_poly(derivative_coeffs(qcoeffs), a, p)
            * scalar_poly(derivative_coeffs(coeffs), qa, p)
            % p,
            scalar_poly(coeffs, qc, p),
        )
        assert composed == chain
        chain_checks += 1

        if a and c:
            assert dmul(x, dinv(x, p), p) == (1, 0, 1)
            inverse_checks += 1

    # The stored epsilon is exactly the derivative-register basis vector.
    eps_coeff = parent["square_zero_epsilon_coefficients"]
    assert tuple(mv(transform, eps_coeff, p)) == (0, 1, 0)
    idem_coeff = parent["double_factor_idempotent_coefficients"]
    assert tuple(mv(transform, idem_coeff, p)) == (1, 0, 0)

    rows.append(
        {
            "prime": p,
            "double_root": r,
            "simple_root": s,
            "coefficient_to_dual_chart": transform,
            "dual_chart_to_coefficient": inverse,
            "chart_determinant": (s - r) ** 2 % p,
            "basis_product_checks": product_checks,
            "polynomial_AD_checks": polynomial_checks,
            "composition_chain_rule_checks": chain_checks,
            "unit_inverse_checks": inverse_checks,
            "epsilon_chart": [0, 1, 0],
            "double_factor_idempotent_chart": [1, 0, 0],
        }
    )

out = {
    "schema": "w33.pass10941.ramified_dual_ad.v1",
    "status": "PASS_RAMIFIED_DUAL_NUMBER_AUTODIFFERENTIATION_ABI",
    "register": {
        "word": "(value_at_double_root, tangent, value_at_simple_root)",
        "algebra": "F_p[epsilon]/epsilon^2 x F_p",
        "primes": [3, 43, 733],
    },
    "opcodes": {
        "DADD": "(a,da,c)+(b,db,d)=(a+b,da+db,c+d)",
        "DMUL": "(a,da,c)*(b,db,d)=(ab,a*db+da*b,cd)",
        "DINV": "(a,da,c)^-1=(a^-1,-da*a^-2,c^-1)",
        "DFMA": "DMUL followed by DADD",
        "DPOLY": "Horner evaluation returns (P(a),da*P'(a),P(c))",
        "DCOMPOSE": "tangent lane obeys the exact chain rule",
    },
    "prime_charts": rows,
    "class_field_router": {
        "unramified": "C2 Kronecker bit plus C3 Artin class route the three etale triality branches",
        "ramified": "the collided pair is replaced by value+tangent while the simple branch remains a scalar lane",
        "parents": [
            "analysis/w33_20260924_triality_class_field_closure.py",
            "analysis/w33_20260924_frobenius_triality_decoder.py",
        ],
    },
    "boundary": (
        "These are exact finite-field arithmetic opcodes. They implement first-order "
        "automatic differentiation in the ramified centroid algebra; they do not "
        "supply real-number gradients, analog hardware, or physical dynamics."
    ),
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": out["status"], "primes": [r["prime"] for r in rows]}, indent=2))
