#!/usr/bin/env python3
"""BT1227 -- combined blocked/partial R3 validator.

Validates both the BT1220 blocked mock sequence and the BT1226 partial fixture.
The expected combined counts are blocked=4, partial=1, candidate=0.
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
        issues.append("metric_block_has_blocking_label")
    if has_blocking_label(sample.get("operator_block", {})):
        issues.append("operator_block_has_blocking_label")
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
    return {"sample_id": sample.get("sample_id", "unknown"), "level": level, "issues": issues}


def load_samples(mock_sequence_path: Path, partial_fixture_path: Path) -> list[dict]:
    mock_sequence = json.loads(mock_sequence_path.read_text())
    partial_fixture = json.loads(partial_fixture_path.read_text())
    samples = list(mock_sequence.get("samples", []))
    samples.append(partial_fixture["sample"])
    return samples


def validate(mock_sequence_path: Path, partial_fixture_path: Path) -> dict:
    samples = load_samples(mock_sequence_path, partial_fixture_path)
    rows = [classify_sample(s) for s in samples]
    counts = {"blocked": 0, "partial": 0, "candidate": 0}
    for row in rows:
        counts[row["level"]] += 1
    expected = {"blocked": 4, "partial": 1, "candidate": 0}
    return {
        "bt": 1227,
        "title": "Combined R3 blocked/partial validator",
        "sources": [str(mock_sequence_path), str(partial_fixture_path)],
        "classifications": rows,
        "counts": counts,
        "expected_counts": expected,
        "counts_match_expected": counts == expected,
        "candidate_allowed": counts["candidate"] > 0 and counts["blocked"] == 0,
        "interpretation": "The R3 pipeline now exercises blocked and partial lanes together while still refusing candidate promotion.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock-sequence", type=Path, default=Path("data/bt1220_r3_schema_valid_mock_sequence.json"))
    parser.add_argument("--partial-fixture", type=Path, default=Path("data/bt1226_r3_partial_sample_fixture.json"))
    parser.add_argument("--out", type=Path, default=Path("data/bt1227_r3_blocked_partial_combined_validator.json"))
    args = parser.parse_args()
    result = validate(args.mock_sequence, args.partial_fixture)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1227, "counts": result["counts"], "ok": result["counts_match_expected"]}, indent=2))


if __name__ == "__main__":
    main()
