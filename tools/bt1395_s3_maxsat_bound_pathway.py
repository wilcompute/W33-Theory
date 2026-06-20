#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from bt1376_s3_gauge_radius3_local_optimum_certificate import build_score_tables, edge_score
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS, S3_PERMS


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def score_labels(labels: list[int]) -> int:
    tables = build_score_tables()
    edge_scores = tables["edge_scores"]
    return sum(edge_score(edge_scores, a, b, labels[a], labels[b]) for a, b in tables["edges"])


def default_witness() -> dict:
    return {
        "format": "bt1395.s3_maxsat_certificate.v1",
        "certificate_type": "witness",
        "claimed_score": 210,
        "labels": list(IMPROVED_GAUGE_LABELS),
        "upper_bound": None,
        "solver": "baseline",
        "source": "BT1373 witness"
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1395_s3_maxsat_bound_pathway.json")
    ns = ap.parse_args()
    cert = load(ns.certificate) if ns.certificate else default_witness()
    ctype = cert["certificate_type"]
    labels = cert.get("labels")
    computed_score = score_labels(labels) if labels is not None else None
    claimed_score = cert["claimed_score"]
    upper_bound = cert.get("upper_bound")
    witness_valid = labels is not None and len(labels) == 40 and labels[0] == 0 and all(isinstance(x, int) and 0 <= x < len(S3_PERMS) for x in labels) and computed_score == claimed_score
    upper_bound_valid = upper_bound is not None and int(upper_bound) >= 0 and int(upper_bound) <= 540 and claimed_score <= int(upper_bound)
    optimality_certified = ctype == "optimality" and witness_valid and upper_bound_valid and computed_score == int(upper_bound)
    checks = {
        "schema_file_exists": (ROOT / "schema" / "bt1395_s3_maxsat_certificate.schema.json").exists(),
        "certificate_type_known": ctype in {"witness", "upper_bound", "optimality"},
        "witness_valid_if_labels_present": witness_valid if labels is not None else True,
        "upper_bound_valid_if_present": upper_bound_valid if upper_bound is not None else True,
        "optimality_requires_matching_bound": (ctype != "optimality") or optimality_certified,
    }
    result = {
        "bt": 1395,
        "title": "S3 MaxSAT bound-certificate pathway",
        "verified": all(checks.values()),
        "checks": checks,
        "certificate_type": ctype,
        "claimed_score": claimed_score,
        "computed_score": computed_score,
        "upper_bound": upper_bound,
        "witness_valid": witness_valid,
        "optimality_status": "optimal_certified" if optimality_certified else ("upper_bound_recorded" if upper_bound is not None else "witness_only"),
        "accepted_certificate_schema": "schema/bt1395_s3_maxsat_certificate.schema.json",
        "boundary": "This verifies the local arithmetic of a witness and/or upper-bound certificate. It does not independently derive a solver proof; that proof must be imported as the certificate source."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1395, "verified": result["verified"], "optimality_status": result["optimality_status"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
