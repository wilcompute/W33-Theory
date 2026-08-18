#!/usr/bin/env python3
"""Batch intake auditor -- runs the .continuity/INSTRUCTIONS.md intake protocol
as one command, so auditing a remote batch is self-service instead of ad hoc.

Born from two intakes done by hand: the July 15 batch's unsupported [[137,1,3]]
(refuted after merge; should have been caught before) and the Pass-399/415-429
stream (audited manually in Pass 430). The protocol exists; this makes it
executable.

WHAT IT RUNS, per batch file or extracted archive directory:
  1. RESULTS_INDEX refresh + rediscovery guard over the batch files
     (collisions name the prior art to read first).
  2. Certificate triage: every batch data/*.json is classified as
     witness (status PASS/FAIL), release-engineering artifact
     (attestation/manifest vocabularies -- exempt), or UNKNOWN vocabulary
     (flagged: new status words have twice confused the ledger checker).
  3. Contradiction scan: batch claims of code parameters [[n,k,d]] are
     checked against certified values already in data/ -- a batch that
     contradicts a certificate must name the certificate it supersedes
     (the [[137,1,3]] rule).
  4. Ledger dry-run: if the batch touches w33_paper.tex, the claims-ledger
     checker runs against the batch's version.
  5. Optional archive verification: --archive PATH --sha256 HEX --size N
     verifies the transport contract (SHA-256 + decoded byte count) BEFORE
     any extraction, per the hash-locked transport convention.

Advisory by design, like the guard: it prints findings and exits nonzero only
on hard failures (archive mismatch, certificate contradiction), never on
collisions alone.

Usage:
  py -3 scripts/audit_batch.py <files-or-dirs...>
  py -3 scripts/audit_batch.py --archive x.tar.gz --sha256 <hex> --size <bytes>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RE_CSS = re.compile(r"\[\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]\]")
WITNESS_STATUSES = {"PASS", "FAIL"}
RELEASE_MARKERS = ("attestation", "release_manifest", "transport")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def certified_css_params() -> dict[tuple[int, int], set[int]]:
    """(n,k) -> distances certified anywhere in data/*.json (witness files)."""
    out: dict[tuple[int, int], set[int]] = {}
    for p in (ROOT / "data").glob("*.json"):
        if any(m in p.name for m in RELEASE_MARKERS):
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if '"status": "PASS"' not in txt and '"status":"PASS"' not in txt:
            continue
        for n, k, d in RE_CSS.findall(txt):
            out.setdefault((int(n), int(k)), set()).add(int(d))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--archive")
    ap.add_argument("--sha256")
    ap.add_argument("--size", type=int)
    args = ap.parse_args()
    hard_fail = False

    # 5. archive contract first -- never extract unverified transport
    if args.archive:
        p = Path(args.archive)
        if not p.exists():
            print(f"[audit] HARD FAIL: archive {p} not found")
            return 1
        got = sha256_file(p)
        ok_sha = (args.sha256 or "").lower() == got
        ok_size = args.size is None or p.stat().st_size == args.size
        print(f"[audit] archive sha256 {'OK' if ok_sha else 'MISMATCH'}: {got}")
        if args.size is not None:
            print(f"[audit] archive size {'OK' if ok_size else 'MISMATCH'}: "
                  f"{p.stat().st_size}")
        if not (ok_sha and ok_size):
            print("[audit] HARD FAIL: transport contract violated -- "
                  "do not extract")
            return 1

    files: list[Path] = []
    for a in args.paths:
        q = Path(a)
        files += sorted(q.rglob("*")) if q.is_dir() else [q]
    files = [f for f in files if f.is_file()]
    if not files:
        print("[audit] no batch files given")
        return 0

    # 1. guard
    subprocess.run([sys.executable, str(ROOT / "analysis" / "build_results_index.py")],
                   capture_output=True)
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_rediscovery.py")]
                       + [str(f) for f in files], capture_output=True, text=True)
    print(r.stdout or "[audit] guard: no collisions")

    # 1b. forced arithmetic (Pass 6160). The Aug 18 batch passed this harness clean
    # while claiming W(3,3)'s SRG multiplicities "encode Monster moonshine"; they are
    # determined by (v,k,lambda,mu). Rediscovery and vocabulary checks cannot see that.
    r2 = subprocess.run([sys.executable,
                         str(ROOT / "scripts" / "check_forced_arithmetic.py")]
                        + [str(f) for f in files], capture_output=True, text=True)
    out2 = (r2.stdout or "").strip()
    if "0 forced-arithmetic finding" in out2:
        print("[audit] forced arithmetic: none")
    else:
        print(out2)

    # 1c. self-containment (Pass 6168). BT1645 evaded 1b by recording multiplicities
    # while omitting the SRG parameters they follow from -- those sat in a sibling file.
    # A certificate that INTERPRETS numbers must carry what they are derived from.
    ENCODE = re.compile(r"encod|means|corresponds? to|is the", re.I)
    for f in files:
        if f.suffix != ".json":
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if ENCODE.search(txt):
            d2 = json.loads(txt)
            flat = json.dumps(d2).lower()
            has_params = all(k in flat for k in ('"v"', '"k"')) or "lambda" in flat
            if not has_params:
                print(f"[audit] {f.name}: interprets numbers but records no parameters "
                      f"they follow from -- not self-contained, cannot be audited alone")

    # 2. certificate triage
    for f in files:
        if f.suffix != ".json":
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[audit] {f.name}: unreadable JSON ({e})")
            hard_fail = True
            continue
        st = d.get("status")
        if st is None:
            continue
        if any(m in f.name for m in RELEASE_MARKERS):
            print(f"[audit] {f.name}: release artifact (status {st!r}) -- exempt")
        elif st in WITNESS_STATUSES:
            if st == "FAIL":
                print(f"[audit] {f.name}: witness status FAIL")
                hard_fail = True
        else:
            print(f"[audit] {f.name}: UNKNOWN status vocabulary {st!r} -- "
                  "classify before merge (this has bitten the ledger twice)")

    # 3. contradiction scan
    cert = certified_css_params()
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for n, k, d in RE_CSS.findall(txt):
            key = (int(n), int(k))
            if key in cert and int(d) not in cert[key]:
                print(f"[audit] {f.name}: [[{n},{k},{d}]] CONTRADICTS certified "
                      f"distances {sorted(cert[key])} for [[{n},{k},*]] -- "
                      "batch must name the certificate it supersedes")
                hard_fail = True

    # 4. ledger dry-run if paper touched
    if any(f.name == "w33_paper.tex" for f in files):
        r = subprocess.run([sys.executable,
                            str(ROOT / "scripts" / "check_claims_ledger.py")],
                           capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            hard_fail = True

    print(f"[audit] {'HARD FAIL' if hard_fail else 'intake clean'} "
          f"({len(files)} files)")
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
