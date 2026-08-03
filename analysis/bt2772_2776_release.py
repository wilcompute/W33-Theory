#!/usr/bin/env python3
"""Aggregate exact release certificate for Passes 2772-2776."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name: str):
    path = DATA / name
    if path.suffix == ".gz":
        with gzip.open(path, "rt") as handle:
            return json.load(handle)
    return json.loads(path.read_text())


def sha(name: str) -> str:
    return hashlib.sha256((DATA / name).read_bytes()).hexdigest()


def main() -> None:
    dist = load("PART_BT2772_M36_TWO_COPY_DISTILLATION.json")
    sensor = load("PART_BT2773_PHYSICAL_METAPLECTIC_SENSOR.json")
    compiler = load("PART_BT2774_COMPRESSED_CX_COMPILER_summary.json")
    ci = load("PART_BT2775_CI_PLACED_NETLIST_CLOSURE.json")
    repeater = load("PART_BT2776_REPEATER_REMOTE_SUM_summary.json")
    checks = {
        "dist_search_85680": dist["search"]["protocol_instances"] == 85680,
        "dist_closed_9264": dist["search"]["m36_closed_instances"] == 9264,
        "dist_improving_48": dist["search"]["strictly_distilling_instances"] == 48,
        "dist_best_slope_half": abs(dist["search"]["best_output_infidelity_slope_in_p"] - 0.5) < 1e-12,
        "dist_threshold_two_thirds": dist["selected_protocol"]["distillation_region"] == "0<p<2/3",
        "sensor_group_51840": sensor["group_order"] == 51840,
        "sensor_k1_alphabet_16": sensor["trace_alphabet"]["k1_size"] == 16,
        "sensor_k2_alphabet_10": sensor["trace_alphabet"]["k2_size"] == 10,
        "sensor_four_settings": len(sensor["physical_protocol"]["settings"]) == 4,
        "sensor_001_shots_21736": sensor["nearest_alphabet_shot_bound"]["shots"]["0.001"]["four_setting_detected_shots"] == 21736,
        "compiler_480": compiler["theorem"]["cx_conjugacy_class"] == 480,
        "compiler_40x12": compiler["theorem"]["lines"] * compiler["theorem"]["forms_per_line"] == 480,
        "compiler_forms_det2": all((f[0] * f[3] - f[1] * f[2]) % 3 == 2 for f in compiler["theorem"]["form_alphabet"]),
        "compiler_rep_max6": compiler["maximum_word_length"] == 6,
        "compiler_suffix_108": compiler["centralizer_occupied_hashes"] == 108,
        "compiler_compression_gt54": compiler["storage"]["compression_ratio"] > 54,
        "ci_old_drift_closed": all(ci["checks"].values()),
        "ci_jobs_decoupled": any("split" in repair for repair in ci["repairs"]),
        "repeater_purification_threshold": repeater["qutrit_purification"]["distillation_region"] == "F>1/3",
        "repeater_erasure_threshold": repeater["outer_erasure_code"]["concatenation_threshold"] == "e<1/2 (eta>1/2)",
        "repeater_transversal_sum": repeater["outer_erasure_code"]["transversal_sum_verified"],
        "repeater_best_8_segments": repeater["best_row_with_F_at_least_0_6"]["segments"] == 8,
        "repeater_best_one_round": repeater["best_row_with_F_at_least_0_6"]["purification_rounds"] == 1,
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]
    artifacts = [
        "PART_BT2772_M36_TWO_COPY_DISTILLATION.json",
        "PART_BT2773_PHYSICAL_METAPLECTIC_SENSOR.json",
        "PART_BT2774_COMPRESSED_CX_COMPILER_summary.json",
        "PART_BT2775_CI_PLACED_NETLIST_CLOSURE.json",
        "PART_BT2776_REPEATER_REMOTE_SUM_summary.json",
    ]
    out = {
        "schema": "w33.pass2772_2776.release.v1",
        "status": "COMPLETE_LOCAL_EXACT_REMOTE_RTL_PNR_PENDING",
        "check_count": len(checks),
        "checks": checks,
        "artifact_sha256": {name: sha(name) for name in artifacts},
        "frontiers": {
            "2772": "two-copy M36 stabilizer distillation with exact p<2/3 threshold",
            "2773": "four-setting physical metaplectic trace sensor and conservative shot bounds",
            "2774": "40x12 CX class factorization and 1.9 kB compressed compiler packet",
            "2775": "certificate-drift repair plus independent RTL/synthesis/P&R jobs",
            "2776": "qutrit purification, [[3,1,2]]_3 erasure threshold, and nested repeater budget",
        },
        "boundaries": {
            "distillation": "exhaustive for two-copy binary [[4,2]] stabilizer projections, not arbitrary multi-copy ququart protocols",
            "sensor": "exact trace alphabet and statistical bound, not measured optical calibration",
            "compiler": "exact finite decomposition; FPGA utilization and timing await remote toolchain",
            "ci": "local reproducibility closed; placed evidence must be observed before promotion",
            "repeater": "exact independent-isotropic/erasure recurrences plus an illustrative queueing approximation",
        },
    }
    path = DATA / "PART_BT2772_BT2776_FIVE_FRONTIERS_results.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"PASS {len(checks)}/{len(checks)}; wrote {path}")


if __name__ == "__main__":
    main()
