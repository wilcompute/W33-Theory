#!/usr/bin/env python3
"""Explicit operational continuation basis inside a primitive Steinberg-81 image.

The previous continuation-superposition pass proved that the obvious F_3^4
81-slot permutation model is reducible.  This module takes the opposite route:
start from a primitive rank-81 Steinberg projector already certified in the
1080-point obstruction-carrier permutation representation and *derive* an
81-coordinate operational basis from its image.

Let Q be the +4 primitive spectral idempotent in the Steinberg multiplicity
block materialized by the repository's exact orbital algebra.  We select 81
independent columns of Q,

    B = [Q e_j]_{j in J} : Q^81 -> im(Q) subset Q^1080,

and 81 coordinate rows R for which B_R is nonsingular.  For each of the four
stored PSp(4,3) permutation generators g we then define

    A_g = B_R^{-1} (P_g B)_R.

Because Q is an orbital-algebra idempotent, it commutes with every group
permutation.  Therefore P_g B is again in im(Q), and the coordinate equality on
R lifts to the exact intertwining relation

    B A_g = P_g B.

This is the missing operational-to-Steinberg map.  It deliberately does NOT
identify the old F_3^4 slot permutation action with Steinberg.  Instead the 81
operational coordinates are the projected-coordinate basis selected here.
"""
from __future__ import annotations

import hashlib
import json
from math import lcm
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
from w33_20260831_all5_frontier_audit import orbit_ids
from w33_20260831_c5_wedderburn_kernel import orbital_mult, center_equations, generic_center, mulvec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_CONTINUATION_STEINBERG_INTERTWINER.json"
MOD = 1_000_003
DIM = 81


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def independent_columns_mod(matrix: np.ndarray, wanted: int, prime: int = MOD) -> list[int]:
    """Greedy exact-rank witness over a large auxiliary prime field."""
    pivots: list[int] = []
    basis: list[np.ndarray] = []
    chosen: list[int] = []
    for j in range(matrix.shape[1]):
        v = np.mod(matrix[:, j], prime).astype(np.int64, copy=True)
        for pivot, row in zip(pivots, basis):
            factor = int(v[pivot])
            if factor:
                v = np.mod(v - factor * row, prime)
        nz = np.flatnonzero(v)
        if not len(nz):
            continue
        pivot = int(nz[0])
        inv = pow(int(v[pivot]), -1, prime)
        v = np.mod(v * inv, prime)
        pivots.append(pivot)
        basis.append(v)
        chosen.append(j)
        if len(chosen) == wanted:
            return chosen
    raise AssertionError(f"matrix has auxiliary-prime rank < {wanted}")


def primitive_projector():
    """Rebuild the exact +4 primitive Steinberg idempotent in orbital coordinates."""
    acts, charts, lines = obs.build_action()
    rel, reps, _sizes = orbit_ids(acts, acts, 1080, 1080)
    assert len(reps) == 59
    T = orbital_mult(rel, reps)
    Z = center_equations(T).nullspace()
    assert len(Z) == 15
    diag = int(rel[0, 0])
    one = sp.zeros(59, 1)
    one[diag] = 1
    z, _L, _cp, factors, _coeff = generic_center(Z, T)
    records, idempotents = obs.central_records(z, factors, T, one, diag)
    si = next(i for i, r in enumerate(records) if r["complexIrrepDegree"] == 81)
    E = idempotents[si]
    assert 1080 * E[diag] == 243

    # Exact 9-dimensional left regular model of the Steinberg multiplicity algebra.
    cols = []
    for j in range(59):
        q = sp.zeros(59, 1)
        q[j] = 1
        cols.append(mulvec(E, q, T))
    M = sp.Matrix.hstack(*cols)
    _r, piv = M.rref()
    piv = list(piv)
    assert len(piv) == 9
    U = sp.Matrix.hstack(*[cols[j] for j in piv])
    _rr, rowp = U.T.rref()
    rowp = list(rowp)
    assert len(rowp) == 9
    Uinv = U[rowp, :].inv()

    def coord(v):
        return Uinv * v[rowp, :]

    def left_matrix(v):
        A = sp.zeros(9, 9)
        for k in range(9):
            A[:, k] = coord(mulvec(v, U[:, k], T))
        return A

    # The repository certificate identifies the symmetric orbital pair (11,25)
    # whose Steinberg restriction has eigenvalues -4,0,+4, each multiplicity 3.
    transpose = []
    for seed in reps:
        a, b = divmod(seed, 1080)
        transpose.append(int(rel[b, a]))
    j = 11
    assert transpose[j] == 25
    q = sp.zeros(59, 1)
    q[j] = 1
    q[transpose[j]] += 1
    b = mulvec(E, q, T)
    BM = left_matrix(b)
    assert sp.factor(BM.charpoly().as_expr()) == sp.factor(sp.Symbol("lambda")**3 * (sp.Symbol("lambda") - 4)**3 * (sp.Symbol("lambda") + 4)**3)

    lam = sp.Integer(4)
    P = E
    den = sp.Integer(1)
    for mu in (sp.Integer(-4), sp.Integer(0)):
        P = mulvec(P, b - mu * E, T)
        den *= lam - mu
    P /= den
    assert mulvec(P, P, T) == P
    assert 1080 * P[diag] == 81
    return acts, rel, P, T, diag


def build_intertwiner() -> dict[str, Any]:
    acts, rel, Qvec, T, diag = primitive_projector()
    scale = 1
    for x in Qvec:
        scale = lcm(scale, int(sp.denom(x)))
    coeff = np.array([int(sp.Integer(scale) * x) for x in Qvec], dtype=np.int64)
    Qint = coeff[rel]
    assert Qint.shape == (1080, 1080)

    # Q^2=Q in the orbital algebra; trace gives its actual permutation-space rank.
    assert mulvec(Qvec, Qvec, T) == Qvec
    assert sp.Rational(1080) * Qvec[diag] == 81

    pivot_columns = independent_columns_mod(Qint, DIM)
    Bint = Qint[:, pivot_columns]
    pivot_rows = independent_columns_mod(Bint.T, DIM)
    Bsub = sp.Matrix(Bint[pivot_rows, :].tolist())
    Bsub_inv = Bsub.inv()  # exact; also certifies the selected 81 columns over Q

    generator_records = []
    operational_generators: list[sp.Matrix] = []
    rel0 = rel
    for gi, perm_tuple in enumerate(acts):
        perm = np.asarray(perm_tuple, dtype=np.int64)
        # Full simultaneous-orbit invariance is the concrete commutation witness QP=PQ.
        orbit_invariant = bool(np.array_equal(rel0[np.ix_(perm, perm)], rel0))
        assert orbit_invariant
        target_cols = [int(perm[j]) for j in pivot_columns]
        target_sub = sp.Matrix(Qint[np.ix_(pivot_rows, target_cols)].tolist())
        A = Bsub_inv * target_sub
        assert A.det() != 0
        operational_generators.append(A)
        generator_records.append({
            "generator": gi,
            "permutation_digest": digest(list(map(int, perm_tuple))),
            "operational_matrix_digest": digest([[str(A[i, j]) for j in range(DIM)] for i in range(DIM)]),
            "orbit_relation_invariant": orbit_invariant,
            "determinant": str(sp.factor(A.det())),
        })

    # A primitive nontrivial Steinberg copy must have no common fixed vector for
    # these generators.  Verify this directly in the derived operational basis.
    fixed_equations = sp.Matrix.vstack(*[A - sp.eye(DIM) for A in operational_generators])
    common_fixed_dimension = DIM - int(fixed_equations.rank())
    assert common_fixed_dimension == 0

    # Map identity: slot s maps to (1/scale) Qint[:, pivot_columns[s]].  The full
    # matrix is reproducible from the committed orbital coefficients + pivots,
    # so the certificate need not dump 87,480 rational entries.
    reconstruction = {
        "scale": scale,
        "orbital_coefficients_scaled": coeff.tolist(),
        "pivot_columns": pivot_columns,
        "pivot_rows": pivot_rows,
    }
    checks = {
        "primitive_projector_actual_rank_is_81": sp.Rational(1080) * Qvec[diag] == 81,
        "selected_operational_basis_has_81_independent_vectors": len(pivot_columns) == DIM and Bsub.det() != 0,
        "all_four_group_generators_preserve_orbital_projector": all(r["orbit_relation_invariant"] for r in generator_records),
        "all_induced_operational_generator_matrices_are_invertible": all(A.det() != 0 for A in operational_generators),
        "derived_operational_action_has_no_common_fixed_vector": common_fixed_dimension == 0,
        "map_is_reconstructible_from_orbital_coefficients_and_pivots": len(coeff) == 59 and len(pivot_rows) == DIM,
    }
    return {
        "schema": "w33.continuation-steinberg-intertwiner.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "projector": {
            "ambient_dimension": 1080,
            "image_dimension": 81,
            "orbital_rank": 59,
            "scaled_orbital_coefficients_digest": digest(reconstruction),
            "scale": scale,
        },
        "operational_basis": {
            "dimension": DIM,
            "pivot_columns": pivot_columns,
            "coordinate_rows": pivot_rows,
            "encoding_rule": "slot s -> Q e_{pivot_columns[s]} in the certified 1080-point permutation module",
            "basis_digest": digest(reconstruction),
        },
        "generators": generator_records,
        "common_fixed_dimension": common_fixed_dimension,
        "theorem": (
            "The 81 continuation-control coordinates are realized explicitly as independent projected coordinate vectors inside a certified primitive Steinberg-81 image. "
            "For each stored PSp(4,3) generator the induced 81x81 rational matrix is defined by exact coordinate extraction and satisfies B A_g = P_g B because the orbital projector commutes with the permutation action."
        ),
        "boundary": (
            "This replaces the false F3^4=Steinberg identification with a representation-theoretically valid operational basis. "
            "It is an exact finite algebra construction; it is not yet a physical optical encoding or a fault-tolerance theorem."
        ),
    }


def main() -> int:
    out = build_intertwiner()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
