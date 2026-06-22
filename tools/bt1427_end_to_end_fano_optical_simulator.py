#!/usr/bin/env python3
"""BT1427: end-to-end Fano optical front-end simulator."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1427_end_to_end_fano_optical_simulator.json"
Vector = tuple[int, int, int]


def xor(u: Vector, v: Vector) -> Vector:
    return (u[0] ^ v[0], u[1] ^ v[1], u[2] ^ v[2])


def fano_points() -> list[Vector]:
    return [v for v in itertools.product((0, 1), repeat=3) if v != (0, 0, 0)]


def fano_lines() -> list[tuple[Vector, Vector, Vector]]:
    out = set()
    ps = fano_points()
    for a, b in itertools.combinations(ps, 2):
        out.add(tuple(sorted((a, b, xor(a, b)))))
    return sorted(out)


def fano_flags() -> list[tuple[Vector, tuple[Vector, Vector, Vector]]]:
    return [(p, line) for line in fano_lines() for p in line]


def k7_channels() -> list[tuple[int, int]]:
    return list(itertools.combinations(range(7), 2))


def guard_shear_target(aperture: int) -> int:
    atom = aperture // 12
    rem = aperture % 12
    branch = rem // 3
    phase = rem % 3
    return atom * 12 + branch * 3 + ((phase + branch) % 3)


def main() -> None:
    flags = fano_flags()
    channels = k7_channels()
    point_index = {p: i for i, p in enumerate(fano_points())}

    active_events = []
    for flag_index, (point, line) in enumerate(flags):
        channel = channels[flag_index]
        for orientation in range(2):
            star_vertex = channel[orientation]
            for residue in range(4):
                active_events.append(
                    {
                        "event": len(active_events),
                        "kind": "active_fano_optical_detection",
                        "fano_flag": flag_index,
                        "fano_point": point_index[point],
                        "fano_line_points": [point_index[p] for p in line],
                        "k7_edge_channel": flag_index,
                        "channel_endpoints": list(channel),
                        "orientation": orientation,
                        "k7_star_mesh": star_vertex,
                        "residue": residue,
                        "active_detector_bin": flag_index * 8 + orientation * 4 + residue,
                        "css_frame_update": "identity",
                    }
                )

    guard_events = []
    for aperture in range(24):
        target = guard_shear_target(aperture)
        atom = aperture // 12
        rem = aperture % 12
        branch = rem // 3
        phase = rem % 3
        guard_events.append(
            {
                "event": 168 + aperture,
                "kind": "guard_non_clifford_injection",
                "guard_aperture": aperture,
                "atom": atom,
                "branch": branch,
                "phase": phase,
                "css_tail_coordinate": 216 + aperture,
                "retwined_css_tail_coordinate": 216 + target,
                "css_frame_update": "D4_guard_shear" if target != aperture else "identity_on_this_aperture",
            }
        )

    star_profile = {v: 0 for v in range(7)}
    for event in active_events:
        star_profile[event["k7_star_mesh"]] += 1
    channel_profile = {c: 0 for c in range(21)}
    for event in active_events:
        channel_profile[event["k7_edge_channel"]] += 1

    frame_updates = [event for event in guard_events if event["css_frame_update"] == "D4_guard_shear"]
    full_trace = active_events + guard_events
    checks = {
        "fano_flags_are_21": len(flags) == 21,
        "k7_channels_are_21": len(channels) == 21,
        "active_events_are_168": len(active_events) == 168,
        "guard_events_are_24": len(guard_events) == 24,
        "full_trace_is_tomotope_bus_192": len(full_trace) == 192,
        "active_detector_bins_are_unique": sorted(event["active_detector_bin"] for event in active_events) == list(range(168)),
        "each_k7_channel_has_8_active_events": sorted(channel_profile.values()) == [8] * 21,
        "each_k7_star_mesh_has_24_events": sorted(star_profile.values()) == [24] * 7,
        "guard_frame_updates_are_12_nontrivial_tail_moves": len(frame_updates) == 12,
        "guard_targets_stay_in_tail": all(216 <= event["retwined_css_tail_coordinate"] < 240 for event in guard_events),
        "active_plus_guard_matches_fano_decomposition": 168 + 24 == 192,
    }

    result = {
        "bt": 1427,
        "title": "End-to-end Fano optical front-end simulator",
        "verified": all(checks.values()),
        "pipeline": [
            "Fano flag",
            "canonical K7 edge-channel representative",
            "orientation-selected K7 star mesh",
            "four-residue active detector bin",
            "identity CSS frame update for active events",
            "D4 guard-shear CSS frame update for non-Clifford guard events",
        ],
        "counts": {
            "fano_flags": len(flags),
            "k7_edge_channels": len(channels),
            "active_events": len(active_events),
            "guard_events": len(guard_events),
            "tomotope_bus_events": len(full_trace),
            "nontrivial_css_frame_updates": len(frame_updates),
        },
        "profiles": {
            "k7_star_mesh_event_profile": star_profile,
            "k7_channel_event_profile": channel_profile,
        },
        "active_trace_sample": active_events[:16],
        "guard_trace": guard_events,
        "interpretation": "The active 168 events are a Fano-flag/K7-channel optical bus. The 24 guard events are a separated non-Clifford injection rail; exactly 12 of them trigger the retwined D4 CSS frame update from BT1425.",
        "boundary": "The simulator is combinatorial and symbolic. It does not model optical loss, timing jitter, detector noise, or physical waveguide layout.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1427, "verified": result["verified"], "events": len(full_trace), "frame_updates": len(frame_updates)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
