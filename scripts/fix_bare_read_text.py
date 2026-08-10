#!/usr/bin/env python3
"""Give every bare .read_text() / .write_text() an explicit encoding.  Pass 4681.

WHY THIS EXISTS
---------------
Pass 4570 traced a failing verifier to one line:

    CERT = json.loads(OUT.read_text())      # no encoding

On Windows `read_text()` defaults to the locale codec (cp1252 here), so a certificate's
correct UTF-8 bytes `\\xc2\\xb7` decode into TWO characters instead of one.  The pass mangled
its own certificate on read, hashed the mangled string, and failed against a correct stored
digest.  It would have passed on Linux CI and failed on a Windows desktop -- the worst place
to leave a fault in a verifier, because the machine that shows it is not the machine that
gates the commit.

630 of 3,627 files under `analysis/` carried the same unexploded call.

WHAT IT CHANGES, AND WHAT IT REFUSES TO
---------------------------------------
Only the encoding argument, and only where none is present:

    p.read_text()            -> p.read_text(encoding="utf-8")
    p.write_text(x)          -> p.write_text(x, encoding="utf-8")
    open(p)                  -> untouched; `open` has other modes and this is not a
                                mechanical rewrite there

A file is rewritten only if it still PARSES afterwards; anything that fails to compile is
restored and reported.  Nothing else in the file is touched, so the diff is auditable
line-by-line.

    py -3 scripts/fix_bare_read_text.py            # report only
    py -3 scripts/fix_bare_read_text.py --apply
    py -3 scripts/fix_bare_read_text.py --selftest
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# NOTE: analysis/ is deliberately EXCLUDED by default. A parallel agent works there
# continuously and a 1,500-file rewrite would collide with its in-flight edits. Run
# with --dirs analysis when that lane is quiet; the fix is identical.
DIRS = ["scripts", "tests", "pillars", "proofs", "exploration", "lib"]

BARE_READ = re.compile(r"\.read_text\(\s*\)")
BARE_WRITE = re.compile(r"\.write_text\(\s*([^),]+?)\s*\)")


def fix_text(src: str) -> tuple[str, int]:
    n = 0
    out, k = BARE_READ.subn('.read_text(encoding="utf-8")', src)
    n += k
    # only rewrite write_text calls with exactly one simple argument
    def w(m):
        nonlocal n
        arg = m.group(1)
        if "encoding" in arg or "=" in arg.split("(")[0]:
            return m.group(0)
        n += 1
        return f'.write_text({arg}, encoding="utf-8")'
    out = BARE_WRITE.sub(w, out)
    return out, n


def selftest() -> int:
    cases = [
        ("bare read", "x = p.read_text()", 'x = p.read_text(encoding="utf-8")', 1),
        ("already encoded", 'p.read_text(encoding="utf-8")',
         'p.read_text(encoding="utf-8")', 0),
        ("read with errors arg", 'p.read_text(encoding="utf-8", errors="replace")',
         'p.read_text(encoding="utf-8", errors="replace")', 0),
        ("bare write", "p.write_text(s)", 'p.write_text(s, encoding="utf-8")', 1),
        ("write already encoded", 'p.write_text(s, encoding="utf-8")',
         'p.write_text(s, encoding="utf-8")', 0),
        ("open() untouched", "f = open(p)", "f = open(p)", 0),
    ]
    ok = True
    print("  selftest")
    for name, src, want, wantn in cases:
        got, n = fix_text(src)
        good = got == want and n == wantn
        ok &= good
        print(f"    {name:26s} n={n} {'PASS' if good else 'FAIL'}"
              + ("" if good else f"   got {got!r}"))
    print("""
  The 'already encoded' cases are the ones that matter. A rewrite that double-applies
  would produce read_text(encoding="utf-8", encoding="utf-8") -- a syntax error in every
  file it touched, which is a loud failure, but the 'errors=' case would silently drop an
  argument and that would not be loud at all.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dirs", nargs="*", default=None,
                    help="override the directory list (e.g. --dirs analysis)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    touched = total = broken = 0
    failures = []
    for d in (a.dirs or DIRS):
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in base.rglob("*.py"):
            try:
                src = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            new, n = fix_text(src)
            if not n:
                continue
            total += n
            touched += 1
            if not a.apply:
                continue
            try:
                ast.parse(new)
            except SyntaxError as e:
                broken += 1
                failures.append((p.name, str(e)[:60]))
                continue
            p.write_text(new, encoding="utf-8")

    print(f"  files with a bare call : {touched}")
    print(f"  call sites             : {total}")
    if a.apply:
        print(f"  rewritten              : {touched - broken}")
        print(f"  skipped (would break)  : {broken}")
        for n, e in failures[:8]:
            print(f"    {n[:52]:52s} {e}")
    else:
        print("\n  (report only -- pass --apply)")
    print("""
  A bare read_text() is not a style issue on this project. It is a
  platform-dependent correctness bug in anything that hashes what it reads, and it
  fails on the developer's machine while passing in CI.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
