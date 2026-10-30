#!/usr/bin/env python3
"""Aggregate fail-closed release certificate for Passes 2767-2771."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(path: str):
    p = DATA / path
    if p.suffix == ".gz":
        with gzip.open(p, "rt") as f:
            return json.load(f)
    return json.loads(p.read_text())


def digest(path: str) -> str:
    return hashlib.sha256((DATA / path).read_bytes()).hexdigest()


def main() -> None:
    m36 = load("PART_BT2767_M36_PREPARATION_ROM.json")
    lift = load("PART_BT2768_SP43_METAPLECTIC_LIFT_SENSOR_summary.json")
    comp = load("PART_BT2769_CX_CENTRALIZER_COMPILER_summary.json")
    power = load("PART_BT2770_SWITCHING_ACTIVITY_PROXY.json")
    remote = load("PART_BT2771_REMOTE_QUTRIT_SUM_LINK.json")
    checks = {
        "m36_states_36": len(m36["rows"]) == 36,
        "m36_grade_census": m36["grade_census"] == {"deep": 8, "mid": 24, "shallow": 4},
        "m36_typed_ququart_boundary": m36["resource_type"] == "M36_Q4_RAW",
        "lift_group_51840": lift["group_order"] == 51840,
        "lift_classes_34": lift["conjugacy_classes"] == 34,
        "projective_signatures_15": lift["geometric_signatures"] == 15,
        "two_shot_lift_complete_34": lift["complete_joint_signatures"] == 34,
        "centralizer_108": comp["centralizer_order"] == 108,
        "centralizer_cosets_480": comp["right_cosets"] == 480,
        "compiler_max_rep_length_6": comp["coset_representative_length"]["max"] == 6,
        "compiler_positive_reduction": comp["unweighted_generator_savings"]["mean"] > 2.5,
        "compiler_entangler_reduction": comp["entangler_count_savings"]["mean"] > 0.6,
        "activity_is_proxy_only": power["status"] == "TECHNOLOGY_INDEPENDENT_PROXY_ONLY",
        "remote_basis_9": remote["exact_protocol"]["basis_states"] == 9,
        "remote_random_32": remote["exact_protocol"]["random_superpositions"] == 32,
        "remote_all_branches_accepted": remote["exact_protocol"]["total_conditional_success"] == 1.0,
        "remote_one_qutrit_pair": remote["exact_protocol"]["entanglement_cost"].startswith("one shared"),
        "remote_two_trits": remote["exact_protocol"]["classical_communication"].startswith("two trits"),
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]
    artifacts = [
        "PART_BT2767_M36_PREPARATION_ROM.json",
        "PART_BT2768_SP43_METAPLECTIC_LIFT_SENSOR.json.gz",
        "PART_BT2768_SP43_METAPLECTIC_LIFT_SENSOR_summary.json",
        "PART_BT2769_CX_CENTRALIZER_COMPILER.json.gz",
        "PART_BT2769_CX_CENTRALIZER_COMPILER_summary.json",
        "PART_BT2770_SWITCHING_ACTIVITY_PROXY.json",
        "PART_BT2771_REMOTE_QUTRIT_SUM_LINK.json",
    ]
    out = {
        "schema": "w33.pass2767_2771.release.v1",
        "status": "COMPLETE_LOCAL_EXACT_REMOTE_PNR_PENDING",
        "checks": checks,
        "check_count": len(checks),
        "artifact_sha256": {name: digest(name) for name in artifacts},
        "boundaries": {
            "m36": "exact preparation and magic witness; no M36 distillation or injection threshold claimed",
            "lift_sensor": "exact finite and projective-unitary computation",
            "compiler": "exact finite-group normalization and cost metrics",
            "fpga": "RTL and activity proxy local; placed timing, utilization, and physical power await remote toolchain",
            "remote_sum": "exact LOCC map and explicit loss model; no combined experimental process fidelity claimed",
        },
    }
    path = DATA / "PART_BT2767_BT2771_FIVE_FRONTIERS_results.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(f"PASS {len(checks)}/{len(checks)}; wrote {path}")


if __name__ == "__main__":
    main()
