#!/usr/bin/env python3
"""BT1042: first-order condition verifier for the BT1041 candidate.

On HS(K), left and right multiplication commute.  For
D_F = sigma_x tensor (L_Phi + R_Phi), the relevant commutator is

  [D_F, L_a] = sigma_x tensor L_[Phi,a]

because R_Phi commutes with L_a.  Since every left multiplication commutes with
every right multiplication, the first-order condition

  [[D_F,L_a], R_b] = 0

holds for all generator pairs.  This script verifies the statement numerically on
the BT1038/BT1041 generator spans.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def E(n: int, i: int, j: int) -> np.ndarray:
    M = np.zeros((n, n), dtype=complex)
    M[i, j] = 1
    return M


def embed_weak(A: np.ndarray) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[1:3, 1:3] = A
    return out


def weak_color_generators() -> list[np.ndarray]:
    I3 = np.eye(3, dtype=complex)
    gens: list[np.ndarray] = []
    gens.append(np.kron(np.diag([1, 0, 0]), I3))
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    for S in [sx, sy, sz]:
        gens.append(np.kron(embed_weak(S), I3))
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        gens.append(np.kron(I3, E(3, i, j) + E(3, j, i)))
        gens.append(np.kron(I3, 1j * (E(3, i, j) - E(3, j, i))))
    gens.append(np.kron(I3, np.diag([1, -1, 0])))
    gens.append(np.kron(I3, np.diag([1, 1, -2])))
    return gens


def left(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    return np.kron(A, np.eye(n, dtype=complex))


def right(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    return np.kron(np.eye(n, dtype=complex), A.T)


def comm(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return A @ B - B @ A


def main() -> None:
    gens = weak_color_generators()
    # Hermitian Higgs sample connecting weak singlet to first weak doublet, color singlet.
    Phi_w = E(3, 0, 1) + E(3, 1, 0)
    Phi = np.kron(Phi_w, np.eye(3, dtype=complex))
    LPhi = left(Phi)
    RPhi = right(Phi)
    max_norm = 0.0
    tested = 0
    for a in gens:
        La = left(a)
        finite_comm = comm(LPhi + RPhi, La)
        for b in gens:
            Rb = right(b)
            c = comm(finite_comm, Rb)
            max_norm = max(max_norm, float(np.linalg.norm(c)))
            tested += 1
    out = {
        "theorem": "BT1042 first-order condition verifier",
        "carrier": "HS(K), K=C^3_weakslot tensor C^3_color, dim HS(K)=81; chiral factor omitted because sigma_x is common",
        "generator_count": len(gens),
        "pairs_tested": tested,
        "max_commutator_norm": max_norm,
        "tolerance": 1e-9,
        "first_order_pass": max_norm < 1e-9,
        "identity_used": "[[L_Phi+R_Phi,L_a],R_b]=[L_[Phi,a],R_b]=0",
        "boundary": "This verifies first-order for the block candidate generator span and sample Higgs direction; full physical Yukawa texture still requires choosing all Phi components/couplings."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1042_first_order_condition_verifier.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
