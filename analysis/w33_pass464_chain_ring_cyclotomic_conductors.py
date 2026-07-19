#!/usr/bin/env python3
"""Pass 464: finite-chain-ring central-character covariance and conductor radicals.

For R=Z/p^nZ, the central Weyl block indexed by t obeys
sigma_a(B_t)=B_{at} for every unit a, while inverse closure gives
B_{-t}=B_t^*.  The valuation of t simultaneously determines the additive
character conductor, the radical of the twisted alternating form, and the
ramified cyclotomic coefficient order.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass464_chain_ring_cyclotomic_conductors.json"


def vp(x: int, p: int, n: int) -> int:
    if x == 0:
        return n
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def units(modulus: int) -> list[int]:
    return [a for a in range(1, modulus) if math.gcd(a, modulus) == 1]


def inverse_pairs(modulus: int) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    vectors = [(x, y) for x in range(modulus) for y in range(modulus) if (x, y) != (0, 0)]
    out = []
    used = set()
    for v in vectors:
        nv = (-v[0] % modulus, -v[1] % modulus)
        key = tuple(sorted((v, nv)))
        if key not in used:
            used.add(key)
            out.append(key)
    return out


def deterministic_section(modulus: int, seed: int) -> dict[tuple[int, int], int]:
    rng = random.Random(seed)
    out: dict[tuple[int, int], int] = {}
    for (v, nv) in inverse_pairs(modulus):
        c = rng.randrange(modulus)
        out[v] = c
        out[nv] = -c % modulus
    return out


def exponent_block(modulus: int, section: dict[tuple[int, int], int], t: int) -> list[list[list[int]]]:
    """Exact m by m Weyl block, each entry a count vector in Z[C_m]."""
    half = pow(2, -1, modulus)
    block = [[[0 for _ in range(modulus)] for _ in range(modulus)] for _ in range(modulus)]
    for (x, y), z in section.items():
        for s in range(modulus):
            target = (s + x) % modulus
            phase = (z + y * s + half * x * y) % modulus
            block[target][s][t * phase % modulus] += 1
    return block


def galois_on_block(block: list[list[list[int]]], a: int) -> list[list[list[int]]]:
    m = len(block)
    out = [[[0 for _ in range(m)] for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for e, count in enumerate(block[i][j]):
                out[i][j][a * e % m] += count
    return out


def conjugate_block(block: list[list[list[int]]]) -> list[list[list[int]]]:
    m = len(block)
    out = [[[0 for _ in range(m)] for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for e, count in enumerate(block[i][j]):
                out[i][j][-e % m] += count
    return out


def adjoint_block(block: list[list[list[int]]]) -> list[list[list[int]]]:
    m = len(block)
    out = [[[0 for _ in range(m)] for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for e, count in enumerate(block[j][i]):
                out[i][j][-e % m] += count
    return out


def transpose_block(block: list[list[list[int]]]) -> list[list[list[int]]]:
    m = len(block)
    return [[list(block[j][i]) for j in range(m)] for i in range(m)]


def character_orbits(p: int, n: int) -> list[list[int]]:
    m = p**n
    U = units(m)
    unseen = set(range(1, m))
    orbits = []
    while unseen:
        t = min(unseen)
        orb = sorted({a * t % m for a in U})
        unseen.difference_update(orb)
        orbits.append(orb)
    return orbits


def radical_size_bruteforce(p: int, n: int, t: int) -> int:
    m = p**n
    count = 0
    for x, y in itertools.product(range(m), repeat=2):
        ok = True
        for u, v in ((1, 0), (0, 1)):
            if t * (x * v - y * u) % m:
                ok = False
                break
        count += ok
    return count


def cyclotomic_shift_data(p: int, conductor_power: int) -> dict:
    x, u = sp.symbols("x u")
    modulus = p**conductor_power
    phi = sp.cyclotomic_poly(modulus, x)
    shifted = sp.Poly(sp.expand(phi.subs(x, 1 + u)), u, domain=sp.ZZ)
    coeffs = [int(shifted.nth(i)) for i in range(shifted.degree() + 1)]
    eisenstein = (
        coeffs[-1] == 1
        and coeffs[0] % p == 0
        and coeffs[0] % (p * p) != 0
        and all(c % p == 0 for c in coeffs[1:-1])
    )
    return {
        "conductor": modulus,
        "phi": int(sp.totient(modulus)),
        "cyclotomic_polynomial": str(phi),
        "shifted_at_one_coefficients_low_to_high": coeffs,
        "eisenstein_at_p": eisenstein,
        "local_ramification_index": int(sp.totient(modulus)),
        "maximal_real_degree": int(sp.totient(modulus) // 2),
    }


def witness(p: int, n: int, seed: int) -> dict:
    m = p**n
    section = deterministic_section(m, seed)
    U = units(m)
    blocks = {t: exponent_block(m, section, t) for t in range(m)}
    covariance = all(galois_on_block(blocks[t], a) == blocks[a * t % m] for t in range(m) for a in U)
    hermitian = all(adjoint_block(blocks[t]) == blocks[t] for t in range(m))
    minus_is_conjugate = all(conjugate_block(blocks[t]) == blocks[-t % m] for t in range(m))
    minus_is_transpose = all(transpose_block(blocks[t]) == blocks[-t % m] for t in range(m))

    strata = []
    for r in range(n):
        ts = [t for t in range(1, m) if vp(t, p, n) == r]
        conductor_power = n - r
        conductor = p**conductor_power
        expected_radical = p ** (2 * r)
        observed_radicals = sorted({radical_size_bruteforce(p, n, t) for t in ts})
        strata.append({
            "valuation": r,
            "characters": len(ts),
            "representative": min(ts),
            "additive_character_order": conductor,
            "center_kernel_size": p**r,
            "alternating_radical_size": expected_radical,
            "observed_radical_sizes": observed_radicals,
            "unit_orbit_size": len(ts),
            "real_galois_orbit_size": len(ts) // 2,
            "coefficient_order": f"Z[zeta_{conductor}]",
            "real_characteristic_coefficient_field": f"Q(zeta_{conductor})^+",
        })

    orbits = character_orbits(p, n)
    orbit_valuations = [sorted({vp(t, p, n) for t in orbit}) for orbit in orbits]
    shifts = [cyclotomic_shift_data(p, k) for k in range(1, n + 1)]
    return {
        "ring": f"Z/{m}Z",
        "p": p,
        "length": n,
        "modulus": m,
        "unit_group_order": len(U),
        "nonzero_character_orbits": orbits,
        "orbit_valuations": orbit_valuations,
        "conductor_strata": strata,
        "cyclotomic_local_orders": shifts,
        "exact_galois_covariance": covariance,
        "exact_each_block_hermitian": hermitian,
        "exact_minus_character_is_conjugate": minus_is_conjugate,
        "exact_minus_character_is_transpose": minus_is_transpose,
        "section_seed": seed,
    }


def build_payload() -> dict:
    z9 = witness(3, 2, 464)
    z25 = witness(5, 2, 465)
    checks = {
        "z9_two_nonzero_conductor_orbits": len(z9["nonzero_character_orbits"]) == 2,
        "z25_two_nonzero_conductor_orbits": len(z25["nonzero_character_orbits"]) == 2,
        "orbits_are_exactly_valuation_strata": all(len(v) == 1 for v in z9["orbit_valuations"] + z25["orbit_valuations"]),
        "z9_stratum_sizes_2_6": [x["characters"] for x in z9["conductor_strata"]] == [6, 2],
        "z25_stratum_sizes_20_4": [x["characters"] for x in z25["conductor_strata"]] == [20, 4],
        "radical_formula_p_2r": all(
            row["observed_radical_sizes"] == [row["alternating_radical_size"]]
            for w in (z9, z25) for row in w["conductor_strata"]
        ),
        "exact_covariance_all_units": z9["exact_galois_covariance"] and z25["exact_galois_covariance"],
        "inverse_closure_makes_each_block_hermitian": z9["exact_each_block_hermitian"] and z25["exact_each_block_hermitian"],
        "minus_character_is_conjugate_transpose_pair": all(w["exact_minus_character_is_conjugate"] and w["exact_minus_character_is_transpose"] for w in (z9, z25)),
        "all_local_cyclotomic_shifts_eisenstein": all(
            row["eisenstein_at_p"] for w in (z9, z25) for row in w["cyclotomic_local_orders"]
        ),
        "primitive_z9_ramification_index_six": z9["cyclotomic_local_orders"][-1]["local_ramification_index"] == 6,
        "primitive_z25_ramification_index_twenty": z25["cyclotomic_local_orders"][-1]["local_ramification_index"] == 20,
    }
    return {
        "schema": "w33.pass464.chain_ring_cyclotomic_conductors.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "For R=Z/p^nZ and an inverse-closed central section, the exact central Weyl blocks satisfy "
            "sigma_a(B_t)=B_{at} for every a in R^*. Inverse closure makes every B_t Hermitian, while B_{-t} is both the entrywise conjugate and the transpose of B_t. If v_p(t)=r<n, then the "
            "additive character has conductor p^(n-r), its alternating bicharacter has radical p^(2r), "
            "and its entries lie in Z[zeta_{p^(n-r)}]. The shifted cyclotomic polynomial "
            "Phi_{p^(n-r)}(1+u) is Eisenstein, so the local coefficient order is totally ramified with "
            "index phi(p^(n-r)); characteristic coefficients fixed by star lie in the corresponding "
            "maximal real subfield."
        ),
        "z9_witness": z9,
        "z25_witness": z25,
        "boundary": (
            "This closes central-character covariance, conductor radicals, and ramified coefficient orders. "
            "It does not assert that characteristic-primary Smith modules split integrally into Fourier blocks; "
            "the non-unimodular Fourier transform is exactly the coupling studied in Pass 466."
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
            raise SystemExit("Pass 464 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
