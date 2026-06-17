#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "bt1275_strict_polar_path_recovery_certificate.json"
BATCH = ROOT / "data" / "bt1274_batch_candidate_scores_summary.json"
INDEX = ROOT / "data" / "bt1279_recovery_packet_index.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify():
    cert = load(CERT)
    batch = load(BATCH)
    index = load(INDEX)
    checks = {
        "target_is_polar_path": cert["target"] == "diam14_polar_path",
        "closure_order_51840": cert["closure"]["order"] == 51840,
        "word_diameter_14": cert["word_metric"]["diameter"] == 14,
        "edge_split_P4P4": cert["edge_geometry"]["polar_graph"] == "P4" and cert["edge_geometry"]["nonpolar_graph"] == "P4",
        "labelled_spread_172": cert["labelled_geodesic"]["channel_spread"] == 172,
        "score_vector_all_ones": cert["score_vector"]["values"] == [1, 1, 1, 1, 1],
        "validator_pass": cert["validator_result"]["band"] == "pass" and cert["validator_result"]["score"] == 5,
        "batch_counts_match": batch["band_counts"] == {"pass": 1, "review": 1, "fail": 2},
        "index_points_to_certificate": index["strict_certificate"] == "data/bt1275_strict_polar_path_recovery_certificate.json",
        "index_target_matches": index["strict_target"] == cert["target"],
    }
    return {
        "bt": 1281,
        "title": "Strict recovery certificate verifier",
        "verified": all(checks.values()),
        "checks": checks,
        "certificate": str(CERT.relative_to(ROOT)),
        "batch_summary": str(BATCH.relative_to(ROOT)),
        "packet_index": str(INDEX.relative_to(ROOT)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1281_recovery_certificate_verification_summary.json")
    ns = ap.parse_args()
    result = verify()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt":1281, "verified":result["verified"], "out":str(ns.out)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
