#!/usr/bin/env python3
"""BT1649: embed the 1600-frame automaton in an 11-bit time-bin qudit envelope."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1649_time_bin_qudit_envelope.json"
MD = ROOT / "analysis" / "BT1649_time_bin_qudit_envelope.md"

TIME_BIN_BITS = 11
ENVELOPE_BINS = 2**TIME_BIN_BITS
ACTIVE_FRAMES = 1600
GUARD_BINS = ENVELOPE_BINS - ACTIVE_FRAMES


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def guard_role(slot: int) -> str:
    if slot < 24:
        return "DARK_REFERENCE"
    if slot < 48:
        return "LOSS_PROBE"
    return "PARITY_OVERFLOW"


def main() -> None:
    charge = load_json("data/bt1648_fano_charge_conservation.json")
    automaton = load_json("data/bt1601_single_photon_transaction_automaton.json")
    bt1604 = load_json("BT1604_physical_calibration_abi.json")

    active_sample = [
        {
            "frame": frame,
            "time_bin": frame,
            "time_bin_word": format(frame, f"0{TIME_BIN_BITS}b"),
            "role": "WITTING_FRAME",
        }
        for frame in list(range(16)) + list(range(ACTIVE_FRAMES - 16, ACTIVE_FRAMES))
    ]
    guard_rows = []
    guard_role_hist: Counter[str] = Counter()
    page_hist: Counter[int] = Counter()
    for address in range(ACTIVE_FRAMES, ENVELOPE_BINS):
        offset = address - ACTIVE_FRAMES
        fano_point = offset // 64
        guard_slot = offset % 64
        role = guard_role(guard_slot)
        row = {
            "time_bin": address,
            "time_bin_word": format(address, f"0{TIME_BIN_BITS}b"),
            "guard_offset": offset,
            "fano_point": fano_point,
            "guard_slot": guard_slot,
            "guard_role": role,
        }
        if role in {"DARK_REFERENCE", "LOSS_PROBE"}:
            row["detector_bin"] = fano_point * 24 + (guard_slot % 24)
            row["fiber_index"] = guard_slot % 24
        else:
            row["parity_guard"] = guard_slot - 48
        guard_rows.append(row)
        guard_role_hist[role] += 1
        page_hist[fano_point] += 1

    dark_bins = {
        row["detector_bin"]
        for row in guard_rows
        if row["guard_role"] == "DARK_REFERENCE"
    }
    loss_bins = {
        row["detector_bin"] for row in guard_rows if row["guard_role"] == "LOSS_PROBE"
    }
    checks = {
        "charge_verified": charge["verified"] is True,
        "automaton_verified": automaton["verified"] is True,
        "calibration_schema_loaded": bt1604["bt"] == "BT1604",
        "eleven_bits_give_2048_time_bins": ENVELOPE_BINS == 2048,
        "active_region_has_1600_frames": ACTIVE_FRAMES
        == automaton["counts"]["frames"]
        == charge["histograms"]["usage"]["9"] * 9
        + charge["histograms"]["usage"]["10"] * 10,
        "guard_region_is_448_equals_7_times_64": GUARD_BINS == 448
        and GUARD_BINS == 7 * 64,
        "guard_pages_are_balanced": dict(sorted(page_hist.items()))
        == {point: 64 for point in range(7)},
        "guard_roles_are_168_168_112": dict(sorted(guard_role_hist.items()))
        == {"DARK_REFERENCE": 168, "LOSS_PROBE": 168, "PARITY_OVERFLOW": 112},
        "dark_and_loss_cover_all_168_detector_bins": dark_bins == set(range(168))
        and loss_bins == set(range(168)),
        "parity_overflow_is_7_times_16": guard_role_hist["PARITY_OVERFLOW"] == 7 * 16,
        "active_and_guard_regions_are_disjoint": ACTIVE_FRAMES
        == min(row["time_bin"] for row in guard_rows),
    }
    result = {
        "bt": 1649,
        "title": "Eleven-bit time-bin qudit envelope for the Witting automaton",
        "verified": all(checks.values()),
        "source_packets": {
            "charge_conservation": "data/bt1648_fano_charge_conservation.json",
            "physical_automaton": "data/bt1601_single_photon_transaction_automaton.json",
            "calibration_abi": "BT1604_physical_calibration_abi.json",
        },
        "envelope_identity": {
            "time_bin_qudit": "2^11 = 2048 addressable time bins",
            "active_region": "time bins 0..1599 are the Witting transaction frames",
            "guard_region": "time bins 1600..2047 are 448 = 7*64 Fano guard bins",
            "external_anchor": (
                "Motivated by single-photon time-bin qudit universal logic with "
                "O(N) linear optics elements; the repo only uses the finite address "
                "envelope here."
            ),
        },
        "counts": {
            "time_bin_bits": TIME_BIN_BITS,
            "envelope_bins": ENVELOPE_BINS,
            "active_frames": ACTIVE_FRAMES,
            "guard_bins": GUARD_BINS,
            "fano_guard_pages": len(page_hist),
            "dark_reference_bins": guard_role_hist["DARK_REFERENCE"],
            "loss_probe_bins": guard_role_hist["LOSS_PROBE"],
            "parity_overflow_bins": guard_role_hist["PARITY_OVERFLOW"],
        },
        "histograms": {
            "guard_page": dict(sorted(page_hist.items())),
            "guard_role": dict(sorted(guard_role_hist.items())),
        },
        "active_sample": active_sample,
        "guard_rows_sample": guard_rows[:24] + guard_rows[-24:],
        "interpretation": (
            "BT1649 puts the 1600-frame automaton inside an 11-bit time-bin qudit "
            "address space. The 448 unused addresses are not waste: they factor as "
            "seven Fano guard pages, each with 24 dark references, 24 loss probes, "
            "and 16 parity-overflow slots."
        ),
        "honesty_boundary": (
            "This is a finite addressing envelope, not an implemented optical chip "
            "or a measured O(N)-element decomposition."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1649 Time-Bin Qudit Envelope\n\n"
        "BT1649 embeds the `1600` Witting transaction frames into an `11`-bit "
        "single-photon time-bin envelope:\n\n"
        "```text\n"
        "2^11 = 2048 time bins\n"
        "2048 - 1600 = 448 = 7*64 guard bins\n"
        "per Fano point: 24 dark references + 24 loss probes + 16 parity overflow\n"
        "```\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1649,
                "verified": result["verified"],
                "envelope_bins": ENVELOPE_BINS,
                "guard_bins": GUARD_BINS,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
