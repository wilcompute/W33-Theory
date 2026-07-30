#!/usr/bin/env python3
"""Read-only quarantine audit for the corrupted Pass 1142-1146 bundle.

The historical transport file was truncated by a literal ellipsization marker.
It is retained only as fingerprinted evidence.  No source member is decoded,
compiled, imported, or otherwise executed from this file.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
from pathlib import Path
from typing import Any, MutableMapping


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "pass1142_1146_source_bundle.b64"
ELLIPSIZATION_MARKER = b"[... ELLIPSIZATION ...]"
KNOWN_CORRUPT = {
    "byte_size": 20023,
    "length_mod_4": 3,
    "sha256": "ea2c81f514a38ca8f4ac7a2b4e1c5d6e7af05539721ffc2ae75f8a79ad610897",
    "ellipsization_offset": 10000,
}


class BundleQuarantinedError(RuntimeError):
    """Raised whenever legacy code asks to execute a quarantined member."""


def inspect_bundle(path: Path = BUNDLE) -> dict[str, Any]:
    """Return a deterministic integrity report without opening an archive."""

    if not path.is_file():
        return {
            "schema": "w33.pass1142_1146.bundle_quarantine.v1",
            "status": "MISSING",
            "path": path.as_posix(),
            "source_execution_enabled": False,
            "known_corrupt_match": False,
        }

    payload = path.read_bytes()
    strict_error: str | None = None
    try:
        base64.b64decode(payload, validate=True)
        strict_base64_valid = True
    except (binascii.Error, ValueError) as exc:
        strict_base64_valid = False
        strict_error = f"{type(exc).__name__}: {exc}"

    observed = {
        "byte_size": len(payload),
        "length_mod_4": len(payload) % 4,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "ellipsization_offset": payload.find(ELLIPSIZATION_MARKER),
    }
    known_corrupt_match = observed == KNOWN_CORRUPT and not strict_base64_valid
    return {
        "schema": "w33.pass1142_1146.bundle_quarantine.v1",
        "status": (
            "KNOWN_CORRUPT_QUARANTINED"
            if known_corrupt_match
            else "UNEXPECTED_BUNDLE_STATE"
        ),
        "path": path.as_posix(),
        "observed": observed,
        "expected_known_corrupt": KNOWN_CORRUPT,
        "strict_base64_valid": strict_base64_valid,
        "strict_base64_error": strict_error,
        "source_execution_enabled": False,
        "known_corrupt_match": known_corrupt_match,
    }


def execute_member(
    member: str,
    namespace: MutableMapping[str, Any] | None = None,
) -> None:
    """Fail closed for callers left over from the historical transport."""

    del namespace
    raise BundleQuarantinedError(
        f"Pass 1142-1146 source member {member!r} is quarantined; "
        "use the checked-in transparent source instead"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assert-known-corrupt",
        action="store_true",
        help="exit successfully only when the retained blob matches its quarantine fingerprint",
    )
    parser.add_argument("--bundle", type=Path, default=BUNDLE)
    args = parser.parse_args()

    report = inspect_bundle(args.bundle)
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.assert_known_corrupt and report["known_corrupt_match"]:
        return
    raise SystemExit(
        "The Pass 1142-1146 bundle is quarantined and cannot execute source"
    )


if __name__ == "__main__":
    main()
