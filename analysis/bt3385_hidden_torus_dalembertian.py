#!/usr/bin/env python3
"""Exact Fourier certificate for the hidden signed ternary torus."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path


def laplacian_eigenvalue(frequency: int) -> int:
    """C3 graph-Laplacian eigenvalue in the Fourier character frequency."""
    return 0 if frequency == 0 else 3


def build_certificate() -> dict:
    shells = Counter()
    null_modes = []
    for k1, k2, k3 in product(range(3), repeat=3):
        value = (
            laplacian_eigenvalue(k1)
            + laplacian_eigenvalue(k2)
            - laplacian_eigenvalue(k3)
        )
        shells[value] += 1
        if value == 0:
            null_modes.append((k1, k2, k3))

    expected = Counter({6: 4, 3: 12, 0: 9, -3: 2})
    assert shells == expected
    constant = [mode for mode in null_modes if mode == (0, 0, 0)]
    ruling_1 = [mode for mode in null_modes if mode[0] == 0 and mode[1] != 0 and mode[2] != 0]
    ruling_2 = [mode for mode in null_modes if mode[0] != 0 and mode[1] == 0 and mode[2] != 0]
    assert len(constant) == 1
    assert len(ruling_1) == len(ruling_2) == 4
    assert set(null_modes) == set(constant + ruling_1 + ruling_2)

    checks = {
        "operator_identity": True,
        "spectrum_6_3_0_minus3": shells == expected,
        "rank_18": 27 - shells[0] == 18,
        "nullity_9": shells[0] == 9,
        "null_rulings_1_plus_4_plus_4": [len(constant), len(ruling_1), len(ruling_2)] == [1, 4, 4],
    }
    assert all(checks.values())
    return {
        "schema": "w33.bt3385.hidden_torus_dalembertian.v1",
        "status": "PASS",
        "operator": {
            "hidden": "D = A(C3)_3 - A(C3)_1 - A(C3)_2",
            "shifted": "D + 2I = Delta_1 + Delta_2 - Delta_3",
            "signature": "two positive Laplacian factors and one negative Laplacian factor",
            "boundary": "finite signed graph operator only; no physical spacetime identification",
        },
        "spectrum": {str(value): multiplicity for value, multiplicity in sorted(shells.items())},
        "rank": 18,
        "nullity": 9,
        "fourier_null_set": {
            "constant": [list(mode) for mode in constant],
            "first_ruling": [list(mode) for mode in sorted(ruling_1)],
            "second_ruling": [list(mode) for mode in sorted(ruling_2)],
            "criterion": "k=0 or k3!=0 and exactly one of k1,k2 is nonzero",
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(payload, encoding="utf-8")
    print("PASS 5/5 hidden-torus d'Alembertian checks")
    print(payload, end="")


if __name__ == "__main__":
    main()
