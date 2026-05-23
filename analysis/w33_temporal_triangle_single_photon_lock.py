"""Part MCCIII: Temporal-triangle single-photon lock.

Formal packaging layer for the existing draft
`analysis/w33_temporal_triangle_single_photon.py`.

This wrapper extracts finite arithmetic identities from the draft payload and
emits a standard PART_..._results.json artifact used by the theorem pipeline.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_temporal_triangle_single_photon import build_payload


def temporal_triangle_single_photon_lock_packet() -> dict[str, object]:
    payload = build_payload()

    q = int(payload["header"]["substrate_constants"]["q"])            # 3
    phi6 = int(payload["header"]["substrate_constants"]["Phi_6"])      # 7
    k = int(payload["header"]["substrate_constants"]["k"])            # 12
    v = int(payload["header"]["substrate_constants"]["v"])            # 40
    h1 = int(payload["header"]["substrate_constants"]["H_1"])          # 81
    qfact = int(payload["header"]["substrate_constants"]["q_factorial"])  # 6
    lambda_g = int(payload["header"]["substrate_constants"]["lambda_gauge"])  # 72

    a = payload["A_temporal_triangle_phi_6"]
    b = payload["B_history_cell_decomposition"]
    c = payload["C_w33_temporal_decomposition"]

    vertices = int(a["vertices_past_now_future"])     # 3
    edges = int(a["edges_among_three"])               # 3
    face = int(a["face_time_duration"])               # 1
    total_cells = int(a["total_cells"])               # 7

    history_total = int(b["past_x_future_total"])     # 9
    diagonal = int(b["diagonal_now_aligned"])         # 3
    directed = int(b["directed_transitions"])         # 6

    now_share = int(c["now_share"])                   # 1
    direct_share = int(c["direct_share"])             # 12
    closure_share = int(c["diagonal_closure_share"])  # 27

    checks = {
        "triangle_cells_are_phi6": vertices + edges + face == total_cells == phi6 == 7,
        "history_split_is_q_plus_qfact": history_total == diagonal + directed == q + qfact == 9,
        "diagonal_equals_q": diagonal == q == 3,
        "directed_equals_qfact": directed == qfact == 6,
        "w33_split_is_1_12_27": now_share == 1 and direct_share == k == 12 and closure_share == q**q == 27,
        "w33_total_is_40": now_share + direct_share + closure_share == v == 40,
        "bell_cloud_is_81": closure_share * q == h1 == 81,
        "lambda_gauge_is_72": lambda_g == 72,
        "rank_root_link": qfact == 6 and lambda_g == 72,
        "all_draft_synthesis_checks_true": all(bool(vv) for vv in payload["synthesis_checks"].values()),
    }

    return {
        "part": "MCCIII",
        "theorem": "Temporal-triangle single-photon lock",
        "packet": {
            "q": q,
            "Phi_6": phi6,
            "triangle_cells": [vertices, edges, face, total_cells],
            "history_split": [history_total, diagonal, directed],
            "w33_split": [now_share, direct_share, closure_share, v],
            "cloud": h1,
            "lambda_gauge": lambda_g,
        },
        "lock": {
            "identity": "(3+3+1)=7=Phi_6; 9=3+6=q+q!; 40=1+12+27; 81=27*3",
            "single_photon_reading": "three time bins (past, now, future) as one-photon self-entangled qutrit mode",
        },
        "finite_universality_surrogate": {
            "statement": "temporal triangle, history split, and W(3,3) shell counts close as one finite packet",
            "boundary": "finite structural identification; not an experimental photonic protocol proof",
        },
        "claim_boundary": "finite temporal-triangle/single-photon structural lock from existing verified chain",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = temporal_triangle_single_photon_lock_packet()
    out_path = ROOT / "PART_MCCIII_TEMPORAL_TRIANGLE_SINGLE_PHOTON_LOCK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCIII: Temporal-Triangle Single-Photon Lock ===")
    print(packet["lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
