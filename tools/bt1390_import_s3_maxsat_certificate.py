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


def default_certificate() -> dict:
    return {
        "format": "bt1390.s3_maxsat_certificate.v1",
        "certificate_type": "witness",
        "claimed_score": 210,
        "labels": list(IMPROVED_GAUGE_LABELS),
        "optimal": False,
        "upper_bound": None,
        "source": "BT1373 witness imported as baseline certificate"
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1390_s3_maxsat_certificate_import.json")
    ns = ap.parse_args()

    cert = load(ns.certificate) if ns.certificate else default_certificate()
    labels = cert["labels"]
    computed_score = score_labels(labels)
    claimed_score = cert.get("claimed_score")
    optimal = bool(cert.get("optimal", False))
    upper_bound = cert.get("upper_bound")
    optimality_certified = bool(optimal and upper_bound == computed_score)
    checks = {
        "forty_labels": len(labels) == 40,
        "root_fixed": labels[0] == 0,
        "labels_in_s3_range": all(isinstance(x, int) and 0 <= x < len(S3_PERMS) for x in labels),
        "claimed_score_matches_computed": claimed_score == computed_score,
        "baseline_score_at_least_210": computed_score >= 210,
        "optimality_claim_requires_bound": (not optimal) or (upper_bound == computed_score),
    }
    result = {
        "bt": 1390,
        "title": "S3 MaxSAT certificate importer",
        "verified": all(checks.values()),
        "checks": checks,
        "certificate_type": cert.get("certificate_type", "unknown"),
        "computed_score": computed_score,
        "claimed_score": claimed_score,
        "optimality_status": "optimal_certified" if optimality_certified else "witness_verified_only",
        "upper_bound": upper_bound,
        "labels": labels,
        "boundary": "A witness certificate verifies a feasible score. A global optimality certificate additionally requires an imported upper bound equal to the computed score."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1390, "verified": result["verified"], "score": computed_score, "optimality_status": result["optimality_status"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
