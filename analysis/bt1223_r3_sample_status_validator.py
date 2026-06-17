#!/usr/bin/env python3
"""BT1223 -- R3 sample status validator.

Classifies K3/R3 sample artifacts as blocked, partial, or candidate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

BLOCKING_WORDS = ("mock", "placeholder", "not_computed", "stub")


def has_blocking_label(value) -> bool:
    if isinstance(value, str):
        return any(word in value for word in BLOCKING_WORDS)
    if isinstance(value, dict):
        return any(has_blocking_label(v) for v in value.values())
    if isinstance(value, list):
        return any(has_blocking_label(v) for v in value)
    return False


def classify_sample(sample: dict) -> dict:
    issues = []
    if has_blocking_label(sample.get("metric_block", {})):
        issues.append("metric_block_has_nonphysical_label")
    if has_blocking_label(sample.get("operator_block", {})):
        issues.append("operator_block_has_nonphysical_label")
    if not sample.get("operator_block", {}).get("eigenvalue_sample"):
        issues.append("missing_operator_sample")
    if sample.get("refinement_block", {}).get("h") is None:
        issues.append("missing_refinement_h")
    if sample.get("heat_block", {}).get("A4", {}).get("value") is None:
        issues.append("missing_A4")
    status = sample.get("claim_status", "unknown")
    if has_blocking_label(status):
        issues.append("claim_status_blocks_candidate")

    if issues:
        level = "blocked"
    elif status == "partial_computed_candidate":
        level = "partial"
    else:
        level = "candidate"
    return {
        "sample_id": sample.get("sample_id", "unknown"),
        "level": level,
        "candidate_allowed": level == "candidate",
        "issues": issues,
    }


def validate_sequence(seq: dict) -> dict:
    samples = seq.get("samples") or []
    rows = [classify_sample(s) for s in samples]
    counts = {"blocked": 0, "partial": 0, "candidate": 0}
    for row in rows:
        counts[row["level"]] += 1
    return {
        "bt": 1223,
        "title": "R3 sample status validator",
        "source_title": seq.get("title"),
        "classifications": rows,
        "counts": counts,
        "candidate_allowed": counts["candidate"] > 0 and counts["blocked"] == 0,
        "rule": "A candidate must have no blocking labels, nonempty operator data, non-null refinement h, non-null A4, and a non-blocking claim status.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/bt1220_r3_schema_valid_mock_sequence.json"))
    parser.add_argument("--out", type=Path, default=Path("data/bt1223_r3_sample_status_validator.json"))
    args = parser.parse_args()
    seq = json.loads(args.input.read_text())
    result = validate_sequence(seq)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1223, "counts": result["counts"], "candidate_allowed": result["candidate_allowed"]}, indent=2))


if __name__ == "__main__":
    main()
