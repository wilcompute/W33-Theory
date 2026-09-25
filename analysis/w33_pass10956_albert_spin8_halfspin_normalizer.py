#!/usr/bin/env python3
"""Pass 10956: Albert Spin(8) half-spin normalizer bridge.

Inside the executable Pass10950 clock Albert algebra, choose one spatial
Peirce-0 direction. Its stabilizer in the certified compact spin(9) is
spin(8). The Peirce 16 splits exactly into two irreducible 8D modules, and
a pi rotation in spin(9) normalizing that stabilizer exchanges the two
modules and squares to the already-certified 2pi matter-parity sign.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction as Fr
from math import lcm
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10956_albert_spin8_halfspin_normalizer.json"

_spec = importlib.util.spec_from_file_location(
    "p50", ROOT / "analysis/w33_pass10950_clock_albert_lorentz_spinor.py")
P50 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P50)
TOL = 1e-8
def commutant(mats, d):
    eqs = []
    for R in mats:
        for r in range(d):
            for c in range(d):
                row = [Fr(0)] * (d * d)
                for k in range(d):
                    if R[k, c] != 0:
                        row[r * d + k] += Fr(R[k, c])
                    if R[r, k] != 0:
                        row[k * d + c] -= Fr(R[r, k])
                eqs.append(row)
    return P50.nullspace(eqs)


def independent_columns(M, count):
    chosen = []
    cols = []
    for j in range(M.cols):
        v = [Fr(sp.Rational(x)) for x in M[:, j]]
        if P50.rank(cols + [v]) > len(cols):
            cols.append(v)
            chosen.append(j)
        if len(chosen) == count:
            break
    assert len(chosen) == count
    return M[:, chosen]


def restrict_to_subspace(R, B):
    pinv = (B.T * B).inv() * B.T
    X = pinv * R * B
    assert B * X == R * B
    return X


def matrix_rational_strings(M):
    return [[str(sp.Rational(M[i, j])) for j in range(M.cols)]
            for i in range(M.rows)]
def main():
    J = P50.build_clock_albert()
    n, prodF = J["n"], J["prod"]
    den = lcm(*[x.denominator for x in prodF.flat])
    Pi = np.array(
        [[[int(x * den) for x in prodF[i, j]] for j in range(n)]
         for i in range(n)], dtype=np.int64)
    Ls = np.stack([Pi[i].T for i in range(n)])

    def Lv(x):
        return np.tensordot(np.asarray(x, dtype=np.int64), Ls, axes=1)

    def mulv(x, y):
        return np.asarray(x, dtype=np.int64) @ np.tensordot(
            Pi, np.asarray(y, dtype=np.int64), axes=([1], [0]))

    I27 = np.eye(n, dtype=np.int64)
    idx, G = J["idx"], J["G"]
    evec = sum(I27[idx[g]] for g in G)
    cvec = I27[idx[G[0]]]
    e2, e3 = I27[idx[G[1]]], I27[idx[G[2]]]
    s0 = e2 - e3
    trL = np.array([np.trace(Ls[i]) for i in range(n)])

    # Rebuild Der(A) and the compact spin(9)=Der_c from Pass10950.
    comms = [Ls[i] @ Ls[j] - Ls[j] @ Ls[i]
             for i, j in itertools.combinations(range(n), 2)]
    basisD, chosen = [], []
    for C in comms:
        v = C.flatten().tolist()
        if P50.rank(chosen + [v]) > len(chosen):
            chosen.append(v)
            basisD.append(C)
        if len(basisD) == 52:
            break
    assert len(basisD) == 52
    Dc_rows = np.stack([D @ cvec for D in basisD]).T.tolist()
    co = P50.nullspace(Dc_rows)
    Dc = []
    for cv in co:
        q = lcm(*[x.denominator for x in cv])
        Dc.append(sum(int(x * q) * D for x, D in zip(cv, basisD)))
    assert len(Dc) == 36

    # Peirce 16 and its exact spin representation.
    Lc = Lv(cvec)
    Ahalf = P50.nullspace((2 * Lc - den * I27).tolist())
    Hi = [np.array(
        [int(x * lcm(*[y.denominator for y in v])) for x in v],
        dtype=np.int64) for v in Ahalf]
    assert len(Hi) == 16
    Harr = np.stack(Hi).T
    Hmat = sp.Matrix(Harr.tolist())
    Hpinv = (Hmat.T * Hmat).inv() * Hmat.T

    def rep16(M):
        img = sp.Matrix((M @ Harr).tolist())
        R = Hpinv * img
        assert Hmat * R == img
        return R

    spin9 = [rep16(D) for D in Dc]
    assert len(commutant(spin9, 16)) == 1

    # Stabilizer of one spatial direction inside spin(9).
    S8rows = np.stack([D @ s0 for D in Dc]).T.tolist()
    co8 = P50.nullspace(S8rows)
    Spin8 = []
    for cv in co8:
        q = lcm(*[x.denominator for x in cv])
        Spin8.append(sum(int(x * q) * D for x, D in zip(cv, Dc)))
    assert len(Spin8) == 28
    R8 = [rep16(D) for D in Spin8]
    # The restricted 16 has a 2D commutant. Its traceless generator is an
    # exact chirality involution with 8+8 eigenspaces.
    com = commutant(R8, 16)
    assert len(com) == 2
    CM = [sp.Matrix(
        16, 16,
        [sp.Rational(x.numerator, x.denominator) for x in v])
        for v in com]
    Id16 = sp.eye(16)
    Y = next(M for M in CM if M - M[0, 0] * Id16 != sp.zeros(16, 16))
    Y0 = Y - (Y.trace() / 16) * Id16
    Y2 = Y0 * Y0
    lam = sp.Rational(Y2[0, 0])
    assert Y2 == lam * Id16 and lam > 0
    assert sp.sqrt(lam).is_Rational
    Chi = sp.simplify(Y0 / sp.sqrt(lam))
    assert Chi * Chi == Id16 and Chi.trace() == 0
    assert Chi.eigenvals() == {-1: 8, 1: 8}

    Pplus = (Id16 + Chi) / 2
    Pminus = (Id16 - Chi) / 2
    Bplus = independent_columns(Pplus, 8)
    Bminus = independent_columns(Pminus, 8)
    Rp = [restrict_to_subspace(R, Bplus) for R in R8]
    Rm = [restrict_to_subspace(R, Bminus) for R in R8]
    assert len(commutant(Rp, 8)) == 1
    assert len(commutant(Rm, 8)) == 1

    # No Spin8 intertwiner between the two 8s: solve A R+ = R- A.
    eqs = []
    for A, B in zip(Rp, Rm):
        for r in range(8):
            for c in range(8):
                row = [Fr(0)] * 64
                for k in range(8):
                    if A[k, c] != 0:
                        row[r * 8 + k] += Fr(A[k, c])
                    if B[r, k] != 0:
                        row[k * 8 + c] -= Fr(B[r, k])
                eqs.append(row)
    cross_intertwiners = P50.nullspace(eqs)
    assert len(cross_intertwiners) == 0
    # Build a deterministic spatial z orthogonal to s0, then the compact
    # rotation generator [L_s0,L_z] in spin(9).
    A0 = P50.nullspace(Lc.tolist())
    A0i = [np.array(
        [int(x * lcm(*[y.denominator for y in v])) for x in v],
        dtype=np.int64) for v in A0]
    uvec = evec - cvec

    def trform(x, y):
        return Fr(int(np.dot(trL, mulv(x, y))), 9 * den * den)

    uu = trform(uvec, uvec)
    spatial = []
    for v in A0i:
        coef = trform(v, uvec) / uu
        w = [Fr(int(a)) - coef * int(b) for a, b in zip(v, uvec)]
        q = lcm(*[x.denominator for x in w])
        spatial.append(np.array([int(x * q) for x in w], dtype=np.int64))
    sp9 = []
    for s in spatial:
        if P50.rank([x.tolist() for x in sp9 + [s]]) > len(sp9):
            sp9.append(s)
    assert len(sp9) == 9

    ss = trform(s0, s0)
    z = None
    for v in sp9:
        coef = trform(v, s0) / ss
        w = [Fr(int(a)) - coef * int(b) for a, b in zip(v, s0)]
        q = lcm(*[x.denominator for x in w])
        vv = np.array([int(x * q) for x in w], dtype=np.int64)
        if any(vv) and trform(vv, vv) != 0:
            z = vv
            break
    assert z is not None and trform(z, s0) == 0
    Drot = Lv(s0) @ Lv(z) - Lv(z) @ Lv(s0)
    assert P50.rank([m.flatten().tolist() for m in Dc] +
                    [Drot.flatten().tolist()]) == 36
    Rrot = rep16(Drot)
    # Read the angular frequency from the exact Peirce-0 vector action.
    A0mat = np.stack(A0i).T.astype(float)
    R0 = np.linalg.lstsq(
        A0mat, Drot.astype(float) @ A0mat, rcond=None)[0]
    evals0 = np.linalg.eigvals(R0)
    freq = sorted(abs(x.imag) for x in evals0 if abs(x.imag) > 1e-9)
    assert len(freq) == 2 and abs(freq[0] - freq[1]) < 1e-8
    omega = freq[0]

    Uhalf = expm(np.pi / omega * np.array(Rrot.tolist(), dtype=float))
    Ufull = expm(2 * np.pi / omega * np.array(Rrot.tolist(), dtype=float))
    Chif = np.array(Chi.evalf(), dtype=float)

    chirality_swap_error = float(np.linalg.norm(
        Uhalf @ Chif @ np.linalg.inv(Uhalf) + Chif))
    square_error = float(np.linalg.norm(Uhalf @ Uhalf - Ufull))
    matter_parity_error = float(np.linalg.norm(Ufull + np.eye(16)))
    order4_error = float(np.linalg.norm(
        np.linalg.matrix_power(Uhalf, 4) - np.eye(16)))
    assert chirality_swap_error < TOL
    assert square_error < TOL
    assert matter_parity_error < TOL
    assert order4_error < TOL

    # On the Peirce-0 vector module, the half-turn sends s0 to -s0, so it
    # normalizes the stabilizer of the unoriented axis {+/-s0}.
    A0M = sp.Matrix(np.stack(A0i).T.tolist())
    A0pinv = (A0M.T * A0M).inv() * A0M.T
    s0c = np.array(
        [float(x) for x in A0pinv * sp.Matrix(s0.tolist())])
    U0half = expm(np.pi / omega * R0)
    axis_flip_error = float(np.linalg.norm(U0half @ s0c + s0c))
    assert axis_flip_error < TOL
    # Explicitly confirm the half-turn swaps the two projector images.
    swap_plus_error = float(np.linalg.norm(
        Uhalf @ np.array(Pplus.evalf(), dtype=float)
        @ Uhalf.T - np.array(Pminus.evalf(), dtype=float)))
    swap_minus_error = float(np.linalg.norm(
        Uhalf @ np.array(Pminus.evalf(), dtype=float)
        @ Uhalf.T - np.array(Pplus.evalf(), dtype=float)))
    assert swap_plus_error < TOL and swap_minus_error < TOL

    p50cert = json.loads(
        (ROOT / "data/w33_pass10950_clock_albert_lorentz_spinor.json")
        .read_text(encoding="utf-8"))
    assert p50cert["lorentz"]["Der_c_dimension"] == 36
    assert p50cert["lorentz"]["spinor_module_dimension"] == 16
    assert p50cert["matter_parity"]["two_pi_rotation_equals_U_s_max_error"] < TOL

    p55 = json.loads(
        (ROOT / "data/w33_pass10955_d4_halfspin_clock_bridge.json")
        .read_text(encoding="utf-8"))
    assert p55["outer_D4_action"]["outer_image"] == "C2 inside Out(D4)=S3"
    assert p55["clock"]["one_tick"] == "S+ <-> S-"

    chi_payload = json.dumps(
        matrix_rational_strings(Chi), sort_keys=True).encode()
    chi_sha = hashlib.sha256(chi_payload).hexdigest()
    out = {
        "schema": "w33.pass10956.albert-spin8-halfspin-normalizer.v1",
        "status": "PASS_ALBERT_SPIN8_HALFSPIN_NORMALIZER_BRIDGE",
        "parent_albert": {
            "pass10950_status": p50cert["status"],
            "spin9_dimension": len(Dc),
            "peirce_spinor_dimension": 16,
        },
        "spin8_stabilizer": {
            "chosen_spatial_axis": "s0=e_g2-e_g3",
            "dimension": len(Spin8),
            "expected": "spin(8)",
            "restriction_commutant_dimension": len(com),
            "halfspin_plus_dimension": 8,
            "halfspin_minus_dimension": 8,
            "plus_commutant_dimension": len(commutant(Rp, 8)),
            "minus_commutant_dimension": len(commutant(Rm, 8)),
            "cross_intertwiner_dimension": len(cross_intertwiners),
            "branching": "16 -> 8_s + 8_c under Spin(8)",
        },
        "chirality_involution": {
            "square": "+I16",
            "trace": 0,
            "eigenvalue_multiplicities": {"+1": 8, "-1": 8},
            "exact_rational_matrix_sha256": chi_sha,
            "commutes_with_all_spin8_generators": True,
        },
        "spin9_normalizer_halfturn": {
            "generator": "[L_s0,L_z] with z spatial and orthogonal to s0",
            "vector_plane_frequency": omega,
            "axis_flip_error": axis_flip_error,
            "chirality_conjugation_to_minus_error": chirality_swap_error,
            "plus_to_minus_projector_error": swap_plus_error,
            "minus_to_plus_projector_error": swap_minus_error,
            "square_equals_full_2pi_error": square_error,
            "two_pi_equals_minus_I16_error": matter_parity_error,
            "fourth_power_identity_error": order4_error,
            "reading":
                "a pi rotation in Spin(9) normalizing the unoriented Spin(8) axis exchanges 8_s and 8_c; its square is the central 2pi spin sign",
        },
        "pass10955_weld": {
            "finite_D4_outer_action":
                "det-minus clock/tetracode elements fix 8_v and exchange 8_s <-> 8_c",
            "albert_realization":
                "the executable Peirce 16 has the same Spin(8) half-spin transposition realized by a Spin(9) normalizer half-turn",
            "common_outer_class": "the transposition of the two half-spin nodes fixing the vector node",
            "not_yet_proved":
                "no homomorphism/intertwiner sends the full order-eight GL(2,3) clock generator to this order-four Spin(9) half-turn",
        },
        "matter_parity_chain": {
            "halfturn_squared": "-I on the Peirce 16",
            "pass10950": "the same -I is the 2pi Spin(9) matter-parity sign",
            "pass10951": "the finite clock has g^4=-I in its spin central character",
            "firewall":
                "the powers differ, so this is a shared central/outer structure, not equality of the clock generator with the half-turn",
        },
        "theorem": (
            "Inside the executable Pass10950 clock Albert algebra, the stabilizer "
            "of one spatial Peirce-0 direction in compact spin(9) has dimension 28. "
            "Its action on the Peirce 16 has a two-dimensional commutant generated "
            "by identity and an exact involution with 8+8 eigenspaces; each eigenspace "
            "is irreducible and there is no Spin(8) intertwiner between them. Thus "
            "the certified 16 restricts objectwise as 8_s+8_c. An explicit pi rotation "
            "in Spin(9) sends the chosen spatial axis to its negative, normalizes the "
            "same unoriented Spin(8), conjugates the chirality involution to its negative, "
            "and exchanges the two 8D projector images. Its square is -I16, the already "
            "certified 2pi matter-parity sign. This realizes on the actual Albert spinor "
            "the same D4 outer transposition found abstractly for the Pass10955 clock "
            "group, while leaving the full order-eight clock intertwiner open."
        ),
        "boundary": (
            "This is an executable branching and normalizer theorem inside the finite "
            "Albert/Spin representation. It does not identify the two half-spin modules "
            "with observed left/right fermions, derive spacetime chirality, or map the "
            "full GL(2,3) order-eight clock into Spin(9)."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "spin8_dim": len(Spin8),
        "branching": out["spin8_stabilizer"]["branching"],
        "swap_error": chirality_swap_error,
        "matter_parity_error": matter_parity_error,
    }, indent=2))


if __name__ == "__main__":
    main()
