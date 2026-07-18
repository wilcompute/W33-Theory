#!/usr/bin/env python3
"""Pass 410: first genuine prime-power Smith closure for the Heisenberg bulk."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import sympy as sp

from w33_pass410_414_common import (
    FiniteField,
    certificate,
    heisenberg_laplacian,
    padic_smith_exact_valuations,
    write_json,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass410_prime_power_smith.json"


def tree_order(q: int) -> int:
    plus = q * (q * q - 1) // 2
    minus = q * (q - 1) * (q - 1) // 2
    return q ** (q**3 + q**2 - 5) * (q - 1) ** plus * (q + 1) ** minus


def valuation_order(exact: list[int]) -> int:
    return sum(level * count for level, count in enumerate(exact))


def exact_counts(exact: list[int], p: int) -> dict[str, int]:
    return {str(p**level): count for level, count in enumerate(exact) if level and count}


def q9_full_primary(characteristic: dict[str, int]) -> dict[str, dict[str, int]]:
    # Semisimple sectors at ell != 3 plus the proven odd-q two-adic pairing law.
    return {
        "2": {"8": 72, "16": 288},
        "3": characteristic,
        "5": {"5": 288},
    }


def order_from_primary(primary: dict[str, dict[str, int]]) -> int:
    out = 1
    for factors in primary.values():
        for order, multiplicity in factors.items():
            out *= int(order) ** int(multiplicity)
    return out


def instance(field: FiniteField, max_exp: int) -> dict:
    lap = heisenberg_laplacian(field)
    exact = padic_smith_exact_valuations(lap, field.p, max_exp)
    q = field.q
    return {
        "p": field.p,
        "extension_degree": field.f,
        "q": q,
        "vertices": q**3,
        "reduced_laplacian_size": q**3 - 1,
        "exact_p_adic_valuation_counts_including_units": {str(i): n for i, n in enumerate(exact) if n},
        "p_primary_elementary_divisors": exact_counts(exact, field.p),
        "p_adic_tree_order_valuation": valuation_order(exact),
        "unit_invariant_factors": exact[0],
    }


def build_payload() -> dict:
    gf3 = FiniteField(3, (0, 1))
    gf5 = FiniteField(5, (0, 1))
    gf9 = FiniteField(3, (1, 0, 1))  # u^2+1 over F_3

    instances = {
        "3": instance(gf3, 5),
        "5": instance(gf5, 5),
        "9": instance(gf9, 8),
    }

    expected = {
        "3": [10, 8, 1, 7],
        "5": [35, 56, 10, 23],
        "9": [100, 128, 292, 92, 37, 0, 79],
    }
    for q, sequence in expected.items():
        observed = instances[q]["exact_p_adic_valuation_counts_including_units"]
        dense = [int(observed.get(str(i), 0)) for i in range(len(sequence))]
        instances[q]["matches_frozen_sequence"] = dense == sequence

    q9_characteristic = instances["9"]["p_primary_elementary_divisors"]
    full = q9_full_primary(q9_characteristic)
    q9_order = tree_order(9)
    q9_factor = {str(k): int(v) for k, v in sorted(sp.factorint(q9_order).items())}

    checks = {
        "gf3_valid": gf3.validate(),
        "gf5_valid": gf5.validate(),
        "gf9_valid": gf9.validate(),
        "q3_recovers_pass405": instances["3"]["matches_frozen_sequence"],
        "q5_recovers_pass405": instances["5"]["matches_frozen_sequence"],
        "q9_exact_sequence": instances["9"]["matches_frozen_sequence"],
        "q9_characteristic_valuation_1610": instances["9"]["p_adic_tree_order_valuation"] == 1610,
        "q9_full_primary_reconstructs_tree_order": order_from_primary(full) == q9_order,
        "q9_tree_factorization": q9_factor == {"2": 1368, "3": 1610, "5": 288},
        "q9_no_3_to_the_5_factors": "243" not in q9_characteristic,
        "q9_top_characteristic_layer_has_q2_minus_2": q9_characteristic.get("729") == 79,
    }

    payload = {
        "schema": "w33.pass410.prime_power_smith.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": {
            "closed_instance": "complete Smith primary decomposition for the first non-prime field q=9",
            "algorithmic_theorem": "for every explicitly represented odd prime power, unit-pivot elimination over Z/p^K computes exact characteristic-primary elementary divisors without integer SNF coefficient explosion",
            "remaining_boundary": "a closed multiplicity formula for every extension degree f is not asserted",
        },
        "algorithm": {
            "field_model": "polynomial-basis F_p[u]/(m(u))",
            "graph": "vertices (x,y,z) in F_q^3; adjacency z'-z=y*x'-x*y'",
            "bockstein_recurrence": "extract every unit pivot over Z/(p^K), delete its row and column, divide the residual p-divisible block by p, and repeat",
            "exactness": "each stage is Smith-equivalent over Z_p; the number of pivots at stage k is the number of invariant factors of exact p-adic valuation k",
        },
        "instances": instances,
        "q9_complete_critical_group_primary_decomposition": full,
        "q9_closed_form": "(Z/8)^72 + (Z/16)^288 + (Z/3)^128 + (Z/9)^292 + (Z/27)^92 + (Z/81)^37 + (Z/729)^79 + (Z/5)^288",
        "q9_tree_order": {
            "prime_factorization": q9_factor,
            "decimal_digits": len(str(q9_order)),
            "sha256": hashlib.sha256(str(q9_order).encode()).hexdigest(),
        },
        "new_structural_observations": {
            "unit_count_jump": "q=9 has 100 p-adic unit invariant factors, not the naive normalization count 25",
            "missing_middle_layer": "the characteristic-primary Smith form contains no 3^5 elementary divisors",
            "top_layer": "all q^2-2=79 trivial-central classes appear at 3^(3f)=3^6",
        },
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 410 certificate drift")
    else:
        write_json(args.output, payload)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
