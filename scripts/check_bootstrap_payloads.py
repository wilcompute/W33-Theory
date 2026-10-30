"""Verify every chunk-encoded payload in bootstrap/*/manifest.json against its recorded hashes (2026-10-30).

Several remote batches committed Python verifiers and certificates as zlib+base64 chunks with a manifest of sha256 hashes.  Some uploads
were truncated (e.g. bootstrap/pass3388_3399: 13,559 base64 characters, not a multiple of 4), which made the loader stubs raise
binascii.Error at IMPORT time -- and an import-time error in one test module aborted the whole CI pytest run at collection.

    py -3 scripts/check_bootstrap_payloads.py          # report every payload: OK / ENCODED-HASH MISMATCH / DECODE ERROR
    py -3 scripts/check_bootstrap_payloads.py --json   # machine-readable; exit status 1 if anything is broken
"""
import base64
import hashlib
import json
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def encoded(meta):
    if "encoded_parts" in meta:
        return "".join((ROOT / p).read_text(encoding="ascii") for p in meta["encoded_parts"])
    return (ROOT / meta["encoded_path"]).read_text(encoding="ascii")


def check(meta):
    try:
        enc = encoded(meta)
    except OSError as e:
        return "MISSING CHUNK", str(e)
    if meta.get("encoded_sha256") and hashlib.sha256(enc.encode()).hexdigest() != meta["encoded_sha256"]:
        return "ENCODED-HASH MISMATCH", f"{len(enc)} chars (mod 4 = {len(enc) % 4})"
    try:
        raw = zlib.decompress(base64.b64decode(enc))
    except Exception as e:  # noqa: BLE001 -- report every decode failure by name
        return "DECODE ERROR", repr(e)
    if meta.get("sha256") and hashlib.sha256(raw).hexdigest() != meta["sha256"]:
        return "DECODED-HASH MISMATCH", f"{len(raw)} bytes"
    return "OK", f"{len(raw)} bytes"


def payload_ok(target):
    """True if the payload that materialises `target` (repo-relative) verifies; None if no manifest mentions it."""
    for man in ROOT.glob("bootstrap/*/manifest.json"):
        m = json.loads(man.read_text(encoding="utf-8"))
        if target in m:
            return check(m[target])[0] == "OK"
    return None


def main():
    rows = []
    for man in sorted(ROOT.glob("bootstrap/*/manifest.json")):
        try:
            m = json.loads(man.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for target, meta in m.items():
            if isinstance(meta, dict) and ("encoded_parts" in meta or "encoded_path" in meta):
                st, info = check(meta)
                rows.append(dict(manifest=str(man.relative_to(ROOT)).replace("\\", "/"), target=target, status=st, info=info))
    bad = [r for r in rows if r["status"] != "OK"]
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
    else:
        print(f"{len(rows)} payloads, {len(bad)} broken")
        for r in bad:
            print(f"  {r['status']:22s} {r['target']}  ({r['manifest']}; {r['info']})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
