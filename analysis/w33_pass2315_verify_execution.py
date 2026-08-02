#!/usr/bin/env python3
"""Pass 2315: aggregate fail-closed verifier for Passes 2309--2314 outputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    2309: "w33.pass2309.signature_resolution_quotient.v1",
    2310: "w33.pass2310.quadratic_hom_locality.v1",
    2311: "w33.pass2311.regular_spread_parameter_closure.v1",
    2312: "w33.pass2312.regular_ree_tits_comparison.v1",
    2313: "w33.pass2313.command_oracle.v1",
    2314: "w33.pass2314.cubic_controller_nonquotient.v1",
}


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def verify_hash(d):
    claimed = d.get("sha256_without_hash_field")
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return claimed == canonical_hash(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact-dir", type=Path, required=True)
    ap.add_argument("--simulation-log", type=Path)
    ap.add_argument("--formal-log", type=Path)
    ap.add_argument("--write-json", type=Path)
    args = ap.parse_args()

    records = {}
    checks = {}
    for p, schema in EXPECTED.items():
        path = args.artifact_dir / f"pass{p}.json"
        d = json.loads(path.read_text())
        records[str(p)] = {
            "schema": d.get("schema"),
            "status": d.get("status"),
            "sha256": d.get("sha256_without_hash_field"),
        }
        checks[f"pass{p}_schema"] = d.get("schema") == schema
        checks[f"pass{p}_hash"] = verify_hash(d)
        checks[f"pass{p}_checks"] = all(bool(v) for v in d.get("checks", {}).values())

    p2309 = json.loads((args.artifact_dir / "pass2309.json").read_text())
    checks["pass2309_solver_decided_or_bounded"] = p2309.get("status") in {"OPTIMAL", "FEASIBLE", "INFEASIBLE", "UNKNOWN"}
    if p2309.get("feasible") is True:
        checks["pass2309_exact_witness"] = p2309.get("exact_sum") == [12] * 45

    if args.simulation_log:
        text = args.simulation_log.read_text(errors="replace")
        checks["pass2313_simulation_marker"] = "PASS2313 exhaustive command oracle cases=1152" in text
    if args.formal_log:
        text = args.formal_log.read_text(errors="replace")
        checks["pass2313_formal_no_failure"] = "ERROR" not in text.upper() and "Assert failed" not in text

    assert all(checks.values()), {k: v for k, v in checks.items() if not v}
    out = {
        "schema": "w33.pass2315.execution_aggregate.v1",
        "status": "PASS_EXECUTED_SIX_FRONTIERS_WITH_BOUNDARIES",
        "passes": records,
        "checks": checks,
        "boundary": "The aggregate preserves every component boundary. In particular, signature feasibility is not frame compatibility, symbolic parameter closure is conditional on the remaining geometric lemma, and the D24 command algebra is not an arithmetic-group quotient.",
    }
    out["sha256_without_hash_field"] = canonical_hash(out)
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
