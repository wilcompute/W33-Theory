#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from bt1376_s3_gauge_radius3_local_optimum_certificate import build_score_tables, edge_score
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def witness_score() -> int:
    tables = build_score_tables()
    edge_scores = tables["edge_scores"]
    return sum(edge_score(edge_scores, a, b, IMPROVED_GAUGE_LABELS[a], IMPROVED_GAUGE_LABELS[b]) for a, b in tables["edges"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1387_s3_maxsat_solver_harness.json")
    ap.add_argument("--wcnf", type=Path, default=ROOT / "data" / "generated" / "bt1384_s3_gauge_maxsat.wcnf")
    ap.add_argument("--solver", default="")
    ns = ap.parse_args()

    # Always regenerate/export the canonical WCNF manifest first.
    subprocess.run([sys.executable, str(ROOT / "tools" / "bt1384_export_s3_gauge_maxsat.py"), "--wcnf", str(ns.wcnf)], cwd=ROOT, check=True, capture_output=True, text=True)
    manifest = load("data/bt1384_s3_gauge_maxsat_manifest.json")
    score = witness_score()

    candidates = [ns.solver] if ns.solver else ["open-wbo", "maxhs", "cashwmaxsatcoreplus", "uwrmaxsat"]
    available = [c for c in candidates if c and shutil.which(c)]
    solver_run = None
    if available:
        solver = available[0]
        proc = subprocess.run([solver, str(ns.wcnf)], cwd=ROOT, capture_output=True, text=True, timeout=120)
        solver_run = {"solver": solver, "returncode": proc.returncode, "stdout_head": proc.stdout[:4000], "stderr_head": proc.stderr[:2000]}

    checks = {
        "wcnf_manifest_verified": manifest["verified"] is True,
        "wcnf_file_exists": ns.wcnf.exists(),
        "witness_score_210": score == 210,
        "variables_780": manifest["stats"]["variables"] == 780,
        "clauses_20626": manifest["stats"]["clauses"] == 20626,
    }
    result = {
        "bt": 1387,
        "title": "S3 MaxSAT external-solver harness",
        "verified": all(checks.values()),
        "checks": checks,
        "wcnf": manifest["stats"],
        "bt1373_witness_score_recomputed": score,
        "available_solver_candidates": available,
        "solver_run": solver_run,
        "optimality_status": "unresolved" if solver_run is None else "solver_output_captured_requires_parse",
        "recommended_commands": [
            "python tools/bt1384_export_s3_gauge_maxsat.py",
            "open-wbo data/generated/bt1384_s3_gauge_maxsat.wcnf",
            "maxhs data/generated/bt1384_s3_gauge_maxsat.wcnf"
        ],
        "boundary": "This is the solver-facing harness. It regenerates the exact WCNF and verifies the 210 witness. A global optimality claim requires importing and checking a real MaxSAT/ILP certificate."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1387, "verified": result["verified"], "optimality_status": result["optimality_status"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
