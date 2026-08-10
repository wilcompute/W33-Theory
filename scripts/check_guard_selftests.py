#!/usr/bin/env python3
"""Run every registered guard's own self-test.  Pass 4726.

WHY THIS EXISTS
---------------
Pass 4708 audited the guards and found 9 of 12 have no self-test at all, including
`certificate-digests`, `novelty-claims` and `rediscovery`.  CLAUDE.md's failure mode 7 says
a clean report from a broken checker is indistinguishable from a clean corpus -- so a guard
without a planted fault it must detect is reporting a number nobody can interpret.

But a self-test that only runs when someone remembers to type `--selftest` is the next thing
to rot, and the evidence is already here: `check_smin_formula.py` shipped inside an
unparseable YAML scalar and had never executed once in the fourteen days it was registered.

WHAT IT DOES
------------
Reads `.pre-commit-config.yaml`, finds each hook's script, and for every script that accepts
`--selftest`, runs it and fails if it does not go green.  Scripts with no self-test are
REPORTED, not failed -- turning that into an error today would block every commit until nine
checkers are retrofitted, which trains `--no-verify`, which is the outcome CLAUDE.md warns
about for the rediscovery hook.

    py -3 scripts/check_guard_selftests.py [--strict]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".pre-commit-config.yaml"
SCRIPT = re.compile(r"((?:scripts|analysis|passes|pillars)/[\w./-]+\.py)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="also fail on guards that have no self-test")
    ap.add_argument("files", nargs="*")           # pre-commit passes filenames; ignored
    a = ap.parse_args()

    try:
        import yaml
        cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  .pre-commit-config.yaml does not parse: {str(e).splitlines()[0]}")
        print("  EVERY HOOK IS DEAD. This is how fourteen days went unguarded.")
        return 1

    hooks = [h for r in cfg.get("repos", []) for h in r.get("hooks", [])]
    tested = missing = failed = 0
    for h in hooks:
        m = SCRIPT.search(h.get("entry", ""))
        if not m:
            continue
        p = ROOT / m.group(1)
        if not p.exists():
            print(f"  {h['id']:32s} SCRIPT MISSING {m.group(1)}")
            failed += 1
            continue
        if "--selftest" not in p.read_text(encoding="utf-8", errors="replace"):
            missing += 1
            print(f"  {h['id']:32s} no self-test")
            continue
        r = subprocess.run(["py", "-3", str(p), "--selftest"], cwd=ROOT,
                           capture_output=True, text=True, timeout=600)
        green = r.returncode == 0 and "FAIL" not in r.stdout
        tested += 1
        if not green:
            failed += 1
            print(f"  {h['id']:32s} SELF-TEST FAILS")
            for line in (r.stdout or r.stderr).splitlines():
                if "FAIL" in line:
                    print(f"      {line.strip()[:90]}")
        else:
            print(f"  {h['id']:32s} self-test green")

    print(f"\n  {tested} self-tested, {missing} without a self-test, {failed} failing")
    if missing:
        print("""
  The guards without a self-test report numbers nobody can interpret. A zero from a checker
  that has never been shown to detect anything is not evidence of a clean corpus -- it is
  the absence of evidence, formatted to look like the presence of it.""")
    return 1 if (failed or (a.strict and missing)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
