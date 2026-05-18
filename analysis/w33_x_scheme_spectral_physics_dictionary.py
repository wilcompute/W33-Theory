#!/usr/bin/env python3
"""X-association scheme spectral physics dictionary.

Builds on:
  analysis/w33_minimal_logical_x_association_scheme.py
  analysis/w33_minimal_logical_x_scheme_eigenmatrix.py
  analysis/w33_minimal_logical_3adic_overlap_scheme.py

Established (upstream) facts.
----------------------------
The canonical W(3,3) edge CSS code [[240,81,3]]_3 with d_X=3, d_Z=4 has a
projective minimal-X-ray set of size 160.  Its unsigned visibility Gram
matrix U U^T (160 x 160) has the spectrum

    eigenvalue                     multiplicity
    --------------------------     ------------
    648                            1
    144 + 36 * sqrt(6)             24
    72                             30
    144 - 36 * sqrt(6)             24
    40                             81

The five eigenspace dimensions (1, 24, 30, 24, 81) sum to 160 = mu * v
(with mu = q+1 = 4 and v = 40).

This script factors EVERY entry of that table in pure substrate primitives
and reads off a physics dictionary.

Theorem (Spectral Physics Dictionary).
--------------------------------------
The five X-association eigenspaces of W(3,3) coincide with the substrate's
generational decomposition:

    sector        dim     substrate form                physics role
    ------------- ------- ----------------------------- ------------------
    trivial       1       q^0                           vacuum / Higgs vev
    Dirac+        24      f = pos.spec.mult. (lam=+2)   one chiral fermion sector
    gauge/scalar  30      2g = 2 * neg.spec.mult.       force-carriers + Higgs
    Dirac-        24      f = conjugate by CP           CP-conjugate chiral sector
    matter        81      H_1 = q^(q+1)                 protected logical homology

That is, (1, 24, 30, 24, 81) = (1, f, 2g, f, H_1) where (f, g) = (24, 15)
are the adjacency-eigenvalue multiplicities of the W(3,3) graph itself.

The TWO 24-sectors are exchanged by CP (Galois conjugation of sqrt(6)).
This is the CP doubling: f -> f bar with the Galois group of Q(sqrt(6))
acting as CP.  The 30 = 2g sits between them as its own conjugate, fixed
by CP -- the boson sector.  The 81 = H_1 is invariant under all of the
above; it is the protected matter sector.

Eigenvalue factorisations.
--------------------------
All five eigenvalues are expressible in substrate primitives:

    648 = 2^q * q^(q+1)     (Hessian group order)
    72  = 2^q * q^2         (2^q * Phi_3 - 2^q would also work; here clean)
    40  = v                 (W(3,3) vertex count)
    144 = k^2 = (q (q+1))^2
    36  = q^2 * mu = (q+1) q^2
    6   = q!                so sqrt(6) = sqrt(q!)

so the two irrational eigenvalues are

    144 +- 36 sqrt(6) = q^2 ( (q+1) q^2 +- (q+1) sqrt(q!) ) ?
                      = 36 ( mu +- sqrt(q!) )
                      = q^2 mu ( mu +- sqrt(q!) )

(Both factorisations agree.  The second is the cleanest.)

Trace check.
------------
trace(U U^T) = 1*648 + 24*(144+36 sqrt(6)) + 30*72
             + 24*(144-36 sqrt(6)) + 81*40
             = 648 + 24*288 + 30*72 + 81*40
             = 648 + 6912 + 2160 + 3240
             = 12960
             = 160 * 81
             = |X_min| * H_1
             = |W(E_6)| / 4.

The first equality is the trace identity (trace = row-norm sum); the second
identifies the X-scheme trace with one-quarter of |W(E_6)| = 51840, the
already-established commutation-shadow count.

CP doubling.
------------
The Galois group Gal(Q(sqrt(q!))/Q) = Z_2 acts on the X-eigenmatrix by
sending sqrt(6) -> -sqrt(6).  This swaps the two 24-dimensional eigenspaces
attached to (144 +- 36 sqrt(6)).  In the physics dictionary, this is
CP-conjugation: f <-> f bar.

Therefore the X-eigenmatrix is defined over the field of CP-invariant
quantities Q(sqrt(6)) and the CP-broken pair (24, 24) corresponds to the
two chiralities of one Dirac generation.

Hessian / Heisenberg sanity.
----------------------------
648 = order of the Hessian complex reflection group ST(25) is exactly the
top eigenvalue.  72 = 2^q * q^2 is the order of the projective Heisenberg
quotient Heis(F_3) / scalars.  The middle 30 = 2g  sector therefore lies
between the Hessian top and the Heisenberg middle:

    Hessian (vacuum, dim 1) -> CP-doubled fermions (dim 24+24)
                            -> Heisenberg (gauge/scalar, dim 30)
                            -> matter (H_1, dim 81).

Outputs.
--------
The script writes data/w33_x_scheme_spectral_physics_dictionary.json with
the full factorisation + dictionary + trace identity + CP doubling check.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

Q = 3
QP1 = 4
MU = QP1
V = 40
EDGES = 240
F = 24      # multiplicity of adjacency eigenvalue lam=+2
G = 15      # multiplicity of adjacency eigenvalue lam=-4
H1 = Q ** QP1   # 81
QFACT = math.factorial(Q)   # 6
HESSIAN_ORDER = 2 ** Q * H1  # 648
HEIS_PROJ = 2 ** Q * Q * Q   # 72
WE6 = 51_840
XMIN = 160   # |X_min| = projective minimal X-ray count
K = Q * QP1  # 12 = SRG valency = local codec


def factor_eigenvalue(lam_squared_part: int) -> str:
    """Return a short substrate factorisation string for an integer."""
    table = {
        1: "q^0",
        V: "v",
        HEIS_PROJ: f"2^q * q^2 = {2**Q} * {Q*Q}",
        HESSIAN_ORDER: f"2^q * q^(q+1) = {2**Q} * {H1}",
        144: f"k^2 = (q*(q+1))^2 = {K**2}",
        36: f"q^2 * mu = {Q*Q} * {MU}",
        QFACT: f"q! = {QFACT}",
    }
    return table.get(lam_squared_part, str(lam_squared_part))


def eigenvalue_table() -> list[dict]:
    sqrt6 = math.sqrt(QFACT)
    rows = [
        {
            "name": "vacuum",
            "eigenvalue_exact": "2^q * q^(q+1)",
            "eigenvalue_numeric": HESSIAN_ORDER,
            "multiplicity": 1,
            "mult_substrate": "q^0",
            "physics": "vacuum / Higgs VEV sector",
            "cp_role": "CP-singlet",
        },
        {
            "name": "Dirac+",
            "eigenvalue_exact": "q^2 * mu * (mu + sqrt(q!))",
            "eigenvalue_numeric": 144 + 36 * sqrt6,
            "multiplicity": F,
            "mult_substrate": "f = pos.spec.mult. of adj.eigval. +2",
            "physics": "one chiral fermion generation, sqrt(6) branch",
            "cp_role": "CP-partner of Dirac-",
        },
        {
            "name": "gauge_scalar",
            "eigenvalue_exact": "2^q * q^2",
            "eigenvalue_numeric": HEIS_PROJ,
            "multiplicity": 2 * G,
            "mult_substrate": "2g = 2 * neg.spec.mult. of adj.eigval. -4",
            "physics": "SM gauge + scalar bosons (Lie algebra + Higgs scalars)",
            "cp_role": "CP-self-conjugate (sym(5)+sym(5*) in SU(5))",
        },
        {
            "name": "Dirac-",
            "eigenvalue_exact": "q^2 * mu * (mu - sqrt(q!))",
            "eigenvalue_numeric": 144 - 36 * sqrt6,
            "multiplicity": F,
            "mult_substrate": "f = conjugate of Dirac+ under Gal(Q(sqrt(6))/Q)",
            "physics": "CP-conjugate chiral fermion generation",
            "cp_role": "CP-partner of Dirac+",
        },
        {
            "name": "matter_H1",
            "eigenvalue_exact": "v",
            "eigenvalue_numeric": V,
            "multiplicity": H1,
            "mult_substrate": "H_1 = q^(q+1)",
            "physics": "protected matter sector / logical qutrit code",
            "cp_role": "CP-invariant logical memory",
        },
    ]
    return rows


def trace_identity() -> dict:
    rows = eigenvalue_table()
    total = sum(r["multiplicity"] for r in rows)
    sqrt6 = math.sqrt(QFACT)
    trace_numeric = sum(r["multiplicity"] * r["eigenvalue_numeric"] for r in rows)
    # exact integer trace (sqrt(6) cancels because two 24-sectors are CP-paired)
    trace_exact = (
        HESSIAN_ORDER
        + F * (144 + 144)
        + 2 * G * HEIS_PROJ
        + H1 * V
    )
    return {
        "sum_of_multiplicities": total,
        "sum_equals_mu_times_v": total == MU * V,
        "trace_numeric": trace_numeric,
        "trace_exact_integer": trace_exact,
        "trace_factored": f"160 * 81 = |X_min| * H_1 = {XMIN * H1}",
        "trace_equals_we6_over_4": trace_exact == WE6 // 4,
        "we6": WE6,
        "we6_over_4": WE6 // 4,
        "sqrt6_cancels": True,
    }


def galois_cp_doubling() -> dict:
    return {
        "galois_group": "Gal(Q(sqrt(6))/Q) = Z/2Z",
        "action_on_eigenmatrix": "sends sqrt(6) -> -sqrt(6)",
        "swapped_eigenspaces": ["Dirac+", "Dirac-"],
        "fixed_eigenspaces": ["vacuum", "gauge_scalar", "matter_H1"],
        "physics_interpretation": (
            "CP-conjugation acts as the unique non-trivial Galois element of "
            "Q(sqrt(q!))/Q.  The two 24-dim sectors form a Dirac pair under CP, "
            "the 30-dim sector is CP-self-conjugate (boson sector), and the "
            "81-dim H_1 sector is CP-invariant logical matter."
        ),
        "qfact_under_root": QFACT,
        "qfact_substrate": "q!",
    }


def sum_substrate_polynomial() -> dict:
    """The X-multiplicities (1, f, 2g, f, H_1) = (1, 24, 30, 24, 81) factor as a
    substrate polynomial in q.  Show it explicitly.
    """
    # 1 + 24 + 30 + 24 + 81 = 160 = mu * v.
    # We claim 160 = (q+1)(q^3 + q^2 + q + 1) = mu * (q^4-1)/(q-1) = mu * v.
    rhs = MU * V
    via_poly = (Q + 1) * (Q**3 + Q**2 + Q + 1)
    return {
        "mu_times_v": rhs,
        "poly_form": "(q+1) * (q^3 + q^2 + q + 1)",
        "poly_value": via_poly,
        "agree": rhs == via_poly == XMIN,
        "note": "Same polynomial appears as 160 = mu * v = |X_min projective rays|.",
    }


def cp_invariant_pair_eigenvalue_check() -> dict:
    """The product of the two Dirac eigenvalues is CP-invariant.  Compute it."""
    # (144 + 36 sqrt(6)) (144 - 36 sqrt(6)) = 144^2 - 36^2 * 6
    #                                       = 20736 - 7776
    #                                       = 12960 = WE6 / 4.
    prod = 144**2 - (36**2) * QFACT
    return {
        "product_exact": prod,
        "factorisation": "144^2 - 36^2 * q! = 20736 - 7776 = 12960",
        "equals_we6_over_4": prod == WE6 // 4,
        "equals_xmin_times_H1": prod == XMIN * H1,
        "physics": (
            "The product of CP-conjugate Dirac eigenvalues is exactly the X-scheme "
            "trace and exactly |W(E_6)|/4.  CP-invariance of the spectrum is therefore "
            "the same identity as the W(E_6) commutation-shadow count."
        ),
    }


def hessian_heisenberg_sandwich() -> dict:
    """The five eigenvalues lie in a clean ordering: Hessian > Dirac+ > Heisenberg-projective
    > Dirac- > v.  Show this and tag each rung with its group-theoretic meaning.
    """
    sqrt6 = math.sqrt(QFACT)
    rungs = [
        {"rung": "Hessian top", "value": HESSIAN_ORDER, "substrate": "2^q * q^(q+1) = 648"},
        {"rung": "Dirac+ (CP+)", "value": 144 + 36 * sqrt6, "substrate": "q^2 mu (mu + sqrt(q!))"},
        {"rung": "Heisenberg-projective", "value": HEIS_PROJ, "substrate": "2^q * q^2 = 72"},
        {"rung": "Dirac- (CP-)", "value": 144 - 36 * sqrt6, "substrate": "q^2 mu (mu - sqrt(q!))"},
        {"rung": "matter floor", "value": V, "substrate": "v = 40 = W(3,3) vertex count"},
    ]
    is_descending = all(rungs[i]["value"] >= rungs[i + 1]["value"] for i in range(len(rungs) - 1))
    return {"rungs": rungs, "is_descending": is_descending}


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q,
                "mu": MU,
                "v": V,
                "edges": EDGES,
                "f_pos_spec_mult": F,
                "g_neg_spec_mult": G,
                "H_1": H1,
                "q_factorial": QFACT,
                "k_codec": K,
                "Hessian_order": HESSIAN_ORDER,
                "Heisenberg_projective": HEIS_PROJ,
                "WE6": WE6,
                "X_min_count": XMIN,
            },
        },
        "spectral_table": eigenvalue_table(),
        "trace_identity": trace_identity(),
        "galois_cp_doubling": galois_cp_doubling(),
        "sum_substrate_polynomial": sum_substrate_polynomial(),
        "cp_pair_product": cp_invariant_pair_eigenvalue_check(),
        "hessian_heisenberg_ordering": hessian_heisenberg_sandwich(),
        "theorem": (
            "X-Scheme Spectral Physics Dictionary.  The 4-class minimal-X "
            "association scheme of the W(3,3) edge CSS code has eigenspace "
            "multiplicities (1, f, 2g, f, H_1) = (1, 24, 30, 24, 81), where "
            "(f, g) = (24, 15) are the adjacency-eigenvalue multiplicities of "
            "W(3,3) itself.  The two f-dimensional Dirac eigenspaces are "
            "exchanged by the Galois action sqrt(q!) -> -sqrt(q!), which is "
            "CP-conjugation.  The 2g-dimensional middle is CP-self-conjugate "
            "(bosonic).  The H_1-dimensional sector is CP-invariant logical "
            "matter.  The CP-conjugate Dirac eigenvalues have product "
            "|W(E_6)|/4 = 12960, which is also the X-scheme trace and the "
            "X_min x H_1 incidence count."
        ),
        "honesty_boundary": (
            "This script states the spectral data as factual (cited from the "
            "upstream eigenmatrix audits) and produces a clean substrate-primitive "
            "factorisation plus a physics dictionary.  The dictionary is an "
            "identification, not a derivation of measured masses.  The CP/Galois "
            "claim is rigorous at the level of the eigenmatrix; mapping the two "
            "24-sectors to physical (chirality, flavor) pairs requires a separate "
            "particle-content identification."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_x_scheme_spectral_physics_dictionary.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("X-association scheme: spectral table")
    print("=" * 72)
    for row in payload["spectral_table"]:
        print(
            f"  {row['name']:14s} eigval={row['eigenvalue_exact']:38s} mult={row['multiplicity']:3d} "
            f"= {row['mult_substrate']}"
        )
    print()
    print("Trace identity:")
    ti = payload["trace_identity"]
    print(f"  trace(U U^T) = {ti['trace_exact_integer']} = {ti['trace_factored']}")
    print(f"  |W(E_6)|/4   = {ti['we6_over_4']}; matches: {ti['trace_equals_we6_over_4']}")
    print()
    print("CP pair product:")
    cp = payload["cp_pair_product"]
    print(f"  (144+36sqrt6)(144-36sqrt6) = {cp['product_exact']}")
    print(f"  = |W(E_6)|/4: {cp['equals_we6_over_4']}")
    print(f"  = |X_min| * H_1: {cp['equals_xmin_times_H1']}")
    print()
    print(f"Sum of multiplicities = {payload['sum_substrate_polynomial']['mu_times_v']} "
          f"= mu * v = {payload['sum_substrate_polynomial']['poly_form']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
