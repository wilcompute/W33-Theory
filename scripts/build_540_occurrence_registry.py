#!/usr/bin/env python3
"""Build a deterministic registry for explicitly selected 540-bearing files.

The registry never guesses an unresolved identity.  It records the checked-in
classifier result together with a whole-file hash and per-occurrence snippet
hash, and refuses output when any selected occurrence remains ambiguous.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.tag_540_disambiguation import audit_file


def _relative_file(root: Path, argument: str) -> tuple[Path, str]:
    path = Path(argument)
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(f"selected file lies outside registry root: {path}") from exc
    if not resolved.is_file():
        raise FileNotFoundError(f"selected registry file does not exist: {relative}")
    return resolved, relative


def _occurrence_record(ordinal: int, occurrence: dict[str, Any]) -> dict[str, Any]:
    snippet = occurrence["snippet"].encode("utf-8")
    return {
        "ordinal": ordinal,
        "line": occurrence["line"],
        "category": occurrence["category"],
        "reason": occurrence["reason"],
        "explicit_tags": occurrence["explicit_tags"],
        "snippet_sha256": hashlib.sha256(snippet).hexdigest(),
    }


def build_registry(root: Path, filenames: list[str]) -> dict[str, Any]:
    """Classify and hash only ``filenames``, in canonical path order."""

    root = root.resolve()
    selected = sorted(
        {_relative_file(root, filename) for filename in filenames},
        key=lambda pair: pair[1],
    )
    records: list[dict[str, Any]] = []
    ambiguous = 0
    total = 0
    for path, relative in selected:
        classification = audit_file(path, root)
        occurrences = [] if classification is None else classification["occurrences"]
        normalized = [
            _occurrence_record(index, occurrence)
            for index, occurrence in enumerate(occurrences)
        ]
        ambiguous_here = sum(
            occurrence["category"] == "ambiguous"
            for occurrence in normalized
        )
        ambiguous += ambiguous_here
        total += len(normalized)
        records.append(
            {
                "path": relative,
                "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "category": (
                    "none" if classification is None else classification["category"]
                ),
                "occurrence_count": len(normalized),
                "ambiguous_occurrences": ambiguous_here,
                "occurrences": normalized,
            }
        )

    return {
        "schema": "w33.540_explicit_file_registry.v1",
        "status": "PASS" if ambiguous == 0 else "NEEDS_TAGGING",
        "selection_mode": "explicit_files_only",
        "selected_file_count": len(records),
        "literal_occurrences": total,
        "ambiguous_occurrences": ambiguous,
        "records": records,
    }


def canonical_bytes(registry: dict[str, Any]) -> bytes:
    return (json.dumps(registry, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="explicit files relative to --root")
    parser.add_argument("--root", type=Path, default=ROOT)
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "--write",
        type=Path,
        help="explicitly write a new registry; stdout is the default",
    )
    output.add_argument(
        "--check",
        type=Path,
        help="compare with an existing registry without writing",
    )
    args = parser.parse_args()

    registry = build_registry(args.root, args.files)
    payload = canonical_bytes(registry)
    if registry["status"] != "PASS":
        sys.stdout.buffer.write(payload)
        raise SystemExit(
            f"{registry['ambiguous_occurrences']} selected 540 occurrence(s) "
            "still need an explicit identity tag"
        )

    if args.check is not None:
        if not args.check.is_file() or args.check.read_bytes() != payload:
            raise SystemExit(f"540 registry drift: {args.check}")
        print(f"PASS: {args.check} matches {len(registry['records'])} selected files")
    elif args.write is not None:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_bytes(payload)
        print(f"PASS: wrote {args.write}")
    else:
        sys.stdout.buffer.write(payload)


if __name__ == "__main__":
    main()
