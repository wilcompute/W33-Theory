#!/usr/bin/env python3
"""Pass 1158 v2: exact 1952-dimensional residual recovery.

The original Pass 1158 only factorized the dimension and proposed arithmetic
splits. Pass 1135 had already computed the full W(E6) character decomposition,
so this compatibility pass now reports that exact decomposition.
"""
from __future__ import annotations

import json
from pathlib import Path

KERNEL_TOTAL = 2195
STEINBERG_PACKET = 243
RESIDUAL = KERNEL_TOTAL - STEINBERG_PACKET

EXACT_RESIDUAL = {
    "1": (1, 13), "6": (6, 16), "15": (15, 5), "15a": (15, 4),
    "20": (20, 21), "24": (24, 2), "30": (30, 9), "60a": (60, 4),
    "64": (64, 10), "90": (90, 1),
}


def factorize(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def main() -> dict:
    dimension = sum(d * m for d, m in EXACT_RESIDUAL.values())
    commutant = sum(m * m for _, m in EXACT_RESIDUAL.values())
    assert RESIDUAL == 1952
    assert dimension == RESIDUAL
    assert commutant == 1109
    result = {
        "schema": "w33.pass1158.kernel_residual_1952.v2",
        "status": "PASS",
        "source_of_truth": "analysis/w33_pass1135_cubic_kernel_decomposition.py",
        "kernel_total": KERNEL_TOTAL,
        "steinberg_packet_dim": STEINBERG_PACKET,
        "residual_dim": RESIDUAL,
        "residual_factorization": factorize(RESIDUAL),
        "exact_residual_decomposition": {
            name: {"degree": d, "multiplicity": m}
            for name, (d, m) in EXACT_RESIDUAL.items()
        },
        "isotypic_species": len(EXACT_RESIDUAL),
        "commutant_dimension": commutant,
        "correction": "Dimension factorizations are not module decompositions; the exact character decomposition is already known.",
    }
    out = Path("data/KERNEL_RESIDUAL_1952_2026_07_27.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1158 v2 residual=1952 exact commutant=1109")
    return result


if __name__ == "__main__":
    main()
