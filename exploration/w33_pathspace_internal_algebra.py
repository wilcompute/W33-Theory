"""
Candidate bridge past the 2026-04-09 spectral-triple obstruction.

Core idea:
- The vertex Bose-Mesner algebra of W(3,3) is commutative and too small.
- The enriched object
    (Hashimoto path space) + (shell doublet) + (Heisenberg qutrit fiber)
  naturally carries a candidate internal algebra

      A_cand = C + H + M_3(C)

  where:
    * C comes from the trivial Hashimoto line,
    * H comes from the two nontrivial Hashimoto shell channels (radius/shadow),
    * M_3(C) comes from the qutrit Weyl-Heisenberg action on the Payne 27-sector.

This script does not prove the full Connes NCG package. It gives an explicit
noncommutative candidate internal algebra built on the enriched W33 object,
rather than on the 40-vertex commutant alone.
"""
from __future__ import annotations
import cmath
import math
from typing import Dict, List, Tuple

import numpy as np

# W(3,3) / SRG(40,12,2,4) parameters
V, K, LAM, MU = 40, 12, 2, 4
Q = 3
omega = cmath.exp(2j * math.pi / 3)


def hashimoto_roots(lam: int, k: int = K) -> Tuple[complex, complex]:
    disc = lam * lam - 4 * (k - 1)
    if disc >= 0:
        root = math.sqrt(disc)
        return ((lam + root) / 2, (lam - root) / 2)
    return (
        complex(lam / 2, math.sqrt(-disc) / 2),
        complex(lam / 2, -math.sqrt(-disc) / 2),
    )


# Nontrivial Hashimoto shell channels
beta_r, beta_r_bar = hashimoto_roots(LAM)
beta_s, beta_s_bar = hashimoto_roots(-MU)

# Quaternionic shell sector
I2 = np.eye(2, dtype=complex)
qi = np.array([[1j, 0], [0, -1j]], dtype=complex)
qj = np.array([[0, 1], [-1, 0]], dtype=complex)
qk = qi @ qj


def is_close(A, B, tol=1e-10):
    return np.allclose(A, B, atol=tol, rtol=0)


def quaternion_relations() -> Dict[str, bool]:
    out = {}
    out["i2=-1"] = is_close(qi @ qi, -I2)
    out["j2=-1"] = is_close(qj @ qj, -I2)
    out["k2=-1"] = is_close(qk @ qk, -I2)
    out["ij=k"] = is_close(qi @ qj, qk)
    out["jk=i"] = is_close(qj @ qk, qi)
    out["ki=j"] = is_close(qk @ qi, qj)
    out["ijk=-1"] = is_close(qi @ qj @ qk, -I2)
    return out


D_shell = np.diag([beta_r, beta_s]).astype(complex)


def shell_summary() -> Dict[str, object]:
    return {
        "beta_r": complex(beta_r),
        "beta_s": complex(beta_s),
        "modulus_sq_r": abs(beta_r) ** 2,
        "modulus_sq_s": abs(beta_s) ** 2,
        "real_gap_sq": (beta_s.real ** 2 - beta_r.real ** 2),
        "imag_gap_sq": (beta_r.imag ** 2 - beta_s.imag ** 2),
        "D_shell_trace": np.trace(D_shell),
        "D_shell_det": np.linalg.det(D_shell),
    }


# Qutrit / Heisenberg color sector
I3 = np.eye(3, dtype=complex)
X = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
Z = np.diag([1, omega, omega**2]).astype(complex)


def heisenberg_span_basis() -> List[np.ndarray]:
    mats = []
    for a in range(3):
        Xa = np.linalg.matrix_power(X, a)
        for b in range(3):
            Zb = np.linalg.matrix_power(Z, b)
            mats.append(Xa @ Zb)
    return mats


def complex_rank(mats: List[np.ndarray]) -> int:
    cols = []
    for M in mats:
        cols.append(M.reshape(-1))
    A = np.stack(cols, axis=1)
    A_real = np.block([[A.real, -A.imag], [A.imag, A.real]])
    return np.linalg.matrix_rank(A_real) // 2


def heisenberg_relations() -> Dict[str, object]:
    mats = heisenberg_span_basis()
    return {
        "XZ=omega ZX": is_close(X @ Z, omega * (Z @ X)),
        "X3=1": is_close(np.linalg.matrix_power(X, 3), I3),
        "Z3=1": is_close(np.linalg.matrix_power(Z, 3), I3),
        "basis_rank": complex_rank(mats),
    }


# Candidate internal algebra as block operators on C + C^2 + C^3
I1 = np.array([[1]], dtype=complex)


def block_diag(*blocks):
    sizes = [b.shape[0] for b in blocks]
    n = sum(sizes)
    out = np.zeros((n, n), dtype=complex)
    s = 0
    for b in blocks:
        m = b.shape[0]
        out[s : s + m, s : s + m] = b
        s += m
    return out


G_scalar = block_diag(I1, np.zeros((2, 2), complex), np.zeros((3, 3), complex))
G_qi = block_diag(np.zeros((1, 1), complex), qi, np.zeros((3, 3), complex))
G_qj = block_diag(np.zeros((1, 1), complex), qj, np.zeros((3, 3), complex))
G_qk = block_diag(np.zeros((1, 1), complex), qk, np.zeros((3, 3), complex))
G_X = block_diag(np.zeros((1, 1), complex), np.zeros((2, 2), complex), X)
G_Z = block_diag(np.zeros((1, 1), complex), np.zeros((2, 2), complex), Z)


def commutator(A, B):
    return A @ B - B @ A


def candidate_dirac() -> np.ndarray:
    trivial = np.array([[1]], dtype=complex)
    shell = D_shell
    color = np.diag([0, 1, -1]).astype(complex)
    return block_diag(trivial, shell, color)


def summary() -> Dict[str, object]:
    qrels = quaternion_relations()
    hrels = heisenberg_relations()
    D = candidate_dirac()
    return {
        "srg": {"V": V, "K": K, "LAM": LAM, "MU": MU, "q": Q},
        "shell": shell_summary(),
        "quaternion_relations": qrels,
        "heisenberg_relations": hrels,
        "candidate_algebra_blocks": ["C", "H", "M3(C)"],
        "candidate_state_dim": int(D.shape[0]),
        "noncommutativity_checks": {
            "[qi,qj]!=0": not is_close(commutator(G_qi, G_qj), np.zeros_like(G_qi)),
            "[X,Z]!=0": not is_close(commutator(G_X, G_Z), np.zeros_like(G_X)),
            "[qi,X]=0 (separate blocks)": is_close(
                commutator(G_qi, G_X), np.zeros_like(G_qi)
            ),
        },
        "dirac_trace": complex(np.trace(D)),
        "dirac_det": complex(np.linalg.det(D)),
    }


def assert_all():
    qrels = quaternion_relations()
    assert all(qrels.values()), qrels
    hrels = heisenberg_relations()
    assert hrels["XZ=omega ZX"]
    assert hrels["X3=1"]
    assert hrels["Z3=1"]
    assert hrels["basis_rank"] == 9, hrels["basis_rank"]
    shell = shell_summary()
    assert abs(shell["modulus_sq_r"] - 11) < 1e-10
    assert abs(shell["modulus_sq_s"] - 11) < 1e-10
    assert abs(shell["real_gap_sq"] - 3) < 1e-10
    assert abs(shell["imag_gap_sq"] - 3) < 1e-10
    assert not is_close(commutator(G_qi, G_qj), np.zeros_like(G_qi))
    assert not is_close(commutator(G_X, G_Z), np.zeros_like(G_X))


if __name__ == "__main__":
    assert_all()
    import json

    def encode(obj):
        if isinstance(obj, complex):
            return {"re": obj.real, "im": obj.imag}
        if isinstance(obj, np.complexfloating):
            return {"re": float(obj.real), "im": float(obj.imag)}
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        raise TypeError(f"Cannot encode type {type(obj)}")

    print(json.dumps(summary(), indent=2, default=encode))
