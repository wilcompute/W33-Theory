#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1397_example_optimality_certificate_verification.json")
    ns = ap.parse_args()
    cert = ROOT / "examples" / "bt1397_example_s3_maxsat_optimality_certificate.json"
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1395_s3_maxsat_bound_pathway.py"), "--certificate", str(cert)], cwd=ROOT, check=True, capture_output=True, text=True)
    parsed = json.loads(proc.stdout)
    example = json.loads(cert.read_text(encoding="utf-8"))
    checks = {
        "bt1395_accepts_example": parsed["verified"] is True,
        "example_reaches_optimal_certified_path": parsed["optimality_status"] == "optimal_certified",
        "example_marked_not_solver_generated": example["solver"] == "example-demonstration-not-solver-generated",
        "source_warns_not_project_proof": "Not a project-level global optimality proof" in example["source"],
        "upper_bound_210": example["upper_bound"] == 210,
    }
    result = {
        "bt": 1397,
        "title": "Example S3 MaxSAT optimality certificate pathway",
        "verified": all(checks.values()),
        "checks": checks,
        "example_certificate": "examples/bt1397_example_s3_maxsat_optimality_certificate.json",
        "bt1395_status_on_example": parsed["optimality_status"],
        "project_optimality_status": "not_solver_certified",
        "boundary": "This demonstrates the optimality-certificate pathway with a synthetic upper-bound file. It is not a solver-generated proof that score 210 is globally optimal."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1397, "verified": result["verified"], "project_optimality_status": result["project_optimality_status"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
