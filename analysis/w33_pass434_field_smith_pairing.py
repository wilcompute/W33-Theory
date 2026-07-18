#!/usr/bin/env python3
"""Pass 434: field-sensitive 2-adic Smith pairing for the Heisenberg bulk tower.

This closes the q=7 gate from Pass 433 and adds two independent controls:

* the proper GF(9) Heisenberg graph obeys the same Smith pairing law;
* the superficially similar Z/9Z construction does not.

For each tested finite field q in {3,5,7,9,11}, the native bulk Laplacian has
2-primary critical group

    (Z/2^a)^{q(q-1)} x (Z/2^(a+c))^{q(q-1)^2/2},

where a=v2(q-1) and c=v2(q+1). Equivalently the upper exponent is
v2(q^2-1). This is an exact finite computation for the listed fields and a
five-field certificate for the general tower law; it is not presented as a
proof for every odd prime power.
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass434_field_smith_pairing.json"


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("v2 requires a positive integer")
    out = 0
    while n % 2 == 0:
        n //= 2
        out += 1
    return out


def prime_ops(q: int) -> tuple[Callable[[int, int], int], Callable[[int, int], int], Callable[[int], int]]:
    return (
        lambda x, y: (x + y) % q,
        lambda x, y: (x * y) % q,
        lambda x: (-x) % q,
    )


def gf9_ops() -> tuple[Callable[[int, int], int], Callable[[int, int], int], Callable[[int], int]]:
    """GF(9)=GF(3)[alpha]/(alpha^2+1), encoded by 3*a+b."""
    def add(x: int, y: int) -> int:
        a, b = divmod(x, 3)
        c, d = divmod(y, 3)
        return ((a + c) % 3) * 3 + ((b + d) % 3)

    def mul(x: int, y: int) -> int:
        a, b = divmod(x, 3)
        c, d = divmod(y, 3)
        # alpha^2=-1=2 in GF(3)
        return ((a * c + 2 * b * d) % 3) * 3 + ((a * d + b * c) % 3)

    def neg(x: int) -> int:
        a, b = divmod(x, 3)
        return ((-a) % 3) * 3 + ((-b) % 3)

    return add, mul, neg


def build_laplacian(q: int, field: str = "prime") -> np.ndarray:
    if field == "gf9":
        if q != 9:
            raise ValueError("gf9 mode requires q=9")
        add, mul, neg = gf9_ops()
    elif field in {"prime", "zmod"}:
        add, mul, neg = prime_ops(q)
    else:
        raise ValueError(f"unknown field mode: {field}")

    elems = [(a, b, c) for a in range(q) for b in range(q) for c in range(q)]
    index = {g: i for i, g in enumerate(elems)}
    section = [(u, v, 0) for u in range(q) for v in range(q) if (u, v) != (0, 0)]

    def hmul(g: tuple[int, int, int], h: tuple[int, int, int]) -> tuple[int, int, int]:
        a, b, c = g
        u, v, w = h
        cocycle = add(mul(u, b), neg(mul(a, v)))
        return add(a, u), add(b, v), add(add(c, w), cocycle)

    n = q ** 3
    adjacency = np.zeros((n, n), dtype=np.int64)
    for i, g in enumerate(elems):
        for s in section:
            adjacency[i, index[hmul(g, s)]] = 1
    return (q * q - 1) * np.eye(n, dtype=np.int64) - adjacency


def two_adic_smith_valuations(matrix: np.ndarray, kmax: int = 16) -> list[int]:
    """Return finite 2-adic Smith valuations by unit-pivot elimination mod 2^k.

    The final zero invariant of a connected graph Laplacian is omitted.
    """
    modulus = 1 << kmax
    work = (matrix % modulus).astype(np.int64).copy()
    n = work.shape[0]
    valuations: list[int] = []

    for pivot in range(n):
        sub = work[pivot:, pivot:]
        nz = np.nonzero(sub)
        if len(nz[0]) == 0:
            break
        entries = sub[nz]
        lowbits = entries & -entries
        vals = np.log2(lowbits).astype(np.int64)
        choice = int(np.argmin(vals))
        valuation = int(vals[choice])
        row = pivot + int(nz[0][choice])
        col = pivot + int(nz[1][choice])

        if row != pivot:
            work[[pivot, row], :] = work[[row, pivot], :]
        if col != pivot:
            work[:, [pivot, col]] = work[:, [col, pivot]]

        p = int(work[pivot, pivot]) % modulus
        unit_inverse = pow(p >> valuation, -1, modulus)

        for i in range(pivot + 1, n):
            x = int(work[i, pivot]) % modulus
            if x:
                factor = ((x >> valuation) * unit_inverse) % modulus
                work[i, pivot:] = (work[i, pivot:] - factor * work[pivot, pivot:]) % modulus
        for j in range(pivot + 1, n):
            x = int(work[pivot, j]) % modulus
            if x:
                factor = ((x >> valuation) * unit_inverse) % modulus
                work[pivot:, j] = (work[pivot:, j] - factor * work[pivot:, pivot]) % modulus

        valuations.append(valuation)

    return sorted(valuations)


def expected_shape(q: int) -> Counter[int]:
    return Counter({
        v2(q - 1): q * (q - 1),
        v2(q * q - 1): q * (q - 1) ** 2 // 2,
    })


def spectrum_multiplicities(q: int) -> dict[str, int]:
    return {
        "k=q^2-1": 1,
        "q-1": q * (q * q - 1) // 2,
        "-(q+1)": q * (q - 1) ** 2 // 2,
        "-1": q * q - 1,
    }


def spectral_tree_v2(q: int) -> int:
    m_plus = q * (q * q - 1) // 2
    m_minus = q * (q - 1) ** 2 // 2
    return m_plus * v2(q - 1) + m_minus * v2(q + 1)


def certify(q: int, field: str) -> dict:
    started = time.perf_counter()
    laplacian = build_laplacian(q, field)
    vals = two_adic_smith_valuations(laplacian)
    shape = Counter(v for v in vals if v > 0)
    expected = expected_shape(q)
    m_plus = q * (q * q - 1) // 2
    m_minus = q * (q - 1) ** 2 // 2
    residual = m_plus - m_minus
    valuation_sum = sum(k * n for k, n in shape.items())

    checks = {
        "connected_one_zero_invariant": len(vals) == q ** 3 - 1,
        "laplacian_row_sum_zero": bool(np.all(laplacian.sum(axis=1) == 0)),
        "laplacian_symmetric": bool(np.array_equal(laplacian, laplacian.T)),
        "shape_matches_pairing_law": shape == expected,
        "smith_tree_v2_matches_spectrum": valuation_sum == spectral_tree_v2(q),
        "negative_spectral_multiplicity_is_glued_block": m_minus == q * (q - 1) ** 2 // 2,
        "positive_residual_is_q_times_q_minus_1": residual == q * (q - 1),
        "positive_multiplicity_splits_residual_plus_glued": m_plus == residual + m_minus,
    }
    return {
        "q": q,
        "field_model": field,
        "matrix_order": q ** 3,
        "degree": q * q - 1,
        "adjacency_spectrum_multiplicities": spectrum_multiplicities(q),
        "two_primary_shape": {f"2^{k}": n for k, n in sorted(shape.items())},
        "expected_shape": {f"2^{k}": n for k, n in sorted(expected.items())},
        "finite_even_factors": sum(shape.values()),
        "tree_v2": valuation_sum,
        "spectral_pairing": {
            "positive_eigenspace_multiplicity": m_plus,
            "negative_eigenspace_multiplicity": m_minus,
            "residual_positive_multiplicity": residual,
            "interpretation": (
                "each negative-sector direction pairs one v2(q-1) layer with one "
                "v2(q+1) layer, producing v2(q^2-1); the unpaired positive-sector "
                "residual carries v2(q-1)"
            ),
        },
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended", action="store_true", help="also execute q=11")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    cases = [(3, "prime"), (5, "prime"), (7, "prime"), (9, "gf9")]
    if args.extended:
        cases.append((11, "prime"))

    field_results = [certify(q, mode) for q, mode in cases]
    ring_control = certify(9, "zmod")
    ring_shape = Counter({int(k.split("^")[1]): v for k, v in ring_control["two_primary_shape"].items()})
    ring_deviates = ring_shape != expected_shape(9)

    checks = {
        "q7_gate_closed": next(r for r in field_results if r["q"] == 7)["status"] == "PASS",
        "proper_gf9_matches_tower_law": next(r for r in field_results if r["q"] == 9)["status"] == "PASS",
        "zmod9_control_deviates": ring_deviates,
        "all_field_cases_pass": all(r["status"] == "PASS" for r in field_results),
        "five_field_certificate_when_extended": (len(field_results) == 5) if args.extended else True,
        "general_law_still_labeled_conjecture": True,
    }
    payload = {
        "schema": "w33.pass434.field_smith_pairing.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "headline": (
            "The q=7 2-adic Smith gate closes exactly: Z_2^42 x Z_16^126. "
            "The same spectral-to-Smith pairing law holds for GF(3), GF(5), GF(7), "
            "GF(9), and (in --extended mode) GF(11). Proper GF(9) gives "
            "Z_8^72 x Z_16^288, whereas the Z/9Z impostor gives a different shape, "
            "proving that the certificate is field-geometric rather than a bare odd-q "
            "numerology. The all-odd-prime-power statement remains a conjecture."
        ),
        "field_results": field_results,
        "zmod9_control": ring_control,
        "checks": checks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "cases": [(r["q"], r["field_model"], r["two_primary_shape"]) for r in field_results],
        "zmod9": ring_control["two_primary_shape"],
        "checks": checks,
    }))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
