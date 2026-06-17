#!/usr/bin/env python3
"""BT1217 -- fused holonet lab-readiness score.

Combines BT1212 (lambda-lock adversarial robustness), BT1214/BT1216
(Clifford tomography signature), BT1215 (K3 schema readiness), and BT1211
(encoded q-invariance) into a single scorecard.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_INPUTS = {
    "lambda_adversary": Path("data/bt1212_lambda_lock_adversary_model_summary.json"),
    "tomography": Path("data/bt1216_synthetic_clifford_tomography_recovery_summary.json"),
    "k3_schema": Path("data/bt1215_k3_geometry_sample_stub_summary.json"),
    "encoded_q": Path("data/bt1211_encoded_lambda_lock_invariance_summary.json"),
}

WEIGHTS = {
    "lambda_lock_robustness": 0.30,
    "clifford_tomography_signature": 0.30,
    "encoded_q_invariance": 0.20,
    "k3_schema_readiness": 0.10,
    "hardware_threshold_readiness": 0.10,
}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def score(inputs: dict[str, dict]) -> dict:
    lambda_ok = inputs["lambda_adversary"]["robust_lambda_lock_pass"]
    tomography_ok = inputs["tomography"]["recovers_bt1214_signature"]
    encoded_ok = inputs["encoded_q"]["cross_layer_q_invariant"]
    k3_schema_ok = inputs["k3_schema"]["valid"] and inputs["k3_schema"]["claim_status"] == "schema_stub_only"
    # Hardware threshold is intentionally not passed: GKP-state generation and encoded threshold remain open.
    hardware_threshold_ok = False

    components = {
        "lambda_lock_robustness": {"weight": WEIGHTS["lambda_lock_robustness"], "passes": lambda_ok},
        "clifford_tomography_signature": {"weight": WEIGHTS["clifford_tomography_signature"], "passes": tomography_ok},
        "encoded_q_invariance": {"weight": WEIGHTS["encoded_q_invariance"], "passes": encoded_ok},
        "k3_schema_readiness": {"weight": WEIGHTS["k3_schema_readiness"], "passes": k3_schema_ok},
        "hardware_threshold_readiness": {"weight": WEIGHTS["hardware_threshold_readiness"], "passes": hardware_threshold_ok},
    }
    readiness = sum(v["weight"] for v in components.values() if v["passes"])
    return {
        "bt": 1217,
        "title": "Holonet lab-readiness scorecard",
        "score": readiness,
        "score_percent": round(100.0 * readiness, 1),
        "components": components,
        "readiness_level": "protocol-ready_not_threshold-ready" if readiness >= 0.8 and not hardware_threshold_ok else "needs_foundational_work",
        "dashboard_claim": "The holonet demonstrator protocol is ready as a falsification roadmap; the fault-tolerant GKP/Steinberg machine is not threshold-ready.",
        "next_blocker": "physical GKP qutrit state generation, threshold squeezing, and encoded syndrome recovery",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/bt1217_holonet_lab_readiness_score.json"))
    args = p.parse_args()
    inputs = {k: load(v) for k, v in DEFAULT_INPUTS.items()}
    result = score(inputs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1217, "score_percent": result["score_percent"], "level": result["readiness_level"]}, indent=2))


if __name__ == "__main__":
    main()
