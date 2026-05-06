#!/usr/bin/env python3
"""Run the E8 operation-bridge artifact pipeline in dependency order.

This is the single-command harness for the H1(W33;Z) -> E8 operation bridge.
It intentionally does not fabricate missing artifacts.  It performs preflight,
then runs each script only when its declared inputs are present.

Usage
-----
  python tools/run_e8_operation_bridge_pipeline.py --dry-run
  python tools/run_e8_operation_bridge_pipeline.py

Pipeline
--------
1. tools/build_e8_root_metadata_table.py
2. tools/export_e8_structure_constants_from_w33_discrete.py
3. tools/verify_e8_z3grading_from_structure_constants.py
4. tools/analyze_e8_g1g2_to_g0_couplings.py
5. tools/analyze_e8_g1g1_couplings_cubic_firewall.py
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Step:
    name: str
    script: str
    requires: List[str]
    produces: List[str]


STEPS: List[Step] = [
    Step(
        name="build_root_metadata",
        script="tools/build_e8_root_metadata_table.py",
        requires=[
            "tools/verify_e8_root_system_from_trinification.py",
            "artifacts/verify_e8_dynkin_from_trinification.json",
            "artifacts/sage_verify_e8_trinification_closeout.json",
            "artifacts/e8_coxeter6_orbits.json",
            "artifacts/e8_root_to_edge.json",
        ],
        produces=[
            "artifacts/e8_root_metadata_table.json",
            "artifacts/e8_root_metadata_table.md",
        ],
    ),
    Step(
        name="export_structure_constants",
        script="tools/export_e8_structure_constants_from_w33_discrete.py",
        requires=["artifacts/e8_root_metadata_table.json"],
        produces=[
            "artifacts/e8_structure_constants_w33_discrete.json",
            "artifacts/e8_structure_constants_w33_discrete.md",
        ],
    ),
    Step(
        name="verify_z3_grading",
        script="tools/verify_e8_z3grading_from_structure_constants.py",
        requires=[
            "artifacts/e8_structure_constants_w33_discrete.json",
            "artifacts/e8_root_metadata_table.json",
        ],
        produces=[
            "artifacts/e8_z3grading_from_structure_constants.json",
            "artifacts/e8_z3grading_from_structure_constants.md",
        ],
    ),
    Step(
        name="analyze_g1g2_to_g0",
        script="tools/analyze_e8_g1g2_to_g0_couplings.py",
        requires=[
            "artifacts/e8_structure_constants_w33_discrete.json",
            "artifacts/e8_root_metadata_table.json",
        ],
        produces=[
            "artifacts/e8_g1g2_to_g0_couplings.json",
            "artifacts/e8_g1g2_to_g0_couplings.md",
        ],
    ),
    Step(
        name="analyze_g1g1_cubic_firewall",
        script="tools/analyze_e8_g1g1_couplings_cubic_firewall.py",
        requires=[
            "artifacts/e8_structure_constants_w33_discrete.json",
            "artifacts/e8_root_metadata_table.json",
            "artifacts/canonical_su3_gauge_and_cubic.json",
            "artifacts/firewall_bad_triads_mapping.json",
        ],
        produces=[
            "artifacts/e8_g1g1_couplings_cubic_firewall.json",
            "artifacts/e8_g1g1_couplings_cubic_firewall.md",
        ],
    ),
]


def exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def step_status(step: Step) -> dict:
    return {
        "name": step.name,
        "script": step.script,
        "script_exists": exists(step.script),
        "requires": {p: exists(p) for p in step.requires},
        "produces": {p: exists(p) for p in step.produces},
        "ready": exists(step.script) and all(exists(p) for p in step.requires),
    }


def preflight() -> dict:
    statuses = [step_status(s) for s in STEPS]
    first_blocked = None
    for status in statuses:
        missing = []
        if not status["script_exists"]:
            missing.append(status["script"])
        missing.extend([p for p, ok in status["requires"].items() if not ok])
        if missing:
            first_blocked = {
                "step": status["name"],
                "missing": missing,
            }
            break
    return {
        "root": str(ROOT),
        "steps": statuses,
        "first_blocked": first_blocked,
        "ready_to_run_all": first_blocked is None,
    }


def run_step(step: Step) -> dict:
    status = step_status(step)
    missing = []
    if not status["script_exists"]:
        missing.append(step.script)
    missing.extend([p for p, ok in status["requires"].items() if not ok])
    if missing:
        return {
            "name": step.name,
            "status": "blocked",
            "missing": missing,
            "returncode": None,
        }

    proc = subprocess.run(
        [sys.executable, step.script],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "name": step.name,
        "status": "ok" if proc.returncode == 0 else "failed",
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "produces": {p: exists(p) for p in step.produces},
    }


def run_pipeline() -> dict:
    results = []
    for step in STEPS:
        result = run_step(step)
        results.append(result)
        if result["status"] != "ok":
            break
    return {
        "status": "ok" if len(results) == len(STEPS) and all(r["status"] == "ok" for r in results) else "incomplete",
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Only print readiness/preflight information.")
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    args = parser.parse_args()

    if args.dry_run:
        payload = {"mode": "dry_run", "preflight": preflight()}
    else:
        payload = {"mode": "run", "preflight_before": preflight(), "pipeline": run_pipeline(), "preflight_after": preflight()}

    text = json.dumps(payload, indent=2, sort_keys=True)
    print(text)

    if not args.dry_run and payload["pipeline"]["status"] != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()
