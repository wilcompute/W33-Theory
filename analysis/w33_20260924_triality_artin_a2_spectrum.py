#!/usr/bin/env python3
"""Artin/Hecke spectral realization of the Pass-409 triality field.

The standard 2D Artin representation of the S3 normal closure is realized by
the exact integral A2 Weyl matrices already used by BT943.  This turns the
Frobenius decoder into a matrix-valued local-factor compiler.
"""
from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_triality_artin_a2_spectrum.json"
D = 94557
BAD = (3, 43, 733)
x, T = sp.symbols("x T")
f = x**3 - x**2 - 53*x - 120
S1 = sp.Matrix([[-1, 1], [0, 1]])
S2 = sp.Matrix([[1, 0], [1, -1]])
R = S1 * S2
I2 = sp.eye(2)

assert S1**2 == I2
assert R**3 == I2
assert S1 * R * S1 == R.inv()

A2_GRAM = sp.Matrix([[2, -1], [-1, 2]])
for M in (S1, S2, R):
    assert M.T * A2_GRAM * M == A2_GRAM

CLASS_MATRIX = {
    "identity": I2,
    "transposition": S1,
    "3-cycle": R,
}
CLASS_SIZE = {"identity": 1, "transposition": 3, "3-cycle": 2}
def characteristic_factor(M: sp.Matrix) -> list[int]:
    poly = sp.Poly(sp.expand((I2 - T * M).det()), T)
    return [int(poly.nth(i)) for i in range(poly.degree() + 1)]


LOCAL_FACTORS = {name: characteristic_factor(M) for name, M in CLASS_MATRIX.items()}
assert LOCAL_FACTORS == {
    "identity": [1, -2, 1],
    "transposition": [1, 0, -1],
    "3-cycle": [1, 1, 1],
}

CHARACTER = {name: int(M.trace()) for name, M in CLASS_MATRIX.items()}
DETERMINANT = {name: int(M.det()) for name, M in CLASS_MATRIX.items()}
assert CHARACTER == {"identity": 2, "transposition": 0, "3-cycle": -1}
assert DETERMINANT == {"identity": 1, "transposition": -1, "3-cycle": 1}
@lru_cache(maxsize=None)
def direct_linear_root_count(p: int) -> int:
    return sum(1 for a in range(p) if (a**3 - a**2 - 53*a - 120) % p == 0)


def frobenius_from_root_count(root_count: int) -> tuple[str, list[int]]:
    # At p not dividing the squarefree discriminant, the cubic is separable.
    if root_count == 3:
        return "identity", [1, 1, 1]
    if root_count == 1:
        return "transposition", [1, 2]
    if root_count == 0:
        return "3-cycle", [3]
    raise AssertionError(root_count)


prime_rows = []
counts = {name: 0 for name in CLASS_MATRIX}
for p in sp.primerange(2, 10000):
    if p in BAD:
        continue
    linear_roots = direct_linear_root_count(p)
    cls, degs = frobenius_from_root_count(linear_roots)
    M = CLASS_MATRIX[cls]
    chi = int(sp.kronecker_symbol(D, p))
    a_p = CHARACTER[cls]
    assert int(M.det()) == chi
    assert a_p == linear_roots - 1
    counts[cls] += 1
    if p < 250:
        prime_rows.append({
            "p": p,
            "factorization_degrees": degs,
            "frobenius_class": cls,
            "a_p": a_p,
            "quadratic_character": chi,
            "A2_matrix": [[int(z) for z in row] for row in M.tolist()],
            "local_factor": LOCAL_FACTORS[cls],
        })
assert counts == {"identity": 203, "transposition": 629, "3-cycle": 394}

# Character moments are dimensions of invariant tensors in rho^{tensor n}.
moments = {}
for n in range(1, 13):
    num = sum(CLASS_SIZE[c] * CHARACTER[c] ** n for c in CLASS_MATRIX)
    assert num % 6 == 0
    moments[str(n)] = num // 6

# At the three bad primes the inertia group is a reflection.  The standard
# A2 representation has a one-dimensional invariant line, so the local Artin
# factor has degree one and the tame conductor exponent is one.
ram = json.loads((ROOT / "data/w33_pass409_cubic_ramification_audit.json").read_text())
bad_rows = []
for row in ram["ramified_reductions"]:
    p = int(row["prime"])
    assert p in BAD
    bad_rows.append({
        "p": p,
        "double_root": int(row["double_root"]),
        "simple_root": int(row["simple_root"]),
        "inertia_class": "transposition/reflection",
        "inertia_invariant_dimension": 1,
        "local_factor": [1, -1],
        "artin_conductor_exponent": 1,
    })
assert math.prod(r["p"] for r in bad_rows) == D
def prime_power_coeffs(p: int, e: int) -> list[int]:
    if p in BAD:
        return [1] * (e + 1)
    cls, _ = frobenius_from_root_count(direct_linear_root_count(p))
    a = CHARACTER[cls]
    det = DETERMINANT[cls]
    vals = [1]
    if e:
        vals.append(a)
    for k in range(2, e + 1):
        vals.append(a * vals[-1] - det * vals[-2])
    return vals


def dirichlet_coefficient(n: int) -> int:
    ans = 1
    for p, e in sp.factorint(n).items():
        ans *= prime_power_coeffs(int(p), int(e))[e]
    return int(ans)


coeffs = [dirichlet_coefficient(n) for n in range(1, 257)]
for m in range(1, 65):
    for n in range(1, 65):
        if math.gcd(m, n) == 1:
            assert dirichlet_coefficient(m * n) == dirichlet_coefficient(m) * dirichlet_coefficient(n)
# Independent LMFDB snapshot, fetched 2026-09-24.
lmfdb = {
    "label": "2.94557.3t2.a.a",
    "url": "https://www.lmfdb.org/ArtinRepresentation/2.94557.3t2.a.a",
    "dimension": 2,
    "conductor": 94557,
    "bad_primes": [3, 43, 733],
    "character_values": [2, 0, -1],
    "parity": "even",
    "root_number": 1,
    "local_factors_by_class": [
        [1, -2, 1],
        [1, 0, -1],
        [1, 1, 1],
    ],
    "common_bad_local_factor": [1, -1],
}
assert lmfdb["character_values"] == [CHARACTER[c] for c in ("identity", "transposition", "3-cycle")]
assert lmfdb["local_factors_by_class"] == [LOCAL_FACTORS[c] for c in ("identity", "transposition", "3-cycle")]
assert lmfdb["conductor"] == math.prod(BAD)
out = {
    "schema": "w33.20260924.triality_artin_a2_spectrum.v1",
    "status": "PASS_TRIALITY_ARTIN_A2_SPECTRAL_REALIZATION",
    "field": {
        "cubic_polynomial": str(f),
        "discriminant": D,
        "quadratic_resolvent": "Q(sqrt(94557))",
        "normal_closure_group": "S3",
        "hilbert_3_class_field": True,
    },
    "A2_weyl_realization": {
        "gram": [[2, -1], [-1, 2]],
        "reflection_s": [[int(z) for z in row] for row in S1.tolist()],
        "rotation_r": [[int(z) for z in row] for row in R.tolist()],
        "relations": ["s^2=1", "r^3=1", "srs=r^-1"],
        "group": "W(A2)=C3:C2=S3",
        "character": CHARACTER,
        "determinant": DETERMINANT,
        "local_characteristic_factors": LOCAL_FACTORS,
        "repo_parent": "analysis/bt943_a2_plane_weyl_lift.py",
    },
    "class_field_phase_layer": {
        "order_three_character": "psi: Cl(F)[3]=C3 -> {1, omega, omega^2}",
        "quadratic_conjugation": "psi -> psi^-1 (omega <-> omega^2)",
        "induced_representation": "rho = Ind_{Gal(N/F)}^{Gal(N/Q)} psi",
        "induced_trace_on_C3": "psi + psi^-1 gives 2 on identity and -1 on nontrivial C3 elements",
        "orientation_boundary": "the rational S3 conjugacy class does not distinguish omega from omega^2",
    },
    "artin_L_function": {
        "representation_dimension": 2,
        "conductor": D,
        "root_number": 1,
        "parity": "even",
        "identity": "L_Q(s,rho)=zeta_K(s)/zeta_Q(s)=L_F(s,psi)",
        "normal_closure_identity": "zeta_N(s)=zeta_F(s)*L_Q(s,rho)^2=zeta_F(s)*zeta_K(s)^2/zeta_Q(s)^2",
        "first_256_dirichlet_coefficients": coeffs,
        "character_tensor_invariant_moments_1_to_12": moments,
    },
    "frobenius_census_below_10000": {
        "counts": counts,
        "unramified_prime_count": sum(counts.values()),
        "rows_below_250": prime_rows,
        "checks": [
            "a_p = number_of_linear_roots_of_f_mod_p - 1",
            "det(rho(Frob_p)) = Kronecker(94557/p)",
            "Euler polynomial = det(I - rho(Frob_p) T) in the BT943 A2 matrices",
        ],
    },
    "ramified_local_layer": {
        "rows": bad_rows,
        "common_local_factor": [1, -1],
        "conductor_exponents": {str(p): 1 for p in BAD},
        "interpretation": "reflection inertia fixes one A2 line, dropping local factor degree from 2 to 1",
    },
    "lmfdb_crosscheck": lmfdb,
    "boundary": (
        "Exact arithmetic/representation theorem. It identifies the standard Artin "
        "representation with the integral A2 Weyl reflection representation and compiles "
        "its Euler factors. The qutrit-phase language refers only to the C3 character "
        "alphabet; no physical SU(3), particle-generation, or optical identification is asserted."
    ),
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": out["status"],
    "counts": counts,
    "conductor": D,
    "moments_1_to_8": {k: moments[k] for k in list(moments)[:8]},
}, indent=2))
