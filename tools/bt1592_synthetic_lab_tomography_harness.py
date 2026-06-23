#!/usr/bin/env python3
"""BT1592: synthetic lab-tomography harness for the OAM holonet front end."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1592_synthetic_lab_tomography_harness.json"
CSV_OUT = ROOT / "analysis" / "BT1592_synthetic_lab_tomography_ingest.csv"
MD = ROOT / "analysis" / "BT1592_synthetic_lab_tomography_harness.md"

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

SECTOR_DIAGONAL_FIDELITY = 0.93
SECTOR_MAX_OFF_DIAGONAL = 0.02
SECTOR_MIN_DIAGONAL = 0.90


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sector_label(shift: tuple[int, int]) -> str:
    return f"X{shift[0]}Z{shift[1]}"


def recenter_class(shift: tuple[int, int]) -> str:
    x_shift, z_shift = shift
    if x_shift == 0 and z_shift == 0:
        return "centered_frame"
    if x_shift != 0 and z_shift == 0:
        return "oam_shift_only"
    if x_shift == 0 and z_shift != 0:
        return "phase_shift_only"
    return "mixed_shift_phase"


def build_sector_confusion() -> list[dict]:
    off_diagonal = round((1.0 - SECTOR_DIAGONAL_FIDELITY) / 8.0, 8)
    rows = []
    for source_index, source_shift in enumerate(TRANSLATIONS):
        probabilities = []
        for target_index, target_shift in enumerate(TRANSLATIONS):
            probabilities.append(
                {
                    "target_sector": target_index,
                    "target_shift": list(target_shift),
                    "target_label": sector_label(target_shift),
                    "probability": (
                        SECTOR_DIAGONAL_FIDELITY
                        if source_index == target_index
                        else off_diagonal
                    ),
                }
            )
        rows.append(
            {
                "source_sector": source_index,
                "source_shift": list(source_shift),
                "source_label": sector_label(source_shift),
                "recenter_class": recenter_class(source_shift),
                "probabilities": probabilities,
                "row_sum": round(sum(row["probability"] for row in probabilities), 8),
                "diagonal_probability": SECTOR_DIAGONAL_FIDELITY,
                "max_off_diagonal": off_diagonal,
            }
        )
    return rows


def build_radial_tomography(radial: dict) -> list[dict]:
    class_thresholds = {
        "centered_frame": radial["model"]["core_gate_threshold"],
        "mixed_shift_phase": radial["model"]["recentered_threshold"],
        "oam_shift_only": radial["model"]["recentered_threshold"],
        "phase_shift_only": radial["model"]["recentered_threshold"],
    }
    rows = []
    for klass, eta in sorted(radial["class_eta_max"].items()):
        threshold = class_thresholds[klass]
        margin = round(threshold - eta, 12)
        rows.append(
            {
                "recenter_class": klass,
                "observed_eta": eta,
                "threshold": threshold,
                "margin": margin,
                "passes": eta <= threshold,
                "source": "BT1589 symbolic LG radial-shell covariance",
            }
        )
    return rows


def build_lane_acceptance(lanes: dict) -> list[dict]:
    lane_counts = lanes["lane_counts"]
    detector_counts = {
        int(slot): count for slot, count in lanes["detector_slot_counts"].items()
    }
    action_counts = lanes["action_level_tick_counts"]
    return [
        {
            "metric": "segments",
            "observed": lanes["counts"]["segments"],
            "expected": 1080,
            "passes": lanes["counts"]["segments"] == 1080,
        },
        {
            "metric": "total_ticks",
            "observed": lanes["counts"]["total_ticks"],
            "expected": 77760,
            "passes": lanes["counts"]["total_ticks"] == 77760,
        },
        {
            "metric": "six_hesse_lanes_balanced",
            "observed": sorted(lane_counts.values()),
            "expected": [12960] * 6,
            "passes": sorted(lane_counts.values()) == [12960] * 6,
        },
        {
            "metric": "detector_slots_balanced",
            "observed": sorted(detector_counts.values()),
            "expected": [19440] * 4,
            "passes": sorted(detector_counts.values()) == [19440] * 4,
        },
        {
            "metric": "native_d4_ticks",
            "observed": action_counts["native_d4_square_pulse"],
            "expected": 25920,
            "passes": action_counts["native_d4_square_pulse"] == 25920,
        },
        {
            "metric": "s4_relabel_ticks",
            "observed": action_counts["s4_analyzer_relabel"],
            "expected": 51840,
            "passes": action_counts["s4_analyzer_relabel"] == 51840,
        },
    ]


def write_csv(
    sector_rows: list[dict], radial_rows: list[dict], lane_rows: list[dict]
) -> None:
    fieldnames = [
        "measurement_id",
        "kind",
        "label",
        "observed",
        "threshold_or_expected",
        "passes",
    ]
    output_rows = []
    for row in sector_rows:
        source = row["source_sector"]
        output_rows.append(
            {
                "measurement_id": f"sector_diag_{source:02d}",
                "kind": "sector_diagonal",
                "label": row["source_label"],
                "observed": f"{row['diagonal_probability']:.8f}",
                "threshold_or_expected": f"{SECTOR_MIN_DIAGONAL:.8f}",
                "passes": str(row["diagonal_probability"] >= SECTOR_MIN_DIAGONAL),
            }
        )
        for probability in row["probabilities"]:
            if probability["target_sector"] == source:
                continue
            output_rows.append(
                {
                    "measurement_id": f"sector_off_{source:02d}_{probability['target_sector']:02d}",
                    "kind": "sector_off_diagonal",
                    "label": f"{row['source_label']}->{probability['target_label']}",
                    "observed": f"{probability['probability']:.8f}",
                    "threshold_or_expected": f"{SECTOR_MAX_OFF_DIAGONAL:.8f}",
                    "passes": str(
                        probability["probability"] <= SECTOR_MAX_OFF_DIAGONAL
                    ),
                }
            )
    for row in radial_rows:
        output_rows.append(
            {
                "measurement_id": f"radial_{row['recenter_class']}",
                "kind": "radial_eta",
                "label": row["recenter_class"],
                "observed": f"{row['observed_eta']:.12f}",
                "threshold_or_expected": f"{row['threshold']:.12f}",
                "passes": str(row["passes"]),
            }
        )
    for row in lane_rows:
        output_rows.append(
            {
                "measurement_id": f"lane_{row['metric']}",
                "kind": "lane_replay",
                "label": row["metric"],
                "observed": json.dumps(row["observed"], sort_keys=True),
                "threshold_or_expected": json.dumps(row["expected"], sort_keys=True),
                "passes": str(row["passes"]),
            }
        )
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def parse_csv() -> dict:
    rows = list(csv.DictReader(CSV_OUT.open(encoding="utf-8")))
    by_kind = Counter(row["kind"] for row in rows)
    return {
        "path": str(CSV_OUT.relative_to(ROOT)),
        "rows": len(rows),
        "kind_counts": dict(sorted(by_kind.items())),
        "all_rows_pass": all(row["passes"] == "True" for row in rows),
        "sample_rows": rows[:8],
    }


def main() -> None:
    frontend = load_json("data/bt1591_oam_mdnn_frontend_firewall.json")
    radial = load_json("data/bt1589_lg_oam_radial_covariance_simulator.json")
    lanes = load_json("data/bt1590_full_witness_lane_sheet_compiler.json")

    sector_rows = build_sector_confusion()
    radial_rows = build_radial_tomography(radial)
    lane_rows = build_lane_acceptance(lanes)
    write_csv(sector_rows, radial_rows, lane_rows)
    csv_ingest = parse_csv()

    diagonal_values = [row["diagonal_probability"] for row in sector_rows]
    off_diagonal_values = [
        probability["probability"]
        for row in sector_rows
        for probability in row["probabilities"]
        if probability["target_sector"] != row["source_sector"]
    ]
    checks = {
        "frontend_verified": frontend["verified"] is True,
        "radial_verified": radial["verified"] is True,
        "lane_sheet_verified": lanes["verified"] is True,
        "sector_matrix_is_9_by_9": len(sector_rows) == 9
        and all(len(row["probabilities"]) == 9 for row in sector_rows),
        "sector_rows_are_stochastic": all(
            abs(row["row_sum"] - 1.0) < 1e-9 for row in sector_rows
        ),
        "sector_diagonal_above_threshold": min(diagonal_values) >= SECTOR_MIN_DIAGONAL,
        "sector_off_diagonal_below_threshold": max(off_diagonal_values)
        <= SECTOR_MAX_OFF_DIAGONAL,
        "radial_rows_all_pass": all(row["passes"] for row in radial_rows),
        "lane_replay_rows_all_pass": all(row["passes"] for row in lane_rows),
        "csv_ingest_all_rows_pass": csv_ingest["all_rows_pass"],
        "csv_ingest_has_expected_rows": csv_ingest["rows"] == 9 + 72 + 4 + 6,
    }
    result = {
        "bt": 1592,
        "title": "Synthetic lab-tomography harness for the OAM holonet front end",
        "verified": all(checks.values()),
        "source_packets": {
            "frontend_firewall": "data/bt1591_oam_mdnn_frontend_firewall.json",
            "radial_covariance": "data/bt1589_lg_oam_radial_covariance_simulator.json",
            "lane_sheet": "data/bt1590_full_witness_lane_sheet_compiler.json",
        },
        "acceptance_thresholds": {
            "sector_min_diagonal": SECTOR_MIN_DIAGONAL,
            "sector_max_off_diagonal": SECTOR_MAX_OFF_DIAGONAL,
            "centered_radial_eta": radial["model"]["core_gate_threshold"],
            "recentered_radial_eta": radial["model"]["recentered_threshold"],
        },
        "sector_confusion_matrix": sector_rows,
        "radial_tomography": radial_rows,
        "lane_replay_acceptance": lane_rows,
        "csv_ingest": csv_ingest,
        "interpretation": (
            "BT1592 turns the BT1591 front-end firewall into a synthetic lab harness: "
            "a 9x9 sector confusion matrix, radial-shell tomography rows, exact lane "
            "replay checks, and a CSV ingest path that can be replaced by real bench data."
        ),
        "honesty_boundary": (
            "The numbers here are acceptance fixtures and deterministic replay checks. "
            "They are not measured OAM crosstalk, measured radial leakage, or detector data."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1592 Synthetic Lab-Tomography Harness\n\n"
        "BT1592 adds the bench-facing shape of the OAM holonet front end: a `9x9` "
        "sector confusion matrix, radial-shell tomography rows, lane replay acceptance "
        "checks, and a CSV ingest fixture at `analysis/BT1592_synthetic_lab_tomography_ingest.csv`. "
        "All rows pass the synthetic acceptance thresholds; replacing the CSV values with "
        "real measurements is the intended falsification path.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1592,
                "verified": result["verified"],
                "csv_rows": csv_ingest["rows"],
                "sector_diagonal": SECTOR_DIAGONAL_FIDELITY,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
