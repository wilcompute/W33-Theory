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
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1380_post_1377_bridge_index.json")
    ns = ap.parse_args()
    runtime = load("data/bt1378_runtime_contract_verification.json")
    gauge = load("data/bt1379_s3_gauge_max2csp_spec.json")
    claims = [
        {"bt": 1362, "claim_class": "CERT", "artifact": "data/bt1362_symmetric_q4_gauge_quotient.json", "role": "symmetric Q4 [[32,4,4]] quotient with C2^4:C4 clock"},
        {"bt": 1363, "claim_class": "STRUCT", "artifact": "data/bt1363_q4_clock_tomotope_medial_descent.json", "role": "Q4 clock descends to three tomotope sheets"},
        {"bt": 1368, "claim_class": "CERT", "artifact": "data/bt1368_q6_tomotope_equivariant_flag_lift.json", "role": "Q6/tomotope 192-flag equivariant lift"},
        {"bt": 1374, "claim_class": "CERT", "artifact": "data/bt1374_q6_tomotope_packet_route_compiler.json", "role": "packet route compiler to Q6 edge addresses"},
        {"bt": 1375, "claim_class": "CERT", "artifact": "data/bt1375_steinberg_cycle_operator_scheduler_lift.json", "role": "central C3 Steinberg scheduler"},
        {"bt": 1376, "claim_class": "CERT", "artifact": "data/bt1376_s3_gauge_radius3_local_optimum_certificate.json", "role": "radius-3 local optimum for S3 gauge"},
        {"bt": 1377, "claim_class": "ENG", "artifact": "data/bt1377_physical_universal_computation_contract.json", "role": "physical Clifford runtime plus non-Clifford port boundary"},
        {"bt": 1378, "claim_class": "CERT", "artifact": "data/bt1378_runtime_contract_verification.json", "role": "cross-artifact runtime contract verifier"},
        {"bt": 1379, "claim_class": "OPT", "artifact": "data/bt1379_s3_gauge_max2csp_spec.json", "role": "global S3 gauge Max-2CSP frontier"}
    ]
    checks = {
        "runtime_verified": runtime["verified"] is True,
        "gauge_spec_verified": gauge["verified"] is True,
        "all_artifacts_exist": all(exists(c["artifact"]) for c in claims),
        "non_clifford_boundary_preserved": "non-Clifford port" in runtime["honest_boundary"],
        "s3_search_space_recorded": gauge["problem"]["search_space_root_fixed"] == "6^39",
        "claim_count_9": len(claims) == 9
    }
    result = {
        "bt": 1380,
        "title": "Post-BT1377 bridge index",
        "verified": all(checks.values()),
        "checks": checks,
        "claims": claims,
        "paper_insert": "tex/bt1380_post_1377_claim_table.tex",
        "reading": "BT1362-BT1380 form the current physical-runtime spine from symmetric Q4 quotient through Q6/tomotope addressing, Steinberg scheduling, S3 synchronization, and the explicit non-Clifford universality port."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1380, "verified": result["verified"], "claim_count": len(claims)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
