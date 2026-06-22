#!/usr/bin/env python3
"""BT1414: Csaszar/Szilassi dual physical port over the tomotope flag bus.

BT1317 already split the 192 tomotope packet as 168 active toroidal slots plus
24 ground slots.  BT1413 now identifies all 192 slots with Q4/tomotope/Q6 flag
addresses.  This packet makes the active 168 slots into a concrete dual
analyzer port:

    21 shared K7 edge channels * 2 orientations * 4 flag residues = 168.

The Csaszar mode reads maximal vertex adjacency.  The Szilassi mode reads the
dual maximal face adjacency.  The remaining 24 flags are the Q4 plaquette guard
band from BT1412/BT1413.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1414_csaszar_szilassi_dual_physical_port.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def k7_edges() -> list[tuple[int, int]]:
    return [(i, j) for i in range(7) for j in range(i + 1, 7)]


def incident_channel_ids(vertex: int, channels: list[tuple[int, int]]) -> list[int]:
    return [
        channel_id
        for channel_id, (left, right) in enumerate(channels)
        if vertex in (left, right)
    ]


def oriented_transports(channels: list[tuple[int, int]]) -> list[dict[str, int]]:
    rows = []
    for channel_id, (left, right) in enumerate(channels):
        rows.append(
            {
                "oriented_transport": len(rows),
                "edge_channel": channel_id,
                "source": left,
                "target": right,
            }
        )
        rows.append(
            {
                "oriented_transport": len(rows),
                "edge_channel": channel_id,
                "source": right,
                "target": left,
            }
        )
    return rows


def build_result() -> dict[str, Any]:
    bt1316 = load_json("data/bt1316_toroidal_authoritative_data_lock.json")
    bt1317 = load_json("data/bt1317_toroidal_tomotope_pipeline_consolidator.json")
    bt1318 = load_json("data/bt1318_toroidal_c2_axis_assignment.json")
    bt1412 = load_json("data/bt1412_toroidal_q4_oscillator_boundary.json")
    bt1413 = load_json("data/bt1413_q4_plaquette_tomotope_face_compiler.json")

    channels = k7_edges()
    oriented = oriented_transports(channels)
    active_slot_rows = []
    for transport in oriented:
        for residue in range(4):
            tomotope_flag = 4 * transport["oriented_transport"] + residue
            active_slot_rows.append(
                {
                    "active_slot": len(active_slot_rows),
                    "tomotope_flag": tomotope_flag,
                    "flag_residue": residue,
                    "edge_channel": transport["edge_channel"],
                    "source": transport["source"],
                    "target": transport["target"],
                    "orientation": f"{transport['source']}->{transport['target']}",
                }
            )

    guard_band_rows = [
        {
            "guard_slot": idx,
            "tomotope_flag": 168 + idx,
            "q4_plaquette": idx,
            "role": "BT1412_Q4_plaquette_guard",
        }
        for idx in range(24)
    ]

    vertex_mode = [
        {
            "analyzer": f"csaszar_vertex_{vertex}",
            "mode": "maximal_vertex_adjacency",
            "label": vertex,
            "edge_channels": incident_channel_ids(vertex, channels),
        }
        for vertex in range(7)
    ]
    face_mode = [
        {
            "analyzer": f"szilassi_face_{face}",
            "mode": "maximal_face_adjacency",
            "label": face,
            "edge_channels": incident_channel_ids(face, channels),
        }
        for face in range(7)
    ]

    channel_profile = Counter(row["edge_channel"] for row in active_slot_rows)
    vertex_channel_hit_profile = Counter(
        channel_id
        for analyzer in vertex_mode
        for channel_id in analyzer["edge_channels"]
    )
    face_channel_hit_profile = Counter(
        channel_id for analyzer in face_mode for channel_id in analyzer["edge_channels"]
    )
    csaszar_fixed_vertex = bt1318["metric_axis_records"]["csaszar"][0]["fixed_vertex"][
        0
    ]
    szilassi_fixed_face = bt1318["metric_axis_records"]["szilassi"][0]["fixed_faces"][0]
    crossed_axis_channel = channels.index(
        tuple(sorted((csaszar_fixed_vertex, szilassi_fixed_face)))
    )

    checks = {
        "bt1316_toroidal_lock_loaded": bt1316["verified"] is True,
        "bt1317_pipeline_split_loaded": bt1317["verified"] is True,
        "bt1318_axis_assignment_loaded": bt1318["verified"] is True,
        "bt1412_boundary_loaded": bt1412["verified"] is True,
        "bt1413_compiler_loaded": bt1413["verified"] is True,
        "shared_channel_count_is_21": len(channels) == 21,
        "oriented_transport_count_is_42": len(oriented) == 42,
        "active_slots_are_168": len(active_slot_rows) == 168,
        "guard_band_is_24": len(guard_band_rows) == 24,
        "active_plus_guard_is_full_tomotope_flag_bus": len(active_slot_rows)
        + len(guard_band_rows)
        == len(bt1413["flag_rows"])
        == 192,
        "active_split_matches_bt1317": bt1317["pipeline_chain"]["active_packet_weight"]
        == 168
        and bt1317["pipeline_chain"]["stationary_ground_weight"] == 24,
        "each_channel_has_two_orientations_times_four_residues": dict(
            sorted(Counter(channel_profile.values()).items())
        )
        == {8: 21},
        "csaszar_vertex_mode_is_k7": len(vertex_mode) == 7
        and all(len(row["edge_channels"]) == 6 for row in vertex_mode)
        and dict(sorted(Counter(vertex_channel_hit_profile.values()).items()))
        == {2: 21},
        "szilassi_face_mode_is_dual_k7": len(face_mode) == 7
        and all(len(row["edge_channels"]) == 6 for row in face_mode)
        and dict(sorted(Counter(face_channel_hit_profile.values()).items())) == {2: 21},
        "axis_records_are_bt1318_current_boundary": csaszar_fixed_vertex == 6
        and szilassi_fixed_face == 4,
        "axis_modes_cross_in_one_edge_channel": crossed_axis_channel
        == channels.index((4, 6)),
        "guard_band_is_q4_plaquette_shell": [
            row["q4_plaquette"] for row in guard_band_rows
        ]
        == list(range(bt1412["q4_toroidal_clock"]["square_faces"])),
    }

    return {
        "bt": 1414,
        "title": "Csaszar/Szilassi dual physical port",
        "verified": all(checks.values()),
        "port_summary": {
            "edge_channels": len(channels),
            "oriented_transports": len(oriented),
            "residues_per_orientation": 4,
            "active_slots": len(active_slot_rows),
            "guard_slots": len(guard_band_rows),
            "full_flag_bus": len(active_slot_rows) + len(guard_band_rows),
            "identity": "21 edges * 2 orientations * 4 residues + 24 guard flags = 192",
        },
        "axis_summary": {
            "csaszar_fixed_vertex": csaszar_fixed_vertex,
            "szilassi_fixed_face": szilassi_fixed_face,
            "crossed_axis_channel": crossed_axis_channel,
            "crossed_axis_edge": list(channels[crossed_axis_channel]),
        },
        "shared_edge_channels": [
            {"edge_channel": idx, "endpoints": list(edge)}
            for idx, edge in enumerate(channels)
        ],
        "csaszar_vertex_mode": vertex_mode,
        "szilassi_face_mode": face_mode,
        "active_slot_rows_sample": active_slot_rows[:24],
        "guard_band_rows": guard_band_rows,
        "physical_reading": (
            "One 21-channel edge bus supports two analyzer modes. Csaszar mode "
            "asks which vertex-neighborhood channel fired; Szilassi mode asks "
            "the dual face-neighborhood question. The same edge channel is read "
            "in either mode, while the 24 remaining flags form the Q4 plaquette "
            "guard band."
        ),
        "boundary": (
            "BT1414 is a port/check ABI over the verified finite toroidal data. "
            "It is not a calibrated optical component layout and does not choose "
            "a unique metric embedding of the toroidal polyhedra."
        ),
        "active_slot_rows": active_slot_rows,
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
                "active_slots": result["port_summary"]["active_slots"],
                "bt": result["bt"],
                "guard_slots": result["port_summary"]["guard_slots"],
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
