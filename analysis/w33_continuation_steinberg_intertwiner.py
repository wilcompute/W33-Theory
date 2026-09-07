#!/usr/bin/env python3
"""Explicit operational continuation basis inside a primitive Steinberg-81 image.

The obvious F_3^4 81-slot permutation model was previously falsified as a
Steinberg model: it has invariant vectors.  This verifier instead starts with
the repository's exact primitive rank-81 Steinberg idempotent Q in the actual
1080-point obstruction-carrier permutation representation and derives an
operational basis from its image.

Choose 81 independent projected coordinate vectors

    B = [Q e_j]_{j in J}: Q^81 -> im(Q) subset Q^1080.

We certify a square coordinate minor B_R as nonsingular by reducing the scaled
integer matrix modulo a large prime p.  A nonzero determinant modulo p implies
the integer determinant is nonzero, hence B is an exact rational basis of the
rank-81 image.

For every stored PSp(4,3) permutation generator g, orbital-relation invariance
proves exactly that P_g Q = Q P_g.  Therefore P_g preserves im(Q), so there is a
unique exact rational operational action

    A_g = B_R^{-1} (P_g B)_R

satisfying B A_g = P_g B.  We do not waste CI expanding four dense 81x81
rational matrices into huge fractions.  Instead, because det(B_R) is nonzero
mod p, the same formula reduces legitimately modulo p; we compute A_g mod p and
verify the full 1080x81 intertwining equation there.  This is both an executable
coordinate certificate and a rigorous witness that the exact rational formula
is well-defined.

A full-rank stacked (A_g-I) system modulo p also proves the exact rational module
has no common fixed vector: a nonzero full-rank minor modulo p is a nonzero
integer/rational minor in characteristic zero.
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
    """Greedy pivot-column certificate over F_p."""
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
        v = np.mod(v * pow(int(v[pivot]), -1, prime), prime)
        pivots.append(pivot)
        basis.append(v)
        chosen.append(j)
        if len(chosen) == wanted:
            return chosen
    raise AssertionError(f"matrix has F_{prime} rank < {wanted}")


def inverse_mod(matrix: np.ndarray, prime: int = MOD) -> np.ndarray:
    """Gauss-Jordan inverse over F_p using Python ints to avoid overflow."""
    n, m = matrix.shape
    if n != m:
        raise ValueError("inverse_mod requires square matrix")
    aug = [[int(matrix[i, j]) % prime for j in range(n)] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    for c in range(n):
        pivot = next((r for r in range(c, n) if aug[r][c] % prime), None)
        if pivot is None:
            raise AssertionError("selected minor is singular modulo certificate prime")
        aug[c], aug[pivot] = aug[pivot], aug[c]
        inv = pow(aug[c][c] % prime, -1, prime)
        aug[c] = [(x * inv) % prime for x in aug[c]]
        for r in range(n):
            if r == c:
                continue
            factor = aug[r][c] % prime
            if factor:
                aug[r] = [(aug[r][k] - factor * aug[c][k]) % prime for k in range(2 * n)]
    return np.asarray([row[n:] for row in aug], dtype=np.int64)


def matmul_mod(a: np.ndarray, b: np.ndarray, prime: int = MOD) -> np.ndarray:
    """Overflow-safe matrix multiplication over F_p."""
    # p^2*81 exceeds signed int64, so accumulate in Python integers by rows.
    out = np.zeros((a.shape[0], b.shape[1]), dtype=np.int64)
    for i in range(a.shape[0]):
        for k in range(a.shape[1]):
            aik = int(a[i, k]) % prime
            if not aik:
                continue
            out[i, :] = np.asarray([(int(out[i, j]) + aik * int(b[k, j])) % prime for j in range(b.shape[1])], dtype=np.int64)
    return out


def rank_mod(matrix: np.ndarray, prime: int = MOD) -> int:
    a = [[int(x) % prime for x in row] for row in matrix.tolist()]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, prime)
        a[r] = [(x * inv) % prime for x in a[r]]
        for i in range(rows):
            if i == r or not a[i][c]:
                continue
            f = a[i][c]
            a[i] = [(a[i][j] - f * a[r][j]) % prime for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def primitive_projector():
    """Rebuild the exact +4 primitive Steinberg idempotent in orbital coordinates."""
    acts, _charts, _lines = obs.build_action()
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

    # Frozen certificate orbital pair: Steinberg restriction eigenvalues -4,0,+4.
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
    lam_sym = sp.Symbol("lambda")
    assert sp.factor(BM.charpoly(lam_sym).as_expr()) == sp.factor(lam_sym**3 * (lam_sym - 4)**3 * (lam_sym + 4)**3)

    P = E
    den = sp.Integer(1)
    for mu in (sp.Integer(-4), sp.Integer(0)):
        P = mulvec(P, b - mu * E, T)
        den *= sp.Integer(4) - mu
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
    assert mulvec(Qvec, Qvec, T) == Qvec
    assert sp.Rational(1080) * Qvec[diag] == 81

    # Exact basis proof from a good-prime minor witness.
    pivot_columns = independent_columns_mod(Qint, DIM)
    Bint = Qint[:, pivot_columns]
    pivot_rows = independent_columns_mod(Bint.T, DIM)
    Bsub = np.mod(Bint[pivot_rows, :], MOD)
    Bsub_inv = inverse_mod(Bsub)
    assert np.array_equal(matmul_mod(Bsub, Bsub_inv), np.eye(DIM, dtype=np.int64))

    generator_records = []
    operational_mod = []
    for gi, perm_tuple in enumerate(acts):
        perm = np.asarray(perm_tuple, dtype=np.int64)
        orbit_invariant = bool(np.array_equal(rel[np.ix_(perm, perm)], rel))
        assert orbit_invariant  # exact QP=PQ witness because Q is constant on orbitals
        target_cols = [int(perm[j]) for j in pivot_columns]
        target_full = np.mod(Qint[:, target_cols], MOD)
        target_sub = target_full[pivot_rows, :]
        A = matmul_mod(Bsub_inv, target_sub)
        full_ok = np.array_equal(matmul_mod(np.mod(Bint, MOD), A), target_full)
        assert full_ok
        assert rank_mod(A) == DIM
        operational_mod.append(A)
        generator_records.append({
            "generator": gi,
            "permutation_digest": digest(list(map(int, perm_tuple))),
            "operational_matrix_mod_p_digest": digest(A.tolist()),
            "certificate_prime": MOD,
            "orbit_relation_invariant_exact": orbit_invariant,
            "full_intertwining_verified_mod_p": full_ok,
            "operational_rank_mod_p": DIM,
        })

    stacked = np.vstack([np.mod(A - np.eye(DIM, dtype=np.int64), MOD) for A in operational_mod])
    fixed_rank_mod = rank_mod(stacked)
    common_fixed_dimension = DIM - fixed_rank_mod
    assert common_fixed_dimension == 0

    reconstruction = {
        "scale": scale,
        "orbital_coefficients_scaled": coeff.tolist(),
        "pivot_columns": pivot_columns,
        "pivot_rows": pivot_rows,
        "certificate_prime": MOD,
    }
    checks = {
        "primitive_projector_actual_rank_is_81": sp.Rational(1080) * Qvec[diag] == 81,
        "selected_81_projected_columns_are_exactly_independent": len(pivot_columns) == DIM,
        "selected_coordinate_minor_is_nonsingular_mod_good_prime": np.array_equal(matmul_mod(Bsub, Bsub_inv), np.eye(DIM, dtype=np.int64)),
        "modular_minor_witness_implies_characteristic_zero_independence": True,
        "all_four_group_generators_preserve_orbital_projector_exactly": all(r["orbit_relation_invariant_exact"] for r in generator_records),
        "all_four_full_intertwining_relations_verify_mod_good_prime": all(r["full_intertwining_verified_mod_p"] for r in generator_records),
        "all_induced_operational_generator_actions_are_invertible": all(r["operational_rank_mod_p"] == DIM for r in generator_records),
        "derived_operational_action_has_no_common_fixed_vector": common_fixed_dimension == 0,
        "map_is_reconstructible_from_orbital_coefficients_and_pivots": len(coeff) == 59 and len(pivot_rows) == DIM,
    }
    return {
        "schema": "w33.continuation-steinberg-intertwiner.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "projector": {
            "ambient_dimension": 1080,
            "image_dimension": 81,
            "orbital_rank": 59,
            "scale": scale,
            "scaled_orbital_coefficients_digest": digest(reconstruction),
        },
        "operational_basis": {
            "dimension": DIM,
            "pivot_columns": pivot_columns,
            "coordinate_rows": pivot_rows,
            "certificate_prime": MOD,
            "encoding_rule": "slot s -> Q e_{pivot_columns[s]} in the exact 1080-point rational permutation module",
            "basis_digest": digest(reconstruction),
        },
        "exact_action_formula": "A_g = B_R^{-1} (P_g B)_R over Q; det(B_R) != 0 is certified because its scaled integer determinant is nonzero modulo p",
        "generators": generator_records,
        "common_fixed_dimension": common_fixed_dimension,
        "theorem": (
            "The 81 continuation-control coordinates are an explicit exact rational basis of a primitive Steinberg-81 image. "
            "Orbital invariance proves P_g Q = Q P_g exactly, hence the exact rational A_g formula is well-defined and satisfies B A_g = P_g B. "
            "The good-prime matrices are executable certificates of the same coordinate actions without giant rational expansion."
        ),
        "boundary": (
            "This replaces the false F3^4=Steinberg identification with a representation-theoretically valid operational encoding. "
            "It is an exact finite-algebra construction plus characteristic-p certification; it is not a physical optical encoding or a fault-tolerance theorem."
        ),
    }


def main() -> int:
    out = build_intertwiner()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
