#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text())


def sha(name):
    return hashlib.sha256((DATA / name).read_bytes()).hexdigest()


def main():
    m36 = load("PART_BT2777_M36_4_2_STABILIZER_CENSUS_summary.json")
    sensor = load("PART_BT2778_METAPLECTIC_INTERFEROMETER_summary.json")
    compiler = load("PART_BT2779_STRUCTURED_CX_COMPILER_summary.json")
    repeater = load("PART_BT2781_REPEATER_REMOTE_SUM_summary.json")
    rom = load("PART_BT2767_M36_PREPARATION_ROM.json")

    rows = {row["grade"]: row for row in m36["rows"]}
    long_link = repeater["scenario_summary"]["1280"]["best_distillable_rate"]

    checks = {
        "distill_codes_5355": m36["search_space"]["isotropic_rank2_codes"] == 5355,
        "distill_branches_21420": m36["search_space"]["branches"] == 21420,
        "distill_no_improving_shallow": rows["shallow"]["m36_closed_branches"] > 0
        and rows["shallow"]["certified_nonimproving_branches"]
        == rows["shallow"]["m36_closed_branches"],
        "distill_no_improving_deep": rows["deep"]["m36_closed_branches"] > 0
        and rows["deep"]["certified_nonimproving_branches"]
        == rows["deep"]["m36_closed_branches"],
        "distill_no_improving_mid": rows["mid"]["m36_closed_branches"] > 0
        and rows["mid"]["certified_nonimproving_branches"]
        == rows["mid"]["m36_closed_branches"],
        "sensor_classes_34": sensor["class_count"] == 34,
        "sensor_trace_pairs_33": sensor["theta_pair_count"] == 33,
        "sensor_min_trace_one_ninth": abs(
            sensor["minimum_nonzero_normalized_trace_magnitude"] - 1 / 9
        )
        < 1e-12,
        "sensor_four_quadrature_budget": sensor[
            "total_detector_events_four_quadratures"
        ]
        == 4 * sensor["shots_per_quadrature_hoeffding"],
        "compiler_group_51840": compiler["checks"]["group_elements"] == 51840,
        "compiler_pairs_40x12": compiler["factorization"]["cosets"] == 480
        and compiler["checks"]["all_pairs_present"],
        "compiler_suffixes_108": compiler["factorization"]["suffixes"] == 108,
        "compiler_all_rewrites": compiler["checks"]["all_rewrites_verified"],
        "compiler_compression_gt_40": compiler["memory_bits"]["compression_ratio"]
        > 40,
        "rom_deterministic_schema": rom["schema"].endswith(".v2")
        and "NumPy" in rom["determinism"],
        "repeater_fixed_points": repeater["isotropic_recurrence"]["fixed_points"]
        == [1 / 9, 1 / 3, 1.0],
        "repeater_improvement_region": repeater["isotropic_recurrence"][
            "improvement_region"
        ]
        == "F > 1/3",
        "repeater_1280_distillable": long_link is not None
        and long_link["distillable"],
        "repeater_1280_segmented": long_link["segments"] > 1,
        "repeater_remote_rate_positive": long_link["remote_sum_rate_hz"] > 0,
    }
    assert all(checks.values()), [key for key, value in checks.items() if not value]

    artifacts = [
        "PART_BT2767_M36_PREPARATION_ROM.json",
        "PART_BT2777_M36_4_2_STABILIZER_CENSUS_summary.json",
        "PART_BT2778_METAPLECTIC_INTERFEROMETER_summary.json",
        "PART_BT2779_STRUCTURED_CX_COMPILER_summary.json",
        "PART_BT2781_REPEATER_REMOTE_SUM_summary.json",
    ]
    output = {
        "schema": "w33.pass2784_2788.five_frontiers.v2",
        "canonical_pass_range": "2784-2788",
        "provisional_artifact_ids": {
            "2777": "2784",
            "2778": "2785",
            "2779": "2786",
            "2780": "2787",
            "2781": "2788",
        },
        "status": "COMPLETE_LOCAL_EXACT_REMOTE_HARDWARE_PENDING",
        "checks": checks,
        "check_count": len(checks),
        "artifact_sha256": {name: sha(name) for name in artifacts},
        "boundaries": {
            "distillation": "exhaustive only for the frozen canonical logical Pauli decoder gauge; arbitrary logical Clifford decoders remain open",
            "sensor": "shot budget assumes independent phase-stable path measurements and calibrated determinant",
            "compiler": "exact matrix accumulator remains upstream input",
            "hardware": "Icarus/Yosys/nextpnr evidence must be observed remotely",
            "repeater": "exact Bell-diagonal recurrences plus engineering scenarios, not measured end-to-end hardware",
        },
    }
    path = DATA / "PART_BT2784_BT2788_FIVE_FRONTIERS_results.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"PASS {len(checks)}/{len(checks)}; wrote {path}")


if __name__ == "__main__":
    main()
