#!/usr/bin/env python3
"""Frobenius decoder for the Pass-409 S3 triality field."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_frobenius_triality_decoder.json"
x = sp.Symbol("x")
f = x**3 - x**2 - 53*x - 120
D = 94557
RAM = {3, 43, 733}


def factorization_type(p: int):
    pieces = sp.factor_list(f, modulus=p)[1]
    degs = []
    for g, e in pieces:
        degs.extend([sp.Poly(g, x, modulus=p).degree()] * e)
    return sorted(degs)
def frobenius_class_from_type(degs):
    if degs == [1, 1, 1]:
        return "identity"
    if degs == [3]:
        return "3-cycle"
    if degs == [1, 2]:
        return "transposition"
    raise AssertionError(f"unexpected unramified cubic type {degs}")


rows = []
counts = Counter()
parity_mismatches = []
for p in sp.primerange(2, 10000):
    if p in RAM:
        continue
    degs = factorization_type(p)
    cls = frobenius_class_from_type(degs)
    chi = int(sp.kronecker_symbol(D, p))
    expected_even = cls in {"identity", "3-cycle"}
    if (chi == 1) != expected_even:
        parity_mismatches.append(p)
    counts[cls] += 1
    if p < 200:
        rows.append({"p": p, "chi_D": chi, "degrees": degs, "frobenius": cls})

assert not parity_mismatches
assert counts == Counter({"transposition": 629, "3-cycle": 394, "identity": 203})
total = sum(counts.values())
densities = {k: counts[k] / total for k in ["identity", "3-cycle", "transposition"]}
chebotarev = {"identity": 1/6, "3-cycle": 1/3, "transposition": 1/2}

# The two-stage class-field decoder:
# chi_D=-1 forces an odd Frobenius (a transposition).
# chi_D=+1 puts Frobenius in Gal(N/F)=C3.  Artin=0 gives identity;
# either nonzero C3 class gives a 3-cycle.  Choosing +1 versus -1 in C3
# requires an orientation of the unique order-three class field and is not
# visible from the cubic factorization type alone.
out = {
    "schema": "w33.20260924.frobenius_triality_decoder.v1",
    "status": "PASS_FROBENIUS_TRIALITY_DECODER",
    "field": {
        "polynomial": str(f),
        "discriminant": D,
        "galois_group": "S3",
        "quadratic_resolvent": "Q(sqrt(94557))",
        "hilbert_3_class_layer": "C3",
    },
    "decoder": {
        "quadratic_bit": "Kronecker symbol (D/p)",
        "rule_minus_1": "transposition; cubic factorization 1+2",
        "rule_plus_1_artin_0": "identity; cubic factorization 1+1+1",
        "rule_plus_1_artin_nonzero": "3-cycle; cubic factorization 3",
        "orientation_boundary": "factorization sees the two nontrivial C3 elements only as one conjugacy class",
    },
    "prime_census_below_10000": {
        "unramified_prime_count": total,
        "counts": dict(counts),
        "densities": densities,
        "chebotarev_target": chebotarev,
        "parity_mismatch_count": len(parity_mismatches),
    },
    "examples_below_200": rows,
    "boundary": (
        "This is an exact arithmetic Frobenius/class-field decoder.  The C2/C3 "
        "register language is group-theoretic only; it is not evidence for a "
        "physical bit/qutrit register without an additional implemented map."
    ),
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": out["status"], "counts": dict(counts),
                  "mismatches": len(parity_mismatches)}, indent=2))
