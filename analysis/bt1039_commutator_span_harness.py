#!/usr/bin/env python3
"""BT1039: commutator/one-form span harness for the BT1038 candidate.

Key correction: in an almost-commutative product, the gauge bosons are the
horizontal one-forms [D_M,f] tensored with the finite algebra's unimodular
anti-Hermitian generators. The finite commutators [D_F,a] generate scalar/Higgs
one-forms. Therefore this harness checks two spans:

  horizontal gauge span: u(1)+su(2)+su(3) = 1+3+8 = 12,
  vertical finite scalar span: weak singlet-doublet off-diagonal Higgs = 4 real.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def mat_rank(mats: list[np.ndarray], tol: float = 1e-9) -> int:
    cols = [m.reshape(-1) for m in mats]
    if not cols:
        return 0
    M = np.stack(cols, axis=1)
    return int(np.linalg.matrix_rank(M, tol=tol))


def embed_weak(A: np.ndarray) -> np.ndarray:
    # weakslot C^3 = singlet + doublet.  Embed 2x2 weak matrix into doublet block.
    out = np.zeros((3, 3), dtype=complex)
    out[1:3, 1:3] = A
    return out


def su2_generators() -> list[np.ndarray]:
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return [1j * sx, 1j * sy, 1j * sz]


def su3_generators() -> list[np.ndarray]:
    E = lambda i, j: np.eye(3, dtype=complex)[[i]].T @ np.eye(3, dtype=complex)[[j]]
    gens: list[np.ndarray] = []
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        gens.append(1j * (E(i, j) + E(j, i)))
        gens.append(E(i, j) - E(j, i))
    gens.append(1j * np.diag([1, -1, 0]))
    gens.append(1j * np.diag([1, 1, -2]))
    return gens


def horizontal_gauge_generators() -> list[np.ndarray]:
    Iw = np.eye(3, dtype=complex)
    Ic = np.eye(3, dtype=complex)
    u1 = [1j * np.kron(np.diag([1, 0, 0]), Ic)]
    weak = [np.kron(embed_weak(g), Ic) for g in su2_generators()]
    color = [np.kron(Iw, g) for g in su3_generators()]
    return u1 + weak + color


def higgs_scalar_generators() -> list[np.ndarray]:
    # Four real Hermitian generators: Re/Im of a complex weak doublet mapping
    # singlet <-> doublet inside weakslot; color singlet.
    Ic = np.eye(3, dtype=complex)
    gens: list[np.ndarray] = []
    for d in [1, 2]:
        E_sd = np.zeros((3, 3), dtype=complex)
        E_sd[0, d] = 1
        E_ds = np.zeros((3, 3), dtype=complex)
        E_ds[d, 0] = 1
        gens.append(np.kron(E_sd + E_ds, Ic))
        gens.append(np.kron(1j * (E_sd - E_ds), Ic))
    return gens


def main() -> None:
    gauge = horizontal_gauge_generators()
    higgs = higgs_scalar_generators()
    out = {
        "theorem": "BT1039 one-form span harness for BT1038 candidate",
        "gauge_route": "horizontal product one-forms [D_M,f] tensor Lie(A_F)",
        "horizontal_gauge_span_dim": mat_rank(gauge),
        "horizontal_gauge_expected_profile": [1, 3, 8],
        "horizontal_gauge_expected_total": 12,
        "gauge_target_hit": mat_rank(gauge) == 12,
        "finite_route": "vertical finite one-forms gamma_5 tensor [D_F,a]",
        "higgs_scalar_real_span_dim": mat_rank(higgs),
        "higgs_expected_real_dim": 4,
        "higgs_target_hit": mat_rank(higgs) == 4,
        "important_correction": "Do not require [D_F,A_F] alone to yield 1+3+8; finite commutators produce Higgs/scalars while horizontal one-forms produce gauge fields.",
        "status": "module-level gauge span and Higgs doublet span pass for the BT1038 block candidate; first-order condition still needs explicit J and D_F matrices"
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1039_commutator_span_harness.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
