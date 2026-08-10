#!/usr/bin/env python3
"""Find files whose name shadows a standard-library module.  Pass 4792.

WHY THIS EXISTS
---------------
Twice now, in this repository, a file has taken a stdlib name and broken imports somewhere
unrelated:

  * `scripts/inspect.py` shadowed the stdlib `inspect` and had to be renamed to
    `scripts/_debug_print_lines.py`.  That one is recorded in the project notes.
  * A scratch `bisect.py` made `igraph` unimportable at Pass 4782 -- because `random`
    imports `bisect`, `tempfile` imports `random`, and `igraph` imports `tempfile`.  The
    error surfaced four levels away from the cause and named a module nobody had touched.

The failure is nasty in a specific way: it is INVISIBLE UNTIL SOMETHING ELSE IMPORTS.  A
shadowing file sits harmlessly for months, then breaks an unrelated tool the first time
that tool is run from the wrong directory.  The traceback points at the victim, not the
cause.

WHAT IT DOES
------------
Lists every `*.py` whose stem is a top-level stdlib module name, ranked by how dangerous the
shadow is: modules imported by the interpreter's own startup path or by very common
libraries are worse than obscure ones.

Directories on sys.path at run time are what matter, so this reports on the repo's
importable roots and flags scratch directories separately -- a shadow in a scratch folder
only bites when something is run from there, which is exactly what happened.

    py -3 scripts/check_stdlib_shadow.py --selftest
    py -3 scripts/check_stdlib_shadow.py [paths...]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Modules whose shadowing breaks things far from the shadow, because they sit on the
# import path of the interpreter or of ubiquitous third-party packages.
HIGH_RISK = {
    "abc", "bisect", "collections", "copy", "enum", "functools", "io", "inspect",
    "itertools", "json", "keyword", "logging", "math", "operator", "os", "pathlib",
    "random", "re", "select", "socket", "string", "struct", "subprocess", "sys",
    "tempfile", "time", "types", "typing", "warnings", "weakref",
}

SCRATCHY = ("scratchpad", "tmp", "temp", "sandbox", "scratch")


def stdlib_names() -> set[str]:
    names = set(getattr(sys, "stdlib_module_names", ()))
    return {n for n in names if not n.startswith("_")}


def scan(paths) -> list[dict]:
    std = stdlib_names()
    out = []
    for p in paths:
        if p.suffix != ".py":
            continue
        stem = p.stem
        if stem not in std:
            continue
        rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else str(p)
        out.append({
            "file": rel,
            "module": stem,
            "risk": "HIGH" if stem in HIGH_RISK else "low",
            "scratch": any(s in rel.lower() for s in SCRATCHY),
        })
    return out


def selftest() -> int:
    import shutil
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="shadow_"))
    cases = [("planted: bisect.py", "bisect.py", True),
             ("planted: inspect.py", "inspect.py", True),
             ("clean: ordinary name", "w33_pass1234_thing.py", False),
             ("clean: near-miss", "collections_helper.py", False),
             ("clean: not python", "json.md", False)]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, fn, want in cases:
        f = tmp / fn
        f.write_text("# test\n", encoding="utf-8")
        got = bool(scan([f]))
        good = got == want
        ok &= good
        print(f"    {name:26s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
        f.unlink()
    print("""
  THE NEAR-MISS CASE IS THE ONE THAT MATTERS. `collections_helper.py` contains a stdlib
  name and shadows nothing; a checker matching substrings would flag every file in the
  repository with a common word in it. The shadow is exact-stem-only, because that is what
  Python's import machinery actually compares.

  ITS LIMIT: it reports NAMES, not reachability. Whether a given shadow bites depends on
  sys.path at run time, which depends on the working directory of whatever is being run --
  the bisect.py that broke igraph lived in a scratch folder and was harmless until a script
  was executed from there.""")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    if a.paths:
        paths = [Path(p) for p in a.paths]
    else:
        paths = [p for d in ("scripts", "analysis", "tools", "tests", "lib", "pillars")
                 for p in (ROOT / d).rglob("*.py") if (ROOT / d).is_dir()]
        paths += list(ROOT.glob("*.py"))

    hits = scan(paths)
    high = [h for h in hits if h["risk"] == "HIGH"]
    for h in sorted(hits, key=lambda x: (x["risk"] != "HIGH", x["file"])):
        tag = " [scratch]" if h["scratch"] else ""
        print(f"  {h['risk']:4s} {h['file']}  shadows stdlib '{h['module']}'{tag}")
    print(f"\n  {len(hits)} shadowing files, {len(high)} high-risk")
    if not hits:
        print("  (zero means nothing unless --selftest passes; run it)")
    return 0        # advisory


if __name__ == "__main__":
    raise SystemExit(main())
