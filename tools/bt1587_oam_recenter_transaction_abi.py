#!/usr/bin/env python3
"""BT1587: bridge the 216 internal Clifford actions to 24 centered transaction words."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1587_oam_recenter_transaction_abi.json"
MD = ROOT / "analysis" / "BT1587_oam_recenter_transaction_abi.md"

TRANSLATIONS = [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2)]
CLASS_COUNTS = {
    "centered_frame": 24,
    "oam_shift_only": 48,
    "phase_shift_only": 48,
    "mixed_shift_phase": 96,
}


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


def inverse_correction(shift: tuple[int, int]) -> str:
    x_shift, z_shift = shift
    inv_x = (-x_shift) % 3
    inv_z = (-z_shift) % 3
    pieces = []
    if inv_x:
        pieces.append(f"X^{inv_x}")
    if inv_z:
        pieces.append(f"Z^{inv_z}")
    return "I" if not pieces else " ".join(pieces)


def build_rows(transaction_words: int) -> list[dict]:
    rows = []
    for shift in TRANSLATIONS:
        klass = recenter_class(shift)
        for frame_index in range(transaction_words):
            rows.append(
                {
                    "affine_shift": list(shift),
                    "recenter_class": klass,
                    "correction": inverse_correction(shift),
                    "centered_transaction_word": frame_index,
                    "transaction_ticks": 72,
                    "witness_gate_set": ["I", "X", "Z", "F3", "S"],
                    "claim_level": (
                        "exact finite ABI"
                        if klass == "centered_frame"
                        else "exact finite ABI after recentering"
                    ),
                }
            )
    return rows


def main() -> None:
    tx = load_json("data/bt1495_72_tick_transaction_word_compiler.json")
    census = load_json("data/bt1570_internal_clifford_orbit_census.json")
    calibration = load_json("data/bt1578_full_centered_basis_calibration_matrix.json")
    leakage = load_json("data/bt1577_radial_leakage_bound_from_oam_phase_ops.json")
    protocol = load_json("data/bt1584_recentered_protocol_table_expansion.json")

    transaction_words = tx["counts"]["transaction_words"]
    rows = build_rows(transaction_words)
    class_counts = Counter(row["recenter_class"] for row in rows)
    word_reuse = Counter(row["centered_transaction_word"] for row in rows)
    one_operation_ticks = sum(row["transaction_ticks"] for row in rows)
    five_witness_ticks = one_operation_ticks * len(calibration["operations"])
    checks = {
        "transaction_words_24": transaction_words == 24,
        "affine_rows_216": len(rows) == 216 == census["counts"]["total"],
        "class_counts_match_protocol": dict(class_counts) == CLASS_COUNTS,
        "origin_moving_192": len(rows) - class_counts["centered_frame"]
        == census["counts"]["origin_moving"]
        == 192,
        "each_word_reused_nine_times": sorted(word_reuse.values()) == [9] * 24,
        "one_operation_tick_budget": one_operation_ticks == 216 * 72 == 15552,
        "five_witness_tick_budget": five_witness_ticks == 216 * 72 * 5 == 77760,
        "five_calibrated_operations": calibration["operations"]
        == ["I", "X", "Z", "F3", "S"],
        "leakage_default_threshold_010": abs(leakage["default_threshold"] - 0.10)
        < 1e-12,
        "protocol_expanded_rows_20": protocol["expanded_rows"] == 20,
    }
    result = {
        "bt": 1587,
        "title": "OAM recenter transaction ABI",
        "verified": all(checks.values()),
        "source_packets": {
            "transaction_words": "data/bt1495_72_tick_transaction_word_compiler.json",
            "internal_clifford": "data/bt1570_internal_clifford_orbit_census.json",
            "calibration": "data/bt1578_full_centered_basis_calibration_matrix.json",
            "leakage": "data/bt1577_radial_leakage_bound_from_oam_phase_ops.json",
            "protocol": "data/bt1584_recentered_protocol_table_expansion.json",
        },
        "counts": {
            "affine_internal_actions": len(rows),
            "centered_transaction_words": transaction_words,
            "translations": len(TRANSLATIONS),
            "one_operation_ticks": one_operation_ticks,
            "five_witness_ticks": five_witness_ticks,
        },
        "class_counts": dict(class_counts),
        "word_reuse_profile": sorted(word_reuse.values()),
        "sample_rows": rows[:12],
        "interpretation": (
            "The 216 internal Clifford/OAM actions are nine affine recentering shifts over "
            "the 24 centered BT1495 transaction words. Translated actions do not need new "
            "packet words; they require inverse recentering before reusing the centered "
            "I,X,Z,F3,S witness table."
        ),
        "honesty_boundary": (
            "This is an ABI and protocol workload certificate. It is not measured OAM "
            "leakage, optical loss, or a claim that all affine corrections are calibrated devices."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text(
        "# BT1587 OAM Recenter Transaction ABI\n\n"
        "The full 216-element internal Clifford/OAM shell is nine affine recentering shifts "
        "over the 24 centered BT1495 transaction words. The class profile is "
        "`24,48,48,96` for centered, OAM-only, phase-only, and mixed shifts. One full "
        "operation sweep uses `216*72=15552` ticks; the five-gate witness sweep uses "
        "`77760` ticks.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1587,
                "verified": result["verified"],
                "rows": len(rows),
                "ticks": one_operation_ticks,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
