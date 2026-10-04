#!/usr/bin/env python3
"""Aggregate the 495 duplicate-free Pass-2977 shard artifacts fail-closed."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

EXPECTED_SHARDS = 495
EXPECTED_TOTAL = 213_648_435
COUNT_KEYS = (
    "subspaces_examined",
    "distinct_general_subspaces_examined",
    "rank4_isotropic_subspaces_in_shard",
    "isotropic_subspaces",
    "examined",
    "count",
)
CANDIDATE_KEYS = ("candidate_rows", "candidates", "hits", "collinearity_projectors")


def walk_for_count(value: Any) -> int | None:
    if isinstance(value, dict):
        for key in COUNT_KEYS:
            candidate = value.get(key)
            if isinstance(candidate, int) and candidate >= 0:
                return candidate
        for child in value.values():
            found = walk_for_count(child)
            if found is not None:
                return found
    return None


def walk_for_candidates(value: Any) -> list[Any]:
    if isinstance(value, dict):
        for key in CANDIDATE_KEYS:
            candidate = value.get(key)
            if isinstance(candidate, list):
                return candidate
        for child in value.values():
            found = walk_for_candidates(child)
            if found:
                return found
    return []


def parse_log(path: Path) -> int | None:
    text = path.read_text(errors="replace")
    patterns = (
        r"(?:subspaces_examined|examined|subspaces|count)\s*[=:]\s*(\d+)",
        r"PASS[^\n]*?\b(\d+)\s+(?:subspaces|isotropic)",
    )
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            return int(matches[-1])
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    all_candidates: list[dict[str, Any]] = []
    missing = []
    unparsed = []

    for index in range(EXPECTED_SHARDS):
        json_paths = sorted(args.root.rglob(f"shard_{index}.json"))
        log_paths = sorted(args.root.rglob(f"shard_{index}.log"))
        count = None
        source = None
        candidates: list[Any] = []
        if json_paths:
            source = json_paths[0]
            payload = json.loads(source.read_text())
            count = walk_for_count(payload)
            candidates = walk_for_candidates(payload)
        elif log_paths:
            source = log_paths[0]
            count = parse_log(source)
        else:
            missing.append(index)
            continue

        if count is None:
            unparsed.append(index)
            continue
        for candidate in candidates:
            if isinstance(candidate, dict):
                all_candidates.append({"pivot_index": index, **candidate})
            else:
                all_candidates.append({"pivot_index": index, "candidate": candidate})
        rows.append(
            {
                "pivot_index": index,
                "subspaces_examined": count,
                "candidate_count": len(candidates),
                "source": str(source.relative_to(args.root)),
            }
        )

    total = sum(row["subspaces_examined"] for row in rows)
    complete = (
        len(rows) == EXPECTED_SHARDS
        and not missing
        and not unparsed
        and total == EXPECTED_TOTAL
    )
    result = {
        "schema": "w33.pass2977.general_isotropic_m36_full.v1",
        "status": "COMPLETE_EXHAUSTIVE" if complete else "INCOMPLETE_FAIL_CLOSED",
        "expected_shards": EXPECTED_SHARDS,
        "parsed_shards": len(rows),
        "missing_shards": missing,
        "unparsed_shards": unparsed,
        "expected_subspaces": EXPECTED_TOTAL,
        "examined_subspaces": total,
        "candidate_count": len(all_candidates),
        "candidate_rows": all_candidates,
        "shard_rows": rows,
        "claim_boundary": (
            "Complete only when all 495 duplicate-free RREF pivot shards parse and "
            "their examined counts sum exactly to 213648435."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "parsed_shards", "examined_subspaces", "candidate_count"
    )}, sort_keys=True))
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
