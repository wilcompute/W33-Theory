#!/usr/bin/env python3
"""BT1429: symbolic pulse scheduler for the retwined Fano optical front end."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1429_retwined_pulse_scheduler.json"


def k7_channels() -> list[tuple[int, int]]:
    return list(itertools.combinations(range(7), 2))


def guard_target(aperture: int) -> int:
    atom = aperture // 12
    branch = (aperture % 12) // 3
    phase = aperture % 3
    return atom * 12 + branch * 3 + ((phase + branch) % 3)


def active_pulses() -> list[dict]:
    channels = k7_channels()
    pulses = []
    for channel_index, (u, v) in enumerate(channels):
        for orientation, star in enumerate((u, v)):
            for residue in range(4):
                detector = channel_index * 8 + orientation * 4 + residue
                pulses.append(
                    {
                        "clock": len(pulses),
                        "pulse_kind": "ACTIVE_OPTICAL_DETECT",
                        "fano_flag": channel_index,
                        "k7_channel": channel_index,
                        "channel_endpoints": [u, v],
                        "orientation": orientation,
                        "k7_star_mesh": star,
                        "residue": residue,
                        "detector_bin": detector,
                        "primitive_stack": [
                            "EDGE_CHANNEL_BALANCED_COUPLER",
                            "ORIENTED_PHASE_LATCH",
                            "F4_RESIDUE_DEMUX",
                            "SINGLE_PHOTON_DETECTOR_BIN",
                        ],
                        "css_frame_update": "identity",
                    }
                )
    return pulses


def guard_pulses(start_clock: int) -> list[dict]:
    pulses = []
    for aperture in range(24):
        target = guard_target(aperture)
        atom = aperture // 12
        branch = (aperture % 12) // 3
        phase = aperture % 3
        nontrivial = target != aperture
        pulses.append(
            {
                "clock": start_clock + aperture,
                "pulse_kind": "GUARD_INJECTION_FRAME_UPDATE" if nontrivial else "GUARD_IDLE_FRAME_SAMPLE",
                "guard_aperture": aperture,
                "atom": atom,
                "branch": branch,
                "phase": phase,
                "tail_coordinate": 216 + aperture,
                "retwined_tail_coordinate": 216 + target,
                "primitive_stack": [
                    "Q4_GUARD_APERTURE",
                    "D4_BRANCH_PHASE_SHEAR" if nontrivial else "IDENTITY_FRAME_SAMPLE",
                    "CSS_FRAME_RETWIN" if nontrivial else "NOOP_FRAME_TRACK",
                ],
                "css_frame_update": "D4_guard_shear" if nontrivial else "identity",
            }
        )
    return pulses


def main() -> None:
    active = active_pulses()
    guard = guard_pulses(len(active))
    schedule = active + guard
    nontrivial_guard = [pulse for pulse in guard if pulse["css_frame_update"] == "D4_guard_shear"]
    channel_profile: dict[int, int] = {i: 0 for i in range(21)}
    star_profile: dict[int, int] = {i: 0 for i in range(7)}
    for pulse in active:
        channel_profile[pulse["k7_channel"]] += 1
        star_profile[pulse["k7_star_mesh"]] += 1

    frame_ops = [
        {
            "frame_op": i,
            "source_clock": pulse["clock"],
            "tail_coordinate": pulse["tail_coordinate"],
            "retwined_tail_coordinate": pulse["retwined_tail_coordinate"],
            "operation": "apply tracked Pauli/CSS coordinate permutation J and decode with H_X J^{-1}, H_Z J^{-1}",
        }
        for i, pulse in enumerate(nontrivial_guard)
    ]

    checks = {
        "active_pulses_are_168": len(active) == 168,
        "guard_pulses_are_24": len(guard) == 24,
        "full_schedule_is_192": len(schedule) == 192,
        "detector_bins_unique": sorted(p["detector_bin"] for p in active) == list(range(168)),
        "each_k7_channel_has_8_pulses": sorted(channel_profile.values()) == [8] * 21,
        "each_k7_star_has_24_pulses": sorted(star_profile.values()) == [24] * 7,
        "nontrivial_guard_frame_ops_are_12": len(nontrivial_guard) == 12,
        "frame_ops_stay_in_css_tail": all(216 <= op["retwined_tail_coordinate"] < 240 for op in frame_ops),
        "schedule_clocks_are_contiguous": [p["clock"] for p in schedule] == list(range(192)),
        "active_then_guard_two_phase_schedule": max(p["clock"] for p in active) == 167 and min(p["clock"] for p in guard) == 168,
    }

    result = {
        "bt": 1429,
        "title": "Retwined pulse scheduler for the Fano optical front end",
        "verified": all(checks.values()),
        "schedule_summary": {
            "active_pulses": len(active),
            "guard_pulses": len(guard),
            "total_pulses": len(schedule),
            "nontrivial_css_frame_updates": len(nontrivial_guard),
            "phase_order": "168 active optical detection pulses, followed by 24 separated guard-frame pulses",
        },
        "profiles": {
            "k7_channel_profile": channel_profile,
            "k7_star_mesh_profile": star_profile,
        },
        "frame_update_program": frame_ops,
        "schedule_samples": {
            "first_active_pulses": active[:12],
            "first_guard_pulses": guard[:12],
            "last_guard_pulses": guard[-6:],
        },
        "interpretation": "BT1429 turns the retwined CSS frame rule into a deterministic symbolic pulse schedule: active bins use identity frame tracking; guard apertures either sample identity or trigger the D4 retwining program.",
        "boundary": "This is a symbolic control schedule. It does not model pulse duration, loss, timing jitter, detector noise, or analog calibration.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1429, "verified": result["verified"], "pulses": len(schedule), "frame_ops": len(frame_ops)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
