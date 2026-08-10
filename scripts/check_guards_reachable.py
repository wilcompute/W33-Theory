#!/usr/bin/env python3
"""Audit the guards themselves: does each one exist, parse, run, and can it fire?  Pass 4708.

WHY THIS EXISTS
---------------
Pass 4692 found that `.pre-commit-config.yaml` had not parsed since 2026-07-27, so every
hook in it was dead for fourteen days, and that `check_rediscovery.py` -- the artifact
CLAUDE.md calls the core of the two-agent protocol -- was never registered at all.

Both failures share a shape that none of the existing checkers can see, because every
existing checker inspects the CORPUS.  Nothing inspected the CHECKERS.  CLAUDE.md's failure
mode 7 says a clean report from a broken checker is indistinguishable from a clean corpus;
the level above it is worse, because a checker that never runs produces no report at all,
and an absent report looks like nothing rather than like a problem.

WHAT IT CHECKS, IN INCREASING ORDER OF STRICTNESS
-------------------------------------------------
  1. CONFIG PARSES        -- the whole file loads as YAML. If not, every hook is dead.
  2. ENTRY RESOLVES       -- the script named by `entry:` exists on disk.
  3. SCRIPT IMPORTS       -- it compiles; a SyntaxError makes a hook silently useless.
  4. HAS A SELF-TEST      -- it accepts --selftest, per failure mode 7.
  5. SELF-TEST PASSES     -- and the self-test actually goes green.
  6. FILE PATTERN MATCHES -- its `files:` regex matches at least one real repo path. A hook
                             scoped to a directory that no longer exists is registered,
                             green, and unreachable.

Check 6 is the one that would have caught a whole class this repo has not looked for: a
guard can be live, correct, self-tested, and still never see a single file.

    py -3 scripts/check_guards_reachable.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".pre-commit-config.yaml"


def repo_paths():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.splitlines()


def main() -> int:
    print("=" * 78)
    print("Pass 4708 -- are the guards reachable?")
    print("=" * 78)

    try:
        import yaml
    except ImportError:
        print("  pyyaml not available")
        return 1

    print("\n  1. CONFIG PARSES")
    try:
        cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
        print("     OK -- the file loads. When it does not, EVERY hook below is dead and")
        print("     git prints 'pre-commit not found for this environment', which reads as")
        print("     a note about the environment. That is how fourteen days went unguarded.")
    except Exception as e:
        print(f"     FAIL -- {str(e).splitlines()[0]}")
        print("     EVERY HOOK IN THIS FILE IS DEAD.")
        return 1

    hooks = [h for r in cfg.get("repos", []) for h in r.get("hooks", [])]
    paths = repo_paths()
    print(f"\n  {len(hooks)} hooks registered, {len(paths)} tracked files\n")

    hdr = (f"  {'hook':32s} {'script':>6s} {'compiles':>9s} {'selftest':>9s} "
           f"{'passes':>7s} {'matches':>8s}")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))

    problems = []
    for h in hooks:
        hid = h.get("id", "?")
        entry = h.get("entry", "")
        # NOT just scripts/ -- the first version of this line looked only there and
        # reported pass-namespace-collision-guard as missing when it lives at
        # analysis/w33_pass1197_parallel_collision_guard.py. A reachability checker that
        # cannot find the script is itself the failure it is auditing for.
        m = re.search(r"((?:scripts|analysis|passes|pillars)/[\w./-]+\.py)", entry)
        script = ROOT / m.group(1) if m else None

        exists = bool(script and script.exists())
        compiles = selftest = passes = None
        if exists:
            r = subprocess.run([sys.executable, "-c",
                                f"import ast,pathlib;ast.parse(pathlib.Path(r'{script}')"
                                f".read_text(encoding='utf-8'))"],
                               capture_output=True, text=True)
            compiles = r.returncode == 0
            src = script.read_text(encoding="utf-8", errors="replace")
            selftest = "--selftest" in src or "selftest" in src
            if selftest and compiles:
                r2 = subprocess.run(["py", "-3", str(script), "--selftest"],
                                    cwd=ROOT, capture_output=True, text=True, timeout=300)
                passes = r2.returncode == 0 and "FAIL" not in r2.stdout

        pat = h.get("files")
        matches = None
        if pat:
            try:
                rx = re.compile(pat)
                matches = sum(1 for p in paths if rx.search(p))
            except re.error:
                matches = -1

        def sym(v):
            return "-" if v is None else ("yes" if v is True else
                                          ("NO" if v is False else str(v)))

        print(f"  {hid[:32]:32s} {sym(exists):>6s} {sym(compiles):>9s} "
              f"{sym(selftest):>9s} {sym(passes):>7s} "
              f"{'-' if matches is None else f'{matches:,}':>8s}")

        if exists is False:
            problems.append((hid, "entry script does not exist"))
        elif compiles is False:
            problems.append((hid, "script does not compile -- hook is silently useless"))
        elif selftest is False:
            problems.append((hid, "no self-test: a clean report proves nothing"))
        elif passes is False:
            problems.append((hid, "self-test FAILS"))
        if matches == 0:
            problems.append((hid, "files: pattern matches ZERO tracked paths -- "
                                  "registered, green, and unreachable"))
        elif matches == -1:
            problems.append((hid, "files: pattern is not a valid regex"))

    print(f"\n  {len(problems)} problems\n")
    for hid, why in problems:
        print(f"    {hid:32s} {why}")

    print("""
  THE COLUMN THAT MATTERS MOST IS THE LAST ONE. A hook whose `files:` pattern matches
  nothing is registered, reports green, and has never examined a single file -- the quietest
  possible failure, and one no amount of testing the checker itself would reveal. The
  'selftest' column is failure mode 7 as CLAUDE.md states it; the 'matches' column is the
  level above, where the check is fine and the wiring is not.

  WHAT THIS CANNOT SEE: whether a hook that matches files actually detects the faults in
  them. Reachability is necessary, not sufficient. A guard can be live, scoped correctly,
  self-tested, and still blind to the fault family that matters -- which is exactly what
  check_tex_insert_pitfalls.py was when it scanned 287 files and reported zero while two of
  them failed to compile.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
