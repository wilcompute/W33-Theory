#!/usr/bin/env python3
"""BT1005 — K3_16 level-2 sparse rank pilot.

This is the staged rank target/pilot for K3_16 level 2.  It uses the BT993
level-2 f-vector and the topological invariants of K3 to derive the exact rank
targets that any sparse/blockwise rank computation must hit.

It deliberately does not attempt a monolithic rank job.  The next implementation
can compute d1 by graph connectivity and then attack d2/d3 blockwise against
these targets.
"""
from __future__ import annotations

import json
from pathlib import Path

F = [2776, 45120, 152960, 184320, 73728]
BETTI = [1, 0, 22, 0, 1]


def rank_targets(f_vector: list[int], betti: list[int]) -> list[int]:
    # Solve b_k = f_k - r_k - r_{k+1}, with r_0=r_5=0.
    # Here ranks are [r1,r2,r3,r4].
    r1 = f_vector[0] - betti[0]
    r2 = f_vector[1] - r1 - betti[1]
    r3 = f_vector[2] - r2 - betti[2]
    r4 = f_vector[3] - r3 - betti[3]
    assert f_vector[4] - r4 == betti[4]
    return [r1, r2, r3, r4]


def main() -> None:
    ranks = rank_targets(F, BETTI)
    out = {
        "theorem": "BT1005 K3_16 level-2 sparse rank pilot",
        "level": 2,
        "f_vector": F,
        "betti_target": BETTI,
        "boundary_rank_targets": ranks,
        "euler_characteristic": sum(((-1) ** i) * F[i] for i in range(5)),
        "stage_plan": [
            "compute rank d1 by vertex-edge connectivity; target 2775",
            "compute rank d4 by top-boundary sparse elimination or dual connectivity; target 73727",
            "compute d2 and d3 blockwise; targets 42345 and 110593",
            "verify recovered Betti profile [1,0,22,0,1]"
        ],
        "boundary_nnz_exact_by_counting": [90240, 458880, 737280, 368640],
        "reading": "K3_16 level-2 rank verification now has exact sparse targets. The pilot reduces the next computation to staged rank recovery rather than exploratory dense linear algebra."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1005_k3_level2_sparse_rank_pilot.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
