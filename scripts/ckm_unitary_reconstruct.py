#!/usr/bin/env python3
"""
Reconstruct a 3x3 unitary mixing matrix from W33 Z3 eigenspaces
and compute the Jarlskog invariant (approx).

Algorithm:
 - Build W33 and classify order-3 elements
 - Pick two non-commuting representatives
 - Compute their generation eigenspaces (81 x 27 complex per gen)
 - For each 27-d generation, take the leading left-singular vector
 - Orthonormalize the three representative vectors to form 81x3 Q
 - Compute V = Q1^† Q2, report |V| and Jarlskog
"""

from __future__ import annotations

import time
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w33_ckm_mixing as mix


def leading_rep(V: np.ndarray) -> np.ndarray:
    """Return principal 81-d representative vector for 81x27 subspace V."""
    U, s, VT = np.linalg.svd(V, full_matrices=False)
    rep = U[:, 0]
    # fix global phase so largest component is real positive
    idx = int(np.argmax(np.abs(rep)))
    if rep[idx] != 0:
        phase = np.angle(rep[idx])
        rep = rep * np.exp(-1j * phase)
    return rep


def orthonormalize(Q: np.ndarray) -> np.ndarray:
    Qr, R = np.linalg.qr(Q)
    # ensure positive diagonal
    d = np.diag(R)
    s = np.sign(np.real(d))
    s[s == 0] = 1
    Qr = Qr * s
    return Qr


def compute_jarlskog(V: np.ndarray) -> float:
    # J = Im(V11 V22 V12* V21*) (one of equivalent expressions)
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


def main():
    t0 = time.time()
    data = mix.build_all(verbose=False)
    order3, refined_map = mix.classify_order3_conjugacy(data)

    # pick two non-commuting representatives (fall back to two classes)
    if len(refined_map) < 2:
        indices = list(refined_map.values())[0]
        el1 = order3[indices[0]]
        el2 = None
        for idx in indices[1:]:
            cand = order3[idx]
            v1, v2 = el1[0], cand[0]
            if tuple(v1[i] for i in v2) != tuple(v2[i] for i in v1):
                el2 = cand
                break
        if el2 is None:
            el2 = order3[indices[1]]
    else:
        keys = sorted(refined_map.keys())
        el1 = order3[refined_map[keys[0]][0]]
        el2 = order3[refined_map[keys[1]][0]]

    s1 = mix.compute_generation_eigenspaces(data, el1)
    s2 = mix.compute_generation_eigenspaces(data, el2)

    labels = ["1", "w", "wb"]
    reps1 = np.column_stack([leading_rep(s1[l]) for l in labels])
    reps2 = np.column_stack([leading_rep(s2[l]) for l in labels])

    Q1 = orthonormalize(reps1)
    Q2 = orthonormalize(reps2)

    V = Q1.conj().T @ Q2
    unitarity_err = np.linalg.norm(V @ V.conj().T - np.eye(3))
    mags = np.abs(V)
    J = compute_jarlskog(V)

    np.set_printoptions(precision=5, suppress=True)
    print("\n3x3 mixing matrix V (complex):")
    print(V)
    print("\n|V|:")
    print(mags)
    print("\nUnitarity error ||V V^† - I|| =", unitarity_err)
    print("Jarlskog J =", J)
    print("elapsed =", time.time() - t0)


if __name__ == "__main__":
    main()
