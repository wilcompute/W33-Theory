#!/usr/bin/env python3
"""Restricted conjugation probe: only basis changes preserving the invariant line are tested.

Writes `data/transport_cocycle_restricted_conjugation_results.json`.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

import numpy as np
from w33_transport_ternary_cocycle_bridge import adapted_reduced_transport_group


MOD = 3


def mat_mod3(a):
    return np.array(a, dtype=int) % MOD


def det_mod3(A: np.ndarray) -> int:
    return int(round(float(np.linalg.det(A)))) % MOD


def inv_mod3(A: np.ndarray) -> np.ndarray:
    d = det_mod3(A)
    if d == 0:
        raise ValueError("singular")
    adj = np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]], dtype=int) % MOD
    invd = pow(d, -1, MOD)
    return (invd * adj) % MOD


def gen_gl2_3():
    mats = []
    for entries in product(range(MOD), repeat=4):
        A = np.array([[entries[0], entries[1]], [entries[2], entries[3]]], dtype=int)
        if det_mod3(A) != 0:
            mats.append(mat_mod3(A))
    return mats


def preserves_line(B: np.ndarray, v: np.ndarray) -> bool:
    # check B*v proportional to v (scalar in F3)
    r = (B @ v) % MOD
    if np.all(r == 0):
        return False
    # try scalars 1 and 2
    for s in (1, 2):
        if np.array_equal(r, (s * v) % MOD):
            return True
    return False


def is_upper_tri(M: np.ndarray) -> bool:
    return int(M[1, 0]) % MOD == 0


def main():
    group = adapted_reduced_transport_group()
    inv = np.array([1, 2], dtype=int) % MOD
    gl = gen_gl2_3()
    results = []
    for B in gl:
        if not preserves_line(B, inv):
            continue
        try:
            B_inv = inv_mod3(B)
        except ValueError:
            continue
        transformed = [mat_mod3((B_inv @ M @ B)) for M in group]
        c_trivial = [int(T[0, 1]) % MOD for T in transformed if int(T[1, 1]) % MOD == 1]
        c_nontrivial = [int(T[0, 1]) % MOD for T in transformed if int(T[1, 1]) % MOD == 2]
        is_trivial_on_trivial = all(x == 0 for x in c_trivial)
        is_constant_on_nontrivial = len(set(c_nontrivial)) <= 1
        is_coboundary = is_trivial_on_trivial and is_constant_on_nontrivial
        results.append(
            {
                "B": B.tolist(),
                "B_inv": B_inv.tolist(),
                "c_trivial_values": c_trivial,
                "c_nontrivial_values": c_nontrivial,
                "is_trivial_on_trivial": is_trivial_on_trivial,
                "is_constant_on_nontrivial": is_constant_on_nontrivial,
                "is_coboundary": is_coboundary,
            }
        )

    out = Path("data") / "transport_cocycle_restricted_conjugation_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    import json

    out.write_text(json.dumps({"found": bool(results, encoding="utf-8"), "cases": results}, indent=2))
    print(f"Wrote {out}; found={bool(results)}; cases={len(results)}")


if __name__ == "__main__":
    main()
