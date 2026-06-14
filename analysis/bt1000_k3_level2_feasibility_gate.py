#!/usr/bin/env python3
"""BT1000 — K3_16 level-2 feasibility gate for the edgewise R3 tower.

BT998 proved CP2_9 level 2 is feasible directly. K3_16 level 2 is much larger:
BT993 predicts f=[2776,45120,152960,184320,73728]. This script converts those
sizes into a concrete execution policy rather than blindly attempting a huge
rank or heat-trace job.

The gate estimates sparse boundary nonzeros from the universal simplex rule
(each d-simplex contributes d+1 boundary entries), carries over level-1 density
ratios where useful, and classifies tasks into direct, blockwise, or stochastic.
"""
from __future__ import annotations

import json
from pathlib import Path

K3_LEVEL1 = {
    "f_vector": [136, 2640, 9440, 11520, 4608],
    "boundary_nnz": [5280, 28320, 46080, 23040],
    "laplacian_nnz": [5416, 165916, 182368, 110870, 27648],
}

K3_LEVEL2_F = [2776, 45120, 152960, 184320, 73728]
CP2_LEVEL2_F = [459, 5976, 19344, 23040, 9216]


def boundary_nnz_from_f(fv: list[int]) -> list[int]:
    # d_k: C_k -> C_{k-1}; each k-simplex has k+1 faces.
    return [(k + 1) * fv[k] for k in range(1, 5)]


def mib_for_int32_entries(nnz: int) -> float:
    # CSR int32 indices + int8/float64 values varies by implementation; this is a
    # conservative 16-byte per nonzero planning rule.
    return nnz * 16 / (1024 * 1024)


def main() -> None:
    k3_bnnz2 = boundary_nnz_from_f(K3_LEVEL2_F)
    # Laplacian exact nnz needs construction; use level-1 nnz/face ratios as a
    # planning estimate for L_k at level 2.
    lap_est = []
    for k, faces in enumerate(K3_LEVEL2_F):
        ratio = K3_LEVEL1["laplacian_nnz"][k] / K3_LEVEL1["f_vector"][k]
        lap_est.append(round(ratio * faces))

    out = {
        "theorem": "BT1000 K3_16 level-2 feasibility gate",
        "k3_level2_predicted_f_vector": K3_LEVEL2_F,
        "cp2_level2_completed_f_vector": CP2_LEVEL2_F,
        "k3_to_cp2_level2_face_ratios": [K3_LEVEL2_F[i] / CP2_LEVEL2_F[i] for i in range(5)],
        "k3_level2_boundary_nnz_exact_by_counting": k3_bnnz2,
        "k3_level2_boundary_storage_mib_rule16": [mib_for_int32_entries(x) for x in k3_bnnz2],
        "k3_level2_laplacian_nnz_planning_estimate": lap_est,
        "k3_level2_laplacian_storage_mib_rule16": [mib_for_int32_entries(x) for x in lap_est],
        "policy": {
            "rank_pipeline": "blockwise/incremental sparse mod-2 elimination; do not allocate dense matrices",
            "heat_trace": "stochastic expm_multiply estimator only; no dense diagonalization",
            "first_direct_target": "degree 0/4 and boundary maps, then degree 2 estimator",
            "ci_target": "smoke tests and marker/build checks, not full K3 level-2 rank by default"
        },
        "verdict": "K3_16 level 2 is feasible as a staged sparse/blockwise computation, not as a monolithic rank/eigensolve job."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1000_k3_level2_feasibility_gate.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
