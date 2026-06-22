#!/usr/bin/env python3
"""BT1417: objectwise linear-optical primitive synthesis for the dual port.

BT1414 gave a finite dual-port ABI.  This packet translates that ABI into
object-level single-photon optical primitives:

* 21 shared K7 edge-channel couplers;
* 42 oriented phase latches;
* 168 active residue detector bins;
* 24 separated Q4 guard apertures.

The synthesis is intentionally objectwise.  It records the analyzer incidence
matrices and primitive counts, but does not claim a calibrated chip layout,
coupling length, insertion loss, or detector efficiency.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1417_linear_optical_dual_port_primitives.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def gram(matrix: list[list[int]]) -> list[list[int]]:
    return [
        [sum(left[col] * right[col] for col in range(len(left))) for right in matrix]
        for left in matrix
    ]


def profile_offdiag(matrix: list[list[int]]) -> dict[str, int]:
    diag = []
    offdiag = []
    for row, values in enumerate(matrix):
        for col, value in enumerate(values):
            if row == col:
                diag.append(value)
            else:
                offdiag.append(value)
    return {
        "diag_unique": len(set(diag)),
        "diag_value": diag[0],
        "offdiag_unique": len(set(offdiag)),
        "offdiag_value": offdiag[0],
    }


def incidence_matrix(analyzers: list[dict[str, Any]], channels: int) -> list[list[int]]:
    rows = []
    for analyzer in analyzers:
        support = set(analyzer["edge_channels"])
        rows.append([1 if channel in support else 0 for channel in range(channels)])
    return rows


def build_result() -> dict[str, Any]:
    bt1414 = load_json("data/bt1414_csaszar_szilassi_dual_physical_port.json")
    channels = bt1414["shared_edge_channels"]
    active_rows = bt1414["active_slot_rows"]
    guard_rows = bt1414["guard_band_rows"]

    channel_primitives = [
        {
            "primitive": "EDGE_CHANNEL_BALANCED_COUPLER",
            "edge_channel": row["edge_channel"],
            "endpoints": row["endpoints"],
            "input_rails": [
                f"rail_{row['endpoints'][0]}",
                f"rail_{row['endpoints'][1]}",
            ],
            "symbolic_unitary": "1/sqrt(2) [[1, 1], [1, -1]]",
        }
        for row in channels
    ]

    orientation_keys = sorted(
        {(row["edge_channel"], row["source"], row["target"]) for row in active_rows}
    )
    orientation_primitives = [
        {
            "primitive": "ORIENTED_PHASE_LATCH",
            "orientation_primitive": idx,
            "edge_channel": edge_channel,
            "source": source,
            "target": target,
            "phase_symbol": "0" if source < target else "pi",
        }
        for idx, (edge_channel, source, target) in enumerate(orientation_keys)
    ]

    active_detector_bins = [
        {
            "primitive": "ACTIVE_RESIDUE_DETECTOR_BIN",
            "active_slot": row["active_slot"],
            "tomotope_flag": row["tomotope_flag"],
            "edge_channel": row["edge_channel"],
            "orientation": row["orientation"],
            "flag_residue": row["flag_residue"],
            "primitive_stack": [
                "EDGE_CHANNEL_BALANCED_COUPLER",
                "ORIENTED_PHASE_LATCH",
                "FOUR_RESIDUE_DEMUX",
                "SINGLE_PHOTON_DETECTOR_BIN",
            ],
        }
        for row in active_rows
    ]

    guard_apertures = [
        {
            "primitive": "Q4_GUARD_APERTURE",
            "guard_slot": row["guard_slot"],
            "tomotope_flag": row["tomotope_flag"],
            "q4_plaquette": row["q4_plaquette"],
            "detector_role": "clock_guard_not_active_dual_port",
        }
        for row in guard_rows
    ]

    csaszar_matrix = incidence_matrix(bt1414["csaszar_vertex_mode"], len(channels))
    szilassi_matrix = incidence_matrix(bt1414["szilassi_face_mode"], len(channels))
    csaszar_gram = gram(csaszar_matrix)
    szilassi_gram = gram(szilassi_matrix)
    channel_usage = Counter(row["edge_channel"] for row in active_detector_bins)

    checks = {
        "bt1414_dual_port_loaded": bt1414["verified"] is True,
        "edge_channel_couplers_are_21": len(channel_primitives) == 21,
        "oriented_phase_latches_are_42": len(orientation_primitives) == 42,
        "active_detector_bins_are_168": len(active_detector_bins) == 168,
        "guard_apertures_are_24": len(guard_apertures) == 24,
        "detector_bins_fill_tomotope_bus": len(active_detector_bins)
        + len(guard_apertures)
        == 192,
        "each_channel_feeds_eight_active_bins": dict(
            sorted(Counter(channel_usage.values()).items())
        )
        == {8: 21},
        "csaszar_incidence_is_k7_vertex_star": profile_offdiag(csaszar_gram)
        == {
            "diag_unique": 1,
            "diag_value": 6,
            "offdiag_unique": 1,
            "offdiag_value": 1,
        },
        "szilassi_incidence_is_dual_k7_face_star": profile_offdiag(szilassi_gram)
        == {
            "diag_unique": 1,
            "diag_value": 6,
            "offdiag_unique": 1,
            "offdiag_value": 1,
        },
        "dual_modes_use_same_channel_set": csaszar_matrix == szilassi_matrix,
        "guard_apertures_are_separate_tail_flags": [
            row["tomotope_flag"] for row in guard_apertures
        ]
        == list(range(168, 192)),
    }

    return {
        "bt": 1417,
        "title": "Linear-optical primitive synthesis for the dual port",
        "verified": all(checks.values()),
        "primitive_summary": {
            "edge_channel_couplers": len(channel_primitives),
            "oriented_phase_latches": len(orientation_primitives),
            "active_residue_detector_bins": len(active_detector_bins),
            "guard_apertures": len(guard_apertures),
            "total_detector_bins": len(active_detector_bins) + len(guard_apertures),
            "identity": "21 couplers, 42 orientation latches, 168 active bins, 24 guard apertures",
        },
        "analyzer_matrices": {
            "field": "integer_incidence_for_objectwise_optical_routing",
            "csaszar_vertex_channel_incidence": csaszar_matrix,
            "szilassi_face_channel_incidence": szilassi_matrix,
            "csaszar_gram": csaszar_gram,
            "szilassi_gram": szilassi_gram,
            "gram_reading": "diagonal 6, off-diagonal 1 is the K7 star-overlap law",
        },
        "primitive_layers": {
            "edge_channel_couplers": channel_primitives,
            "oriented_phase_latches": orientation_primitives,
            "active_detector_bins_sample": active_detector_bins[:32],
            "guard_apertures": guard_apertures,
        },
        "physical_reading": (
            "The same 21 edge-channel mesh can be interrogated as Csaszar vertex "
            "stars or Szilassi face stars. Orientation latches choose direction, "
            "a four-bin demux records the tomotope residue, and the 24 Q4 guard "
            "apertures remain physically separate from the active dual-port mesh."
        ),
        "boundary": (
            "BT1417 is an objectwise optical primitive list and incidence matrix. "
            "It is not a waveguide mask, loss model, detector calibration, or "
            "unique decomposition into a foundry process."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "total_detector_bins": result["primitive_summary"][
                    "total_detector_bins"
                ],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
