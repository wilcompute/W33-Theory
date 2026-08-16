#!/usr/bin/env python3
"""Pass5675: exact normal form of the stabilizer-equivariant deck-odd BdG cone.

Pass5630 proves that, for the 96-element vector Segre stabilizer G,

    V_16 ~= 2 A + 2 Abar,

with A a non-real irreducible complex G-module of dimension four, and that the
G-equivariant Hermitian Hamiltonians satisfying ordinary-conjugation particle-hole
symmetry K H K^{-1}=-H form a four-real-dimensional space.

Schur's lemma then fixes the whole cone, not just its dimension.  After choosing the
multiplicity spaces,

    H_X = (I_A tensor X)  +  (I_Abar tensor -conj(X)),

where X is an arbitrary Hermitian 2x2 matrix.  Consequently every such Hamiltonian
has spectrum

    lambda_1^4 + lambda_2^4 + (-lambda_1)^4 + (-lambda_2)^4,

where superscripts denote multiplicity, and it obeys

    H^4 - s H^2 + p I = 0,
    s=lambda_1^2+lambda_2^2,  p=lambda_1^2 lambda_2^2.

Modulo G-equivariant unitary basis changes, X can be diagonalized.  After removing
one overall nonzero energy scale there remains one continuous dimensionless level
ratio |lambda_2/lambda_1| (plus discrete signature data).  Thus no nonzero mass
ratio, including the magnetic value 2, is protected by G + deck parity + K alone.

The numerical part replays Pass5630 and checks the quartic normal form on deterministic
random points of the full four-dimensional allowed cone.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected as prev

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5675_DECK16_EQUIVARIANT_BDG_NORMAL_FORM.json"


def pair_comp(a, b):
    p, s = a
    q, t = b
    return (tuple(p[q[i]] for i in range(16)), tuple(t[i] * s[q[i]] for i in range(16)))


def pair_closure(gs):
    e = (tuple(range(16)), tuple([1] * 16))
    G = {e}
    front = [e]
    while front:
        x = front.pop()
        for g in gs:
            y = pair_comp(g, x)
            if y not in G:
                G.add(y)
                front.append(y)
    return G


def skew_commutant_basis(pairs):
    gens = []
    cur = {(tuple(range(16)), tuple([1] * 16))}
    for c in pairs:
        if c not in cur:
            test = pair_closure(gens + [c])
            if len(test) > len(cur):
                gens.append(c)
                cur = test
            if len(cur) == 96:
                break
    assert len(cur) == 96
    GR = [prev.signed_matrix(x) for x in gens]
    C = np.vstack([
        np.kron(R.T, np.eye(16)) - np.kron(np.eye(16), R)
        for R in GR
    ])
    _, sing, vh = np.linalg.svd(C)
    nullity = int(np.sum(sing < 1e-9))
    assert nullity == 8
    N = vh[-nullity:].T
    Bs = [N[:, i].reshape(16, 16, order="F") for i in range(nullity)]
    skw = np.column_stack([
        ((X - X.T) / 2).reshape(-1, order="F") for X in Bs
    ])
    U, s, _ = np.linalg.svd(skw, full_matrices=False)
    rank = int(np.sum(s > 1e-9))
    assert rank == 4
    return [U[:, i].reshape(16, 16, order="F") for i in range(rank)]


def cluster(vals, tol=1e-7):
    out = []
    for x in vals:
        if not out or abs(x - out[-1][0]) > tol:
            out.append([float(x), 1])
        else:
            out[-1][1] += 1
    return out


def main():
    pairs, Rs, Hmag = prev.build()
    basis = skew_commutant_basis(pairs)
    rng = np.random.default_rng(5675)
    sample_ratios = []
    max_poly_residual = 0.0
    for _ in range(12):
        coeff = rng.normal(size=4)
        S = sum(c * B for c, B in zip(coeff, basis))
        H = 1j * S
        assert np.max(abs(H - H.conj().T)) < 1e-9
        assert max(np.max(abs(R @ H - H @ R)) for R in Rs) < 1e-8
        assert np.max(abs(H.conj() + H)) < 1e-9
        ev = np.linalg.eigvalsh(H)
        cl = cluster(ev)
        assert len(cl) == 4 and [m for _, m in cl] == [4, 4, 4, 4]
        assert abs(cl[0][0] + cl[3][0]) < 1e-7
        assert abs(cl[1][0] + cl[2][0]) < 1e-7
        a, b = abs(cl[2][0]), abs(cl[3][0])
        if a > 1e-10:
            sample_ratios.append(float(b / a))
        s = a * a + b * b
        p = a * a * b * b
        Rpoly = H @ H @ H @ H - s * (H @ H) + p * np.eye(16)
        max_poly_residual = max(max_poly_residual, float(np.max(abs(Rpoly))))
    assert max_poly_residual < 1e-8

    # The intrinsic magnetic point is the special X with absolute eigenvalues 3,6.
    mev = np.linalg.eigvalsh(Hmag)
    assert np.allclose(mev, [-6]*4 + [-3]*4 + [3]*4 + [6]*4, atol=1e-8)
    magnetic_poly = np.max(abs(
        Hmag @ Hmag @ Hmag @ Hmag - 45 * (Hmag @ Hmag) + 324 * np.eye(16)
    ))
    assert magnetic_poly < 1e-8

    out = {
        "pass": 5675,
        "status": "FULL_EQUIVARIANT_CLASS_D_CONE_IS_HERM2_WITH_ONE_CONTINUOUS_RATIO_AFTER_SCALE",
        "input_module": "V16 = 2 A + 2 Abar, dim A=4, A non-real irreducible",
        "normal_form": "H_X = I_A tensor X direct-sum I_Abar tensor (-conj X), X Hermitian 2x2",
        "real_parameter_dimension": 4,
        "spectrum": "lambda1^4, lambda2^4, (-lambda1)^4, (-lambda2)^4",
        "annihilator": "H^4-(lambda1^2+lambda2^2)H^2+(lambda1^2 lambda2^2)I=0",
        "moduli_after_equivariant_unitary_conjugacy": "two real eigenvalues of X, unordered",
        "moduli_after_nonzero_overall_scale": "one continuous absolute level ratio plus discrete signature",
        "magnetic_point": {
            "absolute_levels": [3, 6],
            "ratio": 2,
            "annihilator": "H^4-45H^2+324I=0"
        },
        "numerical_replay": {
            "samples": 12,
            "all_level_multiplicities": [4, 4, 4, 4],
            "sample_ratio_min": min(sample_ratios),
            "sample_ratio_max": max(sample_ratios),
            "max_quartic_residual": max_poly_residual
        },
        "theorem": "Carrier symmetry plus K particle-hole symmetry fixes the fourfold degeneracy pattern but leaves a continuous dimensionless two-level ratio. The value 2 is not protected.",
        "physics_boundary": "This is a finite stabilizer-equivariant BdG normal form. It does not assign the two levels to physical particles and leaves the overall dimensionful scale free."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
