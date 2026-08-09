#!/usr/bin/env python3
"""Re-run each pass and check its certificate comes back BYTE-IDENTICAL.

WHY THIS EXISTS
---------------
`scripts/check_certificates.py` (Pass 2482) checks that a certificate's stored digest
matches its own bytes.  That catches the certificate whose digest could never have been
right.  It does NOT catch the certificate that no longer matches the script that made it --
because it never re-runs the script.  A pass that was edited after its certificate was
written, or that depends on a file that has since changed, produces a certificate which is
internally consistent and externally stale, and every existing check passes it.

That is failure mode 7 in `CLAUDE.md`: a clean report from a check that cannot see the
fault.  The only way to see this one is to run the thing.

WHAT IT DOES
------------
For each pass script given (default: `analysis/w33_pass*.py`), find the `data/*.json` it
writes, snapshot those bytes, re-run the script in a scratch copy of `data/`, and compare.
Verdicts:

    REPRODUCES   re-run produced identical bytes
    DRIFTED      re-run produced DIFFERENT bytes -- the committed certificate is stale
    FAILED       the script no longer runs
    TIMEOUT      the script exceeds the budget (not a fault; report and move on)
    NO-CERT      the script writes no certificate

PLANTED FAULT (failure mode 7 says every check ships with one)
--------------------------------------------------------------
`--selftest` writes a tiny pass that emits a certificate, verifies it REPRODUCES, then
corrupts the stored certificate on disk and verifies the checker reports DRIFTED.  A
checker that cannot fail is not evidence.

    py -3 scripts/check_certificates_regenerate.py --selftest
    py -3 scripts/check_certificates_regenerate.py analysis/w33_pass43*.py
"""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
# Pass 4461: this ORIGINALLY matched only PART_*.json and therefore missed 746 of
# the 878 passes that do emit a certificate -- the dominant convention here is
# w33_passNNNN_*.json.  Pass 4424's headline "1015 emit no certificate" was an
# artifact of this regex and is retracted at Pass 4461.
WRITES = re.compile(r"""["'](?:data/)?([A-Za-z0-9_]+\.json)["']""")


def certificates_of(script: Path) -> list[str]:
    src = script.read_text(encoding="utf-8", errors="replace")
    return sorted(set(WRITES.findall(src)))


def check(script: Path, budget: int) -> tuple[str, str]:
    names = certificates_of(script)
    if not names:
        return "NO-CERT", ""
    present = [n for n in names if (DATA / n).exists()]
    if not present:
        return "NO-CERT", "declared but never written"

    with tempfile.TemporaryDirectory() as td:
        keep = Path(td)
        for n in present:
            shutil.copy2(DATA / n, keep / n)
        try:
            r = subprocess.run([sys.executable, str(script)], cwd=ROOT,
                               capture_output=True, text=True, timeout=budget)
        except subprocess.TimeoutExpired:
            for n in present:                       # restore, we may have half-written
                shutil.copy2(keep / n, DATA / n)
            return "TIMEOUT", f"> {budget}s"
        if r.returncode != 0:
            for n in present:
                shutil.copy2(keep / n, DATA / n)
            tail = (r.stderr or r.stdout).strip().splitlines()
            return "FAILED", (tail[-1][:70] if tail else f"exit {r.returncode}")

        drifted = [n for n in present if not filecmp.cmp(keep / n, DATA / n, shallow=False)]
        for n in present:                            # never leave the tree modified
            shutil.copy2(keep / n, DATA / n)
        if drifted:
            return "DRIFTED", ", ".join(drifted)[:70]
        return "REPRODUCES", f"{len(present)} cert(s)"


def selftest() -> int:
    print("selftest: a checker that cannot fail is not evidence")
    tmp_script = ROOT / "analysis" / "_selftest_regen_pass.py"
    cert = DATA / "PART_SELFTEST_REGEN.json"
    tmp_script.write_text(
        "import json, pathlib\n"
        "p = pathlib.Path(__file__).resolve().parents[1] / 'data' /"
        " 'PART_SELFTEST_REGEN.json'\n"
        "out = {'value': 42, 'schema': 'selftest.v1'}\n"
        "p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True)"
        " + '\\n', encoding='utf-8')\n", encoding="utf-8")
    try:
        subprocess.run([sys.executable, str(tmp_script)], cwd=ROOT, check=True,
                       capture_output=True)
        v1, _ = check(tmp_script, 60)
        print(f"  clean certificate            -> {v1}")
        # plant the fault: corrupt the committed bytes
        cert.write_text('{\n  "schema": "selftest.v1",\n  "value": 43\n}\n',
                        encoding="utf-8")
        v2, _ = check(tmp_script, 60)
        print(f"  certificate corrupted on disk -> {v2}")
        ok = v1 == "REPRODUCES" and v2 == "DRIFTED"
        print(f"  selftest: {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    finally:
        tmp_script.unlink(missing_ok=True)
        cert.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts", nargs="*", help="pass scripts (default analysis/w33_pass*)")
    ap.add_argument("--budget", type=int, default=120, help="seconds per script")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 on DRIFTED or FAILED")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    paths = ([Path(s) for s in a.scripts] if a.scripts
             else sorted((ROOT / "analysis").glob("w33_pass*.py")))
    tally: dict[str, int] = {}
    bad: list[tuple[str, str, str]] = []
    print(f"{'verdict':11s} {'script':58s} note")
    for p in paths:
        v, note = check(p if p.is_absolute() else ROOT / p, a.budget)
        tally[v] = tally.get(v, 0) + 1
        if v != "NO-CERT":
            print(f"{v:11s} {p.name[:58]:58s} {note}")
        if v in ("DRIFTED", "FAILED"):
            bad.append((v, p.name, note))

    print("\n  " + "  ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    if bad:
        print("\n  needs attention:")
        for v, n, note in bad:
            print(f"    {v:10s} {n}  {note}")
    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
