#!/usr/bin/env python3
"""Bench-facing shot packet for the frequency-bin Hashimoto compiler."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_frequency_bin_lab_packet.json"
CSV_OUT = ROOT / "docs" / "holonet_frequency_bin_phase_probe_schedule.csv"
JSONL_OUT = ROOT / "docs" / "holonet_frequency_bin_raw_shot_template.jsonl"
MD_OUT = ROOT / "docs" / "holonet_frequency_bin_lab_packet.md"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def build_schedule(compiler: dict[str, Any]) -> list[dict[str, Any]]:
    hesse_bins = compiler["frequency_plan"]["hesse_bins"]
    sidebands = compiler["frequency_plan"]["hashimoto_sidebands"]
    packets_per_mirror = compiler["probe_budget"]["packets_per_mirror_atlas"]
    slots_per_probe = compiler["probe_budget"]["runtime_slots_per_phase_probe"]

    rows: list[dict[str, Any]] = []
    probe_id = 0
    for packet_frame in range(packets_per_mirror):
        for hesse in hesse_bins:
            for sideband in sidebands:
                runtime_start = probe_id * slots_per_probe
                rows.append(
                    {
                        "probe_id": probe_id,
                        "mirror_atlas_id": 0,
                        "packet_frame": packet_frame,
                        "packet_local_probe": (hesse["bin_index"] * len(sidebands))
                        + (0 if sideband["sector"] == "gauge" else 1),
                        "runtime_slot_start": runtime_start,
                        "runtime_slot_end": runtime_start + slots_per_probe - 1,
                        "hesse_bin": hesse["bin_index"],
                        "hesse_label": hesse["label"],
                        "route_trit": hesse["route_trit"],
                        "phase_trit": hesse["phase_trit"],
                        "phase_lane_tick": hesse["phase_lane_tick"],
                        "qutrit_phase_degrees": hesse["qutrit_phase_degrees"],
                        "sector": sideband["sector"],
                        "sector_bin": sideband["bin_index"],
                        "sector_label": sideband["label"],
                        "hashimoto_phase_degrees": sideband["phase_degrees"],
                        "frequency_offset_units": hesse["frequency_offset_units"],
                        "calibration_action": "measure_sector_probe_visibility",
                        "accepted_flag_field": "accepted_flag",
                        "measurement_fields": "plus_counts,minus_counts,total_counts,visibility,phase_error_degrees",
                    }
                )
                probe_id += 1
    return rows


def write_csv(rows: list[dict[str, Any]]) -> None:
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl_template(rows: list[dict[str, Any]]) -> None:
    template_rows = []
    for row in rows[:4]:
        template_rows.append(
            {
                "shot_id": row["probe_id"],
                "probe_id": row["probe_id"],
                "mirror_atlas_id": row["mirror_atlas_id"],
                "packet_frame": row["packet_frame"],
                "hesse_bin": row["hesse_bin"],
                "sector": row["sector"],
                "frequency_bin_label": row["sector_label"],
                "runtime_slot_start": row["runtime_slot_start"],
                "runtime_slot_end": row["runtime_slot_end"],
                "pulse_shaper_phase_degrees": row["hashimoto_phase_degrees"],
                "qutrit_phase_degrees": row["qutrit_phase_degrees"],
                "eom_phase_reference": "locked_to_packet_phase_lane",
                "plus_counts": None,
                "minus_counts": None,
                "total_counts": None,
                "visibility": None,
                "phase_error_degrees": None,
                "dark_reference": False,
                "loss_probe": False,
                "accepted_flag": None,
                "claim_boundary": "template row only; fill counts from bench data",
            }
        )
    JSONL_OUT.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in template_rows),
        encoding="utf-8",
    )


def write_markdown(result: dict[str, Any]) -> None:
    MD_OUT.write_text(
        "\n".join(
            [
                "# Holonet Frequency-Bin Phase Probe Lab Packet",
                "",
                "Purpose: turn the frequency-bin Hashimoto compiler into a bench-facing schedule.",
                "",
                "Generated artifacts:",
                "",
                "- `docs/holonet_frequency_bin_phase_probe_schedule.csv`",
                "- `docs/holonet_frequency_bin_raw_shot_template.jsonl`",
                "- `data/w33_frequency_bin_lab_packet.json`",
                "",
                "The schedule has 540 rows for one 2160-slot mirror atlas. Each probe owns four runtime slots, so the atlas identity is `540*4 = 2160`. Across 24 mirror atlases this becomes `12960*4 = 51840`.",
                "",
                "This is a shot schedule and schema packet. It is not a measured phase-visibility result.",
                "",
                "Validation summary:",
                "",
                f"- verified: `{result['verified']}`",
                f"- probes per mirror atlas: `{result['schedule_summary']['rows']}`",
                f"- probes per packet: `{result['schedule_summary']['probes_per_packet']}`",
                f"- slots per probe: `{result['schedule_summary']['runtime_slots_per_probe']}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def build_certificate() -> dict[str, Any]:
    compiler = load_json("data/w33_frequency_bin_hashimoto_compiler.json")
    rows = build_schedule(compiler)
    rows_by_packet = Counter(row["packet_frame"] for row in rows)
    rows_by_hesse_sector = Counter((row["hesse_label"], row["sector"]) for row in rows)
    slot_starts = [row["runtime_slot_start"] for row in rows]
    slot_ends = [row["runtime_slot_end"] for row in rows]
    slots_per_probe = compiler["probe_budget"]["runtime_slots_per_phase_probe"]
    mirror_slots = compiler["probe_budget"]["packets_per_mirror_atlas"] * 72

    checks = {
        "source_frequency_compiler_verified": compiler["verified"] is True,
        "schedule_has_540_rows": len(rows) == 540,
        "probe_ids_are_contiguous": [row["probe_id"] for row in rows]
        == list(range(540)),
        "each_packet_has_18_probes": sorted(rows_by_packet.values()) == [18] * 30,
        "each_hesse_sector_pair_appears_30_times": sorted(rows_by_hesse_sector.values())
        == [30] * 18,
        "runtime_slots_tile_one_mirror_atlas": (
            slot_starts[0] == 0
            and slot_ends[-1] == mirror_slots - 1
            and slot_starts == [i * slots_per_probe for i in range(len(rows))]
        ),
        "mirror_identity_540_times_4_equals_2160": len(rows) * slots_per_probe
        == mirror_slots,
        "supercycle_identity_24_times_schedule_equals_12960": len(rows) * 24
        == compiler["probe_budget"]["phase_probes_per_supercycle"],
        "qutrit_phase_values_are_three_valued": sorted(
            {row["qutrit_phase_degrees"] for row in rows}
        )
        == [0, 120, 240],
        "sector_values_are_two_valued": sorted({row["sector"] for row in rows})
        == ["chiral", "gauge"],
    }

    result = {
        "theorem": "W33 frequency-bin Hashimoto lab packet",
        "verified": all(checks.values()),
        "breakthrough": (
            "The 11-bin frequency compiler now has a bench-facing shot schedule: "
            "one mirror atlas is 540 sector-probe rows, each row owns four "
            "runtime slots, so 540*4 = 2160 and 24 atlases give "
            "12960*4 = 51840."
        ),
        "schedule_summary": {
            "rows": len(rows),
            "packets_per_mirror_atlas": compiler["probe_budget"][
                "packets_per_mirror_atlas"
            ],
            "probes_per_packet": rows_by_packet[0],
            "runtime_slots_per_probe": slots_per_probe,
            "runtime_slots_per_mirror_atlas": mirror_slots,
            "supercycle_probe_rows": len(rows) * 24,
            "supercycle_runtime_slots": compiler["probe_budget"][
                "runtime_slots_per_supercycle"
            ],
            "csv": str(CSV_OUT.relative_to(ROOT)),
            "raw_jsonl_template": str(JSONL_OUT.relative_to(ROOT)),
        },
        "sample_rows": rows[:6],
        "source_certificates": [
            "data/w33_frequency_bin_hashimoto_compiler.json",
            "data/w33_hashimoto_packet_phase_bridge.json",
            "data/w33_holonet_firmware_fabric_profile.json",
        ],
        "claim_boundary": [
            "This is a schedule/schema packet, not measured bench data.",
            "Real runs must fill counts, visibility, and phase-error fields in the JSONL schema.",
            "Pass/fail thresholds for visibility and phase error remain a separate preregistered calibration choice.",
        ],
        "checks": checks,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_csv(rows)
    write_jsonl_template(rows)
    write_markdown(result)
    return result


def main() -> int:
    result = build_certificate()
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(result["theorem"])
    print(f"  verified: {result['verified']}")
    print(
        "  schedule: "
        f"{result['schedule_summary']['rows']} probes * "
        f"{result['schedule_summary']['runtime_slots_per_probe']} slots = "
        f"{result['schedule_summary']['runtime_slots_per_mirror_atlas']}"
    )
    print(f"  wrote {OUT}")
    print(f"  wrote {CSV_OUT}")
    print(f"  wrote {JSONL_OUT}")
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
