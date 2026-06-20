#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1383_runtime_frontier_integration.json")
    ns = ap.parse_args()
    solver = load("data/bt1381_s3_gauge_global_solver_probe.json")
    port = load("data/bt1382_non_clifford_port_abi.json")
    checks = {
        "solver_probe_verified": solver["verified"] is True,
        "solver_best_score_210": solver["solver"]["best_score"] == 210,
        "port_abi_verified": port["verified"] is True,
        "port_has_two_options": len(port["ports"]) == 2,
        "tex_insert_exists": exists("tex/bt1381_bt1383_runtime_frontier_insert.tex"),
        "claim_master_exists": exists("paper/w33_q4_claim_stratified_master.tex"),
        "post_1377_table_exists": exists("tex/bt1380_post_1377_claim_table.tex"),
    }
    result = {
        "bt": 1383,
        "title": "Runtime frontier paper/release integration verifier",
        "verified": all(checks.values()),
        "checks": checks,
        "paper_inserts": [
            "tex/bt1380_post_1377_claim_table.tex",
            "tex/bt1381_bt1383_runtime_frontier_insert.tex"
        ],
        "release_frontier_artifacts": [
            "data/bt1378_runtime_contract_verification.json",
            "data/bt1379_s3_gauge_max2csp_spec.json",
            "data/bt1381_s3_gauge_global_solver_probe.json",
            "data/bt1382_non_clifford_port_abi.json"
        ],
        "reading": "The claim-stratified master paper can now absorb the runtime contract, S3 optimization frontier, and non-Clifford port ABI without changing claim classes."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1383, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
