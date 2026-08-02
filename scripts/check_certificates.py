#!/usr/bin/env python3
"""Verify that every frozen certificate in data/ reproduces its own digest.

Added at Pass 2478.  This started as a hand-run sweep and caught a real defect:
the parallel track's Pass 2304 certificate carried a stale embedded hash after a
later correction changed the object, so its own verifier failed before any theorem
check ran.  A sweep that finds that costs milliseconds; a sweep nobody runs finds
it after merge.

It also scans frozen `checks` blocks for any `false`, because six separate times in
this repo a question was recorded as "open" while its answer sat in a committed
certificate with a passing check.

WARNS, never blocks -- same policy as scripts/check_rediscovery.py.  A blocking hook
trains `--no-verify`, and a stale hash is a candidate for review, not proof of error:
a certificate may legitimately have no hash field, or hash a subset of its keys.

Usage:
    py -3 scripts/check_certificates.py                 # sweep all of data/
    py -3 scripts/check_certificates.py <files...>      # sweep only these
    py -3 scripts/check_certificates.py --quiet         # only report problems
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest_without(d: dict, key: str) -> str:
    """The repo's canonical digest: the object minus its own hash field."""
    x = {k: v for k, v in d.items() if k != key}
    return hashlib.sha256(
        json.dumps(x, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


# Calibrated at Pass 2478 by measuring every sha256-named key across all of data/.
# Matching on "sha256" anywhere in the key name flags 145 of 289 files -- a 50%
# false-positive rate, pure noise, and exactly the mistake check_rediscovery.py was
# calibrated away from.  The reason: most sha256-named keys hash an INPUT, not the
# certificate.  Measured verify/mismatch counts per key name:
#
#     sha256_without_hash_field   91 /  6      canonical, keep
#     sha256                      33 /  1      canonical, keep
#     universe_sha256              1 /  0      canonical, keep
#     certificate_sha256          27 / 84      different convention, EXCLUDE
#     genome_/matrix_/tensor_/...  0 / many    hashes of inputs, EXCLUDE
#
# Restricting to the three canonical names gives a ~5% flag rate, which is
# actionable rather than noise.
SELF_DIGEST_KEYS = ("sha256_without_hash_field", "sha256", "universe_sha256")


def hash_key(d: dict) -> str | None:
    """The key holding this object's OWN digest, or None.

    A usable field is one of the canonical names above holding a 64-char hex string.
    """
    for k in SELF_DIGEST_KEYS:
        v = d.get(k)
        if isinstance(v, str) and len(v) == 64:
            try:
                int(v, 16)
            except ValueError:
                continue
            return k
    return None


def sweep(paths: list[Path], quiet: bool = False) -> int:
    hashed = verified = nohash = unreadable = 0
    problems: list[str] = []

    for p in sorted(paths):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report, never raise
            unreadable += 1
            problems.append(f"  UNREADABLE  {p.name}: {str(exc)[:60]}")
            continue
        if not isinstance(d, dict):
            continue

        key = hash_key(d)
        if key is None:
            nohash += 1
        else:
            hashed += 1
            embedded, computed = d[key], digest_without(d, key)
            if embedded == computed:
                verified += 1
            else:
                problems.append(
                    f"  HASH MISMATCH  {p.name}\n"
                    f"      embedded {embedded[:16]}...\n"
                    f"      computed {computed[:16]}..."
                )

        checks = d.get("checks")
        if isinstance(checks, dict):
            failed = [k for k, v in checks.items() if v is False]
            if failed:
                problems.append(
                    f"  FALSE CHECK    {p.name}: {', '.join(failed[:4])}"
                )

    if not quiet:
        print(f"certificates scanned : {hashed + nohash}")
        print(f"  with an embedded hash : {hashed}   verified {verified}")
        print(f"  with no hash field    : {nohash}")
        if unreadable:
            print(f"  unreadable            : {unreadable}")

    if problems:
        print(f"\ncheck_certificates: {len(problems)} problem(s) - review, not a block:")
        for line in problems:
            print(line)
    elif not quiet:
        print("all frozen certificates reproduce their digests; no false checks.")

    return 0  # never blocks


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    args = [a for a in argv if not a.startswith("--")]
    if args:
        paths = [Path(a) for a in args if a.endswith(".json")]
    else:
        paths = list((ROOT / "data").glob("*.json"))
    if not paths:
        return 0
    return sweep(paths, quiet=quiet)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
