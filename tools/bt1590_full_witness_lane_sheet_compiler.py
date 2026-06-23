#!/usr/bin/env python3
"""BT1590: compile the full 77760-tick OAM witness protocol lane sheet."""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1495_72_tick_transaction_word_compiler import compile_word

OUT = ROOT / "data" / "bt1590_full_witness_lane_sheet_compiler.json"
MD = ROOT / "analysis" / "BT1590_full_witness_lane_sheet_compiler.md"

TRANSLATIONS = [
    (0, 0),
    (1, 0),
    (2, 0),
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
]
WITNESS_GATES = ["I", "X", "Z", "F3", "S"]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def recenter_class(shift: tuple[int, int]) -> str:
    x_shift, z_shift = shift
    if x_shift == 0 and z_shift == 0:
        return "centered_frame"
    if x_shift != 0 and z_shift == 0:
        return "oam_shift_only"
    if x_shift == 0 and z_shift != 0:
        return "phase_shift_only"
    return "mixed_shift_phase"


def correction_label(shift: tuple[int, int]) -> str:
    x_shift, z_shift = shift
    pieces = []
    if x_shift:
        pieces.append(f"X^{(-x_shift) % 3}")
    if z_shift:
        pieces.append(f"Z^{(-z_shift) % 3}")
    return "I" if not pieces else " ".join(pieces)


def build_words() -> list[dict]:
    perms = sorted(itertools.permutations(range(4)))
    return [compile_word(i, perm) for i, perm in enumerate(perms)]


def main() -> None:
    abi = load_json("data/bt1587_oam_recenter_transaction_abi.json")
    radial = load_json("data/bt1589_lg_oam_radial_covariance_simulator.json")
    tx = load_json("data/bt1495_72_tick_transaction_word_compiler.json")

    words = build_words()
    radial_eta = {
        (tuple(row["affine_shift"]), row["witness_gate"]): row["effective_eta"]
        for row in radial["rows"]
    }

    segments = []
    lane_counts: Counter[str] = Counter()
    gate_tick_counts: Counter[str] = Counter()
    class_tick_counts: Counter[str] = Counter()
    detector_slot_counts: Counter[int] = Counter()
    action_level_tick_counts: Counter[str] = Counter()
    word_reuse_counts: Counter[int] = Counter()
    radial_case_reuse: Counter[str] = Counter()
    sample_ticks = []

    segment_index = 0
    for gate_index, gate in enumerate(WITNESS_GATES):
        for translation_index, shift in enumerate(TRANSLATIONS):
            klass = recenter_class(shift)
            correction = correction_label(shift)
            for word in words:
                start_tick = segment_index * 72
                end_tick = start_tick + 71
                word_index = int(word["action_index"])
                segment = {
                    "segment_index": segment_index,
                    "start_tick": start_tick,
                    "end_tick": end_tick,
                    "witness_gate": gate,
                    "gate_index": gate_index,
                    "affine_shift": list(shift),
                    "translation_index": translation_index,
                    "recenter_class": klass,
                    "correction": correction,
                    "centered_transaction_word": word_index,
                    "word_level": word["level"],
                    "radial_effective_eta": radial_eta[(shift, gate)],
                    "tick_count": 72,
                    "global_tick_formula": "((((gate_index*9)+translation_index)*24 + word_index)*72 + transaction_tick)",
                }
                segments.append(segment)
                word_reuse_counts[word_index] += 1
                radial_case_reuse[f"{shift}:{gate}"] += 1

                for tick in word["ticks"]:
                    lane_counts[tick["hesse_lane"]] += 1
                    gate_tick_counts[gate] += 1
                    class_tick_counts[klass] += 1
                    detector_slot_counts[tick["detector_slot"]] += 1
                    action_level_tick_counts[word["level"]] += 1
                    if len(sample_ticks) < 36 or start_tick >= 77760 - 12:
                        sample_ticks.append(
                            {
                                "global_tick": start_tick + tick["transaction_tick"],
                                "segment_index": segment_index,
                                "transaction_tick": tick["transaction_tick"],
                                "witness_gate": gate,
                                "affine_shift": list(shift),
                                "recenter_class": klass,
                                "centered_transaction_word": word_index,
                                "hesse_lane": tick["hesse_lane"],
                                "detector_slot": tick["detector_slot"],
                                "mirror_slot_mod_4": tick["mirror_slot_mod_4"],
                                "frame_tick": tick["frame_tick"],
                            }
                        )
                segment_index += 1

    total_ticks = sum(segment["tick_count"] for segment in segments)
    expected_class_ticks = {
        "centered_frame": 8640,
        "mixed_shift_phase": 34560,
        "oam_shift_only": 17280,
        "phase_shift_only": 17280,
    }
    checks = {
        "abi_verified": abi["verified"] is True,
        "radial_verified": radial["verified"] is True,
        "transaction_words_verified": tx["verified"] is True,
        "segments_1080": len(segments) == 5 * 9 * 24 == 1080,
        "total_ticks_77760": total_ticks == 77760,
        "segment_ticks_are_72": all(
            segment["tick_count"] == 72 for segment in segments
        ),
        "six_hesse_lanes_balanced": dict(sorted(lane_counts.items()))
        == {
            "ERASE": 12960,
            "PHASE": 12960,
            "ROUTE": 12960,
            "T-BIT": 12960,
            "X-CORR": 12960,
            "Z-CORR": 12960,
        },
        "five_gate_sweeps_equal": dict(sorted(gate_tick_counts.items()))
        == {gate: 15552 for gate in WITNESS_GATES},
        "class_tick_counts_match_bt1589": dict(sorted(class_tick_counts.items()))
        == expected_class_ticks
        == radial["class_tick_counts"],
        "native_d4_tick_count": action_level_tick_counts["native_d4_square_pulse"]
        == 5 * 9 * 8 * 72
        == 25920,
        "s4_relabel_tick_count": action_level_tick_counts["s4_analyzer_relabel"]
        == 5 * 9 * 16 * 72
        == 51840,
        "detector_slots_balanced": dict(sorted(detector_slot_counts.items()))
        == {0: 19440, 1: 19440, 2: 19440, 3: 19440},
        "each_word_reused_45_times": sorted(word_reuse_counts.values()) == [45] * 24,
        "each_radial_case_reused_24_times": sorted(radial_case_reuse.values())
        == [24] * 45,
        "last_tick_is_77759": segments[-1]["end_tick"] == 77759,
    }
    segment_samples = (
        segments[:12]
        + [
            segment
            for segment in segments
            if segment["recenter_class"] == "mixed_shift_phase"
        ][:6]
        + segments[-12:]
    )
    result = {
        "bt": 1590,
        "title": "Full OAM witness physical lane sheet",
        "verified": all(checks.values()),
        "source_packets": {
            "abi": "data/bt1587_oam_recenter_transaction_abi.json",
            "radial_covariance": "data/bt1589_lg_oam_radial_covariance_simulator.json",
            "transaction_words": "data/bt1495_72_tick_transaction_word_compiler.json",
        },
        "counts": {
            "segments": len(segments),
            "ticks_per_segment": 72,
            "total_ticks": total_ticks,
            "witness_gates": len(WITNESS_GATES),
            "affine_translations": len(TRANSLATIONS),
            "centered_transaction_words": len(words),
        },
        "segment_grid": {
            "axis_order": [
                "witness_gate",
                "affine_translation",
                "centered_transaction_word",
            ],
            "witness_gates": WITNESS_GATES,
            "affine_translations": [list(shift) for shift in TRANSLATIONS],
            "centered_transaction_words": list(range(len(words))),
            "segment_index_formula": "(gate_index*9 + translation_index)*24 + word_index",
            "start_tick_formula": "segment_index*72",
            "global_tick_formula": "((((gate_index*9)+translation_index)*24 + word_index)*72 + transaction_tick)",
        },
        "lane_counts": dict(sorted(lane_counts.items())),
        "gate_tick_counts": dict(sorted(gate_tick_counts.items())),
        "class_tick_counts": dict(sorted(class_tick_counts.items())),
        "detector_slot_counts": dict(sorted(detector_slot_counts.items())),
        "action_level_tick_counts": dict(sorted(action_level_tick_counts.items())),
        "word_reuse_profile": sorted(word_reuse_counts.values()),
        "radial_case_reuse_profile": sorted(radial_case_reuse.values()),
        "segment_samples": segment_samples,
        "sample_ticks": sample_ticks,
        "interpretation": (
            "The five-gate OAM witness is now a concrete physical lane sheet: "
            "5 witness gates times 9 recenter shifts times 24 centered transaction "
            "words times 72 ticks. The sheet preserves Hesse lane balance, detector "
            "slot balance, native D4 fast-lane accounting, and S4 relabel accounting."
        ),
        "honesty_boundary": (
            "This is a deterministic lane compiler and timing certificate. It is not "
            "an optical-loss, detector-efficiency, or beam-quality measurement."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1590 Full OAM Witness Lane Sheet\n\n"
        "BT1590 compiles the full witness protocol into `1080` exact 72-tick segments, "
        "for `77760` ticks total. Each Hesse lane appears `12960` times, each detector "
        "slot appears `19440` times, native D4 square pulses occupy `25920` ticks, and "
        "S4 analyzer relabel ticks occupy `51840` ticks.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1590,
                "verified": result["verified"],
                "segments": len(segments),
                "ticks": total_ticks,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
