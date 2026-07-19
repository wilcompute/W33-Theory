#!/usr/bin/env python3
"""Pass 463: exact central-character sheet exchange behind the genuine q=5 collision.

The Pass-456 pair is not related by a group automorphism or by the natural
switching/trade families exhausted in Pass 460.  Its rational cospectrality is
instead produced in the faithful Wedderburn component: the square and
nonsquare central-character sheets exchange their two conjugate Q(sqrt(5))
quintic factors.

All trace calculations below are exact in Z[zeta_5], represented in the basis
1,z,z^2,z^3 with Phi_5(z)=1+z+z^2+z^3+z^4=0.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass463_q5_central_sheet_exchange.json"
Q = 5
PAIR_A = (0, 3, 4, 1, 1, 0, 2, 0, 1, 1, 2, 2)
PAIR_B = (0, 2, 3, 0, 2, 2, 4, 1, 0, 3, 3, 2)


def section_pairs() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    vecs = [(a, b) for a in range(Q) for b in range(Q) if (a, b) != (0, 0)]
    out = []
    used = set()
    for v in vecs:
        nv = (-v[0] % Q, -v[1] % Q)
        key = tuple(sorted((v, nv)))
        if key not in used:
            used.add(key)
            out.append(key)
    return out


PAIRS = section_pairs()


def full_section(offsets: tuple[int, ...]) -> dict[tuple[int, int], int]:
    f: dict[tuple[int, int], int] = {}
    for (v, nv), c in zip(PAIRS, offsets):
        f[v] = c
        f[nv] = -c % Q
    return f


def phase_matrices(offsets: tuple[int, ...], t: int) -> list[np.ndarray]:
    """Return B_t=sum_e zeta^e M_e on the 25-dimensional central Fourier sheet."""
    base = [(a, b) for a in range(Q) for b in range(Q)]
    idx = {v: i for i, v in enumerate(base)}
    mats = [np.zeros((Q * Q, Q * Q), dtype=np.int64) for _ in range(Q)]
    for a, b in base:
        i = idx[(a, b)]
        for (x, y), z in full_section(offsets).items():
            j = idx[((a + x) % Q, (b + y) % Q)]
            exponent = t * (z - a * y + x * b) % Q
            mats[exponent][i, j] += 1
    return mats


def poly_matrix_multiply(left: list[np.ndarray], right: list[np.ndarray]) -> list[np.ndarray]:
    out = [np.zeros_like(left[0]) for _ in range(Q)]
    for i in range(Q):
        for j in range(Q):
            out[(i + j) % Q] += left[i] @ right[j]
    return out


def canonical_cyclotomic(coeff5: list[int] | tuple[int, ...]) -> tuple[int, int, int, int]:
    """Quotient Z[C5] by Phi_5, eliminating z^4."""
    return tuple(int(coeff5[i] - coeff5[4]) for i in range(4))


def trace_moments(offsets: tuple[int, ...], t: int, order: int = 5) -> list[tuple[int, int, int, int]]:
    block = phase_matrices(offsets, t)
    power = [np.zeros_like(block[0]) for _ in range(Q)]
    power[0] = np.eye(Q * Q, dtype=np.int64)
    moments = []
    for _ in range(order):
        power = poly_matrix_multiply(power, block)
        moments.append(canonical_cyclotomic([int(np.trace(power[e])) for e in range(Q)]))
    return moments


Cyclo = tuple[int, int, int, int]
ZERO: Cyclo = (0, 0, 0, 0)
ONE: Cyclo = (1, 0, 0, 0)


def cadd(a: Cyclo, b: Cyclo) -> Cyclo:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def csub(a: Cyclo, b: Cyclo) -> Cyclo:
    return tuple(x - y for x, y in zip(a, b))  # type: ignore[return-value]


def cscale(a: Cyclo, n: int) -> Cyclo:
    return tuple(n * x for x in a)  # type: ignore[return-value]


def cmul(a: Cyclo, b: Cyclo) -> Cyclo:
    aa = list(a) + [0]
    bb = list(b) + [0]
    cc = [0] * 5
    for i, x in enumerate(aa):
        for j, y in enumerate(bb):
            cc[(i + j) % 5] += x * y
    return canonical_cyclotomic(cc)


def cdiv_exact(a: Cyclo, n: int) -> Cyclo:
    if not all(x % n == 0 for x in a):
        raise AssertionError((a, n))
    return tuple(x // n for x in a)  # type: ignore[return-value]


def quintic_coefficients(moments25: list[Cyclo]) -> list[Cyclo]:
    """Newton identities after removing the regular multiplicity five."""
    power_sums = [ZERO] + [cdiv_exact(x, 5) for x in moments25]
    elementary = [ONE]
    for k in range(1, 6):
        total = ZERO
        for i in range(1, k + 1):
            term = cmul(elementary[k - i], power_sums[i])
            total = cadd(total, term) if (i - 1) % 2 == 0 else csub(total, term)
        elementary.append(cdiv_exact(total, k))
    return [ONE] + [cscale(elementary[k], -1 if k % 2 else 1) for k in range(1, 6)]


def sqrt5_form(coefficients: list[Cyclo]) -> list[str]:
    """Render the special real coefficients; all observed coefficients use 1 and z^2+z^3."""
    r = sp.sqrt(5)
    z2z3 = -(1 + r) / 2
    rendered = []
    for a0, a1, a2, a3 in coefficients:
        if a1 != 0 or a2 != a3:
            raise AssertionError((a0, a1, a2, a3))
        rendered.append(str(sp.expand(a0 + a2 * z2z3)))
    return rendered


def polynomial_from_rendered(coefficients: list[str]) -> sp.Expr:
    x = sp.Symbol("x")
    return sp.expand(sum(sp.sympify(c) * x ** (5 - i) for i, c in enumerate(coefficients)))


def affine_orbit_contains(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    """Repeat the exact Pass-456 12,000-element affine orbit firewall."""
    f = full_section(left)
    matrices = []
    for a, b, c, d in itertools.product(range(Q), repeat=4):
        det = (a * d - b * c) % Q
        if det:
            matrices.append((a, b, c, d, det))

    def inv(M: tuple[int, int, int, int, int]) -> tuple[int, int, int, int]:
        a, b, c, d, det = M
        u = pow(det, -1, Q)
        return d * u % Q, -b * u % Q, -c * u % Q, a * u % Q

    def mv(M: tuple[int, int, int, int], v: tuple[int, int]) -> tuple[int, int]:
        a, b, c, d = M
        return (a * v[0] + b * v[1]) % Q, (c * v[0] + d * v[1]) % Q

    for M in matrices:
        Mi = inv(M)
        det = M[4]
        for r, s in itertools.product(range(Q), repeat=2):
            values = []
            for v, _nv in PAIRS:
                pre = mv(Mi, v)
                values.append((det * f[pre] + r * v[0] + s * v[1]) % Q)
            if tuple(values) == right:
                return True
    return False


def build_payload() -> dict:
    a_mom = {str(t): trace_moments(PAIR_A, t) for t in range(1, 5)}
    b_mom = {str(t): trace_moments(PAIR_B, t) for t in range(1, 5)}

    p_coeff = quintic_coefficients(a_mom["1"])
    q_coeff = quintic_coefficients(a_mom["2"])
    p_rendered = sqrt5_form(p_coeff)
    q_rendered = sqrt5_form(q_coeff)
    P = polynomial_from_rendered(p_rendered)
    Qpoly = polynomial_from_rendered(q_rendered)
    x, r = sp.symbols("x r")
    P_r = x**5 - 60*x**3 - (15 + 25*r)*x**2/2 + (310 + 25*r)*x - 54 + 25*r
    Q_r = x**5 - 60*x**3 - (15 - 25*r)*x**2/2 + (310 - 25*r)*x - 54 - 25*r
    norm = sp.Poly(sp.expand(P_r * Q_r), r, domain=sp.QQ[x]).rem(
        sp.Poly(r**2 - 5, r, domain=sp.QQ[x])
    ).as_expr()
    expected_norm = (
        x**10 - 120*x**8 - 15*x**7 + 4220*x**6 + 792*x**5
        - 37925*x**4 + 4955*x**3 + 96910*x**2 - 39730*x - 209
    )

    swapped_equal = (
        a_mom["1"] == b_mom["2"]
        and a_mom["4"] == b_mom["3"]
        and a_mom["2"] == b_mom["1"]
        and a_mom["3"] == b_mom["4"]
    )
    unswapped_distinguished = a_mom["1"][2] != b_mom["1"][2]
    checks = {
        "twelve_inverse_pairs": len(PAIRS) == 12,
        "genuine_pair_still_affine_inequivalent": not affine_orbit_contains(PAIR_A, PAIR_B),
        "exact_square_nonsquare_sheet_exchange": swapped_equal,
        "unswapped_sheets_separate_at_trace_cube": unswapped_distinguished,
        "regular_multiplicity_five_divides_moments": all(
            all(v % 5 == 0 for v in moment)
            for table in (a_mom, b_mom)
            for moments in table.values()
            for moment in moments
        ),
        "quintics_are_sqrt5_conjugates": sp.expand(Q_r - P_r.xreplace({r: -r})) == 0,
        "exact_norm_is_pass456_degree10_factor": sp.expand(norm - expected_norm) == 0,
        "rendered_quintics_match_closed_forms": sp.expand(P - P_r.subs(r, sp.sqrt(5))) == 0 and sp.expand(Qpoly - Q_r.subs(r, sp.sqrt(5))) == 0,
    }
    return {
        "schema": "w33.pass463.q5.central_sheet_exchange.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "collision_offsets": {"A": list(PAIR_A), "B": list(PAIR_B)},
        "central_character_classes": {
            "square": [1, 4],
            "nonsquare": [2, 3],
            "exchange_multiplier": 2,
        },
        "exact_trace_moments_25d_basis_1_z_z2_z3": {"A": a_mom, "B": b_mom},
        "faithful_quintic_factors": {
            "P_plus_sqrt5": str(P_r),
            "P_minus_sqrt5": str(Q_r),
            "norm_to_Q": str(expected_norm),
            "A_assignment": {"square": "P_plus_sqrt5", "nonsquare": "P_minus_sqrt5"},
            "B_assignment": {"square": "P_minus_sqrt5", "nonsquare": "P_plus_sqrt5"},
        },
        "theorem": (
            "The genuine q=5 Smith-identical collision is a faithful Wedderburn-sheet exchange. "
            "Graph A assigns the two Galois-conjugate Q(sqrt(5)) quintics P+ and P- to the square and "
            "nonsquare central characters respectively; graph B reverses that assignment. Their rational "
            "norm P+P- is unchanged, so the full spectrum is unchanged. The exchange is not induced by "
            "an affine automorphism of the Heisenberg section and therefore need not preserve the marked "
            "Cayley relation or local common-neighbor profile."
        ),
        "boundary": (
            "This identifies an exact semisimple adjacency-algebra mechanism. It is deliberately not "
            "rebranded as a graph isomorphism, a Godsil-McKay switch, or a local edge trade."
        ),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Pass 463 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
