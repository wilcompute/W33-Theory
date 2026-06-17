#!/usr/bin/env python3
"""BT1225 -- recent artifacts verifier.

Checks the BT1218--BT1224 packet for file presence and core claims.  This is a
lightweight CI-style verifier for the latest holonet/R3 artifacts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_FILES = [
    "paper/sections/sec_bt1218_holonet_experimental_readiness.tex",
    "data/bt1218_holonet_experimental_readiness_summary.json",
    "data/bt1219_exact_sl23_closure_summary.json",
    "data/bt1220_r3_schema_valid_mock_sequence_summary.json",
    "data/bt1221_exact_sp43_generator_summary.json",
    "tools/integrate_bt1218_holonet_experimental_readiness.py",
    "data/bt1223_r3_sample_status_validator_summary.json",
    "data/bt1224_exact_clifford_fingerprint_dashboard_summary.json",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def verify(root: Path) -> dict:
    missing = [p for p in REQUIRED_FILES if not (root / p).exists()]
    checks = {"required_files_present": not missing}
    if not missing:
        bt1218 = read_json(root / "data/bt1218_holonet_experimental_readiness_summary.json")
        bt1219 = read_json(root / "data/bt1219_exact_sl23_closure_summary.json")
        bt1221 = read_json(root / "data/bt1221_exact_sp43_generator_summary.json")
        bt1223 = read_json(root / "data/bt1223_r3_sample_status_validator_summary.json")
        bt1224 = read_json(root / "data/bt1224_exact_clifford_fingerprint_dashboard_summary.json")
        checks.update({
            "bt1218_protocol_not_threshold_ready": bt1218.get("readiness_claim") == "protocol_ready_not_threshold_ready",
            "bt1219_sl23_exact": bt1219.get("order") == 24 and bt1219.get("closure_ok") is True,
            "bt1221_sp43_exact": bt1221.get("order") == 51840 and bt1221.get("all_generated_matrices_symplectic") is True,
            "bt1223_blocks_mock_r3": bt1223.get("candidate_allowed") is False and bt1223.get("counts", {}).get("blocked") == 4,
            "bt1224_dashboard_pass": bt1224.get("dashboard_pass") is True,
        })
    return {
        "bt": 1225,
        "title": "Recent BT artifact verifier",
        "required_files": REQUIRED_FILES,
        "missing_files": missing,
        "checks": checks,
        "passes_all_checks": all(checks.values()),
        "interpretation": "The recent holonet/R3 packet is internally consistent if all files exist, exact finite groups match their orders, mock R3 samples remain blocked, and the dashboard passes.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("data/bt1225_recent_artifacts_verifier.json"))
    args = parser.parse_args()
    result = verify(args.root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1225, "passes": result["passes_all_checks"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
