#!/usr/bin/env python3
"""Dihedral Maass / symmetric-square fixed-point corollary of the triality field.

This packet is exact arithmetic/representation theory.  It turns the order-3
Hilbert-class character of F=Q(sqrt(94557)) into its weight-zero dihedral
automorphic induction and records the t=0, lambda=1/4 endpoint.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_triality_maass_quarter_fixed_point.json"

cf = json.loads((ROOT / "data/w33_20260924_triality_class_field_closure.json").read_text())
art = json.loads((ROOT / "data/w33_20260924_triality_artin_a2_spectrum.json").read_text())

D = int(cf["cubic"]["discriminant"])
assert D == 94557
assert cf["quadratic_resolvent"]["class_number"] == 6
assert cf["quadratic_resolvent"]["three_primary_class_group"] == "C3"
assert cf["normal_closure"]["identification"].startswith("Hilbert 3-class field")
# Pure class-group character: no archimedean frequency and even parity.
ell = 0
kappa = 0
regulator = float(cf["quadratic_resolvent"]["regulator_float"])
assert regulator > 0
t0 = math.pi * abs(ell) / regulator
laplace0 = 0.25 + t0 * t0
assert t0 == 0.0
assert laplace0 == 0.25

# The order-3 character is complex, so it is not fixed by quadratic conjugation
# and its automorphic induction is cuspidal rather than a norm pullback.
class_character = {
    "order": 3,
    "values": ["1", "omega", "omega^2"],
    "complex": True,
    "conjugation": "psi^sigma = psi^-1 = psi^2",
    "finite_conductor": "O_F (unramified)",
    "archimedean_index_ell": ell,
    "parity_kappa": kappa,
}
# S3 character algebra, class order: e, transposition, 3-cycle.
one = [1, 1, 1]
sign = [1, -1, 1]
rho = [2, 0, -1]
rho_tensor_rho = [v * v for v in rho]
assert rho_tensor_rho == [a + b + c for a, b, c in zip(one, sign, rho)]

# Sym^2 character uses (chi(g)^2 + chi(g^2))/2.
# g^2 lies in classes e,e,3cycle respectively.
rho_g2 = [2, 2, -1]
sym2 = [(a*a + b)//2 for a, b in zip(rho, rho_g2)]
wedge2 = [(a*a - b)//2 for a, b in zip(rho, rho_g2)]
assert sym2 == [3, 1, 0]
assert wedge2 == sign
assert sym2 == [a + b for a, b in zip(one, rho)]
assert [a*b for a, b in zip(sign, rho)] == rho
ad0 = [a - 1 for a in rho_tensor_rho]
assert ad0 == [a + b for a, b in zip(sign, rho)]
# Tensor-invariant dimensions are an exact Jacobsthal shift.
def jacobsthal(n: int) -> int:
    if n == 0:
        return 0
    a, b = 0, 1
    for _ in range(n):
        a, b = b, b + 2*a
    return a


moments = {int(k): int(v) for k, v in art["artin_L_function"]["character_tensor_invariant_moments_1_to_12"].items()}
for n, mult in moments.items():
    assert mult == jacobsthal(n - 1)
    assert mult == (2**n + 2*((-1)**n)) // 6

# Full dihedral spectral spacing from the same Pell regulator.
spacing = math.pi / regulator
spectral_ladder = []
for n in range(0, 13):
    t = n * spacing
    spectral_ladder.append({
        "ell": n,
        "t": t,
        "laplace_eigenvalue": 0.25 + t*t,
    })
# Hecke/Artin coefficients are the same Euler data already certified.
coeffs = art["artin_L_function"]["first_256_dirichlet_coefficients"]
assert coeffs[0] == 1
prime_rows = art["frobenius_census_below_10000"]["rows_below_250"]
assert {row["a_p"] for row in prime_rows} <= {-1, 0, 2}
assert art["lmfdb_crosscheck"]["parity"] == "even"
assert art["lmfdb_crosscheck"]["root_number"] == 1
assert art["lmfdb_crosscheck"]["conductor"] == D

out = {
    "schema": "w33.20260924.triality_maass_quarter_fixed_point.v1",
    "status": "PASS_TRIALITY_MAASS_QUARTER_FIXED_POINT",
    "base_field": {
        "F": "Q(sqrt(94557))",
        "discriminant": D,
        "class_group": "C6",
        "three_primary": "C3",
        "fundamental_unit": cf["quadratic_resolvent"]["fundamental_unit"],
        "regulator": regulator,
    },
    "class_character": class_character,
    "dihedral_maass_form": {
        "construction": "automorphic induction AI_{F/Q}(psi)",
        "level": D,
        "nebentypus": "chi_94557",
        "weight": 0,
        "parity": "even",
        "spectral_parameter_t": t0,
        "laplace_eigenvalue": laplace0,
        "root_number": 1,
        "cuspidal_reason": "order-3 class character is complex, hence does not factor through Norm_{F/Q}",
        "L_identity": "L(s,g_psi)=L_F(s,psi)=L_Q(s,rho)=zeta_K(s)/zeta_Q(s)",
        "prime_eigenvalue_rule": "lambda_g(p)=tr rho(Frob_p)=#roots(f mod p)-1 for p not dividing 94557",
    },
    "spectral_ladder": {
        "formula": "t_ell = pi*|ell|/log(epsilon_F)",
        "spacing": spacing,
        "first_13_nonnegative_modes": spectral_ladder,
        "endpoint": "ell=0 is the exact lambda=1/4 class-field mode",
    },
    "self_lift": {
        "rho_tensor_rho": "1 + sign + rho",
        "symmetric_square": "Sym^2(rho)=1+rho",
        "exterior_square": "Lambda^2(rho)=sign=chi_94557",
        "adjoint_trace_zero": "Ad^0(rho)=sign+rho",
        "order3_character_identity": "psi^2=psi^-1=psi^sigma, hence AI(psi^2)=AI(psi)",
        "automorphic_symmetric_square": "Sym^2(g)=1 boxplus g",
        "automorphic_adjoint": "Ad(g)=chi_94557 boxplus g",
        "L_symmetric_square": "L(s,Sym^2 g)=zeta(s)*L(s,g)",
        "L_adjoint": "L(s,Ad g)=L(s,chi_94557)*L(s,g)",
    },
    "tensor_invariants": {
        "formula": "dim((rho^tensor n)^S3)=(2^n+2(-1)^n)/6=Jacobsthal(n-1)",
        "n_1_to_12": {str(k): v for k, v in moments.items()},
        "repo_prior_boundary": "Jacobsthal values occurred numerically before; this packet supplies a representation-theoretic mechanism for the full sequence.",
    },
    "evidence": {
        "artin_certificate": "data/w33_20260924_triality_artin_a2_spectrum.json",
        "class_field_certificate": "data/w33_20260924_triality_class_field_closure.json",
        "literature_formula": "Humphries-Khan: dihedral Maass newforms from real-quadratic Hecke characters, t=pi|ell|/log epsilon",
        "recent_crosscheck": "Tanaka 2026 explicitly constructs Maass wave cusp forms from Hecke characters on arbitrary real quadratic fields, including dihedral Artin examples.",
    },
    "boundary": (
        "Exact automorphic/arithmetic consequence of the class-field packet. "
        "The equality lambda=1/4 is a Laplace eigenvalue of the associated dihedral Maass form. "
        "Its numerical equality with 1/mu for W(3,3), mu=4, is NOT promoted: no map from "
        "the graph intersection number mu to this automorphic Laplacian has been constructed."
    ),
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": out["status"],
    "level": D,
    "t": t0,
    "laplace": laplace0,
    "spacing": spacing,
    "sym2": out["self_lift"]["symmetric_square"],
    "jacobsthal_1_to_8": {str(n): moments[n] for n in range(1, 9)},
}, indent=2))
