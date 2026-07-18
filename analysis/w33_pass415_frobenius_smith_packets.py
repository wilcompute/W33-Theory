#!/usr/bin/env python3
"""Pass 415: Frobenius packets and normalized Smith theory for q=p^f.

This pass proves the part of the prime-power characteristic-primary analysis
that is visible before integral conductor gluing.  It also identifies the
exact conductor *index* for every odd prime power and freezes the first
extension-field correction at q=9 from Pass 410.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import reduce
import hashlib
import json
from math import gcd
from pathlib import Path

import sympy as sp

from w33_pass410_414_common import FiniteField, certificate, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass415_frobenius_smith_packets.json"
PASS410 = ROOT / "data" / "w33_pass410_prime_power_smith.json"


def convolution_power(base: list[int], power: int) -> list[int]:
    result = [1]
    for _ in range(power):
        nxt = [0] * (len(result) + len(base) - 1)
        for i, a in enumerate(result):
            for j, b in enumerate(base):
                nxt[i + j] += a * b
        result = nxt
    return result


def projective_line_representatives(field: FiniteField) -> tuple[int, ...]:
    """Canonical representatives of F_q^*/F_p^*."""
    unseen = set(range(1, field.q))
    reps: list[int] = []
    base_scalars = range(1, field.p)
    while unseen:
        a = min(unseen)
        line = {field.mul(c, a) for c in base_scalars}
        reps.append(min(line))
        unseen.difference_update(line)
    return tuple(sorted(reps))


def frobenius_projective_orbits(field: FiniteField) -> list[tuple[int, ...]]:
    reps = projective_line_representatives(field)
    rep_of: dict[int, int] = {}
    for rep in reps:
        for c in range(1, field.p):
            rep_of[field.mul(c, rep)] = rep
    unseen = set(reps)
    orbits: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        orbit: list[int] = []
        current = start
        while current not in orbit:
            orbit.append(current)
            current = rep_of[field.pow(current, field.p)]
        if current != start:
            raise AssertionError("Frobenius packet did not close at its start")
        unseen.difference_update(orbit)
        orbits.append(tuple(orbit))
    return sorted(orbits, key=lambda orbit: (len(orbit), orbit))


def mobius_orbit_census(p: int, f: int) -> dict[int, int]:
    """Number of Frobenius orbits of exact length d on F_q^*/F_p^*."""
    q = p**f
    n = (q - 1) // (p - 1)
    fixed = {d: gcd(n, p**d - 1) for d in sp.divisors(f)}
    exact_points: dict[int, int] = {}
    orbit_counts: dict[int, int] = {}
    for d in sorted(sp.divisors(f)):
        exact = sum(int(sp.mobius(d // e)) * fixed[e] for e in sp.divisors(d))
        exact_points[d] = exact
        if exact % d:
            raise AssertionError("exact Frobenius period count is not divisible by period")
        orbit_counts[d] = exact // d
    if sum(d * count for d, count in orbit_counts.items()) != n:
        raise AssertionError("Frobenius orbit census does not cover projective lines")
    return orbit_counts


def pi_exponent_distribution(p: int, f: int) -> dict[int, int]:
    """SNF pi-exponents of the additive symplectic Fourier block.

    Choosing an F_p-basis of F_q identifies the q x q additive character table
    with F_p^{tensor f}; the symplectic block is therefore F_p^{tensor 2f}.
    """
    coeffs = convolution_power([1] * p, 2 * f)
    return {i: value for i, value in enumerate(coeffs) if value}


def normalized_cyclotomic_counts(p: int, f: int) -> dict[int, int]:
    """Z_p elementary-divisor counts before conductor gluing.

    One R=Z_p[zeta_p] packet represents p-1 cyclotomic characters.  There are
    (q-1)/(p-1) projective central packets.  R/(pi^s) contributes r copies of
    p^(a+1) and p-1-r copies of p^a when s=a(p-1)+r.
    """
    q = p**f
    packets = (q - 1) // (p - 1)
    ramification = p - 1
    counts: Counter[int] = Counter()
    for exponent, multiplicity in pi_exponent_distribution(p, f).items():
        a, r = divmod(exponent, ramification)
        if a:
            counts[a] += packets * multiplicity * (ramification - r)
        if r:
            counts[a + 1] += packets * multiplicity * r
    return dict(sorted(counts.items()))


def normalized_with_trivial_sector(p: int, f: int) -> dict[int, int]:
    q = p**f
    counts = Counter(normalized_cyclotomic_counts(p, f))
    counts[2 * f] += q * q - 2
    return dict(sorted(counts.items()))


def p_order(counts: dict[int, int]) -> int:
    return sum(exponent * multiplicity for exponent, multiplicity in counts.items())


def exact_tree_p_valuation(p: int, f: int) -> int:
    q = p**f
    return f * (q**3 + q**2 - 5)


def normalized_tree_p_valuation(p: int, f: int) -> int:
    q = p**f
    return f * (q**3 + q**2 - 4)


def dense_counts(record: dict[str, int]) -> dict[int, int]:
    return {int(round(sp.log(int(order), 3))): int(mult) for order, mult in record.items()}


def instance(p: int, modulus: tuple[int, ...]) -> dict:
    field = FiniteField(p, modulus)
    f = field.f
    q = field.q
    orbits = frobenius_projective_orbits(field)
    observed = Counter(map(len, orbits))
    predicted = mobius_orbit_census(p, f)
    pi_counts = pi_exponent_distribution(p, f)
    cyclotomic = normalized_cyclotomic_counts(p, f)
    normalized = normalized_with_trivial_sector(p, f)
    return {
        "p": p,
        "f": f,
        "q": q,
        "projective_central_packets": (q - 1) // (p - 1),
        "frobenius_orbits": [list(orbit) for orbit in orbits],
        "frobenius_orbit_length_counts": {str(k): v for k, v in sorted(observed.items())},
        "mobius_predicted_orbit_length_counts": {str(k): v for k, v in sorted(predicted.items())},
        "pi_exponent_distribution": {str(k): v for k, v in pi_counts.items()},
        "normalized_cyclotomic_zp_counts": {str(p**k): v for k, v in cyclotomic.items()},
        "normalized_plus_trivial_zp_counts": {str(p**k): v for k, v in normalized.items()},
        "normalized_p_order_valuation": p_order(normalized),
        "critical_group_p_order_valuation": exact_tree_p_valuation(p, f),
        "conductor_index_p_valuation": p_order(normalized) - exact_tree_p_valuation(p, f),
        "checks": {
            "field_valid": field.validate(),
            "orbit_census_matches_mobius": dict(observed) == predicted,
            "fourier_distribution_has_q_squared_entries": sum(pi_counts.values()) == q * q,
            "normalized_order_matches_closed_formula": p_order(normalized) == normalized_tree_p_valuation(p, f),
            "conductor_index_equals_f": p_order(normalized) - exact_tree_p_valuation(p, f) == f,
        },
    }


def build_payload() -> dict:
    q3 = instance(3, (0, 1))
    q5 = instance(5, (0, 1))
    q9 = instance(3, (1, 0, 1))
    q25 = instance(5, (2, 0, 1))  # u^2+2 is irreducible over F_5
    q27 = instance(3, (1, 2, 0, 1))  # u^3+2u+1 has no F_3 root

    pass410 = json.loads(PASS410.read_text())
    exact_q9 = {
        int(round(sp.log(int(order), 3))): int(mult)
        for order, mult in pass410["instances"]["9"]["p_primary_elementary_divisors"].items()
    }
    normalized_q9 = {
        int(round(sp.log(int(order), 3))): int(mult)
        for order, mult in q9["normalized_plus_trivial_zp_counts"].items()
    }
    all_exponents = sorted(set(normalized_q9) | set(exact_q9))
    q9_correction = {k: exact_q9.get(k, 0) - normalized_q9.get(k, 0) for k in all_exponents}

    checks: dict[str, bool] = {}
    for label, record in {"q3": q3, "q5": q5, "q9": q9, "q25": q25, "q27": q27}.items():
        for name, value in record["checks"].items():
            checks[f"{label}_{name}"] = bool(value)

    checks.update({
        "q9_frobenius_packets_are_1_1_2": q9["frobenius_orbit_length_counts"] == {"1": 2, "2": 1},
        "q25_frobenius_packets_are_1_1_2_2": q25["frobenius_orbit_length_counts"] == {"1": 2, "2": 2},
        "q27_frobenius_packets_are_1_plus_four_3_cycles": q27["frobenius_orbit_length_counts"] == {"1": 1, "3": 4},
        "q9_exact_top_layer_q_squared_minus_2": exact_q9.get(6) == 79,
        "q9_missing_p_to_5_layer": exact_q9.get(5, 0) == 0,
        "q9_correction_preserves_index_defect_two": (
            p_order(normalized_q9) - p_order(exact_q9) == 2
        ),
    })

    p, f = sp.symbols("p f", integer=True, positive=True)
    q = sp.symbols("q", integer=True, positive=True)
    symbolic = {
        "mean_pi_exponent": "f*(p-1)",
        "cyclotomic_order": "f*q^2*(q-1)",
        "trivial_sector_order": "2*f*(q^2-2)",
        "normalized_total_order": "f*(q^3+q^2-4)",
        "critical_tree_order": "f*(q^3+q^2-5)",
        "conductor_index": "p^f=q",
    }

    payload = {
        "schema": "w33.pass415.frobenius_smith_packets.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": {
            "central_packet_space": "nonzero additive characters modulo Gal(Q_p(zeta_p)/Q_p) are the projective lines F_q^*/F_p^*",
            "frobenius_action": "sigma([a])=[a^p] on the cyclic group of order (q-1)/(p-1)",
            "fixed_packet_count": "Fix(sigma^d)=gcd((q-1)/(p-1), p^d-1)",
            "exact_orbit_count": "O_d=(1/d) sum_{e|d} mu(d/e) gcd((q-1)/(p-1),p^e-1)",
            "normalized_fourier_block": "over R=Z_p[zeta_p], every projective central packet has pi-Smith polynomial (1+x+...+x^(p-1))^(2f)",
            "conductor_index": "the normalization plus trivial-central lattice exceeds the integral critical lattice by p-adic order f, hence conductor index p^f=q",
        },
        "proof_ledger": {
            "tensor_descent": "an F_p-basis of F_q identifies its additive character table with F_p^(tensor f); the symplectic two-coordinate block is F_p^(tensor 2f)",
            "packet_descent": "cyclotomic Galois scales nonzero characters by F_p^*, leaving (q-1)/(p-1) projective packets; arithmetic Frobenius permutes those packets",
            "order_identity": "packet Fourier order f*q^2*(q-1) plus trivial order 2f(q^2-2) equals f(q^3+q^2-4), one factor q above the matrix-tree p-order",
            "integral_boundary": "the theorem fixes the normalization, Frobenius packets, and total conductor index; a closed all-f formula for how the conductor redistributes individual p^k factors is not asserted",
        },
        "symbolic_order_identities": symbolic,
        "instances": {str(record["q"]): record for record in (q3, q5, q9, q25, q27)},
        "q9_integral_conductor_correction": {
            "normalized_exponent_counts": {str(k): v for k, v in normalized_q9.items()},
            "exact_exponent_counts": {str(k): v for k, v in exact_q9.items()},
            "exact_minus_normalized": {str(k): v for k, v in q9_correction.items()},
            "interpretation": "the f=2 conductor removes 75 generators, shifts the q^2-2 trivial classes from p^(2f) to p^(3f), creates no p^5 layer, and has total index p^f=9",
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
            raise SystemExit("Pass 415 certificate drift")
    else:
        write_json(args.output, payload)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
