#!/usr/bin/env python3
"""
Sample many non-commuting Z3 pairs and collect statistics:
 - mixing probability matrix (3x3)
 - reconstructed unitary unitarity error
 - Jarlskog invariant

Writes data/ckm_sample_stats.json
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import time
import sys

sys.path.insert(0, str(Path(__file__).parent))
import w33_ckm_mixing as mix


def leading_rep(V: np.ndarray) -> np.ndarray:
    U, s, VT = np.linalg.svd(V, full_matrices=False)
    rep = U[:, 0]
    idx = int(np.argmax(np.abs(rep)))
    if rep[idx] != 0:
        phase = np.angle(rep[idx])
        rep = rep * np.exp(-1j * phase)
    return rep


def orthonormalize(Q: np.ndarray) -> np.ndarray:
    Qr, R = np.linalg.qr(Q)
    d = np.diag(R)
    s = np.sign(np.real(d))
    s[s == 0] = 1
    Qr = Qr * s
    return Qr


def compute_jarlskog(V: np.ndarray) -> float:
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


def main(sample_target: int = 50):
    t0 = time.time()
    data = mix.build_all(verbose=False)
    order3, refined_map = mix.classify_order3_conjugacy(data)

    all_indices = list(range(len(order3)))
    results = []
    pair_count = 0

    for i in range(len(all_indices)):
        if pair_count >= sample_target:
            break
        for j in range(i + 1, len(all_indices)):
            v1 = order3[all_indices[i]][0]
            v2 = order3[all_indices[j]][0]
            g1g2 = tuple(v1[k] for k in v2)
            g2g1 = tuple(v2[k] for k in v1)
            if g1g2 == g2g1:
                continue

            s1 = mix.compute_generation_eigenspaces(data, order3[all_indices[i]])
            s2 = mix.compute_generation_eigenspaces(data, order3[all_indices[j]])
            M = mix.compute_mixing_matrix(s1, s2)

            # skip trivial (identity-like)
            if np.max(M) > 0.99:
                continue

            # reconstruct unitary via leading reps
            labels = ["1", "w", "wb"]
            reps1 = np.column_stack([leading_rep(s1[l]) for l in labels])
            reps2 = np.column_stack([leading_rep(s2[l]) for l in labels])
            Q1 = orthonormalize(reps1)
            Q2 = orthonormalize(reps2)
            V = Q1.conj().T @ Q2
            unitarity_err = float(np.linalg.norm(V @ V.conj().T - np.eye(3)))
            J = compute_jarlskog(V)

            results.append(
                {
                    "pair": [all_indices[i], all_indices[j]],
                    "max_M": float(np.max(M)),
                    "mean_M": float(np.mean(M)),
                    "unitarity_err": unitarity_err,
                    "jarlskog": J,
                }
            )
            pair_count += 1
            if pair_count >= sample_target:
                break

    arr_unit = np.array([r["unitarity_err"] for r in results]) if results else np.array([])
    arr_j = np.array([r["jarlskog"] for r in results]) if results else np.array([])

    summary = {
        "n_samples": len(results),
        "unitarity_mean": float(np.mean(arr_unit)) if arr_unit.size else None,
        "unitarity_std": float(np.std(arr_unit)) if arr_unit.size else None,
        "jarlskog_mean": float(np.mean(arr_j)) if arr_j.size else None,
        "jarlskog_std": float(np.std(arr_j)) if arr_j.size else None,
    }

    out = {"summary": summary, "results": results}
    Path("data/ckm_sample_stats.json").write_text(json.dumps(out, indent=2))

    print("Wrote data/ckm_sample_stats.json")
    print("Samples:", len(results))
    if arr_unit.size:
        print(f"Unitary err mean={summary['unitarity_mean']:.4f}, std={summary['unitarity_std']:.4f}")
    if arr_j.size:
        print(f"Jarlskog mean={summary['jarlskog_mean']:.4e}, std={summary['jarlskog_std']:.4e}")
    print("elapsed:", time.time() - t0)


if __name__ == "__main__":
    raise SystemExit(main())
