#!/usr/bin/env python3
"""BT765 — unified phase/duo/Pluecker CI runner.

This runner orchestrates the current fail-closed chain:

  BT753  local phase+duo selector enumeration
  BT761  local+global gluing firewall
  BT758  Q(4,3) target model verifier
  BT760  Q(4,3) oriented-apartment mirror harness
  BT764  explicit r^6 transport verifier

Default mode is audit mode: missing optional artifacts are reported as pending
rather than silently promoted.  Use --strict to require every command to exit 0
and every expected output to exist.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt765_phase_duo_plucker_ci_summary.json"

STEPS = [
    {
        "id": "BT753",
        "label": "phase_duo_candidate_enumerator",
        "command": [sys.executable, "analysis/bt753_phase_duo_candidate_enumerator.py"],
        "expected_outputs": ["data/bt753_phase_duo_candidate_enumerator.json"],
        "critical": True,
    },
    {
        "id": "BT761",
        "label": "phase_duo_gluing_runner",
        "command": [sys.executable, "analysis/bt761_phase_duo_gluing_runner.py"],
        "expected_outputs": ["data/bt761_phase_duo_gluing_runner_results.json"],
        "critical": True,
    },
    {
        "id": "BT758",
        "label": "q43_plucker_model_verifier",
        "command": [sys.executable, "analysis/bt758_q43_plucker_model_verifier.py"],
        "expected_outputs": ["data/bt758_q43_plucker_model_verifier_results.json"],
        "critical": True,
    },
    {
        "id": "BT760",
        "label": "q43_duo_transport_harness",
        "command": [sys.executable, "analysis/bt760_q43_duo_transport_harness.py"],
        "expected_outputs": ["data/bt760_q43_duo_transport_harness_results.json"],
        "critical": True,
    },
    {
        "id": "BT764",
        "label": "r6_transport_verifier",
        "command": [sys.executable, "analysis/bt764_r6_transport_verifier.py"],
        "expected_outputs": ["data/bt764_r6_transport_verifier_results.json"],
        "critical": False,
        "pending_if_missing": "data/bt760_root_torsor_to_q43_transport.json",
    },
]


def run_step(step, execute: bool, strict: bool):
    missing_gate = step.get("pending_if_missing")
    if missing_gate and not (ROOT / missing_gate).exists():
        return {
            "id": step["id"],
            "label": step["label"],
            "status": "pending_missing_input",
            "missing_input": missing_gate,
            "accepted": False,
            "boundary": "Pending input means no Pluecker-duo promotion is allowed."
        }
    if not execute:
        return {
            "id": step["id"],
            "label": step["label"],
            "status": "planned",
            "command": step["command"],
            "expected_outputs": step["expected_outputs"],
            "accepted": False,
        }
    proc = subprocess.run(
        step["command"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    outputs = {p: (ROOT / p).exists() for p in step["expected_outputs"]}
    ok = proc.returncode == 0 and all(outputs.values())
    status = "pass" if ok else "fail"
    if not ok and not strict and not step.get("critical", True):
        status = "pending_or_fail_noncritical"
    return {
        "id": step["id"],
        "label": step["label"],
        "status": status,
        "returncode": proc.returncode,
        "expected_outputs": outputs,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "accepted": ok,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--execute", action="store_true", help="actually run the chain; default only writes a plan")
    ap.add_argument("--strict", action="store_true", help="fail nonzero unless every step passes")
    args = ap.parse_args()

    results = [run_step(step, execute=args.execute, strict=args.strict) for step in STEPS]
    critical_pass = all(r.get("accepted") for r in results if next(s for s in STEPS if s["id"] == r["id"]).get("critical", True))
    transport_pass = any(r["id"] == "BT764" and r.get("accepted") for r in results)
    summary = {
        "theorem": "BT765 unified phase-duo Pluecker CI runner",
        "mode": "execute" if args.execute else "plan_only",
        "strict": args.strict,
        "steps": results,
        "critical_chain_pass": critical_pass,
        "transport_pass": transport_pass,
        "accepted_plucker_duo_claim": critical_pass and transport_pass,
        "boundary": "BT753+BT761+BT758+BT760 can pass target/local/global checks, but the Pluecker-duo claim remains false until BT764 passes against an explicit transport table."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.strict and not summary["accepted_plucker_duo_claim"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
