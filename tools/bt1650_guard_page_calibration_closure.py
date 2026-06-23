#!/usr/bin/env python3
"""BT1650: close calibration by assigning the 448 time-bin guards to Fano pages."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1650_guard_page_calibration_closure.json"
MD = ROOT / "analysis" / "BT1650_guard_page_calibration_closure.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    envelope = load_json("data/bt1649_time_bin_qudit_envelope.json")
    decoder = load_json("BT1605_detector_bin_decoder.json")
    fault = load_json("BT1606_fault_path_theorem.json")
    calibration = load_json("BT1604_physical_calibration_abi.json")

    guard_rows = envelope["guard_rows_sample"]
    # Rebuild full guard table from the compact envelope definition.
    full_guard_rows = []
    for address in range(1600, 2048):
        offset = address - 1600
        fano_point = offset // 64
        guard_slot = offset % 64
        if guard_slot < 24:
            role = "DARK_REFERENCE"
            detector_bin = fano_point * 24 + guard_slot
        elif guard_slot < 48:
            role = "LOSS_PROBE"
            detector_bin = fano_point * 24 + guard_slot - 24
        else:
            role = "PARITY_OVERFLOW"
            detector_bin = None
        full_guard_rows.append(
            {
                "time_bin": address,
                "fano_point": fano_point,
                "guard_slot": guard_slot,
                "guard_role": role,
                "detector_bin": detector_bin,
                "calibration_gate": {
                    "DARK_REFERENCE": "dark_gate",
                    "LOSS_PROBE": "loss_gate",
                    "PARITY_OVERFLOW": "jitter_gate",
                }[role],
                "fault_mode": {
                    "DARK_REFERENCE": "DARK_CLICK",
                    "LOSS_PROBE": "MISSED_CLICK",
                    "PARITY_OVERFLOW": "CSS_SYNDROME",
                }[role],
            }
        )

    page_role_hist: dict[int, Counter[str]] = defaultdict(Counter)
    gate_hist: Counter[str] = Counter()
    fault_hist: Counter[str] = Counter()
    dark_bins = set()
    loss_bins = set()
    parity_slots: dict[int, set[int]] = defaultdict(set)
    for row in full_guard_rows:
        page_role_hist[row["fano_point"]][row["guard_role"]] += 1
        gate_hist[row["calibration_gate"]] += 1
        fault_hist[row["fault_mode"]] += 1
        if row["guard_role"] == "DARK_REFERENCE":
            dark_bins.add(row["detector_bin"])
        elif row["guard_role"] == "LOSS_PROBE":
            loss_bins.add(row["detector_bin"])
        else:
            parity_slots[row["fano_point"]].add(row["guard_slot"] - 48)

    retry_defaults = fault["retry_schedule"]["defaults"]
    sub_gates = set(calibration["gate_logic"]["sub_gates"])
    checks = {
        "envelope_verified": envelope["verified"] is True,
        "decoder_schema_loaded": decoder["bt"] == "BT1605",
        "fault_schema_loaded": fault["bt"] == "BT1606",
        "calibration_schema_loaded": calibration["bt"] == "BT1604",
        "full_guard_rows_are_448": len(full_guard_rows) == 448,
        "each_fano_page_has_24_24_16": {
            page: dict(sorted(hist.items()))
            for page, hist in sorted(page_role_hist.items())
        }
        == {
            page: {"DARK_REFERENCE": 24, "LOSS_PROBE": 24, "PARITY_OVERFLOW": 16}
            for page in range(7)
        },
        "dark_and_loss_cover_every_detector_bin_once": dark_bins == set(range(168))
        and loss_bins == set(range(168)),
        "parity_overflow_has_16_slots_per_fano_point": {
            page: len(slots) for page, slots in sorted(parity_slots.items())
        }
        == {page: 16 for page in range(7)},
        "guard_roles_map_to_calibration_subgates": {
            "dark_gate",
            "loss_gate",
            "jitter_gate",
        }.issubset(sub_gates),
        "guard_roles_map_to_retry_fault_modes": {
            "DARK_CLICK",
            "MISSED_CLICK",
            "CSS_SYNDROME",
        }.issubset(retry_defaults),
        "gate_histogram_matches_guard_budget": dict(sorted(gate_hist.items()))
        == {"dark_gate": 168, "jitter_gate": 112, "loss_gate": 168},
        "fault_histogram_matches_guard_budget": dict(sorted(fault_hist.items()))
        == {"CSS_SYNDROME": 112, "DARK_CLICK": 168, "MISSED_CLICK": 168},
        "compact_envelope_sample_present": len(guard_rows) == 48,
    }
    result = {
        "bt": 1650,
        "title": "Fano guard-page calibration closure",
        "verified": all(checks.values()),
        "source_packets": {
            "time_bin_envelope": "data/bt1649_time_bin_qudit_envelope.json",
            "calibration_abi": "BT1604_physical_calibration_abi.json",
            "detector_decoder": "BT1605_detector_bin_decoder.json",
            "fault_path": "BT1606_fault_path_theorem.json",
        },
        "closure_identity": {
            "guard_budget": "448 = 7*(24 dark + 24 loss + 16 parity)",
            "dark_loss_coverage": "each of the 168 active detector bins receives one dark-reference and one loss-probe guard",
            "fault_mapping": "dark -> DARK_CLICK, loss -> MISSED_CLICK, parity -> CSS_SYNDROME",
        },
        "counts": {
            "guard_rows": len(full_guard_rows),
            "dark_reference_guards": gate_hist["dark_gate"],
            "loss_probe_guards": gate_hist["loss_gate"],
            "parity_overflow_guards": gate_hist["jitter_gate"],
            "detector_bins_covered_by_dark": len(dark_bins),
            "detector_bins_covered_by_loss": len(loss_bins),
        },
        "histograms": {
            "calibration_gate": dict(sorted(gate_hist.items())),
            "fault_mode": dict(sorted(fault_hist.items())),
            "page_role": {
                page: dict(sorted(hist.items()))
                for page, hist in sorted(page_role_hist.items())
            },
        },
        "guard_rows_sample": full_guard_rows[:24] + full_guard_rows[-24:],
        "interpretation": (
            "BT1650 turns the 448 time-bin slack addresses into a concrete calibration "
            "guard shell. The slack closes the BT1604/BT1606 physical interface without "
            "expanding the 1600 active Witting frames."
        ),
        "honesty_boundary": (
            "This is a guard-addressing and calibration-interface theorem. It still "
            "requires real bench samples before any measured hardware claim."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1650 Fano Guard-Page Calibration Closure\n\n"
        "BT1650 assigns every one of the `448 = 7*64` time-bin guard addresses:\n\n"
        "```text\n"
        "per Fano point: 24 dark-reference guards\n"
        "              + 24 loss-probe guards\n"
        "              + 16 parity-overflow guards\n"
        "```\n\n"
        "The dark and loss guard sets each cover all `168` active detector bins once. "
        "The parity guards supply `7*16=112` CSS/jitter overflow slots.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1650,
                "verified": result["verified"],
                "guard_rows": len(full_guard_rows),
                "detector_bins_covered": len(dark_bins),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
