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


# POINTER SEMANTICS. A registry entry uses `sha256` to name the digest of the certificate
# it REGISTERS, not its own. Such a file can never satisfy a self-digest check, and the guard
# reported 10 of them as HASH MISMATCH (Pass 4932) -- found only by aiming it at another
# lane's files, since this lane writes no registry entries.
#
# This is the second false-positive family in this checker from the same assumption: that a
# key NAME implies a convention. Pass 4801 found the first, where the presence of numeric
# keys was read as evidence the producer used integer keys.
POINTER_MARKERS = ("certificate", "registers", "target", "points_to", "artifact_path")


def is_pointer_entry(d: dict) -> bool:
    """True when the digest field names ANOTHER object's digest, not this file's."""
    for k in POINTER_MARKERS:
        v = d.get(k)
        if isinstance(v, str) and v.endswith(".json"):
            return True
    return False


def hash_key(d: dict) -> str | None:
    """The key holding this object's OWN digest, or None.

    A usable field is one of the canonical names above holding a 64-char hex string, in a
    file that is not a pointer entry.
    """
    if is_pointer_entry(d):
        return None
    for k in SELF_DIGEST_KEYS:
        v = d.get(k)
        if isinstance(v, str) and len(v) == 64:
            try:
                int(v, 16)
            except ValueError:
                continue
            return k
    return None


def stale_pointers(paths: list[Path]) -> list[dict]:
    """Registry entries whose recorded digest cannot be reconciled with their target.

    Two outcomes, and they are not the same finding:

      STALE         the target HAS a self-digest and it differs from what was recorded.
      UNVERIFIABLE  the target has NO self-digest, and the recorded value matches none of
                    raw bytes / compact JSON / indent=2 JSON. The convention is unknown,
                    not violated.

    The first version of this function called both STALE. It could not: for 5 of the 10
    registry entries the target carries no digest at all, so there is nothing to be stale
    against. Asserting a convention from a key name is what produced this checker's other
    two false-positive families (Passes 4801, 4932) and it nearly produced a third here.
    """
    out = []
    for p in sorted(paths):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict) or not is_pointer_entry(d):
            continue
        # The registry schema uses "sha256"; read it through the canonical list
        # anyway, so a registry variant under another name is not silently skipped.
        recorded = next((d[k] for k in SELF_DIGEST_KEYS
                         if isinstance(d.get(k), str)), None)
        target = d.get("certificate")
        if not (isinstance(recorded, str) and isinstance(target, str)):
            continue
        tp = ROOT / target
        if not tp.is_file():
            out.append({"registry": p.name, "target": target, "status": "target missing"})
            continue
        try:
            td = json.loads(tp.read_text(encoding="utf-8"))
        except Exception:
            out.append({"registry": p.name, "target": target,
                        "status": "target unreadable"})
            continue
        # DO NOT SAY "STALE" WITHOUT KNOWING THE CONVENTION. The first version of this
        # function compared the registry's digest against the target's own sha256 field and
        # labelled every mismatch STALE. For 5 of the 10 the target has NO sha256 field at
        # all, and the recorded value matches none of raw bytes, compact JSON, or indent=2
        # JSON of the target. So the convention is unknown, not violated -- and asserting a
        # convention from a key name is the exact mistake that produced this checker's other
        # two false-positive families (Passes 4801 and 4932).
        # THE TARGET'S SELF-DIGEST MAY BE UNDER ANY OF THE CANONICAL NAMES. Looking only
        # for "sha256" reported 5 entries as unverifiable when the target used
        # "sha256_without_hash_field" -- the FOURTH time in this checker that a key name
        # was assumed rather than looked up (Passes 4801, 4932, 4933, and here).
        actual = None
        if isinstance(td, dict):
            for k in SELF_DIGEST_KEYS:
                if isinstance(td.get(k), str):
                    actual = td[k]
                    break
        if actual is None:
            candidates = {
                "raw": hashlib.sha256(tp.read_bytes()).hexdigest(),
                "compact": hashlib.sha256(json.dumps(
                    td, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                "indent2": hashlib.sha256((json.dumps(
                    td, indent=2, sort_keys=True) + "\n").encode()).hexdigest(),
            }
            hit = next((k for k, v in candidates.items() if v == recorded), None)
            out.append({"registry": p.name, "target": target,
                        "status": "verified" if hit else "UNVERIFIABLE",
                        "matched_serialisation": hit,
                        "recorded": recorded[:16], "actual": "no self-digest field"})
        elif actual != recorded:
            out.append({"registry": p.name, "target": target, "status": "STALE",
                        "recorded": recorded[:16], "actual": actual[:16]})
    return [o for o in out if o["status"] != "verified"]


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

    # 5. a POINTER entry: sha256 names ANOTHER file's digest, not its own. Pass 4932
    #    found 10 of these reported as HASH MISMATCH, because the checker read the key
    #    name as implying self-digest semantics.
    ptr = tmp / "registry_entry.json"
    ptr.write_text(json.dumps(
        {"pass": 1856, "certificate": "data/whatever.json", "owner": "track-b",
         "sha256": "a" * 64}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    cases.append(("registry pointer entry", ptr, False))

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

  THE POINTER CASE IS THE ONE THAT TOOK TWO PASSES TO FIND. A registry entry carries a
  sha256 that names the certificate it registers. Nothing distinguishes it from a
  self-digest except the presence of a `certificate` field, and this lane writes no
  registry entries -- so it took aiming the guard at another lane's files to surface.

  ITS LIMIT: recall is measured against the five fault shapes above. A certificate that is
  wrong in some other way -- right digest over wrong content -- passes every one of them.""")
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--pointers" in argv:
        reg = sorted((ROOT / "data").rglob("*.json"))
        bad = stale_pointers(reg)
        for b in bad:
            print(f"  {b['status']:16s} {b['registry']} -> {b['target']}")
            if b.get("recorded"):
                print(f"      recorded {b['recorded']}...  actual {b['actual']}...")
        print(f"\n  {len(bad)} registry pointer(s) that cannot be reconciled")
        return 0
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
