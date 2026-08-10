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


def digest_without(d: dict, key: str) -> list[str]:
    """Every digest the object minus its hash field could legitimately have.

    Two serialisation conventions are in use in this repo and BOTH are correct:
    compact separators, and indent=2 with a trailing newline.  Calibrated at
    Pass 2482 -- trying only the compact one reported six of my own certificates
    as broken when the checker was simply using the wrong serialisation.
    """
    x = {k: v for k, v in d.items() if k != key}
    compact = json.dumps(x, sort_keys=True, separators=(",", ":"))
    indented = json.dumps(x, indent=2, sort_keys=True) + "\n"
    return [
        hashlib.sha256(compact.encode()).hexdigest(),
        hashlib.sha256(indented.encode()).hexdigest(),
    ]


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
            if embedded in computed:
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


def selftest() -> int:
    """Planted faults this checker must detect, and clean files it must stay silent on.

    Added Pass 4725. This guard reports 14 problems across 4,229 certificates and had no
    self-test, so a reader could not tell whether 14 meant "14 faults" or "14 of however
    many this checker happens to notice". CLAUDE.md failure mode 7: a clean report from a
    broken checker is indistinguishable from a clean corpus -- and a NON-clean report from
    a partly-broken one is worse, because it looks like evidence of working.

    The int-key case is the Pass 2482 trap and is the one that matters: it is not a stale
    digest, it is a certificate that never could reproduce and never will.
    """
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="certtest_"))
    cases = []

    def write(name, obj, digest_key="sha256"):
        canonical = json.dumps(json.loads(json.dumps(obj)), indent=2,
                               sort_keys=True) + "\n"
        obj = dict(obj)
        obj[digest_key] = hashlib.sha256(canonical.encode()).hexdigest()
        p = tmp / name
        p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return p

    # 1. clean: digest computed the round-trip way, must NOT be flagged
    good = write("clean.json", {"result": 42, "checks": {"ok": True}})
    cases.append(("clean certificate", good, False))

    # 2. planted: digest corrupted, MUST be flagged
    bad = tmp / "stale.json"
    d = json.loads(good.read_text(encoding="utf-8"))
    d["sha256"] = "0" * 64
    bad.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    cases.append(("stale digest", bad, True))

    # 3. planted: a false entry in checks, MUST be flagged
    fc = tmp / "falsecheck.json"
    d2 = json.loads(good.read_text(encoding="utf-8"))
    d2["checks"] = {"ok": True, "the_one_that_matters": False}
    fc.write_text(json.dumps(d2, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    cases.append(("false check", fc, True))

    # 4. planted: the Pass 2482 integer-key trap -- hashed live with int keys, so the
    #    digest can never be reproduced from the bytes on disk
    live = {"hist": {i: i * i for i in range(1, 12)}, "note": "int keys"}
    wrong = json.dumps(live, indent=2, sort_keys=True) + "\n"   # ints sort numerically
    live_out = dict(live)
    live_out["sha256"] = hashlib.sha256(wrong.encode()).hexdigest()
    ik = tmp / "intkeys.json"
    ik.write_text(json.dumps(live_out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    cases.append(("integer-key trap (Pass 2482)", ik, True))

    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, path, want in cases:
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sweep([path], quiet=True)
        got = "MISMATCH" in buf.getvalue() or "FALSE CHECK" in buf.getvalue()
        good_case = got == want
        ok &= good_case
        print(f"    {name:32s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good_case else 'FAIL'}")

    print("""
  The clean case and the stale case are byte-identical apart from the digest, so a checker
  that flagged both would be reporting on the presence of a digest field rather than on its
  correctness. The integer-key case is the one worth having: it is indistinguishable from a
  stale digest in the report, and the fix is completely different -- re-running the producer
  repairs a stale digest and cannot repair this one.

  ITS LIMIT: recall is measured against the four fault shapes above. A certificate that is
  wrong in some other way -- right digest over wrong content -- passes every one of them.""")
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
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
